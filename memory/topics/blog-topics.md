# Blog topics — Excalibur BLOG

Формат карточек. **Utility-only:** см. `shared/editorial-utility-only.md`.

**Разрешённые `search_intent`:** `how_to`, `checklist`, `comparison`, `troubleshooting`, `workflow`, `parent_guide`  
`**article_mode`:** только **B** (гайд/инструкция). Режим A (новости) — не публикуем.

## Редакционные приоритеты следующих тем

Главная аудитория — новички и обычные люди без технического бэкграунда, которые хотят практическую автоматизацию, трафик, лиды, контент и сайты без команды разработчиков.

**P0-направления сейчас:**

1. **Cursor AI для новичков** — как сделать сайт, лендинг, правки дизайна, компонент, форму, SEO-страницу, GitHub/Cloud workflow без сложного кода.
2. **Маркетинг и дизайн сайтов через Cursor AI** — лендинги, квизы, формы заявок, страницы услуг, UI-блоки, A/B тексты, быстрый редизайн.
3. **Автопостинг и соцсети** — Telegram, VK, Дзен, Pinterest, Reels/Shorts, расписание, UTM, обложки, повторное использование контента.
4. **Авто-блог и контент-завод для новичка** — от идеи до черновика, проверки, публикации, перелинковки и обновления статьи.
5. **Трафик и лиды** — лид-магниты, автоворонки, CRM, формы, боты, аналитика, обработка заявок через Make.com/Cursor AI.
6. **Рабочие задачи через Make.com + Cursor AI** — таблицы, документы, заявки, отчёты, письма, поддержка, простые AI-агенты в реальном процессе.

Scout должен предпочитать темы с формулировками: "как начать", "первый сценарий", "без кода", "для новичка", "чек-лист запуска", "как получить заявки/трафик/публикации".

Перед research:

```bash
python scripts/excalibur_blog_utility_gate.py --topic-id <ID>
```

---

## B01 — Пример темы

- **priority:** P0
- **slug:** primer-seo-stati
- **h1:** Как писать SEO-статьи, которые читают люди
- **primary_query:** как писать seo статьи
- **secondary_queries:** seo текст для блога, geo оптимизация статьи
- **search_intent:** how_to
- **article_mode:** B
- **h2_outline:**
  1. Зачем SEO и GEO в одной статье
  2. Структура longread
  3. FAQ и schema
  4. Чеклист перед публикацией
- **faq_hints:** сколько символов в seo статье; что такое geo в seo
- **internal_links:** /
- **cover_scene_hint:** редактор за ноутбуком, блокнот, тёплый свет

---

## B02 — Автоматизация процессов на n8n

- **priority:** P0
- **slug:** avtomatizaciya-n8n-ai-agents
- **h1:** Как настроить ИИ-агентов в n8n: пошаговое руководство по автоматизации бизнеса
- **primary_query:** автоматизация n8n
- **secondary_queries:** автоматизация ии n8n, примеры автоматизации n8n, ии агенты и автоматизация с n8n, автоматизация бизнеса n8n
- **search_intent:** how_to
- **article_mode:** B
- **h2_outline:**
  1. Почему n8n стал лидером автоматизации с ИИ в 2026 году
  2. Пошаговая настройка первого ИИ-агента в ноде AI Agent
  3. Подключение памяти и векторных баз данных (RAG) без кода
  4. Реальные примеры автоматизации n8n для бизнеса
  5. Сравнение n8n self-hosted и Make: что выбрать в 2026 году
- **faq_hints:** как устроен ai agent node в n8n; чем отличается n8n от make в 2026; как подключить базу знаний к ии в n8n
- **internal_links:** /services/
- **cover_scene_hint:** робот собирает конструктор из кубиков-интеграций (нод), яркие розовые стикеры с надписями "LangChain" и "AI Agent", неоновый свет, diy коллаж

---

## B03 — Подключение MCP в Cursor

