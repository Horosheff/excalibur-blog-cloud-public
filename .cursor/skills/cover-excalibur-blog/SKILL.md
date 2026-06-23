# Excalibur BLOG — Cover Agent (полный skill)

## Когда запускаться

После **GEO QA PASS**. Вход: `article.html`, `article.meta.json`, handoff `ready_for: excalibur-blog-cover`.

Параллельно с `excalibur-blog-schema`. **Не** править schema и body longread.

---

## Архитектура (зафиксировано)

```text
reference PNG → reference_url_hosted
       ↓
quad-manifest.json (agent fills hooks + scene_hint)
       ↓
quad-mcp-batch.json (1 job, input_urls, api_args)
       ↓
ONE Kie GPT Image 2 i2i API task → canvas-quad.png 2048×1152
       ↓
split → cover.png + inline-01..03.png (1200×675)
       ↓
inject <figure> after H2 in article.html
```

**Запрещено:** 4 отдельных image jobs на cover + inline.

---

## Контракты и конфиги

| Путь | Назначение |
|------|------------|
| `shared/blog-cover-quad-canvas-contract.md` | канонический контракт |
| `shared/kie-gpt-image-api-contract.md` | прямой async Kie API для Cursor Cloud |
| `shared/mcp-image-async-contract.md` | legacy async contract для image MCP tools |
| `agents/excalibur-blog-cover.md` | agent-md (этот skill дублирует runbook) |
| `memory/cover/blog-hero.json` | visual_lock, outfit_rule, reference_url_hosted |
| `memory/cover/assets/blog-hero-reference.png` | локальный эталон лица |
| `memory/cover/cover-design-code.json` | human hook collage, fake скрины, мемы |
| `memory/cover/quad-style-digital-meme-collage-ru.json` | style preset + design_code link |
| `memory/cover/inline-visual-types.json` | типы inline-панелей |
| `memory/brief/site-brief.md` | blog_hero_id, обложка = крючок |

---

## Панели quad 2×2

| Квадрант | Слот | Содержание |
|----------|------|------------|
| top-left | cover | hook + meme_caption_ru + **герой (reference face)** + design code |
| top-right | inline_1 | visual_type по H2 #1, **без героя** |
| bottom-left | inline_2 | visual_type по H2 #2 |
| bottom-right | inline_3 | visual_type по H2 #3 |

---

## Герой (blog-host)

**Lock (reference i2i):** очки, quiff, борода — то же лицо.  
**Lock (outfit):** белое плотное худи heavyweight fabric.
**Free (агент):** поза, жест, ракурс, выражение, реквизит и композиция — по `cover_hook` и `scene_hint`; каждый раз заметно разные. Наушники/headset/earbuds запрещены.
**Не** копировать костюм с reference-фото, если scene_hint не просит.

---

## Design code — открываемость

Из `cover-design-code.json`:

1. Fake UI: Wordstat, Metrica, Telegram, отзывы ★☆☆☆☆
2. Background: чистый белый `#FFFFFF` для cover и всех inline; без бежевого/серого/grunge-фона
3. Typography: как на DESIGN.md-референсе — жирный condensed Cyrillic, ротация hot-акцентов (hot pink, hot purple, hot blue, hot orange и другие), sticker labels, brush bubbles, handwritten speech bubble; без price badges
4. DIY: torn paper, scotch tape, pink sticky notes, marker arrows
5. Highlight: розовый маркер на ключевом слове hook
6. Memes: визуальные reaction cutouts (cat, facepalm, rough-edge visual cutout) — max 1 Drake на холст, без принудительного сленга и без токсичных/оскорбительных sticker-фраз
7. Формат **16:9**, не Instagram carousel 9:16
8. Inline: полезный UI + обязательный human layer (рваная бумага, tape, pink sticky note, marker annotation, маленький visual meme reaction cutout) на белой базе. Plain whiteboard / минималистичная SaaS-схема = blocker.

---

## Пошаговый runbook

### Шаг 0 — прочитать статью

