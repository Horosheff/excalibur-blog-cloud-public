# QA: B10 ollama-lokalnaya-llm-dlya-biznesa

date: 2026-06-17
score_total: 91/100
core_eeat_lite: 18/20
link_verify: pass
research_notes_gate: pass
utility_gate: pass
human_voice_gate: pass
verdict: PASS

## Pain → solution → outcome

| Элемент | Где в статье |
|---------|----------------|
| **Боль** | Lead: IT-директор тянет 32B на 8 ГБ VRAM, открывает порт 11434 в LAN — утечка в логах и ответы медленнее облака; аналитик с OLLAMA_HOST=0.0.0.0 — коллега видит модели без пароля |
| **Решение** | H2 «Выберите сценарий» → «Сверьте железо с моделью» → «Установите и проверьте инференс» → «OpenAI API к n8n/Cursor» → «Закройте периметр 11434» |
| **Результат** | H2 «Пройдите чек-лист запуска»: ollama ps + nvidia-smi, curl /v1/chat/completions, smoke-test n8n, порт не в интернет, 20 тест-кейсов + правило эскалации на облако |

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 20 | H2×6, primary «ollama», FAQ 6, ol 11 шагов — OK |
| GEO / citability | 25 | 24 | TL;DR, 4 blockquote, 2 таблицы, FAQ 6, схема интеграции; −1 нет `<img>` с alt |
| CORE-EEAT lite | 15 | 13 | 18/20; −2 за шаблонный блок «Материал проверен» |
| Human voice | 15 | 14 | 0 slop, Flesch RU 89.5; −1 warnings (2× списка по 5, template fact-check) |
| Fact safety | 15 | 13 | fact-check PASS; 2/11 чисел в fact-bank (Wordstat, Ollama 0.30 в research-notes) |
| Contract HTML | 10 | 7 | linter PASS; −3 нет `<img>` с alt |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, research gate pass, utility gate pass, human voice pass — **выполнен**.

## CORE-EEAT lite: 18/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | Title/H1 закрывают «ollama» + workflow до API |
| C02 | ✓ | Lead — direct answer с двумя кейсами боли, без «в этой статье» |
| C03 | ✓ | Аудитория: IT-директор, малый бизнес, агентство |
| C04 | ✓ | VRAM, API, OLLAMA_HOST, human-in-the-loop — на пальцах |
| O01 | ✓ | H2 совпадают с research action outline (6 шагов) |
| O02 | ✓ | Outline: сценарий → железо → install → API → security → чек-лист |
| O03 | ✓ | FAQ 6, queries из Wordstat/research |
| O04 | ✓ | ol (6+5), 2 таблицы, ul, blockquotes |
| R01 | ✓ | TL;DR + схема интеграции + FAQ — standalone |
| R02 | ✓ | Wordstat 32 669/5 854/782, issue #13814, Ollama 0.30 — из research |
| R03 | ✓ | Нет выдуманных цен SaaS |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «workflow, не рейтинг моделей» |
| E02 | ✓ | «Делайте / Не делайте» в H2 security и hardware |
| E03 | ✓ | CTA курс Make ×1, artur-horosheff ×1 |
| Exp01 | ✓ | Режим B; reader_story в lead (аналитик + IT-директор) |
| Exp02 | ✓ | Тон research, surprising_fact ollama ps vs nvidia-smi |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | 152-ФЗ, OLLAMA_HOST, порт 11434 без auth, логи без PII |
| Ept02 | ✓ | Internal links ×3: n8n B02, MCP B03, RAG B07 |

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

- total: 5, failed: 0
- OK: /avtomatizaciya-n8n-ai-agents/, /podklyuchenie-mcp-cursor/, /postroenie-rag-sistemy-vektornaya-baza/, kv-ai.ru/obuchenie-po-make, kv-ai.ru/artur-horosheff

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 4 (lead/таблицы — допустимо)
- Flesch RU: 89.5 (Very Easy)
- see `slop-detector-report.json`

## Fact-check

- verdict: pass (11 extracted, 2 verified in fact-bank, 9 unverified — Wordstat, issue #13814, VRAM в research-notes, не blocker)
- see `fact-check-report.json`

## Cannibalization

- verdict: pass (0 issues, 10 articles in blog-dir)
- see `cannibalization-report.json`

## Utility gate

- article: PASS (`numbered_list_items: 11`, `h2_sections: 6`, `faq_h3: 6`, `tables: 2`, `blockquotes: 4`)
- topic: PASS (utility-gate-topic.json, research phase)

## Human voice gate

- status: PASS
- warnings: template fact-check block; 2 списка ровно по 5 пунктов
- reader_story / pain / outcome overlap: strong
- see `human-voice-report.json`

## Fix cycle

- cycle 0: правок `article.html` не потребовалось — все скрипты PASS с первого прогона

## Optional (не blocker)

- добавить 1 `<img>` с alt по контракту
- варьировать длину нумерованных списков (не оба по 5)
- перефразировать шаблонный блок «Материал проверен»

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (6) | HowTo: no | Review: no | E-E-A-T SameAs Author: pending (author_id: artur-horoshev)
