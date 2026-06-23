research_date: 2026-06-16
accessed_at: 2026-06-16
prefer_sources_after: 2026-03-18
utility_verdict: PASS
reader_outcome: читатель сможет за один рабочий подход собрать короткий /llms.txt для своего сайта, выложить его в корень, проверить доступность и понять, когда нужен отдельный llms-full.txt, а когда это лишняя работа.
reader_pain: владелец сайта слышит обещания "llms.txt даст попадание в ответы нейросетей", боится упустить GEO/AEO-тренд и не понимает, что реально положить в файл, чтобы не сделать мусорный SEO-артефакт.
success_criteria: файл открывается по https://domain.ru/llms.txt с Markdown-структурой, содержит только ключевые страницы с короткими описаниями, не конфликтует с robots.txt, в Lighthouse/ручной проверке нет серверной ошибки, а Writer честно объясняет, что Google Search не даёт бонуса за файл.
voice_angle: спокойный практик разбирает хайп без злости: "не волшебная кнопка в ChatGPT, а дешёвая карта сайта для AI-агентов; если делать, то за 30-60 минут и без обещаний клиенту".
reader_story: маркетолог добавил в robots.txt строчку про llms.txt, сгенерировал огромный файл из всех URL блога и ждал цитат в Perplexity. Через месяц в логах ноль обращений, зато файл устарел. В статье нужно показать, как сузить файл до 10-30 важных страниц, добавить описания и проверять результат по фактам, а не по надежде.
surprising_fact: Ahrefs изучил 137,210 доменов за май 2026 и нашёл, что 97% валидных llms.txt не получили ни одного запроса, но Chrome Lighthouse v13.3.0 в мае 2026 добавил Agentic Browsing category в default config и проверяет llms.txt как readiness-сигнал.

## research_questions
1. Что такое llms.txt в первоисточнике и где он должен лежать?
2. Какие секции обязательны, а какие лучше вынести в Optional?
3. Чем llms.txt отличается от robots.txt и sitemap.xml?
4. Нужно ли добавлять llms.txt в robots.txt?
5. Какие обещания про попадание в AI-ответы нельзя давать читателю?
6. Когда достаточно короткого llms.txt, а когда оправдан llms-full.txt?
7. Какие реальные сайты и AI-документации уже публикуют такие файлы?
8. Какими инструментами можно сгенерировать файл для WordPress/статического сайта/Next.js/Astro/Vite/Docusaurus?
9. Как проверить, что файл не сломан: HTTP, MIME, Markdown, Lighthouse, ручной тест агентом?
10. Как поддерживать файл, чтобы он не превратился в устаревший список ссылок?

