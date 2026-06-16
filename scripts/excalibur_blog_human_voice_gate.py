#!/usr/bin/env python3
"""Check Excalibur BLOG articles for human voice and anti-template signals."""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path
from typing import Any

from excalibur_repo_paths import repo_relative


CONCRETE_MARKERS = (
    "например",
    "на практике",
    "типичная ошибка",
    "живой пример",
    "представьте",
    "в реальном проекте",
    "разберем ситуацию",
    "часто ломается",
    "из практики",
)

PAIN_MARKERS = (
    "боль",
    "проблем",
    "ошиб",
    "ломает",
    "не работает",
    "теряет",
    "дорого",
    "долго",
    "рутин",
    "хаос",
    "застр",
    "сложно",
)

OUTCOME_MARKERS = (
    "результат",
    "получите",
    "сможете",
    "сэконом",
    "проверьте",
    "запустите",
    "соберите",
    "настройте",
    "исправьте",
    "выберите",
)

AI_OPENERS = (
    "в современном мире",
    "давайте разберемся",
    "давайте разберёмся",
    "в этой статье",
    "на сегодняшний день",
    "стоит отметить",
    "важно понимать",
)

TEXTBOOK_H2_STARTS = (
    "что такое",
    "почему важно",
    "зачем нужен",
    "основные преимущества",
    "ключевые особенности",
)


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def strip_html(html: str) -> str:
    text = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def extract_h2_titles(html: str) -> list[str]:
    titles: list[str] = []
    for match in re.finditer(r"<h2[^>]*>(.*?)</h2>", html, flags=re.I | re.S):
        title = re.sub(r"<[^>]+>", "", match.group(1))
        title = re.sub(r"^\s*\d+[\).]\s*", "", title)
        title = re.sub(r"\s+", " ", title).strip()
        if title and title.lower() not in {"частые вопросы", "faq"}:
            titles.append(title)
    return titles


def extract_paragraph_lengths(html: str) -> list[int]:
    lengths: list[int] = []
    for match in re.finditer(r"<p[^>]*>(.*?)</p>", html, flags=re.I | re.S):
        text = strip_html(match.group(1))
        words = re.findall(r"\b[а-яёa-zA-Z0-9-]+\b", text.lower())
        if words:
            lengths.append(len(words))
    return lengths


def extract_field(notes: str, field: str) -> str:
    pattern = re.compile(rf"^\s*{re.escape(field)}\s*:\s*(.+)$", flags=re.I | re.M)
    match = pattern.search(notes)
    return match.group(1).strip() if match else ""


def keyword_overlap(source: str, target: str) -> list[str]:
    words = re.findall(r"\b[а-яёa-zA-Z0-9-]{5,}\b", source.lower())
    stop = {"котор", "можно", "нужно", "будет", "после", "через", "такой", "такие", "стать"}
    keywords = [w for w in words if w not in stop]
    target_lower = target.lower()
    return sorted({word for word in keywords[:30] if word in target_lower})


