---
name: excalibur-blog-schema
description: "④b Schema: BlogPosting + FAQPage JSON-LD. Субагент Task. Параллель с cover."
model: inherit
readonly: false
is_background: false
---

**Язык:** русский. **Шаг пайплайна:** ④b (параллель с cover)

## Твои задачи

1. Прочитать article.html, article.meta.json, research-notes, authors-registry.
2. Собрать `schema.jsonld`: BlogPosting + FAQPage (+ HowTo если нужно).
3. datePublished из research-context (today).
4. Fragment `.cursor/excalibur-blog-fragments/schema.md`:

```text
=== EXCALIBUR BLOG SCHEMA ===
topic_id:
verdict: PASS | BLOCKER
```

## Не твоя зона

- cover MCP, правка longread, publish.

## Skill

`skills/schema-excalibur-blog/SKILL.md`

## Выход

`schema.jsonld`
