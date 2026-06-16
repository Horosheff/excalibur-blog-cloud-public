#!/usr/bin/env python3
"""Excalibur BLOG HTML Tag Linter & Sanitizer.

Enforces strict whitelist of HTML tags, prevents unclosed tags, and checks for malformed markup.
Allowed tags: h2, h3, p, b, i, a, ul, ol, li, blockquote, table, thead, tbody, tr, th, td
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


def detect_anchor_toc(html: str) -> list[str]:
    """Fail if article contains in-body table of contents (anchor link list)."""
    errors: list[str] = []
    # Block: ol/ul with 3+ li containing href="#..."
    list_blocks = re.findall(r"<(?:ol|ul)[^>]*>(.*?)</(?:ol|ul)>", html, flags=re.IGNORECASE | re.DOTALL)
    for block in list_blocks:
        anchor_links = re.findall(
            r'<li[^>]*>\s*<a\s+[^>]*href=["\']#([^"\']+)["\']',
            block,
            flags=re.IGNORECASE,
        )
        if len(anchor_links) >= 3:
            errors.append(
                "Forbidden in-body TOC: list with 3+ anchor links to headings "
                f"(#{', #'.join(anchor_links[:5])}{'...' if len(anchor_links) > 5 else ''}). "
                "Remove <ol>/<ul> navigation after TL;DR; see excalibur-article-writing-contract.md block 3."
            )
    return errors


def detect_duplicate_faq_sections(html: str) -> list[str]:
    """Fail if article has more than one FAQ heading block."""
    errors: list[str] = []
    faq_headings = re.findall(
        r"<h2[^>]*>\s*(.*?)\s*</h2>",
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    faq_like = []
    for raw in faq_headings:
        text = re.sub(r"<[^>]+>", "", raw).strip().lower()
        if re.search(r"faq|частые вопрос|задаваемые вопрос", text):
            faq_like.append(text)
    if len(faq_like) > 1:
        errors.append(
            "Forbidden duplicate FAQ sections in article.html: "
            + "; ".join(faq_like[:4])
            + ". Keep exactly one <h2>Частые вопросы</h2> block."
        )
    banned_second = re.search(
        r"<h2[^>]*>\s*[^<]*(?:задаваемые вопросы по теме|faq по теме)",
        html,
        flags=re.IGNORECASE,
    )
    if banned_second:
        errors.append(
            "Forbidden second FAQ block title (e.g. «Часто задаваемые вопросы по теме»). "
            "Use only one thematic FAQ section."
        )
    return errors


class HTMLTagLinter(HTMLParser):
    def __init__(self, whitelist: set[str]) -> None:
        super().__init__()
        self.whitelist = whitelist
        self.errors: list[str] = []
        self.tag_stack: list[tuple[str, int, int]] = []  # (tag, line, col)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag_lower = tag.lower()
        line, col = self.getpos()

        # Check whitelist
        if tag_lower not in self.whitelist:
            self.errors.append(f"Line {line}, Col {col}: Forbidden HTML tag <{tag}> used.")

        # Check nested structure
        # Self-closing tags in HTML5 parser like <img> don't need closing, but we stack block elements
        self_closing = {"img", "br", "hr"}
        if tag_lower not in self_closing:
            self.tag_stack.append((tag_lower, line, col))

    def handle_endtag(self, tag: str) -> None:
        tag_lower = tag.lower()
        line, col = self.getpos()
        self_closing = {"img", "br", "hr"}
        if tag_lower in self_closing:
            return

        if not self.tag_stack:
            self.errors.append(f"Line {line}, Col {col}: Unexpected closing tag </{tag_lower}> with no matching open tag.")
            return

        # Find matching open tag in stack
        expected_tag, o_line, o_col = self.tag_stack.pop()
        if expected_tag != tag_lower:
            self.errors.append(
                f"Line {line}, Col {col}: Tag mismatch. Closed </{tag_lower}> but expected </{expected_tag}> "
                f"opened at Line {o_line}, Col {o_col}."
            )
            # Re-push expected tag to stack to keep linting subsequent tags gracefully
            self.tag_stack.append((expected_tag, o_line, o_col))

    def check_unclosed_tags(self) -> None:
        while self.tag_stack:
            tag, line, col = self.tag_stack.pop()
            self.errors.append(f"Line {line}, Col {col}: Unclosed HTML tag <{tag}> at end of document.")


def lint_html_file(html_path: Path, whitelist: set[str]) -> dict[str, Any]:
    html_content = html_path.read_text(encoding="utf-8")
    linter = HTMLTagLinter(whitelist)
    linter.feed(html_content)
    linter.check_unclosed_tags()
    linter.errors.extend(detect_anchor_toc(html_content))
    linter.errors.extend(detect_duplicate_faq_sections(html_content))

    return {
        "file": str(html_path.name),
        "verdict": "pass" if not linter.errors else "fail",
        "total_errors": len(linter.errors),
        "errors": linter.errors,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Excalibur BLOG HTML Whitelist & Nesting Linter")
    ap.add_argument("html", type=Path, help="Path to article.html")
    ap.add_argument("-o", "--output", type=Path, help="Path to write html-linter-report.json")
    args = ap.parse_args()

    if not args.html.is_file():
        print(f"File not found: {args.html}", file=sys.stderr)
        return 2

    # Whitelist tags based on excalibur contract and cover inline figure injection.
    allowed_tags = {
        "h2", "h3", "p", "b", "i", "a", "ul", "ol", "li", "blockquote",
        "table", "thead", "tbody", "tr", "th", "td", "figure", "img", "br"
    }

    report = lint_html_file(args.html, allowed_tags)
    text = json.dumps(report, ensure_ascii=False, indent=2)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")

    print(f"HTML Linter Verdict: {report['verdict'].upper()}")
    if report["errors"]:
        print(f"Found {report['total_errors']} HTML errors/warnings:")
        for err in report["errors"]:
            print(f" - {err}")
    else:
        print("All HTML tags are clean, validated, and conform to whitelist!")

    return 0 if report["verdict"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
