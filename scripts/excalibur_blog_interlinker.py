#!/usr/bin/env python3
"""Excalibur BLOG Interlinker: Hub-and-Spoke internal linking manager.

Scans articles in memory/blog/articles/, matches keywords to other articles,
and generates linking recommendations or automatically injects links.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_all_articles(blog_dir: Path) -> list[dict[str, Any]]:
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
                articles.append({
                    "topic_id": meta.get("topic_id", article_dir.name),
                    "slug": meta.get("slug", ""),
                    "title": meta.get("title") or meta.get("h1", ""),
                    "primary_query": meta.get("primary_query", ""),
                    "secondary_queries": meta.get("secondary_queries", []),
                    "anchor_variants": meta.get("anchor_variants", []),
                    "html_path": html_path,
                    "meta_path": meta_path,
                    "html_content": html_content,
                    "dir_name": article_dir.name,
                })
            except Exception as e:
                print(f"Error loading {article_dir.name}: {e}")
    return articles


def find_linking_opportunities(articles: list[dict[str, Any]], site_base: str) -> list[dict[str, Any]]:
    suggestions = []
    # Normalize site base URL
    site_base = site_base.rstrip("/")

    for target in articles:
        target_slug = target["slug"]
        if not target_slug:
            continue

        target_url = f"{site_base}/blog/{target_slug}/"
        # Prioritize natural anchor variants for diversification, then primary, then secondary queries
        raw_keywords = target.get("anchor_variants", []) + [target["primary_query"]] + target["secondary_queries"]
        # Remove duplicates while preserving order
        seen = set()
        keywords = []
        for k in raw_keywords:
            if k and k.strip():
                k_clean = k.strip()
                if k_clean not in seen:
                    seen.add(k_clean)
                    keywords.append(k_clean)

        if not keywords:
            continue

        for source in articles:
            if source["topic_id"] == target["topic_id"]:
                continue  # Don't link to itself

            source_html = source["html_content"]
            # Check if source already links to target slug
            if target_slug in source_html:
                continue  # Already linked

            for keyword in keywords:
                # Find occurrences of keyword in source HTML, avoiding inside existing <a> tags or headings
                # Handle multi-word phrases vs single words for Russian word endings
                if " " in keyword:
                    pattern = re.compile(rf"\b({re.escape(keyword)})\b", re.IGNORECASE)
                else:
                    pattern = re.compile(rf"\b({re.escape(keyword)}[а-яё]*)\b", re.IGNORECASE)

                matches = list(pattern.finditer(source_html))
                for match in matches:
                    start_idx, end_idx = match.span()
                    matched_text = match.group(1)

                    # Simple validation: make sure it's not inside a tag (e.g. href="...") or within <a>...</a>
                    # We can check if there's an open <a> before this match that isn't closed yet.
                    # Or simpler: if the match is inside <...> or immediately surrounded by <a>
                    before = source_html[:start_idx]
                    after = source_html[end_idx:]

                    # Check if inside a tag
                    if before.count("<") > before.count(">"):
                        continue  # Inside tag attributes/brackets

                    # Check if inside <a>...</a>
                    # Count open and close <a> tags before match
                    open_a = before.lower().count("<a ") + before.lower().count("<a>")
                    close_a = before.lower().count("</a>")
                    if open_a > close_a:
                        continue  # Inside an active anchor link

                    # Check if inside heading tags like <h2>, <h3>
                    open_h = before.lower().count("<h1") + before.lower().count("<h2") + before.lower().count("<h3")
                    close_h = before.lower().count("</h1>") + before.lower().count("</h2>") + before.lower().count("</h3>")
                    if open_h > close_h:
                        continue  # Inside a heading tag

                    # Found a valid opportunity!
                    suggestions.append({
                        "source_topic_id": source["topic_id"],
                        "source_dir": source["dir_name"],
                        "source_slug": source["slug"],
                        "target_topic_id": target["topic_id"],
                        "target_dir": target["dir_name"],
                        "target_slug": target["slug"],
                        "target_url": target_url,
                        "keyword": keyword,
                        "matched_text": matched_text,
                        "context": source_html[max(0, start_idx-60):min(len(source_html), end_idx+60)].strip().replace("\n", " "),
                        "start_idx": start_idx,
                        "end_idx": end_idx,
                    })
                    break  # Suggest one link per source-target-keyword pair to prevent over-linking
    return suggestions


def filter_suggestions_for_article(
    suggestions: list[dict[str, Any]],
    article_dir: Path | None,
    articles: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if not article_dir:
        return suggestions
    article_dir = article_dir.resolve()
    selected = None
    for article in articles:
        if article["html_path"].parent.resolve() == article_dir:
            selected = article
            break
    if not selected:
        raise ValueError(f"article-dir not found in loaded articles: {article_dir}")
    topic_id = selected["topic_id"]
    # New article indexing needs both outbound links from it and inbound links to it.
    return [
        suggestion
        for suggestion in suggestions
        if suggestion["source_topic_id"] == topic_id or suggestion["target_topic_id"] == topic_id
    ]


def apply_interlinks(suggestions: list[dict[str, Any]], articles: list[dict[str, Any]]) -> int:
    applied_count = 0
    # Group suggestions by source article path to modify each file once
    by_source: dict[Path, list[dict[str, Any]]] = {}
    articles_by_path = {a["html_path"]: a for a in articles}

    for sug in suggestions:
        src_article = next((a for a in articles if a["topic_id"] == sug["source_topic_id"]), None)
        if src_article:
            by_source.setdefault(src_article["html_path"], []).append(sug)

    for html_path, sugs in by_source.items():
        # Sort suggestions in reverse order of index so offset changes don't affect previous indices
        sugs.sort(key=lambda s: s["start_idx"], reverse=True)
        content = html_path.read_text(encoding="utf-8")

        for sug in sugs:
            # Re-verify that context matches just in case
            matched_text = sug["matched_text"]
            start = sug["start_idx"]
            end = sug["end_idx"]

            if content[start:end] == matched_text:
                link_html = f'<a href="/blog/{sug["target_slug"]}/">{matched_text}</a>'
                content = content[:start] + link_html + content[end:]
                applied_count += 1

        html_path.write_text(content, encoding="utf-8")
        print(f"Applied {len(sugs)} internal links to {html_path.name}")

    return applied_count


def main() -> int:
    ap = argparse.ArgumentParser(description="Excalibur BLOG Hub-and-Spoke Interlinker")
    ap.add_argument("--blog-dir", type=Path, default=None, help="Path to articles/ directory")
    ap.add_argument("--article-dir", type=Path, default=None, help="Limit suggestions to one article as source or target")
    ap.add_argument("--site-base", type=str, default="https://example.com", help="Base site URL")
    ap.add_argument("--apply", action="store_true", help="Directly edit html files to apply links")
    ap.add_argument("--output", type=Path, default=None, help="Output path for JSON suggestions report")
    args = ap.parse_args()

    root = project_root()
    blog_dir = args.blog_dir or root / "memory/blog/articles"
    if not blog_dir.is_absolute():
        blog_dir = root / blog_dir

    if not blog_dir.is_dir():
        print(f"Blog directory not found: {blog_dir}")
        return 1

    articles = load_all_articles(blog_dir)
    print(f"Loaded {len(articles)} articles from memory.")

    suggestions = find_linking_opportunities(articles, args.site_base)
    article_dir = args.article_dir
    if article_dir and not article_dir.is_absolute():
        article_dir = root / article_dir
    suggestions = filter_suggestions_for_article(suggestions, article_dir, articles)
    print(f"Found {len(suggestions)} internal linking opportunities.")

    report = {
        "site_base": args.site_base,
        "total_articles": len(articles),
        "opportunities_found": len(suggestions),
        "suggestions": [
            {
                "source": s["source_dir"],
                "target": s["target_dir"],
                "keyword": s["keyword"],
                "context": s["context"],
                "link_replacement": f'<a href="/blog/{s["target_slug"]}/">{s["matched_text"]}</a>'
            }
            for s in suggestions
        ]
    }

    output_path = args.output or root / "memory/blog/interlink-suggestions.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Saved suggestions report to {output_path.relative_to(root) if root in output_path.parents else output_path}")

    if args.apply and suggestions:
        applied = apply_interlinks(suggestions, articles)
        print(f"Successfully applied {applied} internal links across articles.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
