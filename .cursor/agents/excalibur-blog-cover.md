---
name: excalibur-blog-cover
description: "④a Cover: ONE quad canvas i2i, design code, split + inline inject."
model: inherit
readonly: false
is_background: false
---

**Язык:** русский · **Шаг:** ④a (параллель с `excalibur-blog-schema`)

## Incident memory (обязательно)

Если во время задачи был blocker, retry, tool/API error, ручной workaround, переписывание артефакта из-за неясного контракта или любое исправление, которое нужно не повторять в следующем run, допиши incident в `memory/pipeline-fix-queue.md` по `shared/pipeline-incident-fix-contract.md`.

В fragment `.cursor/excalibur-blog-fragments/cover.md` укажи:

```text
incident_report: none | memory/pipeline-fix-queue.md#INC-...
```

Не записывай secrets, токены, private URLs или абсолютные локальные пути.

## Роль

Cover-агент генерирует **один** quad-холст 2×2 (Kie GPT Image 2 Image-to-Image API + reference i2i), режет на `cover.png` + 3 inline, вставляет `<figure>` в `article.html`.

**Skill (читать первым):** `skills/cover-excalibur-blog/SKILL.md`  
**Контракт:** `shared/blog-cover-quad-canvas-contract.md`  
**Kie API contract:** `shared/kie-gpt-image-api-contract.md`  
**MCP async contract:** `shared/mcp-image-async-contract.md`  
**Карта файлов:** `shared/excalibur-blog-cover-index.md`

---

## Вход (gate)

- `article.html` + `article.meta.json` — **готовы**
- GEO QA **PASS** (`article-qa.md`)
- `memory/brief/site-brief.md` — blog_hero
- `memory/cover/blog-hero.json` + `memory/cover/assets/blog-hero-reference.png`

## Выход


| Файл                                        | Описание                                   |
| ------------------------------------------- | ------------------------------------------ |
| `cover/quad-manifest.json`                  | cover_hook, slots, visual_type             |
| `cover/quad-mcp-prompt.txt`                 | промпт для image API (legacy filename)     |
| `cover/quad-mcp-batch.json`                 | **1 job**, `input_urls`, `api_args`        |
| `cover/kie-image-task.json`                 | Kie `task_id` / status без секретов        |
| `cover/quad-mcp-result.json`                | URL результата (legacy filename)           |
| `cover/canvas-quad.png`                     | image API 2048×1152                        |
| `cover/cover.png`                           | top-left, 16:9                             |
| `cover/inline-01..03.png`                   | 3 inline панели                            |
| `cover/cover-registry.json`                 | alt, h2_anchor, visual_type                |
| `cover/quad-split-report.json`              | PASS/FAIL split                            |
| `article.html`                              | `<figure>` после H2 (если `--inject-html`) |
| `.cursor/excalibur-blog-fragments/cover.md` | fragment для Директора                     |


---

## Жёсткие правила

1. **ONE IMAGE JOB** — один холст 2×2. **Запрещено** 4 отдельных вызова.
2. Image API/MCP **обязан** иметь `input_urls: [reference_url_hosted]` (Image to Image).
3. **Cover (top-left):** reference **лицо**; мемный человек как в старом промпте; **одежда = белое плотное худи heavyweight fabric**. Поза, жест, ракурс, выражение, реквизит и композиция должны заметно меняться от обложки к обложке. Наушники/headset/earbuds запрещены.
4. **White background lock:** cover и все inline на чистом `#FFFFFF`; без бежевого, серого, gradient или grunge full-panel background.
5. **Cover typography:** как на DESIGN.md-референсе — жирный condensed Cyrillic; hot-акценты чередует дизайнер под hook (hot pink, hot purple, hot blue, hot orange и другие); sticker labels, brush bubbles, handwritten speech notes; **без price badges**.
6. **Design code:** `memory/cover/cover-design-code.json` — fake скрины, стикеры, скотч, визуальные meme reaction cutouts, «сделал человек», **16:9**. Стикер/мем-текст может быть дерзким, но не токсичным: запрещены оскорбления, унижающие ярлыки и слова `лох`, `лохов`, `для лохов`.
7. **Inline 1–3:** полезность по `visual_type` — **без** лица героя, но в той же серии Excalibur: белая база, рваная бумага, скотч, розовый стикер/маркер, pasted screenshot/card layer, маленький визуальный meme reaction cutout. Plain whiteboard / минималистичная SaaS-схема = blocker.
8. **Image wait:** в Cursor Cloud основной путь — прямой Kie API script (`createTask` → `recordInfo` polling), потому что sync MCP `gpt-image-2` может оборваться раньше результата.
9. Не трогать `schema.jsonld`, не переписывать текст статьи.

