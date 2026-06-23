# Research notes — B07 «Как построить RAG-систему с векторной базой знаний»

**topic_id:** B07  
**slug:** postroenie-rag-sistemy-vektornaya-baza  
**article_mode:** B (workflow)  
**search_intent:** workflow  
**disclaimer:** Все даты, версии и статистика проверены на 2026-06-16 (2026 год). Окно свежести: prefer_sources_after=2026-03-18.

---

research_date: 2026-06-16
accessed_at: 2026-06-16
utility_verdict: PASS
reader_outcome: Читатель пройдёт workflow от PDF/DOCX до ответов с цитатами — выберет векторное хранилище (pgvector или Qdrant/Chroma для PoC), настроит чанкинг 300–512 токенов с overlap 10–20%, соберёт retrieval-цепочку на Python (LangChain) или в n8n и проверит качество по eval-чеклисту из 10+ вопросов.
reader_pain: Демо «загрузил PDF — задал вопрос — получил уверенную ерунду»: retrieval возвращает нерелевантные чанки, ответы не ссылаются на источник, а при росте корпуса растут задержки и счёт за токены; непонятно, нужен ли вообще RAG или хватит длинного контекста.
success_criteria: На 10–15 тестовых вопросах из своих документов система отвечает с указанием файла/раздела, в ≥8 из 10 случаев ответ подтверждается найденным чанком; при «нет данных в базе» модель отказывается галлюцинировать; время ответа и стоимость зафиксированы в таблице до/после настройки rerank и гибридного поиска.
voice_angle: Инженер, который один раз «убил RAG» большим контекстом и публично облажался перед пользователями — показывает честный пайплайн 2026 без магии «векторная БД за вечер».
reader_story: Команда загрузила 200 регламентов в Chroma, задала вопрос про исключение из политики возвратов — retrieval вернул чанк «возвраты разрешены», а фраза «кроме акционных билетов» осталась в соседнем чанке; бот ответил клиенту уверенно и неверно. После смены чанкинга на 400 токенов + overlap 15% и rerank точность на golden set выросла с 4/10 до 9/10.
surprising_fact: В 2026 тренд «длинный контекст вместо RAG» снова откатывается: на Habr автор с реальным продакшеном описывает, что замена retrieval на «вставим весь корпус в промпт» сначала прошла демо, а потом дала предсказуемые провалы — устаревшие документы, ответы не тому пользователю и уверенные галлюцинации; при этом у pgvector лимит HNSW — 2000 измерений, и для text-embedding-3-large (3072) без halfvec индекс не соберётся.

## research_questions

1. Когда RAG с векторной БД оправдан, а когда достаточно длинного контекста LLM?
2. Какой чанкинг (размер, overlap, разделители) даёт приемлемый recall на русскоязычных регламентах и PDF?
3. pgvector в Postgres vs Qdrant/Chroma для PoC: что выбрать под self-host и под n8n?
4. Как настроить HNSW, top-k, гибридный BM25+vector и rerank без перегруза latency?
5. Как собрать ingestion + query в LangChain (Python) и альтернативу в n8n (два workflow)?
6. Какие failure modes (chunk boundary, context sufficiency, embedding mismatch) ловить в eval?
7. Что пишут конкуренты в SERP 2026 и где у них нет пошагового workflow с eval?

## source_table

