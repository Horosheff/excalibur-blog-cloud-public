# Promotion checklist — B07 postroenie-rag-sistemy-vektornaya-baza

Дата публикации: 2026-06-16  
Live URL: [REDACTED]/postroenie-rag-sistemy-vektornaya-baza/

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
RAG уверенно врёт — или вы плохо порезали PDF? Chroma вернула «возвраты разрешены», а «кроме акционных билетов» осталось в соседнем чанке.

Главное из разбора:
• RAG — не магия: PDF → чанки 300–512 токенов, overlap 10–20% → pgvector или Qdrant → ответ с цитатой.
• Long context годится для пилота; в проде нужны свежесть, ACL и eval на golden set 10–15 вопросов.
• Hybrid + rerank: после overlap 15% точность выросла с 4/10 до 9/10 на том же наборе.

Пошаговый workflow от документов до проверяемого бота (LangChain и n8n):
Читать: [REDACTED]/postroenie-rag-sistemy-vektornaya-baza/
```

## Перелинковка

- [ ] Добавить ссылку на новый пост с главной blog section (если Aurora не auto)
- [ ] Обновить 1–2 старых поста → link to new (если есть)

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query (ручная проверка / Wordstat)

## Notes

Interlinker (2026-06-16): 0 новых контекстных ссылок — статья уже содержит 2 internal links (n8n, MCP Cursor). llms.txt обновлён (7 статей).