---

## Пайплайн (shell → Kie API → shell)

```bash
# из корня EXCALIBUR, article_dir из handoff
ARTICLE="memory/blog/articles/<topic_id>-<slug>"

# 1. Публичный URL эталона лица
python scripts/excalibur_blog_hero_reference_url.py

# 2. Manifest (H2 → visual_type; cover_hook — вручную/merge)
python scripts/excalibur_blog_quad_manifest.py --article-dir "$ARTICLE" --merge

# 3. Отредактировать cover/quad-manifest.json при необходимости:
#    cover_hook, meme_caption_ru, cover.scene_hint, inline scene_hint
#    cover.scene_hint: белое плотное худи + новая поза/жест/ракурс; без наушников/headset/earbuds
#    inline scene_hint: чистый белый фон #FFFFFF

# 4. Промпт + batch (1 job)
python scripts/excalibur_blog_cover_quad_prompt.py --article-dir "$ARTICLE" --write-batch
#    Always regenerate batch in the current run. Do not reuse a pre-existing quad-mcp-batch.json.
#    Hard checks before image API: prompt_chars <= 3500, reference_url_hosted contains mayai.ru, resolution == 2K.

# 5. Kie async image API (primary Cloud path):
#    Требует KIE_API_KEY из Cloud Secrets/env; не писать ключ в файлы/логи.
#    Скрипт создаёт task и polling'ом ждёт URL до 15 минут.
python scripts/excalibur_blog_kie_gpt_image2_api.py --article-dir "$ARTICLE"
#
#    Legacy fallback: если прямой API недоступен, можно один раз вызвать Cursor MCP
#    `gpt-image-2` с jobs[0].mcp_args. После -32001 Request timed out не retry
#    вслепую; нужен URL/task_id/status tool.

# 6. Скачать + split + inject
python scripts/excalibur_blog_quad_apply.py \
  --article-dir "$ARTICLE" \
  --inject-html

# 7. Visual QA: открыть cover.png и inline-01..03.png.
#    Split PASS проверяет геометрию, но НЕ стиль. Если inline выглядит как
#    plain whiteboard/minimal SaaS без Excalibur collage layer — COVER STYLE BLOCKER и перегенерация.
```

---

## Kie API `gpt-image-2-image-to-image`

```json
{
  "model": "gpt-image-2-image-to-image",
  "input": {
    "prompt": "<из quad-mcp-batch.json jobs[0].mcp_args.prompt>",
    "input_urls": ["<blog-hero.json reference_url_hosted>"],
    "aspect_ratio": "16:9",
    "resolution": "2K"
  }
}
```

Запуск:

```bash
python scripts/excalibur_blog_kie_gpt_image2_api.py --article-dir "$ARTICLE"
python scripts/excalibur_blog_quad_apply.py --article-dir "$ARTICLE" --inject-html
```

Перед вызовом: убедиться, что `KIE_API_KEY` задан в Cloud Secrets/env, batch пересобран текущим run, `input_urls` не пуст. Без `input_urls` → **❌ COVER HERO BLOCKER**.

### Async/timeout policy