| source | url | accessed_at | why_it_matters |
| --- | --- | --- | --- |
| LangChain — tutorial RAG (Python) | https://python.langchain.com/docs/tutorials/rag/ | accessed_at: 2026-06-16 | Канонический пайплайн: load → split → embed → vector store → retriever → generation |
| n8n Docs — RAG in n8n | https://docs.n8n.io/advanced-ai/rag-in-n8n/ | accessed_at: 2026-06-16 | Два workflow (ingestion/query), сплиттеры, vector store как tool у агента |
| Qdrant Documentation | https://qdrant.tech/documentation/ | accessed_at: 2026-06-16 | Коллекции, points, batch upsert, cloud/local quickstart для PoC |
| pgvector — guide HNSW/IVFFlat (март 2026) | https://www.dbi-services.com/blog/pgvector-a-guide-for-dba-part-2-indexes-update-march-2026/ | accessed_at: 2026-06-16 | Лимит 2000 dim для HNSW, halfvec, tuning ef_search; выбор индекса |
| Habr OTUS — «Возвращение RAG в 2026» | https://habr.com/ru/companies/otus/articles/1001970/ | accessed_at: 2026-06-16 | Боль продакшена: big context vs RAG, гибрид, rerank, eval retrieval-слоя |
| Red Gate — RAG hallucinations (6 failure points) | https://www.red-gate.com/simple-talk/ai/how-to-stop-ai-hallucinations-in-enterprise-rag-systems-a-complete-guide/ | accessed_at: 2026-06-16 | Чанкинг, version drift, hybrid+rerank+confidence gates |
| OvertimeLabs — Stop RAG hallucinating | https://overtimelabs.ai/articles/stop-rag-hallucinating | accessed_at: 2026-06-16 | Диагностика retrieval vs generation failure; структурный чанкинг 200–500 tokens |
| Appycodes — Production RAG Pipeline 2026 | https://appycodes.dev/blog/production-rag-pipeline-2026/ | accessed_at: 2026-06-16 | Recall@5 пик 600–900 tokens; retrieve k=20 → rerank до 4–6 в prompt |
| n8nautomation.cloud — Build RAG workflows | https://n8nautomation.cloud/blog/build-rag-workflows-n8n-vector-stores-ai-memory | accessed_at: 2026-06-16 | Ingestion vs query, PGVector/Qdrant в n8n, совпадение embedding-модели |
| SAP Community — Chunking strategies production | https://community.sap.com/t5/artificial-intelligence-blogs-posts/the-rag-chunking-strategies-that-can-actually-survive-production/ba-p/14412471 | accessed_at: 2026-06-16 | Обзор стратегий: recursive, semantic, contextual retrieval, adaptive chunking |
| IXBT — Google agentic RAG (июнь 2026) | https://www.ixbt.com/news/2026/06/08/google-agentic-rag.html | accessed_at: 2026-06-16 | Контекст тренда: agentic RAG vs одношаговый retrieve |
| ai.low-light.ru — корпоративная база знаний RAG 2026 | https://ai.low-light.ru/blog/rag-sistemy-korporativnaya-baza-znaniy-2026/ | accessed_at: 2026-06-16 | Конкурент SERP: архитектура, сравнение LangChain/LlamaIndex, Qdrant/Pinecone/FAISS |
| Habr — документный хаос, RAG Python ChromaDB | https://habr.com/ru/articles/955768/ | accessed_at: 2026-06-16 | Практический workflow на русском: индексация → поиск → ответ с контекстом |

## wordstat

Данные: MCP `wordstat_get_top_requests`, сервер mcp-kv, регион 225 (Россия), 2026-06-16.

| phrase | impressions |
| --- | ---: |
| rag система | 2125 |
| система retrieval augmented generation rag | 102 |
| rag система ии | 86 |
| создание rag системы | 76 |
| rag система ai | 63 |
| локальная rag система | 57 |
| разработка rag систем | 51 |
| архитектура rag системы | 40 |
| построение rag системы | 39 |
| rag система python | 24 |
| как сделать rag систему | 20 |
| локальные нейросети с rag системой | 16 |

**LSI для writer:** векторная база знаний, эмбеддинги, чанкинг, гибридный поиск, rerank, pgvector, Qdrant, LangChain, n8n vector store, top-k, HNSW, локальная rag, eval качества ответов.

## github_evidence

