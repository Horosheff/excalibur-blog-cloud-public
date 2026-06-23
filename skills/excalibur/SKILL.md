---
name: excalibur
description: |
  Excalibur BLOG — справочник контрактов и артефактов. Оркестрация: director-excalibur-blog + Task(subagents).
---

# Excalibur BLOG — справочник

> **Директор:** [director-excalibur-blog/SKILL.md](../director-excalibur-blog/SKILL.md)  
> **Субагенты:** [FOR-AGENTS.md](../../agents/FOR-AGENTS.md)

## Артефакты на тему

```text
memory/blog/articles/<topic_id>-<slug>/
  research-context.json
  research-serp.json
  research-notes.md
  article.html
  article.meta.json
  article-qa.md
  schema.jsonld
  cover/cover.png
  … QA reports …
```

## Контракты

- `shared/excalibur-article-writing-contract.md`
- `shared/editorial-utility-only.md`
- `shared/blog-cover-mcp-contract.md`
- `shared/excalibur-wp-publish-contract.md`
- `shared/pipeline-incident-fix-contract.md`
- `shared/quality-blog.md`

## Incident memory

- Durable queue: `memory/pipeline-fix-queue.md`
- Post-run fixer: `agents/excalibur-blog-fixer.md` + `skills/fixer-excalibur-blog/SKILL.md`

## References

`skills/excalibur/references/*`

Fragment: `=== EXCALIBUR BLOG (SEO/GEO СТАТЬИ) ===`