## source_table
| source | url | accessed_at | why_it_matters |
| --- | --- | --- | --- |
| llmstxt.org specification | https://llmstxt.org/ | accessed_at: 2026-06-16 | Первоисточник формата: файл /llms.txt в корне, Markdown, H1, blockquote, H2 sections, link lists, special Optional section, coexistence with robots.txt and sitemap.xml. |
| Answer.AI original proposal | https://www.answer.ai/posts/2024-09-03-llmstxt | accessed_at: 2026-06-16 | Подтверждает происхождение предложения Jeremy Howard/Answer.AI от 2024-09-03 и базовую идею "LLM-friendly content". |
| Google Search Central AI optimization guide | https://developers.google.com/search/docs/fundamentals/ai-optimization-guide | accessed_at: 2026-06-16 | Официальная позиция Google Search: llms.txt и специальные AI-файлы не нужны для AI Overviews/AI Mode и не помогают ранжированию. |
| Chrome for Developers Lighthouse llms.txt audit | https://developer.chrome.com/docs/lighthouse/agentic-browsing/llms-txt | accessed_at: 2026-06-16 | Официально объясняет: Lighthouse считает отсутствие файла 404 как N/A, а серверную ошибку при запросе /llms.txt флагует; файл optional at the moment. |
| GoogleChrome Lighthouse v13.3.0 release | https://github.com/GoogleChrome/lighthouse/releases/tag/v13.3.0 | accessed_at: 2026-06-16 | Дата и версия: v13.3.0 published 2026-05-07, Agentic Browsing category добавлена в default config, есть llms-txt changes/smoketests. |
| Ahrefs llms.txt study | https://ahrefs.com/blog/llmstxt-study/ | accessed_at: 2026-06-16 | Свежие логи за май 2026: 137,210 доменов, 28% публикуют файл, 97% валидных файлов без запросов, 96% обращений к читаемым файлам от ботов. |
| OpenAI LLMs.txt | https://cdn.openai.com/API/docs/txt/llms.txt | accessed_at: 2026-06-16 | Реальный пример крупного AI-провайдера: OpenAI публикует индекс docs, pricing, API reference и llms-full.txt для разработчиков. |
| Anthropic Developer Documentation llms.txt | https://platform.claude.com/llms.txt | accessed_at: 2026-06-16 | Реальная реализация на документации Anthropic: индекс документации, языковые разделы и ссылки на Markdown-страницы. |
| llms-txt Python module and CLI | https://llmstxt.org/intro.html | accessed_at: 2026-06-16 | Практический инструмент проверки/сборки контекста: pip install llms-txt, llms_txt2ctx llms.txt > llms.md, --optional True. |
| PyPI llms-txt v0.0.6 | https://pypi.org/project/llms-txt/ | accessed_at: 2026-06-16 | Версия инструмента: v0.0.6, release date 2026-01-29, Python >=3.10, статус Alpha. |
| AnswerDotAI GitHub repo | https://github.com/AnswerDotAI/llms-txt | accessed_at: 2026-06-16 | GitHub-площадка спецификации, issues/PRs и community input; важно для статуса "informal proposal", а не формальный стандарт W3C/IETF. |
| henu-wang examples repo | https://github.com/henu-wang/llms-txt-examples | accessed_at: 2026-06-16 | Примеры для SaaS, e-commerce, blog/media, documentation, local business; пригодно Writer для шаблонов. |
| llmoptimizer GitHub repo | https://github.com/ihuzaifashoukat/llmoptimizer | accessed_at: 2026-06-16 | Генератор для сайтов и docs: crawling, sitemaps, static builds, Next.js, Vite, Nuxt, Astro, Remix, Markdown/MDX. |
| Docusaurus plugin GitHub repo | https://github.com/rachfop/docusaurus-plugin-llms | accessed_at: 2026-06-16 | Инструмент для docs-сайтов: генерирует llms.txt, llms-full.txt, section links, cleans HTML/MDX. |

## wordstat
source: wordstat_get_top_requests on MCP server mcp-kv, region 225 Russia, devices DEVICE_ALL, accessed_at: 2026-06-16.

| phrase | impressions |
| --- | ---: |
| llms txt | 859 |
| файл llms txt | 151 |
| llms txt пример | 57 |
| генератор llms txt | 49 |
| llms full txt | 39 |
| создать llms txt | 37 |
| llms txt generator | 22 |
| llms txt тильда | 20 |
| создать файл llms txt | 16 |
| llms txt в robots txt | 15 |
| файл llms txt пример | 15 |

LSI for Writer: файл llms txt, llms txt пример, генератор llms txt, llms full txt, создать файл llms txt, llms txt generator, llms txt в robots txt, llms.txt шаблон, llms-full.txt, robots.txt vs llms.txt, sitemap.xml, Lighthouse Agentic Browsing. Wordstat "похожие запросы" mostly noisy and unrelated, so do not use them as semantic core.

## github_evidence
| repo/issue/doc | url | signal |
| --- | --- | --- |
| AnswerDotAI/llms-txt | https://github.com/AnswerDotAI/llms-txt | Primary public repo for the informal specification and discussion; use it to avoid presenting llms.txt as an official search standard. |
| GoogleChrome/lighthouse v13.3.0 release | https://github.com/GoogleChrome/lighthouse/releases/tag/v13.3.0 | Official release evidence: Agentic Browsing added to default config on 2026-05-07, llms-txt audit changes and smoketests included. |
| henu-wang/llms-txt-examples | https://github.com/henu-wang/llms-txt-examples | Template repo with real-world categories: SaaS, ecommerce, blog/media, docs, local business. |
| ihuzaifashoukat/llmoptimizer | https://github.com/ihuzaifashoukat/llmoptimizer | Practical generator for crawling/sitemaps/static builds and framework adapters: Next.js, Vite, Nuxt, Astro, Remix. |
| rachfop/docusaurus-plugin-llms | https://github.com/rachfop/docusaurus-plugin-llms | Docs-site plugin that generates llms.txt and llms-full.txt and cleans documentation content. |