- **priority:** P0
- **slug:** podklyuchenie-mcp-cursor
- **h1:** Как подключить MCP-серверы в Cursor: пошаговая инструкция для автоматизации
- **primary_query:** cursor mcp
- **secondary_queries:** mcp сервер для cursor, как подключить mcp к cursor, cursor ai mcp, настройка mcp сервера
- **search_intent:** how_to
- **article_mode:** B
- **h2_outline:**
  1. Что такое MCP и зачем подключать серверы в Cursor в 2026 году
  2. Где лежит конфиг: ~/.cursor/mcp.json и .cursor/mcp.json в проекте
  3. Пошаговое подключение stdio-сервера через npx (пример mcp.json)
  4. Проверка в Settings → Tools & MCP и настройка безопасности (auto-run, allowlist)
  5. Топ MCP-серверов для автоматизации: браузер, Wordstat, WordPress, Figma
  6. Troubleshooting: красный статус, spawn ENOENT, ошибки JSON и логи Output
- **faq_hints:** как подключить mcp к cursor; какие mcp серверы лучше для cursor; почему mcp сервер не подключается в cursor
- **internal_links:** /avtomatizaciya-n8n-ai-agents/
- **cover_scene_hint:** ноутбук с IDE Cursor, вокруг экрана «кубики-плагины» MCP-серверов, стикеры Browser/WordPress/Wordstat, неоновый diy-коллаж

---

## B04 — GEO-оптимизация сайта под нейросети

- **priority:** P0
- **slug:** geo-optimizaciya-sajta-2026
- **h1:** Как настроить GEO-оптимизацию сайта: чек-лист для попадания в ответы нейросетей
- **primary_query:** geo оптимизация
- **secondary_queries:** geo оптимизация сайта, geo seo оптимизация, с чего начать geo оптимизацию, geo оптимизация контента
- **search_intent:** checklist
- **article_mode:** B
- **h2_outline:**
  1. GEO vs SEO: что меняется в 2026 и зачем оптимизировать под ChatGPT, Алису и Perplexity
  2. Аудит текущего присутствия: как проверить, цитирует ли вас нейровыдача
  3. Структура контента под извлечение ИИ: блоки 40–80 слов, FAQ, таблицы и заголовки
  4. Schema.org и технический доступ: FAQPage, Article, robots.txt для GPTBot и PerplexityBot
  5. Чек-лист GEO-оптимизации: 30+ пунктов с приоритетами (критично / важно / бонус)
  6. Мониторинг AI Share of Voice: как отслеживать цитирование и обновлять контент
- **faq_hints:** с чего начать geo оптимизацию; чем geo отличается от seo; как попасть в ответы яндекс нейро; нужна ли schema для geo
- **internal_links:** /primer-seo-stati/
- **cover_scene_hint:** экран сайта в центре, вокруг «пузыри-ответы» ChatGPT/Алиса/Perplexity со стрелками-цитатами, чек-лист на стикерах, блоки FAQ и schema, тёплый неоновый diy-коллаж

---

## B05 — Контент-завод на нейросетях

- **priority:** P0
- **slug:** avtonomnyj-kontent-zavod-nejroseti
- **h1:** Как создать автономный контент-завод на нейросетях: пошаговое руководство по автоматизации
- **primary_query:** контент завод
- **secondary_queries:** контент завод ии, автоматизация создания контента, как создать контент завод, контент завод для бизнеса
- **search_intent:** how_to
- **article_mode:** B
- **h2_outline:**
  1. Что такое контент-завод на нейросетях и почему ручной промптинг умер в 2026 году
  2. Архитектура автономного конвейера: связка Make.com, n8n и ИИ-агентов
  3. Настройка ИИ-сотрудников: роли исследователя, копирайтера и редактора (Newsroom)
  4. Автоматическая дистрибуция: автопостинг в Telegram, WordPress и социальные сети
  5. Экономика и ROI контент-завода: как снизить стоимость производства на 85%
- **faq_hints:** как создать контент завод; какие нейросети использовать для контент завода; сколько стоит запуск контент завода для бизнеса
- **internal_links:** /avtomatizaciya-n8n-ai-agents/
- **cover_scene_hint:** футуристический конвейер (завод), на ленте которого вместо деталей собираются светящиеся 3D-иконки постов, логотипы Telegram и WordPress, робот-манипулятор с кистью наносит неоновые надписи "AI Content", яркий diy-коллаж

---

## B06 — Make AI Agents и MCP для бизнеса

