# Cursor Cloud Agent Pipeline с нуля: универсальный шаблон для любого плагина/автоматизации

Документ для урока: как спроектировать **любой** agent/subagent pipeline так, чтобы он работал в **Cursor Cloud** через **GitHub**: загрузил репозиторий, подключил Secrets, запустил Cloud Agent/Automation, получил проверяемые артефакты и PR/коммиты.

> Это не инструкция только для Excalibur BLOG. Ниже универсальный каркас, который можно адаптировать под SEO-пайплайн, генератор документов, автотесты, CRM-автоматизацию, Telegram-ботов, WordPress-паблишер, контент-завод, DevOps-проверки или любой другой workflow.

---

## 1. Главная идея

Cloud-ready pipeline = не “один агент всё делает в голове”, а **репозиторий с контрактами, ролями, скриптами и проверками**.

Правильная архитектура:

```text
GitHub repo
  → Cursor Cloud VM clones repo
  → repo-level environment installs deps
  → Director/orchestrator reads AGENTS.md
  → Director runs shell preflight
  → Director launches subagents by roles
  → each role writes artifacts + PASS/FAIL report
  → gates validate before next stage
  → publish/deploy step runs only after gates
  → fixer loop records and fixes repeated pipeline failures
  → changes are committed/pushed through GitHub
```

Ключевой принцип:

> Всё, что агенту нужно знать и повторять, должно лежать в Git: `AGENTS.md`, `.cursor/environment.json`, `.cursor/agents/`, `.cursor/skills/`, `shared/`, `scripts/`, `memory/` templates.  
> Всё секретное должно лежать в Cursor Dashboard Secrets, а не в Git.

---

## 2. Что Cursor Cloud делает через GitHub

Cursor Cloud Agent работает так:

1. Подключается к GitHub/GitLab репозиторию через Cursor GitHub App / integration.
2. Клонирует repo в изолированную Ubuntu VM.
3. Берёт environment config из `.cursor/environment.json` или из сохранённого Cloud environment.
4. Выполняет install/start commands.
5. Работает с файлами, запускает shell, вызывает MCP/tools.
6. Пушит изменения обратно в GitHub:
   - обычно в ветку `cursor/...` и PR;
   - либо прямо в выбранную branch, если запуск настроен на current branch / main.

Для учебного проекта лучше сначала работать через PR. Для production automation можно запускать на `main`, если вы осознанно хотите автокоммиты.

---

## 3. Минимальная структура репозитория

```text
my-cloud-pipeline/
  AGENTS.md
  README.md
  requirements.txt / package.json
  .gitignore

  .cursor/
    environment.json
    rules/
      orchestrator.mdc
    agents/
      my-director.md
      my-research.md
      my-writer.md
      my-qa.md
      my-publish.md
      my-fixer.md
    skills/
      director-my-pipeline/
        SKILL.md
      research-my-pipeline/
        SKILL.md
      writer-my-pipeline/
        SKILL.md
      qa-my-pipeline/
        SKILL.md
      publish-my-pipeline/
        SKILL.md
      fixer-my-pipeline/
        SKILL.md

  agents/
    my-director.md
    my-research.md
    my-writer.md
    my-qa.md
    my-publish.md
    my-fixer.md

  skills/
    director-my-pipeline/
      SKILL.md
    ...

  shared/
    pipeline-task-map.md
    pipeline-handoff.template.md
    pipeline-incident-fix-contract.md
    agent-pipeline-pitfalls.md

  scripts/
    doctor.py
    start_run.py
    validate_research.py
    validate_article.py
    publish.py

  memory/
    pipeline-fix-queue.md
    runs/
      .gitkeep
```

### Почему две копии `agents/` и `.cursor/agents/`

- `agents/` и `skills/` удобно считать исходниками.
- `.cursor/agents/` и `.cursor/skills/` — то, что Cloud Task/subagent увидит как project-level agents/skills.
- Если правите agent/skill, синхронизируйте обе стороны.

Можно упростить и хранить только `.cursor/agents` / `.cursor/skills`, но для учебного проекта лучше явно показать обе зоны.

---

## 4. `.cursor/environment.json`

Это repo-level настройка Cloud VM.

Минимальный Python-проект:

