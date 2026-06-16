# Excalibur BLOG Visual Assets MCP Policy

Этот контракт действует для всех агентов, которые проектируют, собирают или проверяют сайт.

## Главный Принцип

Агенты вольны делать всё, что нужно для production-качества визуала:

- генерировать новые визуалы через MCP KV `gpt-image-2`;
- удалять фон через MCP KV `recraft_remove_background`;
- создавать inline SVG;
- использовать CSS masks, clip-path, gradients, pseudo-elements, blend modes;
- делать section dividers, waves, blobs, overlapping layers, cutout compositions;
- готовить отдельные ассеты для mobile/tablet/desktop, если один ассет ломается.

Нельзя заменять сложный визуал generic block/card шаблоном только потому, что так проще.

Нельзя считать CSS-карточку, gradient placeholder, однотонную плашку или decorative blob заменой image-bearing зоны из референса.

## Когда Обязательно Использовать MCP KV

Используй MCP KV, если для точного дизайна нужны:

- hero/person/object/case-study image;
- cutout PNG без фона;
- сложная иллюстрация, текстура, 3D-объект, персонаж, UI-мокап;
- визуальный объект, который нельзя честно собрать CSS/SVG;
- референс требует изображения, а не абстрактной CSS-заглушки.
- один и тот же персонаж/объект повторяется в разных сценах и должен иметь разные позы/композиции.

Ожидаемые инструменты:

```text
user-mcp-kv/gpt-image-2
user-mcp-kv/recraft_remove_background
```

Если в конкретной среде exact tool name отличается, агент обязан сначала посмотреть доступные MCP KV tools и использовать ближайший инструмент Image 2 / background removal.

## Background Removal — Обязательный 2-Step Pipeline

Если объект должен быть поверх фона, градиента, hero, карточки, overlap или section transition — это **cutout asset**. Для него обязателен двухшаговый MCP pipeline:

1. **Шаг 1:** Cursor MCP tool call → выбрать `gpt-image-2` в `Available Tools` (server `user-mcp-kv`) → получить `url` (исходник с фоном).
2. **Шаг 2:** Cursor MCP tool call → выбрать `recraft_remove_background` в `Available Tools` (server `user-mcp-kv`) с `{ "image": "<url из шага 1>" }` → получить `transparent_url`.
3. В `AURA_ASSET_REGISTRY.json` записать оба URL, `requires_background_removal: true`, `background_removal_tool: "recraft_remove_background"`, `background_removal_status: "ready"`, `packaged_url: "<transparent_url>"`.
4. В тему/package/deploy скачивать **только** `packaged_url` или `transparent_url`, никогда исходный `url`.

Нельзя:

- пропускать шаг 2 и класть в тему `url` от `gpt-image-2`;
- писать “фон удалён”, пока нет реального `transparent_url` от `recraft_remove_background`;
- считать CSS `background: transparent`, checkerboard fringe или Pillow/crop/chroma key заменой MCP remove background;
- ставить `status: ready`, если cutout zone есть, а `transparent_url` пустой.

Если AURA пропустила шаг 2, Aurora обязана сама вызвать `recraft_remove_background` по `url` из registry или поставить `❌ CONTENT BLOCKER`.

### Когда cutout обязателен

`requires_background_removal: true` для:

- hero mascot/person/object over gradient/blob;
- form-side character;
- object overlap into next section;
- sticker/callout over colored band;
- любой zone из `AURA_VISUAL_INVENTORY.json` с `requires_cutout: true`.

Для flat card photos, blog thumbs и infographics без overlap cutout может быть `false`, если zone не требует прозрачности.

## Section Transitions

Если референс имеет нестандартные переходы между блоками, AURA и Aurora обязаны повторить их:

- wave divider;
- diagonal cut;
- blob overlap;
- organic mask;
- torn paper / sticker edge;
- section overlap with negative margin;
- hero image entering next section;
- gradient fade;
- custom SVG separator;
- layered cards crossing section boundaries.

Такие переходы фиксируются в:

```text
memory/design/AURA_SECTION_TRANSITIONS.json
```

## Asset Registry

Каждый visual asset должен иметь запись:

```json
{
  "id": "...",
  "type": "generated-image | removed-background | svg | css-shape | texture | section-transition",
  "source": "mcp-kv | inline-svg | css | reference",
  "tool": "gpt-image-2",
  "tools_pipeline": ["gpt-image-2", "recraft_remove_background"],
  "requires_background_removal": true,
  "background_removal_tool": "recraft_remove_background",
  "background_removal_status": "ready | pending | failed",
  "url": "...",
  "transparent_url": "...",
  "packaged_url": "...",
  "alt_text": "...",
  "used_in": ["front-page:hero"],
  "counts_as_meaningful_image": true,
  "covers_visual_zone_ids": ["hero-mascot"],
  "responsive_notes": "...",
  "status": "ready | blocker"
}
```

`packaged_url` = URL, который Aurora обязана скачать в `planned_theme_path`. Для cutout это всегда `transparent_url`.

Каждый asset обязан иметь `alt_text` (русский, осмысленный, не generic). Alt попадает в WP attachment meta и в HTML.

`AURA_ASSET_REGISTRY.json` должен покрывать required zones из `AURA_VISUAL_INVENTORY.json`. Если зона обязательна для визуальной точности, но asset ещё `pending`, это blocker, а не backlog.