| repo/issue/doc | url | signal |
| --- | --- | --- |
| pgvector README | https://github.com/pgvector/pgvector | Официальный Postgres-экстеншен; HNSW/IVFFlat, cosine/L2 ops |
| infiniflow/ragflow — issue #3118 | https://github.com/infiniflow/ragflow/issues/3118 | Разные чанки в RAGFlow vs LangChain+FAISS — боль «не тот chunker» |
| Yigtwxx/Awesome-RAG-Production | https://github.com/Yigtwxx/Awesome-RAG-Production | Production pitfalls: fixed chunk size, 256–512 tokens старт, Ragas/DeepEval |
| ombharatiya/ai-system-design-guide — chunking | https://github.com/ombharatiya/ai-system-design-guide/blob/main/06-retrieval-systems/02-chunking-strategies.md | Parent-child hierarchical chunking против broken context |
| infiniflow/ragflow | https://github.com/infiniflow/ragflow | Open-source RAG engine; reference для enterprise UI поверх того же пайплайна |
| langchain-ai/langchain — RAG tutorial path | https://github.com/langchain-ai/langchain | Экосистема LCEL/LangGraph для retrieval chains |

## pain_solution_map

| pain | solution | proof/source | reader_result |
| --- | --- | --- | --- |
| Ответ уверенный, но неверный — retrieval нашёл «похожий», но неполный чанк | Recursive split 300–512 токенов, overlap 10–20%, parent-child или заголовок в тексте чанка; rerank top-20 → 4–6 | https://www.red-gate.com/simple-talk/ai/how-to-stop-ai-hallucinations-in-enterprise-rag-systems-a-complete-guide/ ; https://appycodes.dev/blog/production-rag-pipeline-2026/ | На golden set растёт доля ответов, подтверждённых цитатой из нужного раздела |
| Пропускаются артикулы, коды ошибок, имена — чистый vector top-k | Гибридный поиск BM25 + vector + metadata filters (tenant, doc type) | https://habr.com/ru/companies/otus/articles/1001970/ | Запросы с точными токенами находят нужный фрагмент |
| «Зачем RAG, если контекст 1M токенов?» — демо ок, прод ломается | RAG как отбор доказательств: freshness, ACL, audit trail, cost/latency | https://habr.com/ru/companies/otus/articles/1001970/ | Читатель фиксирует критерии: когда long context, когда векторная БД обязательна |
| Разные ответы в n8n и в Python — разные embeddings или chunker | Один embedding на ingest и query; в n8n — тот же splitter, что в dev | https://docs.n8n.io/advanced-ai/rag-in-n8n/ ; https://n8nautomation.cloud/blog/build-rag-workflows-n8n-vector-stores-ai-memory | Повторяемые результаты между PoC и прод-workflow |
| pgvector: индекс не строится на больших embedding | halfvec или смена модели (≤2000 dim); HNSW defaults m=16, ef_construction=64 | https://www.dbi-services.com/blog/pgvector-a-guide-for-dba-part-2-indexes-update-march-2026/ | Индекс создаётся, latency поиска предсказуема |
| Нет метрик — «кажется лучше» | Eval: 10–15 Q&A + отказ при пустом retrieval + лог chunk IDs | https://overtimelabs.ai/articles/stop-rag-hallucinating | Команда видит регрессии при смене чанкинга/модели |

## competitor_gaps

| competitor | what_they_miss | how_we_write_better |
| --- | --- | --- |
| chimitdorzhi.tech / aibotmanager — «что такое RAG 2026» | Мало пошагового workflow с eval и выбором pgvector vs Qdrant | Один сквозной pipeline документы → ответы + чеклист качества |
| annelo.ru / whitetigersoft — обзор без кода | Нет n8n-ветки и hybrid+rерank | Две дорожки: Python (LangChain) и n8n для no-code |
| ai.low-light.ru — корпоративный гайд | Слабая связка с автоматизацией (n8n agents) | Internal link на /avtomatizaciya-n8n-ai-agents/ + RAG tool в агенте |
| external.software / promaren — SEO-лонгриды | Повторяют определения, мало failure modes | reader_story + pain_solution_map как скелет H2 |

## action_outline

