---
description: Excalibur BLOG — полный прогон статьи через оркестратор и субагентов.
---

# Excalibur BLOG — запуск пайплайна

Откройте workspace с плагином **EXCALIBUR** и выполните команду или напишите:

«Запусти Excalibur BLOG для темы **B01**»

## Параметры

- `topic_id`: B01 | B02 | B03 | all | P0-only (если не указан — Scout подбирает следующую P0)
- `publish`: yes | no (**default: yes** — публикация автоматически после Indexer)

### Правило publish (обязательно для директора)

1. **По умолчанию** после шага ⑤ Indexer директор **обязан** запустить шаг ⑥ `Task(excalibur-blog-publish)`.
2. Пропуск publish **только** при явном `publish: no` / «без публикации» / «draft only».
3. Субагент: `excalibur-blog-publish` + skill `publish-excalibur-blog/SKILL.md`.
4. Если `EXCALIBUR_BLOG_ALLOW_PUBLISH != yes` в Cloud Secrets / env vars или `memory/site.env.local` — publish-агент возвращает `❌ PUBLISH BLOCKER` (шаг выполнен, не silent skip).

Примеры:

```text
/excalibur-blog-run topic_id: B04
/excalibur-blog-run topic_id: B04 publish: yes
/excalibur-blog-run topic_id: B04 publish: no
```

## Пайплайн (7 субагентов + директор)

```text
Scout → Research → Writer → GEO QA → Cover||Schema → Indexer → Publish (auto)
```

## Оркестратор

Директор — **основной агент чата** (не Task). Сценарий: [skills/director-excalibur-blog/SKILL.md](../skills/director-excalibur-blog/SKILL.md).

Handoff runtime: `.cursor/excalibur-blog-handoff.md`  
Локальный шаблон: `shared/excalibur-blog-handoff.template.md`
