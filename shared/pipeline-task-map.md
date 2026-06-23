# Excalibur BLOG — карта задач и субагентов

Директор **не** Task. Все роли ниже — `Task(<name>)`.

## Схема

```text
[Д] Директор (чат)
  │
  ├─ 🔍 Task(excalibur-blog-scout)       ← Генерация / подбор свежих тем
  │
  ├─ shell: excalibur_blog_today.py
  ├─ shell: excalibur_blog_research_start.py
  │
  ├─ ① Task(excalibur-blog-research)
  ├─ ② Task(excalibur-blog-writer)
  ├─ ③ Task(excalibur-blog-geo-qa)
  │
  ├─ ④a Task(excalibur-blog-cover)  ─┐ параллель
  ├─ ④b Task(excalibur-blog-schema) ─┘
  │
  ├─ ⑤ Task(excalibur-blog-indexer)
  ├─ ⑥ Task(excalibur-blog-publish)   ← автоматически после Indexer (skip только publish:no)
  └─ ⑦ Task(excalibur-blog-fixer)     ← только если memory/pipeline-fix-queue.md содержит open incidents
```

## Таблица распределения


| Шаг | Кто          | Task name                 | Задачи                                                                                     | Артефакты                                                                                                 | Handoff / fragment                                |
| --- | ------------ | ------------------------- | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| 🔍  | **Scout**    | `excalibur-blog-scout`    | Поиск трендов 2026, Wordstat проверка, Jaccard-тест на уникальность                        | blog-topics.md (новые темы)                                                                               | —                                                 |
| 0   | **Директор** | — (shell)                 | дата, SERP, **utility gate темы**, article_dir, reserve topic                              | research-context.json, research-serp.json, published-articles.md status=in_progress                       | обновить таблицу статуса                          |
| ①   | **Research** | `excalibur-blog-research` | deep research на текущую дату, pain_solution_map, Wordstat, GitHub/docs/community evidence | research-notes.md, research-notes-gate.json                                                               | handoff `=== RESEARCH ===`                        |
| ②   | **Writer**   | `excalibur-blog-writer`   | human longread 8.5–9.5k: боль → решение → результат, FAQ HTML, meta_ab                     | article.html, article.meta.json                                                                           | handoff `=== WRITER ===`                          |
| ③   | **GEO QA**   | `excalibur-blog-geo-qa`   | QA-скрипты + research gate + utility gate + human voice gate, score ≥80                    | *-report.json, research-notes-gate.json, utility-gate-report.json, human-voice-report.json, article-qa.md | handoff `=== GEO QA ===`                          |
| ④a  | **Cover**    | `excalibur-blog-cover`    | ONE Kie API quad 2×2 i2i + design code + split → cover + 3 inline                          | canvas-quad.png, cover.png, inline-01..03, registry                                                       | fragment cover.md                                 |
| ④b  | **Schema**   | `excalibur-blog-schema`   | BlogPosting + FAQPage JSON-LD                                                              | schema.jsonld                                                                                             | fragment schema.md                                |
| ⑤   | **Indexer**  | `excalibur-blog-indexer`  | interlink --apply, llms.txt                                                                | article.html (links), llms*.txt, promotion-checklist                                                      | handoff `=== INDEXER ===`                         |
| ⑥   | **Publish**  | `excalibur-blog-publish`  | SSH WP post, featured, schema meta                                                        | wp-publish-result.json                                                                                    | handoff `=== PUBLISH ===` + published-articles.md |
| ⑦   | **Fixer**    | `excalibur-blog-fixer`    | open incidents → durable repo fixes                                                        | memory/pipeline-fix-queue.md, agents/skills/shared/scripts changes                                        | handoff/summary `=== FIXER ===`                   |


## Кто чем НЕ занимается


| Роль     | Запрещено                                       |
| -------- | ----------------------------------------------- |
| Research | писать article.html                             |
| Writer   | QA-скрипты, cover, schema, publish              |
| GEO QA   | править текст статьи (только FIX цикл → writer) |
| Cover    | schema, HTML статьи                             |
| Schema   | cover, HTML статьи                              |
| Indexer  | publish, переписывать body с нуля               |
| Publish  | писать/редактировать longread                   |
| Fixer    | publish, генерация статьи/картинок без incident |


