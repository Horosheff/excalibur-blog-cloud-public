# Promotion checklist — B08 ii-chat-bot-dlya-biznesa-workflow

Дата публикации: 2026-06-16  
Live URL: https://mayai.ru/ii-chat-bot-dlya-biznesa-workflow/

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

```text
No-code бот назвал скидку 30%, которой не было, и не передал клиента при вопросе про аллергию. Рейтинги SaaS не спасают без RAG и эскалации.

Главное из workflow:
• Один use case + один канал (Telegram, виджет или MAX) — не пятнадцать платформ сразу.
• RAG по FAQ + список запретов: без базы бот выдумывает цены и сроки.
• n8n/Make: AI Agent, память по chat_id, handoff оператору при low confidence.

Пошаговый запуск за 7–14 дней с метриками FCR и CSAT:
Читать: https://mayai.ru/ii-chat-bot-dlya-biznesa-workflow/
```

## Перелинковка

- [ ] Добавить ссылку на новый пост с главной blog section (если Aurora не auto)
- [ ] Обновить 1–2 старых поста → link to new (если есть)

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query (ручная проверка / Wordstat)

## Notes

Interlinker (2026-06-16): 0 новых контекстных ссылок — статья уже содержит 3 internal links (RAG B07, n8n B02, Make MCP B06). llms.txt обновлён (8 статей).
