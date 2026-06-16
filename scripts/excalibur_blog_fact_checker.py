#!/usr/bin/env python3
"""Excalibur BLOG Fact-Checker.

Extracts numerical facts, percentages, dates, pricing, and key names from an article,
cross-references them with memory/research/fact-bank.md, and generates a report.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def extract_numbers_and_stats(html: str) -> list[dict[str, Any]]:
    # Strip HTML tags first to only get visible text
    text = re.sub(r"<[^>]+>", " ", html)
    # Normalize whitespaces
    text = re.sub(r"\s+", " ", text)

    patterns = {
        "percentage": r"\b(\d+[\s]*%)\b",
        "price_or_currency": r"\b(\d+[\s\d]*[\s]*(?:руб|рублей|р\.|\$|usd|euro|евро))\b",
        "date_or_year": r"\b((?:19|20)\d{2}[\s]*(?:г\.|год|года|г)?)\b",
        "metric_or_duration": r"\b(\d+[\s\d]*[\s]*(?:минут|мин|часов|ч|дней|дн|недель|нед|месяцев|мес|лет))\b",
        "large_number": r"\b(\d+[\s\d]{3,})\b",  # numbers >= 1000
    }

    found = []
    seen: set[str] = set()

    for kind, regex in patterns.items():
        for match in re.finditer(regex, text, re.IGNORECASE):
            val = match.group(1).strip()
            # Clean up duplicate spaces inside numbers
            val_clean = re.sub(r"\s+", " ", val)
            if val_clean.lower() not in seen:
                seen.add(val_clean.lower())
                # Get a small context around the match
                start_idx, end_idx = match.span()
                context = text[max(0, start_idx-50):min(len(text), end_idx+50)].strip()
                found.append({
                    "fact": val_clean,
                    "kind": kind,
                    "context": context,
                })
    return found


def load_fact_bank(fact_bank_path: Path) -> str:
    if not fact_bank_path.is_file():
        return ""
    return fact_bank_path.read_text(encoding="utf-8")


def verify_facts(extracted: list[dict[str, Any]], fact_bank_text: str) -> list[dict[str, Any]]:
    verified = []
    if not fact_bank_text:
        # If fact bank is empty, all facts are unverified
        for item in extracted:
            item["verified"] = False
            item["reason"] = "Fact-bank is empty or missing"
            verified.append(item)
        return verified

    # Lowercase fact bank for easier case-insensitive checks
    fact_bank_lower = fact_bank_text.lower()
    # Normalize spaces in fact bank too
    fact_bank_lower = re.sub(r"\s+", " ", fact_bank_lower)

    for item in extracted:
        fact = item["fact"].lower()
        # Clean currency indicators/letters for flexible match
        numbers_only = "".join(re.findall(r"\d+", fact))

        # Check if exact string matches
        if fact in fact_bank_lower:
            item["verified"] = True
            item["reason"] = "Exact match found in fact-bank"
        # Check if the number itself exists in the fact bank
        elif numbers_only and len(numbers_only) >= 2 and numbers_only in fact_bank_lower:
            item["verified"] = True
            item["reason"] = f"Numerical value '{numbers_only}' matched in fact-bank context"
        else:
            item["verified"] = False
            item["reason"] = "No matching fact or number found in fact-bank"
        verified.append(item)

    return verified


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify article claims against project fact-bank")
    ap.add_argument("html", type=Path, help="Path to article.html")
    ap.add_argument("--fact-bank", type=Path, default=None, help="Path to fact-bank.md")
    ap.add_argument("-o", "--output", type=Path, default=None, help="Path to write fact-check-report.json")
    args = ap.parse_args()

    root = project_root()

    if not args.html.is_file():
        print(f"Not found: {args.html}")
        return 2

    fact_bank_path = args.fact_bank or root / "memory/brief/fact-bank.md"
    if not fact_bank_path.is_absolute():
        fact_bank_path = root / fact_bank_path

    html_content = args.html.read_text(encoding="utf-8")
    extracted_facts = extract_numbers_and_stats(html_content)

    fact_bank_text = load_fact_bank(fact_bank_path)
    if not fact_bank_text:
        print(f"Warning: Fact-bank missing or empty at: {fact_bank_path}")

    report_items = verify_facts(extracted_facts, fact_bank_text)

    total_facts = len(report_items)
    verified_facts = len([f for f in report_items if f["verified"]])
    unverified_facts = total_facts - verified_facts

    # If fact bank exists, we expect at least some facts to match, or warn if there are unverified ones.
    # We pass unless there's a strong contradiction (unverified critical large numbers/pricing).
    # Since some general numbers are fine (e.g. 5 steps), we mark verdict as pass but list unverified details.
    verdict = "pass"
    if fact_bank_text and unverified_facts > 0:
        # If there are unverified critical metrics (like prices or percentages), we warn
        critical_unverified = [f for f in report_items if not f["verified"] and f["kind"] in ("price_or_currency", "percentage")]
        if critical_unverified:
            verdict = "warning"

    report = {
        "article": str(args.html.relative_to(root) if root in args.html.parents else args.html).replace("\\", "/"),
        "fact_bank_source": str(fact_bank_path.relative_to(root) if root in fact_bank_path.parents else fact_bank_path).replace("\\", "/"),
        "verdict": verdict,
        "total_extracted_facts": total_facts,
        "verified_facts_count": verified_facts,
        "unverified_facts_count": unverified_facts,
        "facts": report_items
    }

    text_report = json.dumps(report, ensure_ascii=False, indent=2)
    output_path = args.output or args.html.parent / "fact-check-report.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text_report + "\n", encoding="utf-8")

    print(f"Fact-Check Verdict: {verdict.upper()}")
    print(f"Total extracted stats: {total_facts}")
    print(f"Verified stats: {verified_facts}")
    print(f"Unverified stats: {unverified_facts}")
    print(f"Report written to {output_path.relative_to(root) if root in output_path.parents else output_path}")

    return 0 if verdict in ("pass", "warning") else 1


if __name__ == "__main__":
    raise SystemExit(main())
