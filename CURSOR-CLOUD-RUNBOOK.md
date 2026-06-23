# Cursor Cloud Agent runbook

Краткая выжимка из документации Cursor Cloud Agent, Setup, Capabilities, Automations и GitHub Integration для приватного репозитория Excalibur BLOG.

## Что важно для этого репозитория

- Cloud Agent работает в изолированной Ubuntu VM, клонирует GitHub/GitLab repo, создает ветку и возвращает изменения через PR.
- Cursor выбирает инфраструктуру в таком порядке: `.cursor/environment.json` в repo, затем сохраненная личная инфраструктура, затем командная инфраструктура.
- Секреты не хранятся в Git. Их нужно добавить в Cursor Dashboard -> Cloud Agents -> Secrets.
- Для GitHub нужен установленный Cursor GitHub App с доступом к приватному repo и правами на pull requests/checks.
- Automations запускают Cloud Agents по расписанию, GitHub events, webhooks, Slack и другим триггерам. Для scheduled automation нужно явно выбрать repo и ветку.
- MCP в Cloud лучше подключать через HTTP. Stdio MCP запускается внутри VM и требует, чтобы зависимости были доступны в окружении.

## Repo-level environment

Файл `.cursor/environment.json` выполняется из корня проекта:

```json
{
  "install": "python3 -m pip install --user -r requirements.txt && python3 scripts/excalibur_blog_doctor.py",
  "start": "",
  "terminals": []
}
```

`install` должен быть идемпотентным: его можно запускать много раз, и он не должен писать секреты или runtime-артефакты в Git.

## Cursor Secrets

Минимум для dry-run:

```text
PUBLIC_SITE_URL=https://mayai.ru
EXCALIBUR_BLOG_ALLOW_PUBLISH=no
```

Для боевой публикации:

```text
PUBLIC_SITE_URL=https://mayai.ru
WP_SITE_URL=https://mayai.ru
SSH_HOST=<host>
SSH_USER=<user>
SSH_PASS=<password>
SSH_ROOT=.
SSH_PORT=22
EXCALIBUR_BLOG_ALLOW_PUBLISH=yes
```

Дополнительно:

```text
EXCALIBUR_TOPIC_ID=<optional fixed topic id>
```

Запрещено добавлять в repo реальные `.env`, `memory/site.env.local`, MCP tokens, SSH credentials, Cursor API keys.

## GitHub setup

1. Создать приватный GitHub repo.
2. В Cursor Dashboard -> Integrations подключить GitHub App.
3. Выбрать этот приватный repo в списке доступных репозиториев.
4. В Cursor Cloud Agents открыть repo и убедиться, что infrastructure использует `.cursor/environment.json`.
5. Добавить Secrets.
6. Запустить тестового Cloud Agent с промптом из `CLOUD-AUTOMATION.md`.

## Automation setup

Рекомендуемый первый режим:

- Trigger: manual или schedule 1 раз в день.
- Repository: этот приватный repo.
- Branch: `main`.
- Prompt: шаблон из `CLOUD-AUTOMATION.md`.
- Tools: GitHub PR, MCP tools только те, которые нужны конкретному pipeline.
- Memory: включать осторожно, не хранить секреты и токены.

Для боевого автопубликационного режима включать `EXCALIBUR_BLOG_ALLOW_PUBLISH=yes` только после успешного dry-run.

## Acceptance check

Перед включением расписания Cloud Agent должен пройти:

```bash
python3 scripts/excalibur_blog_doctor.py
python3 scripts/excalibur_blog_today.py
python3 scripts/excalibur_blog_research_start.py --topic-id B01
```

Для publish-preflight:

```bash
python3 scripts/excalibur_blog_doctor.py --publish
python3 scripts/excalibur_blog_wp_publish.py --env-check
```

Если `--publish` падает из-за секретов, это нормально для dry-run окружения и блокер для боевой публикации.
Если SSH upload пишет warning про fallback на `.`, обновите Cursor Secret `SSH_ROOT` на `.` или уберите несуществующий panel/root path. Секретные значения не записывать в repo.

## Optional GitHub Actions preflight

Пример workflow лежит в `shared/cloud-preflight-workflow.yml.example`. Он не включен активным `.github/workflows/*`, потому что GitHub требует у token scope `workflow` для пуша workflow-файлов.

Чтобы включить CI:

```bash
gh auth refresh -s workflow
mkdir -p .github/workflows
cp shared/cloud-preflight-workflow.yml.example .github/workflows/cloud-preflight.yml
git add .github/workflows/cloud-preflight.yml
git commit -m "Add cloud preflight workflow"
git push
```
