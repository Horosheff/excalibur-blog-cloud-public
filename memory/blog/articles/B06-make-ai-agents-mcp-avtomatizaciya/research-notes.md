# Research notes — B06 «Как настроить автоматизацию Make с AI Agents и MCP: пошаговый workflow для бизнеса»

**topic_id:** B06  
**slug:** make-ai-agents-mcp-avtomatizaciya  
**article_mode:** B (workflow)  
**research_date:** 2026-06-16  
**disclaimer:** Все даты, версии и статистика проверены на 16.06.2026.

---

## 1. SERP-обзор (WebSearch Cursor, 16.06.2026)

| # | URL | Тип | Сильные стороны | Слабые / пробелы | Что не копировать |
|---|-----|-----|-----------------|------------------|-------------------|
| 1 | [developers.make.com/mcp-server](https://developers.make.com/mcp-server) | Официальная docs Make | Канон: сценарии как tools, scopes, transport (Streamable HTTP/SSE), timeout, executionId | Для разработчиков; нет русской бизнес-инструкции | Сухой перевод без workflow и safety-чеклиста |
| 2 | [make.com/en/ai-agents](https://www.make.com/en/ai-agents) | Официальная продуктовая страница | 3000+ apps, visual builder, Reasoning panel, manual approvals, отличие от ChatGPT | Маркетинг, мало пошаговых шагов | Обещания «агенты сделают всё» без ограничений |
| 3 | [make.com/en/blog/make-ai-agents-trust-through-transparency](https://www.make.com/en/blog/make-ai-agents-trust-through-transparency) | Официальный deep dive | Agent vs standard modules, 5 паттернов, cost control, hybrid design | EN, требует адаптации под no-code RU | Перегруз теорией без сборки |
| 4 | [make.com/en/blog/model-context-protocol-mcp-server](https://www.make.com/en/blog/model-context-protocol-mcp-server) | Официальный MCP-гайд | No-code MCP Server: token, cloud gateway, сценарии как tools | Нет связки с AI Agents внутри canvas | Утверждать «без затрат» без оговорки про credits |
| 5 | [community.make.com/t/feature-spotlight-add-mcp-tools-to-make-ai-agents/110260](https://community.make.com/t/feature-spotlight-add-mcp-tools-to-make-ai-agents/110260) | Make Community (июнь 2026) | External MCP servers в Make AI Agent builder; mix MCP tools + native modules в одном run | Community, не полная docs | Продавать как mature enterprise без теста |
| 6 | [mayai.ru/make-ai-agents-gayd-biznes](https://mayai.ru/make-ai-agents-gayd-biznes/) | RU практический конкурент / свой кластер | Tools, Reasoning Panel, MCP, бизнес-кейсы, тарифы credits | Риск каннибализации B06; часть фактов — вторичные | Копировать структуру 1:1 |
| 7 | [mayai.ru/make-com-i-mcp-kak-vnedrit-agentov-dlya-avtomatizaczii-kontenta](https://mayai.ru/make-com-i-mcp-kak-vnedrit-agentov-dlya-avtomatizaczii-kontenta/) | RU how-to MCP+Make | Контент-кейс, гибрид «мозг + руки» | Узкий контент-угол | Расширять до «только контент-завод» |
| 8 | [vc.ru/ai/1962053-avtomatizatsiya-biznes-protsessov-s-make-com](https://vc.ru/ai/1962053-avtomatizatsiya-biznes-protsessov-s-make-com) | RU обзор Make | Триггер → действие, beginner-friendly | Нет AI Agents/MCP/governance | Длинный ввод «что такое Make» |
| 9 | [soloai.ru/vibe/make-automation-guide](https://soloai.ru/vibe/make-automation-guide) | RU beginner guide 2026 | Первый сценарий, Maia, модули | Нет MCP и security | Копировать H2 «как пользоваться» как основу статьи |
| 10 | [help.make.com/make-ai-agents](https://help.make.com/make-ai-agents) | Help Center | Канонический раздел docs (обновлён 03.02.2026) | Минимум текста на landing | Ссылаться как primary для терминов |

**Паттерн SERP:** три кластера — официальный Make (AI Agents + MCP Server/Client), русские how-to «автоматизация make com / как пользоваться», общие статьи про ИИ-агентов 2026. Запросы с MCP + Make AI Agents на русском почти не закрыты одной практической инструкцией с scopes, approval и cost control.

**SERP intent:** workflow. Пользователь ищет не обзор платформы, а последовательность: выбрать процесс → собрать сценарий → добавить AI Agent → подключить MCP (Server или external tools) → ограничить права → протестировать reasoning/logs → запустить с human-in-the-loop.

**Пробел для Excalibur:** русский гайд «безопасный гибридный workflow»: deterministic модули держат поток, AI Agent — только неоднозначные решения, MCP расширяет tools, человек подтверждает критичные действия. Связка с B02 (n8n) и B03 (MCP в Cursor).

---

## 2. Яндекс Wordstat (MCP `mcp-kv`, регион 225, 16.06.2026)

Сервер `user-mcp-kv` в среде недоступен; вызов выполнен через `mcp-kv.wordstat_get_top_requests`. Авторизация успешна.

### Таблица спроса

| Фраза | Показы/мес |
|-------|------------|
| автоматизация make | 223 |
| make сценарии | 94 |
| make ai agent | 44 |
| автоматизация make com | 38 |
| make ии агенты | 29 |
| автоматизация процессов make | 26 |
| сервис автоматизации make | 25 |
| сценарий make com | 25 |
| услуги по автоматизации на make | 8 |
| make com как пользоваться | 8 |

### LSI для writer

- автоматизация make, автоматизация make com, автоматизация процессов make, сервис автоматизации make
- make сценарии, сценарий make com, make com как пользоваться
- make ai agent, make ии агенты; смежные (из related, без цифр): что такое ии агент, как создать ии агента, ии агенты что это, ai automation
- MCP server, MCP client, Make MCP token, scopes, scenario as tool, external MCP tools
- Reasoning Panel, tools, instructions, canvas, in-canvas chat, Library of Agents
- human-in-the-loop, manual approval, router, webhook, credits, execution history

**SEO-стратегия:** primary «автоматизация make» (223) в title/H1/lead. Secondary: «make сценарии» (94), «make ai agent» (44), «автоматизация make com» (38), «автоматизация процессов make» (26) — в H2/H3 и FAQ. Низкочастотный, но коммерчески полезный хвост: «услуги по автоматизации на make» (8).

**Предупреждение:** блок «Похожие запросы» в Wordstat шумный («ты моя», «сценка», «автоматически»). Использовать только релевантные строки из топа выше.

---

## 3. Таблица фактов (цифры и утверждения только с URL)

| Факт | Источник | Дата | Можно в текст |
|------|----------|------|---------------|
| Make AI Agents доступны на всех планах; строятся в visual builder без кода | [make.com/en/ai-agents](https://www.make.com/en/ai-agents) | 16.06.2026 | да |
| Make AI Agents работают с 3000+ интеграциями в одной visual platform | [make.com/en/ai-agents](https://www.make.com/en/ai-agents) | 16.06.2026 | да |
| Отличие от ChatGPT: агенты reason, choose next step и trigger real workflows | [make.com/en/ai-agents](https://www.make.com/en/ai-agents) | 16.06.2026 | да |
| Каждое решение агента видно step by step в Reasoning panel на canvas | [make.com/en/ai-agents](https://www.make.com/en/ai-agents) | 16.06.2026 | да |
| Можно set rules, manual approvals или stop Agent at specific points | [make.com/en/ai-agents](https://www.make.com/en/ai-agents) | 16.06.2026 | да |
| Агенты built, run, debugged в том же canvas, что и scenarios | [make.com/en/blog/make-ai-agents-trust-through-transparency](https://www.make.com/en/blog/make-ai-agents-trust-through-transparency) | 16.06.2026 | да |
| Hybrid: standard modules для fixed rules, agents для unstructured input | [make.com/en/blog/make-ai-agents-trust-through-transparency](https://www.make.com/en/blog/make-ai-agents-trust-through-transparency) | 16.06.2026 | да |
| Пять паттернов: conversational, synthesizer, routing, qualifier, orchestrator | [make.com/en/blog/make-ai-agents-trust-through-transparency](https://www.make.com/en/blog/make-ai-agents-trust-through-transparency) | 16.06.2026 | да |
| Make AI Agents can connect to external MCP servers; mix MCP + native modules в одном run | [community.make.com/.../110260](https://community.make.com/t/feature-spotlight-add-mcp-tools-to-make-ai-agents/110260) | 06.2026 | да |
| Make MCP Server: LLM run scenarios и manage Make account через MCP | [developers.make.com/mcp-server](https://developers.make.com/mcp-server) | 16.06.2026 | да |
| Active/on-demand scenarios становятся callable tools для AI | [developers.make.com/mcp-server](https://developers.make.com/mcp-server) | 16.06.2026 | да |
| Callable tools зависят от выбранных scopes токена | [developers.make.com/mcp-server](https://developers.make.com/mcp-server) | 16.06.2026 | да |
| Scenario run tools — все планы; management tools (view/modify) — paid plans | [developers.make.com/mcp-server](https://developers.make.com/mcp-server) | 16.06.2026 | да |
| Cloud MCP: Streamable HTTP и SSE; Stateless Streamable HTTP — default/recommended | [developers.make.com/mcp-server](https://developers.make.com/mcp-server) | 16.06.2026 | да |
| Scenario run timeout: OAuth `mcp.make.com` — 25 с; MCP token URL — 40 с | [developers.make.com/mcp-server](https://developers.make.com/mcp-server) | 16.06.2026 | да |
| После timeout сценарий может работать до 40 мин; output по executionId при нужных scopes | [developers.make.com/mcp-server](https://developers.make.com/mcp-server) | 16.06.2026 | да |
| Make MCP Server — cloud gateway без local Node/Python; token из профиля Make | [make.com/en/blog/model-context-protocol-mcp-server](https://www.make.com/en/blog/model-context-protocol-mcp-server) | 16.06.2026 | да |
| Free plan: $0, до 1 000 credits/мес; Core от $9/мес за 10k credits | [make.com/en/pricing](https://www.make.com/en/pricing) | 16.06.2026 | да |
| Большинство module actions = 1 credit; AI Provider/advanced могут списывать больше | [make.com/en/pricing](https://www.make.com/en/pricing) | 16.06.2026 | да (с оговоркой про beta) |
| Help Center Make AI Agents: раздел обновлён 03.02.2026 | [help.make.com/make-ai-agents](https://help.make.com/make-ai-agents) | 03.02.2026 | да |
| Best practices (New) обновлены 28.05.2026 | [help.make.com/make-ai-agents-new-best-practices](https://help.make.com/make-ai-agents-new-best-practices) | 28.05.2026 | да |
| MCP — открытый протокол host/client/server; tools требуют consent и access controls | [modelcontextprotocol.io/specification/2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) | 16.06.2026 | да |
| <2.5% сложных неструктурированных задач завершаются автономно без человека (fact-bank) | [mayai.ru/kontent-zavod-avtomatizacziya-cherez-ii-razbiraem-otzyvy](https://mayai.ru/kontent-zavod-avtomatizacziya-cherez-ii-razbiraem-otzyvy/) | 11.06.2026 | да |
| Make: 2500+ интеграций; compute/credit billing удорожает media/AI workflows (fact-bank) | [mayai.ru/n8n-ili-make-com-chto-vybrat...](https://mayai.ru/n8n-ili-make-com-chto-vybrat-dlya-kontent-zavoda-i-frilansa-v-2026-godu/) | 11.06.2026 | да (осторожно; в первичниках Make — 3000+ apps) |
| Прототип на Make на ~40% быстрее за счёт visual debugger (fact-bank) | [mayai.ru/n8n-ili-make-com-chto-vybrat...](https://mayai.ru/n8n-ili-make-com-chto-vybrat-dlya-kontent-zavoda-i-frilansa-v-2026-godu/) | 11.06.2026 | да |

---

## 4. Угол статьи (utility-only, режим B)

**Главный угол:** за один вечер собрать безопасный Make workflow: обычный сценарий (триггер, router, фильтры, approval) + Make AI Agent только на неоднозначных шагах + MCP (Server для Cursor/Claude или external MCP tools в агенте) с минимальными scopes.

**reader_outcome:** читатель выберет один бизнес-процесс, соберёт гибридный Make-сценарий с AI Agent, подключит нужные tools/MCP, добавит human-in-the-loop, проверит Reasoning Panel и запустит на тестовых данных без слепой автономности.

**Отличие от конкурентов:**

- Официальные страницы Make — продукт, не русская пошаговая сборка для бизнеса.
- RU-гайды часто = «как пользоваться Make» или «ИИ-агенты вообще», без governance (scopes, tokens, approvals, credits).
- B06 связывает B02 (когда n8n) и B03 (MCP в Cursor) в операционный Make-canvas.

**Tone:** практик для предпринимателя/маркетолога: «агент — умный модуль внутри проверяемого сценария, не директор».

---

## 5. action_outline (5–9 шагов для writer)

1. **Выбрать процесс:** один повторяемый кейс (лид, тикет, документ, контент-brief). Исключить из пилота деньги, ПДн и необратимые действия.
2. **Разделить deterministic и agentic:** fixed rules — modules/router/filters; агенту — классификация, summary, выбор следующего шага.
3. **Собрать базовый сценарий:** trigger → normalization → router → logging → тестовый data bundle. Без агента убедиться, что вход чистый.
4. **Добавить Make AI Agent на canvas:** Instructions (роль, guardrails, output format), Knowledge, Model; критерий `needs_human_review`.
5. **Подключить tools:** сначала native modules / Call a scenario; затем external MCP servers в agent builder (если нативного модуля нет).
6. **Настроить Make MCP Server** (если Cursor/Claude/ChatGPT должен вызывать Make): on-demand scenario, inputs/outputs, MCP token, минимальные scopes, только нужные сценарии.
7. **Встроить human-in-the-loop:** approval перед письмами, CRM, публикациями, платежами.
8. **Протестировать:** 10–20 кейсов, Reasoning Panel, execution history, timeout/fallback, credits per run.
9. **Запустить с лимитами:** alerts на 75/90% credits, владелец процесса, метрики (время ответа, auto-resolved %, ошибки).

**Workflow-схема:** Trigger → Normalize → Router (simple) → AI Agent (judgment) → Tool/MCP → Human approval → Action → Log + metric

---

## 6. Рекомендуемая структура H2

1. Где в Make нужен AI Agent, а где хватит обычного сценария  
2. Архитектура workflow: trigger → modules → AI Agent → MCP → approval → action  
3. Пошаговая сборка Make-сценария с AI Agent  
4. Make MCP Server: сценарии как tools для Cursor/Claude/ChatGPT  
5. External MCP tools внутри Make AI Agent  
6. Безопасность и бюджет: scopes, токены, Reasoning Panel, credits, HITL  
7. Чек-лист запуска и troubleshooting  

---

## 7. FAQ hints

- Как пользоваться Make.com для автоматизации бизнеса?
- Чем Make AI Agents отличаются от обычных сценариев Make?
- Как подключить MCP к Make (Server vs external tools в агенте)?
- Можно ли подключить Make MCP к Cursor?
- Какие scopes выдавать MCP token?
- Почему сценарий через MCP уходит в timeout?
- Когда выбрать n8n вместо Make?
- Сколько credits съедает AI Agent и как не перерасходовать?

---

## 8. Internal links

- B02: `/avtomatizaciya-n8n-ai-agents/` — блок «когда Make, когда n8n».
- B03: `/podklyuchenie-mcp-cursor/` — Make MCP Server в Cursor/Claude.

**CTA:** не более 2 CTA на курс Make; после practical checklist.

---

## 9. Предупреждения для writer

- Не обещать полную автономность: fact-bank + Make HITL → checkpoints обязательны.
- MCP без отдельной платы ≠ бесплатные запуски: сценарии тратят credits.
- Management MCP tools только на paid plans; scenario run — на всех.
- Не путать Make MCP Server (AI вызывает Make) и external MCP tools в агенте (Make вызывает внешние tools).
- Не копировать mayai.ru/make-ai-agents-gayd-biznes 1:1; факты — из Make primary sources.
- Не показывать реальные токены; URL-шаблоны с `<MAKE_ZONE>`, `<MCP_TOKEN>`.
- В тексте статьи: среднее тире «–», прямые кавычки «"», без эмодзи (site-brief).

---

## 10. Utility gate (research)

**utility_verdict:** PASS

**reader_outcome:** Читатель сможет собрать первый безопасный Make workflow с AI Agent и MCP: от выбора процесса и базового сценария до scopes, approval, тестового запуска, Reasoning Panel и метрик результата.

| Критерий | Статус |
|----------|--------|
| Utility gate темы | PASS |
| SERP WebSearch | PASS |
| Wordstat MCP | PASS |
| Таблица фактов с URL | PASS |
| action_outline 5–9 шагов | PASS |
| FAQ + internal links | PASS |

**Writer:** готов. Вход: этот файл + `research-context.json` + карточка B06 в `memory/topics/blog-topics.md` + `memory/brief/fact-bank.md`.
