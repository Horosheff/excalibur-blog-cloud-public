# Excalibur BLOG — Quad Canvas (1 MCP → 4 панели)

Cover-агент работает **после** `article.html` + GEO QA PASS.

## Главное правило

**Один** вызов MCP `gpt-image-2` → один холст `2048×1152` (2×2, каждая панель 16:9) → split в `cover.png` + `inline-01..03.png`.

Prompt должен быть коротким: один общий style-lock + 4 коротких описания квадрантов. Не дублировать длинные style/negative blocks на каждую панель.

Hard gate перед MCP:

- `quad-mcp-batch.json` пересобран текущим run, а не взят из старого article artifact
- `validation.prompt_chars <= 3500`
- `reference_url_hosted` содержит `example.com`; `example.com/assets` запрещён для reference
- `jobs[0].mcp_args.resolution == "2K"`

| Панель | Роль | Герой |
|--------|------|-------|
| **top-left cover** | Крючок + RU-мем | **да**, лицо с reference (`input_urls`); **одежда — на усмотрение агента** |
| **3 inline** | Полезность по H2: таблица, workflow, чеклист, UI | **нет** |

## Workflow

```bash
# 1. Публичный URL эталона (обязательно для i2i)
python scripts/excalibur_blog_hero_reference_url.py

# 2. Manifest: cover_hook + visual_type для inline
python scripts/excalibur_blog_quad_manifest.py \
  --article-dir memory/blog/articles/<topic_id>-<slug> --merge

# 3. Промпт + MCP batch (1 job)
python scripts/excalibur_blog_cover_quad_prompt.py \
  --article-dir memory/blog/articles/<topic_id>-<slug> --write-batch

# 4. MCP image tool:
#    Prefer async image tools if Available Tools exposes them:
#    create/start once with jobs[0].mcp_args → task_id; status/result by task_id → url.
#    If only sync `gpt-image-2` exists, call it once with jobs[0].mcp_args.
#    input_urls: [reference_url_hosted] — обязательно
#    Backend gpt-image-2 может ждать Kie.ai до 15 минут, но Cursor MCP client может оборвать sync call раньше.
#    HTTP MCP -32001 Request timed out — не финальный blocker с первой попытки:
#    если sync call вернул -32001:
#    - не искать URL в cover/* — он появится там только после ручной записи quad-mcp-result.json;
#    - проверить expanded tool response / Cursor MCP Logs;
#    - если есть generated URL — записать cover/quad-mcp-result.json вручную или передать URL сразу в quad_apply;
#    - если есть task_id — использовать status/result MCP tool;
#    - если нет URL/task_id/status tool — COVER MCP ASYNC BLOCKER: backend должен дать async retrieval, не retry вслепую.

# 5. Скачать canvas + split
python scripts/excalibur_blog_quad_apply.py \
  --article-dir memory/blog/articles/<topic_id>-<slug> \
  --url "<mcp_url>" --inject-html
```

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

## Файлы

| Файл | Кто |
|------|-----|
| `memory/cover/blog-hero.json` | `reference_url_hosted` |
| `memory/cover/inline-visual-types.json` | типы inline-панелей |
| `cover/quad-manifest.json` | cover + inline slots |
| `cover/quad-mcp-batch.json` | **1 job**, `input_urls` |
| `cover/canvas-quad.png` | MCP результат |
| `cover/cover.png`, `inline-01..03.png` | split script |
| `cover/cover-registry.json` | split script |

## Design code (открываемость)

`memory/cover/cover-design-code.json` — human hook collage для cover panel:

- fake скрины (Wordstat, отзывы, Telegram, analytics)
- рваная бумага, скотч, розовые стикеры, маркер
- визуальные meme reaction cutouts (не один Drake на весь холст): facepalm, кот-реакция, rough-edge visual cutout; без принудительных сленговых надписей
- 16:9 widescreen, **не** vertical carousel

Inline panels: полезный UI + обязательный human layer той же серии Excalibur (рваная бумага, scotch tape, pink sticky note, marker annotation, pasted screenshot/card layer, маленький visual meme reaction cutout). Plain whiteboard / минималистичная SaaS-схема без этих признаков = **COVER STYLE BLOCKER**, требуется перегенерация.

См. `memory/cover/inline-visual-types.json`. Выбор по keywords H2 в `excalibur_blog_quad_manifest.py`.

## Blockers

- `❌ COVER HERO BLOCKER` — нет `reference_url_hosted` или MCP без `input_urls`
- `❌ COVER MCP TIMEOUT BLOCKER` — image tool вернул повторный timeout, а status/result tool подтверждает failed/no result
- `❌ COVER MCP ASYNC BLOCKER` — sync `gpt-image-2` обрывается по client timeout, а MCP server не даёт `task_id` и отдельный status/result tool для получения позднего URL
- **4 отдельных MCP** на cover+inline — запрещено
- inline-панель с meme/host вместо UI/схемы
- inline-панель выглядит как plain whiteboard/minimal SaaS и не несёт Excalibur collage style / visual meme cutout
- обложка без крючка / без `meme_caption_ru`
