# Cover system — Excalibur BLOG

Канон: **`shared/blog-cover-quad-canvas-contract.md`**

## Pipeline

`quad_canvas_1x_mcp` — **1** MCP → canvas 2048×1152 → split 4×16:9 (1200×675 outputs). Prompt compact: one shared style lock + four short panel briefs. Hard gate: fresh batch, `example.com` reference, prompt <= 3500 chars, resolution 2K.

## Техника

- **MCP:** `user-mcp-kv` / `gpt-image-2` с **`input_urls`** (reference hero)
- **Aspect:** 16:9 (canvas и каждая панель)
- **Hero:** reference = лицо; одежда = агент
- **Design code:** `memory/cover/cover-design-code.json`

## Скрипты

```bash
python scripts/excalibur_blog_hero_reference_url.py
python scripts/excalibur_blog_quad_manifest.py --article-dir ... --merge
python scripts/excalibur_blog_cover_quad_prompt.py --article-dir ... --write-batch
# ONE MCP
python scripts/excalibur_blog_quad_apply.py --article-dir ... --url ... --inject-html
```

## QA

- Pillow decode PNG
- alt в `cover-registry.json` для cover + 3 inline
- Cover: hook + meme_caption_ru + fake скрины (design code)
- Inline: visual_type, без лица героя
- **Не** 4 отдельных MCP

## Legacy

`cover-concept.json` (single cover, no text) — устарел для quad pipeline. Style: `quad-style-digital-meme-collage-ru.json`.
