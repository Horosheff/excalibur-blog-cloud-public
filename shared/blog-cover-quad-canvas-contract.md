# Excalibur BLOG — Quad Canvas (1 Image API → 4 панели)

Cover-агент работает **после** `article.html` + GEO QA PASS.

## Главное правило

**Одна** генерация Kie GPT Image 2 Image-to-Image API → один холст `2048×1152` (2×2, каждая панель 16:9) → split в `cover.png` + `inline-01..03.png`.

Prompt должен быть коротким: один общий style-lock + 4 коротких описания квадрантов. Не дублировать длинные style/negative blocks на каждую панель.

Hard gate перед image API:

- `quad-mcp-batch.json` пересобран текущим run, а не взят из старого article artifact
- `validation.prompt_chars <= 3500`
- `reference_url_hosted` содержит `mayai.ru`; `files.catbox.moe` запрещён для reference
- `jobs[0].mcp_args.resolution == "2K"`

| Панель | Роль | Герой |
|--------|------|-------|
| **top-left cover** | Крючок + RU-мем | **да**, лицо с reference (`input_urls`); одежда = белое плотное худи; поза/жест/ракурс/реквизит каждый раз разные; без наушников |
| **3 inline** | Полезность по H2: таблица, workflow, чеклист, UI | **нет** |

## Workflow

```bash
# 1. Публичный URL эталона (обязательно для i2i)
python scripts/excalibur_blog_hero_reference_url.py

# 2. Manifest: cover_hook + visual_type для inline
python scripts/excalibur_blog_quad_manifest.py \
  --article-dir memory/blog/articles/<topic_id>-<slug> --merge

# 3. Промпт + image batch (1 job)
python scripts/excalibur_blog_cover_quad_prompt.py \
  --article-dir memory/blog/articles/<topic_id>-<slug> --write-batch

# 4. Kie async image API (primary Cloud path):
#    Требует env KIE_API_KEY из Cloud Secrets. Не писать ключ в файлы/логи.
#    Скрипт создаёт task через createTask, polling'ом recordInfo ждёт success,
#    затем пишет cover/quad-mcp-result.json с URL.
python scripts/excalibur_blog_kie_gpt_image2_api.py \
  --article-dir memory/blog/articles/<topic_id>-<slug>

# 5. Скачать canvas + split
python scripts/excalibur_blog_quad_apply.py \
  --article-dir memory/blog/articles/<topic_id>-<slug> \
  --inject-html
```

Legacy MCP fallback: если прямой Kie API недоступен, можно использовать Cursor MCP
`gpt-image-2` один раз с `jobs[0].mcp_args`. В Cursor Cloud sync MCP 2K i2i
может упасть с `-32001 Request timed out`; без URL/task_id/status tool это
`COVER MCP ASYNC BLOCKER`, повторять sync create вслепую нельзя.

## Раскладка 2×2

```text
+------------------+------------------+
|  cover (hero)    |  inline_1 (UI)   |
|  top_left        |  top_right       |
+------------------+------------------+
|  inline_2        |  inline_3        |
|  bottom_left     |  bottom_right    |
+------------------+------------------+
```

Split-скрипт **не режет механически 50/50**: ищет белые gutters у центра холста и режет по ним; затем center-crop до 16:9. Промпт: gutters только на линиях x=1024 / y=576, контент строго внутри квадранта.

## Visual locks

- Background: cover и все inline-панели на чистом белом `#FFFFFF`; запрещены beige/cream/off-white, gray, gradient и grunge full-panel backgrounds.
- Cover typography: как на DESIGN.md-референсе — жирный condensed Cyrillic, крупный uppercase hook, ротация hot-акцентов (hot pink, hot purple, hot blue, hot orange и другие), sticker labels, brush bubbles, handwritten speech notes; без price badges.
- Hero: сохранить старый meme-person vibe и reference face; одежда = белое плотное худи heavyweight fabric. Позу, жест, ракурс, выражение, реквизит и композицию менять от обложки к обложке. Headphones/headset/earbuds запрещены.

## Файлы

| Файл | Кто |
|------|-----|
| `memory/cover/blog-hero.json` | `reference_url_hosted` |
| `memory/cover/inline-visual-types.json` | типы inline-панелей |
| `cover/quad-manifest.json` | cover + inline slots |
| `cover/quad-mcp-batch.json` | **1 job**, `input_urls`, `api_args` |
| `cover/kie-image-task.json` | task_id/status прямого Kie API |
| `cover/quad-mcp-result.json` | URL результата (имя legacy, читает apply) |
| `cover/canvas-quad.png` | результат image API |
| `cover/cover.png`, `inline-01..03.png` | split script |
| `cover/cover-registry.json` | split script |

## Design code (открываемость)

`memory/cover/cover-design-code.json` — human hook collage для cover panel:

- fake скрины (Wordstat, отзывы, Telegram, analytics)
- чистый белый фон `#FFFFFF` для cover и inline
- типографика как DESIGN.md-референс: жирный condensed Cyrillic, hot-акценты чередуются (hot pink / hot purple / другие), sticker labels, brush bubbles, handwritten notes; без price badges
- рваная бумага, скотч, розовые стикеры, маркер
- визуальные meme reaction cutouts (не один Drake на весь холст): facepalm, кот-реакция, rough-edge visual cutout; без принудительных сленговых надписей
- 16:9 widescreen, **не** vertical carousel

Inline panels: полезный UI + обязательный human layer той же серии Excalibur на белой базе (рваная бумага, scotch tape, pink sticky note, marker annotation, pasted screenshot/card layer, маленький visual meme reaction cutout). Plain whiteboard / минималистичная SaaS-схема без этих признаков или цветной/beige/grunge фон = **COVER STYLE BLOCKER**, требуется перегенерация.

См. `memory/cover/inline-visual-types.json`. Выбор по keywords H2 в `excalibur_blog_quad_manifest.py`.

## Blockers

- `❌ COVER HERO BLOCKER` — нет `reference_url_hosted` или image call без `input_urls`
- `❌ KIE API BLOCKER` — нет `KIE_API_KEY`, createTask/recordInfo вернул fail, или polling не получил URL
- `❌ COVER MCP TIMEOUT BLOCKER` — image tool вернул повторный timeout, а status/result tool подтверждает failed/no result
- `❌ COVER MCP ASYNC BLOCKER` — sync `gpt-image-2` обрывается по client timeout, а MCP server не даёт `task_id` и отдельный status/result tool для получения позднего URL
- **4 отдельных image jobs** на cover+inline — запрещено
- inline-панель с meme/host вместо UI/схемы
- inline-панель выглядит как plain whiteboard/minimal SaaS и не несёт Excalibur collage style / visual meme cutout
- cover или inline имеют beige/gray/grunge/gradient full-panel background вместо чистого белого `#FFFFFF`
- обложка без крючка / без `meme_caption_ru`