## current_fact_checks
| fact | url | accessed_at |
| --- | --- | --- |
| The base proposal asks sites to add /llms.txt as a Markdown file with brief context and links to detailed Markdown files. | https://llmstxt.org/ | accessed_at: 2026-06-16 |
| The Optional section has semantic meaning: links in it can be skipped when shorter context is needed. | https://llmstxt.org/ | accessed_at: 2026-06-16 |
| llms.txt is not robots.txt: it gives context and curated links, it does not control crawling or block access. | https://llmstxt.org/ | accessed_at: 2026-06-16 |
| Google Search says LLMS.txt files and other special AI files are not needed to appear in Google Search generative AI features and do not help or harm rankings. | https://developers.google.com/search/docs/fundamentals/ai-optimization-guide | accessed_at: 2026-06-16 |
| Chrome Lighthouse marks missing /llms.txt 404 as N/A because providing the file is optional at the moment, but flags server errors. | https://developer.chrome.com/docs/lighthouse/agentic-browsing/llms-txt | accessed_at: 2026-06-16 |
| Lighthouse v13.3.0 was published 2026-05-07 and added the new Agentic Browsing category to default config. | https://github.com/GoogleChrome/lighthouse/releases/tag/v13.3.0 | accessed_at: 2026-06-16 |
| Ahrefs studied 137,210 domains in May 2026; 28% published llms.txt, and 97% of valid files received zero requests. | https://ahrefs.com/blog/llmstxt-study/ | accessed_at: 2026-06-16 |
| Of llms.txt files that did receive requests in Ahrefs data, 96% of requests came from bots. | https://ahrefs.com/blog/llmstxt-study/ | accessed_at: 2026-06-16 |
| OpenAI publishes LLM-friendly docs files including llms-models-pricing.txt, llms-guides.txt, llms-api-reference.txt and llms-full.txt. | https://cdn.openai.com/API/docs/txt/llms.txt | accessed_at: 2026-06-16 |
| Anthropic publishes a Developer Documentation llms.txt with English and localized documentation links; the fetched file listed English docs and multiple localized sections. | https://platform.claude.com/llms.txt | accessed_at: 2026-06-16 |
| The llms-txt CLI can convert llms.txt to context with llms_txt2ctx llms.txt > llms.md and can include Optional via --optional True. | https://llmstxt.org/intro.html | accessed_at: 2026-06-16 |
| PyPI lists llms-txt v0.0.6 with release date 2026-01-29 and Python >=3.10. | https://pypi.org/project/llms-txt/ | accessed_at: 2026-06-16 |

## serp_takeaways
1. SERP intent is mostly "что это + как создать + пример"; Russian results overpromise "видимость в AI-поиске", while English/docs sources are more cautious.
2. Strong competitor angle: many guides pitch llms.txt as AI SEO hack. Our better utility angle: make a clean, maintainable file and do not sell it as ranking guarantee.
3. The most useful current conflict: Google Search rejects llms.txt as Search/AIO requirement; Chrome Lighthouse checks it for agentic browsing readiness. Writer should explain "Search visibility" and "agent readiness" as two different jobs.
4. For non-technical business sites, a short manually curated file is enough. For developer docs or large knowledge bases, consider llms-full.txt and generator tooling.
5. The article must include a ready checklist and template, not a general history of the standard.

## reader_pain_deep
- Страх упустить тренд: "все пишут GEO/AEO, вдруг без llms.txt нейросети не увидят сайт".
- Практический затык: какие URL выбрать из сотен страниц, что делать с блогом, прайсом, кейсами и политиками.
- Технический страх: куда положить файл на WordPress/Tilda/самописном сайте, нужен ли robots.txt, какой MIME, что проверять.
- Риск для агентства/фрилансера: пообещать клиенту рост цитирований в ChatGPT и потом не иметь доказательств.

