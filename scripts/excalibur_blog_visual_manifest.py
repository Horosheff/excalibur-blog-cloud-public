#!/usr/bin/env python3
"""DEPRECATED — do not use. See excalibur_blog_quad_manifest.py.

Build visual-manifest.json: cover hook + inline visual types from article H2."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


TYPE_PRIORITY = [
    "comparison_table_ui",
    "workflow_diagram",
    "checklist_board",
    "schema_faq_ui",
    "tool_screenshot",
    "infographic_card",
]
INLINE_FILES = {
    "inline_1": "inline-01.png",
    "inline_2": "inline-02.png",
    "inline_3": "inline-03.png",
}


def project_root() -> Path:
    env_root = os.environ.get("EXCALIBUR_PROJECT_ROOT", "").strip()
    if env_root:
        return Path(env_root)
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def extract_h2_titles(article_html: Path) -> list[str]:
    if not article_html.is_file():
        return []
    text = article_html.read_text(encoding="utf-8")
    titles: list[str] = []
    for match in re.finditer(r"<h2[^>]*>(.*?)</h2>", text, flags=re.I | re.S):
        title = re.sub(r"<[^>]+>", "", match.group(1))
        title = re.sub(r"\s+", " ", title).strip()
        if not title:
            continue
        if title.lower() in {"частые вопросы", "faq"}:
            break
        titles.append(title)
    return titles


def score_type(h2: str, type_id: str, type_def: dict) -> int:
    hay = h2.lower()
    score = 0
    for kw in type_def.get("keywords") or []:
        if kw.strip().lower() in hay:
            score += 2
    return score


def pick_visual_type(h2: str, types_catalog: dict, used: set[str]) -> str:
    types = types_catalog.get("types") or {}
    scored: list[tuple[int, str]] = []
    for type_id, type_def in types.items():
        scored.append((score_type(h2, type_id, type_def), type_id))
    scored.sort(key=lambda item: (-item[0], TYPE_PRIORITY.index(item[1]) if item[1] in TYPE_PRIORITY else 99))

    for score, type_id in scored:
        if score > 0 and type_id not in used:
            return type_id
    for type_id in TYPE_PRIORITY:
        if type_id not in used:
            return type_id
    return TYPE_PRIORITY[0]


def scene_hint_for_type(type_id: str, h2: str, article_topic: str) -> str:
    hints = {
        "comparison_table_ui": f"Таблица «SEO vs GEO» к секции «{h2}»: критерии, цели, что видит человек vs AI",
        "workflow_diagram": f"6 шагов workflow longread к «{h2}»: интент → семантика → outline → lead → факты → FAQ",
        "checklist_board": f"Printable чеклист перед публикацией для «{h2}»: мета, H2, FAQ, schema, ссылки",
        "schema_faq_ui": f"UI mockup FAQ + JSON-LD schema для «{h2}»",
        "tool_screenshot": f"Скрин SEO-инструмента по теме «{article_topic}» для «{h2}»",
        "infographic_card": f"Карточка фактов и цифр по «{h2}»",
    }
    return hints.get(type_id, f"Полезная иллюстрация к «{h2}»")


def alt_for_type(type_id: str, h2: str, types_catalog: dict) -> str:
    label = ((types_catalog.get("types") or {}).get(type_id) or {}).get("label_ru") or type_id
    return f"{label}: {h2}"


def build_manifest(article_dir: Path, root: Path, preserve_cover: dict | None) -> dict[str, Any]:
    meta_path = article_dir / "article.meta.json"
    meta = load_json(meta_path) if meta_path.is_file() else {}
    types_path = root / "memory/cover/inline-visual-types.json"
    types_catalog = load_json(types_path)
    h2s = extract_h2_titles(article_dir / "article.html")
    topic_id = meta.get("topic_id") or article_dir.name.split("-")[0]
    article_topic = meta.get("h1") or meta.get("primary_query") or article_dir.name

    cover = preserve_cover or {
        "file": "cover/cover.png",
        "hook": "SEO-текст, который люди дочитают — миф или workflow?",
        "meme_caption_ru": "15k ключей — 0 прочтений?",
        "scene_hint": "герой с reference-лицом, шок/ирония SEOшника, Wordstat + ноутбук, крючок на клик",
        "alt": f"Обложка: {article_topic}",
    }

    used: set[str] = set()
    inline_slots: list[dict[str, Any]] = []
    for idx, slot_key in enumerate(("inline_1", "inline_2", "inline_3"), start=1):
        h2 = h2s[idx - 1] if idx - 1 < len(h2s) else f"Секция {idx}"
        visual_type = pick_visual_type(h2, types_catalog, used)
        used.add(visual_type)
        inline_slots.append(
            {
                "slot": slot_key,
                "file": f"cover/{INLINE_FILES[slot_key]}",
                "h2_anchor": h2,
                "visual_type": visual_type,
                "scene_hint": scene_hint_for_type(visual_type, h2, str(article_topic)),
                "alt": alt_for_type(visual_type, h2, types_catalog),
            }
        )

    return {
        "pipeline_version": "split_v2",
        "topic_id": topic_id,
        "blog_hero": "memory/cover/blog-hero.json",
        "cover_style": "memory/cover/quad-style-digital-meme-collage-ru.json",
        "inline_types_catalog": "memory/cover/inline-visual-types.json",
        "cover": cover,
        "inline_slots": inline_slots,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--article-dir", required=True)
    ap.add_argument("--out", default="cover/visual-manifest.json")
    ap.add_argument("--merge", action="store_true", help="Keep existing cover fields if manifest exists")
    args = ap.parse_args()

    root = project_root()
    article_dir = Path(args.article_dir)
    if not article_dir.is_absolute():
        article_dir = root / article_dir

    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = article_dir / out_path

    preserve_cover = None
    if args.merge and out_path.is_file():
        existing = load_json(out_path)
        preserve_cover = existing.get("cover")

    manifest = build_manifest(article_dir, root, preserve_cover)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    save_json(out_path, manifest)
    print(f"OK manifest={out_path}")
    for slot in manifest["inline_slots"]:
        print(f"  {slot['slot']}: {slot['visual_type']} -> {slot['h2_anchor']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
