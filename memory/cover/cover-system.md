# Cover system — Excalibur BLOG

Канон: **`shared/blog-cover-quad-canvas-contract.md`**

## Pipeline

`quad_canvas_1x_image_api` — **1** Kie GPT Image 2 i2i API task → canvas 2048×1152 → split 4×16:9 (1200×675 outputs). Prompt compact: one shared style lock + four short panel briefs. Hard gate: fresh batch, `mayai.ru` reference, prompt <= 3500 chars, resolution 2K.

## Техника

- **Image API:** `scripts/excalibur_blog_kie_gpt_image2_api.py` с **`input_urls`** (reference hero), env `KIE_API_KEY`
- **Aspect:** 16:9 (canvas и каждая панель)
- **Hero:** reference = лицо; одежда = белое плотное худи heavyweight fabric; поза/жест/ракурс/выражение/реквизит/композиция каждый раз заметно разные; headphones/headset/earbuds запрещены
- **Design code:** `memory/cover/cover-design-code.json`
- **Background:** чистый белый `#FFFFFF` для cover и всех inline; без бежевого/серого/grunge-фона
- **Typography:** обложка в духе DESIGN.md-референса — жирный condensed Cyrillic, ротация hot-акцентов (hot pink, hot purple, hot blue, hot orange и другие), sticker labels, brush bubbles, handwritten notes; без price badges

## Скрипты

```bash
python scripts/excalibur_blog_hero_reference_url.py
python scripts/excalibur_blog_quad_manifest.py --article-dir ... --merge
python scripts/excalibur_blog_cover_quad_prompt.py --article-dir ... --write-batch
# ONE image API task
python scripts/excalibur_blog_kie_gpt_image2_api.py --article-dir ...
python scripts/excalibur_blog_quad_apply.py --article-dir ... --inject-html
```

## QA

- Pillow decode PNG
- alt в `cover-registry.json` для cover + 3 inline
- Cover: hook + meme_caption_ru + fake скрины (design code)
- Inline: visual_type, без лица героя
- **Не** 4 отдельных image jobs

## Legacy

`cover-concept.json` (single cover, no text) — устарел для quad pipeline. Style: `quad-style-digital-meme-collage-ru.json`.
