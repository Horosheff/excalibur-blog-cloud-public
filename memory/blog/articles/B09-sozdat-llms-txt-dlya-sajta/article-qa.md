# QA: B09 sozdat-llms-txt-dlya-sajta

date: 2026-06-16
score_total: 91/100
core_eeat_lite: 18/20
link_verify: pass
research_notes_gate: pass
utility_gate: pass
human_voice_gate: pass
verdict: PASS

## Pain → solution → outcome

| Элемент | Где в статье |
|---------|--------------|
| **Боль** | Lead: маркетолог боится, что без llms.txt сайт пропадёт из ответов нейросетей, путает файл с robots.txt и не понимает, что реально положить в файл. |
| **Решение** | H2 идут как практический маршрут: развести SEO-обещание и задачу файла → отобрать 10-30 URL → собрать Markdown-шаблон → не смешивать robots/sitemap/llms.txt → выложить и проверить отдачу → решить про llms-full.txt и генератор → настроить поддержку. |
| **Результат** | До FAQ есть явный критерий готовности: файл открывается по `https://domain.ru/llms.txt`, внутри H1, описание, 2-5 разделов, ссылки с пояснениями и Optional; нет конфликта с robots.txt, HTML-ошибки и server error в Lighthouse. |

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 19 | H2 x7, FAQ x6, primary query раскрыт; минус 1 за отсутствие дополнительных внутренних ссылок на статьи блога. |
| GEO / citability | 25 | 23 | TL;DR, таблица сравнения, шаблон llms.txt, workflow, FAQ; минус 2 за компактный набор источников в самом HTML. |
| CORE-EEAT lite | 15 | 14 | 18/20: есть авторская проверка, факты и ограничения; минус 1 за шаблонный fact-check block. |
| Human voice | 15 | 15 | human voice PASS, 0 slop hits, Flesch RU 79.0, конкретные маркеры и reader_story overlap сильные. |
| Fact safety | 15 | 13 | fact-check PASS; 4 факта, 3 verified, 1 unverified non-critical (`137 210` есть в research-notes, не в fact-bank). |
| Contract HTML | 10 | 7 | linter PASS после QA-fix; минус 3 за необходимость заменить forbidden `<pre><code>`. |

**Порог PASS:** score >=80, CORE-EEAT >=16/20, link-verify pass, research gate pass, utility gate pass, human voice pass — **выполнен**.

## CORE-EEAT lite: 18/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1 и мета закрывают запрос `llms txt` и интент "как создать / пример / чек-лист". |
| C02 | ✓ | Lead начинается с боли и reader_story, без абстрактного "в этой статье". |
| C03 | ✓ | Аудитория ясна: владелец сайта, маркетолог, агентство/фрилансер, не разработчик уровня core infra. |
| C04 | ✓ | Технические термины объяснены: AI-агент, API, robots/sitemap/llms.txt. |
| O01 | ✓ | H2 следуют action_outline и pain_solution_map из research-notes. |
| O02 | ✓ | Структура ведёт от решения "делать без SEO-мифа" к публикации, проверке и поддержке. |
| O03 | ✓ | FAQ x6 закрывает Wordstat/secondary queries: создать, robots.txt, AI-ответы, sitemap, llms-full, обновление. |
| O04 | ✓ | Есть ol 6 шагов, ul чеклист, таблица, blockquote, FAQ. |
| R01 | ✓ | TL;DR и "как понять, что задача решена" дают standalone answer. |
| R02 | ✓ | Использованы research facts: Google Search Central, Lighthouse Agentic Browsing, Ahrefs May 2026. |
| R03 | ✓ | Нет обещаний ранжирования/цитирования; ограничения проговорены до первого H2 и в FAQ. |
| R04 | ✓ | FAQ отвечает в первом предложении и не уходит в продажу. |
| E01 | ✓ | Угол "low-cost housekeeping, не волшебная SEO-кнопка" сохранён. |
| E02 | ✓ | H2 дают практические действия: отобрать, собрать, не смешивать, выложить, решить, настроить. |
| E03 | ✓ | CTA аккуратный: Make workflow и Telegram по одному разу, без давления. |
| Exp01 | ✓ | Article mode B: практический чек-лист с историей боли в lead. |
| Exp02 | ✓ | Surprising fact Ahrefs/Lighthouse раскрыт в первых абзацах. |
| Exp03 | ✓ | Slop detector: 0 cliches, 0 over-long sentences. |
| Ept01 | ✓ | Пример Markdown-шаблона и проверочный workflow применимы сразу. |
| Ept02 | ✗ | Нет межстатейной перелинковки на соседние темы блога; ожидаемо до Indexer, не blocker GEO QA. |

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
- OK: Google Search Central, Chrome Lighthouse, llmstxt.org, kv-ai.ru/obuchenie-po-make, t.me/maya_pro

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 0
- Flesch RU: 79.0 (Easy)
- see `slop-detector-report.json`

## Fact-check

- verdict: pass
- extracted: 4; verified: 3; unverified: 1
- unverified: `137 210` не найден в `memory/brief/fact-bank.md`, но подтверждён в `research-notes.md` source_table/current_fact_checks; не blocker.

## Cannibalization

- verdict: pass
- issues: 0
- checked: 9 article metadata definitions in `memory/blog/articles`

## Utility gate

- article: PASS (`numbered_list_items: 6`, `h2_sections: 7`, `faq_h3: 6`, `tables: 1`, `blockquotes: 5`)
- errors/warnings: none

## Human voice gate

- status: PASS
- errors/warnings: none
- concrete markers: "например", "на практике", "типичная ошибка", "в реальном проекте", "часто ломается"
- reader_story / pain / outcome / success criteria overlap: strong

## Fix cycle

- cycle 1: HTML linter rejected forbidden `<pre><code>` in the Markdown template block. Replaced it with whitelist-safe `<blockquote><p><br>` markup while preserving the template content.
- `article.meta.json` char_count updated to 9515 after the QA-fix.

## Optional (не blocker)

- Indexer can add contextual internal links to related blog articles.
- Fact-bank could include the Ahrefs `137 210` number to reduce future fact-check noise.

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (6) | HowTo: no | Review: no | E-E-A-T SameAs Author: pending (author_id: artur-horoshev)