1. **Зафиксировать сценарий и golden set:** 10–15 реальных вопросов по вашим PDF/DOCX + критерий «ответ только из базы».
2. **Решить RAG vs long context:** если нужны ACL, свежесть, аудит или корпус > нескольких МБ — векторная БД; иначе — короткий пилот с полным файлом в промпте.
3. **Подготовить документы:** парсинг PDF/DOCX/MD, очистка; RecursiveCharacterTextSplitter 300–512 токенов, overlap 10–20%, метаданные source/section/page.
4. **Выбрать хранилище:** PoC — Qdrant Docker или Chroma; если уже есть Postgres — pgvector + HNSW (проверить размерность embedding).
5. **Индексация:** одна embedding-модель на ingest и query; batch upsert; для pgvector — `CREATE INDEX ... USING hnsw` с cosine ops.
6. **Retrieval-цепочка:** hybrid BM25+vector, top-k 15–20, rerank до 4–6 чанков, system prompt «только по контексту + цитаты».
7. **Сборка интерфейса:** Python (LangChain RAG chain) или n8n — workflow ingestion + workflow query (QA Chain для строгого RAG или AI Agent с vector tool).
8. **Eval и мониторинг:** прогон golden set, лог retrieved chunk IDs, порог отказа при низкой similarity; повтор при смене корпуса.
9. **Подключение к автоматизации:** n8n AI Agent + RAG tool, webhook/Telegram; план обновления базы при смене регламентов.

## verified_facts

| Факт | Источник | accessed_at |
| --- | --- | --- |
| Спрос «rag система» в Wordstat РФ — 2125 показов/мес | MCP wordstat_get_top_requests | accessed_at: 2026-06-16 |
| n8n рекомендует Recursive Character Text Splitter для большинства кейсов; чанки 200–500 tokens | https://docs.n8n.io/advanced-ai/rag-in-n8n/ | accessed_at: 2026-06-16 |
| RAG в n8n: отдельные workflow для загрузки и для запросов | https://docs.n8n.io/advanced-ai/rag-in-n8n/ | accessed_at: 2026-06-16 |
| pgvector HNSW: лимит 2000 измерений на тип vector; halfvec до 4000 | https://www.dbi-services.com/blog/pgvector-a-guide-for-dba-part-2-indexes-update-march-2026/ | accessed_at: 2026-06-16 |
| HNSW defaults: m=16, ef_construction=64, ef_search=40 | https://dev.to/philip_mcclarence_2ef9475/ivfflat-vs-hnsw-in-pgvector-which-index-should-you-use-305p | accessed_at: 2026-06-16 |
| Production-практика: retrieve k=20, rerank до 4–6; recall@5 пик 600–900 tokens | https://appycodes.dev/blog/production-rag-pipeline-2026/ | accessed_at: 2026-06-16 |
| LangChain RAG: indexing = split + embed + vector store; query = similarity search + LLM | https://python.langchain.com/docs/tutorials/rag/ | accessed_at: 2026-06-16 |
| Qdrant: point = vector + optional payload; batch upsert для ingestion | https://qdrant.tech/documentation/manage-data/points/ | accessed_at: 2026-06-16 |
| Фиксированный чанкинг режет правило и исключение по разным чанкам → галлюцинации | https://www.red-gate.com/simple-talk/ai/how-to-stop-ai-hallucinations-in-enterprise-rag-systems-a-complete-guide/ | accessed_at: 2026-06-16 |
| «RAG мёртв» ломается на freshness, permissions, audit, cost | https://habr.com/ru/companies/otus/articles/1001970/ | accessed_at: 2026-06-16 |

## h2_mapping (из blog-topics B07)

1. Сценарий: векторная БД vs длинный контекст  
2. Подготовка документов: парсинг, чанкинг 300–512, overlap 10–20%  
3. pgvector vs Qdrant/Chroma для PoC  
4. Эмбеддинги, HNSW, top-k, hybrid BM25+vector  
5. Retrieval: rerank, prompt grounding, anti-hallucination  
6. n8n/API: AI Agent + RAG tool, обновление базы, eval-чеклист  

**Internal links:** /avtomatizaciya-n8n-ai-agents/, /podklyuchenie-mcp-cursor/
