# Excalibur BLOG — quality standard

Стандарт качества **только для статей блога**. Excalibur BLOG автономен — со своими собственными gates.

## Blockers (статья)

- `UTILITY ARTICLE BLOCKER` — `excalibur_blog_utility_gate.py` FAIL (мало шагов, нет workflow/таблицы, вода)
- `RESEARCH NOTES BLOCKER` — `excalibur_blog_research_notes_gate.py` FAIL (research не на текущую дату, мало источников, нет GitHub/docs/community evidence или human brief)
- `HUMAN VOICE BLOCKER` — `excalibur_blog_human_voice_gate.py` FAIL (шаблонная структура, нет живого примера/reader_story, одинаковые H2)
- `PAIN/SOLUTION BLOCKER` — статья не называет боль читателя, не показывает результат или H2 не закрывают конкретные pain points
- Выдуманные цены, даты, проценты без источника в `fact-bank.md` / `research-notes.md`
- AI-slop из blocklist (`skills/excalibur/references/ai-slop-blocklist.md`)
- Объём вне 8 500–9 500 символов текста
- Нет FAQ (5–7 пар)
- GEO QA score < 80 или CORE-EEAT < 16/20
- Link verify fail после 2 циклов
- HTML linter FAIL (запрещённые теги или **оглавление с якорными ссылками** в теле статьи)

## Обязательно PASS

- `research-notes.md` с current-date deep research, таблицей фактов, `accessed_at`, Wordstat, GitHub/docs/community evidence, `reader_pain`, `reader_outcome`, `success_criteria`, `pain_solution_map`, `reader_story`, `voice_angle`, `surprising_fact`
- `research-notes-gate.json` status PASS
- `human-voice-report.json` status PASS
- `article-qa.md` verdict PASS
- `schema.jsonld` BlogPosting + FAQPage
- Cover PNG с alt

## Не применяется к Excalibur BLOG

- AURA visual budget, paint QA, Design Guardian
- Semantic core / Ядрышко pipeline
- Aurora theme build gates
