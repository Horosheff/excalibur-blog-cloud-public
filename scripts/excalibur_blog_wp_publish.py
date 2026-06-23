#!/usr/bin/env python3
"""Publish one Excalibur blog article to WordPress (SFTP bootstrap)."""
from __future__ import annotations

import argparse
import base64
import io
import json
import os
import sys
import urllib.request
from pathlib import Path
from typing import Any

from asset_download import download_url_bytes
from excalibur_repo_paths import repo_relative
from image_validate import sniff_image_format, validate_image_file


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


PUBLISH_ENV_KEYS = {
    "PUBLIC_SITE_URL",
    "WP_HOME",
    "WP_SITE_URL",
    "FTP_HOST",
    "FTP_PORT",
    "FTP_USER",
    "FTP_PASS",
    "FTP_PASSWORD",
    "FTP_ROOT",
    "FTP_PATH",
    "SSH_HOST",
    "SSH_PORT",
    "SSH_USER",
    "SSH_PASS",
    "SSH_PASSWORD",
    "SSH_ROOT",
    "EXCALIBUR_BLOG_ALLOW_PUBLISH",
}


def _read_env_file(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not path.is_file():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


def load_env(root: Path) -> dict[str, str]:
    env = _read_env_file(root / "memory/site.env.local")
    for key in PUBLISH_ENV_KEYS:
        value = os.environ.get(key)
        if value:
            env[key] = value
    if not env.get("FTP_PASS") and env.get("FTP_PASSWORD"):
        env["FTP_PASS"] = env["FTP_PASSWORD"]
    if not env.get("SSH_PASS") and env.get("SSH_PASSWORD"):
        env["SSH_PASS"] = env["SSH_PASSWORD"]
    if not env.get("FTP_HOST") and env.get("SSH_HOST"):
        env["FTP_HOST"] = env["SSH_HOST"]
    if not env.get("FTP_USER") and env.get("SSH_USER"):
        env["FTP_USER"] = env["SSH_USER"]
    if not env.get("FTP_PASS") and env.get("SSH_PASS"):
        env["FTP_PASS"] = env["SSH_PASS"]
    if not env.get("SSH_HOST"):
        env["SSH_HOST"] = env.get("FTP_HOST", "")
    if not env.get("SSH_USER"):
        env["SSH_USER"] = env.get("FTP_USER", "")
    if not env.get("SSH_PASS"):
        env["SSH_PASS"] = env.get("FTP_PASS", "")
    return env


def validate_publish_env(env: dict[str, str]) -> list[str]:
    missing: list[str] = []
    if not (env.get("SSH_HOST") or env.get("FTP_HOST")):
        missing.append("SSH_HOST or FTP_HOST")
    if not (env.get("SSH_USER") or env.get("FTP_USER")):
        missing.append("SSH_USER or FTP_USER")
    if not (env.get("SSH_PASS") or env.get("FTP_PASS") or env.get("SSH_PASSWORD") or env.get("FTP_PASSWORD")):
        missing.append("SSH_PASS/SSH_PASSWORD or FTP_PASS/FTP_PASSWORD")
    if not (env.get("PUBLIC_SITE_URL") or env.get("WP_HOME") or env.get("WP_SITE_URL")):
        missing.append("PUBLIC_SITE_URL")
    return missing


def publish_env_check_report(env: dict[str, str]) -> dict[str, object]:
    root_label = sftp_root_label(env)
    return {
        "allow_publish": env.get("EXCALIBUR_BLOG_ALLOW_PUBLISH", "").strip().lower() == "yes",
        "public_site_url_configured": bool(env.get("PUBLIC_SITE_URL") or env.get("WP_HOME") or env.get("WP_SITE_URL")),
        "sftp": {
            "host_configured": bool(env.get("SSH_HOST") or env.get("FTP_HOST")),
            "user_configured": bool(env.get("SSH_USER") or env.get("FTP_USER")),
            "password_configured": bool(
                env.get("SSH_PASS")
                or env.get("FTP_PASS")
                or env.get("SSH_PASSWORD")
                or env.get("FTP_PASSWORD")
            ),
            "root": root_label,
            "dot_fallback_enabled": root_label == "configured-non-dot",
        },
        "missing": validate_publish_env(env),
    }


def normalize_post_title(title: str) -> str:
    """Keep SEO lower-case queries out of the visible WordPress title."""
    title = " ".join(str(title or "").split())
    if not title:
        return title
    return title[0].upper() + title[1:]


def cover_url_from_registry(registry_path: Path) -> str:
    if not registry_path.is_file():
        return ""
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    for key in ("transparent_url", "remote_packaged_url", "packaged_url", "attachment_url", "url", "cover_url", "image_url"):
        value = str(registry.get(key) or "").strip()
        if value.startswith(("http://", "https://")):
            return value
    return ""


def normalize_cover_png(cover_path: Path, registry_path: Path, root: Path) -> dict[str, object]:
    evidence: dict[str, object] = {
        "path": repo_relative(cover_path, root),
        "source": "existing_file",
        "decode_verified": False,
    }
    errors = validate_image_file(cover_path) if cover_path.is_file() else [f"missing cover file: {cover_path}"]

    if errors:
        remote_url = cover_url_from_registry(registry_path)
        if not remote_url:
            raise RuntimeError("; ".join(errors) + "; no remote cover URL in cover-registry.json")
        data, remote_evidence = download_url_bytes(remote_url, timeout=20, retries=6, chunk_size=8 * 1024)
        detected = sniff_image_format(data)
        if not detected:
            raise RuntimeError("downloaded cover bytes are not a known image format")
        cover_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = cover_path.with_name(f"{cover_path.stem}.tmp{cover_path.suffix}")
        try:
            if detected == "png":
                tmp.write_bytes(data)
            elif detected in {"webp", "jpeg", "gif"}:
                from PIL import Image

                with Image.open(io.BytesIO(data)) as image:
                    image.save(tmp, format="PNG")
            else:
                raise RuntimeError(f"unsupported cover format: {detected}")
            cover_errors = validate_image_file(tmp)
            if cover_errors:
                raise RuntimeError("; ".join(cover_errors))
            tmp.replace(cover_path)
        finally:
            tmp.unlink(missing_ok=True)
        evidence.update(
            {
                "source": "range_download",
                "remote_url": remote_url,
                "remote_content_type": remote_evidence.get("content_type"),
                "remote_content_range": remote_evidence.get("content_range"),
                "remote_signature_hex": remote_evidence.get("signature_hex"),
                "downloaded_bytes": len(data),
                "detected_remote_format": detected,
            }
        )

    final_errors = validate_image_file(cover_path)
    if final_errors:
        raise RuntimeError("; ".join(final_errors))
    if sniff_image_format(cover_path.read_bytes()) != "png":
        raise RuntimeError(f"cover must be a real PNG after normalization: {cover_path}")

    evidence.update(
        {
            "bytes": cover_path.stat().st_size,
            "detected_format": "png",
            "decode_verified": True,
        }
    )
    return evidence


def load_article(article_dir: Path) -> dict:
    meta_path = article_dir / "article.meta.json"
    html_path = article_dir / "article.html"
    if not meta_path.is_file() or not html_path.is_file():
        raise FileNotFoundError("article.meta.json and article.html required")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta_ab = meta.get("meta_ab") or {}
    content = html_path.read_text(encoding="utf-8").strip()
    cover_path = article_dir / "cover" / "cover.png"
    schema_path = article_dir / "schema.jsonld"
    cover_b64 = ""
    cover_evidence: dict[str, object] = {}
    cover_reg = article_dir / "cover" / "cover-registry.json"
    if cover_path.is_file():
        cover_evidence = normalize_cover_png(cover_path, cover_reg, project_root())
        cover_b64 = base64.b64encode(cover_path.read_bytes()).decode("ascii")
    schema_raw = ""
    if schema_path.is_file():
        schema_raw = schema_path.read_text(encoding="utf-8").strip()
    cover_alt = meta.get("cover_alt") or meta.get("cover_alt_text") or ""
    if cover_reg.is_file():
        reg = json.loads(cover_reg.read_text(encoding="utf-8"))
        cover_alt = cover_alt or reg.get("cover_alt_text", "")

    import re
    img_srcs = re.findall(r'<img\s+[^>]*src=["\']([^"\']+)["\']', content)
    inline_images = []
    for src in img_srcs:
        if not src.startswith(("http://", "https://", "data:")):
            local_path = article_dir / src
            if local_path.is_file():
                img_bytes = local_path.read_bytes()
                b64_data = base64.b64encode(img_bytes).decode("ascii")
                inline_images.append({
                    "src": src,
                    "b64": b64_data,
                    "filename": local_path.name
                })

    wp_post_id = meta.get("wp_post_id") or meta.get("post_id")
    result_path = article_dir / "wp-publish-result.json"
    if not wp_post_id and result_path.is_file():
        try:
            prev = json.loads(result_path.read_text(encoding="utf-8"))
            wp_post_id = prev.get("post_id")
        except json.JSONDecodeError:
            wp_post_id = None

    return {
        "slug": meta["slug"],
        "post_id": int(wp_post_id) if wp_post_id else 0,
        "title": normalize_post_title(
            meta.get("title")
            or meta.get("h1")
            or meta_ab.get("title_aeo")
            or meta_ab.get("title_seo")
            or meta_ab.get("title_ctr")
            or meta["slug"]
        ),
        "excerpt": meta.get("description")
        or meta_ab.get("description_seo")
        or meta_ab.get("description_ctr")
        or meta_ab.get("description_aeo")
        or "",
        "content": content,
        "cover_b64": cover_b64,
        "cover_evidence": cover_evidence,
        "cover_alt": cover_alt,
        "schema_jsonld": schema_raw,
        "topic_id": meta.get("topic_id", ""),
        "inline_images": inline_images,
    }


def build_php(payload: dict) -> str:
    b64 = base64.b64encode(json.dumps(payload, ensure_ascii=False).encode("utf-8")).decode("ascii")
    return f"""<?php
require __DIR__ . '/wp-load.php';
require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/media.php';
require_once ABSPATH . 'wp-admin/includes/image.php';
require_once ABSPATH . 'wp-admin/includes/post.php';

$p = json_decode(base64_decode('{b64}'), true);
$slug = $p['slug'];
$post_id = 0;
if (!empty($p['post_id'])) {{
    $post_id = (int) $p['post_id'];
    wp_update_post([
        'ID' => $post_id,
        'post_title' => $p['title'],
        'post_name' => $slug,
        'post_content' => $p['content'],
        'post_excerpt' => $p['excerpt'],
        'post_status' => 'publish',
    ]);
}} else {{
$existing = get_page_by_path($slug, OBJECT, 'post');
if ($existing instanceof WP_Post) {{
    $post_id = (int) $existing->ID;
    wp_update_post([
        'ID' => $post_id,
        'post_title' => $p['title'],
        'post_name' => $slug,
        'post_content' => $p['content'],
        'post_excerpt' => $p['excerpt'],
        'post_status' => 'publish',
    ]);
}} else {{
    $post_id = (int) wp_insert_post([
        'post_title' => $p['title'],
        'post_name' => $slug,
        'post_content' => $p['content'],
        'post_excerpt' => $p['excerpt'],
        'post_status' => 'publish',
        'post_type' => 'post',
    ], true);
}}
}}
if (is_wp_error($post_id)) {{
    echo 'ERR post: ' . $post_id->get_error_message() . PHP_EOL;
    exit(1);
}}
echo 'OK post=' . $post_id . ' slug=' . $slug . PHP_EOL;

if (!empty($p['cover_b64'])) {{
    $bin = base64_decode($p['cover_b64']);
    $tmp = wp_tempnam('excalibur-cover-' . $slug . '.png');
    file_put_contents($tmp, $bin);
    $file_array = [
        'name' => $slug . '-cover.png',
        'tmp_name' => $tmp,
        'type' => 'image/png',
        'error' => 0,
        'size' => strlen($bin),
    ];
    $att_id = media_handle_sideload($file_array, $post_id, null, [
        'post_title' => $slug . ' cover',
    ]);
    if (is_wp_error($att_id)) {{
        echo 'WARN cover: ' . $att_id->get_error_message() . PHP_EOL;
    }} else {{
        set_post_thumbnail($post_id, (int) $att_id);
        if (!empty($p['cover_alt'])) {{
            update_post_meta((int) $att_id, '_wp_attachment_image_alt', sanitize_text_field($p['cover_alt']));
        }}
        echo 'OK featured_image=' . (int) $att_id . PHP_EOL;
    }}
    @unlink($tmp);
}}

if (!empty($p['schema_jsonld'])) {{
    update_post_meta($post_id, '_excalibur_blog_schema_jsonld', wp_slash($p['schema_jsonld']));
    update_post_meta($post_id, '_excalibur_blog_skip_theme_faq', '1');
    echo 'OK schema_meta=1' . PHP_EOL;
    echo 'OK skip_theme_faq_meta=1' . PHP_EOL;
}}

if (!empty($p['inline_images'])) {{
    $content_updated = $p['content'];
    foreach ($p['inline_images'] as $img) {{
        $bin = base64_decode($img['b64']);
        $filename = $img['filename'];
        $src = $img['src'];
        
        $tmp = wp_tempnam('excalibur-inline-' . $slug . '-' . sanitize_title($filename));
        file_put_contents($tmp, $bin);
        
        $file_array = [
            'name' => $slug . '-' . $filename,
            'tmp_name' => $tmp,
            'type' => 'image/png',
            'error' => 0,
            'size' => strlen($bin),
        ];
        
        $att_id = media_handle_sideload($file_array, $post_id, null, [
            'post_title' => $slug . ' ' . pathinfo($filename, PATHINFO_FILENAME),
        ]);
        
        if (is_wp_error($att_id)) {{
            echo 'WARN inline_img_upload: ' . $att_id->get_error_message() . ' for ' . $src . PHP_EOL;
        }} else {{
            $new_url = wp_get_attachment_url((int) $att_id);
            if ($new_url) {{
                $content_updated = str_replace('src="' . $src . '"', 'src="' . $new_url . '"', $content_updated);
                $content_updated = str_replace("src='" . $src . "'", "src='" . $new_url . "'", $content_updated);
                echo 'OK inline_image_upload=' . (int) $att_id . ' src=' . $src . ' url=' . $new_url . PHP_EOL;
            }}
        }}
        @unlink($tmp);
    }}
    wp_update_post([
        'ID' => $post_id,
        'post_content' => $content_updated,
    ]);
}}

$permalink = get_permalink($post_id);
echo 'permalink=' . $permalink . PHP_EOL;
"""


def _ssh_creds(env: dict[str, str]) -> tuple[str, int, str, str]:
    host = env.get("SSH_HOST") or env["FTP_HOST"]
    port = int(env.get("SSH_PORT") or "22")
    user = env.get("SSH_USER") or env["FTP_USER"]
    password = env.get("SSH_PASS") or env["FTP_PASS"]
    return host, port, user, password


def configured_sftp_root(env: dict[str, str]) -> str:
    return (env.get("SSH_ROOT") or env.get("FTP_ROOT") or env.get("FTP_PATH") or "").strip()


def sftp_remote_path(env: dict[str, str], remote: str, root_override: str | None = None) -> str:
    root = configured_sftp_root(env) if root_override is None else root_override.strip()
    if not root:
        return remote
    return root.rstrip("/") + "/" + remote


def sftp_root_label(env: dict[str, str]) -> str:
    root = configured_sftp_root(env)
    if not root:
        return "unset"
    if root in {".", "./"}:
        return "dot"
    return "configured-non-dot"


def sftp_root_candidates(env: dict[str, str]) -> list[str]:
    root = configured_sftp_root(env)
    if root and root not in {".", "./"}:
        return [root, "."]
    return [root]


def is_missing_remote_path_error(exc: OSError) -> bool:
    errno_value = getattr(exc, "errno", None)
    if errno_value == 2:
        return True
    text = str(exc).lower()
    return "no such file" in text or "enoent" in text


def upload_bootstrap_sftp(env: dict[str, str], remote: str, data: bytes) -> str:
    import paramiko

    host, port, user, password = _ssh_creds(env)
    transport = paramiko.Transport((host, port))
    transport.connect(username=user, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    try:
        candidates = sftp_root_candidates(env)
        for index, root_candidate in enumerate(candidates):
            remote_path = sftp_remote_path(env, remote, root_candidate)
            try:
                with sftp.open(remote_path, "w") as handle:
                    handle.write(data.decode("utf-8"))
                if index > 0:
                    print(
                        "WARN SFTP root fallback: configured remote root was not found; "
                        "used '.' for bootstrap. Update SSH_ROOT/FTP_ROOT to '.' in Cloud Secrets "
                        "if this is the intended SFTP login cwd."
                    )
                print(f"SFTP upload OK: {remote_path} ({len(data)} bytes)")
                return remote_path
            except OSError as exc:
                if index < len(candidates) - 1 and is_missing_remote_path_error(exc):
                    print(
                        "WARN SFTP upload: configured remote root returned ENOENT; retrying bootstrap at '.'.",
                        file=sys.stderr,
                    )
                    continue
                raise
    finally:
        sftp.close()
        transport.close()
    raise RuntimeError("SFTP upload did not complete")


def delete_bootstrap_sftp(env: dict[str, str], remote: str, remote_path: str | None = None) -> None:
    import paramiko

    host, port, user, password = _ssh_creds(env)
    remote_path = remote_path or sftp_remote_path(env, remote)
    transport = paramiko.Transport((host, port))
    transport.connect(username=user, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    try:
        sftp.remove(remote_path)
    except OSError:
        pass
    finally:
        sftp.close()
        transport.close()


def trigger_bootstrap_http(url: str, root: Path) -> str:
    try:
        print(f"Triggering HTTP publish on {url}...")
        with urllib.request.urlopen(
            urllib.request.Request(url, headers={"User-Agent": "ExcaliburBlogPublish/1.0"}),
            timeout=120,
        ) as response:
            return response.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"Local HTTP trigger failed ({type(e).__name__}: {e}). Entering Cloud WebFetch Fallback mode...")
        print(f"=== FALLBACK_TRIGGER_URL ===\n{url}\n=============================")
        print("Waiting for cloud-agent to write response to memory/webfetch-response.txt...")
        fallback_file = root / "memory" / "webfetch-response.txt"
        fallback_file.unlink(missing_ok=True)
        import time

        for _ in range(120):
            if fallback_file.is_file():
                out = fallback_file.read_text(encoding="utf-8")
                fallback_file.unlink()
                print("Cloud response detected successfully!")
                return out
            time.sleep(1)
        raise RuntimeError("Cloud WebFetch Fallback timed out after 120 seconds. Please trigger manually.")


def publish_via_sftp(env: dict[str, str], php: str, public_base: str) -> str:
    remote = "excalibur-blog-publish-once.php"
    data = php.encode("utf-8")
    url = public_base.rstrip("/") + "/" + remote
    root = project_root()

    uploaded_remote_path = upload_bootstrap_sftp(env, remote, data)

    try:
        out = trigger_bootstrap_http(url, root)
    finally:
        try:
            delete_bootstrap_sftp(env, remote, uploaded_remote_path)
        except Exception as cleanup_error:  # noqa: BLE001
            print(f"WARN cleanup: could not delete bootstrap {remote}: {cleanup_error}", file=sys.stderr)
    return out


def upsert_publish_ledger(root: Path, payload: dict[str, Any], permalink: str) -> None:
    if not permalink:
        return
    ledger_path = root / "shared" / "published-articles.md"
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    if not ledger_path.is_file():
        ledger_path.write_text(
            "# Excalibur BLOG — журнал опубликованных статей\n\n"
            "| date | topic_id | slug | url | status |\n"
            "|------|----------|------|-----|--------|\n",
            encoding="utf-8",
        )

    from datetime import date

    topic_id = str(payload.get("topic_id") or "").upper()
    slug = str(payload.get("slug") or "")
    row = f"| {date.today().isoformat()} | {topic_id} | {slug} | {permalink} | published |"
    lines = ledger_path.read_text(encoding="utf-8").splitlines()
    replaced = False
    for index, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[1].upper() == topic_id:
            lines[index] = row
            replaced = True
            break
    if not replaced:
        lines.append(row)
    ledger_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--article-dir", type=Path, default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--env-check",
        action="store_true",
        help="Validate publish env/secrets without loading article payload or printing secret values",
    )
    ap.add_argument("--public-base", type=str, default=None, help="Override PUBLIC_SITE_URL")
    args = ap.parse_args()
    root = project_root()

    if args.env_check:
        env = load_env(root)
        report = publish_env_check_report(env)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["allow_publish"] and not report["missing"] else 1

    if args.article_dir is None:
        print("--article-dir is required unless --env-check is used", file=sys.stderr)
        return 2

    article_dir = args.article_dir if args.article_dir.is_absolute() else root / args.article_dir
    payload = load_article(article_dir)
    php = build_php(payload)

    if args.dry_run:
        print(json.dumps({"dry_run": True, "slug": payload["slug"], "title": payload["title"]}, ensure_ascii=False, indent=2))
        print("PHP bytes:", len(php.encode("utf-8")))
        return 0

    env = load_env(root)
    if env.get("EXCALIBUR_BLOG_ALLOW_PUBLISH", "").strip().lower() != "yes":
        print("BLOCKER: EXCALIBUR_BLOG_ALLOW_PUBLISH != yes", file=sys.stderr)
        return 1
    missing = validate_publish_env(env)
    if missing:
        print(f"BLOCKER: missing publish env: {', '.join(missing)}", file=sys.stderr)
        return 2
    public = args.public_base or env.get("PUBLIC_SITE_URL") or env.get("WP_HOME") or env.get("WP_SITE_URL") or ""
    if not public:
        print("PUBLIC_SITE_URL or --public-base required", file=sys.stderr)
        return 2
    out = publish_via_sftp(env, php, public)
    print(out)

    result_path = article_dir / "wp-publish-result.json"
    permalink = ""
    for line in out.splitlines():
        if line.startswith("permalink="):
            permalink = line.split("=", 1)[1].strip()
    result = {
        "slug": payload["slug"],
        "topic_id": payload["topic_id"],
        "permalink": permalink,
        "publish_method": "sftp",
        "cover_evidence": payload.get("cover_evidence", {}),
        "raw_output": out,
        "verdict": "pass" if "OK post=" in out else "fail",
    }
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if result["verdict"] == "pass":
        upsert_publish_ledger(root, payload, permalink)
    return 0 if result["verdict"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
