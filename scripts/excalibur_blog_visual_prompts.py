#!/usr/bin/env python3
"""DEPRECATED — do not use. See excalibur_blog_cover_quad_prompt.py (ONE quad MCP).

Build MCP batch JSON: cover i2i with hero reference + 3 inline t2i by visual type."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any


def project_root() -> Path:
    env_root = os.environ.get("EXCALIBUR_PROJECT_ROOT", "").strip()
    if env_root:
        return Path(env_root)
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_cover_prompt(cover: dict, style: dict, hero: dict) -> str:
    suffix = style.get("global_prompt_suffix", "").strip()
    for fragment in ("single canvas 2048x1152", "2x2", "four equal"):
        if fragment in suffix:
            suffix = ""
            break
    lines = [
        style.get("global_prompt_prefix", "").strip(),
        "COVER ONLY — single 16:9 image, not a grid.",
        hero.get("prompt_fragment", "").strip(),
        "CRITICAL: preserve EXACT face likeness from reference photo — same glasses, quiff hair, salt-and-pepper beard.",
        f'Clickbait hook scene: {cover.get("scene_hint", "")}.',
        f'Large readable Cyrillic meme caption: "{cover.get("meme_caption_ru", "")}".',
        f'Hook idea: {cover.get("hook", "")}.',
        "Russian internet meme collage, ironic SEO humor, host points at caption or reacts dramatically.",
        suffix,
        f"Negative: {style.get('global_negative_prompt', '')}",
    ]
    return "\n".join(line for line in lines if line)


def build_inline_prompt(slot: dict, types_catalog: dict) -> str:
    type_id = slot.get("visual_type") or "infographic_card"
    type_def = (types_catalog.get("types") or {}).get(type_id) or {}
    lines = [
        type_def.get("prompt_prefix", "").strip(),
        f"Article section H2: «{slot.get('h2_anchor', '')}».",
        slot.get("scene_hint", "").strip(),
        type_def.get("prompt_suffix", "").strip(),
        f"Negative: {type_def.get('negative', '')}",
    ]
    return "\n".join(line for line in lines if line)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--article-dir", required=True)
    ap.add_argument("--manifest", default="cover/visual-manifest.json")
    ap.add_argument("--out", default="cover/visual-mcp-batch.json")
    args = ap.parse_args()

    root = project_root()
    article_dir = Path(args.article_dir)
    if not article_dir.is_absolute():
        article_dir = root / article_dir

    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = article_dir / manifest_path
    if not manifest_path.is_file():
        print(f"❌ PROMPT BLOCKER: manifest not found: {manifest_path}", file=sys.stderr)
        return 1

    manifest = load_json(manifest_path)
    hero = load_json(root / manifest.get("blog_hero", "memory/cover/blog-hero.json"))
    style = load_json(root / manifest.get("cover_style", "memory/cover/quad-style-digital-meme-collage-ru.json"))
    types_catalog = load_json(root / manifest.get("inline_types_catalog", "memory/cover/inline-visual-types.json"))

    ref_url = (hero.get("reference_url_hosted") or "").strip()
    if not ref_url:
        print("❌ COVER HERO BLOCKER: reference_url_hosted missing. Run excalibur_blog_hero_reference_url.py", file=sys.stderr)
        return 1

    cover = manifest.get("cover") or {}
    jobs: list[dict[str, Any]] = [
        {
            "slot": "cover",
            "output_file": cover.get("file", "cover/cover.png"),
            "tool": "gpt-image-2",
            "mcp_args": {
                "prompt": build_cover_prompt(cover, style, hero),
                "input_urls": [ref_url],
                "aspect_ratio": "16:9",
                "resolution": "2K",
            },
        }
    ]

    for slot in manifest.get("inline_slots") or []:
        jobs.append(
            {
                "slot": slot.get("slot"),
                "output_file": slot.get("file"),
                "visual_type": slot.get("visual_type"),
                "tool": "gpt-image-2",
                "mcp_args": {
                    "prompt": build_inline_prompt(slot, types_catalog),
                    "aspect_ratio": "16:9",
                    "resolution": "2K",
                },
            }
        )

    batch = {
        "pipeline_version": "split_v2",
        "article_dir": str(article_dir.relative_to(root)).replace("\\", "/"),
        "reference_url_hosted": ref_url,
        "jobs": jobs,
    }

    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = article_dir / out_path
    save_json(out_path, batch)
    print(f"OK batch={out_path} jobs={len(jobs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
