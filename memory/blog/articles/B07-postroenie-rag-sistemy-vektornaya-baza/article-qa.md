# QA: B07 postroenie-rag-sistemy-vektornaya-baza

date: 2026-06-16
score_total: 93/100
core_eeat_lite: 18/20
link_verify: pass
research_notes_gate: pass
utility_gate: pass
human_voice_gate: pass
verdict: PASS

## Pain → solution → outcome

| Элемент | Где в статье |
|---------|----------------|
| **Боль** | Lead: 200 регламентов в Chroma, retrieval вернул неполный чанк про возвраты — бот ответил уверенно и неверно; демо RAG без цитаты источника |
| **Решение** | H2 «Решите RAG vs контекст» → «Разбейте на чанки» → «pgvector/Qdrant/Chroma» → «эмбеддинги + hybrid» → «retrieval + rerank» → «Python/n8n + golden set» |
| **Результат** | H2 «Как понять, что RAG работает»: ≥8/10 на golden set с файлом/разделом, отказ при пустом retrieval, таблица время/стоимость до/после rerank |

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 20 | H2×8, primary «rag система», FAQ 6, ol 14 шагов — OK |
| GEO / citability | 25 | 25 | TL;DR, 4 blockquote, 2 таблицы, FAQ 6, workflow-схемы |
| CORE-EEAT lite | 15 | 13 | 18/20; −2 за шаблонный блок «Материал проверен» |
| Human voice | 15 | 14 | 0 slop, Flesch RU 88.3; −1 warnings (2× списка по 5 шагов, template fact-check) |
| Fact safety | 15 | 13 | fact-check PASS; 3/13 чисел в fact-bank (остальное из research-notes / Wordstat) |
| Contract HTML | 10 | 8 | linter PASS после замены `<code>`→`<b>`; −2 нет `<img>` с alt |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, research gate pass, utility gate pass, human voice pass — **выполнен**.

## CORE-EEAT lite: 18/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | Title/H1 закрывают «rag система» + workflow |
| C02 | ✓ | Lead — direct answer с кейсом боли, без «в этой статье» |
| C03 | ✓ | Аудитория: команды, строящие корпоративный RAG |
| C04 | ✓ | RAG, эмбеддинги, HNSW, BM25, rerank — на пальцах |
| O01 | ✓ | H2 совпадают с research-каркасом (9 шагов action outline) |
| O02 | ✓ | Outline: решение → чанкинг → store → hybrid → chain → deploy → eval |
| O03 | ✓ | FAQ 6, queries из Wordstat/research |
| O04 | ✓ | ol (5+5+4), 2 таблицы, blockquotes |
| R01 | ✓ | TL;DR + 3 схемы workflow + FAQ — standalone |
| R02 | ✓ | Wordstat 2125, pgvector HNSW 2000 dim, тренд long context — из research |
| R03 | ✓ | Нет выдуманных цен; метрики 4/10→9/10 из reader_story research |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «убил RAG длинным контекстом — откат в проде» |
| E02 | ✓ | «Делайте / Не делайте» в каждой H2 |
| E03 | ✓ | CTA курс Make ×1 |
| Exp01 | ✓ | Режим B; «я пробовал» = voice_angle, не fake enterprise case |
| Exp02 | ✓ | Тон research, reader_story в lead |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | pgvector dim limits, failure modes, agentic RAG после eval |
| Ept02 | ✓ | Internal links ×2: `/avtomatizaciya-n8n-ai-agents/`, `/podklyuchenie-mcp-cursor/` |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| research-notes gate | PASS | research-notes-gate.json |
| fact-check | PASS | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | PASS | slop-detector-report.json |
| cannibalization | PASS | cannibalization-report.json |
| utility gate (article) | PASS | utility-gate-report.json |
| human voice gate | PASS | human-voice-report.json |

## Link verify

- total: 3, failed: 0
- OK: internal n8n-agents, internal MCP Cursor, kv-ai.ru/obuchenie-po-make

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 5 (таблицы/lead — допустимо)
- Flesch RU: 88.3 (Very Easy)
- see `slop-detector-report.json`

## Fact-check

- verdict: pass (13 extracted, 3 verified in fact-bank, 10 unverified — pgvector dim, Wordstat, chunk metrics в research-notes, не blocker)
- see `fact-check-report.json`

## Cannibalization

- verdict: pass (0 issues, 7 articles in blog-dir)
- see `cannibalization-report.json`

## Utility gate

- article: PASS (`numbered_list_items: 14`, `h2_sections: 8`, `faq_h3: 6`, `tables: 2`, `blockquotes: 4`)
- topic: PASS (utility-gate-topic.json, research phase)

## Human voice gate

- status: PASS
- warnings: template fact-check block; 2 списка ровно по 5 пунктов
- reader_story / pain / outcome overlap: strong
- see `human-voice-report.json`

## Fix cycle

- cycle 1: заменён запрещённый `<code>` на `<b>` (html-linter FAIL → PASS); остальные скрипты без правок контента

## Optional (не blocker)

- добавить 1 `<img>` с alt по контракту
- варьировать длину нумерованных списков (не все по 5)
- перефразировать шаблонный блок «Материал проверен»

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (6) | HowTo: no | Review: no | E-E-A-T SameAs Author: pending (author_id: artur-horoshev)
