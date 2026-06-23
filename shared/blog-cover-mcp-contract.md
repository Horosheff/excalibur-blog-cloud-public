# Excalibur BLOG — Blog Cover Image API Contract

**Актуальный контракт:** `shared/blog-cover-quad-canvas-contract.md`

## Primary Cloud flow: Kie API

- Script: `scripts/excalibur_blog_kie_gpt_image2_api.py`
- Auth: `KIE_API_KEY` из Cloud Secrets/env, не коммитить и не печатать
- API: `createTask` → `taskId`, затем `recordInfo?taskId=...` до `state=success`
- **Одна** генерация на статью → `cover/canvas-quad.png`
- **Обязательно:** `input_urls: [blog-hero.json → reference_url_hosted]`
- Перед API всегда пересобрать `quad-mcp-batch.json`; не использовать старый article artifact
- Hard gate: `mayai.ru` reference, prompt <= 3500 chars, `resolution: 2K`
- Result URL: `cover/quad-mcp-result.json` (legacy filename, используется `quad_apply`)
- Split → `cover/cover.png` + `inline-01..03.png`
- Registry: `cover/cover-registry.json`

## Legacy MCP fallback

- Tool: `gpt-image-2` (`user-mcp-kv`)
- Только если прямой Kie API недоступен
- Cursor Cloud sync MCP 2K i2i может упасть по `-32001 Request timed out`
- После timeout не повторять sync create вслепую; нужен URL/task_id/status tool

## Agent + skill

- `agents/excalibur-blog-cover.md`
- `skills/cover-excalibur-blog/SKILL.md`

## Blockers

- API/MCP без `input_urls`
- нет `KIE_API_KEY` в Cloud Secrets/env
- 4 отдельных image jobs
- freestyle без `quad-manifest.json`

Методология design code: `memory/cover/cover-design-code.json`
