---
name: excalibur-research
description: Excalibur BLOG Research — topic research перед статьёй (SERP, факты, угол). Gate до article.html.
---

# Excalibur BLOG — Research

## Когда

**Шаг 0 (скрипт, обязательно):** перед любым research — зафиксировать дату и собрать свежий SERP.

```bash
python scripts/excalibur_blog_research_start.py --topic-id B01
```

Создаёт в папке статьи:

- `research-context.json` — сегодняшняя дата, год, окно свежести, тема, список поисковых запросов
- `research-serp.json` — результаты web-поиска по запросам с `{year}` и текущим месяцем

`--dry-run` — только дата и запросы без HTTP.

Перед **каждой** статьей затем пиши `research-notes.md`. Без него нельзя утверждать цены, даты, версии, статистику.

## Вход

- Карточка из `memory/topics/blog-topics.md`
- `memory/brief/site-brief.md`, `fact-bank.md`
- `shared/quality-blog.md`
- MCP сервер `user-mcp-kv` со всеми инструментами `wordstat_*`

## Выход

`memory/blog/articles/<topic_id>-<slug>/research-context.json`  
`memory/blog/articles/<topic_id>-<slug>/research-serp.json`  
`memory/blog/articles/<topic_id>-<slug>/research-notes.md` (с разделом по Вордстату!)

## Обязательное использование Yandex Wordstat MCP, WebSearch Курсора и GitHub evidence

1. **Анализ спроса через Wordstat API:**
   Каждый прогон исследования **обязан** задействовать инструмент `wordstat_get_top_requests` сервера `user-mcp-kv` для анализа спроса:
   - Вызови `wordstat_get_top_requests` для `primary_query` и ключевых `secondary_queries`.
   - Если вызов вернул `401 Unauthorized` (токен устарел):
     * Запиши в `research-notes.md` предупреждение: `⚠️ WORDSTAT AUTH WARNING: Токен Wordstat устарел. Обновите токен через: https://oauth.yandex.ru/authorize?response_type=token&client_id=c654b948515a4a07a4c89648a0831d40`
     * Сделай экспертную оценку семантики, но явно укажи, что точные объемы спроса не получены из-за авторизации.
   - Если вызов успешен:
     * Сформируй в `research-notes.md` таблицу спроса: Фраза | Показы в месяц.
     * Выдели сопутствующие LSI-запросы из топа выдачи Вордстата для использования копирайтером.

2. **Deep research вместо простого SERP-обзора:**
   - Сначала разложи тему на **5–8 research_questions**: спрос, свежие изменения, инструменты, риски, ошибки внедрения, что спорят конкуренты, что реально может сделать новичок без технического бэкграунда.
   - По каждой группе вопросов собери источники через `WebSearch`/`WebFetch`, а не только из `research-serp.json`.
   - Для технических тем обязательно ищи GitHub: repos, issues, discussions, README, changelog. Минимум 3 GitHub URL в `github_evidence`.
   - Всегда ищи официальные docs/changelog/developer pages и community experience (форумы, Reddit, Habr/VC/Dev.to, если релевантно).

3. **Замена уличных поисковиков (DuckDuckGo) на WebSearch Курсора:**
   Мы **отказываемся** от ненадежных сторонних утилит и парсеров DuckDuckGo («уток»).
   - Агент имеет полноценный доступ в интернет через нативный инструмент **`WebSearch`** (или `WebFetch` для чтения конкретных страниц).
   - Для анализа конкурентов в SERP **всегда используй инструмент `WebSearch`**. Ищи статьи, руководства, гайды по `primary_query` и ключевым словам в Яндексе и Google.
   - Игнорируй сырой `research-serp.json` из шага 0, если он пуст, неполный или нерелевантный. Твой собственный поиск через `WebSearch` — приоритетный источник свежих данных 2026 года.

## Обязательный structured brief в research-notes.md

`research-notes.md` должен быть машинно проверяемым. Используй эти поля буквально:

```text
research_date: YYYY-MM-DD
accessed_at: YYYY-MM-DD
utility_verdict: PASS
reader_outcome: одно предложение — какой первый понятный результат новичок сможет сделать после статьи
reader_pain: конкретная боль, риск, страх или затык новичка
success_criteria: как новичок поймёт, что проблема решена
voice_angle: человеческий угол, сцена или напряжение темы
reader_story: мини-сценарий/ошибка читателя, которую Writer обязан вплести
surprising_fact: неожиданный факт, конфликт мнений или свежая деталь

## research_questions
1. ...

## source_table
| source | url | accessed_at | why_it_matters |

## wordstat
| phrase | impressions |

## github_evidence
| repo/issue/doc | url | signal |

## pain_solution_map
| pain | solution | proof/source | reader_result |

## competitor_gaps
| competitor | what_they_miss | how_we_write_better |

## action_outline
1. ...
```

После записи обязательно:

```bash
python scripts/excalibur_blog_research_notes_gate.py \
  --article-dir memory/blog/articles/<topic_id>-<slug> \
  -o research-notes-gate.json
```

Если gate вернул BLOCK — исправь `research-notes.md`; Writer не стартует.

## Правила

0. **Сначала** `excalibur_blog_research_start.py` (шаг 0) — для валидации даты/года и utility-gate темы.
1. Web research 15–25 мин: используй инструмент **`WebSearch`** Курсора для глубинного анализа ТОП-5 конкурентов, официальных docs, GitHub evidence и community pain points в реальном времени. GitHub/docs нужны для фактов, но итоговый угол обязан быть beginner-first: что новичку нажать, подключить, проверить и как не сломать процесс. Приоритетный источник фактов — `fact-bank.md`.
2. Микро-исследование Wordstat через `user-mcp-kv` -> `wordstat_get_top_requests` (см. выше).
3. Извлеки минимум 10–15 проверенных фактов (цифр/утверждений) с точными URL источников из твоего интернет-поиска.
4. Каждая цифра → таблица фактов в `research-notes.md` или не использовать.
5. Не копировать структуру конкурента 1:1.
6. Каждая статья должна решать боль новичка: без `reader_pain`, `pain_solution_map`, `success_criteria` и beginner-friendly `reader_outcome` research не готов.
7. Не писать “экспертную оценку” вместо источников, кроме явного `⚠️ WORDSTAT AUTH WARNING`. Без источников для ключевых утверждений — blocker.

## Blockers

- `❌ RESEARCH BLOCKER` — тема не найдена и не создана из запроса пользователя
- `❌ RESEARCH BLOCKER` — нет источников для ключевых утверждений
- `❌ RESEARCH BLOCKER` — нет явной боли читателя, карты решения и критерия результата
- `❌ RESEARCH BLOCKER` — research angle ушёл в материал для профи/архитекторов и не даёт новичку первого понятного результата
- `❌ RESEARCH BLOCKER` — `research-notes-gate.json` status BLOCK