def analyze_human_voice(article_dir: Path) -> dict[str, Any]:
    root = project_root()
    html_path = article_dir / "article.html"
    notes_path = article_dir / "research-notes.md"
    errors: list[str] = []
    warnings: list[str] = []

    if not html_path.is_file():
        return {
            "gate": "human-voice",
            "status": "BLOCK",
            "article_dir": repo_relative(article_dir, root),
            "errors": ["article.html not found"],
            "warnings": [],
            "metrics": {},
        }

    html = html_path.read_text(encoding="utf-8")
    text = strip_html(html)
    text_lower = text.lower()
    notes = notes_path.read_text(encoding="utf-8") if notes_path.is_file() else ""

    h2s = extract_h2_titles(html)
    h2_openers = [re.sub(r"[^\wа-яё-]+", "", h.lower().split()[0]) for h in h2s if h.split()]
    repeated_openers = sorted({op for op in h2_openers if op and h2_openers.count(op) >= 3})
    textbook_h2s = [h for h in h2s if h.lower().startswith(TEXTBOOK_H2_STARTS)]

    paragraph_lengths = extract_paragraph_lengths(html)
    avg_len = statistics.mean(paragraph_lengths) if paragraph_lengths else 0
    variance = statistics.pstdev(paragraph_lengths) if len(paragraph_lengths) > 1 else 0
    uniform_ratio = round(variance / avg_len, 2) if avg_len else 0

    concrete_hits = [marker for marker in CONCRETE_MARKERS if marker in text_lower]
    ai_opening_hits = [marker for marker in AI_OPENERS if marker in text_lower[:900]]
    blockquotes = re.findall(r"<blockquote[\s\S]*?</blockquote>", html, flags=re.I)
    fact_check_templates = [
        quote
        for quote in blockquotes
        if "материал проверен" in quote.lower() and "достоверность данных" in quote.lower()
    ]
    exactly_five_lists = len(re.findall(r"<ol[\s\S]*?(?:<li[\s\S]*?){5}</ol>", html, flags=re.I))

    reader_story = extract_field(notes, "reader_story")
    reader_pain = extract_field(notes, "reader_pain")
    reader_outcome = extract_field(notes, "reader_outcome")
    success_criteria = extract_field(notes, "success_criteria")
    voice_angle = extract_field(notes, "voice_angle")
    surprising_fact = extract_field(notes, "surprising_fact")
    story_overlap = keyword_overlap(reader_story, text) if reader_story else []
    pain_overlap = keyword_overlap(reader_pain, text) if reader_pain else []
    outcome_overlap = keyword_overlap(reader_outcome, text) if reader_outcome else []
    success_overlap = keyword_overlap(success_criteria, text) if success_criteria else []
    angle_overlap = keyword_overlap(voice_angle, text) if voice_angle else []
    surprising_overlap = keyword_overlap(surprising_fact, text) if surprising_fact else []
    pain_hits = [marker for marker in PAIN_MARKERS if marker in text_lower]
    outcome_hits = [marker for marker in OUTCOME_MARKERS if marker in text_lower]

    if ai_opening_hits:
        errors.append(f"AI-style opening phrases near lead: {ai_opening_hits}")
    if len(concrete_hits) < 2:
        errors.append("too few concrete human markers: need examples/practice/error/scenario language")
    if len(pain_hits) < 2:
        errors.append("reader pain is weak or invisible: article must name the problem it solves")
    if len(outcome_hits) < 3:
        errors.append("reader outcome is weak or invisible: article must promise and deliver a usable result")
    if repeated_openers:
        errors.append(f"repeated H2 openers make article formulaic: {repeated_openers}")
    if len(textbook_h2s) >= 2:
        errors.append(f"too many textbook H2 openings: {textbook_h2s[:3]}")
    if paragraph_lengths and uniform_ratio < 0.35:
        warnings.append(f"paragraph rhythm too uniform: variance/avg={uniform_ratio}")
    if fact_check_templates:
        warnings.append("Fact Check block uses a repeated template; vary wording while preserving facts")
    if exactly_five_lists >= 2:
        warnings.append("multiple exactly-5-step lists detected; vary list size when editorially possible")
    if reader_story and not story_overlap:
        errors.append("article does not appear to use reader_story from research-notes.md")
    if reader_pain and not pain_overlap:
        errors.append("article does not appear to use reader_pain from research-notes.md")
    if reader_outcome and not outcome_overlap:
        errors.append("article does not appear to use reader_outcome from research-notes.md")
    if success_criteria and not success_overlap:
        warnings.append("article weakly reflects success_criteria from research-notes.md")
    if voice_angle and not angle_overlap:
        warnings.append("article weakly reflects voice_angle from research-notes.md")
    if surprising_fact and not surprising_overlap:
        warnings.append("article weakly reflects surprising_fact from research-notes.md")
    if not notes_path.is_file():
        warnings.append("research-notes.md not found; cannot check story/angle grounding")

    status = "PASS" if not errors else "BLOCK"
    return {
        "gate": "human-voice",
        "status": status,
        "article_dir": repo_relative(article_dir, root),
        "errors": errors,
        "warnings": warnings,
        "metrics": {
            "h2_count": len(h2s),
            "repeated_h2_openers": repeated_openers,
            "textbook_h2_count": len(textbook_h2s),
            "paragraph_count": len(paragraph_lengths),
            "paragraph_avg_words": round(avg_len, 1) if avg_len else 0,
            "paragraph_variance_ratio": uniform_ratio,
            "concrete_markers": concrete_hits,
            "pain_markers": pain_hits,
            "outcome_markers": outcome_hits,
            "ai_opening_hits": ai_opening_hits,
            "reader_story_overlap": story_overlap,
            "reader_pain_overlap": pain_overlap,
            "reader_outcome_overlap": outcome_overlap,
            "success_criteria_overlap": success_overlap,
            "voice_angle_overlap": angle_overlap,
            "surprising_fact_overlap": surprising_overlap,
            "exactly_five_lists": exactly_five_lists,
            "fact_check_template_blocks": len(fact_check_templates),
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate article human voice and anti-template signals")
    ap.add_argument("--article-dir", type=Path, required=True)
    ap.add_argument("-o", "--output", type=Path, default=None)
    args = ap.parse_args()

    root = project_root()
    article_dir = args.article_dir if args.article_dir.is_absolute() else root / args.article_dir
    report = analyze_human_voice(article_dir)

    if args.output:
        output = args.output if args.output.is_absolute() else article_dir / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Human Voice Gate: {report['status']}")
    for error in report.get("errors") or []:
        print(f"ERROR: {error}", file=sys.stderr)
    for warning in report.get("warnings") or []:
        print(f"WARN: {warning}", file=sys.stderr)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
