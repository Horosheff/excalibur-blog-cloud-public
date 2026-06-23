# Excalibur BLOG — handoff template

Runtime handoff for a real run lives in:

```text
.cursor/excalibur-blog-handoff.md
```

Do not commit runtime handoff files. At the start of a run, the Director creates a fresh file from this shape:

```text
# Excalibur BLOG — новая сессия

`pipeline_started_at`:
`topic_id`:
`article_dir`:
`publish`: yes

## Статус пайплайна

| Шаг | Агент | Статус | Время |
| --- | --- | --- | --- |
| 0 | shell research_start + utility gate | pending | |
| 1 | excalibur-blog-research | pending | |
| 2 | excalibur-blog-writer | pending | |
| 3 | excalibur-blog-geo-qa | pending | |
| 4 | excalibur-blog-cover || excalibur-blog-schema | pending | |
| 5 | excalibur-blog-indexer | pending | |
| 6 | excalibur-blog-publish | pending | |
| 7 | excalibur-blog-fixer (if incidents open) | pending | |

## Incident memory

`incident_queue`: memory/pipeline-fix-queue.md
`incident_contract`: shared/pipeline-incident-fix-contract.md

Each agent block must include:

```text
incident_report: none | memory/pipeline-fix-queue.md#INC-...
```

=== EXCALIBUR BLOG (PIPELINE DONE) ===
topic_id:
article_dir:
qa:
publish:
permalink:
incident_queue:
```
