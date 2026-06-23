# QA: B08 ii-chat-bot-dlya-biznesa-workflow

date: 2026-06-16
score_total: 90/100
core_eeat_lite: 18/20
link_verify: pass
research_notes_gate: pass
utility_gate: pass
human_voice_gate: pass
verdict: PASS

## Pain → solution → outcome

| Элемент | Где в статье |
|---------|----------------|
| **Боль** | Lead: no-code бот назвал скидку 30% без основания и не передал клиента при вопросе про аллергию; недели на «ТОП-15 конструкторов», галлюцинации по ценам, лиды не в CRM |
| **Решение** | H2 «Выберите задачу и канал» → «База ответов + запреты» → «Интенты и эскалация» → «n8n/Make: триггер, AI Agent, память, CRM» → «RAG + 50–100 тест-кейсов» |
| **Результат** | H2 «Проверьте запуск по метрикам FCR, CSAT и fallback»: 50–100 тест-кейсов PASS, ≥60% без оператора, эскалация при жалобах/low confidence, лиды в CRM, ответ <5 с |

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 20 | H2×6, primary «чат боты для бизнеса», FAQ 6, ol 10 шагов — OK |
| GEO / citability | 25 | 24 | TL;DR, 3 blockquote, 1 таблица, FAQ 6, workflow-схема; −1 нет второй таблицы |
| CORE-EEAT lite | 15 | 13 | 18/20; −2 за шаблонный блок «Материал проверен» |
| Human voice | 15 | 14 | 0 slop, Flesch RU 72.4; −1 warnings (2× списка по 5, uniform rhythm) |
| Fact safety | 15 | 13 | fact-check PASS; 2/10 чисел в fact-bank (Wordstat, MAX/Telegram в research-notes) |
| Contract HTML | 10 | 8 | linter PASS; −2 нет `<img>` с alt |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, research gate pass, utility gate pass, human voice pass — **выполнен**.

## CORE-EEAT lite: 18/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | Title/H1 закрывают «чат боты для бизнеса» + workflow |
| C02 | ✓ | Lead — direct answer с кейсом боли, без «в этой статье» |
| C03 | ✓ | Аудитория: малый бизнес, салоны/услуги, Telegram-аудитория |
| C04 | ✓ | RAG, business_connection_id, session_id, FCR/CSAT — на пальцах |
| O01 | ✓ | H2 совпадают с research-каркасом (6 шагов action outline) |
| O02 | ✓ | Outline: задача/канал → база → диалог → n8n/Make → RAG-тесты → метрики |
| O03 | ✓ | FAQ 6, queries из Wordstat/research |
| O04 | ✓ | ol (5+5), 1 таблица, ul, blockquotes |
| R01 | ✓ | TL;DR + workflow-схема + FAQ — standalone |
| R02 | ✓ | Wordstat 886/116/113, MAX лимиты, n8n 1.82+ — из research |
| R03 | ✓ | Нет выдуманных цен SaaS; 5 800 ₽/мес — kv-ai.ru в research |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «один use case → один канал → один workflow 7–14 дней» |
| E02 | ✓ | «Делайте / Не делайте» в каждой H2 |
| E03 | ✓ | CTA курс Make ×1, Telegram ×1 |
| Exp01 | ✓ | Режим B; reader_story в lead, не fake enterprise case |
| Exp02 | ✓ | Тон research, surprising_fact MAX vs «ии чат бот» |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | business_connection_id, session_id, модерация MAX, 152-ФЗ логи |
| Ept02 | ✓ | Internal links ×3: RAG B07, n8n B02, Make B06 |

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

- total: 6, failed: 0
- OK: internal RAG B07, n8n B02, Make B06, kv-ai.ru/obuchenie-po-make, t.me/maya_pro, kv-ai.ru/artur-horosheff

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 5 (TL;DR/таблица — допустимо)
- Flesch RU: 72.4 (Easy)
- see `slop-detector-report.json`

## Fact-check

- verdict: pass (10 extracted, 2 verified in fact-bank, 8 unverified — Wordstat, MAX/Telegram, 7–14 дней в research-notes, не blocker)
- see `fact-check-report.json`

## Cannibalization

- verdict: pass (0 issues, 8 articles in blog-dir)
- see `cannibalization-report.json`

## Utility gate

- article: PASS (`numbered_list_items: 10`, `h2_sections: 6`, `faq_h3: 6`, `tables: 1`, `blockquotes: 3`)
- topic: PASS (utility-gate-topic.json, research phase)

## Human voice gate

- status: PASS
- warnings: uniform paragraph rhythm; template fact-check block; 2 списка ровно по 5 пунктов
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