## pain_solution_map
| pain | solution | proof/source | reader_result |
| --- | --- | --- | --- |
| Боль: читатель думает, что llms.txt гарантирует попадание в AI Overviews или ChatGPT-ответы. | Решение: в lead сразу развести "Google Search visibility" и "agent readability"; запретить обещание ранжирования. | https://developers.google.com/search/docs/fundamentals/ai-optimization-guide; https://ahrefs.com/blog/llmstxt-study/ | Результат: читатель делает файл как low-cost housekeeping, а не как магическую SEO-кнопку. |
| Боль: непонятно, что писать в файле. | Решение: дать минимальную структуру: H1, blockquote summary, 2-5 H2 sections, Markdown link list, Optional for low-priority pages. | https://llmstxt.org/ | Результат: у читателя есть шаблон, который можно заполнить за 30-60 минут. |
| Боль: читатель смешивает robots.txt, sitemap.xml и llms.txt. | Решение: таблица отличий: robots controls access, sitemap lists indexable pages, llms.txt curates context and links. | https://llmstxt.org/ | Результат: читатель не пытается "разрешать" или "запрещать" AI через llms.txt. |
| Боль: файл добавили, но сервер отдаёт ошибку или HTML-страницу. | Решение: чеклист проверки HTTP 200, content-type text/plain or text/markdown, Markdown content, no soft 404, Lighthouse no server error. | https://developer.chrome.com/docs/lighthouse/agentic-browsing/llms-txt | Результат: файл не ломает agent-readiness audit и читается вручную. |
| Боль: сайт большой, ручной файл быстро устареет. | Решение: для docs/большого блога использовать генератор из sitemap/Markdown/MDX или workflow обновления после публикаций. | https://github.com/ihuzaifashoukat/llmoptimizer; https://github.com/rachfop/docusaurus-plugin-llms | Результат: файл обновляется вместе с сайтом, а не превращается в мёртвый список. |
| Боль: владелец сайта хочет llms-full.txt, но не понимает зачем. | Решение: объяснить правило: llms.txt - навигационная карта, llms-full.txt - полный контекст для docs/knowledge base; обычному лендингу чаще не нужен. | https://cdn.openai.com/API/docs/txt/llms.txt; https://platform.claude.com/llms.txt | Результат: читатель не генерирует огромный файл без пользы. |

## action_outline
1. Сначала принять решение: делаем llms.txt как карту для AI-агентов, а не как гарантию AI SEO. Если цель только "попасть в Google AI", сослаться на Google Search Central и не обещать эффект.
2. Собрать список 10-30 главных URL: главная, о компании/эксперте, услуги/продукты, ключевые гайды, кейсы, FAQ, контакты; исключить теги, пагинацию, мусорные архивы.
3. Сгруппировать ссылки по задачам, а не по типу контента: "Что делает компания", "Гайды и инструкции", "Кейсы", "Данные и цены", "Контакты". Для docs-сайта группировать по продуктовым поверхностям/API.
4. Написать файл в формате Markdown: H1 с названием сайта, blockquote с 1-2 предложениями, короткий контекст, H2-разделы и bullets вида [Название](URL): зачем читать эту страницу.
5. Вынести второстепенное в ## Optional: новости, архивы, changelog, press kit, низкоприоритетный блог, если они не нужны для первого ответа агента.
6. Решить, нужен ли llms-full.txt: да для документации/API/базы знаний; обычно нет для небольшого бизнес-сайта или лендинга.
7. Разместить /llms.txt в корне сайта: public/llms.txt для статических/Next/Astro, файл в корне хостинга для WordPress, route/rewrites для CMS, следить за content-type text/plain или text/markdown.
8. Проверить вручную: открыть https://domain.ru/llms.txt, убедиться в HTTP 200, отсутствии HTML/404-шаблона, рабочих абсолютных URL, нормальном Markdown и актуальных описаниях.
9. Прогнать Lighthouse Agentic Browsing/Chrome DevTools или хотя бы убедиться, что запрос /llms.txt не даёт 5xx; помнить, что 404 без файла сейчас N/A, но если файл есть, он должен быть корректным.
10. Добавить процесс поддержки: обновлять файл при публикации ключевой страницы, раз в месяц смотреть server logs на запросы /llms.txt, удалять устаревшие URL и не мерить успех только по цитатам в AI.

## practical_template_notes_for_writer
- Обязательный framing: "llms.txt не продвигает сайт сам по себе; он помогает агенту быстрее понять, что читать".
- Не использовать формулировки "попадание в ответы нейросетей гарантировано", "Google любит llms.txt", "новый robots.txt".
- В статье дать короткий шаблон для обычного сайта и отдельную ремарку для docs/knowledge base.
- До FAQ нужен блок "как понять, что задача решена": URL открывается, структура валидная, ссылки рабочие, файл актуален, в логах можно видеть обращения, но их может не быть.
- CTA можно связать с Make/Cursor workflow: автоматизировать обновление llms.txt из sitemap/таблицы контент-приоритетов, но не превращать статью в продажу.
