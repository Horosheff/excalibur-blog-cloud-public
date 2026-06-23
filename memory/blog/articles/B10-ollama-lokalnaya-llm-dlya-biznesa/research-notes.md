research_date: 2026-06-17
accessed_at: 2026-06-17
utility_verdict: PASS
reader_outcome: Развернуть локальную LLM через Ollama на корпоративном ПК или мини-сервере — от выбора сценария и модели под железо до проверки `ollama ps`, подключения OpenAI-совместимого API к n8n/Cursor/Python и безопасного контура с human-in-the-loop.
reader_pain: IT-директор или фрилансер слышит «локальная нейросеть = бесплатно и безопасно», ставит Ollama на офисный ПК с 8 ГБ VRAM, тянет 32B-модель, получает 2 токена/с на CPU, открывает порт 11434 в LAN «для коллег» — и через неделю узнаёт, что данные клиентов утекают в логи, а качество ответов хуже облака без fallback.
success_criteria: `ollama run qwen3:8b` (или выбранная модель) стабильно отвечает на тестовый промпт; `ollama ps` показывает 100% GPU (не CPU); `curl http://localhost:11434/v1/chat/completions` возвращает JSON; n8n/Cursor/Python-скрипт ходит в локальный endpoint; порт 11434 не торчит в интернет без прокси; задокументированы latency, качество на 20 тест-кейсах и правило эскалации на облако для критичных ответов.
voice_angle: Не обзор «топ моделей 2026», а цех владельца малого бизнеса: один сценарий (суммаризация внутренних документов / черновики писем / автоматизация через n8n), один сервер под столом, честный компромисс «приватность vs скорость», с чек-листом до первого API-запроса.
reader_story: Аналитик в агентстве поставил Ollama на Windows-сервер, сделал `OLLAMA_HOST=0.0.0.0` «чтобы n8n в Docker достучался», забыв про auth. Коллега из соседнего VLAN случайно увидел список моделей через `/api/tags`. Параллельно `ollama pull llama3.1:70b` на RTX 3060 12GB — модель «загрузилась», но `ollama ps` молча показал 80% CPU; проект списали как «локальный ИИ не работает».
surprising_fact: Ollama 0.30 (июнь 2026) сменил движок на нативный llama.cpp вместо GGML — это расширило совместимость с GGUF, но community фиксирует регрессии: `ollama ps` может показывать «100% GPU», пока `nvidia-smi` остаётся на нуле (issue #13814); первый диагностический шаг — не «переустановить всё», а сверить `ollama ps` с `nvidia-smi` и уменьшить модель.

Окно свежести источников: prefer_sources_after=2026-03-19 (контекст research-context.json, 2026 год).

## research_questions

1. Какой спрос и LSI у «ollama», «локальные нейросети» и вторичных запросов в РФ (июнь 2026)?
2. Когда локальная LLM через Ollama выгоднее облачного API для бизнеса (приватность, офлайн, стоимость токенов, 152-ФЗ)?
3. Какие минимальные требования к RAM/VRAM/GPU под qwen/llama/gemma4 в Ollama на 2026-06-17?
4. Как установить Ollama на Windows/Linux/macOS, скачать модель (`ollama pull`) и проверить инференс?
5. Как настроить OpenAI-совместимый API (`/v1/chat/completions`) и подключить к n8n, Cursor или Python?
6. Какие риски безопасности при `OLLAMA_HOST=0.0.0.0` и как закрыть контур (прокси, VPN, localhost-only)?
7. Какие типичные ошибки community (GPU fallback, Docker networking, контекст OOM) и как их диагностировать?
8. Что изменилось в Ollama 0.30 / MLX (июнь 2026) и как это влияет на выбор железа?
9. Где конкуренты в SERP дают только «топ моделей», не давая workflow до API?
10. Какие GitHub/docs-сигналы подтверждают стек Ollama + n8n + OpenAI SDK?

## source_table

| source | url | accessed_at | why_it_matters |
| --- | --- | --- | --- |
| Yandex Wordstat MCP (primary + secondary) | https://wordstat.yandex.ru | 2026-06-17 | Спрос: ollama 32 669/мес; локальные нейросети 5 854; ollama api 782 |
| Ollama — главная | https://ollama.com/ | 2026-06-17 | Официальный продукт, библиотека моделей, скачивание |
| Ollama Blog (июнь 2026) | https://ollama.com/blog | 2026-06-17 | Релизы 0.30, MLX 11.06, Nemotron 3 Ultra, ollama launch |
| Ollama Docs — OpenAI compatibility | https://docs.ollama.com/openai | 2026-06-17 | `base_url=http://localhost:11434/v1/`, api_key обязателен но игнорируется |
| Ollama Docs — n8n integration | https://docs.ollama.com/integrations/n8n | 2026-06-17 | Credential: localhost:11434 или host.docker.internal + extra_hosts |
| GitHub — ollama/ollama releases | https://github.com/ollama/ollama/releases | 2026-06-17 | v0.30 llama.cpp, июньские фиксы launch/MLX, теги релизов |
| GitHub — GPU silent fallback issue #13814 | https://github.com/ollama/ollama/issues/13814 | 2026-06-17 | `ollama ps` vs реальная загрузка GPU; регрессии 0.13.x |
| GitHub — warn on CPU fallback PR #14261 | https://github.com/ollama/ollama/pull/14261 | 2026-06-17 | Сообщество требует явного предупреждения при CPU fallback |
| n8n Blog — AI agents production | https://blog.n8n.io/best-practices-for-deploying-ai-agents-in-production/ | 2026-06-17 | Local LLMs via Ollama: нулевые API-затраты, полный контроль данных |
| Securing Ollama production guide | https://localaimaster.com/blog/securing-ollama-guide | 2026-06-17 | Нет встроенной auth; reverse proxy; 14k+ открытых инстансов в Shodan |
| InsiderLLM — ollama ps GPU fix | https://insiderllm.com/guides/ollama-not-using-gpu-fix/ | 2026-06-17 | Диагностика 100% CPU vs GPU/CPU split |
| Habr — топ локальных нейросетей 2026 | https://habr.com/ru/companies/bothub/articles/1028906/ | 2026-06-17 | Контекст спроса на локальный ИИ; приватность vs облако |
| Ollama MLX preview blog | https://ollama.com/blog/mlx | 2026-06-17 | MLX на Apple Silicon, NVFP4, требование 32GB+ unified memory для топ-моделей |
| Download Ollama Windows | https://ollama.com/download/windows | 2026-06-17 | Windows 10+, GPU acceleration, официальный инсталлятор |
| LocalLLM.in — VRAM guide 2026 | https://localllm.in/blog/ollama-vram-requirements-for-local-llms | 2026-06-17 | Таблицы VRAM: Qwen3 8B Q4 ~5.8GB, 14B Q4 ~10.7GB |

## wordstat

Данные: `wordstat_get_top_requests`, регион 225 (Россия), accessed_at: 2026-06-17.

| phrase | impressions |
| --- | ---: |
| ollama | 32669 |
| ollama модели | 2396 |
| ollama скачать | 1871 |
| ollama api | 782 |
| ollama windows | 880 |
| ollama нейросеть | 446 |
| установить ollama | 419 |
| ollama pull | 374 |
| ollama server | 377 |
| qwen ollama | 911 |
| ollama openai api | 36 |
| ollama local api | 46 |
| локальные нейросети | 5854 |
| как локально развернуть нейросеть | 124 |
| как установить нейросеть локально | 141 |
| локальная нейросеть на пк | 468 |
| ollama модели — лучшие модели для ollama | 100 |
| ollama модели — ollama русские модели | 42 |
| как установить ollama | 234 |
| ollama api key | 143 |

**LSI для Writer:** модели, скачать, установить, api, windows, qwen, локальные нейросети, pull, server, openai api, русские модели, нейросеть на пк, для кодинга, бесплатные модели.

**Смежный спрос (похожие):** llama — 30 566; нейросеть бесплатно — 1 138 727 (широкий хвост, не смешивать с узким intent ollama).

## github_evidence

| repo/issue/doc | url | signal |
| --- | --- | --- |
| ollama/ollama releases v0.30 | https://github.com/ollama/ollama/releases | 0.30: llama.cpp backend, GGUF, MLX на Apple Silicon; релизы 03–15.06.2026 |
| ollama/ollama README | https://github.com/ollama/ollama/blob/main/README.md | Официальные команды install, pull, run; список поддерживаемых моделей |
| Issue #13814 — GPU not used | https://github.com/ollama/ollama/issues/13814 | `ollama ps` врёт про GPU; регрессия скорости с 0.13.2 |
| PR #14261 — warn CPU fallback | https://github.com/ollama/ollama/pull/14261 | Предложение явно предупреждать при fallback на CPU |
| ollama/docs API | https://github.com/ollama/ollama/tree/main/docs | REST API, generate/chat/embeddings — контракт для интеграций |

## pain_solution_map

| pain | solution | proof/source | reader_result |
| --- | --- | --- | --- |
| Боль: модель «работает», но ответы идут минутами | Решение: проверить `ollama ps` (Processor: 100% GPU); уменьшить модель до Q4_K_M под VRAM (qwen3:8b на 8GB) | https://insiderllm.com/guides/ollama-not-using-gpu-fix/ ; https://github.com/ollama/ollama/issues/13814 | Результат: стабильные 20–40+ tok/s на GPU; предсказуемый SLA для внутренних задач |
| Боль: n8n в Docker не видит Ollama на хосте | Решение: credential `http://host.docker.internal:11434` + `extra_hosts: host.docker.internal:host-gateway` (Linux) | https://docs.ollama.com/integrations/n8n | Результат: workflow в n8n проходит тест «Connection tested successfully» |
| Боль: открыли Ollama в LAN без auth — риск утечки | Решение: `OLLAMA_HOST=127.0.0.1:11434` по умолчанию; для команды — reverse proxy с API key или Tailscale/VPN | https://localaimaster.com/blog/securing-ollama-guide | Результат: данные клиентов не доступны посторонним в сети |
| Боль: облачные токены съедают маржу на рутине | Решение: локальная модель для черновиков/классификации; облако только для сложного reasoning (hybrid) | https://blog.n8n.io/best-practices-for-deploying-ai-agents-in-production/ ; memory/brief/fact-bank.md (human-in-the-loop) | Результат: снижение API-затрат на повторяющиеся задачи при контролируемом качестве |
| Боль: непонятно, какую модель тянуть для русского и кода | Решение: qwen3 / gemma4 QAT для офисного ПК; таблица VRAM перед `ollama pull` | https://localllm.in/blog/ollama-vram-requirements-for-local-llms ; https://ollama.com/blog | Результат: одна рабочая модель под железо без OOM и переустановок |
| Боль: юридический страх — персональные данные в ChatGPT | Решение: self-hosted Ollama — промпты не покидают периметр; логи и retention под своей политикой | https://habr.com/ru/companies/bothub/articles/1028906/ | Результат: согласование с ИБ — обработка ПДн на своём железе |

## competitor_gaps

| competitor | what_they_miss | how_we_write_better |
| --- | --- | --- |
| vc.ru/dtf — «как установить Ollama 2026» | Установка и список моделей без бизнес-контура и API | Сквозной workflow: сценарий → железо → pull → API → n8n → security checklist |
| toolhalla/meshworld — «best models 2026» | Бенчмарки без интеграции в автоматизацию | Модель выбираем под задачу (суммаризация vs код), не под MMLU |
| trashexpert/universus — «топ локальных нейросетей» | Сравнение LM Studio vs Ollama без корпоративного API | Ollama как единый REST/OpenAI endpoint для n8n и Cursor |
| aravana/dtf howto | Нет раздела про `OLLAMA_HOST` и отсутствие auth | Явный блок «безопасный контур для офиса» с proxy/VPN |

## verified_facts

| fact | source | date_verified |
| --- | --- | --- |
| Спрос «ollama» — 32 669 показов/мес (РФ) | Wordstat MCP | 2026-06-17 |
| «локальные нейросети» — 5 854; «как локально развернуть нейросеть» — 124 | Wordstat MCP | 2026-06-17 |
| «ollama api» — 782; «ollama модели» — 2 396 | Wordstat MCP | 2026-06-17 |
| Ollama 0.30 (июнь 2026) использует llama.cpp для GGUF; MLX дополняет на Apple Silicon | https://ollama.com/blog ; https://github.com/ollama/ollama/releases | 2026-06-17 |
| MLX-обновление 11.06.2026: выше качество и скорость на Apple Silicon | https://ollama.com/blog | 2026-06-17 |
| OpenAI SDK: `base_url='http://localhost:11434/v1/'`, api_key required but ignored | https://docs.ollama.com/openai | 2026-06-17 |
| n8n: Base URL `http://localhost:11434` или `host.docker.internal:11434` + extra_hosts на Linux | https://docs.ollama.com/integrations/n8n | 2026-06-17 |
| Ollama не имеет встроенной аутентификации — auth через reverse proxy | https://localaimaster.com/blog/securing-ollama-guide | 2026-06-17 |
| Qwen3 8B Q4_K_M — ~5.8 GB VRAM (8k context) | https://localllm.in/blog/ollama-vram-requirements-for-local-llms | 2026-06-17 |
| 8 GB VRAM: комфортно 7–8B Q4; 16 GB — sweet spot для 13–14B | https://localllm.in/blog/ollama-vram-requirements-for-local-llms | 2026-06-17 |
| `ollama ps` показывает Processor: 100% CPU при проблемах с GPU | https://insiderllm.com/guides/ollama-not-using-gpu-fix/ | 2026-06-17 |
| Автономные ИИ завершают <2,5% сложных неструктурированных задач без человека (контекст HITL) | memory/brief/fact-bank.md | 2026-06-17 |
| ~40% проектов автономных ИИ-агентов отменяются из-за скрытых затрат и нулевого ROI | memory/brief/fact-bank.md | 2026-06-17 |

## source_access_log

- ollama.com/blog — accessed_at: 2026-06-17
- docs.ollama.com/openai — accessed_at: 2026-06-17
- docs.ollama.com/integrations/n8n — accessed_at: 2026-06-17
- github.com/ollama/ollama/releases — accessed_at: 2026-06-17
- github.com/ollama/ollama/issues/13814 — accessed_at: 2026-06-17
- wordstat.yandex.ru (MCP) — accessed_at: 2026-06-17
- localaimaster.com/blog/securing-ollama-guide — accessed_at: 2026-06-17
- insiderllm.com/guides/ollama-not-using-gpu-fix/ — accessed_at: 2026-06-17

## action_outline

1. **Выбрать один бизнес-сценарий** — внутренняя суммаризация документов, черновики писем, классификация тикетов или узел в n8n-workflow; зафиксировать, что модель не заменяет юриста/врача и требует human-in-the-loop на критичных ответах.
2. **Проверить железо и ОС** — RAM ≥16 GB, VRAM 8/12/16/24 GB; Windows 10+, Ubuntu 22.04+, macOS с Apple Silicon; таблица: 8 GB VRAM → qwen3:8b/gemma4:e4b Q4; 16 GB → qwen3:14b; сверить с https://localllm.in/blog/ollama-vram-requirements-for-local-llms.
3. **Установить Ollama и скачать модель** — `curl -fsSL https://ollama.com/install.sh | sh` (Linux) или инсталлятор с https://ollama.com/download/windows; `ollama pull qwen3:8b`; `ollama run qwen3:8b` + тестовый промпт на русском.
4. **Диагностировать GPU** — после первого запроса: `ollama ps` (ожидаем 100% GPU); параллельно `nvidia-smi`; при 100% CPU — меньшая модель или драйвер CUDA 12.4+.
5. **Поднять API** — проверить `curl http://localhost:11434/v1/chat/completions` с JSON body; для Python: OpenAI SDK с `base_url=http://localhost:11434/v1/` (docs.ollama.com/openai).
6. **Подключить к n8n или Cursor** — n8n: credential Ollama, при Docker на Linux — `extra_hosts`; Cursor: OpenAI-compatible endpoint на локальный URL; smoke-test одного workflow.
7. **Закрыть периметр** — не публиковать 11434 в интернет; `OLLAMA_HOST=127.0.0.1` или proxy с API key / Tailscale; логирование без сырого PII.
8. **Чек-лист запуска** — 20 тест-кейсов (качество, latency tok/s), правило fallback на облачную модель, регламент `ollama pull` для обновлений, метрика «стоимость сэкономленных токенов vs амортизация железа».