Если один asset покрывает несколько zones, нужно явно объяснить `reuse_reason`. Без причины это считается схлопыванием визуальных зон и blocker.

## Local Artifact Law

После Aurora build каждый required visual asset должен существовать как локальный файл внутри темы:

```text
memory/wp/theme/<theme-slug>/assets/images/<asset>.png
```

или как другой явный файл внутри theme package (`.svg`, `.webp`, `.jpg`), если это указано в registry. Одного remote URL, live URL или tempfile URL недостаточно.

Aurora обязана:

- для каждого asset читать `AURA_ASSET_REGISTRY.json` и скачивать `packaged_url`, а если его нет — `transparent_url` при `requires_background_removal: true`, иначе `url`;
- **никогда** не скачивать исходный `url` для cutout/overlap/hero-object zones;
- если `requires_background_removal: true`, но `transparent_url` пуст — вызвать `recraft_remove_background` через MCP KV или blocker;
- скачать/сохранить MCP KV images в локальную тему;
- скачивать MCP/CDN изображения устойчиво: сначала probe `Range: bytes=0-15`, затем полный файл Range-чанками с retry и сверкой общей длины. Один полный `GET/read()` может зависать на `tempfile.aiquickdraw.com` и не является достаточным download evidence.
- проверить `file_exists` для каждого path из `inc/assets.php` / `AURA_ASSET_REGISTRY.json`;
- проверить каждый raster asset по bytes, а не по словам MCP: PNG начинается с `89 50 4E 47 0D 0A 1A 0A`, WebP начинается с `RIFF....WEBP`, JPEG с `FF D8 FF`. `content-type: image/png` и URL `.png` не являются доказательством PNG.
- выполнить decode verification (`PIL.Image.open(...).verify()` и повторный `load()`) для каждого PNG/JPEG/WebP/GIF. Если decoder падает или GET тела таймаутит/обрывается — это `ASSET_BINARY_BLOCKER`, не ready.
- если MCP/Recraft возвращает `.png` URL, но byte signature WebP, агент обязан либо пересохранить настоящий PNG после успешного декодирования, либо сохранить `.webp` с честным расширением и обновить maps/templates. Просто переименовывать WebP в `.png` запрещено.
- включить эти файлы в zip/package/deploy;
- записать `local_asset_files_status` и `missing_local_asset_files` в `site-spec.json`, `build-report.json`, `content-completeness-report.md`.

Design Guardian и QA обязаны блокировать PASS, если live URL отдаёт asset, но локальный artifact отсутствует в `memory`. Такой прогон невоспроизводим и не production-ready.

## WordPress Media Upload

MCP/tempfile URLs — только этап генерации. Production HTML обязан использовать **WordPress Media Library** (`wp-content/uploads/`), не remote links.

См. `shared/wp-media-upload-contract.md`.

Aurora после деплоя обязана:

- импортировать каждый required asset в медиатеку WP (`media_handle_sideload`, WP-CLI `wp media import` или эквивалент);
- записать `attachment_id`, `attachment_url`, `alt_text` в `memory/wp/wp-media-map.json`;
- проставить `_wp_attachment_image_alt` для каждого attachment;
- в шаблонах выводить изображения через `wp_get_attachment_image()` / theme media helper, с alt из registry/content pack;
- не оставлять в public HTML `tempfile.aiquickdraw.com` или другие MCP URLs.

## Blockers

Статус не может быть `✅`, если:

- MCP-required asset заменён CSS-заглушкой;
- source имеет image-bearing cards/form-side visuals, а итоговый сайт оставляет только один hero image;
- `meaningful_image_count` меньше `minimum_homepage_visual_assets` / `minimum_meaningful_image_assets_homepage`;
- per-page `meaningful_image_count` меньше `minimum_meaningful_image_assets` для любой selected/build page;
- несколько source image scenes закрыты одним hero image или одним strip без отдельных visual compositions;
- внутренняя selected/build page заменяет required visuals generic text blocks;
- объекту нужен прозрачный фон, но remove background не выполнен;
- cutout asset в теме скачан с `url`, хотя в registry есть `transparent_url` / `packaged_url`;
- `requires_background_removal: true`, но `transparent_url`, `packaged_url` или `background_removal_status: ready` отсутствуют;
- агент не вызвал `recraft_remove_background`, хотя zone требует cutout;
- public HTML использует remote MCP/tempfile URL вместо WP Media Library;
- `wp-media-map.json` отсутствует или `attachment_id` пуст для required asset;
- meaningful image без `alt_text` или с пустым/generic alt.
- сложный transition из референса заменён обычным прямым белым блоком;
- `AURA_ASSET_REGISTRY.json` не содержит URL/пути созданных ассетов;
- required visual asset отсутствует локально в `memory/wp/theme/<theme-slug>/assets/images/` или не попал в package/deploy;
- `inc/assets.php` ссылается на asset path, которого нет в локальной теме;
- local asset имеет расширение `.png`, но byte signature `RIFF....WEBP`, HTML/error page или unknown;
- MCP/Recraft URL имеет `content-type: image/png`, но bytes не PNG;
- asset URL существует, но тело файла не скачивается полностью и стабильно;
- агент не пробует Range-chunk download после timeout/partial read полного GET;
- raster asset не проходит Pillow verify/load;
- на mobile asset обрезается, перекрывает текст или ломает CTA;
- агент скрыл проблему словами “можно добавить позже”.

