# QA: B06 make-ai-agents-mcp-avtomatizaciya

date: 2026-06-16
score_total: 94/100
core_eeat_lite: 19/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 20 | H2/H3, primary query «автоматизация make», FAQ 7, ol 12 шагов — OK |
| GEO / citability | 25 | 24 | Lead answer-first, TL;DR, 3 blockquote-схемы, FAQ 7, 6+6 шагов; −1 нет таблиц |
| CORE-EEAT lite | 15 | 14 | 19/20 (см. ниже); −1 за pricing credits не в fact-bank (есть в research-notes) |
| Human voice | 15 | 15 | 0 AI-slop hits, Flesch RU 77.5, практический тон без fake case |
| Fact safety | 15 | 13 | fact-check PASS; 2/5 чисел не в fact-bank (1 000 / 10 000 credits — make.com/pricing в research) |
| Contract HTML | 10 | 8 | linter PASS, объём 9348 ✓, CTA ×1 ✓, internal href ×2 ✓; −2 нет `<img>` с alt |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate pass — **выполнен**.

## CORE-EEAT lite: 19/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | Lead/TL;DR закрывают «автоматизация make» |
| C02 | ✓ | Первый абзац — direct answer, без «в этой статье» |
| C03 | ✓ | Аудитория: бизнес, маркетинг, операционные процессы |
| C04 | ✓ | MCP, JSON, scope, API, HITL — «на пальцах» |
| O01 | ✓ | H2 совпадают с research-каркасом (процесс → схема → сборка → Agent → MCP Server/Client → security → чек-лист) |
| O02 | ✓ | Outline: выбор процесса → гибрид workflow → пошаговая сборка → MCP → HITL → метрики |
| O03 | ✓ | FAQ 7 пар, queries из research/Wordstat |
| O04 | ✓ | ol (6+6 шагов), ul (4 пункта security), blockquotes |
| R01 | ✓ | TL;DR + схема workflow + author blockquote — standalone блоки |
| R02 | ✓ | HITL <2.5%, timeout 25–40 с / 40 мин, Make pricing — с research-notes |
| R03 | ✓ | Цены credits с первоисточника make.com/pricing (research); без выдуманных % |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол: безопасный гибрид deterministic + Agent + MCP + approval (не клон SERP) |
| E02 | ✓ | Практические «делайте / не делайте» в каждой H2 |
| E03 | ✓ | CTA курс Make ×1, author blockquote ×1 |
| Exp01 | ✓ | Режим B, без fake «я внедрил» |
| Exp02 | ✓ | Тон brief/research, не generic AI |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Ограничения: scopes, credits, HITL, timeout, не давать агенту всё |
| Ept02 | ✓ | Internal links ×2: `/podklyuchenie-mcp-cursor/`, `/avtomatizaciya-n8n-ai-agents/` (200 на mayai.ru) |

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

- total: 3, failed: 0
- OK: mayai.ru/podklyuchenie-mcp-cursor/, mayai.ru/avtomatizaciya-n8n-ai-agents/, kv-ai.ru/obuchenie-po-make

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 4 (lead/blockquote — допустимо)
- Flesch RU: 77.5 (Easy)
- see `slop-detector-report.json`

## Fact-check

- verdict: pass (5 extracted, 3 verified in fact-bank, 2 unverified — 1 000 / 10 000 credits из make.com/pricing в research-notes, не blocker)
- see `fact-check-report.json`

## Cannibalization

- verdict: pass (0 issues, 6 articles in blog-dir)
- see `cannibalization-report.json`

## Utility gate

- article: PASS (`numbered_list_items: 12`, `h2_sections: 9`, `faq_h3: 7`, `blockquotes: 3`)
- topic: PASS (utility-gate-topic.json, research phase)

## Fix cycle

- cycle 0: все скрипты PASS без правок `article.html`

## Optional (не blocker)

- добавить 1 `<img>` с alt по контракту
- занести Make pricing credits (1 000 / 10 000) в fact-bank

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | E-E-A-T SameAs Author: pending (author_id: artur-horoshev)
