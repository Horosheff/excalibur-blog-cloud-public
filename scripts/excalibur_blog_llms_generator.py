#!/usr/bin/env python3
"""Excalibur BLOG LLMs Generator: AI-First Crawler Policy.

Generates and maintains standard llms.txt and llms-full.txt in the root folder,
providing LLM-readable indices and plain-text summaries of all blog articles.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def strip_html(html: str) -> str:
    # Remove script and style tags completely
    html = re.sub(r"<(script|style)[^>]*>[\s\S]*?</\1>", "", html, flags=re.IGNORECASE)
    # Convert paragraph endings and headers to newlines
    html = re.sub(r"</?(p|h1|h2|h3|li|div|blockquote)[^>]*>", "\n", html, flags=re.IGNORECASE)
    # Remove all other HTML tags
    text = re.sub(r"<[^>]+>", "", html)
    # Normalize whitespaces and newlines
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n", "\n\n", text)
    return text.strip()


def load_articles(blog_dir: Path) -> list[dict[str, Any]]:
    articles = []
    if not blog_dir.is_dir():
        return articles

    for article_dir in blog_dir.iterdir():
        if not article_dir.is_dir():
            continue
        meta_path = article_dir / "article.meta.json"
        html_path = article_dir / "article.html"
        if meta_path.is_file() and html_path.is_file():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                html_content = html_path.read_text(encoding="utf-8")
                plain_text = strip_html(html_content)

                # Use AEO description as the highly dense summaries for AI
                meta_ab = meta.get("meta_ab", {})
                aeo_desc = meta_ab.get("description_aeo") or meta_ab.get("description_seo") or meta.get("description", "")

                articles.append({
                    "slug": meta.get("slug", article_dir.name),
                    "title": meta_ab.get("title_aeo") or meta_ab.get("title_seo") or meta.get("title") or meta.get("h1", article_dir.name),
                    "description": aeo_desc,
                    "plain_text": plain_text,
                })
            except Exception as e:
                print(f"Error loading {article_dir.name}: {e}")
    return articles


def article_url(site_base: str, blog_path: str, slug: str) -> str:
    site_base = site_base.rstrip("/")
    path = "/" + blog_path.strip("/")
    if path == "/":
        return f"{site_base}/{slug}/"
    return f"{site_base}{path}/{slug}/"


def build_llms_txt(
    site_name: str,
    site_desc: str,
    articles: list[dict[str, Any]],
    site_base: str,
    blog_path: str,
) -> str:
    lines = [
        f"# {site_name}",
        f"> {site_desc}",
        "",
        "## Blog Articles",
        ""
    ]
    for a in articles:
        url = article_url(site_base, blog_path, a["slug"])
        lines.append(f"- [{a['title']}]({url}): {a['description']}")

    return "\n".join(lines) + "\n"


def build_llms_full_txt(site_name: str, articles: list[dict[str, Any]], site_base: str, blog_path: str) -> str:
    lines = [
        f"# {site_name} - Full LLM Knowledge Base",
        "This file contains full plain-text articles optimized for AI reasoning and semantic search.",
        "",
        "---",
        ""
    ]

    for a in articles:
        url = article_url(site_base, blog_path, a["slug"])
        lines.extend([
            f"## {a['title']}",
            f"- **URL**: {url}",
            f"- **Summary**: {a['description']}",
            "",
            a["plain_text"],
            "",
            "---",
            ""
        ])

    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate AI-friendly llms.txt and llms-full.txt")
    ap.add_argument("--blog-dir", type=Path, default=None)
    ap.add_argument("--site-name", type=str, default="Maya AI — Excalibur BLOG")
    ap.add_argument("--site-desc", type=str, default="Практический блог по автоматизации бизнеса на Make.com, вайбкодингу и ИИ-агентам.")
    ap.add_argument("--site-base", type=str, default="https://mayai.ru")
    ap.add_argument("--blog-path", type=str, default="/", help="URL prefix for posts, e.g. /blog/ or /")
    ap.add_argument("--out-dir", type=Path, default=None, help="Output directory for llms.txt/llms-full.txt")
    args = ap.parse_args()

    root = project_root()
    blog_dir = args.blog_dir or root / "memory/blog/articles"
    if not blog_dir.is_absolute():
        blog_dir = root / blog_dir

    out_dir = args.out_dir or root
    if not out_dir.is_absolute():
        out_dir = root / out_dir

    articles = load_articles(blog_dir)
    print(f"Loaded {len(articles)} articles to index for LLMs.")

    llms_txt = build_llms_txt(args.site_name, args.site_desc, articles, args.site_base, args.blog_path)
    llms_full_txt = build_llms_full_txt(args.site_name, articles, args.site_base, args.blog_path)

    llms_path = out_dir / "llms.txt"
    llms_full_path = out_dir / "llms-full.txt"

    llms_path.write_text(llms_txt, encoding="utf-8")
    llms_full_path.write_text(llms_full_txt, encoding="utf-8")

    print(f"llms.txt generated at {llms_path.relative_to(root) if root in llms_path.parents else llms_path}")
    print(f"llms-full.txt generated at {llms_full_path.relative_to(root) if root in llms_full_path.parents else llms_full_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