## Параллель (только одна пара)

**④a Cover || ④b Schema** — после ③ QA PASS.

Нельзя параллелить: ①→②→③, ⑤ после ④, ⑥ после ⑤.

## Промпты для Директора (копировать в Task)

Добавляй к каждому Task-промпту:

```text
Если встретишь blocker/retry/tool error/workaround/переписывание артефакта из-за неясного контракта, допиши incident в memory/pipeline-fix-queue.md по shared/pipeline-incident-fix-contract.md. В итоговом handoff/fragment укажи incident_report: none | memory/pipeline-fix-queue.md#INC-...
```

### 🔍 Scout (Генератор свежих тем)

```text
Ты excalibur-blog-scout.
Прочитай agents/excalibur-blog-scout.md + skills/scout-excalibur-blog/SKILL.md + shared/editorial-utility-only.md.
1) python scripts/excalibur_blog_scout_helper.py --suggest-next
2) WebSearch Курсора — найди горячие тренды 2026 (ИИ, автоматизация, n8n, Cursor, Make)
3) Вызови wordstat_get_top_requests в user-mcp-kv для проверки показов в месяц и LSI-ключей
4) python scripts/excalibur_blog_scout_helper.py --check-query "<запрос>" (защита от каннибализации)
5) Сделай карточку темы и допиши (append) её в конец memory/topics/blog-topics.md.
```

### ① Research

```text
Ты excalibur-blog-research. topic_id: {ID}. article_dir из handoff.
Прочитай agents/excalibur-blog-research.md + skills/excalibur-research/SKILL.md + shared/editorial-utility-only.md.
Сначала utility gate темы. Вызови MCP-KV wordstat_get_top_requests для сбора спроса и LSI-ключей по primary_query.
Сделай deep research через WebSearch/WebFetch: конкуренты, official docs, GitHub repos/issues, community pain points, свежесть на today_iso.
Выход: research-notes.md с current-date source_table, Wordstat, github_evidence, reader_pain, reader_outcome, success_criteria, pain_solution_map, reader_story, voice_angle, surprising_fact, action_outline и research-notes-gate.json PASS.
Блок === EXCALIBUR BLOG RESEARCH ===. Не пиши article.html.
```

### ② Writer

```text
Ты excalibur-blog-writer. topic_id: {ID}.
Прочитай agents/excalibur-blog-writer.md + skills/writer-excalibur-blog/SKILL.md + shared/editorial-utility-only.md.
Только режим B: человеческая статья из research brief, reader_pain в lead, H2 закрывают pain_solution_map, success_criteria до FAQ, шаги, рекомендации, без воды. 8500–9500 символов.
Блок === EXCALIBUR BLOG WRITER ===. Не запускай QA и cover.
```

### ③ GEO QA

```text
Ты excalibur-blog-geo-qa. topic_id: {ID}.
Прочитай agents/excalibur-blog-geo-qa.md + skills/excalibur-geo-qa/SKILL.md.
Запусти все QA-скрипты + excalibur_blog_research_notes_gate.py + excalibur_blog_utility_gate.py + excalibur_blog_human_voice_gate.py. article-qa.md verdict PASS обязателен.
Блок === EXCALIBUR BLOG GEO QA ===. Не делай cover/schema.
```

### ④a Cover (параллель)