```json
{
  "install": "python3 -m pip install --user -r requirements.txt && python3 scripts/doctor.py",
  "start": "",
  "terminals": []
}
```

Node-проект:

```json
{
  "install": "npm ci && npm run doctor",
  "start": "",
  "terminals": []
}
```

Docker-проект:

```json
{
  "build": {
    "dockerfile": "Dockerfile",
    "context": ".."
  },
  "install": "npm ci",
  "start": "sudo service docker start",
  "terminals": []
}
```

Правила:

- `install` должен быть **идемпотентным**.
- Не писать секреты в файлы.
- Не запускать production publish/deploy в `install`.
- `doctor.py` должен проверять окружение и давать понятный PASS/FAIL.

---

## 5. `.gitignore`

Минимум:

```gitignore
.env
.env.local
*.local
__pycache__/
*.pyc
node_modules/
tmp/

# runtime handoff / fragments
.cursor/my-pipeline-handoff.md
.cursor/my-pipeline-fragments/

# local secrets
memory/site.env.local
```

Коммитить можно:

- contracts;
- templates;
- generated public artifacts, если они нужны следующему run;
- ledger/status files без secrets.

Не коммитить:

- API keys;
- FTP/SSH passwords;
- Cursor API keys;
- MCP tokens;
- raw private URLs, если они считаются secrets в вашем проекте;
- runtime handoff, если он содержит transient details.

---

## 6. `AGENTS.md`: главный Cloud contract

`AGENTS.md` — первое место, которое читает Cloud Agent.

Шаблон:

```markdown
# My Pipeline Cloud Instructions

Язык работы: русский.

## Главное правило

Полный production pipeline нельзя выполнять одним агентом.
Cloud Agent обязан работать как Director/orchestrator и запускать отдельные роли:

```text
doctor + start_run
  → my-research
  → my-writer
  → my-qa
  → my-assets || my-schema
  → my-indexer
  → my-publish
  → my-fixer, если есть open incidents
```

## Что считать ошибкой

- Parent сам делает работу роли вместо subagent.
- Следующий этап стартует без PASS gate предыдущего.
- Publish/deploy без ledger update.
- Secrets попали в handoff/commit/log.

## Canonical paths

| Artifact | Path |
|----------|------|
| Agents source | `agents/` |
| Cloud agents | `.cursor/agents/` |
| Skills source | `skills/` |
| Cloud skills | `.cursor/skills/` |
| Shared contracts | `shared/` |
| Scripts/gates | `scripts/` |
| Runtime memory | `memory/` |
| Incident queue | `memory/pipeline-fix-queue.md` |

## Preflight

```bash
python3 scripts/doctor.py
python3 scripts/start_run.py --run-id <id>
```

## Secrets

Secrets только через Cursor Dashboard Secrets / env vars.
Не печатать ключи в handoff, PR, logs.

Required env:

- `PUBLIC_SITE_URL`
- `PUBLISH_ALLOW=yes|no`
- `API_TOKEN_X`

## Incident memory

Если агент встретил blocker/retry/tool error/workaround, он пишет incident в:

`memory/pipeline-fix-queue.md`

Формат:

`shared/pipeline-incident-fix-contract.md`
```

---

## 7. Director: роль оркестратора

Director — это не обычный worker. Он:

- читает `AGENTS.md`;
- запускает preflight shell commands;
- создаёт runtime handoff;
- запускает subagents;
- проверяет gates;
- переносит fragments;
- запускает fixer loop.

Файл:

```text
agents/my-director.md
.cursor/agents/my-director.md
skills/director-my-pipeline/SKILL.md
.cursor/skills/director-my-pipeline/SKILL.md
```

Director-agent template:

```markdown
---
name: my-director
description: "Director: orchestrates My Pipeline, runs shell preflight, launches subagents."
model: inherit
readonly: false
is_background: false
---

Ты — Director. Ты не выполняешь роли сам.

## Handoff

- Runtime: `.cursor/my-pipeline-handoff.md`
- Template: `shared/pipeline-handoff.template.md`
- В начале run полностью пересоздай handoff.

## Algorithm

1. `python3 scripts/doctor.py`
2. `python3 scripts/start_run.py --run-id <id>`
3. Task(my-research)
4. Validate research gate.
5. Task(my-writer)
6. Task(my-qa)
7. If QA PASS, run my-assets and my-schema in parallel.
8. Task(my-indexer)
9. Task(my-publish), unless `publish:no`.
10. If `memory/pipeline-fix-queue.md` has `status: open`, Task(my-fixer).

## Forbidden

- No nested Director task.
- No single-agent full pipeline.
- No publish before QA PASS.
- No secrets in handoff.
```