Правильный image-tool контракт для Cursor Cloud: **async HTTP API**, а не один длинный sync MCP call.

Основной flow:

1. `scripts/excalibur_blog_kie_gpt_image2_api.py` читает `cover/quad-mcp-batch.json`.
2. `POST /api/v1/jobs/createTask` возвращает `taskId` быстро.
3. Скрипт пишет `cover/kie-image-task.json` и polling'ом вызывает `GET /api/v1/jobs/recordInfo?taskId=...`.
4. При `state=success` достаёт `resultJson.resultUrls[0]` и пишет `cover/quad-mcp-result.json`.
5. `excalibur_blog_quad_apply.py` скачивает URL из `quad-mcp-result.json`, режет и inject'ит HTML.

Ключ API: только env `KIE_API_KEY`; не сохранять в handoff, PR, article files или terminal output.

Legacy MCP fallback:

Если прямой Kie API недоступен, можно использовать MCP flow:

1. Найти в Cursor `Available Tools` image async tools на сервере `user-mcp-kv`: create/start tool + status/result tool.
2. Вызвать create/start **один раз** с arguments из `jobs[0].mcp_args`; получить `task_id`.
3. Проверять status/result tool по `task_id` каждые 10–15 секунд, пока не появится `url`.
4. Записать `url` в `cover/quad-mcp-result.json` или передать URL напрямую в `quad_apply`.

Если доступен только sync `gpt-image-2`, вызвать его один раз. `gpt-image-2` в Cloud может работать дольше HTTP timeout клиента. Если sync MCP tool call вернул:

```text
HTTP MCP tool execution failed: MCP error -32001: Request timed out
```

Это **не** означает, что генерация невозможна. Это означает, что Cursor MCP client оборвал длинный call раньше, чем backend вернул URL. Cover-агент обязан:

1. Проверить, что это именно `-32001 Request timed out`, а не ошибка schema/auth/input.
2. Не искать URL в `cover/*` или других article files: при timeout `quad-mcp-result.json` ещё не существует, пока агент сам не запишет URL.
3. Проверить expanded MCP tool response / Cursor MCP Logs: если там уже появился generated image URL, это **успех**, а не blocker.
4. Если в логе есть `task_id`, но нет URL, использовать status/result MCP tool, если он доступен.
5. Если нет URL, нет `task_id` и нет status/result tool — остановиться с `COVER MCP ASYNC BLOCKER`: MCP backend должен вернуть `task_id` быстро и дать отдельный status/result tool. Не повторять sync create вслепую.

Важно: MCP-вызов выполняется **только** как legacy fallback. Основной Cloud path — прямой Kie API script.

Запрещено после первого timeout:

- писать `COVER BLOCKER`;
- запускать 4 отдельных генерации;
- запускать повторную генерацию, если URL уже виден в MCP/Cloud log;
- повторять sync `gpt-image-2` после client timeout, если нет явного статуса, что предыдущий job не создан;
- делать split/apply без URL;
- пропускать cover и передавать pipeline дальше.

---

## quad-manifest.json — что заполняет агент

```json
{
  "cover_hook": "провокация для клика",
  "slots": {
    "cover": {
      "meme_caption_ru": "2–6 слов кириллицей",
      "scene_hint": "лицо reference + белое плотное худи + новая поза/жест/ракурс + fake скрины + мемы + белый фон + без наушников/headset/earbuds",
      "alt": "осмысленный alt"
    },
    "inline_1": {
      "h2_anchor": "точный текст H2 из article.html",
      "visual_type": "comparison_table_ui | workflow_diagram | ...",
      "scene_hint": "конкретика секции",
      "alt": "..."
    }
  }
}
```

Типы inline: `memory/cover/inline-visual-types.json`  
Автовыбор H2→type: `excalibur_blog_quad_manifest.py`

---

## Design code (открываемость)

`memory/cover/cover-design-code.json` + `memory/cover/quad-style-digital-meme-collage-ru.json`