```text
Ты excalibur-blog-cover. topic_id: {ID}. article_dir из handoff.
Прочитай agents/excalibur-blog-cover.md + skills/cover-excalibur-blog/SKILL.md + shared/blog-cover-quad-canvas-contract.md.
1) excalibur_blog_hero_reference_url.py
2) excalibur_blog_quad_manifest.py --merge
3) правка cover/quad-manifest.json (hook, scene_hint, outfit агента)
4) excalibur_blog_cover_quad_prompt.py --write-batch
5) ONE Cursor MCP tool call: выбрать gpt-image-2 в Available Tools (server user-mcp-kv), arguments = jobs[0].mcp_args из quad-mcp-batch.json (input_urls обязателен)
   Если HTTP MCP вернул -32001 Request timed out: это не blocker с первой попытки.
   Не искать URL в cover/*: он появится там только после ручной записи quad-mcp-result.json.
   Проверить MCP tool log / expanded tool response / Cursor MCP Logs.
   Если generated URL уже виден — записать cover/quad-mcp-result.json вручную или передать URL сразу в apply.
   Если URL ещё нет — проверять MCP log короткими polling-проверками каждые 15–30 секунд, максимум 5 минут; не запускать длинное shell-ожидание одной командой.
   Повторять ONE quad request через MCP tool gpt-image-2 только если лог доступен и подтверждает, что URL не появился.
   Если MCP log недоступен агенту — COVER MCP RECOVERY NEEDED, нужен URL из лога; не retry вслепую.
   Максимум 2 попытки / общий бюджет 10 минут. Без URL не делать apply/split.
6) excalibur_blog_quad_apply.py --url ... --inject-html
Fragment .cursor/excalibur-blog-fragments/cover.md (=== EXCALIBUR BLOG COVER ===). Не 4 MCP. Не трогай schema.
```

### ④b Schema (параллель)

```text
Ты excalibur-blog-schema. topic_id: {ID}.
Прочитай agents/excalibur-blog-schema.md + skills/schema-excalibur-blog/SKILL.md.
schema.jsonld BlogPosting+FAQPage. Fragment .cursor/excalibur-blog-fragments/schema.md (=== EXCALIBUR BLOG SCHEMA ===). Не делай cover.
```

### ⑤ Indexer

```text
Ты excalibur-blog-indexer. topic_id: {ID}.
Прочитай agents/excalibur-blog-indexer.md + skills/indexer-excalibur-blog/SKILL.md.
interlinker --apply + llms generator. Блок === EXCALIBUR BLOG INDEXER === в handoff.
```

### ⑥ Publish (автоматически после Indexer)

```text
Ты excalibur-blog-publish. topic_id: {ID}. article_dir из handoff.
Прочитай agents/excalibur-blog-publish.md + skills/publish-excalibur-blog/SKILL.md + shared/excalibur-wp-publish-contract.md.
Preflight link-verify → dry-run → publish → обнови shared/published-articles.md + memory/blog/wp-publish-log.md.
Блок === EXCALIBUR BLOG PUBLISH === + permalink в PIPELINE DONE.
При HTTP timeout bootstrap — WebFetch fallback (см. skill).
```

### ⑦ Fixer (post-run, только если есть open incidents)

```text
Ты excalibur-blog-fixer.
Прочитай agents/excalibur-blog-fixer.md + skills/fixer-excalibur-blog/SKILL.md + shared/pipeline-incident-fix-contract.md.
Открой memory/pipeline-fix-queue.md, найди status: open по текущему run.
Сделай durable repo changes, чтобы следующая попытка не повторила ошибку: agents/.cursor/agents, skills/.cursor/skills, shared, scripts, templates, stable memory configs.
Запусти проверки, обнови incident statuses fixed|needs-human.
Блок === EXCALIBUR BLOG FIXER ===.
```

## Файлы субагентов


| name                    | agent-md                                                                  |
| ----------------------- | ------------------------------------------------------------------------- |
| excalibur-blog-research | [agents/excalibur-blog-research.md](../agents/excalibur-blog-research.md) |
| excalibur-blog-writer   | [agents/excalibur-blog-writer.md](../agents/excalibur-blog-writer.md)     |
| excalibur-blog-geo-qa   | [agents/excalibur-blog-geo-qa.md](../agents/excalibur-blog-geo-qa.md)     |
| excalibur-blog-cover    | [agents/excalibur-blog-cover.md](../agents/excalibur-blog-cover.md)       |
| excalibur-blog-schema   | [agents/excalibur-blog-schema.md](../agents/excalibur-blog-schema.md)     |
| excalibur-blog-indexer  | [agents/excalibur-blog-indexer.md](../agents/excalibur-blog-indexer.md)   |
| excalibur-blog-publish  | [agents/excalibur-blog-publish.md](../agents/excalibur-blog-publish.md)   |
| excalibur-blog-fixer    | [agents/excalibur-blog-fixer.md](../agents/excalibur-blog-fixer.md)       |


Cloud: те же имена в `.cursor/agents/`.