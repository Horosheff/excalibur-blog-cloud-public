# Excalibur BLOG — Cloud Automation Setup

Настройка запуска в **Cursor Cloud Agents / Automations** по образцу [kovcheg-office-cloud](https://github.com/ExampleOrg/kovcheg-office-cloud).

## Что запускаем

Пайплайн одной статьи:

```text
doctor + today + research_start → research → writer → geo-qa → cover||schema → indexer → publish (auto; skip только publish:no)
```

## Структура репозитория (как у Kovcheg Cloud)

```text
<PROJECT_ROOT>/
  AGENTS.md                          ← инструкции Cloud Agent
  CLOUD-AUTOMATION.md                ← этот файл
  .env.example
  .cursor/
    agents/                          ← Task types для Cloud
    skills/
    rules/
    excalibur-blog-handoff.md        ← runtime, не в git
    excalibur-blog-fragments/        ← cover + schema parallel
  agents/                            ← исходники плагина
  skills/
  shared/
  scripts/
  memory/
  .cursor-plugin/plugin.json
```

## Cursor docs

- [Cloud Agents setup](https://cursor.com/docs/cloud-agent/setup.md)
- [Secrets / env vars](https://cursor.com/docs/cloud-agent/setup.md#environment-variables-and-secrets)
- [Automations](https://cursor.com/docs/cloud-agent/automations.md)
- [Self-hosted pool](https://cursor.com/docs/cloud-agent/self-hosted-pool.md)
- [MCP in Cloud](https://cursor.com/docs/cloud-agent/capabilities.md#mcp-tools)

Локальная выжимка без внешней навигации: [`CURSOR-CLOUD-RUNBOOK.md`](CURSOR-CLOUD-RUNBOOK.md).

## Repo infrastructure

Cursor Cloud должен использовать `.cursor/environment.json`:

```json
{
  "install": "python3 -m pip install --user -r requirements.txt && python3 scripts/excalibur_blog_doctor.py",
  "start": "",
  "terminals": []
}
```

Опциональный GitHub Actions preflight лежит как пример: `shared/cloud-preflight-workflow.yml.example`.
Чтобы активировать его, скопируй файл в `.github/workflows/cloud-preflight.yml` после `gh auth refresh -s workflow` или через GitHub UI.

## Self-hosted worker

Нужен, если в облаке Cursor нет:

- MCP KV (`gpt-image-2` для обложек);
- SFTP/SSH к WordPress;
- стабильного web search для research.

```powershell
cd "<PROJECT_ROOT>"
# Set CURSOR_API_KEY in your shell or Cursor Cloud Secrets before starting the worker.
$env:EXCALIBUR_PROJECT_ROOT="<PROJECT_ROOT>"
agent worker start --pool --pool-name excalibur-blog --idle-release-timeout 600
```

## Secrets / env vars

Из `.env.example` + Cloud Dashboard:

| Variable | Зачем |
|----------|-------|
| `PUBLIC_SITE_URL` | link verify, recent WP posts |
| `SSH_*` | `excalibur_blog_wp_publish.py`; transport сразу SFTP/SSH |
| `EXCALIBUR_BLOG_ALLOW_PUBLISH` | `yes` только когда готовы публиковать |
| `EXCALIBUR_TOPIC_ID` | опционально фиксировать тему (иначе today.py предложит P0) |
| `EXCALIBUR_PROJECT_ROOT` | корень репо на worker |

Не коммитить: `memory/site.env.local`, реальные ключи MCP.

## Automation schedule

Cursor Automation → Schedule, пример:

```text
0 10,15,20 * * *
```

- Repository: ваш fork `excalibur-blog` / EXCALIBUR
- Worker pool: `excalibur-blog`
- Branch: `main`

## Automation prompt (шаблон)

```text
Ты работаешь в репозитории Excalibur BLOG.

Запусти полный пайплайн SEO/GEO статьи через оркестратора (Директор), не выполняя роли сам.

0. Прочитай AGENTS.md и shared/agent-pipeline-pitfalls.md.
0.1. Прочитай CURSOR-CLOUD-RUNBOOK.md и убедись, что работаешь в Cloud-ready repo.
1. python3 scripts/excalibur_blog_doctor.py — preflight окружения (для боевого publish: добавь --publish).
2. python3 scripts/excalibur_blog_today.py — зафиксируй дату и topic_id.
3. Сбрось .cursor/excalibur-blog-handoff.md одной строкой "# Excalibur BLOG — новая сессия".
4. Очисти .cursor/excalibur-blog-fragments/.
5. Если `EXCALIBUR_TOPIC_SELECTION=needs_scout` — запусти Task(excalibur-blog-scout), затем возьми новый topic_id.
6. python3 scripts/excalibur_blog_research_start.py --topic-id <из EXCALIBUR_SUGGESTED_TOPIC_ID или env/scout> — резервирует topic_id в `shared/published-articles.md` как `in_progress`.
7. Task(excalibur-blog-research) → current-date deep research: research-notes.md + pain_solution_map + research-notes-gate.json PASS.
8. Task(excalibur-blog-writer) → human article.html + meta from reader_pain/reader_story/voice_angle/surprising_fact, with clear reader outcome.
9. Task(excalibur-blog-geo-qa) → PASS + все QA JSON, включая human-voice-report.json.
10. ПАРАЛЛЕЛЬНО Task(excalibur-blog-cover) + Task(excalibur-blog-schema).
   Cover/schema пишут во fragments; перенеси в handoff.
   Cover: перед MCP обязательно пересобрать `quad-mcp-batch.json`; hard gate: `validation.prompt_chars <= 3500`, `reference_url_hosted` содержит `example.com` (не `example.com/assets`), `jobs[0].mcp_args.resolution == "2K"`. Если gate не проходит — не вызывать MCP, исправить batch. Image MCP должен быть client-timeout-safe. Если Available Tools содержит async image create/start + status/result — использовать async flow: create once → task_id → status/result → url. Если доступен только sync `gpt-image-2` — вызвать один раз с JSON arguments из `jobs[0].mcp_args`. Если sync call вернул `HTTP MCP -32001 Request timed out`, не retry вслепую и не искать URL в `cover/*`; проверить expanded tool response / Cursor MCP Logs. URL → записать `cover/quad-mcp-result.json`; task_id → использовать status/result tool. Если нет URL/task_id/status tool — `COVER MCP ASYNC BLOCKER`: backend должен дать async retrieval для позднего URL.
11. Task(excalibur-blog-indexer).
12. Task(excalibur-blog-publish) — **автоматически** после Indexer (skip только publish:no). Skill: publish-excalibur-blog. Обнови shared/published-articles.md.

Fallback: если Task types недоступны — generalPurpose per role (см. AGENTS.md).

Запрещено: single-agent pipeline, cover до QA PASS, секреты в handoff.

Финальный ответ: article_dir + QA verdict + publish URL или блокер.
```

## После каждого прогона

Проверь изменения:

- `shared/published-articles.md` (если publish)
- `memory/blog/excalibur-blog-run-log.md`
- артефакты в `memory/blog/articles/<topic_id>-<slug>/`

Если Automation через PR — merge PR, чтобы следующий run видел ledger.

## Локальная разработка плагина

Правки agents/skills делай в `agents/` и `skills/`, затем **синхронизируй в `.cursor/`**:

```powershell
Copy-Item agents\* .cursor\agents\ -Force
Copy-Item skills\* .cursor\skills\ -Recurse -Force
Copy-Item rules\* .cursor\rules\ -Force
```

Или добавь script `scripts/sync_cursor_cloud.ps1` при необходимости.
