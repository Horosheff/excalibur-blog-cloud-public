#!/usr/bin/env python3
"""Utility-only editorial gate for Excalibur BLOG topics and articles."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


from excalibur_repo_paths import repo_relative


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_topic_card(topics_path: Path, topic_id: str) -> dict[str, str]:
    text = topics_path.read_text(encoding="utf-8")
    pattern = rf"##\s+{re.escape(topic_id)}\s+—[^\n]*\n(.*?)(?=\n---|\n##\s+[A-Z]\d+|\Z)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if not match:
        raise ValueError(f"topic card not found: {topic_id}")

    block = match.group(1)

    def field(name: str, default: str = "") -> str:
        m = re.search(rf"-\s*\*\*{re.escape(name)}:\*\*\s*(.+)", block, re.IGNORECASE)
        return m.group(1).strip() if m else default

    return {
        "topic_id": topic_id.upper(),
        "priority": field("priority"),
        "slug": field("slug"),
        "h1": field("h1"),
        "primary_query": field("primary_query"),
        "search_intent": field("search_intent"),
        "article_mode": field("article_mode"),
        "h2_outline": field("h2_outline"),
    }


def strip_html(html: str) -> str:
    text = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


def extract_h2_titles(html: str) -> list[str]:
    titles = []
    for match in re.finditer(r"<h2[^>]*>(.*?)</h2>", html, flags=re.I | re.S):
        title = re.sub(r"<[^>]+>", "", match.group(1))
        title = re.sub(r"\s+", " ", title).strip()
        if title and title.lower() not in {"частые вопросы", "faq"}:
            titles.append(title)
    return titles


def is_actionable_h2(title: str) -> bool:
    t = title.lower()
    action_tokens = [
        "как", "почему", "зачем", "сколько", "где", "чеклист", "чек-лист", "шаг", "инструкция", "руководство",
        "выбор", "настройка", "сравнение", "сравните", "выберите", "настройте", "запустите", "создайте",
        "соберите", "проверьте", "оптимизируйте", "избегайте", "внедрите", "используйте", "оптимизация",
        "запуск", "создание", "сбор", "проверка", "внедрение", "использование", "структура", "что делать",
        "не делать", "ошибки", "ошибок", "этап", "рекомендац", "советы", "правила"
    ]
    if any(tok in t for tok in action_tokens):
        return True
    words = [w.strip(".,!?\"'") for w in t.split()]
    for w in words:
        if w.endswith(("йте", "ите", "емся", "имся", "ешь", "ишь", "ть", "ти")):
            # basic check for imperative or infinitive action verbs
            if len(w) > 3:
                return True
    return False


def count_markers(text: str, markers: list[str]) -> int:
    hay = text.lower()
    return sum(hay.count(marker.lower()) for marker in markers)


def gate_topic(topic: dict[str, str], policy: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    intent = (topic.get("search_intent") or "").strip().lower()
    allowed = [x.lower() for x in policy.get("allowed_search_intent") or []]
    rejected = [x.lower() for x in policy.get("rejected_search_intent") or []]

    if intent in rejected:
        errors.append(f"search_intent={intent!r} в rejected")
    if intent and intent not in allowed:
        errors.append(f"search_intent={intent!r} не в allowed {allowed}")

    mode = (topic.get("article_mode") or "").strip().upper()
    allowed_modes = [str(x).upper() for x in policy.get("allowed_article_mode") or ["B"]]
    if mode and mode not in allowed_modes:
        errors.append(f"article_mode={mode} не разрешён (utility-only: {allowed_modes})")

    title_blob = " ".join(
        [
            topic.get("h1", ""),
            topic.get("primary_query", ""),
            topic.get("slug", ""),
        ]
    ).lower()
    title_patterns = policy.get("topic_title_must_match") or []
    if title_patterns and not any(p.lower() in title_blob for p in title_patterns):
        errors.append("h1/primary_query не содержит маркер практической темы (как/чек-лист/гайд/…)")

    if not topic.get("h2_outline") and not topic.get("primary_query"):
        warnings.append("нет h2_outline — writer должен построить action-outline в research")

    status = "PASS" if not errors else "BLOCK"
    return {
        "gate": "topic",
        "topic_id": topic.get("topic_id"),
        "status": status,
        "search_intent": intent,
        "article_mode": mode,
        "errors": errors,
        "warnings": warnings,
    }


def gate_article(article_dir: Path, policy: dict[str, Any]) -> dict[str, Any]:
    html_path = article_dir / "article.html"
    meta_path = article_dir / "article.meta.json"
    errors: list[str] = []
    warnings: list[str] = []

    if not html_path.is_file():
        return {"gate": "article", "status": "BLOCK", "errors": ["article.html not found"], "warnings": []}

    html = html_path.read_text(encoding="utf-8")
    plain = strip_html(html)

    req = policy.get("article_required_signals") or {}
    ol_blocks = list(re.finditer(r"<ol[\s\S]*?</ol>", html, flags=re.I))
    li_in_ol = sum(len(re.findall(r"<li[\s>]", m.group(0), flags=re.I)) for m in ol_blocks)
    ul_lists = len(re.findall(r"<ul[\s\S]*?</ul>", html, flags=re.I))
    tables = len(re.findall(r"<table[\s\S]*?</table>", html, flags=re.I))
    blockquotes = len(re.findall(r"<blockquote[\s\S]*?</blockquote>", html, flags=re.I))
    faq_h3 = len(re.findall(r"<h3[^>]*>", html, flags=re.I))

    markers = policy.get("recommendation_markers_ru") or []
    marker_count = count_markers(plain, markers)

    min_steps = int(req.get("min_numbered_steps") or 5)
    if li_in_ol < min_steps:
        errors.append(f"мало нумерованных шагов: {li_in_ol} < {min_steps}")

    min_h2 = int(req.get("min_actionable_h2") or 3)
    h2s = extract_h2_titles(html)
    if len(h2s) < min_h2:
        errors.append(f"мало H2-секций: {len(h2s)} < {min_h2}")
    else:
        actionable_h2s = [h for h in h2s if is_actionable_h2(h)]
        if len(actionable_h2s) < min_h2:
            errors.append(
                f"мало практических H2-секций с действием: {len(actionable_h2s)} < {min_h2}. "
                f"Найдено: {h2s}. Заголовки H2 должны мотивировать к действию (глаголы, как/чек-лист/сравнение)."
            )

    min_faq = int(req.get("min_faq_pairs") or 5)
    if faq_h3 < min_faq:
        warnings.append(f"FAQ h3={faq_h3}, ожидалось ≥{min_faq}")

    min_rec = int(req.get("min_recommendation_markers") or 8)
    if marker_count < min_rec:
        errors.append(f"мало action-маркеров в тексте: {marker_count} < {min_rec}")

    pain_markers = policy.get("pain_markers_ru") or []
    outcome_markers = policy.get("outcome_markers_ru") or []
    pain_count = count_markers(plain, pain_markers)
    outcome_count = count_markers(plain, outcome_markers)

    min_pain = int(req.get("min_pain_markers") or 2)
    if pain_count < min_pain:
        errors.append(f"слабо раскрыта боль читателя: pain_markers={pain_count} < {min_pain}")

    min_outcome = int(req.get("min_outcome_markers") or 3)
    if outcome_count < min_outcome:
        errors.append(f"слабо раскрыта польза/результат: outcome_markers={outcome_count} < {min_outcome}")

    if req.get("requires_workflow_or_table_or_checklist"):
        has_utility_block = bool(tables or blockquotes or ul_lists >= 2 or "→" in html)
        if not has_utility_block:
            errors.append("нет workflow (→/blockquote), таблицы или чеклиста (ul)")

    water = policy.get("water_phrases_ru") or []
    water_hits = [p for p in water if p.lower() in plain]
    if len(water_hits) >= 2:
        errors.append(f"вода/штампы: {water_hits[:5]}")
    elif water_hits:
        warnings.append(f"1 water phrase: {water_hits[0]}")

    meta = load_json(meta_path) if meta_path.is_file() else {}
    
    # ----------------------------------------------------
    # Meta A/B/AEO Headline & Description Validation
    # ----------------------------------------------------
    meta_ab = meta.get("meta_ab")
    meta_ab_rules = policy.get("meta_ab_rules") or {}
    if not meta_ab:
        errors.append("В article.meta.json отсутствует обязательная секция 'meta_ab' для CTR/AEO оптимизации заголовков.")
    else:
        # title_seo check
        t_seo = meta_ab.get("title_seo", "")
        if not t_seo:
            errors.append("meta_ab.title_seo не заполнен")
        else:
            seo_len = len(t_seo)
            if seo_len < meta_ab_rules.get("title_seo_min_len", 35) or seo_len > meta_ab_rules.get("title_seo_max_len", 75):
                warnings.append(f"meta_ab.title_seo длина {seo_len} вне {meta_ab_rules.get('title_seo_min_len')}-{meta_ab_rules.get('title_seo_max_len')} симв.")
            
            p_query = meta.get("primary_query", "")
            if p_query:
                pq_words = [w.lower().strip(".,!?\"'") for w in p_query.split() if len(w) > 2]
                t_seo_lower = t_seo.lower()
                missing_pq_words = [w for w in pq_words if w not in t_seo_lower]
                if missing_pq_words:
                    warnings.append(f"meta_ab.title_seo не содержит ключевые слова из primary_query: {missing_pq_words}")

        # title_ctr check
        t_ctr = meta_ab.get("title_ctr", "")
        if not t_ctr:
            errors.append("meta_ab.title_ctr не заполнен")
        else:
            ctr_len = len(t_ctr)
            if ctr_len < meta_ab_rules.get("title_ctr_min_len", 40) or ctr_len > meta_ab_rules.get("title_ctr_max_len", 100):
                warnings.append(f"meta_ab.title_ctr длина {ctr_len} вне {meta_ab_rules.get('title_ctr_min_len')}-{meta_ab_rules.get('title_ctr_max_len')} симв.")
            
            has_emoji = any(ord(char) > 0x2000 for char in t_ctr)
            has_hook = has_emoji or "?" in t_ctr or "!" in t_ctr
            if meta_ab_rules.get("title_ctr_must_have_emoji_or_hook") and not has_hook:
                warnings.append("meta_ab.title_ctr рекомендуется добавить эмодзи или хук (?, !)")

        # title_aeo check
        t_aeo = meta_ab.get("title_aeo", "")
        if not t_aeo:
            errors.append("meta_ab.title_aeo не заполнен")
        else:
            aeo_len = len(t_aeo)
            if aeo_len < meta_ab_rules.get("title_aeo_min_len", 35) or aeo_len > meta_ab_rules.get("title_aeo_max_len", 90):
                warnings.append(f"meta_ab.title_aeo длина {aeo_len} вне {meta_ab_rules.get('title_aeo_min_len')}-{meta_ab_rules.get('title_aeo_max_len')} симв.")
            
            aeo_lower = t_aeo.lower()
            is_question = "?" in t_aeo or any(aeo_lower.startswith(q) for q in ["как", "что", "почему", "зачем", "сколько", "где", "какой", "какие", "какая", "кто"])
            if meta_ab_rules.get("title_aeo_must_be_question") and not is_question:
                warnings.append("meta_ab.title_aeo (AEO/ИИ заголовок) должен содержать вопросительное слово или '?'")

        # description_seo check
        d_seo = meta_ab.get("description_seo", "")
        if d_seo:
            d_len = len(d_seo)
            if d_len < meta_ab_rules.get("description_seo_min_len", 100) or d_len > meta_ab_rules.get("description_seo_max_len", 180):
                warnings.append(f"meta_ab.description_seo длина {d_len} вне {meta_ab_rules.get('description_seo_min_len')}-{meta_ab_rules.get('description_seo_max_len')} симв.")

    mode = str(meta.get("article_mode") or "").upper()
    if mode and mode not in [str(x).upper() for x in policy.get("allowed_article_mode") or ["B"]]:
        errors.append(f"article_mode={mode} — utility-only требует B")

    char_count = meta.get("char_count")
    if isinstance(char_count, int) and (char_count < 8500 or char_count > 9500):
        warnings.append(f"char_count={char_count} вне 8500–9500")

    status = "PASS" if not errors else "BLOCK"
    return {
        "gate": "article",
        "article_dir": repo_relative(article_dir, project_root()),
        "status": status,
        "metrics": {
            "numbered_list_items": li_in_ol,
            "h2_sections": len(h2s),
            "faq_h3": faq_h3,
            "tables": tables,
            "blockquotes": blockquotes,
            "ul_lists": ul_lists,
            "action_markers": marker_count,
            "pain_markers": pain_count,
            "outcome_markers": outcome_count,
            "water_hits": water_hits,
        },
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Utility-only editorial gate")
    ap.add_argument("--topic-id", default="", help="Validate topic card in blog-topics.md")
    ap.add_argument("--article-dir", default="", help="Validate article.html utility signals")
    ap.add_argument("--policy", default="memory/brief/editorial-policy.json")
    ap.add_argument("--output", default="", help="Write JSON report")
    args = ap.parse_args()

    root = project_root()
    policy_path = Path(args.policy)
    if not policy_path.is_absolute():
        policy_path = root / policy_path
    policy = load_json(policy_path)

    reports: list[dict[str, Any]] = []

    if args.topic_id:
        topics_path = root / "memory/topics/blog-topics.md"
        topic = parse_topic_card(topics_path, args.topic_id.strip())
        reports.append(gate_topic(topic, policy))

    if args.article_dir:
        article_dir = Path(args.article_dir)
        if not article_dir.is_absolute():
            article_dir = root / article_dir
        reports.append(gate_article(article_dir, policy))

    if not reports:
        print("❌ UTILITY GATE: specify --topic-id and/or --article-dir", file=sys.stderr)
        return 1

    overall = "PASS" if all(r["status"] == "PASS" for r in reports) else "BLOCK"
    payload = {"policy_id": policy.get("policy_id"), "overall": overall, "reports": reports}

    if args.output:
        out = Path(args.output)
        if not out.is_absolute() and args.article_dir:
            base = Path(args.article_dir)
            if not base.is_absolute():
                base = root / base
            out = base / out if not str(out).startswith("memory/") else root / out
        elif not out.is_absolute():
            out = root / out
        save_json(out, payload)

    for rep in reports:
        label = rep.get("topic_id") or rep.get("article_dir")
        print(f"{rep['gate']} {label}: {rep['status']}")
        for err in rep.get("errors") or []:
            print(f"  ERROR: {err}")
        for warn in rep.get("warnings") or []:
            print(f"  WARN: {warn}")

    if overall != "PASS":
        print("❌ UTILITY GATE BLOCKER", file=sys.stderr)
        return 1

    print("OK UTILITY GATE PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