- H2 (до FAQ): первые 3 → inline anchors
- lead, primary query → cover_hook
- `article.meta.json`: h1, topic_id

### Шаг 1 — reference URL

```bash
python scripts/excalibur_blog_hero_reference_url.py
```

Проверить `memory/cover/blog-hero.json` → `reference_url_hosted`.  
Fallback env: `BLOG_HERO_REFERENCE_URL`.

### Шаг 2 — manifest

```bash
python scripts/excalibur_blog_quad_manifest.py \
  --article-dir memory/blog/articles/<topic_id>-<slug> \
  --merge
```

**Руками** доработать `cover/quad-manifest.json`:

- `cover_hook` — провокация
- `slots.cover.meme_caption_ru` — 2–6 слов, дерзко/иронично, но без оскорблений и унижающих ярлыков (`лох`, `лохов`, `для лохов` и похожее запрещены)
- `slots.cover.scene_hint` — fake скрины + мемы + белое плотное худи + новая поза/жест/ракурс агента; без наушников/headset/earbuds
- `slots.inline_*.scene_hint` — конкретика H2 + чисто белый фон `#FFFFFF`
- `alt` — осмысленные, не «seo картинка»

### Шаг 3 — prompt + batch

```bash
python scripts/excalibur_blog_cover_quad_prompt.py \
  --article-dir memory/blog/articles/<topic_id>-<slug> \
  --write-batch
```

Проверить `cover/quad-mcp-batch.json`: **jobs.length === 1**, `input_urls` не пуст.

Hard checks перед MCP:

- batch всегда пересобран в текущем run; не использовать старый `quad-mcp-batch.json`
- `validation.prompt_chars <= 3500`
- `reference_url_hosted` содержит `mayai.ru`, не `files.catbox.moe`
- `jobs[0].mcp_args.resolution === "2K"`

### Шаг 4 — Kie image API

Правильный контракт для Cursor Cloud: **async HTTP API flow**, не sync MCP call.

```bash
python scripts/excalibur_blog_kie_gpt_image2_api.py \
  --article-dir memory/blog/articles/<topic_id>-<slug>
```

Требования:

- `KIE_API_KEY` задан в Cloud Secrets/env; ключ не писать в файлы, handoff, PR или terminal output.
- Скрипт читает `cover/quad-mcp-batch.json`, создаёт `createTask`, polling'ом вызывает `recordInfo`, пишет `cover/quad-mcp-result.json`.
- `cover/kie-image-task.json` хранит `task_id`/status без секретов.

Ожидание: Image to Image, 1 входное фото, aspect 16:9, resolution 2K.

Prompt budget: короткий compact prompt. Не дублировать полный brand-lock, suffix и negative на каждую панель; одна общая style-инструкция + короткое описание 4 квадрантов.

### Шаг 4.1 — legacy MCP fallback / timeout policy

Backend `gpt-image-2` может ждать Kie.ai до **15 минут**. В Cloud HTTP-клиент MCP может оборвать sync call раньше с:

```text
HTTP MCP tool execution failed: MCP error -32001: Request timed out
```

Это означает, что Cursor MCP client оборвал длинный sync call раньше, чем backend вернул URL. Делай так:

1. Убедись, что ошибка именно `-32001 Request timed out`, а не schema/auth/input.
2. Не ищи URL в `cover/*` или других article files: при timeout `quad-mcp-result.json` ещё не существует, пока агент сам не запишет URL.
3. Проверь expanded MCP tool response / Cursor MCP Logs: если там уже появился generated image URL, это **успех**.
4. Если в логе есть `task_id`, но нет URL — используй status/result MCP tool, если он доступен.
5. Если нет URL, нет `task_id` и нет status/result tool — используй прямой Kie API script. Если прямой API недоступен — `COVER MCP ASYNC BLOCKER`.

MCP-вызов теперь только legacy fallback. Основной Cloud path — `scripts/excalibur_blog_kie_gpt_image2_api.py`.

Запрещено: останавливать cover после первого timeout без диагностики, запускать повторную sync-генерацию после client timeout, делать 4 отдельных генерации, вызывать MCP через скрипт, идти дальше без URL.

