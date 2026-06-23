# Excalibur BLOG — Cover Agent: карта файлов

Для `Task(excalibur-blog-cover)`. Полный runbook: **`agents/excalibur-blog-cover.md`**.

## Читать первым

1. `agents/excalibur-blog-cover.md`
2. `skills/cover-excalibur-blog/SKILL.md`
3. `shared/blog-cover-quad-canvas-contract.md`
4. `shared/kie-gpt-image-api-contract.md`

## Memory (глобально)

| Файл | Назначение |
|------|------------|
| `memory/cover/blog-hero.json` | visual_lock, outfit_rule, reference_url_hosted |
| `memory/cover/assets/blog-hero-reference.png` | эталон лица |
| `memory/cover/cover-design-code.json` | human hook collage, fake скрины |
| `memory/cover/quad-style-digital-meme-collage-ru.json` | style preset |
| `memory/cover/inline-visual-types.json` | типы inline-панелей |
| `memory/brief/site-brief.md` | blog_hero, правила обложки |
| `memory/cover/cover-system.md` | краткая техника |

## Per-article (`<article_dir>/cover/`)

| Файл | Кто пишет |
|------|-----------|
| `quad-manifest.json` | агент (+ `quad_manifest.py --merge`) |
| `quad-mcp-prompt.txt` | `cover_quad_prompt.py` |
| `quad-mcp-batch.json` | `cover_quad_prompt.py --write-batch` |
| `kie-image-task.json` | `kie_gpt_image2_api.py` |
| `quad-mcp-result.json` | `kie_gpt_image2_api.py` (legacy filename) |
| `canvas-quad.png` | image API result (ONE job) |
| `cover.png`, `inline-01..03.png` | `quad_apply.py` / split |
| `cover-registry.json` | split |
| `quad-split-report.json` | split |

## Скрипты (порядок)

```bash
python scripts/excalibur_blog_hero_reference_url.py
python scripts/excalibur_blog_quad_manifest.py --article-dir ... --merge
python scripts/excalibur_blog_cover_quad_prompt.py --article-dir ... --write-batch
# Hard gate: fresh batch only; reference_url_hosted contains mayai.ru; validation.prompt_chars <= 3500; resolution == 2K.
# If the batch has files.catbox.moe, 1K, or a long prompt, regenerate/fail before image API.
# Primary Cloud image call: KIE_API_KEY env -> createTask -> recordInfo polling -> quad-mcp-result.json.
python scripts/excalibur_blog_kie_gpt_image2_api.py --article-dir ...
python scripts/excalibur_blog_quad_apply.py --article-dir ... --inject-html
```

## Handoff out

`.cursor/excalibur-blog-fragments/cover.md` — шаблон в agent-md.

## Deprecated

`excalibur_blog_visual_*.py` — не использовать.

## Эталон

`memory/blog/articles/B01-primer-seo-stati/cover/`