---

## 8. Subagents: роли

Subagent нужен, когда:

- роль имеет отдельный контекст;
- роль может быть проверена по артефактам;
- роль нельзя смешивать с другими этапами;
- можно запускать параллельно независимые ветки.

Пример subagent:

```markdown
---
name: my-research
description: "Research: collects sources and writes research-notes.md."
model: inherit
readonly: false
is_background: false
---

**Язык:** русский.

## Incident memory

Если был blocker/retry/tool error/workaround, допиши incident в:
`memory/pipeline-fix-queue.md`

В финальном handoff-блоке укажи:

```text
incident_report: none | memory/pipeline-fix-queue.md#INC-...
```

## Tasks

1. Read `memory/runs/<run-id>/context.json`.
2. Collect sources.
3. Write `research-notes.md`.
4. Run `python3 scripts/validate_research.py --run-dir <dir>`.
5. Append `=== MY PIPELINE RESEARCH ===` to handoff.

## Not your zone

- Do not write final article.
- Do not publish.
- Do not launch nested Task.

## Skill

`skills/research-my-pipeline/SKILL.md`
```

---

## 9. Skills: подробные runbook-и

Agent-md должен быть коротким. Skill — подробным.

```text
skills/research-my-pipeline/SKILL.md
.cursor/skills/research-my-pipeline/SKILL.md
```

Template:

```markdown
---
name: research-my-pipeline
description: Research skill for My Pipeline.
---

# Research My Pipeline

## Input

- `memory/runs/<run-id>/context.json`
- `shared/editorial-policy.md`

## Steps

1. Verify run dir.
2. Search sources.
3. Build source table.
4. Write `research-notes.md`.
5. Run validation.

## Output contract

```text
research_date:
source_table:
reader_pain:
reader_outcome:
action_outline:
verdict: PASS
```

## Blockers

- missing context;
- no sources;
- validation FAIL.
```

---

## 10. Handoff и fragments

Runtime handoff нужен, чтобы Director видел состояние pipeline.

`shared/pipeline-handoff.template.md`:

```markdown
# My Pipeline — new session

`run_started_at`:
`run_id`:
`run_dir`:
`publish`: yes

## Status

| Step | Agent | Status | Time |
|------|-------|--------|------|
| 0 | shell start_run | pending | |
| 1 | my-research | pending | |
| 2 | my-writer | pending | |
| 3 | my-qa | pending | |
| 4 | my-assets || my-schema | pending | |
| 5 | my-publish | pending | |
| 6 | my-fixer | pending | |

## Incident memory

`incident_queue`: memory/pipeline-fix-queue.md

Each block must include:

```text
incident_report: none | memory/pipeline-fix-queue.md#INC-...
```

=== MY PIPELINE DONE ===
run_id:
run_dir:
qa:
publish:
incident_queue:
```

### Fragments for parallel roles

Если две роли запускаются параллельно, они не должны писать в один handoff одновременно.

```text
.cursor/my-pipeline-fragments/assets.md
.cursor/my-pipeline-fragments/schema.md
```

Director после завершения обоих переносит fragments в handoff.

---

## 11. Scripts и gates

Cloud pipeline должен проверяться скриптами, а не только “ощущением агента”.

Минимальный набор:

```text
scripts/
  doctor.py
  start_run.py
  validate_research.py
  validate_article.py
  validate_assets.py
  publish.py
```

### `doctor.py`

Проверяет окружение:

- Python/Node version;
- dependencies;
- наличие folders;
- env vars, но без вывода значений;
- доступность optional tools;
- write permissions.

Вывод:

```text
OK dependency X
OK env PUBLIC_SITE_URL configured
SUMMARY errors=0 warnings=0
```

### Gate script

Gate должен:

