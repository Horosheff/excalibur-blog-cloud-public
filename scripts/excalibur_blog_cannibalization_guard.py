#!/usr/bin/env python3
"""Excalibur BLOG Keyword Cannibalization Guard.

Scans article metadata in memory/blog/articles/ to detect keyword overlaps,
duplicate primary queries, and high semantic cannibalization risks.
Works without external dependencies using an n-gram and prefix overlap similarity metric.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def normalize_and_tokenize(text: str) -> list[str]:
    """Helper to tokenize, lowercase, and stem/prefix Russian words.

    Using prefixes of length 4-5 as a lightweight stemmer fallback.
    """
    text = text.lower()
    # Remove punctuation
    text = re.sub(r"[^\w\s\-]", " ", text)
    words = text.split()
    tokens = []
    for w in words:
        w_clean = w.strip()
        if not w_clean:
            continue
        # Stop words (very basic RU stop list)
        if w_clean in {"в", "на", "и", "или", "с", "по", "для", "как", "что", "это", "под", "из", "за"}:
            continue
        # Stemming fallback (take first 4 chars for Russian word matching)
        if len(w_clean) > 4:
            tokens.append(w_clean[:5])
        else:
            tokens.append(w_clean)
    return tokens


def calculate_jaccard_similarity(set1: set[str], set2: set[str]) -> float:
    if not set1 or not set2:
        return 0.0
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union


def check_cannibalization(articles: list[dict[str, Any]], threshold: float) -> dict[str, Any]:
    issues = []
    verdict = "pass"

    for i in range(len(articles)):
        a1 = articles[i]
        tokens1_primary = set(normalize_and_tokenize(a1["primary_query"]))

        for j in range(i + 1, len(articles)):
            a2 = articles[j]
            tokens2_primary = set(normalize_and_tokenize(a2["primary_query"]))

            # 1. Check exact match of primary query (FAIL condition)
            if a1["primary_query"].strip().lower() == a2["primary_query"].strip().lower():
                issues.append({
                    "severity": "fail",
                    "type": "duplicate_primary_query",
                    "message": f"CRITICAL: Articles '{a1['dir_name']}' and '{a2['dir_name']}' share the EXACT SAME primary query: '{a1['primary_query']}'",
                    "articles": [a1["dir_name"], a2["dir_name"]],
                    "query": a1["primary_query"]
                })
                verdict = "fail"
                continue

            # 2. Check Jaccard similarity of primary queries
            prim_sim = calculate_jaccard_similarity(tokens1_primary, tokens2_primary)
            if prim_sim >= threshold:
                issues.append({
                    "severity": "warning",
                    "type": "high_primary_overlap",
                    "message": f"WARNING: High primary query overlap ({round(prim_sim*100)}%) between '{a1['dir_name']}' and '{a2['dir_name']}'. Queries: '{a1['primary_query']}' vs '{a2['primary_query']}'",
                    "articles": [a1["dir_name"], a2["dir_name"]],
                    "queries": [a1["primary_query"], a2["primary_query"]],
                    "similarity": round(prim_sim, 2)
                })
                if verdict != "fail":
                    verdict = "warning"

            # 3. Check primary query of A1 cannibalizing secondary queries of A2
            all_queries2 = [a2["primary_query"]] + a2["secondary_queries"]
            for s_q in a2["secondary_queries"]:
                tokens_sq = set(normalize_and_tokenize(s_q))
                sim = calculate_jaccard_similarity(tokens1_primary, tokens_sq)
                if sim >= threshold or a1["primary_query"].strip().lower() == s_q.strip().lower():
                    issues.append({
                        "severity": "warning",
                        "type": "primary_secondary_cannibalization",
                        "message": f"WARNING: Primary query of '{a1['dir_name']}' ('{a1['primary_query']}') highly overlaps with secondary query of '{a2['dir_name']}' ('{s_q}'). Similarity: {round(sim*100)}%",
                        "articles": [a1["dir_name"], a2["dir_name"]],
                        "primary_query": a1["primary_query"],
                        "secondary_query": s_q,
                        "similarity": round(sim, 2)
                    })
                    if verdict != "fail":
                        verdict = "warning"

            # 4. Check primary query of A2 cannibalizing secondary queries of A1
            for s_q in a1["secondary_queries"]:
                tokens_sq = set(normalize_and_tokenize(s_q))
                sim = calculate_jaccard_similarity(tokens2_primary, tokens_sq)
                if sim >= threshold or a2["primary_query"].strip().lower() == s_q.strip().lower():
                    issues.append({
                        "severity": "warning",
                        "type": "primary_secondary_cannibalization",
                        "message": f"WARNING: Primary query of '{a2['dir_name']}' ('{a2['primary_query']}') highly overlaps with secondary query of '{a1['dir_name']}' ('{s_q}'). Similarity: {round(sim*100)}%",
                        "articles": [a1["dir_name"], a2["dir_name"]],
                        "primary_query": a2["primary_query"],
                        "secondary_query": s_q,
                        "similarity": round(sim, 2)
                    })
                    if verdict != "fail":
                        verdict = "warning"

    return {
        "verdict": verdict,
        "total_issues": len(issues),
        "issues": issues
    }


def load_all_metas(blog_dir: Path) -> list[dict[str, Any]]:
    metas = []
    if not blog_dir.is_dir():
        return metas

    for article_dir in blog_dir.iterdir():
        if not article_dir.is_dir():
            continue
        meta_path = article_dir / "article.meta.json"
        if meta_path.is_file():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                metas.append({
                    "topic_id": meta.get("topic_id", article_dir.name),
                    "dir_name": article_dir.name,
                    "primary_query": meta.get("primary_query", ""),
                    "secondary_queries": meta.get("secondary_queries", []),
                    "meta_path": meta_path
                })
            except Exception as e:
                print(f"Error loading {meta_path.name}: {e}")
    return metas


def main() -> int:
    ap = argparse.ArgumentParser(description="Excalibur BLOG Keyword Cannibalization Guard")
    ap.add_argument("--blog-dir", type=Path, default=None, help="Path to articles directory")
    ap.add_argument("--threshold", type=float, default=0.7, help="Jaccard similarity warning threshold (0.0 to 1.0)")
    ap.add_argument("-o", "--output", type=Path, default=None, help="Output path for cannibalization report JSON")
    args = ap.parse_args()

    root = project_root()
    blog_dir = args.blog_dir or root / "memory/blog/articles"
    if not blog_dir.is_absolute():
        blog_dir = root / blog_dir

    if not blog_dir.is_dir():
        print(f"Blog directory not found: {blog_dir}", file=sys.stderr)
        return 2

    articles = load_all_metas(blog_dir)
    print(f"Loaded {len(articles)} article metadata definitions for cannibalization checks.")

    report = check_cannibalization(articles, args.threshold)
    report_text = json.dumps(report, ensure_ascii=False, indent=2)

    output_path = args.output or root / "memory/blog/cannibalization-report.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_text + "\n", encoding="utf-8")

    print(f"\nKeyword Cannibalization Guard Verdict: {report['verdict'].upper()}")
    print(f"Total issues/warnings detected: {report['total_issues']}")

    if report["issues"]:
        print("\nDetails:")
        for issue in report["issues"]:
            prefix = "[FAIL]" if issue["severity"] == "fail" else "[WARN]"
            print(f" {prefix} {issue['message']}")

    return 0 if report["verdict"] != "fail" else 1


if __name__ == "__main__":
    raise SystemExit(main())
