# Promotion checklist — B03 podklyuchenie-mcp-cursor

Дата публикации: YYYY-MM-DD  
Live URL: https://mayai.ru/podklyuchenie-mcp-cursor/

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
Cursor без MCP не видит ваши сервисы — подключите первый сервер за 15–30 минут через Tools & MCP или mcp.json.

• 10 шагов: global vs project конфиг, stdio и url, зелёный статус
• Таблица серверов под автоматизацию (Browser, Context7, GitHub)
• Чеклист из 11 пунктов + troubleshooting через MCP Logs
• Связка с n8n/Make: IDE готовит, сценарии публикуют 24/7

Читать: https://mayai.ru/blog/podklyuchenie-mcp-cursor/
```

## Перелинковка

- [ ] Добавить ссылку на новый пост с главной blog section (если Aurora не auto)
- [ ] Обновить B02 (n8n-агенты) → link to B03 на упоминании MCP (anchor «cursor mcp» / «подключить MCP»)

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «cursor mcp» (ручная проверка / Wordstat)

## Notes

Indexer: interlinker --apply — 0 автоматических вставок (anchor_variants B03 не встречаются в B01/B02; B03 уже содержит 3× ссылку на B02). llms.txt обновлён: 3 статьи в `memory/blog/llms.txt`. После publish — перезапустить interlinker с `--site-base https://mayai.ru` для inbound-ссылок из B02.
