#!/usr/bin/env python3
"""Excalibur BLOG AI-Slop Detector & Readability Analyzer.

Scans the HTML article, detects corporate cliches/AI-slop phrases, checks sentence lengths,
and computes general readability metrics (adapted for Russian).
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


def load_blocklist(blocklist_path: Path) -> list[str]:
    if not blocklist_path.is_file():
        # Fallback hardcoded blocklist
        return [
            "в современном мире", "давайте разберёмся", "давайте поговорим",
            "подводя итог", "в заключение", "резюмируя",
            "стоит отметить", "важно понимать", "не секрет что",
            "на сегодняшний день", "в наше время", "в этой статье мы рассмотрим",
            "безусловно", "несомненно", "undoubtedly", "играет важную роль",
            "ключевую роль", "комплексный подход", "всесторонний",
            "уникальная возможность", "революционный", "на 100%", "гарантированно"
        ]

    content = blocklist_path.read_text(encoding="utf-8")
    phrases = []
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("- ") and not line.startswith("- ["):
            phrase = line[2:].strip()
            # Handle list inline descriptions or english counterparts
            phrase_clean = re.split(r"\s+[\(\/]", phrase)[0].strip()
            if phrase_clean:
                phrases.append(phrase_clean.lower())
    return phrases


def calculate_flesch_ru(text: str) -> dict[str, Any]:
    """Calculate readability score tailored for the Russian language (Oborneva formula).

    Formula: 206.835 - (1.3 * ASL) - (60.1 * ASW)
    Where:
      - ASL (Average Sentence Length): Average number of words per sentence
      - ASW (Average Syllables per Word): Average syllables per word (vowels in RU)
    """
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]

    # Russian vowels are syllables indicators
    vowels = set("аеёиоуыэюя")

    words = re.findall(r"\b[а-яёA-Za-z\-]+\b", text.lower())

    if not sentences or not words:
        return {"score": 100, "level": "Easy", "avg_sentence_len": 0}

    total_syllables = sum(1 for char in text.lower() if char in vowels)

    asl = len(words) / len(sentences)
    asw = total_syllables / len(words)

    # Oborneva Flesch score adapted for RU
    score = 206.835 - (1.3 * asl) - (60.1 * asw)
    score = max(0.0, min(100.0, score))

    if score > 80:
        level = "Very Easy (Simple conversational / children's text)"
    elif score > 60:
        level = "Easy (Standard modern readable web content)"
    elif score > 45:
        level = "Standard (Intellectual editorial/expert text)"
    elif score > 30:
        level = "Hard (Academic / specialized / complex structures)"
    else:
        level = "Very Hard (Bureaucratic legalese / dry corporate water)"

    return {
        "score": round(score, 1),
        "level": level,
        "avg_sentence_len": round(asl, 1),
        "avg_syllables_per_word": round(asw, 1),
    }


def analyze_slop_and_style(html_path: Path, blocklist_path: Path) -> dict[str, Any]:
    html = html_path.read_text(encoding="utf-8")
    text = re.sub(r"<[^>]+>", " ", html)
    text_clean = re.sub(r"\s+", " ", text).strip()

    blocklist = load_blocklist(blocklist_path)
    text_lower = text_clean.lower()

    hits = []
    for phrase in blocklist:
        # Avoid matching partial words
        pattern = re.compile(rf"\b{re.escape(phrase)}\b", re.IGNORECASE)
        matches = list(pattern.finditer(text_lower))
        for m in matches:
            start, end = m.span()
            hits.append({
                "phrase": phrase,
                "context": text_clean[max(0, start-40):min(len(text_clean), end+40)].strip()
            })

    # Sentence length audit (flag sentences with > 25 words which are common indicators of AI output)
    sentences = re.split(r"[.!?]+", text_clean)
    over_long_sentences = []
    for s in sentences:
        s = s.strip()
        words = re.findall(r"\b[а-яёa-z\-]+\b", s.lower())
        if len(words) > 25:
            over_long_sentences.append({
                "sentence": s,
                "word_count": len(words)
            })

    readability = calculate_flesch_ru(text_clean)

    # Let's assess general style verdict
    verdict = "pass"
    if len(hits) >= 2 or len(over_long_sentences) > 5 or readability["score"] < 40:
        verdict = "warning"
    if len(hits) >= 4:
        verdict = "fail"

    return {
        "verdict": verdict,
        "total_slop_hits": len(hits),
        "slop_hits": hits,
        "total_over_long_sentences": len(over_long_sentences),
        "over_long_sentences": over_long_sentences,
        "readability": readability
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Excalibur BLOG AI-Slop & Readability Analyzer")
    ap.add_argument("html", type=Path, help="Path to article.html")
    ap.add_argument("--blocklist", type=Path, default=None)
    ap.add_argument("-o", "--output", type=Path, help="Path to write slop-detector-report.json")
    args = ap.parse_args()

    root = project_root()
    if not args.html.is_file():
        print(f"File not found: {args.html}", file=sys.stderr)
        return 2

    blocklist_path = args.blocklist or root / "skills/excalibur/references/ai-slop-blocklist.md"
    if not blocklist_path.is_absolute():
        blocklist_path = root / blocklist_path

    report = analyze_slop_and_style(args.html, blocklist_path)
    text_report = json.dumps(report, ensure_ascii=False, indent=2)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text_report + "\n", encoding="utf-8")

    print(f"AI-Slop Detector Verdict: {report['verdict'].upper()}")
    print(f"Total cliches found: {report['total_slop_hits']}")
    print(f"Over-long sentences (>25 words): {report['total_over_long_sentences']}")
    print(f"Flesch Readability Score (RU): {report['readability']['score']} ({report['readability']['level']})")

    if report["errors" if "errors" in report else "slop_hits"]:
        print("\nStyle alerts to review:")
        for h in report["slop_hits"]:
            print(f" - Found cliche: '{h['phrase']}' in context: '...{h['context']}...'")

    return 0 if report["verdict"] in ("pass", "warning") else 1


if __name__ == "__main__":
    raise SystemExit(main())
