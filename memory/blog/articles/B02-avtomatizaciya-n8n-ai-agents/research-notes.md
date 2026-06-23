# Research notes — B02 «Как настроить ИИ-агентов в n8n: пошаговое руководство по автоматизации бизнеса»

**topic_id:** B02  
**slug:** avtomatizaciya-n8n-ai-agents  
**article_mode:** B (how-to + comparison)  
**research_date:** 2026-06-11  
**disclaimer:** Все даты, версии и статистика проверены на 11.06.2026.

---

## 1. SERP-обзор (WebSearch + research-serp.json, 8 конкурентов)

| # | URL | Тип | Сильные стороны | Слабые / пробелы | Что не копировать |
|---|-----|-----|-----------------|------------------|-------------------|
| 1 | [bot-craft.ru/blog/n8n-automation-2026](https://bot-craft.ru/blog/n8n-automation-2026/) | Агентский longread (2026) | Self-hosted vs Cloud, цены, кейсы «сайт → CRM → уведомление», контекст ухода Zapier из РФ | Мало пошаговой настройки AI Agent; продаёт услуги интегратора | Цены «под ключ» без первичника; sales-CTA агентства |
| 2 | [neiroscop.ru/blog/n8n-avtomatizaciya-s-ai-gajd](https://neiroscop.ru/blog/n8n-avtomatizaciya-s-ai-gajd) | AI-гайд (2026) | AI + бизнес-кейсы, упоминание reasoning chains | Общие формулировки, слабая техника нод | Непроверенные цифры «15–20 ч/нед экономии» |
| 3 | [lpmotor.ru/articles/kak-sozdat-i-nastroit-ii-agenta-v-n8n-polnoe-rukovodstvo-2603](https://lpmotor.ru/articles/kak-sozdat-i-nastroit-ii-agenta-v-n8n-polnoe-rukovodstvo-2603) | Пошаговый how-to (март 2026) | Близко к H1: Chat Trigger, AI Agent, System Message, Max Iterations | Нет сравнения с Make; нет RAG-блока | Структуру 1:1; коммерческий хвост LPmotor |
| 4 | [fulcrumlabs.ru/blog/sozdanie-ii-chat-agenta-v-n8n](https://fulcrumlabs.ru/blog/sozdanie-ii-chat-agenta-v-n8n-polnoe-rukovodstvo-dlya-nachinayushih/) | Гайд для новичков | Простой язык, чат-агент с нуля | Узкий фокус (только чат), без бизнес-кейсов и comparison | Короткий объём без comparison |
| 5 | [ai-uchi.ru/guides/avtomatizatsiia-s-n8n-i-ai-poshagovyi-gaid](https://ai-uchi.ru/guides/avtomatizatsiia-s-n8n-i-ai-poshagovyi-gaid/) | Глубокий гайд (2025–2026) | MCP, Human-in-the-Loop, LangChain, Docker-установка | Техничнее аудитории «Ковчег»; нет Make-сравнения | Перегруз DevOps-деталями для не-программистов |
| 6 | [neiropotok.ru/blog/n8n-ai-agent-bez-koda](https://neiropotok.ru/blog/n8n-ai-agent-bez-koda) | Практик + comparison | Таблица n8n vs Make vs Zapier по AI; Telegram-кейс за 30 мин | Односторонний bias в пользу n8n; нет Make AI Agents 2026 | Копировать таблицу без перепроверки и баланса |
| 7 | [docs.n8n.io/advanced-ai/intro-tutorial](https://docs.n8n.io/advanced-ai/intro-tutorial/) | Официальный tutorial | Канон: Chat Trigger → AI Agent → Chat Model → Memory; LLM vs Agent | Нет бизнес-контекста, RAG, comparison | Сухой перевод docs без «на пальцах» |
| 8 | [make.com/en/ai-agents](https://www.make.com/en/ai-agents) | Официальный продукт (конкурент) | Make AI Agents: Reasoning panel, 3000+ apps, без кода | Нет n8n-инструкции (ожидаемо) | Не продавать Make вместо гайда; использовать как источник фактов для comparison |

**Паттерн SERP:** топ — «n8n + AI 2026» longread и пошаговые гайды по AI Agent node. Отдельный кластер — курсы («ИИ агенты и автоматизация с n8n» на Stepik, Softline). Сравнение n8n vs Make встречается точечно (neiropotok, flowframe), но без позиции практика Make-клуба.

**Intent:** how_to — пользователь хочет собрать первого ИИ-агента в n8n и понять, не проще ли Make/Zapier. Вторичный intent: RAG/база знаний, self-hosted vs cloud, цена.

**Пробел для «Ковчег»:** честный гайд n8n + comparison с Make.com от практика Make (Артур), язык для не-программистов, CTA на курс когда self-host/DevOps не нужен.

---

## 2. Яндекс Wordstat (MCP user-mcp-kv, регион 225, 11.06.2026)

### Таблица спроса

| Фраза | Показы/мес |
|-------|------------|
| n8n | 37 115 |
| n8n ai | 720 |
| n8n агенты | 699 |
| n8n ии | 553 |
| автоматизация n8n | 539 |
| n8n docker | 498 |
| n8n cloud | 498 |
| обучение n8n | 401 |
| n8n установка | 364 |
| автоматизация ии n8n | 56 |
| ai автоматизация и n8n | 54 |
| примеры автоматизации n8n | 35 |
| ai агенты и автоматизация с n8n | 30 |
| ии агенты и n8n | 74 |
| создание ии агента n8n | 52 |
| ии агенты и автоматизация с n8n | 29 |
| как создать ии агента в n8n | 17 |
| автоматизация бизнеса n8n | 17 |

### LSI для writer (из топа Wordstat + SERP)

- n8n ai agent node, chat trigger, system message, simple memory  
- n8n docker / self-hosted / cloud  
- n8n vs make / make ai agents  
- rag n8n vector store база знаний  
- telegram bot n8n ai  
- mcp n8n langchain  
- примеры автоматизации n8n для бизнеса  

**SEO-стратегия:** primary «автоматизация n8n» (539) + head «n8n» (37k) через H2/H3; secondary «n8n ai», «n8n агенты», «создание ии агента n8n».

---

## 3. Таблица фактов (цифры только с URL)

| Факт | Источник | Дата | Можно в текст |
|------|----------|------|---------------|
| n8n Cloud Starter: 20 €/мес (годовая оплата), 2 500 executions | [n8n.io/pricing](https://n8n.io/pricing/) | 11.06.2026 | да |
| n8n Cloud Pro: 50 €/мес, 10 000 executions | [n8n.io/pricing](https://n8n.io/pricing/) | 11.06.2026 | да |
| n8n Business: 667 €/мес, 40 000 executions, self-hosted | [n8n.io/pricing](https://n8n.io/pricing/) | 11.06.2026 | да |
| n8n считает execution = один полный прогон workflow, не каждый шаг | [n8n.io/pricing](https://n8n.io/pricing/) | 11.06.2026 | да |
| Community Edition на GitHub: self-hosted, без лимита executions в лицензии | [n8n.io/pricing](https://n8n.io/pricing/) | 11.06.2026 | да |
| Cloud trial Starter/Pro: 14 дней, карта не нужна | [n8n.io/pricing](https://n8n.io/pricing/) | 11.06.2026 | да |
| Данные hosted n8n хранятся в EU (Frankfurt) | [n8n.io/pricing](https://n8n.io/pricing/) | 11.06.2026 | да |
| AI Agent node: LLM + tools + memory; агент выбирает действия, LLM только генерирует текст | [docs.n8n.io/advanced-ai/intro-tutorial](https://docs.n8n.io/advanced-ai/intro-tutorial/) | 11.06.2026 | да |
| Порядок в tutorial: Chat Trigger → AI Agent → OpenAI Chat Model → System message → Simple Memory | [docs.n8n.io/advanced-ai/intro-tutorial](https://docs.n8n.io/advanced-ai/intro-tutorial/) | 11.06.2026 | да |
| Simple Memory по умолчанию: 5 interactions | [docs.n8n.io/advanced-ai/intro-tutorial](https://docs.n8n.io/advanced-ai/intro-tutorial/) | 11.06.2026 | да |
| AI Agent node требует n8n 1.19.0+ | [kevinamayi.com](https://kevinamayi.com/how-to-build-an-n8n-ai-agent-step-by-step-tutorial/) | 2026 | да |
| Рекомендуемый порядок setup: trigger → model → tools → memory → prompt rules | [synta.io](https://synta.io/blog/n8n-ai-agent-node-complete-setup-and-tutorial-2026) | 2026 | да |
| Tools Agent — рекомендуемый тип для GPT-4, Claude 3, Gemini 1.5 (function calling) | [scriflow.busca.software](https://scriflow.busca.software/blog/en/n8n-ai-agent-langchain) | 2026 | да |
| n8n AI Agents: memory, tools, human-in-the-loop, MCP server | [n8n.io/ai-agents](https://n8n.io/ai-agents/) | 11.06.2026 | да |
| MCP Client Tool + MCP Server Trigger анонсированы n8n (апрель 2025) | [community.n8n.io](https://community.n8n.io/t/we-re-adding-mcp-client-tool-mcp-trigger-nodes-try-them-now/99338) | 10.04.2025 | да |
| Instance-level MCP: рекомендуется n8n 2.18.4+ | [blog.n8n.io/n8n-mcp-server](https://blog.n8n.io/n8n-mcp-server/) | 29.04.2026 | да |
| Make AI Agents доступны на всех тарифах | [make.com/en/ai-agents](https://www.make.com/en/ai-agents) | 11.06.2026 | да |
| Make Free: 1 000 credits/мес | [make.com/en/pricing](https://www.make.com/en/pricing) | 11.06.2026 | да |
| Make Core/Pro/Teams: базово 10 000 credits/мес (тарифы отличаются фичами) | [make.com/en/pricing](https://www.make.com/en/pricing) | 11.06.2026 | да |
| Make: 3 000+ интеграций, визуальный builder без кода | [make.com/en/ai-agents](https://www.make.com/en/ai-agents) | 11.06.2026 | да |
| Make native AI modules: динамическое списание credits (не всегда 1:1); внешний LLM через HTTP ≈ 1 credit + оплата провайдеру | [hookdeck.com](https://hookdeck.com/webhooks/platforms/how-to-reduce-make-com-credit-usage) | 2026 | да |
| Курс Make.com kv-ai.ru: подписка 5 800 ₽/мес, 159+ уроков | [site-brief / kv-ai.ru](https://kv-ai.ru/obuchenie-po-make) | 11.06.2026 | да (единственный верифицированный прайс продукта) |

**Не использовать без первичника:** «~1 750 ₽/мес VPS+API» (1develop.ru); «15–20 ч/нед экономии» (neiroscop, landingpro); «10 011 шаблонов» — можно как «10 000+» со ссылкой на [n8n.io/workflows](https://n8n.io/workflows/) если writer проверит актуальное число на странице.

---

## 4. Угол статьи (utility-only, режим B)

**Главный угол:** пошагово собрать **первого рабочего ИИ-агента в n8n** (Chat Trigger + AI Agent + модель + 1–2 tools + memory) и **принять решение**: оставаться на n8n или перейти на **Make.com** для того же бизнес-кейса без серверов и DevOps.

**Почему отличается от конкурентов:**
- Официальный tutorial n8n не сравнивает с Make и не переводит на язык предпринимателя.
- Русскоязычные гайды либо продают n8n-услуги, либо хвалят n8n без честного «когда Make проще».
- «Ковчег»: эксперт Make (Артур) показывает n8n честно, comparison с таблицей, мягкий CTA на курс Make для аудитории без техбэкграунда.

**Tone:** по-человечески; RAG, MCP, webhook, LangChain — сразу «на пальцах». Без снобизма «n8n для всех» и без обесценивания n8n.

**H2-каркас (из карточки + research):**
1. Почему n8n + ИИ-агенты в 2026 (self-host, LangChain, MCP) — коротко, 1 экран
2. Пошаговая настройка первого AI Agent (Chat Trigger, модель, System Message, tools)
3. Память и RAG без кода (Simple Memory → Vector Store + документы)
4. Примеры автоматизации для бизнеса (support-бот, лиды, контент)
5. **Сравнение n8n vs Make.com: таблица + «выбирай n8n если… / Make если…»**
6. FAQ + чеклист перед продакшеном

**Conversion (conversion-map.md):**
- CTA курс Make: max 2× → [kv-ai.ru/obuchenie-po-make](https://kv-ai.ru/obuchenie-po-make) — в блоке comparison и финале
- Telegram @maya_pro — только если уместно (1×)
- Профиль автора — 1× для E-E-A-T

**Internal link:** `/services/` (из карточки)

---

## 5. Comparison-матрица (черновик для writer)

| Критерий | n8n | Make.com |
|----------|-----|----------|
| Установка | Cloud trial или self-host (Docker/VPS) | SaaS, регистрация за минуты |
| AI Agent | Native AI Agent node (LangChain), tools, memory, MCP | Make AI Agents, Reasoning panel, 3000+ apps |
| Self-host / данные в РФ | Да (Community Edition) | Нет (облако Make) |
| Цена входа | CE бесплатно + infra; Cloud от 20 €/мес | Free 1 000 credits; Core от ~$9–12/мес |
| Модель billing | Executions (весь workflow = 1 run) | Credits (модули; AI-native — дороже) |
| Аудитория | Техкоманды, агенты с RAG/MCP, self-host | Маркетологи, ops, no-code без серверов |
| Обучение в экосистеме автора | Мало рус. community | Курс «Ковчег» 159+ уроков, @maya_pro |

**Позиция автора:** n8n — когда нужен контроль, RAG, MCP, локальные модели. Make — когда нужна скорость, команда без DevOps, контент-заводы и CRM-воронки «из коробки».

---

## 6. FAQ-кандидаты (5–7)

1. **Как устроен AI Agent node в n8n?** — узел-оркестратор: принимает prompt, подключает Chat Model, Memory и Tools sub-nodes; агент сам выбирает инструменты.
2. **Чем n8n отличается от Make в 2026?** — n8n: self-host, executions, глубокие AI/MCP; Make: managed SaaS, credits, 3000+ apps, Make AI Agents без серверов.
3. **Как подключить базу знаний (RAG) к ИИ в n8n?** — Document Loader + Vector Store + tool retrieval в AI Agent; пошагово в H2-3.
4. **Нужен ли Docker для n8n?** — не обязательно: есть n8n Cloud trial; self-host чаще через Docker Compose.
5. **Сколько стоит n8n для малого бизнеса?** — CE бесплатно + VPS; Cloud от 20 €/мес за 2 500 runs; API LLM отдельно.
6. **Когда выбрать Make вместо n8n?** — нет желания админить сервер; команда no-code; типовые интеграции CRM/SMM/Telegram.
7. **Какие типичные ошибки при первом агенте?** — слишком много tools, нет System Message, memory включена без нужды, нет Continue on Error на tools.

---

## 7. GEO hooks

| Hook | Где | Формат |
|------|-----|--------|
| Определение «ИИ-агент в n8n» 40–60 слов | Lead после H1 | «ИИ-агент в n8n — …» |
| Таблица n8n vs Make | H2-5 | Сравнительная таблица + 2 списка «выбирай если» |
| Workflow-схема | H2-2 | Chat Trigger → AI Agent → Model/Tools/Memory |
| FAQ 5–7 | Конец | Короткие ответы-действия |
| Island test | QA | Каждый H2 = подзадача + рекомендация |
| Schema | handoff schema | BlogPosting + FAQPage |
| E-E-A-T | Автор | Артур Хорошев, практик Make + AI |

**Целевые формулировки:** «автоматизация n8n», «n8n ai агент», «n8n vs make», «как создать ии агента в n8n», «rag n8n».

---

## 8. Риски для writer

- Не выдумывать цены n8n/Make кроме таблицы фактов; прайс продукта «Ковчег» — только 5 800 ₽/мес.
- Не копировать структуру lpmotor/neiropotok 1:1.
- Объём: 8 500–9 500 знаков (quality-blog).
- Без эмодзи; дефис вместо длинного тире; прямые кавычки.
- Comparison честный: n8n сильнее в AI-depth, Make — в скорости и no-code для ЦА блога.
- Min 5 нумерованных шагов + comparison-таблица + чеклист 10+ пунктов (utility gate статьи).

---

## 9. Utility gate (research)

**utility_verdict:** PASS

**reader_outcome:** Читатель соберёт первого ИИ-агента в n8n (триггер, модель, system prompt, инструменты, опционально память/RAG), протестирует в Chat UI и по таблице решит, оставаться на n8n или быстрее закрыть тот же кейс на Make.com без self-host.

**action_outline (для writer):**

1. **Выбрать способ запуска:** n8n Cloud (14-day trial) или self-hosted Docker; параллельно оценить Make Free для no-code-кейса.
2. **Создать workflow:** Chat Trigger → AI Agent node на пустом canvas.
3. **Подключить Chat Model** (OpenAI gpt-4o-mini / Anthropic) + credentials API-ключа.
4. **Написать System Message:** роль агента, когда вызывать tools, формат ответа, лимиты (не выдумывать факты).
5. **Добавить 1–3 Tool sub-nodes** (HTTP Request или Call n8n Workflow) с понятными именами и description для LLM.
6. **Включить Simple Memory** (если мультитёрновый чат) или пропустить на первом MVP.
7. **Протестировать в Chat UI,** открыть Logs AI Agent, исправить типичные ошибки (лишние tools, нет fallback).
8. **Опционально RAG:** Document Loader + Vector Store → tool «search knowledge base» для support-бота.
9. **Сравнить с Make AI Agents** по таблице из раздела 5 и зафиксировать выбор платформы под свой кейс; при выборе Make — CTA на курс.

---

## 10. Готовность к writer

| Критерий | Статус |
|----------|--------|
| Utility gate темы | PASS |
| SERP ≥ 3 конкурента | ✅ (8) |
| Wordstat MCP | ✅ |
| Таблица фактов с URL | ✅ (21 факт) |
| utility_verdict + action_outline | ✅ |
| Comparison n8n vs Make | ✅ |
| FAQ 5–7 | ✅ |
| GEO hooks | ✅ |

**Writer:** готов. Вход: этот файл + `research-context.json` + карточка B02 + `site-brief.md` + `conversion-map.md`.
