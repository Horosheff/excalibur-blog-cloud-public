#!/usr/bin/env python3
"""DEPRECATED — do not use. See excalibur_blog_quad_apply.py.

Download MCP image URLs into cover/inline PNGs and update registry."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from asset_download import download_url_bytes  # noqa: E402


def project_root() -> Path:
    env_root = os.environ.get("EXCALIBUR_PROJECT_ROOT", "").strip()
    if env_root:
        return Path(env_root)
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def inject_figures(article_html: Path, manifest: dict[str, Any]) -> list[str]:
    if not article_html.is_file():
        return ["article.html not found — skip inject"]

    html = article_html.read_text(encoding="utf-8")
    changes: list[str] = []

    for slot in manifest.get("inline_slots") or []:
        slot_key = slot.get("slot")
        src = slot.get("file", "").replace("\\", "/")
        alt = slot.get("alt") or ""
        h2 = slot.get("h2_anchor")
        if not slot_key or not h2:
            continue
        figure = (
            f'\n<figure class="inline-visual" data-slot="{slot_key}" data-type="{slot.get("visual_type", "")}">\n'
            f'  <img src="{src}" alt="{alt}" loading="lazy">\n'
            f"</figure>\n"
        )
        pattern = re.compile(rf"(<h2[^>]*>\s*{re.escape(h2)}\s*</h2>)", re.I | re.S)
        if f'data-slot="{slot_key}"' in html:
            html = re.sub(
                rf'<figure class="inline-(?:quad|visual)" data-slot="{re.escape(slot_key)}"[\s\S]*?</figure>\s*',
                "",
                html,
                count=1,
            )
        if not pattern.search(html):
            changes.append(f"skip {slot_key}: H2 not found — {h2}")
            continue
        html = pattern.sub(r"\1" + figure, html, count=1)
        changes.append(f"injected {slot_key} after H2 — {h2}")

    article_html.write_text(html, encoding="utf-8", newline="\n")
    return changes


def build_registry(article_dir: Path, manifest: dict[str, Any], results: dict[str, Any]) -> dict[str, Any]:
    meta_path = article_dir / "article.meta.json"
    meta = load_json(meta_path) if meta_path.is_file() else {}
    assets: list[dict[str, Any]] = []

    cover = manifest.get("cover") or {}
    assets.append(
        {
            "role": "cover",
            "slot": "cover",
            "file": cover.get("file", "cover/cover.png"),
            "alt": cover.get("alt") or meta.get("h1") or "",
            "visual_type": "cover_meme_hero",
            "mcp_url": results.get("cover"),
        }
    )
    for slot in manifest.get("inline_slots") or []:
        assets.append(
            {
                "role": "inline",
                "slot": slot.get("slot"),
                "file": slot.get("file"),
                "alt": slot.get("alt") or "",
                "h2_anchor": slot.get("h2_anchor"),
                "visual_type": slot.get("visual_type"),
                "mcp_url": results.get(slot.get("slot")),
            }
        )

    return {
        "topic_id": manifest.get("topic_id") or meta.get("topic_id"),
        "slug": meta.get("slug"),
        "pipeline": "split_v2",
        "file": cover.get("file", "cover/cover.png"),
        "alt": cover.get("alt") or meta.get("h1") or "",
        "aspect_ratio": "16:9",
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "assets": assets,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--article-dir", required=True)
    ap.add_argument("--manifest", default="cover/visual-manifest.json")
    ap.add_argument("--results", default="cover/visual-mcp-results.json")
    ap.add_argument("--inject-html", action="store_true")
    ap.add_argument("--resize", default="1200x675", help="Optional WxH resize via Pillow")
    args = ap.parse_args()

    root = project_root()
    article_dir = Path(args.article_dir)
    if not article_dir.is_absolute():
        article_dir = root / article_dir
    cover_dir = article_dir / "cover"
    cover_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = article_dir / args.manifest
    results_path = article_dir / args.results
    if not manifest_path.is_file():
        print(f"❌ APPLY BLOCKER: {manifest_path} not found", file=sys.stderr)
        return 1
    if not results_path.is_file():
        print(f"❌ APPLY BLOCKER: {results_path} not found", file=sys.stderr)
        return 1

    manifest = load_json(manifest_path)
    results = load_json(results_path)
    slots: dict[str, str] = {}
    cover_file = (manifest.get("cover") or {}).get("file", "cover/cover.png")
    slots["cover"] = cover_file
    for slot in manifest.get("inline_slots") or []:
        slots[slot["slot"]] = slot["file"]

    try:
        from PIL import Image
        import io

        pillow_ok = True
    except ImportError:
        pillow_ok = False
        if args.resize:
            print("WARN Pillow missing — skip resize", file=sys.stderr)

    resize = None
    if args.resize and pillow_ok:
        w, h = args.resize.lower().split("x")
        resize = (int(w), int(h))

    for slot_key, rel_file in slots.items():
        url = (results.get(slot_key) or "").strip()
        if not url:
            print(f"❌ APPLY BLOCKER: missing url for {slot_key}", file=sys.stderr)
            return 1
        out_path = article_dir / rel_file
        out_path.parent.mkdir(parents=True, exist_ok=True)
        data, _evidence = download_url_bytes(url)
        if resize and pillow_ok:
            img = Image.open(io.BytesIO(data)).convert("RGBA")
            img = img.resize(resize, Image.Resampling.LANCZOS)
            img.save(out_path, format="PNG", optimize=True)
        else:
            out_path.write_bytes(data)
        print(f"OK {slot_key}={out_path}")

    registry = build_registry(article_dir, manifest, results)
    save_json(cover_dir / "cover-registry.json", registry)

    report = {"status": "PASS", "pipeline": "split_v2", "results": str(results_path.name)}
    if args.inject_html:
        report["html_inject"] = inject_figures(article_dir / "article.html", manifest)
    save_json(cover_dir / "visual-apply-report.json", report)
    print(f"OK registry={cover_dir / 'cover-registry.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