- возвращать exit code `0` на PASS;
- exit code `1` на FAIL;
- писать JSON report;
- иметь понятную ошибку.

Пример:

```bash
python3 scripts/validate_article.py --run-dir memory/runs/R001 -o article-qa.json
```

Report:

```json
{
  "status": "PASS",
  "score": 91,
  "checks": {
    "links": "PASS",
    "html": "PASS"
  }
}
```

---

## 12. Incident memory и fixer loop

Это защита от повторных трат токенов на одну и ту же ошибку.

Файл:

```text
memory/pipeline-fix-queue.md
```

Контракт:

```text
shared/pipeline-incident-fix-contract.md
```

Когда агент пишет incident:

- tool/API error;
- retry;
- ручной workaround;
- stale docs;
- validation failed;
- секрет/ENV не настроен;
- prompt был слишком жёсткий/неясный;
- пришлось исправлять артефакт из-за плохого контракта.

Incident format:

```markdown
## INC-YYYYMMDD-HHMM-role-short-slug
status: open
run_date: YYYY-MM-DD
role: my-agent
run_id: R001
severity: low | medium | high | blocker
category: prompt | script | docs | env | api | handoff | qa | publish | other

### What went wrong
- ...

### How the agent recovered this run
- ...

### Durable fix needed before next run
- ...

### Suggested files to inspect/change
- `path`

### Secrets
- none recorded

### Fixer resolution
- pending
```

Fixer после pipeline:

1. Читает open incidents.
2. Меняет durable sources:
   - `agents/`;
   - `.cursor/agents/`;
   - `skills/`;
   - `.cursor/skills/`;
   - `shared/`;
   - `scripts/`;
   - templates;
   - stable `memory/` configs.
3. Запускает проверки.
4. Меняет status на `fixed` или `needs-human`.

---

## 13. Secrets и env vars

Все секреты — только в Cursor Dashboard → Cloud Agents → Secrets.

Примеры:

```text
PUBLIC_SITE_URL=https://example.com
PUBLISH_ALLOW=yes
API_TOKEN=...
SSH_HOST=...
SSH_USER=...
SSH_PASS=...
```

В Git можно хранить только names, не values:

```markdown
Required env:
- `PUBLIC_SITE_URL`
- `PUBLISH_ALLOW`
- `API_TOKEN`
```

Если Cursor secret scanner считает `PUBLIC_SITE_URL` secret, то в committed artifacts используйте:

```text
[REDACTED]
```

или env placeholder:

```text
${PUBLIC_SITE_URL}
```

---

## 14. MCP для Cloud

MCP tools в Cloud лучше подключать как HTTP MCP.

Правила:

- не hardcode tokens;
- использовать `${env:MY_TOKEN}`;
- не давать агенту лишние tools;
- если tool долгий, нужен async flow: create → task_id → status/result;
- если sync tool timeout, не retry вслепую, сначала проверить task_id/result.

Пример `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "my-api": {
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${env:MY_API_TOKEN}"
      }
    }
  }
}
```

Для stdio MCP убедитесь, что runtime установлен в Cloud VM через `.cursor/environment.json`.

---

## 15. Automations

Cursor Automations запускают Cloud Agents по:

- schedule/cron;
- GitHub event;
- PR comment;
- webhook;
- Slack/Linear/Sentry/PagerDuty events.

Первый безопасный режим:

```text
Trigger: manual или schedule 1 раз в день
Repository: ваш GitHub repo
Branch: main
Prompt: полный automation prompt
Publish flag: no / dry-run
```

Production режим:

```text
Branch: main
Publish flag: yes
Secrets configured
Doctor publish preflight PASS
```

---

## 16. Automation prompt template

