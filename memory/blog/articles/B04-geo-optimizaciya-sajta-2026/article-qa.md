# QA: B04 geo-optimizaciya-sajta-2026

date: 2026-06-11
score_total: 94/100
core_eeat_lite: 19/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 20 | H2/H3, primary query «geo оптимизация», FAQ 7, чек-лист 32 пункта — OK |
| GEO / citability | 25 | 24 | Lead answer-first, TL;DR, 2 таблицы (SEO/GEO/AEO + SoV), FAQ 7, 5+5 шагов, robots blockquote |
| CORE-EEAT lite | 15 | 14 | 19/20 (см. ниже); −1 за B01 href (404, draft_ready) |
| Human voice | 15 | 15 | 0 AI-slop hits, Flesch RU 97.3, editorial first-person |
| Fact safety | 15 | 13 | fact-check PASS; 3/9 чисел в fact-bank (Wordstat, 60–90 мин, 160 — из research-notes) |
| Contract HTML | 10 | 8 | linter PASS, объём 8921 ✓, CTA ≤3 ✓, internal href ×2; −2 нет `<img>` с alt |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate pass — **выполнен**.

## CORE-EEAT lite: 19/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/Title закрывают «geo оптимизация» |
| C02 | ✓ | Lead — direct answer, без «в этой статье» |
| C03 | ✓ | Аудитория: маркетологи и владельцы сайтов DIY |
| C04 | ✓ | RAG, SoV, JSON-LD, GPTBot — «на пальцах» |
| O01 | ✓ | H2 совпадают с research-каркасом (7 секций + FAQ) |
| O02 | ✓ | Outline: GEO vs SEO → аудит → контент → Schema → чек-лист → SoV → next |
| O03 | ✓ | FAQ 7 пар, queries из research/Wordstat |
| O04 | ✓ | ol (5+5+32 шагов), 2 table, 5 blockquote |
| R01 | ✓ | TL;DR + схема аудита + robots example + Fact Check blockquote |
| R02 | ✓ | Wordstat 981/248, Princeton +30–40%, Habr RAG — с research-notes |
| R03 | ✓ | Цифры с оговорками («по оценке индустрии», Seer Interactive) |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол Ковчег: чек-лист 32 пункта + связка B01/B02/B03 |
| E02 | ✓ | «Делайте / Не делайте» в каждой H2 |
| E03 | ✓ | CTA Make ×1, @maya_pro ×1, author blockquote ×1 |
| Exp01 | ✓ | Режим B, без fake case |
| Exp02 | ✓ | Тон brief/research, не generic AI |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Ограничения: B01 draft, llms.txt опционален, 3–6 недель на SoV |
| Ept02 | ✗ | B01 `/primer-seo-stati/` — 404 (draft_ready); plain text до publish B01 |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| fact-check | PASS | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | PASS | slop-detector-report.json |
| cannibalization | PASS | cannibalization-report.json |
| utility gate (article) | PASS | utility-gate-report.json |

## Link verify

- total: 5, failed: 0
- OK: search.google.com/test/rich-results, mayai.ru/avtomatizaciya-n8n-ai-agents/, mayai.ru/podklyuchenie-mcp-cursor/, kv-ai.ru/obuchenie-po-make, t.me/maya_pro
- fix applied (cycle 1):
  - `<a href="/primer-seo-stati/">` → plain text «пример SEO-статьи (B01, href после публикации)» (HTTP 404 — B01 draft_ready)
- **Перед publish:** восстановить href `/blog/primer-seo-stati/` или `/primer-seo-stati/` после публикации B01, повторить link-verify

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 4 (таблицы/blockquote — допустимо)
- Flesch RU: 97.3 (Very Easy)
- see `slop-detector-report.json`

## Fact-check

- verdict: pass (9 extracted, 3 verified in fact-bank, 6 unverified — Wordstat/длительности из research, не blocker)
- see `fact-check-report.json`

## Cannibalization

- verdict: pass (0 issues, 4 articles in blog-dir)
- see `cannibalization-report.json`

## Utility gate

- article: PASS (`numbered_list_items: 42`, `h2_sections: 7`, `faq_h3: 7`, `tables: 2`)
- topic: PASS (utility-gate-topic.json, research phase)

## Fix cycle

- cycle 1: GEO QA — `<pre><code>` robots.txt → blockquote (html-linter); B01 404 → plain text (link-verify)

## Optional (не blocker)

- добавить 1 `<img>` с alt по контракту
- восстановить href B01 после публикации B01 на mayai.ru
- занести Wordstat-цифры в fact-bank

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | E-E-A-T SameAs Author: pending (author_id: elena-kovaleva)
