# Promotion checklist — B04 geo-optimizaciya-sajta-2026

Дата публикации: 2026-06-11  
Live URL: https://mayai.ru/geo-optimizaciya-sajta-2026/

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
ChatGPT и Алиса отвечают без клика на ваш сайт? GEO — настройка страниц под цитирование в нейроответах за 60–90 минут.

• 32 пункта чек-листа: robots.txt для AI-ботов, answer-first, FAQ, Schema
• Таблица SEO vs GEO vs AEO + шаблон мониторинга Share of Voice
• Аудит 20–30 промптов в ChatGPT, Perplexity и Алисе
• Связка с n8n и MCP Cursor для автоматизации мониторинга

Читать: https://mayai.ru/geo-optimizaciya-sajta-2026/
```

## Перелинковка

- [ ] Добавить ссылку на новый пост с главной blog section (если Aurora не auto)
- [ ] Обновить B02 (n8n) → link to B04 на упоминании GEO/мониторинга (anchor «geo оптимизация»)
- [ ] Обновить B03 (MCP) → link to B04 на упоминании нейропоиска (anchor «geo seo»)
- [ ] Восстановить href B01 → B04 после публикации `/blog/primer-seo-stati/` (inbound уже есть из B01)

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «geo оптимизация» (ручная проверка / Wordstat)

## Notes

Indexer: interlinker --apply — 1 автоматическая вставка (B01 → B04, anchor «geo оптимизация»). B04 уже содержит outbound на B02 и B03. llms.txt и llms-full.txt обновлены: 4 статьи в `memory/blog/llms.txt`. После publish — перезапустить interlinker для inbound из B02/B03 и href B01 в B04.
