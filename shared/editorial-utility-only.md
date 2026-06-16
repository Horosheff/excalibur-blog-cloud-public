# Excalibur BLOG — только полезные статьи (utility-only)

Канон: `memory/brief/editorial-policy.json`

## Принцип

**Публикуем только то, что даёт действие.** После прочтения читатель знает *что сделать* — не «вообще про тему».

| ✅ Берём | ❌ Не берём |
|---------|------------|
| How-to, пошаговый гайд | Новости, «вышло обновление» |
| Чеклист перед действием | Мнение без инструкции |
| Comparison с таблицей и выбором | «Что такое X» на 9k без шагов |
| Troubleshooting / fix | Trend-посты, размышления |
| Workflow (A→B→C) | Корпоративная вода, мотивация |

## Gate 1 — тема (`blog-topics.md`)

Перед research:

```bash
python scripts/excalibur_blog_utility_gate.py --topic-id B01
```

**Blocker `UTILITY TOPIC BLOCKER`** — тему не пускаем в пайплайн.

Обязательные поля карточки:

- `search_intent`: `how_to` | `checklist` | `comparison` | `troubleshooting` | `workflow` | `parent_guide`
- `article_mode`: **B** (инструкция/гайд)
- `h1` / `primary_query`: глагол действия («как…», «чек-лист…», «сравнение…»)

## Gate 2 — research

Research-агент **отклоняет** угол без практики. В `research-notes.md`:

- `utility_verdict: PASS`
- `research_date` совпадает с `research-context.json` → `today_iso`
- `source_table` с URL и `accessed_at`
- `github_evidence` для технических тем
- `reader_pain`: конкретная боль/риск/затык читателя
- `reader_outcome`: одно предложение — что сможет сделать читатель
- `success_criteria`: как читатель поймёт, что проблема решена
- `voice_angle`, `reader_story`, `surprising_fact`: материал для человеческого lead/H2
- `pain_solution_map`: таблица pain → solution → proof/source → reader_result
- `action_outline`: 5–9 шагов или чеклист-пунктов

Машинный gate:

```bash
python scripts/excalibur_blog_research_notes_gate.py \
  --article-dir memory/blog/articles/<topic_id>-<slug> \
  -o research-notes-gate.json
```

## Gate 3 — writer

Контракт: `shared/excalibur-article-writing-contract.md`

- Каждый H2 = подзадача + **рекомендация** (делать / не делать)
- Минимум **5** нумерованных шагов ИЛИ чеклист 10+ пунктов
- Workflow-схема (`→`) или таблица (comparison)
- FAQ — короткие **ответы-действия**, не пересказ
- Lead/H2 используют `reader_story`, `voice_angle`, `surprising_fact`
- Lead называет боль, H2 закрывают боли из `pain_solution_map`, до FAQ есть понятный критерий результата.
- Human voice gate PASS: нет шаблонных H2, есть живые примеры, разный ритм абзацев

## Gate 4 — GEO QA

```bash
python scripts/excalibur_blog_utility_gate.py \
  --article-dir memory/blog/articles/<topic_id>-<slug>
```

**Blocker `UTILITY ARTICLE BLOCKER`** — writer правит (FIX), QA не PASS.

Плюс slop-detector (вода/штампы).

## Как провернуть без воды (чеклист редактора)

1. **Island test:** вырежь H2 — остаётся ли actionable кусок?
2. **So what test:** каждый абзац — «и что мне с этим делать?»
3. **Lead:** боль + ответ + результат (не «в этой статье»)
4. **Нет режима A** в utility-only блоге
5. **Цифры** только из research / fact-bank
6. **CTA ≤ 3**, не подменяет пользу

## Связанные файлы

- `memory/brief/site-brief.md` — niche + editorial
- `skills/excalibur/references/article-archetypes.md` — скелет B
- `skills/excalibur/references/ai-slop-blocklist.md` — вода/штампы
- `shared/quality-blog.md` — blockers