Cover panel:

- fake Wordstat / Metrica / Telegram / отзывы
- чистый белый фон `#FFFFFF` для cover и inline; без beige/gray/grunge background
- typography как DESIGN.md-референс: жирный condensed Cyrillic, ротация hot-акцентов (hot pink / hot purple / другие), sticker labels, brush bubbles, handwritten notes; без price badges
- рваная бумага, скотч, розовые стикеры, маркер
- визуальные meme reaction cutouts (не один шаблон на весь холст): facepalm, кот/реакция, rough-edge visual cutout; не навязывать сленговые слова
- видимый текст стикеров/мемов без токсичности и оскорблений (`лох`, `лохов`, `для лохов` и похожие ярлыки запрещены)
- формат **16:9 widescreen**, не vertical carousel 9:16

---

## Fragment (обязательно)

Записать `.cursor/excalibur-blog-fragments/cover.md`:

```markdown
=== EXCALIBUR BLOG COVER ===
topic_id: {ID}
status: ✅ | ❌
article_dir: {path}
pipeline: quad_canvas_1x_image_api
image_mode: image-to-image
reference_url: {url}
canvas: cover/canvas-quad.png
cover: cover/cover.png | alt: ...
inline: inline-01..03 + h2_anchor + visual_type
registry: cover/cover-registry.json
inject_html: ok | skip
blockers: none | ...
summary: ...
```

---

## Blockers


| Код                | Причина                                             |
| ------------------ | --------------------------------------------------- |
| COVER HERO BLOCKER | нет `reference_url_hosted` или image call без `input_urls` |
| KIE API BLOCKER | нет `KIE_API_KEY`, createTask/recordInfo fail, polling timeout или нет resultUrls |
| QUAD SPLIT BLOCKER | нет canvas / не 2×2 16:9 / нет alt в manifest       |
| COVER BLOCKER      | 4 отдельных image jobs                              |
| COVER BLOCKER      | inline с героем вместо UI/схемы                     |
| COVER BLOCKER      | cover без hook / meme_caption_ru                    |
| COVER STYLE BLOCKER | после визуальной проверки PNG inline выглядит как plain whiteboard/minimal SaaS, без рваной бумаги/скотча/розового стикера/маркерной пометки/визуального meme cutout |
| COVER MCP TIMEOUT BLOCKER | async status/result tool подтвердил failed/no result или повторный timeout уже в status/result flow |
| COVER MCP RECOVERY NEEDED | после timeout агент не имеет доступа к MCP/Cursor log, где виден generated URL; нужен URL из лога, повторять генерацию вслепую нельзя |
| COVER MCP ASYNC BLOCKER | sync `gpt-image-2` обрывается по client timeout, а MCP server не даёт `task_id` и отдельный status/result tool для получения позднего URL |


---

## Скрипты (канон)


| Скрипт                                 | Назначение                          |
| -------------------------------------- | ----------------------------------- |
| `excalibur_blog_hero_reference_url.py` | keeps `reference_url_hosted` (preferred: WordPress media URL) |
| `excalibur_blog_quad_manifest.py`      | `cover/quad-manifest.json`          |
| `excalibur_blog_cover_quad_prompt.py`  | prompt + `--write-batch`            |
| `excalibur_blog_quad_apply.py`         | download URL → split → inject       |
| `excalibur_blog_cover_quad_split.py`   | split only (вызывается из apply)    |


## Deprecated — не использовать

- `excalibur_blog_visual_prompts.py`
- `excalibur_blog_visual_apply.py`
- `excalibur_blog_visual_manifest.py`

---

## Справочные memory-файлы

- `memory/cover/blog-hero.json`
- `memory/cover/cover-design-code.json`
- `memory/cover/inline-visual-types.json`
- `memory/cover/quad-style-digital-meme-collage-ru.json`
- `shared/blog-visual-pipeline-contract.md` → redirect на quad contract

