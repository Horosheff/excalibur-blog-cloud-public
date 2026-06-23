# Research notes — B04 «Как настроить GEO-оптимизацию сайта: чек-лист для попадания в ответы нейросетей»

**topic_id:** B04  
**slug:** geo-optimizaciya-sajta-2026  
**article_mode:** B (checklist)  
**research_date:** 2026-06-11  
**disclaimer:** Все даты, версии и статистика проверены на 11.06.2026.

---

## 1. SERP-обзор (WebSearch + research-serp.json, 8 конкурентов)

| # | URL | Тип | Сильные стороны | Слабые / пробелы | Что не копировать |
|---|-----|-----|-----------------|------------------|-------------------|
| 1 | [habr.com/ru/articles/1042732](https://habr.com/ru/articles/1042732/) | Longread RU (Head Promo, 2026) | RAG-архитектура, 7 принципов GEO, кейсы Clatch/Central Trans, разбивка по платформам | Очень длинный; чек-лист «размазан» по тексту, нет 30+ пунктов с приоритетами | Структуру 1:1; агентский tone |
| 2 | [trigub.ru/geo-v-2026-godu](https://trigub.ru/geo-v-2026-godu/) | Практик + чек-лист 50+ | robots.txt, Schema, замеры SoV, различие Алиса vs AI Overviews | Уклон в услуги SEO-агентства; цены «от 25 000 ₽» | Коммерческий bias как основной CTA |
| 3 | [sitegeo.ru](https://sitegeo.ru/) | Справочник чек-листов по типам сайта | 8 типов (e-com, SaaS, B2B, YMYL), приоритеты критично/важно/средне | Нет единого «универсального» чек-листа в одной статье; EN-ориентир | Копировать таблицы 1:1 |
| 4 | [getllmspy.com/ru/blog/geo-aeo-optimizaciya](https://getllmspy.com/ru/blog/geo-aeo-optimizaciya) | RU гайд 2026 | Готовый robots.txt + FAQPage JSON-LD, 35% рунета блокирует GPTBot | Продаёт Getllmspy; часть цифр без первичного источника | Цифры без cross-check как «факт рынка» |
| 5 | [ics-media.ru/blog/marketing/check-list-geo-aeo](https://ics-media.ru/blog/marketing/check-list-geo-aeo/) | Чек-лист GEO/AEO | Техаудит → мониторинг цитирования | Короткий; мало про Яндекс.Бизнес и RU-специфику | Формат agency whitepaper |
| 6 | [digitalrocket.ru/articles/geo-seo-optimizatsiya-neyroseti-2026](https://digitalrocket.ru/articles/geo-seo-optimizatsiya-neyroseti-2026/) | RU how-to + чек-лист | Отдельные блоки Google vs Яндекс Нейро | Поверхностный технический слой | Дублировать «вероятно в 2026» без фактов |
| 7 | [generative-optimization.ru/cheklist-geo-optimizaczii](https://generative-optimization.ru/cheklist-geo-optimizaczii) | Landing-чек-лист | Прямое попадание в H1-intent | Мало доказательной базы, узкий бренд | Thin checklist без контекста |
| 8 | [audit4seo.ru/blog/geo-optimizaciya-2026](https://audit4seo.ru/blog/geo-optimizaciya-2026) | Обзор GEO | llms.txt, Share of Voice, multi-platform | Смешивает GEO (generative) и «гео» локального SEO в сниппетах | Путать Generative Engine Optimization с локальной гео-SEO |

**Паттерн SERP:** топ — длинные гайды 2026 (Хабр, trigub, sitegeo) + чек-листы агентств. Запрос «с чего начать geo оптимизацию» (21 показ/мес) закрыт фрагментарно. Почти никто не даёт **единый чек-лист 30+ пунктов с приоритетами** + **пошаговый старт за одну сессию** для владельца сайта без SEO-команды.

**Intent:** checklist — пользователь хочет **проверить сайт по пунктам**, понять что критично сегодня, настроить robots.txt/Schema/FAQ и **замерить**, цитирует ли его ChatGPT, Алиса, Perplexity. Вторичный intent: чем GEO отличается от SEO и с чего начать.

**Пробел для Excalibur / Maya AI:** практический чек-лист «сделай сам за вечер» на русском: аудит AI-видимости → техдоступ → структура контента → Schema → мониторинг SoV; связка с линейкой B01 (SEO-статья), B02 (автоматизация), B03 (MCP для контент-завода). Угол **автоматизатора**, не «GEO заменит SEO».

---

## 2. Яндекс Wordstat (MCP user-mcp-kv, регион 225, 11.06.2026)

### Таблица спроса

| Фраза | Показы/мес |
|-------|------------|
| geo оптимизация | 981 |
| geo оптимизация сайта | 248 |
| geo seo оптимизация | 67 |
| оптимизация под geo | 51 |
| geo оптимизация гайд | 42 |
| geo оптимизация контента | 29 |
| с чего начать geo оптимизацию | 21 |
| geo ии оптимизация | 19 |
| geo оптимизация под чат джипити и прочие | 19 |
| geo seo (из scout, смежный) | 798 |
| агентство geo оптимизации | 23 |
| geo оптимизация заказать | 45 |

*Примечание:* в Wordstat «похожие запросы» часто уводят в школьную «географию» — в текст не включать.

### LSI для writer (из топа Wordstat + SERP)

- geo оптимизация сайта, geo seo оптимизация, с чего начать geo оптимизацию  
- generative engine optimization, AEO, нейропоиск, AI Overviews, Яндекс Нейро, Алиса AI  
- llms.txt, robots.txt GPTBot, PerplexityBot, Schema.org FAQPage  
- чек-лист geo, answer-first, share of voice / share of model  
- как попасть в ответы chatgpt, цитирование нейросетями  

**SEO-стратегия:** primary «geo оптимизация» (981) + «geo оптимизация сайта» (248) в H1/lead; «с чего начать geo оптимизацию» (21) и faq_hints — в FAQ и H2 «старт»; «geo seo» (798) — в блок GEO vs SEO, не в title целиком (риск путаницы с CEO/«сео»).

---

## 3. Таблица фактов (цифры только с URL)

| Факт | Источник | Дата | Можно в текст |
|------|----------|------|---------------|
| GEO (Generative Engine Optimization) — оптимизация контента для видимости в ответах генеративных поисковых систем | [arxiv.org/html/2311.09735](https://arxiv.org/html/2311.09735) | 11.2023 | да |
| Princeton GEO-bench: 10 000 запросов; методы Cite Sources, Quotation Addition, Statistics Addition дают **+30–40%** visibility (Position-Adjusted Word Count) | [arxiv.org/html/2311.09735](https://arxiv.org/html/2311.09735) | 11.2023 | да |
| На Perplexity.ai авторы зафиксировали улучшение visibility до **37%** | [arxiv.org/html/2311.09735](https://arxiv.org/html/2311.09735) | 11.2023 | да |
| Keyword stuffing в GEO-контексте работает **хуже** baseline (≈ −10%) | [arxiv.org/html/2311.09735](https://arxiv.org/html/2311.09735) | 11.2023 | да |
| Июнь 2025: AI-сервисы направили **>1,13 млрд** переходов на TOP-1000 сайтов; рост **357%** г/г (Similarweb/TechCrunch, цит. в RU-гайде) | [habr.com/ru/articles/1042732](https://habr.com/ru/articles/1042732/) | 2026 | да (как вторичная цитата) |
| **60–80%** пользователей получают ответ в интерфейсе чат-бота без перехода на сайт (цит. Head Promo на Habr) | [habr.com/ru/articles/1042732](https://habr.com/ru/articles/1042732/) | 2026 | да (с оговоркой «по оценке индустрии») |
| HubSpot потерял **70–80%** органических переходов к началу 2026 из-за AI-ответов в поиске (цит. Habr) | [habr.com/ru/articles/1042732](https://habr.com/ru/articles/1042732/) | 2026 | да (как кейс, не как универсальный прогноз) |
| LiveInternet: российские СМИ −**12–15%** просмотров/посетителей в Яндексе/Google (янв–июл, цит. Habr) | [habr.com/ru/articles/1042732](https://habr.com/ru/articles/1042732/) | 2026 | да |
| **44,2%** цитат LLM приходится на первые **30%** текста страницы (Grows Memo, февр. 2026, цит. Habr) | [habr.com/ru/articles/1042732](https://habr.com/ru/articles/1042732/) | 2026 | да |
| **68,7%** цитируемых страниц используют структурированные заголовки (цит. Habr) | [habr.com/ru/articles/1042732](https://habr.com/ru/articles/1042732/) | 2026 | да |
| RAG: генеративные движки (AI Overviews, Яндекс Нейро) извлекают чанки из внешнего индекса и генерируют ответ со ссылками | [habr.com/ru/articles/1045826](https://habr.com/ru/articles/1045826/) | 2026 | да |
| Яндекс Нейро: **5** финальных источников отбираются из **топ-30** органической выдачи | [habr.com/ru/articles/1045826](https://habr.com/ru/articles/1045826/) | 2026 | да |
| YandexGPT в нейроответе опирается на текст источников, а не на «память» модели | [habr.com/ru/articles/1045826](https://habr.com/ru/articles/1045826/) | 2026 | да |
| 22 мая 2025 на «День Поиска» Яндекс: **Алиса** заменила **Нейро**, тексты — **YandexGPT 5 Pro**, изображения — **YandexART 2.5** | [ashmanov.com/education/articles/obnovleniya-poiska-yandeksa-alisa-vmesto-neyro-vertikali-i-drugie-ii-novinki](https://www.ashmanov.com/education/articles/obnovleniya-poiska-yandeksa-alisa-vmesto-neyro-vertikali-i-drugie-ii-novinki/) | 05.2025 | да |
| Около **35%** русскоязычных сайтов блокируют **GPTBot** в robots.txt (оценка Getllmspy) | [getllmspy.com/ru/blog/geo-aeo-optimizaciya](https://getllmspy.com/ru/blog/geo-aeo-optimizaciya) | 2026 | да (как оценка рынка, не официальная статистика Яндекса) |
| **74%** брендов из топ-10 Google присутствуют в ответах ChatGPT; корреляция позиции и AI-упоминания **0,65** (Seer Interactive, 2025, цит. Getllmspy) | [getllmspy.com/ru/blog/geo-aeo-optimizaciya](https://getllmspy.com/ru/blog/geo-aeo-optimizaciya) | 2026 | да |
| Формат «вопрос → прямой ответ до **80 слов**» — наиболее цитируемый LLM-формат (Getllmspy) | [getllmspy.com/ru/blog/geo-aeo-optimizaciya](https://getllmspy.com/ru/blog/geo-aeo-optimizaciya) | 2026 | да |
| llms.txt **не заменяет** robots.txt; на Habr указано, что использование llms.txt пока **не обязательно** | [habr.com/ru/articles/1042732](https://habr.com/ru/articles/1042732/) | 2026 | да |
| Schema.org: Product, Organization, Article, HowTo, **FAQPage** снижают риск «галлюцинаций» при описании бренда | [habr.com/ru/articles/1042732](https://habr.com/ru/articles/1042732/) | 2026 | да |
| GPTBot, PerplexityBot, OAI-SearchBot, Google-Extended, YandexAdditional должны быть **не заблокированы** без веской причины | [trigub.ru/geo-v-2026-godu](https://trigub.ru/geo-v-2026-godu/) | 2026 | да |
| AI-краулеры часто **не выполняют JavaScript** — основной контент должен быть в HTML | [trigub.ru/geo-v-2026-godu](https://trigub.ru/geo-v-2026-godu/) | 2026 | да |
| Google-Extended блокируется **только через robots.txt** product token; не путать с Googlebot | [fokal.com/ai-seo/ai-crawler-access](https://www.fokal.com/ai-seo/ai-crawler-access/) | 2026 | да |
| Крупные бренды: прирост трафика до **30%**; контентные сайты: потеря до **30%** органики от генеративного поиска (PR-CY про Алису AI) | [pr-cy.ru/news/p/10545-yandex-neuro](https://pr-cy.ru/news/p/10545-yandex-neuro) | 2026 | да (диапазон, не среднее) |
| Первые сдвиги в AI-цитируемости после Schema/robots — **3–6 недель**; устойчивый SoV — **2–3 месяца** (trigub, отраслевая практика) | [trigub.ru/geo-v-2026-godu](https://trigub.ru/geo-v-2026-godu/) | 2026 | да (как ориентир, не SLA) |

**fact-bank.md:** пуст для GEO — все цифры только из таблицы выше.

**Не использовать без оговорки:** «GEO вытесняет SEO» (vc.ru marketing-хайп); «llms.txt обязателен для всех»; локальная «гео-SEO» (Google Maps) как синоним Generative Engine Optimization.

---

## 4. Угол статьи (utility-only, режим B)

**Главный угол:** за **одну рабочую сессию (60–90 мин)** пройти **аудит AI-видимости** и внедрить **минимальный GEO-стек**: robots.txt для AI-ботов → answer-first блоки + FAQ → JSON-LD (FAQPage, Article, Organization) → sitemap → **ручной замер** 20–30 промптов в ChatGPT/Алисе/Perplexity. В теле — **чек-лист 30+ пунктов** с метками 🔴 критично / 🟡 важно / 🟢 бонус.

**Почему отличается от конкурентов:**
- Хабр/trigub — encyclopedia; у нас **action-first checklist** с приоритетами.
- sitegeo — 8 разрозненных чек-листов; у нас **один универсальный** + отсылка «для e-com/SaaS доработайте X».
- Agency-лендинги продают услуги; Excalibur — **DIY для автоматизатора** + связка с контент-заводом (B02/B03).
- Явно разводим **GEO (generative)** и локальную гео-SEO, чтобы не ловить не тот intent.

**Tone:** «GEO = SEO + структура для цитирования ИИ»; без паники «SEO мёртв»; каждый H2 заканчивается «что проверить руками».

**H2-каркас (из карточки + research):**
1. GEO vs SEO в 2026: цель — цитирование, не только клик  
2. Быстрый аудит: 10 промптов + robots.txt + Rich Results Test  
3. Контент под RAG: answer-first, блоки 40–80 слов, FAQ, таблицы  
4. Schema.org и HTML-доступность для AI-краулеров  
5. Чек-лист 30+ пунктов (критично / важно / бонус)  
6. Мониторинг Share of Voice: таблица промптов, частота замеров  
7. FAQ  

**Conversion (conversion-map.md):**
- CTA Make/kv-ai — max 2×: «автоматизируйте мониторинг промптов и обновление FAQ»  
- Internal: [/primer-seo-stati/](/primer-seo-stati/) (B01), B02 n8n, B03 MCP  
- Telegram @maya_pro — 1× если уместно  

---

## 5. Черновик чек-листа (30+ пунктов для writer)

### 🔴 Критично (12)

1. Открыть `https://site.ru/robots.txt` — нет `Disallow: /` для AI-ботов без причины.  
2. Разрешить GPTBot, OAI-SearchBot, PerplexityBot, ClaudeBot/anthropic-ai, Google-Extended, YandexBot/YandexAdditional.  
3. Проверить, что ключевые страницы отдают контент **без обязательного JS** (view-source).  
4. На каждой money-page: **прямой ответ** в первых 1–2 абзацах после H1/H2.  
5. Добавить блок FAQ **5–7** реальных вопросов клиентов; ответ **≤80 слов** каждый.  
6. Внедрить JSON-LD **FAQPage** на страницах с FAQ.  
7. JSON-LD **Organization** + **WebSite** на главной; **Article** на блоге (author, datePublished, dateModified).  
8. Проверить разметку в [Google Rich Results Test](https://search.google.com/test/rich-results).  
9. Актуальный **sitemap.xml** с блогом, FAQ, кейсами, карточками услуг.  
10. Title ≤60 символов, meta description ≤160 — с формулировкой вопроса пользователя.  
11. Указать **дату публикации и обновления** на видимом месте (не только в schema).  
12. Прогнать **20–30 промптов** ниши в ChatGPT + Алиса + Perplexity; зафиксировать, цитируют ли сайт/бренд.

### 🟡 Важно (12)

13. Таблица сравнения или список с цифрами на ключевых landing (Princeton: stats ↑ visibility).  
14. Блок «краткий вывод / TL;DR» в начале longread.  
15. H2–H4 без пропусков уровней; один H1 на страницу.  
16. Внутренняя перелинковка hub → spoke (pillar + FAQ).  
17. Страница автора с bio, sameAs (LinkedIn, ORCID, профиль компании).  
18. About/Contacts: NAP, юрлицо, реквизиты (важно для GigaChat/локальных AI в РФ).  
19. Яндекс.Бизнес / 2GIS — для B2C локального (отдельный подблок, не путать с GEO-term).  
20. Обновить устаревшие статьи с датой «2023–2024» в title без refresh.  
21. Убрать keyword stuffing и «SEO-вода» — хуже для GEO (Princeton baseline).  
22. Добавить исходящие ссылки на **авторитетные** источники там, где даёте цифры.  
23. Скорость ответа сервера: TTFB не блокирует краул (ориентир <2–3 с для AI fetch).  
24. Проверить, что paywall/login не закрывает контент, который должен цитироваться.

### 🟢 Бонус (8+)

25. Файл **llms.txt** в корне (опционально; не вместо robots.txt).  
26. HowTo schema для пошаговых инструкций.  
27. Person schema для экспертов команды.  
28. Review/AggregateRating где legally applicable.  
29. Wikidata / consistent `@id` + sameAs для entity graph.  
30. UGC-сигналы: текстовые отзывы на индексируемых площадках.  
31. Экспертные гостевые статьи на Habr/vc.ru/отраслевых медиа.  
32. Ежемесячный re-measure SoV + журнал изменений на сайте.

---

## 6. FAQ-кандидаты (5–7)

1. **С чего начать GEO-оптимизацию?** — robots.txt + 10 тестовых промптов + FAQ-блок на главной money-page.  
2. **Чем GEO отличается от SEO?** — SEO = позиция и клик; GEO = попадание в синтезированный ответ ИИ (цитирование).  
3. **Нужна ли Schema для GEO?** — да, FAQPage/Article/Organization — гигиенический минимум 2026.  
4. **Как попасть в ответы Яндекс Нейро / Алисы?** — топ-30 органики + структура + answer-first; 5 источников в ответе.  
5. **Обязателен ли llms.txt?** — нет; приоритет robots.txt + HTML + Schema.  
6. **Сколько ждать результат?** — техправки 3–6 недель; устойчивый SoV 2–3 месяца замеров.  
7. **GEO заменяет SEO?** — нет; 74% брендов из топ-10 Google есть в ChatGPT — SEO остаётся фундаментом.

---

## 7. GEO hooks

| Hook | Где | Формат |
|------|-----|--------|
| Определение GEO 40–60 слов | Lead | «GEO — Generative Engine Optimization…» |
| Таблица SEO vs GEO vs AEO | H2-1 | 3 колонки, 5–6 строк |
| Мини-аудит robots.txt | H2-2 | Пример Allow + список User-agent |
| Чек-лист 30+ | H2-5 | 🔴🟡🟢 + checkbox markdown |
| Шаблон таблицы мониторинга промптов | H2-6 | Промпт / ChatGPT / Алиса / Perplexity / дата |
| FAQ 5–7 | Конец | FAQPage schema |
| E-E-A-T | Автор | Экспертиза Maya AI / автоматизация + SEO |

**Целевые формулировки:** «geo оптимизация сайта», «с чего начать geo оптимизацию», «geo seo оптимизация», «чек-лист geo».

---

## 8. Риски для writer

- Не путать **GEO (generative)** с **локальной geo-SEO** (Google Maps, «рядом со мной»).  
- Не выдумывать проценты «+300% за неделю» — только из таблицы фактов.  
- llms.txt — **опционально**, с оговоркой Habr/Getllmspy/Fokal.  
- Объём: **8 500–9 500** знаков (quality-blog) + чек-лист может быть длиннее в таблице.  
- Min **5** нумерованных шагов в action_outline + чек-лист **30+** пунктов.  
- Без эмодзи в article.html (в research — допустимо для приоритетов; writer решает по style guide).  
- Internal link: `/primer-seo-stati/` из карточки темы.

---

## 9. Utility gate (research)

**utility_verdict:** PASS

**reader_outcome:** Читатель проверит robots.txt на блокировку AI-ботов, добавит answer-first блоки и FAQ со Schema, пройдёт чек-лист 30+ пунктов с приоритетами, создаст таблицу 20–30 промптов для мониторинга цитирования в ChatGPT, Алисе и Perplexity и поймёт, какие правки делать в первую очередь.

**action_outline (для checklist-статьи):**

1. **Зафиксировать baseline:** составить 20–30 промптов (брендовые, коммерческие, информационные) и прогнать в ChatGPT, Яндекс (Алиса/нейроответ), Perplexity — записать, есть ли цитата сайта/бренда.  
2. **Техаудит доступа:** открыть `/robots.txt`; убрать блокировки GPTBot, PerplexityBot, OAI-SearchBot, ClaudeBot, Google-Extended, Yandex-ботов; сохранить запрет только для чувствительных разделов.  
3. **Проверить HTML-доступность:** view-source ключевых URL — основной текст виден без JS; при SPA — SSR/пререндер или статические fallback-блоки.  
4. **Перестроить 3–5 priority-страниц:** после каждого H2 — 1–2 абзаца прямого ответа; добавить TL;DR в начало; блок FAQ 5–7 вопросов (ответ ≤80 слов).  
5. **Внедрить Schema.org JSON-LD:** FAQPage на FAQ-блоках, Article на статьях, Organization/WebSite на главной; прогнать Rich Results Test.  
6. **Обновить sitemap.xml** и даты `dateModified` на изменённых страницах; перелинковать hub-страницу с FAQ и кейсами.  
7. **Пройти чек-лист 30+ пунктов** (раздел 5): отметить 🔴, затем 🟡, затем 🟢; зафиксировать дедлайны на 2 недели.  
8. **Настроить мониторинг SoV:** таблица промптов × платформы × дата; повторять каждые 2–4 недели; при росте — масштабировать шаблон на остальные URL.  
9. **Опционально llms.txt + внешние упоминания:** после закрытия 🔴 пунктов — llms.txt в корне; одна экспертная публикация/интервью для entity signals.

---

## 10. Готовность к writer

| Критерий | Статус |
|----------|--------|
| Utility gate темы | PASS |
| SERP ≥ 3 конкурента | ✅ (8) |
| Wordstat MCP | ✅ |
| Таблица фактов с URL | ✅ (24 факта) |
| utility_verdict + action_outline | ✅ |
| Чек-лист 30+ черновик | ✅ |
| FAQ 5–7 | ✅ |
| GEO hooks | ✅ |

**Writer:** готов. Вход: этот файл + `research-context.json` + карточка B04 + `site-brief.md` + `conversion-map.md`.

---

=== EXCALIBUR BLOG RESEARCH ===
topic_id: B04
article_dir: memory/blog/articles/B04-geo-optimizaciya-sajta-2026
status: ✅ PASS
utility_verdict: PASS
summary: SERP — 8 конкурентов (Habr 1042732, trigub, sitegeo, getllmspy, ics-media, digitalrocket, generative-optimization.ru, audit4seo). Wordstat: geo оптимизация 981, geo оптимизация сайта 248. Угол — DIY чек-лист 30+ пунктов (🔴🟡🟢) + аудит robots.txt/Schema/FAQ + мониторинг SoV за 60–90 мин. 24 факта с URL, 9 шагов action_outline, 7 FAQ. Готов к writer.
===
