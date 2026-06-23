# Promotion checklist — B01 primer-seo-stati

Дата публикации: 2026-06-10  
Live URL: https://... (заполнить после publish)

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после WP publish).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (theme или plugin)
- [ ] Проверить internal links из статьи (200)
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
SEO-статья в 2026 — это не набор ключей, а единый workflow SEO + GEO: от семантики до FAQ и schema.

• Один longread вместо двух проектов: интент, H2-чанки, BlogPosting + FAQPage
• Lead 350–500 знаков, атомарные блоки для нейропоиска
• Чеклист из 15 пунктов перед публикацией

Читать: [URL]
```

## Перелинковка

- [ ] Добавить ссылку на новый пост с главной blog section (если Aurora не auto)
- [ ] Обновить 1–2 старых поста → link to new (если есть)

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query (ручная проверка / Wordstat)

## Notes

Indexer: 0 interlink opportunities (единственная статья в `memory/blog/articles`). После публикации второй статьи — перезапустить `excalibur_blog_interlinker.py --apply`.
