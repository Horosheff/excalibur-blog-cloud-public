# Promotion checklist — B02 avtomatizaciya-n8n-ai-agents

Дата публикации: YYYY-MM-DD  
Live URL: https://mayai.ru/blog/avtomatizaciya-n8n-ai-agents/ (заполнить после publish)

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
ИИ-агент в n8n — это узел-дирижёр: Chat Trigger → AI Agent → модель + tools + память. Соберите MVP за вечер без DevOps.

• 7 шагов: от Cloud trial до теста в Chat UI
• RAG и Simple Memory без кода
• Таблица n8n vs Make.com — когда что выбрать
• Чеклист из 12 пунктов перед продакшеном

Читать: https://mayai.ru/blog/avtomatizaciya-n8n-ai-agents/
```

## Перелинковка

- [ ] Добавить ссылку на новый пост с главной blog section (если Aurora не auto)
- [ ] Обновить 1–2 старых поста → link to new (если есть)

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «автоматизация n8n» (ручная проверка / Wordstat)

## Notes

Indexer: 0 interlink changes (B01 — SEO/GEO, B02 — n8n/AI; пересечения anchor_variants в текстах нет). После публикации B01 на mayai.ru — перезапустить `excalibur_blog_interlinker.py --apply --site-base https://mayai.ru`. llms.txt обновлён: 2 статьи в `memory/blog/llms.txt`.