- **priority:** P0
- **slug:** make-ai-agents-mcp-avtomatizaciya
- **h1:** Как настроить автоматизацию Make с AI Agents и MCP: пошаговый workflow для бизнеса
- **primary_query:** автоматизация make
- **secondary_queries:** автоматизация make com, автоматизация процессов make, make ai agent, make ии агенты, make сценарии, make com как пользоваться
- **search_intent:** workflow
- **article_mode:** B
- **h2_outline:**
  1. Выбрать процесс для Make AI Agent: где нужен ИИ, а где обычный сценарий
  2. Собрать базовый сценарий Make.com с триггером, действиями и ручным approval
  3. Подключить Make AI Agent внутри canvas и задать инструкции, инструменты и ограничения
  4. Настроить Make MCP Server/Client: как дать агенту доступ к сценариям и внешним инструментам
  5. Проверить безопасность: токены, scopes, логи reasoning panel, лимиты запусков и human-in-the-loop
  6. Чек-лист запуска: тестовые данные, fallback, алерты, стоимость и метрики результата
- **faq_hints:** как пользоваться make; чем Make AI Agents отличаются от обычных сценариев; как подключить MCP к Make; когда выбирать Make, а когда n8n
- **internal_links:** /avtomatizaciya-n8n-ai-agents/, /podklyuchenie-mcp-cursor/
- **cover_scene_hint:** визуальный canvas Make.com с блоками сценария, прозрачный ИИ-агент в центре, MCP-кабель к Cursor/Claude, стикеры "approval", "scopes", "reasoning", яркий diy-коллаж

---

## B07 — RAG-система с векторной базой знаний

- **priority:** P0
- **slug:** postroenie-rag-sistemy-vektornaya-baza
- **h1:** Как построить RAG-систему с векторной базой знаний: пошаговый workflow от документов до ответов
- **primary_query:** rag система
- **secondary_queries:** создание rag системы, локальная rag система, архитектура rag системы, как сделать rag систему, rag система python
- **search_intent:** workflow
- **article_mode:** B
- **h2_outline:**
  1. Выбрать сценарий RAG: когда нужна векторная база, а когда хватит длинного контекста
  2. Подготовить документы: парсинг PDF/DOCX, чанкинг 300–512 токенов и overlap 10–20%
  3. Развернуть векторное хранилище: pgvector в Postgres vs Qdrant/Chroma для PoC
  4. Настроить эмбеддинги и индекс HNSW: размерность, top-k и гибридный поиск BM25+vector
  5. Собрать retrieval-цепочку: reranking, system prompt «только по контексту» и защита от галлюцинаций
  6. Подключить к n8n или API: AI Agent + RAG tool, обновление базы и eval-чеклист качества
- **faq_hints:** как сделать rag систему; чем отличается rag от fine-tuning; какой размер чанка выбрать для rag; pgvector или pinecone для rag в 2026
- **internal_links:** /avtomatizaciya-n8n-ai-agents/, /podklyuchenie-mcp-cursor/
- **cover_scene_hint:** стопка PDF-документов режется на светящиеся чанки, стрелки ведут в цилиндр Postgres/pgvector, из него — в пузырь ответа LLM, стикеры «HNSW», «top-k», «rerank», тёплый неоновый diy-коллаж

---

## B08 — ИИ чат-бот для бизнеса

- **priority:** P0
- **slug:** ii-chat-bot-dlya-biznesa-workflow
- **h1:** Как создать ИИ чат-бот для бизнеса: пошаговый workflow от сценария до запуска
- **primary_query:** чат боты для бизнеса
- **secondary_queries:** ии чат бот для бизнеса, чат бот создать для бизнеса, чат боты для бизнеса в телеграмм, чат боты для бизнеса и автоматизации
- **search_intent:** workflow
- **article_mode:** B
- **h2_outline:**
  1. Выбрать задачу и канал: поддержка, лиды или продажи (Telegram, виджет сайта, MAX)
  2. Собрать базу ответов: FAQ, скрипты операторов и границы «что бот не делает»
  3. Спроектировать диалог: интенты, уточняющие вопросы и правила эскалации к человеку
  4. Собрать бота в n8n или Make: триггер, AI Agent, память и подключение CRM или таблицы
  5. Подключить базу знаний и прогнать тест-кейсы: порог уверенности, логи и защита от галлюцинаций
  6. Чек-лист запуска: метрики FCR и CSAT, мониторинг диалогов и обновление FAQ
