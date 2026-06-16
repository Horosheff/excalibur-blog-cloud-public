# Excalibur BLOG — Cursor-плагин + Cloud

SEO/GEO статьи: **оркестратор + субагенты**, параллель **cover || schema**.

## Cloud (как kovcheg-office-cloud)

| Файл | Назначение |
|------|------------|
| [AGENTS.md](AGENTS.md) | Инструкции Cloud Agent |
| [CLOUD-AUTOMATION.md](CLOUD-AUTOMATION.md) | Worker, secrets, automation prompt |
| [.cursor/agents/](.cursor/agents/) | Task types для Cloud |
| [.cursor/excalibur-blog-handoff.md](.cursor/excalibur-blog-handoff.md) | Runtime handoff (gitignore) |
| [.cursor/excalibur-blog-fragments/](.cursor/excalibur-blog-fragments/) | cover + schema parallel |

После правок `agents/` / `skills/`:

```powershell
.\scripts\sync_cursor_cloud.ps1
```

## Локальный запуск

Команда `/excalibur-blog-run` — Директор в чате → [director-excalibur-blog/SKILL.md](skills/director-excalibur-blog/SKILL.md)

## Пайплайн

```text
today + research_start
  → research → writer → geo-qa
  → cover || schema
  → indexer → publish (auto; skip только publish:no)
```

Субагенты: [agents/FOR-AGENTS.md](agents/FOR-AGENTS.md)
