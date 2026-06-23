# Research notes — B03 «Как подключить MCP-серверы в Cursor: пошаговая инструкция для автоматизации»

**topic_id:** B03  
**slug:** podklyuchenie-mcp-cursor  
**article_mode:** B (how-to)  
**research_date:** 2026-06-11  
**disclaimer:** Все даты, версии и статистика проверены на 11.06.2026.

---

## 1. SERP-обзор (WebSearch + research-serp.json, 8 конкурентов)

| # | URL | Тип | Сильные стороны | Слабые / пробелы | Что не копировать |
|---|-----|-----|-----------------|------------------|-------------------|
| 1 | [cursor.com/docs/mcp](https://cursor.com/docs/mcp) | Официальная docs (EN) | Канон: mcp.json, stdio/HTTP, OAuth, переменные `${env:}`, Marketplace | Английский; мало troubleshooting на русском | Сухой перевод без «на пальцах» для не-программистов |
| 2 | [cursor.com/ru/help/customization/mcp](https://cursor.com/ru/help/customization/mcp) | Официальная help (RU) | One-click install, пути конфигов, Auto-review 3.6+, MCP Logs | Короткая; нет готового стека для автоматизации контента | Копировать 1:1 без расширения кейсов |
| 3 | [truefoundry.com/blog/mcp-servers-in-cursor-setup-configuration-and-security-guide](https://www.truefoundry.com/blog/mcp-servers-in-cursor-setup-configuration-and-security-guide) | Longread EN (2026) | stdio vs HTTP, Docker-пример GitHub, security/CVE | Устаревший акцент на «лимит 40 tools» (см. dynamic context 2026) | Цифру «40 tools» как жёсткий лимит без оговорки про 2026 |
| 4 | [nxcode.io/resources/news/cursor-mcp-servers-complete-guide-2026](https://www.nxcode.io/resources/news/cursor-mcp-servers-complete-guide-2026) | Гайд 2026 (RU/EN) | Три метода setup, project vs global, troubleshooting JSON | Много «что такое MCP», мало Make/автоматизации бизнеса | Структуру 1:1; news-формат |
| 5 | [fast.io/resources/cursor-mcp-server-setup](https://fast.io/resources/cursor-mcp-server-setup/) | Step-by-step EN (2026) | UI + mcp.json, пути Windows `%USERPROFILE%\.cursor\mcp.json` | Продаёт свой MCP-сервер | Коммерческий bias |
| 6 | [shtruzel.ru/articles/mcp-v-cursor-podklyuchenie-i-luchshie-servery-2026](https://shtruzel.ru/articles/mcp-v-cursor-podklyuchenie-i-luchshie-servery-2026) | RU how-to + топ серверов | Marketplace, топ-10, типичные ошибки | Узкий уклон в 1С/BSL | Нишевый 1С-фокус как основной угол |
| 7 | [mayai.ru/mcp-server-sozdat-gayd-cursor-claude](https://mayai.ru/mcp-server-sozdat-gayd-cursor-claude/) | RU гайд (свой сайт) | Создание MCP с нуля, цепочка протокол → код | Другой intent: build, не connect готовых серверов | Каннибализацию: в B03 — подключение; ссылка на mayai как «следующий шаг» |
| 8 | [khar-ag.ru/docs/cursor-mcp-guide](https://khar-ag.ru/docs/cursor-mcp-guide/) | RU технический гайд | mcp.json, протокол, серверы | Для разработчиков; без аудитории «маркетолог без кода» | Перегруз терминами без расшифровки |

**Паттерн SERP:** топ — официальная docs Cursor + англоязычные setup-гайды 2026 + русские обзоры «лучшие MCP» и нишевые (1С, Figma). Запрос «как подключить mcp к cursor» (12 показов/мес) почти не закрыт отдельным русским how-to в топе — пробел для «Ковчег».

**Intent:** how_to — пользователь хочет **подключить** готовый MCP-сервер (stdio или URL), увидеть зелёный статус в Cursor и вызвать tool из Agent. Вторичный intent: какие серверы взять для автоматизации (браузер, CMS, docs), безопасность (allowlist), починка красного статуса.

**Пробел для «Ковчег»:** пошаговый гайд на русском для **не-программистов** (маркетолог, SMM, предприниматель): от первого mcp.json до рабочего стека под контент-завод и Make-воронки; язык «на пальцах»; связка с B02 (n8n agents) и внутренней статьёй mayai про **создание** MCP.

---

## 2. Яндекс Wordstat (MCP user-mcp-kv, 11.06.2026)

### Таблица спроса

| Фраза | Показы/мес |
|-------|------------|
| cursor mcp | 630 |
| cursor ai mcp | 61 |
| figma cursor mcp | 48 |
| mcp сервер для cursor | 32 |
| настройка mcp сервера | 74 |
| cursor mcp 1с | 21 |
| playwright mcp cursor | 18 |
| unity mcp cursor | 16 |
| cursor directory mcp | 16 |
| как подключить mcp к cursor | 12 |
| mcp servers for cursor | 11 |
| лучшие mcp для cursor | 9 |
| context 7 mcp cursor | 9 |
| cursor github mcp | 4 |

### LSI для writer (из топа Wordstat + SERP)

- cursor mcp настройка, mcp.json, stdio, Tools & MCP  
- mcp сервер для cursor скачать / marketplace / cursor.directory  
- playwright mcp cursor, figma cursor mcp, context7 mcp  
- как подключить mcp к cursor, почему не подключается  
- allowlist, auto-run, MCP Logs, permissions.json  
- автоматизация контента, wordpress mcp, browser mcp  

**SEO-стратегия:** primary «cursor mcp» (630) в H1/lead; secondary «mcp сервер для cursor» (32), «как подключить mcp к cursor» (12), «настройка mcp сервера» (74) — в H2/H3 и FAQ. Long-tail: figma/playwright/context7 — в блок «топ серверов», не в title.

---

## 3. Таблица фактов (цифры только с URL)

| Факт | Источник | Дата | Можно в текст |
|------|----------|------|---------------|
| MCP (Model Context Protocol) — открытый стандарт Anthropic для подключения AI к внешним данным и инструментам | [anthropic.com/news/model-context-protocol](https://www.anthropic.com/news/model-context-protocol) | 25.11.2024 | да |
| Анонс MCP: 25 ноября 2024; open-source спецификация + SDK + репозиторий серверов | [anthropic.com/news/model-context-protocol](https://www.anthropic.com/news/model-context-protocol) | 25.11.2024 | да |
| Cursor: MCP подключает Agent к GitHub, Linear, Notion, БД, API | [cursor.com/ru/help/customization/mcp](https://cursor.com/ru/help/customization/mcp) | 11.06.2026 | да |
| Глобальный конфиг: `~/.cursor/mcp.json`; проектный: `.cursor/mcp.json` в корне проекта | [cursor.com/ru/help/customization/mcp](https://cursor.com/ru/help/customization/mcp) | 11.06.2026 | да |
| Оба файла **объединяются**; при совпадении имени сервера побеждает конфиг **уровня проекта** | [cursor.com/ru/help/customization/mcp](https://cursor.com/ru/help/customization/mcp) | 11.06.2026 | да |
| Локальный stdio-сервер: поля `command`, `args`, `env` внутри `mcpServers` | [cursor.com/ru/help/customization/mcp](https://cursor.com/ru/help/customization/mcp) | 11.06.2026 | да |
| Удалённый сервер: поле `url`; опционально `headers` для Bearer-токена | [cursor.com/ru/help/customization/mcp](https://cursor.com/ru/help/customization/mcp) | 11.06.2026 | да |
| One-click: Settings → Tools & MCP → «Add to Cursor» (или Marketplace) | [cursor.com/ru/help/customization/mcp](https://cursor.com/ru/help/customization/mcp) | 11.06.2026 | да |
| Hotkey настроек Cursor: Mac `Cmd+Shift+J`, Windows/Linux `Ctrl+Shift+J` | [cursor.com/ru/help/customization/mcp](https://cursor.com/ru/help/customization/mcp) | 11.06.2026 | да |
| После правки mcp.json нужен **перезапуск Cursor** | [cursor.com/ru/help/customization/mcp](https://cursor.com/ru/help/customization/mcp) | 11.06.2026 | да |
| Agent видит MCP-tools автоматически; вкл/выкл — в списке tools в чате | [cursor.com/ru/help/customization/mcp](https://cursor.com/ru/help/customization/mcp) | 11.06.2026 | да |
| По умолчанию Agent **запрашивает подтверждение** перед вызовом MCP-tool | [cursor.com/ru/help/customization/mcp](https://cursor.com/ru/help/customization/mcp) | 11.06.2026 | да |
| Cursor 3.6+: режим Auto-review в Settings > Agents > Run Mode; allowlist через `permissions.json` | [cursor.com/ru/help/customization/mcp](https://cursor.com/ru/help/customization/mcp) | 11.06.2026 | да |
| Troubleshooting: панель Output → **MCP Logs** (`Cmd+Shift+U` / `Ctrl+Shift+U`) | [cursor.com/ru/help/customization/mcp](https://cursor.com/ru/help/customization/mcp) | 11.06.2026 | да |
| Каталог серверов: Cursor Marketplace + [cursor.directory](https://cursor.directory) | [cursor.com/ru/help/customization/mcp](https://cursor.com/ru/help/customization/mcp) | 11.06.2026 | да |
| Cursor поддерживает расширение **MCP Apps** (интерактивный UI в чате) | [cursor.com/ru/help/customization/mcp](https://cursor.com/ru/help/customization/mcp) | 11.06.2026 | да |
| Cloud Agents поддерживают MCP из dashboard; Team — shared MCP в Settings > Integrations | [cursor.com/ru/help/customization/mcp](https://cursor.com/ru/help/customization/mcp) | 11.06.2026 | да |
| Windows-путь глобального mcp.json: `%USERPROFILE%\.cursor\mcp.json` | [fast.io/resources/cursor-mcp-server-setup](https://fast.io/resources/cursor-mcp-server-setup/) | 2026 | да |
| Reload Window: Command Palette → «Reload Window» (альтернатива полному рестарту) | [corcava.com/docs/mcp-troubleshooting-cursor-wont-reload](https://corcava.com/es/docs/mcp-troubleshooting-cursor-wont-reload) | 2026 | да |
| Невалидный JSON в mcp.json → Cursor **молча не загружает** конфиг | [corcava.com/docs/mcp-troubleshooting-cursor-wont-reload](https://corcava.com/es/docs/mcp-troubleshooting-cursor-wont-reload) | 2026 | да |
| Dynamic Context Discovery: описания MCP-tools синхронизируются в папку; agent подгружает детали по demand | [cursor.com/blog/dynamic-context-discovery](https://cursor.com/blog/dynamic-context-discovery) | 2026 | да |
| A/B-тест Cursor: при вызове MCP-tool снижение agent tokens на **46,9%** (dynamic context) | [cursor.com/blog/dynamic-context-discovery](https://cursor.com/blog/dynamic-context-discovery) | 2026 | да |
| На форуме Cursor (март 2026): пользователи с **80+ tools** без warning на актуальных версиях | [forum.cursor.com/t/regarding-the-quantity-limit-of-mcp-tools/153432](https://forum.cursor.com/t/regarding-the-quantity-limit-of-mcp-tools/153432) | 03.2026 | да (как community signal, не официальный SLA) |
| FastMCP: Cursor использует `~/.cursor/mcp.json` как стандарт MCP JSON | [gofastmcp.com/integrations/mcp-json-configuration](https://gofastmcp.com/integrations/mcp-json-configuration) | 2026 | да |
| Курс Make.com kv-ai.ru: подписка **5 800 ₽/мес**, 159+ уроков | [site-brief / kv-ai.ru](https://kv-ai.ru/obuchenie-po-make) | 11.06.2026 | да (единственный верифицированный прайс продукта) |

**Не использовать без оговорки:** «жёсткий лимит 40 tools» как актуальное ограничение 2026 — в старых гайдах (TrueFoundry) есть, но Cursor в 2026 продвигает dynamic context; писать: «раньше советовали ≤40, сейчас можно больше, но включайте только нужные tools».

**fact-bank.md:** пуст для MCP/Cursor — все цифры только из таблицы выше.

---

## 4. Угол статьи (utility-only, режим B)

**Главный угол:** за **15–30 минут** подключить **первый MCP-сервер** в Cursor (one-click или mcp.json), проверить в Tools & MCP, вызвать tool из Agent и собрать **минимальный стек из 2–3 серверов** под автоматизацию (браузер/docs/CMS) без написания своего сервера.

**Почему отличается от конкурентов:**
- Официальная docs — канон, но без сценариев «контент-завод / Make-воронка».
- EN-гайды не бьют в русский low-volume intent «как подключить mcp к cursor».
- Обзоры «топ-12 MCP» не дают пошагового первого подключения с troubleshooting.
- «Ковчег»: практик автоматизации, язык для не-программистов, связка MCP + Make + контент (не новость про Cursor 2.x).

**Tone:** MCP = «розетка, к которой Agent подключает внешние инструменты»; stdio = «локальная программа на вашем ПК»; url = «облачный сервер по ссылке». Без снобизма Senior-dev.

**H2-каркас (из карточки + research):**
1. MCP за 60 секунд: зачем маркетологу/автоматизатору, не только разработчику  
2. Где лежит конфиг: global vs project, Windows-путь  
3. Способ A: one-click через Tools & MCP / Marketplace  
4. Способ B: ручной mcp.json (stdio через npx + remote url)  
5. Безопасность: подтверждение tool, allowlist, Auto-review 3.6+  
6. Стартовый набор MCP для автоматизации (browser, Context7/docs, WordPress/Figma по Wordstat)  
7. Troubleshooting: красный статус, JSON, ENOENT, MCP Logs  
8. FAQ + чеклист перед продакшеном  

**Conversion (conversion-map.md):**
- CTA курс Make: max 2× — «MCP в Cursor + сценарии в Make» → [kv-ai.ru/obuchenie-po-make](https://kv-ai.ru/obuchenie-po-make)  
- Telegram @maya_pro — 1× если уместно  
- Internal: [B02 n8n agents](/avtomatizaciya-n8n-ai-agents/), [mayai создать MCP](https://mayai.ru/mcp-server-sozdat-gayd-cursor-claude/) как advanced track  

---

## 5. Стартовый набор MCP (черновик для writer, без выдуманных install-команд)

| Сервер | Зачем автоматизатору | Транспорт | Примечание |
|--------|---------------------|-----------|------------|
| Browser / Playwright MCP | Проверка страниц, скриншоты, QA лендингов | stdio (npx) | Wordstat: playwright mcp cursor (18) |
| Context7 / docs MCP | Актуальная документация библиотек без галлюцинаций | stdio или url | Wordstat: context 7 mcp cursor (9) |
| GitHub MCP | PR, issues, репозиторий контент-завода | stdio + PAT в env | cursor github mcp (4) |
| Figma MCP | Дизайн → код/контент | stdio | figma cursor mcp (48) |
| WordPress MCP (community) | Публикация/правки постов из Agent | stdio/url | Указать: проверять README сервера, не выдумывать endpoint |

**Рекомендация writer:** в статье один **полный** рабочий пример (например filesystem или официальный `@modelcontextprotocol/server-*` из docs), остальные — таблица «что подключить следующим» со ссылкой на cursor.directory.

---

## 6. FAQ-кандидаты (5–7)

1. **Как подключить MCP к Cursor?** — Settings → Tools & MCP (one-click) или `.cursor/mcp.json` / `~/.cursor/mcp.json`, перезапуск.  
2. **Где файл mcp.json на Windows?** — `C:\Users\<user>\.cursor\mcp.json` (глобально) или `.cursor\mcp.json` в проекте.  
3. **Почему MCP сервер красный / не подключается?** — MCP Logs, JSON-синтаксис, нет Node/npx в PATH (ENOENT), неверный API key в `env`.  
4. **Нужно ли каждый раз подтверждать вызов tool?** — по умолчанию да; allowlist / permissions.json / Auto-review (3.6+).  
5. **Сколько MCP-серверов можно включить?** — формально много; в 2026 dynamic context снижает проблему старых лимитов; практически — 3–5 нужных, не весь cursor.directory.  
6. **Чем MCP отличается от Skills в Cursor?** — MCP = внешние tools/данные; Skills = упакованные инструкции/воркфлоу агента (кратко, без ухода в новость).  
7. **MCP vs Make/n8n?** — MCP расширяет **IDE-агента**; Make/n8n — фоновые сценарии 24/7; связка: Agent готовит → Make публикует (1 абзац + ссылка B02).

---

## 7. GEO hooks

| Hook | Где | Формат |
|------|-----|--------|
| Определение MCP 40–60 слов | Lead после H1 | «MCP в Cursor — …» |
| Таблица global vs project config | H2-2 | Путь + когда что выбирать |
| Пример mcp.json (stdio) | H2-4 | Блок кода + пояснение полей |
| Workflow | H2-4–5 | Выбор сервера → mcp.json → restart → test prompt → allowlist |
| FAQ 5–7 | Конец | Ответы-действия |
| Schema | handoff schema | BlogPosting + FAQPage |
| E-E-A-T | Автор | Артур Хорошев, автоматизация Make + Cursor |

**Целевые формулировки:** «cursor mcp», «mcp сервер для cursor», «как подключить mcp к cursor», «настройка mcp сервера cursor».

---

## 8. Риски для writer

- Не выдумывать версии Cursor/npx-пакетов — «актуальная версия на дату статьи», команды брать из README сервера на cursor.directory.  
- Не копировать nxcode/shtruzel 1:1.  
- Объём: 8 500–9 500 знаков (quality-blog).  
- Без эмодзи; дефис вместо длинного тире; прямые кавычки.  
- Min **5** нумерованных шагов + чеклист **10+** пунктов (utility gate статьи).  
- Не подменять how-to списком «топ-20 серверов» без шагов подключения.  
- CVE/security — одним абзацем со ссылкой на docs, не fear-mongering.

---

## 9. Utility gate (research)

**utility_verdict:** PASS

**reader_outcome:** Читатель откроет Tools & MCP или создаст mcp.json, подключит первый MCP-сервер (stdio или URL), увидит активный статус, вызовет tool из Agent с понятными правилами безопасности и при ошибке найдёт причину через MCP Logs; сможет добавить 2–3 сервера под свои задачи автоматизации.

**action_outline (для writer):**

1. **Обновить Cursor** до актуальной версии; открыть Settings (`Ctrl+Shift+J`) → **Tools & MCP** — убедиться, что раздел доступен.  
2. **Выбрать область конфига:** личный `~/.cursor/mcp.json` (все проекты) или командный `.cursor/mcp.json` в репозитории (приоритет при конфликте имён).  
3. **Подключить первый сервер — способ A:** Marketplace / «Add to Cursor» → пройти OAuth или подтвердить install.  
4. **Или способ B — mcp.json:** добавить блок `mcpServers` с `command`/`args`/`env` (stdio) или `url`/`headers` (remote); сохранить **валидный JSON**.  
5. **Перезапустить Cursor** (или Reload Window из Command Palette); в Tools & MCP проверить **зелёный/активный** статус сервера.  
6. **В чате Agent** включить нужные MCP-tools в списке; отправить тестовый prompt, который явно требует tool (например, поиск docs / файлов).  
7. **Настроить безопасность:** оставить подтверждение вызовов или добавить доверенные tools в allowlist / `permissions.json` (упомянуть Auto-review 3.6+).  
8. **При красном статусе:** Output → MCP Logs; проверить JSON, PATH к node/npx, переменные `env`, перезапуск после правки shell profile.  
9. **Добавить 2–3 сервера под стек автоматизации** (browser, docs, CMS/GitHub) по таблице раздела 5; не включать десятки серверов «на всякий случай».

---

## 10. Готовность к writer

| Критерий | Статус |
|----------|--------|
| Utility gate темы | PASS |
| SERP ≥ 3 конкурента | ✅ (8) |
| Wordstat MCP | ✅ |
| Таблица фактов с URL | ✅ (22 факта) |
| utility_verdict + action_outline | ✅ |
| FAQ 5–7 | ✅ |
| GEO hooks | ✅ |

**Writer:** готов. Вход: этот файл + `research-context.json` + карточка B03 + `site-brief.md` + `conversion-map.md`.