- **faq_hints:** как создать чат бот для бизнеса; ии чат бот для бизнеса бесплатно; чат боты для бизнеса в телеграмм; какие чат боты для бизнеса
- **internal_links:** /avtomatizaciya-n8n-ai-agents/, /make-ai-agents-mcp-avtomatizaciya/, /postroenie-rag-sistemy-vektornaya-baza/
- **cover_scene_hint:** смартфон с чатом Telegram и виджет сайта, робот-оператор передаёт стикер «оператор», блок-схема intent→AI→CRM, стикеры FAQ/handoff/CSAT, яркий diy-коллаж

---

## B09 — llms.txt для сайта

- **priority:** P0
- **slug:** sozdat-llms-txt-dlya-sajta
- **h1:** Как создать llms.txt для сайта: чек-лист для попадания в ответы нейросетей
- **primary_query:** llms txt
- **secondary_queries:** файл llms txt, llms txt пример, генератор llms txt, создать llms txt, llms txt в robots txt
- **search_intent:** checklist
- **article_mode:** B
- **h2_outline:**
  1. Проверить, нужен ли сайту llms.txt: какие страницы и ответы нейросетей он должен усилить
  2. Собрать карту страниц: услуги, кейсы, FAQ, авторы и материалы с E-E-A-T сигналами
  3. Создать файл llms.txt по структуре: H1, краткое описание, разделы и ссылки с аннотациями
  4. Настроить robots.txt, sitemap и schema так, чтобы AI-crawlers могли найти файл и ключевые страницы
  5. Проверить результат в ChatGPT, Perplexity, Gemini и Яндекс Нейро: тестовые запросы и таблица мониторинга
  6. Чек-лист обновления: когда менять llms.txt, как не открыть лишнее и как мерить цитирование
- **faq_hints:** что такое llms txt; как создать llms txt; нужен ли llms txt в robots txt; чем отличается llms txt от sitemap; что писать в llms full txt
- **internal_links:** /geo-optimizaciya-sajta-2026/, /primer-seo-stati/
- **cover_scene_hint:** корневой каталог сайта с файлом llms.txt на ярком стикере, рядом robots.txt и sitemap, стрелки к ChatGPT/Perplexity/Яндекс Нейро, чек-лист и замок приватности, тёплый неоновый diy-коллаж

---

## B10 — Локальная LLM через Ollama для бизнеса

- **priority:** P0
- **slug:** ollama-lokalnaya-llm-dlya-biznesa
- **h1:** Как развернуть локальную LLM через Ollama для бизнеса: пошаговый workflow от установки до API
- **primary_query:** ollama
- **secondary_queries:** ollama модели, ollama скачать, ollama api, как установить ollama, локальные нейросети, как локально развернуть нейросеть
- **search_intent:** workflow
- **article_mode:** B
- **h2_outline:**
  1. Выбрать сценарий: когда локальная LLM выгоднее облака (приватность, офлайн, стоимость токенов)
  2. Проверить железо и ОС: RAM, GPU/CPU, Windows vs Linux — таблица минимальных требований под qwen/llama
  3. Установить Ollama, скачать модель (`ollama pull`) и проверить инференс в терминале
  4. Настроить Ollama API и подключить к n8n, Cursor или Python-скрипту автоматизации
  5. Собрать безопасный контур: доступ по сети, логи, обновление моделей и human-in-the-loop для критичных ответов
  6. Чек-лист запуска: latency, качество ответов, fallback на облачную модель и метрики стоимости
- **faq_hints:** как установить ollama; какие ollama модели выбрать для бизнеса; чем ollama отличается от облачного api; как подключить ollama к n8n
- **internal_links:** /avtomatizaciya-n8n-ai-agents/, /podklyuchenie-mcp-cursor/, /postroenie-rag-sistemy-vektornaya-baza/
- **cover_scene_hint:** мини-сервер или ПК с логотипом Ollama, из корпуса — стрелки к qwen/llama-стикерам, кабель API к n8n и Cursor, замок «данные локально», чек-лист RAM/GPU, тёплый неоновый diy-коллаж

