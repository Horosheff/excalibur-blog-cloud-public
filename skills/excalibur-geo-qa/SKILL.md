---
name: excalibur-geo-qa
description: Excalibur BLOG GEO QA — fact-check, link verify, linter, slop, cannibalization, article-qa PASS.
---

# Excalibur BLOG — GEO QA

## Когда

После `article.html` + `article.meta.json` от Writer. **До** cover/schema (их делает директор параллельно после PASS).

## Скрипты (обязательно)

```bash
python scripts/excalibur_blog_research_notes_gate.py \
  --article-dir memory/blog/articles/<dir> \
  -o research-notes-gate.json

python scripts/excalibur_blog_fact_checker.py \
  memory/blog/articles/<dir>/article.html \
  -o memory/blog/articles/<dir>/fact-check-report.json

python scripts/excalibur_blog_link_verify.py \
  memory/blog/articles/<dir>/article.html \
  -o memory/blog/articles/<dir>/link-verify.json \
  --site-base https://YOUR_SITE

python scripts/excalibur_blog_html_linter.py \
  memory/blog/articles/<dir>/article.html \
  -o memory/blog/articles/<dir>/html-linter-report.json
```

HTML linter **блокирует оглавление в теле** (`<ol>/<ul>` с 3+ ссылками `href="#..."`). При fail — Writer удаляет TOC (после TL;DR сразу `<p>`).

```bash
python scripts/excalibur_blog_slop_detector.py \
  memory/blog/articles/<dir>/article.html \
  -o memory/blog/articles/<dir>/slop-detector-report.json

python scripts/excalibur_blog_cannibalization_guard.py \
  --article-dir memory/blog/articles/<dir>

python scripts/excalibur_blog_utility_gate.py \
  --article-dir memory/blog/articles/<dir> \
  --output utility-gate-report.json

python scripts/excalibur_blog_human_voice_gate.py \
  --article-dir memory/blog/articles/<dir> \
  -o human-voice-report.json
```

**Pass:** score ≥ 80, CORE-EEAT ≥ 16/20, link-verify pass, **research notes gate PASS**, **utility gate PASS**, **human voice gate PASS**. В `article-qa.md` отдельно зафиксируй: какая боль решена, где показано решение, какой результат получит читатель.

Schema и cover — **не** твоя зона (отдельные субагенты после PASS).
