#!/usr/bin/env python3
"""Run GPT Image 2 i2i through the Kie async HTTP API.

The cover pipeline already prepares `cover/quad-mcp-batch.json` with the exact
prompt/input_urls/aspect_ratio/resolution payload. This script reuses that
batch, creates a Kie job, polls for completion, and writes the same
`cover/quad-mcp-result.json` shape consumed by `excalibur_blog_quad_apply.py`.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_CREATE_URL = "https://api.kie.ai/api/v1/jobs/createTask"
DEFAULT_RECORD_URL = "https://api.kie.ai/api/v1/jobs/recordInfo"
DEFAULT_MODEL = "gpt-image-2-image-to-image"
DEFAULT_API_KEY_ENV = "KIE_API_KEY"
DEFAULT_POLL_INTERVAL_SECONDS = 15
DEFAULT_MAX_WAIT_SECONDS = 900


class KieApiError(RuntimeError):
    """Raised for API or response-shape failures."""


def project_root() -> Path:
    env_root = os.environ.get("EXCALIBUR_PROJECT_ROOT", "").strip()
    if env_root:
        return Path(env_root)
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve_path(root: Path, article_dir_arg: str, path_arg: str) -> Path:
    article_dir = Path(article_dir_arg)
    if not article_dir.is_absolute():
        article_dir = root / article_dir
    path = Path(path_arg)
    if not path.is_absolute():
        path = article_dir / path
    return path


def http_json(method: str, url: str, api_key: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = None
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise KieApiError(f"Kie API HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise KieApiError(f"Kie API network error: {exc.reason}") from exc

    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise KieApiError(f"Kie API returned non-JSON response: {body[:500]}") from exc
    if not isinstance(parsed, dict):
        raise KieApiError("Kie API returned a non-object JSON response")
    return parsed


def require_success(response: dict[str, Any], action: str) -> None:
    if response.get("code") == 200:
        return
    msg = response.get("msg") or "unknown error"
    raise KieApiError(f"Kie API {action} failed: code={response.get('code')} msg={msg}")


def batch_mcp_args(batch_path: Path) -> dict[str, Any]:
    batch = load_json(batch_path)
    jobs = batch.get("jobs")
    if not isinstance(jobs, list) or len(jobs) != 1:
        raise KieApiError(f"Expected exactly one job in {batch_path}")
    job = jobs[0]
    if not isinstance(job, dict):
        raise KieApiError(f"Invalid job entry in {batch_path}")
    args = job.get("mcp_args")
    if not isinstance(args, dict):
        raise KieApiError(f"Missing jobs[0].mcp_args in {batch_path}")

    prompt = str(args.get("prompt") or "").strip()
    input_urls = args.get("input_urls")
    if not prompt:
        raise KieApiError("Missing prompt in jobs[0].mcp_args")
    if not isinstance(input_urls, list) or not input_urls:
        raise KieApiError("Missing non-empty input_urls in jobs[0].mcp_args")
    return {
        "prompt": prompt,
        "input_urls": input_urls,
        "aspect_ratio": args.get("aspect_ratio") or "auto",
        "resolution": args.get("resolution") or "1K",
    }


def create_task(
    *,
    create_url: str,
    api_key: str,
    model: str,
    image_input: dict[str, Any],
    callback_url: str,
) -> tuple[str, dict[str, Any]]:
    payload: dict[str, Any] = {
        "model": model,
        "input": image_input,
    }
    if callback_url:
        payload["callBackUrl"] = callback_url
    response = http_json("POST", create_url, api_key, payload)
    require_success(response, "createTask")
    task_id = ((response.get("data") or {}).get("taskId") or "").strip()
    if not task_id:
        raise KieApiError(f"Kie API createTask response missing data.taskId: {response}")
    return task_id, response


def query_task(*, record_url: str, api_key: str, task_id: str) -> dict[str, Any]:
    query = urllib.parse.urlencode({"taskId": task_id})
    separator = "&" if "?" in record_url else "?"
    response = http_json("GET", f"{record_url}{separator}{query}", api_key)
    require_success(response, "recordInfo")
    data = response.get("data")
    if not isinstance(data, dict):
        raise KieApiError(f"Kie API recordInfo response missing data object: {response}")
    return data


def parse_result_urls(result_json: Any) -> list[str]:
    if not result_json:
        return []
    if isinstance(result_json, str):
        try:
            parsed = json.loads(result_json)
        except json.JSONDecodeError as exc:
            raise KieApiError(f"Kie resultJson is not valid JSON: {result_json[:500]}") from exc
    elif isinstance(result_json, dict):
        parsed = result_json
    else:
        raise KieApiError("Kie resultJson has unsupported type")
    urls = parsed.get("resultUrls") or parsed.get("result_urls") or []
    if not isinstance(urls, list):
        raise KieApiError("Kie resultJson resultUrls is not an array")
    return [str(url).strip() for url in urls if str(url).strip()]


def poll_until_result(
    *,
    record_url: str,
    api_key: str,
    task_id: str,
    poll_interval: int,
    max_wait: int,
) -> dict[str, Any]:
    started = time.monotonic()
    last_state = ""
    while True:
        data = query_task(record_url=record_url, api_key=api_key, task_id=task_id)
        state = str(data.get("state") or "").strip().lower()
        if state != last_state:
            print(f"Kie task {task_id}: state={state or 'unknown'}")
            last_state = state

        if state == "success":
            urls = parse_result_urls(data.get("resultJson"))
            if not urls:
                raise KieApiError("Kie task succeeded but resultJson has no resultUrls")
            return data
        if state == "fail":
            fail_code = data.get("failCode")
            fail_msg = data.get("failMsg")
            raise KieApiError(f"Kie task failed: failCode={fail_code} failMsg={fail_msg}")

        elapsed = time.monotonic() - started
        if elapsed >= max_wait:
            raise KieApiError(f"Kie task did not finish within {max_wait} seconds; task_id={task_id}")
        time.sleep(min(poll_interval, max(1, int(max_wait - elapsed))))


def result_record(task_data: dict[str, Any], task_id: str) -> dict[str, Any]:
    urls = parse_result_urls(task_data.get("resultJson"))
    url = urls[0]
    return {
        "url": url,
        "urls": urls,
        "task_id": task_id,
        "source": "kie-api",
        "model": task_data.get("model") or DEFAULT_MODEL,
        "state": task_data.get("state"),
        "costTime": task_data.get("costTime"),
        "completeTime": task_data.get("completeTime"),
        "createTime": task_data.get("createTime"),
    }


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Create/poll a Kie GPT Image 2 i2i job from cover/quad-mcp-batch.json"
    )
    ap.add_argument("--article-dir", required=True)
    ap.add_argument("--batch", default="cover/quad-mcp-batch.json")
    ap.add_argument("--result", default="cover/quad-mcp-result.json")
    ap.add_argument("--task-record", default="cover/kie-image-task.json")
    ap.add_argument("--api-key-env", default=DEFAULT_API_KEY_ENV)
    ap.add_argument("--create-url", default=DEFAULT_CREATE_URL)
    ap.add_argument("--record-url", default=DEFAULT_RECORD_URL)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--callback-url", default=os.environ.get("KIE_CALLBACK_URL", "").strip())
    ap.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL_SECONDS)
    ap.add_argument("--max-wait", type=int, default=DEFAULT_MAX_WAIT_SECONDS)
    ap.add_argument("--task-id", default="", help="Poll an existing Kie task instead of creating a new one")
    ap.add_argument("--create-only", action="store_true", help="Create task, write task record, and exit")
    ap.add_argument("--dry-run", action="store_true", help="Validate batch and print sanitized create payload")
    args = ap.parse_args()

    root = project_root()
    batch_path = resolve_path(root, args.article_dir, args.batch)
    result_path = resolve_path(root, args.article_dir, args.result)
    task_record_path = resolve_path(root, args.article_dir, args.task_record)

    try:
        image_input = batch_mcp_args(batch_path)
        create_payload = {
            "model": args.model,
            "input": image_input,
        }
        if args.callback_url:
            create_payload["callBackUrl"] = args.callback_url

        if args.dry_run:
            print(json.dumps({"create_url": args.create_url, "payload": create_payload}, ensure_ascii=False, indent=2))
            return 0

        api_key = os.environ.get(args.api_key_env, "").strip()
        if not api_key:
            print(
                f"❌ KIE API BLOCKER: set {args.api_key_env} in Cloud Secrets/env; the key must not be committed or printed.",
                file=sys.stderr,
            )
            return 1

        task_id = args.task_id.strip()
        create_response: dict[str, Any] | None = None
        if not task_id:
            task_id, create_response = create_task(
                create_url=args.create_url,
                api_key=api_key,
                model=args.model,
                image_input=image_input,
                callback_url=args.callback_url,
            )
            save_json(
                task_record_path,
                {
                    "task_id": task_id,
                    "source": "kie-api",
                    "model": args.model,
                    "state": "created",
                    "create_response": create_response,
                    "created_at_epoch": int(time.time()),
                },
            )
            print(f"Kie task created: task_id={task_id}")

        if args.create_only:
            print(f"OK task_record={task_record_path}")
            return 0

        task_data = poll_until_result(
            record_url=args.record_url,
            api_key=api_key,
            task_id=task_id,
            poll_interval=max(1, args.poll_interval),
            max_wait=max(1, args.max_wait),
        )
        record = result_record(task_data, task_id)
        save_json(result_path, record)
        save_json(
            task_record_path,
            {
                "task_id": task_id,
                "source": "kie-api",
                "model": task_data.get("model") or args.model,
                "state": task_data.get("state"),
                "result_path": str(result_path.relative_to(root) if result_path.is_relative_to(root) else result_path),
                "updated_at_epoch": int(time.time()),
            },
        )
        print(f"OK url={record['url']}")
        print(f"OK result={result_path}")
        return 0
    except KieApiError as exc:
        print(f"❌ KIE API BLOCKER: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
