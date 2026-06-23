# Excalibur BLOG Cloud Instructions

Язык работы: русский.

## Главное правило

Для полной SEO/GEO статьи **нельзя** выполнять весь пайплайн одним Cloud Agent.

Cloud Agent обязан оркестрировать через **Директора** (роль в чате, не Task) и запускать субагентов:

```text
shell today + research_start
  → excalibur-blog-research (research-notes-gate.json PASS)
  → excalibur-blog-writer (human article from research brief)
  → excalibur-blog-geo-qa (human-voice-report.json PASS)
  → excalibur-blog-cover || excalibur-blog-schema
  → excalibur-blog-indexer
  → excalibur-blog-publish (автоматически после Indexer; skip только publish:no)
 → excalibur-blog-fixer (если memory/pipeline-fix-queue.md содержит open incidents)
```

## Cloud Task fallback

Если Cloud API не принимает `excalibur-blog-research`, `excalibur-blog-writer`, … как Task types:

- **отдельный `Task(generalPurpose)` на каждую роль**;
- передай путь `.cursor/agents/<role>.md` и `.cursor/skills/<skill>/SKILL.md`;
- короткий контракт: входные файлы, маркер результата, запреты;
- один Task = одна роль;
- параллель `cover || schema` — **два отдельных Task** в одном сообщении.

Если недоступен даже `generalPurpose` Task:

`❌ БЛОКЕР: Cloud Agent не может запускать отдельные Task/subagents даже через generalPurpose. Single-agent pipeline запрещён.`

## Что считать ошибкой

- Parent сам пишет `article.html` вместо Task writer.
- Parent сам делает cover/schema вместо параллельных Task.
- Parent запускает cover||schema **до** GEO QA PASS.
- Writer стартует без `research-notes-gate.json` PASS.
- GEO QA пропускает `human-voice-report.json`.
- Publish без обновления `shared/published-articles.md`.

## Handoff и fragments

- Handoff: `.cursor/excalibur-blog-handoff.md`
- Параллельные роли (cover, schema) пишут во фрагменты:
  - `.cursor/excalibur-blog-fragments/cover.md`
  - `.cursor/excalibur-blog-fragments/schema.md`
- Директор переносит фрагменты в handoff.

Маркеры:

- `=== EXCALIBUR BLOG RESEARCH ===`
- `=== EXCALIBUR BLOG WRITER ===`
- `=== EXCALIBUR BLOG GEO QA ===`
- `=== EXCALIBUR BLOG COVER ===`
- `=== EXCALIBUR BLOG SCHEMA ===`
- `=== EXCALIBUR BLOG INDEXER ===`
- `=== EXCALIBUR BLOG PUBLISH ===`
- `=== EXCALIBUR BLOG FIXER ===`
- `=== EXCALIBUR BLOG (PIPELINE DONE) ===`

## Канонические пути

`<PROJECT_ROOT>` — корень репозитория (без `C:\Users\...`).

| Артефакт | Путь |
|----------|------|
| Плагин / контракты | `agents/`, `skills/`, `shared/`, `scripts/` |
| Runtime memory | `memory/` |
| Durable incident queue | `memory/pipeline-fix-queue.md` |
| Журнал публикаций | `shared/published-articles.md` |
| Cloud agents | `.cursor/agents/` |
| Cloud skills | `.cursor/skills/` |

Перед пайплайном прочитай `shared/agent-pipeline-pitfalls.md`.

## Preflight (обязательно)

```bash
python3 scripts/excalibur_blog_doctor.py
python3 scripts/excalibur_blog_today.py
python3 scripts/excalibur_blog_research_start.py --topic-id B01
```

Используй `EXCALIBUR_RUN_DATE`, `EXCALIBUR_SUGGESTED_TOPIC_ID` из today.py.
Если `python` недоступен — `python3`.
`research_start.py` обязан зарезервировать topic_id в `shared/published-articles.md` со status=`in_progress`; это защита от повторного выбора темы новым Cloud run.

## Research and human writing gates

- Research обязан сделать current-date deep research: `research_date == today_iso`, source table с `accessed_at`, Wordstat, GitHub/docs/community evidence, `reader_pain`, `reader_outcome`, `success_criteria`, `pain_solution_map`, `reader_story`, `voice_angle`, `surprising_fact`.
- После Research обязательно: `python scripts/excalibur_blog_research_notes_gate.py --article-dir <article_dir> -o research-notes-gate.json`.
- Writer пишет только после `research-notes-gate.json` PASS и обязан строить статью по связке: боль в lead → решение в H2 → понятный результат до FAQ.
- GEO QA обязательно запускает `excalibur_blog_human_voice_gate.py`; cover/schema стартуют только после PASS.

## Секреты

Только Cloud Secrets / env vars. Не печатать SSH/API ключи в handoff, PR, ответах.

- `SSH_*`, `PUBLIC_SITE_URL`, `EXCALIBUR_BLOG_ALLOW_PUBLISH`
- Publish transport: только SSH; legacy upload-алиасы не использовать.
- MCP через `${env:...}` в mcp.json

## Git hygiene

**Не коммитить:** `.cursor/excalibur-blog-handoff.md`, `shared/excalibur-blog-handoff.md`, `.cursor/excalibur-blog-fragments/`, `memory/site.env.local`, абсолютные пути Windows/macOS в отчётах.

**Коммитить после publish:** `shared/published-articles.md`, при необходимости артефакты статьи в `memory/blog/`.

## Incident memory и fixer loop

- Любой агент, который встретил blocker, retry, tool/API error, ручной workaround, переписывание артефакта из-за неясного контракта или user correction, обязан дописать incident в `memory/pipeline-fix-queue.md`.
- Формат и запреты: `shared/pipeline-incident-fix-contract.md`.
- В каждом handoff/fragment агент пишет `incident_report: none | memory/pipeline-fix-queue.md#INC-...`.
- После `PIPELINE DONE` или терминального blocker Директор проверяет очередь и запускает `Task(excalibur-blog-fixer)`.
- Fixer вносит durable repo changes в `agents/`, `.cursor/agents/`, `skills/`, `.cursor/skills/`, `shared/`, `scripts/`, templates или stable `memory/` configs, запускает проверки и закрывает incident как `fixed` или `needs-human`.

## Субагенты (.cursor/agents)

| name | skill |
|------|-------|
| excalibur-blog-research | excalibur-research |
| excalibur-blog-writer | writer-excalibur-blog |
| excalibur-blog-geo-qa | excalibur-geo-qa |
| excalibur-blog-cover | cover-excalibur-blog |
| excalibur-blog-schema | schema-excalibur-blog |
| excalibur-blog-indexer | indexer-excalibur-blog |
| excalibur-blog-publish | excalibur-wp-publish |
| excalibur-blog-fixer | fixer-excalibur-blog |

Директор: `.cursor/agents/excalibur-blog-director.md` + `director-excalibur-blog` skill — **не Task**.

Полная настройка worker/automation: `CLOUD-AUTOMATION.md`.

## Cursor Cloud specific instructions

Этот репозиторий подготовлен для Cursor Cloud Agent:

- repo-level инфраструктура: `.cursor/environment.json`;
- краткая выжимка документации Cursor Cloud: `CURSOR-CLOUD-RUNBOOK.md`;
- пример CI preflight: `shared/cloud-preflight-workflow.yml.example`.

Cloud Agent должен брать секреты только из Cursor Dashboard Secrets / env vars. Если для publish нет `EXCALIBUR_BLOG_ALLOW_PUBLISH=yes` или SSH/public site переменных, publish-агент обязан вернуть явный blocker, а не пытаться угадать доступы.
