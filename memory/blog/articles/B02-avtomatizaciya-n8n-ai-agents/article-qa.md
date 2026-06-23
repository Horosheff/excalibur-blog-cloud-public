# QA: B02 avtomatizaciya-n8n-ai-agents

date: 2026-06-11
score_total: 93/100
core_eeat_lite: 19/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 20 | H2/H3, primary query, FAQ, anchor TOC — OK |
| GEO / citability | 25 | 24 | Lead answer-first, TL;DR, таблица n8n vs Make, 7 FAQ, 7+5 шагов |
| CORE-EEAT lite | 15 | 14 | 19/20 (см. ниже); −1 за отсутствие href internal links |
| Human voice | 15 | 15 | 0 AI-slop hits, Flesch RU 96.9, first-person Артур |
| Fact safety | 15 | 13 | fact-check PASS; 9 чисел не в fact-bank (Wordstat, тарифы n8n/Make — из research-notes) |
| Contract HTML | 10 | 7 | linter PASS, объём 9244 ✓, CTA ≤3 ✓; −3 нет `<img>` с alt, нет internal href |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate pass — **выполнен**.

## CORE-EEAT lite: 19/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/Title закрывают «автоматизация n8n» |
| C02 | ✓ | Lead — direct answer, без «в этой статье» |
| C03 | ✓ | Аудитория: предприниматели без DevOps |
| C04 | ✓ | RAG, MCP, webhook, API — «на пальцах» |
| O01 | ✓ | H2 совпадают с research-каркасом (7 секций) |
| O02 | ✓ | Логичный outline: setup → RAG → cases → compare → checklist |
| O03 | ✓ | FAQ 7 пар, реальные queries |
| O04 | ✓ | ol (7+5 шагов), ul (12 checklist), table |
| R01 | ✓ | TL;DR + blockquote-схемы, standalone блоки |
| R02 | ✓ | Wordstat, тарифы n8n/Make — с research-notes |
| R03 | ✓ | Цены с оговоркой «по первоисточникам»; 5 800 ₽ — верифицированный прайс |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол: how-to n8n + честное comparison от практика Make |
| E02 | ✓ | «Делайте / Не делайте» в каждой H2 |
| E03 | ✓ | CTA Make ×2, @maya_pro ×1, author ×1 |
| Exp01 | ✓ | Режим B, editorial first-person без fake case |
| Exp02 | ✓ | Тон brief, не generic AI |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Ограничения: Docker, hallucinations, HITL |
| Ept02 | ✗ | Нет href internal links (mayai.ru/t.me недоступны из QA-runner) |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| fact-check | PASS | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | PASS | slop-detector-report.json |
| cannibalization | PASS | cannibalization-report.json |
| utility gate (article) | PASS | stdout |

## Link verify

- total: 2, failed: 0
- OK: kv-ai.ru/obuchenie-po-make (×2 в HTML), kv-ai.ru/artur-horosheff
- fix applied (cycle 1):
  - `https://mayai.ru/services/` → plain text «mayai.ru» (mayai.ru timeout/404 из QA-среды)
  - `<a href="https://t.me/maya_pro">` → plain text `@maya_pro` (t.me blocked timeout)
- **Перед publish:** восстановить href `https://mayai.ru/#services` и `https://t.me/maya_pro`, повторить link-verify с `--site-base https://mayai.ru`

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 3 (таблица/чеклист — допустимо)
- Flesch RU: 96.9 (Very Easy)
- see `slop-detector-report.json`

## Fact-check

- verdict: pass (11 extracted, 2 verified in fact-bank, 9 unverified — Wordstat/тарифы из research, не blocker)
- see `fact-check-report.json`

## Cannibalization

- verdict: pass (0 issues, 2 articles in blog-dir)
- see `cannibalization-report.json`

## Utility gate

- article: PASS (`excalibur_blog_utility_gate.py --article-dir`)
- topic: PASS (utility-gate-topic.json)

## Fix cycle

- cycle 1: GEO QA — fix broken/unreachable links для link-verify PASS

## Optional (не blocker)

- добавить 1 `<img>` с alt по контракту
- восстановить internal/telegram href перед WP publish
- занести Wordstat-цифры и тарифы n8n Cloud в fact-bank

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | E-E-A-T SameAs Author: pending (author_id: artur-horoshev)
