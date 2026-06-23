# Research notes — B01 «Как писать SEO-статьи, которые читают люди»

**topic_id:** B01  
**slug:** primer-seo-stati  
**article_mode:** B (longread + демонстрация формата на самой статье)  
**research_date:** 2026-06-10  
**disclaimer:** Все даты, версии и статистика проверены на 10.06.2026.

---

## 1. SERP-обзор (минимум 3 конкурента)

| # | URL | Тип | Сильные стороны | Слабые / пробелы | Что не копировать |
|---|-----|-----|-----------------|------------------|-------------------|
| 1 | [direct.yandex.ru/base/articles/seo-tekst-chto-eto-i-kak-pravilno-pisat](https://direct.yandex.ru/base/articles/seo-tekst-chto-eto-i-kak-pravilno-pisat) | Официальный гайд Яндекса (янв. 2026) | Авторитет источника; пошаговый workflow (тема → семантика → структура → текст → оптимизация); примеры «плохо/хорошо»; акцент на естественность ключей и читабельность; Wordstat, alt, мета, перелинковка | Нет GEO/нейропоиска; продвижение Директа в конце; объём без универсального норматива, но без GEO-hooks | Блок про Директ и коммерческий CTA; дублировать каноническую структуру H1–H4 без GEO-слоя |
| 2 | [pikapuka.com/blog/kak-napisat-seo-tekst-samomu-polnyy-gayd-ot-semantiki-do-e-e-a-t](https://pikapuka.com/blog/kak-napisat-seo-tekst-samomu-polnyy-gayd-ot-semantiki-do-e-e-a-t) | Агентский longread (май 2026) | Глубокая семантика (интент, LSI, Wordstat, Serpstat); E-E-A-T с кейсами; чек-лист 10 шагов; Schema Article + FAQPage; Title ~65 знаков; Featured Snippet / AI-ответы | Кейс «+140% трафика за 3 недели» без верифицируемого источника; перегруз agency-экспертизой; GEO как побочный эффект E-E-A-T, не отдельный блок | Непроверенные проценты в кейсах; копировать 7-разделную структуру 1:1 |
| 3 | [maryproject.ru/blog/kak-pravilno-pisat-stati-pod-seo/](https://maryproject.ru/blog/kak-pravilno-pisat-stati-pod-seo/) | SEO-агентство (апр./июн. 2026) | Короткий, понятный принцип «полный ответ на одной странице»; LSI и «хвосты»; поведенческий сигнал (не возвращаться в поиск) | Мало практики: нет чек-листа, FAQ, schema, GEO; короткий объём (~1,5k знаков) | Формулировки «просто следуй принципам» без actionable шагов |
| 4 | [audit4seo.ru/blog/geo-optimizaciya-2026](https://audit4seo.ru/blog/geo-optimizaciya-2026) | GEO-гайд (2026) | Атомарные чанки, front-loading, conversational queries, llms.txt, Schema; сравнение SEO vs GEO; ссылка на Aggarwal et al. | Фокус на GEO, не на написании SEO-статьи; часть цифр без первичного источника | Таблицу SEO vs GEO можно адаптировать, не копировать блоки про AI-трекеры |
| 5 | [digitalimpuls.ru/blog/geo-optimization-2026/](https://digitalimpuls.ru/blog/geo-optimization-2026/) | GEO-агентство (2026) | Share of Voice, Citation Share; AI-краулеры (GPTBot, ClaudeBot и др.); llms.txt (сент. 2024, Jeremy Howard); интеграция SEO+GEO | Коммерческий кейс ASHA; цены GEO; длинный sales-narrative | Прайсы и демо-страницы агентства; непроверенные «1,5–2×» без источника |

**Паттерн SERP:** топ — «полный гайд 2026» с E-E-A-T, Wordstat, чек-листом. Отдельный кластер — GEO-лонгриды. Прямого совпадения с H1 «которые читают люди» в топе почти нет (bestseoserg.com — близкий заголовок, но слабее по глубине).

**Intent:** how_to — пользователь хочет пошаговую систему: собрать семантику → структура → текст → техника → проверка. Вторичный intent: понять связку SEO + GEO в одном материале.

---

## 2. Таблица фактов (цифры только с URL)

| Факт | Источник | Дата источника | Можно в текст |
|------|----------|----------------|---------------|
| Универсального объёма SEO-статьи не существует — он зависит от сложности темы и конкуренции в выдаче | [Яндекс Директ — SEO-текст](https://direct.yandex.ru/base/articles/seo-tekst-chto-eto-i-kak-pravilno-pisat) | 27.01.2026 | да |
| Абзацы SEO-текста — ориентир 3–5 строк; списки для перечислений | [Яндекс Директ — SEO-текст](https://direct.yandex.ru/base/articles/seo-tekst-chto-eto-i-kak-pravilno-pisat) | 27.01.2026 | да |
| H1 — один на страницу; H2–H4 для смысловых блоков | [Яндекс Директ — SEO-текст](https://direct.yandex.ru/base/articles/seo-tekst-chto-eto-i-kak-pravilno-pisat) | 27.01.2026 | да |
| Поисковики оценивают смысл и полезность, не плотность ключей; переспам вреден | [Яндекс Директ — SEO-текст](https://direct.yandex.ru/base/articles/seo-tekst-chto-eto-i-kak-pravilno-pisat) | 27.01.2026 | да |
| Семантику собирают в Яндекс Вордстат и Яндекс Вебмастер | [Яндекс Директ — SEO-текст](https://direct.yandex.ru/base/articles/seo-tekst-chto-eto-i-kak-pravilno-pisat) | 27.01.2026 | да |
| Title и Description влияют на сниппет и кликабельность | [Яндекс Директ — SEO-текст](https://direct.yandex.ru/base/articles/seo-tekst-chto-eto-i-kak-pravilno-pisat) | 27.01.2026 | да |
| H1 должен отличаться от Title | [Pikapuka — гайд SEO-статьи](https://pikapuka.com/blog/kak-napisat-seo-tekst-samomu-polnyy-gayd-ot-semantiki-do-e-e-a-t) | 09.05.2026 | да |
| Title — ориентир ~65 знаков, с ключом и триггером (чек-лист, инструкция) | [Pikapuka — гайд SEO-статьи](https://pikapuka.com/blog/kak-napisat-seo-tekst-samomu-polnyy-gayd-ot-semantiki-do-e-e-a-t) | 09.05.2026 | да |
| Schema.org: Article + FAQPage для сниппета и структуры | [Pikapuka — гайд SEO-статьи](https://pikapuka.com/blog/kak-napisat-seo-tekst-samomu-polnyy-gayd-ot-semantiki-do-e-e-a-t) | 09.05.2026 | да |
| GEO (Generative Engine Optimization) — оптимизация для цитирования в ответах AI, не замена SEO | [audit4seo — GEO 2026](https://audit4seo.ru/blog/geo-optimizaciya-2026) | 2026 | да |
| Нейросети извлекают пассажи (passages), не страницы целиком — каждый H2-блок = «остров смысла» | [audit4seo — GEO 2026](https://audit4seo.ru/blog/geo-optimizaciya-2026) | 2026 | да |
| Первые 100–150 слов страницы — ключевая зона для извлечения ответа AI | [audit4seo — GEO 2026](https://audit4seo.ru/blog/geo-optimizaciya-2026) | 2026 | да |
| Стандарт llms.txt предложен в сентябре 2024 (Jeremy Howard / Answer.AI) | [Digital Impuls — GEO 2026](https://digitalimpuls.ru/blog/geo-optimization-2026/) | 2026 | да |
| Алиса AI встроена в основную выдачу Яндекса с осени 2024 | [Digital Impuls — GEO 2026](https://digitalimpuls.ru/blog/geo-optimization-2026/) | 2026 | да |
| 39% россиян хотя бы раз пробовали нейросети (ВЦИОМ, август 2024) | [Digital Impuls — GEO 2026](https://digitalimpuls.ru/blog/geo-optimization-2026/) | 2026 | да* |
| ~20% месячной интернет-аудитории РФ — пользователи ChatGPT (Mediascope, август 2024) | [Digital Impuls — GEO 2026](https://digitalimpuls.ru/blog/geo-optimization-2026/) | 2026 | да* |
| Главная задача статьи — полный ответ на запрос; если пользователь возвращается в поиск — сигнал низкого качества | [MaryProject — SEO-статьи](https://maryproject.ru/blog/kak-pravilno-pisat-stati-pod-seo/) | 10.06.2026 | да |

\* Вторичный источник (агентский блог со ссылкой на ВЦИОМ/Mediascope). В тексте — «по данным исследований 2024 года» без точной цифры, если QA не найдёт первичник.

**Не использовать в тексте (нет в fact-bank / непроверено):** «+140% трафика за 3 недели» (Pikapuka); «AI обрабатывает 25% запросов» (audit4seo без первичника); «микроразметка повышает цитирование в 1,5–2 раза» (Digital Impuls без первичника); «Aggarwal +40% видимости» — можно упомянуть как исследование, без точного % без arxiv.

---

## 3. Угол статьи (дифференциация)

**Главный угол:** SEO-статья 2026 = **читаемый longread**, который закрывает запрос человека **и** упакован для нейропоиска. Не «ещё один чек-лист ключей», а **единый workflow**: интент → структура → инфостиль → FAQ/schema → GEO-чанки → финальный чеклист.

**Почему это отличается от конкурентов:**
- Яндекс даёт канон SEO без GEO; GEO-гайды не учат писать текст с нуля.
- Агентские гайды перегружены E-E-A-T-кейсами и CTA.
- H1 из карточки B01 («которые читают люди») — слабо раскрыт в SERP; наш фокус: **читабельность как SEO-фактор** (структура, инфостиль, «острова смысла») + техника.

**Режим B — как применить:** сама статья B01 — **эталон**: 8,5–9,5k знаков, 5–7 FAQ, BlogPosting + FAQPage, атомарные H2, lead-абзац с определением, внутренняя перелинковка на `/`.

**Tone (site-brief):** практично, по-человечески, редакция бренда; без корпоративной воды и эмодзи.

**H2-каркас (из карточки + research):**
1. Зачем SEO и GEO в одной статье (не два проекта, один контент)
2. Структура longread: H1–H3, lead, списки, таблицы
3. FAQ и schema — зачем и как (JSON-LD, не в body)
4. Чеклист перед публикацией (15–20 пунктов, printable logic)

Дополнительные подтемы для глубины (внутри блоков, не отдельные H2 верхнего уровня): семантика/Wordstat, Title/Description, E-E-A-T lite, llms.txt, AI-краулеры в robots.txt.

---

## 4. GEO hooks (для writer и schema)

| Hook | Где в статье | Формат |
|------|--------------|--------|
| Определение SEO-статьи в 40–60 слов | Первый абзац после H1 | «SEO-статья — …» |
| Определение GEO в 40–60 слов | Блок «SEO + GEO» | «GEO (Generative Engine Optimization) — …» |
| Conversational H2 | «Что такое GEO в SEO?», «Сколько символов нужно в SEO-статье?» | Вопрос в заголовке |
| FAQ 5–7 пар | Конец longread | Короткий ответ 2–4 предложения |
| Атомарные чанки | Каждый H2 | Первое предложение = тезис; 3–4 предложения в абзаце |
| Island test | QA для writer | Блок понятен без соседних |
| Schema handoff | Не в HTML body | BlogPosting + FAQPage |
| Даты | Метаданные | datePublished / dateModified = 2026-06-10 |
| llms.txt | Упоминание в GEO-блоке | Что это и зачем для блога |
| E-E-A-T lite | Автор/редакция | Имя, роль, без выдуманных регалий |
| Внутренняя ссылка | Из карточки | На `/` (главная) |
| Alt обложки | Cover | «Редактор за ноутбуком…» (cover_scene_hint) |

**Целевые AI-формулировки для вкрапления:** «как писать seo статьи», «seo текст для блога», «geo оптимизация статьи», «сколько символов в seo статье», «что такое geo в seo».

---

## 5. FAQ-кандидаты (5–7)

1. **Сколько символов должно быть в SEO-статье?** — нет универсальной нормы; ориентир — полнота ответа и конкуренты в SERP; для how-to longread в Excalibur — 8 500–9 500 знаков текста.
2. **Что такое GEO в SEO?** — GEO дополняет SEO: цель — цитирование в AI-ответах, база — индексируемый и структурированный контент.
3. **Нужно ли переспамить ключевые слова в 2026 году?** — нет; естественные вхождения + LSI/тематические слова.
4. **Чем Title отличается от H1?** — Title для сниппета (~65 знаков), H1 — заголовок на странице; не дублировать.
5. **Какие schema нужны для SEO-статьи блога?** — BlogPosting (или Article) + FAQPage для блока вопросов.
6. **Что такое llms.txt и нужен ли он блогу?** — файл для AI-краулеров; полезный сигнал, не замена sitemap.
7. **Как проверить статью перед публикацией?** — чеклист: семантика, мета, структура, FAQ, schema, ссылки, читабельность.

---

## 6. Риски и blockers для writer

- Не выдумывать статистику; использовать только таблицу фактов выше.
- Не копировать структуру Pikapuka (7 разделов) 1:1.
- Объём текста: 8 500–9 500 знаков (quality-blog.md).
- Без эмодзи, без VPN/обход блокировок.
- site_url example.com — в ссылках использовать плейсхолдер или `/` по карточке.

---

## 7. Готовность к writer

| Критерий | Статус |
|----------|--------|
| SERP ≥ 3 конкурента | ✅ |
| Таблица фактов с URL | ✅ |
| Угол + дифференциация | ✅ |
| GEO hooks | ✅ |
| FAQ-кандидаты 5–7 | ✅ |
| Режим B описан | ✅ |
| H2 outline | ✅ |

**Writer:** готов. Вход: этот файл + `research-context.json` + карточка B01 в `blog-topics.md` + `site-brief.md`.

---

=== EXCALIBUR BLOG RESEARCH ===
topic_id: B01
article_dir: memory/blog/articles/B01-primer-seo-stati
status: ✅
summary: SERP — 5 конкурентов (Яндекс Direct, Pikapuka, MaryProject, audit4seo, Digital Impuls). Угол — единый workflow SEO+GEO longread «для людей»: читабельность, атомарные чанки, FAQ/schema, чеклист. Режим B, 17 фактов с URL, 7 FAQ-кандидатов. Готов к writer.
===
