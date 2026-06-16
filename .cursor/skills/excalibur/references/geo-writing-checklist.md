# Excalibur — GEO writing checklist

Адаптация практик из [aaron-he-zhu/seo-geo-claude-skills](https://github.com/aaron-he-zhu/seo-geo-claude-skills) (`geo-content-optimizer`, `seo-content-writer`) под Excalibur BLOG HTML.

## Answer-first (первые 60–100 слов)

- Первый `<p>` 350–500 символов: боль → прямой ответ → обещание пользы
- Primary query естественно в первых 100 словах (не stuffing)
- Можно вырезать первый абзац как самостоятельный ответ для AI Overview / Нейро

## Chunkable blocks (на цитирование)

- Минимум **3** блока по **40–60 слов** (определение, «коротко», итог секции)
- Один тезис на абзац; абзацы 3–6 предложений
- H2/H3 читаются как outline без body
- Списки `<ul>/<ol>` для шагов и сравнений

## Quotable statements

- 2–4 предложения с конкретикой (цифра+источник, named entity, дата)
- Формулировки standalone — без «как сказано выше»
- Источники в `research-notes.md`, в тексте — осторожные маркеры («по данным …», «на момент публикации»)

## FAQ (GEO + schema)

- 5–7 пар `<h3>` + `<p>`; вопрос = формулировка из queries/PAA
- Ответ: прямое первое предложение, затем нюанс
- FAQ дублирует видимый контент (для FAQPage JSON-LD)

## Snippet patterns


| Тип          | Паттерн                                                                            |
| ------------ | ---------------------------------------------------------------------------------- |
| Definition   | «[Термин] — это … Важно, потому что …» (40–60 слов)                                |
| How-to       | H2 + текстовая схема-цепочка (`<blockquote>` + `→`) + нумерованный `<ol>` с шагами |
| Comparison   | H2 + сравнительная таблица `<table>` + вердикт эксперта `<blockquote>`             |
| Listicle     | H2 + `<ul>` с parallel phrasing                                                    |
| Visual Media | Внедрено 1–3 `<img>` с подробным `alt` и курсивной подписью `<i>` снизу            |


## Яндекс / Google AI

- Title 50–65 символов, Description 120–160 (в `article.meta.json`)
- Internal links 2–3 из карточки темы
- Нет hidden schema-only FAQ — всё видно в HTML
- Свежесть: дата в meta + актуальные версии/цены только из research

## E-E-A-T & Author Attribution (Авторитетность и Авторы)

- Автор статьи выбран из единого реестра `shared/authors-registry.json` (например, `alexander-smirnov` или `elena-kovaleva`)
- Имя автора и его ссылки `sameAs` в `schema.jsonld` соответствуют реестру
- В статью встроен блок «Мнение эксперта» (`<blockquote>` или отдельный блок) с цитатой выбранного автора

## Anchor Text Diversification (Анкоры перелинковки)

- В `article.meta.json` заполнен блок `"anchor_variants"` (3-5 естественных фраз для ссылок на эту статью из других текстов)
- Использованы разнообразные анкоры (прямые, разбавленные, брендовые) вместо одного и того же коммерческого ключа
- Запущен `excalibur_blog_interlinker.py --apply` для автоматического связывания по диверсифицированным анкорам

## Anti patterns

- Нет «в этой статье вы узнаете»
- Нет стены текста без H2 > 400 слов
- Нет generic AI conclusion («подводя итог», «в заключение»)