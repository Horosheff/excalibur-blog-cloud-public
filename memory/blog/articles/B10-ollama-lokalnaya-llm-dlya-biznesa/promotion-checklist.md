# Promotion checklist — B10 ollama-lokalnaya-llm-dlya-biznesa

Дата публикации: 2026-06-17
Live URL: [REDACTED]/ollama-lokalnaya-llm-dlya-biznesa/

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
Локальная нейросеть через Ollama — не «бесплатно и безопасно», если GPU молчит, а порт 11434 открыт в LAN.

Что сделать до первого API-запроса:
• Выбрать модель под VRAM (qwen3:8b, не 32B на 8 ГБ).
• Сверить ollama ps с nvidia-smi — 100% GPU в UI ≠ реальная загрузка.
• Закрыть контур: localhost или прокси, не OLLAMA_HOST=0.0.0.0 без auth.

Пошаговый workflow: pull → API → n8n + чек-лист из 20 тест-кейсов:
Читать: [REDACTED]/ollama-lokalnaya-llm-dlya-biznesa/
```

## Перелинковка

- [ ] Добавить ссылку на новый пост с главной blog section (если Aurora не auto)
- [ ] Обновить 1–2 старых поста → link to new (если есть)

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query (ручная проверка / Wordstat)

## Notes

Interlinker (2026-06-17): 0 новых контекстных ссылок — не найдено безопасных внутренних linking opportunities. llms.txt обновлён (10 статей). Существующие internal links в article.html: n8n AI agents, MCP Cursor, RAG векторная база.
