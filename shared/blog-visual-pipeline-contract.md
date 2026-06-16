# Excalibur BLOG — Visual Pipeline

Канонический контракт: **`shared/blog-cover-quad-canvas-contract.md`**

- **1 MCP** → quad canvas 2×2 → split
- Cover (top-left): герой + reference `input_urls`
- Inline 1–3: полезные визуалы по `visual_type` (не мемы с ведущим)

Скрипты `excalibur_blog_visual_prompts.py` / `visual_apply.py` / `visual_manifest.py` — **ошибочный эксперiment, не использовать**.

Используй:

- `excalibur_blog_hero_reference_url.py`
- `excalibur_blog_quad_manifest.py`
- `excalibur_blog_cover_quad_prompt.py --write-batch`
- `excalibur_blog_quad_apply.py`