```text
Ты работаешь в GitHub repo <REPO_NAME> в Cursor Cloud.

Запусти полный pipeline через Director. Не выполняй роли сам.

0. Прочитай AGENTS.md, shared/agent-pipeline-pitfalls.md, CURSOR-CLOUD-RUNBOOK.md.
1. Запусти python3 scripts/doctor.py.
2. Создай runtime handoff из shared/pipeline-handoff.template.md.
3. Запусти python3 scripts/start_run.py --run-id <id>.
4. Task(my-research) → research gate PASS.
5. Task(my-writer) → article/output artifact.
6. Task(my-qa) → QA PASS.
7. Если QA PASS, параллельно Task(my-assets) + Task(my-schema).
8. Task(my-indexer).
9. Task(my-publish), если publish yes.
10. Если memory/pipeline-fix-queue.md содержит status: open, Task(my-fixer).

Fallback:
Если typed Task недоступны, используй отдельный Task(generalPurpose) на каждую роль:
- .cursor/agents/<role>.md
- .cursor/skills/<skill>/SKILL.md
- shared contracts

Запрещено:
- single-agent pipeline;
- publish до QA PASS;
- secrets в handoff/log/commit;
- пропуск fixer loop при open incidents.

Финальный ответ:
- run_id;
- artifacts;
- QA verdict;
- publish URL или blocker;
- incident_queue status.
```

---

## 17. GitHub Actions preflight

Опционально добавьте CI:

```yaml
name: Cloud preflight

on:
  pull_request:
  push:
    branches:
      - main

jobs:
  preflight:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: python -m pip install -r requirements.txt
      - run: python -m compileall scripts
      - run: python scripts/doctor.py
```

Не включайте workflow, если у вас нет GitHub token с правом `workflow`.

---

## 18. Acceptance checklist перед первым Cloud run

Repo:

- [ ] GitHub repo создан.
- [ ] Cursor GitHub App подключён к repo.
- [ ] `.cursor/environment.json` есть.
- [ ] `AGENTS.md` есть.
- [ ] `.cursor/agents/` есть.
- [ ] `.cursor/skills/` есть.
- [ ] `scripts/doctor.py` PASS.
- [ ] `.gitignore` закрывает secrets/runtime handoff.

Secrets:

- [ ] Все required env vars добавлены в Cursor Dashboard.
- [ ] `.env` не в Git.
- [ ] MCP tokens не в Git.

Pipeline:

- [ ] Director не выполняет worker-роли сам.
- [ ] У каждой роли есть output contract.
- [ ] Между этапами есть gates.
- [ ] Parallel roles пишут fragments, не один общий файл.
- [ ] Publish/deploy обновляет ledger.
- [ ] Incident/fixer loop включён.

Validation:

- [ ] `git diff --check`
- [ ] Python/Node compile/lint
- [ ] JSON/YAML parse
- [ ] doctor PASS
- [ ] dry-run publish/deploy PASS

---

## 19. Типовые ошибки

### Ошибка: агент сам делает весь pipeline

Fix: вынести роли в subagents, Director только оркестрирует.

### Ошибка: Cloud не видит зависимости

Fix: добавить install в `.cursor/environment.json`, проверить `doctor.py`.

### Ошибка: typed Task недоступен

Fix: fallback `Task(generalPurpose)` per role, передать `.cursor/agents/<role>.md` и `.cursor/skills/<skill>/SKILL.md`.

### Ошибка: secrets попали в commit

Fix:

- заменить на `[REDACTED]`;
- использовать `${ENV_VAR}`;
- усилить `.gitignore`;
- добавить secret scan check.

### Ошибка: publish/deploy работает локально, но не в Cloud

Fix:

- проверить env через safe `--env-check`;
- не использовать локальные абсолютные пути;
- для SFTP/SSH проверить root/cwd;
- не печатать секреты.

### Ошибка: один и тот же workaround повторяется каждый run

Fix:

- записать incident;
- запустить fixer;
- изменить durable contract/script;
- закрыть incident как `fixed`.

---

## 20. Как объяснить ученикам за 10 минут

1. **GitHub repo — это источник правды.**
2. **Cursor Cloud — это одноразовая Ubuntu VM, которая читает repo.**
3. **AGENTS.md объясняет Cloud Agent правила игры.**
4. **.cursor/environment.json готовит окружение.**
5. **Director запускает роли, а не делает всё сам.**
6. **Subagents изолируют контекст.**
7. **Skills хранят подробные инструкции роли.**
8. **Scripts/gates дают PASS/FAIL.**
9. **Secrets живут только в Cursor Dashboard.**
10. **Fixer loop превращает ошибки в улучшения repo.**

Если эти 10 пунктов соблюдены, любой plugin/pipeline можно загрузить в GitHub и запускать в Cursor Cloud воспроизводимо.
