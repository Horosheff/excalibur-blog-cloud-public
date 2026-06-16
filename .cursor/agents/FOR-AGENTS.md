# Excalibur BLOG — субагенты и распределение задач

Полная карта: [shared/pipeline-task-map.md](../shared/pipeline-task-map.md)

## Директор (не Task)

| | |
|-|-|
| **Файл** | [excalibur-blog-director.md](excalibur-blog-director.md) |
| **Skill** | [director-excalibur-blog](../skills/director-excalibur-blog/SKILL.md) |
| **Задача** | shell preflight, запуск Task, перенос fragments, финальный статус |

## 8 субагентов (Task)

|| # | `Task(name)` | Роль | agent | skill |
|---|---|--------------|------|-------|-------|
|| 🔍 | `excalibur-blog-scout` | Разведка трендов и подбор тем | [scout](excalibur-blog-scout.md) | [scout-excalibur-blog](../skills/scout-excalibur-blog/SKILL.md) |
|| ① | `excalibur-blog-research` | Research, SERP, факты | [research](excalibur-blog-research.md) | [excalibur-research](../skills/excalibur-research/SKILL.md) |
| ② | `excalibur-blog-writer` | Longread HTML + meta | [writer](excalibur-blog-writer.md) | [writer-excalibur-blog](../skills/writer-excalibur-blog/SKILL.md) |
| ③ | `excalibur-blog-geo-qa` | QA-скрипты, PASS | [geo-qa](excalibur-blog-geo-qa.md) | [excalibur-geo-qa](../skills/excalibur-geo-qa/SKILL.md) |
| ④a | `excalibur-blog-cover` | ONE MCP quad i2i + inline | [cover](excalibur-blog-cover.md) | [cover-excalibur-blog](../skills/cover-excalibur-blog/SKILL.md) |
| ④b | `excalibur-blog-schema` | JSON-LD schema | [schema](excalibur-blog-schema.md) | [schema-excalibur-blog](../skills/schema-excalibur-blog/SKILL.md) |
| ⑤ | `excalibur-blog-indexer` | Interlink + llms | [indexer](excalibur-blog-indexer.md) | [indexer-excalibur-blog](../skills/indexer-excalibur-blog/SKILL.md) |
| ⑥ | `excalibur-blog-publish` | WP publish (post, featured, inline, schema) | [publish](excalibur-blog-publish.md) | [publish-excalibur-blog](../skills/publish-excalibur-blog/SKILL.md) |

**④a + ④b** — параллельно, одним сообщением Директора (после ③ PASS).

## Где лежат файлы

```text
agents/                    ← исходники (локальная разработка)
.cursor/agents/            ← Cloud Task types (sync: scripts/sync_cursor_cloud.ps1)
skills/<role>/SKILL.md     ← детальные инструкции роли
```

## Handoff

- Cloud: `.cursor/excalibur-blog-handoff.md`
- Fragments (cover+schema): `.cursor/excalibur-blog-fragments/`
