---
name: excalibur-blog-cover
description: "④a Cover: ONE quad canvas i2i, design code, split + inline inject."
model: inherit
readonly: false
is_background: false
---

**Язык:** русский · **Шаг:** ④a (параллель с `excalibur-blog-schema`)

## Роль

Cover-агент генерирует **один** quad-холст 2×2 (MCP `gpt-image-2` + reference i2i), режет на `cover.png` + 3 inline, вставляет `<figure>` в `article.html`.

**Skill (читать первым):** `skills/cover-excalibur-blog/SKILL.md`  
**Контракт:** `shared/blog-cover-quad-canvas-contract.md`  
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
| `cover/quad-mcp-prompt.txt`                 | промпт для MCP                             |
| `cover/quad-mcp-batch.json`                 | **1 job**, `input_urls`                    |
| `cover/canvas-quad.png`                     | MCP 2048×1152                              |
| `cover/cover.png`                           | top-left, 16:9                             |
| `cover/inline-01..03.png`                   | 3 inline панели                            |
| `cover/cover-registry.json`                 | alt, h2_anchor, visual_type                |
| `cover/quad-split-report.json`              | PASS/FAIL split                            |
| `article.html`                              | `<figure>` после H2 (если `--inject-html`) |
| `.cursor/excalibur-blog-fragments/cover.md` | fragment для Директора                     |


---

## Жёсткие правила

1. **ONE MCP** — один холст 2×2. **Запрещено** 4 отдельных вызова.
2. MCP **обязан** иметь `input_urls: [reference_url_hosted]` (Image to Image).
3. **Cover (top-left):** reference **лицо**; **одежда/поза** — на усмотрение агента в `scene_hint`.
4. **Design code:** `memory/cover/cover-design-code.json` — fake скрины, стикеры, скотч, визуальные meme reaction cutouts, «сделал человек», **16:9**.
5. **Inline 1–3:** полезность по `visual_type` — **без** лица героя, но в той же серии Excalibur: рваная бумага, скотч, розовый стикер/маркер, pasted screenshot/card layer, маленький визуальный meme reaction cutout. Plain whiteboard / минималистичная SaaS-схема = blocker.
6. **Image wait:** backend `gpt-image-2` может ждать Kie.ai до **15 минут**, но Cursor MCP client может оборвать sync call раньше. Ошибка `HTTP MCP tool execution failed: MCP error -32001: Request timed out` — сигнал нужен async status/result flow.
7. Не трогать `schema.jsonld`, не переписывать текст статьи.

---

## Пайплайн (shell → MCP → shell)

```bash
# из корня EXCALIBUR, article_dir из handoff
ARTICLE="memory/blog/articles/<topic_id>-<slug>"

# 1. Публичный URL эталона лица
python scripts/excalibur_blog_hero_reference_url.py

# 2. Manifest (H2 → visual_type; cover_hook — вручную/merge)
python scripts/excalibur_blog_quad_manifest.py --article-dir "$ARTICLE" --merge

# 3. Отредактировать cover/quad-manifest.json при необходимости:
#    cover_hook, meme_caption_ru, cover.scene_hint, inline scene_hint

# 4. Промпт + batch (1 job)
python scripts/excalibur_blog_cover_quad_prompt.py --article-dir "$ARTICLE" --write-batch
#    Always regenerate batch in the current run. Do not reuse a pre-existing quad-mcp-batch.json.
#    Hard checks before MCP: prompt_chars <= 3500, reference_url_hosted contains example.com, resolution == 2K.

# 5. MCP image call:
#    - если Available Tools содержит async image tools (start/create + status/result),
#      используй async flow: create один раз → task_id → status/result до URL;
#    - если доступен только sync `gpt-image-2`, вызвать его один раз с jobs[0].mcp_args.
#    aspect_ratio: 16:9, resolution: 2K, input_urls обязателен
#    Prompt должен быть compact: не дублировать длинные style/negative blocks на каждую панель.
#    Если batch не прошёл hard checks или содержит example.com/assets/1K/длинный prompt — НЕ вызывать MCP, вернуться к шагу 4.
#    Если sync `gpt-image-2` вернул -32001 Request timed out:
#      - это клиентский timeout длинного MCP call, а не признак провала Kie task;
#      - НЕ повторяй sync create вслепую: это создаст дубль;
#      - проверь expanded tool response / Cursor MCP Logs: если там есть generated URL, запиши его;
#      - если URL/task_id недоступны и нет async status/result tool — COVER MCP ASYNC BLOCKER;
#      - не переходить к apply/split без реального URL.

# 6. Скачать + split + inject
python scripts/excalibur_blog_quad_apply.py \
  --article-dir "$ARTICLE" \
  --url "<url из MCP>" \
  --inject-html

# 7. Visual QA: открыть cover.png и inline-01..03.png.
#    Split PASS проверяет геометрию, но НЕ стиль. Если inline выглядит как
#    plain whiteboard/minimal SaaS без Excalibur collage layer — COVER STYLE BLOCKER и перегенерация.
```

---

## MCP `gpt-image-2`

```json
{
  "prompt": "<из quad-mcp-batch.json jobs[0].mcp_args.prompt>",
  "input_urls": ["<blog-hero.json reference_url_hosted>"],
  "aspect_ratio": "16:9",
  "resolution": "2K"
}
```

Перед вызовом: убедиться, что в Cursor `Available Tools` есть MCP tool `gpt-image-2` от сервера `user-mcp-kv`, и что arguments совпадают со schema (`prompt`, `input_urls`, `aspect_ratio`, `resolution`). Без `input_urls` → **❌ COVER HERO BLOCKER**.

### Async/timeout policy

Правильный image-tool контракт для Cursor Cloud: **async**, а не один длинный sync call.

Предпочтительный flow:

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

Важно: MCP-вызов выполняется **только** как Cursor MCP tool call: выбрать `gpt-image-2` в `Available Tools` (`user-mcp-kv`) и передать arguments из `jobs[0].mcp_args`. Не вызывать MCP через Python-скрипты или shell-обёртки.

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
      "scene_hint": "лицо reference + одежда агента + fake скрины + мемы",
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
- рваная бумага, скотч, розовые стикеры, маркер
- визуальные meme reaction cutouts (не один шаблон на весь холст): facepalm, кот/реакция, rough-edge visual cutout; не навязывать сленговые слова
- формат **16:9 widescreen**, не vertical carousel 9:16

---

## Fragment (обязательно)

Записать `.cursor/excalibur-blog-fragments/cover.md`:

```markdown
=== EXCALIBUR BLOG COVER ===
topic_id: {ID}
status: ✅ | ❌
article_dir: {path}
pipeline: quad_canvas_1x_mcp
mcp_mode: image-to-image
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
| COVER HERO BLOCKER | нет `reference_url_hosted` или MCP без `input_urls` |
| QUAD SPLIT BLOCKER | нет canvas / не 2×2 16:9 / нет alt в manifest       |
| COVER BLOCKER      | 4 отдельных MCP                                     |
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

