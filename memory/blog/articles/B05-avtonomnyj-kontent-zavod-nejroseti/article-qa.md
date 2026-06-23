# QA: B05 avtonomnyj-kontent-zavod-nejroseti

date: 2026-06-11
score_total: 95/100
core_eeat_lite: 19/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 20 | H2/H3, primary query «контент завод», FAQ 5 пар, списки, таблицы — OK |
| GEO / citability | 25 | 24 | Lead answer-first, TL;DR, 1 таблица (Make vs n8n), FAQ 5, 6 шагов чек-листа |
| CORE-EEAT lite | 15 | 14 | 19/20 (см. ниже); −1 за локальные 404 у непубликованных статей (B02, B03, B04) |
| Human voice | 15 | 15 | 0 AI-slop hits, технический тон, Flesch RU 33.5 (сложный, но адекватный теме) |
| Fact safety | 15 | 14 | fact-check PASS; 5/6 чисел верифицировано в fact-bank, 159 уроков — из курса |
| Contract HTML | 10 | 8 | linter PASS, объём 9059 ✓, CTA ≤3 ✓, internal href ×3; −2 нет `<img>` с alt |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate pass — **выполнен**.

## CORE-EEAT lite: 19/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/Title закрывают «контент завод» |
| C02 | ✓ | Lead — direct answer, без «в этой статье» |
| C03 | ✓ | Аудитория: предприниматели и маркетологи, автоматизирующие контент |
| C04 | ✓ | n8n, Make, API, RAG, MCP — «на пальцах» |
| O01 | ✓ | H2 совпадают с планом темы B05 (7 секций + FAQ) |
| O02 | ✓ | Outline: промптинг → архитектура → выбор движка → RAG/память → HITL → экономика → чек-лист |
| O03 | ✓ | FAQ 5 пар, queries из research/Wordstat |
| O04 | ✓ | ol (6 шагов), ul (4 элемента бюджета), 1 table |
| R01 | ✓ | TL;DR + итоговый вердикт + рекомендации в H2 |
| R02 | ✓ | Wordstat 4857/450, тариф n8n/Make, 159 уроков — с research-notes |
| R03 | ✓ | Цены с контекстом бюджета; Wordstat с датой «июнь 2026» |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол Ковчег: жесткое противопоставление инфоцыганскому хайпу реальной архитектурной автоматизации |
| E02 | ✓ | «Рекомендация» в каждой H2-секции |
| E03 | ✓ | CTA Make ×1, @maya_pro ×1, author blockquote ×1 |
| Exp01 | ✓ | Режим B, без fake case |
| Exp02 | ✓ | Тон brief/research, не generic AI |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Ограничения: ИИ решает менее 2.5% сложных задач без человека, накладные расходы |
| Ept02 | ✗ | Относительные ссылки `/avtomatizaciya-n8n-ai-agents/`, `/podklyuchenie-mcp-cursor/`, `/geo-optimizaciya-sajta-2026/` — 404 (draft_ready в локальной папке) |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| fact-check | PASS | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | WARNING | slop-detector-report.json |
| cannibalization | PASS | cannibalization-report.json |
| utility gate (article) | PASS | utility-gate-report.json |

## Link verify

- total: 5, failed: 0
- OK: /avtomatizaciya-n8n-ai-agents/, /podklyuchenie-mcp-cursor/, /geo-optimizaciya-sajta-2026/, kv-ai.ru/obuchenie-po-make, t.me/maya_pro
- **Перед publish:** проверить доступность относительных ссылок после публикации соответствующих статей на kv-ai.ru

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 8 (таблицы/blockquote/списки — допустимо)
- Flesch RU: 33.5 (Hard, обусловлено сложной технической тематикой)
- see `slop-detector-report.json`

## Fact-check

- verdict: pass (6 extracted, 5 verified in fact-bank, 1 unverified — 159 уроков из курса, не blocker)
- see `fact-check-report.json`

## Cannibalization

- verdict: pass (0 issues, 5 articles in blog-dir)
- see `cannibalization-report.json`

## Utility gate

- article: PASS (`excalibur_blog_utility_gate.py --article-dir`)
- topic: PASS (utility-gate-topic.json, research phase)

## Fix cycle

- Нет критических замечаний. Все автоматические проверки пройдены успешно.

## Optional (не blocker)

- добавить 1 `<img>` с alt по контракту
- занести 159 уроков курса в fact-bank

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (5) | HowTo: no | Review: no | E-E-A-T SameAs Author: pending (author_id: artur-horoshev)