### Шаг 5 — apply

```bash
python scripts/excalibur_blog_quad_apply.py \
  --article-dir memory/blog/articles/<topic_id>-<slug> \
  --inject-html
```

Требует Pillow. Выход: cover, inline PNG, registry, inject в article.html.

### Шаг 6 — fragment

`.cursor/excalibur-blog-fragments/cover.md` — шаблон в `agents/excalibur-blog-cover.md`.

### Шаг 6.5 — visual QA PNG

Открыть/проверить `cover/cover.png` и `cover/inline-01..03.png`.

`quad-split-report.json PASS` проверяет геометрию, но не стиль. Если inline-панель выглядит как plain whiteboard / минималистичная SaaS-схема без рваной бумаги, скотча, розового стикера, маркерной пометки и visual meme cutout — это `COVER STYLE BLOCKER`, нужна перегенерация quad canvas.

---

## visual_type (inline)

| type | Когда |
|------|-------|
| `comparison_table_ui` | SEO vs GEO, сравнение |
| `workflow_diagram` | структура, шаги, longread |
| `checklist_board` | чеклист, публикация |
| `schema_faq_ui` | FAQ, schema, JSON-LD |
| `tool_screenshot` | Wordstat, инструменты |
| `infographic_card` | цифры, факты |

Keywords + автовыбор: `inline-visual-types.json` + `quad_manifest.py`.

---

## QA перед ✅

- [ ] 1 image job, не 4
- [ ] input_urls в image API/MCP
- [ ] cover.png + 3 inline существуют
- [ ] alt в registry для всех 4
- [ ] inline привязаны к H2 (`h2_anchor`)
- [ ] cover: hook + meme caption видны на PNG
- [ ] cover/inline visible text: нет токсичных или оскорбительных sticker-фраз (`лох`, `лохов`, `для лохов`, унижающие ярлыки)
- [ ] inline: без лица героя
- [ ] cover и inline: чистый белый фон `#FFFFFF`, без бежевого/серого/grunge-фона
- [ ] cover: typography похожа на DESIGN.md-референс (жирный condensed Cyrillic, hot-акценты чередуются: hot pink/hot purple/другие, sticker labels/brush bubbles/handwritten notes, без price badges)
- [ ] inline: в стиле Excalibur series, не plain whiteboard/minimal SaaS
- [ ] визуальные meme reaction cutouts есть на cover и хотя бы малым sticker-layer на inline, без forced slang
- [ ] fragment cover.md записан

---

## Blockers → verdict ❌

- нет reference_url_hosted
- image call text-only (без input_urls)
- `KIE API BLOCKER`: нет `KIE_API_KEY`, createTask/recordInfo fail, polling timeout или нет resultUrls
- async status/result tool подтвердил failed/no result или повторный timeout уже в status/result flow
- `COVER MCP RECOVERY NEEDED`: после timeout агент не имеет доступа к MCP/Cursor log, где виден generated URL; нужен URL из лога, повторять генерацию вслепую нельзя
- `COVER MCP ASYNC BLOCKER`: sync `gpt-image-2` обрывается по client timeout, а MCP server не даёт `task_id` и отдельный status/result tool для получения позднего URL
- 4 отдельные генерации
- QUAD SPLIT fail
- inline = meme с ведущим вместо UI
- inline = plain whiteboard/minimal SaaS без рваной бумаги, скотча, розового стикера, маркерной пометки и визуального meme cutout
- visible generated sticker text contains insults/toxic labels (`лох`, `лохов`, `для лохов`, унижающие ярлыки)

---

## Deprecated scripts

Не вызывать:

- `excalibur_blog_visual_prompts.py`
- `excalibur_blog_visual_apply.py`
- `excalibur_blog_visual_manifest.py`

См. `shared/blog-visual-pipeline-contract.md`.

---

## Эталон (B01)

`memory/blog/articles/B01-primer-seo-stati/cover/` — reference implementation после design code v1.
