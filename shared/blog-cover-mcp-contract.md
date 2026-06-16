# Excalibur BLOG — Blog Cover MCP Contract

**Актуальный контракт:** `shared/blog-cover-quad-canvas-contract.md`

## MCP

- Tool: `gpt-image-2` (`user-mcp-kv`)
- **Один** вызов на статью → `cover/canvas-quad.png`
- **Обязательно:** `input_urls: [blog-hero.json → reference_url_hosted]`
- Перед MCP всегда пересобрать `quad-mcp-batch.json`; не использовать старый article artifact
- Hard gate: `example.com` reference, prompt <= 3500 chars, `resolution: 2K`
- Split → `cover/cover.png` + `inline-01..03.png`
- Registry: `cover/cover-registry.json`

## Agent + skill

- `agents/excalibur-blog-cover.md`
- `skills/cover-excalibur-blog/SKILL.md`

## Blockers

- MCP без `input_urls`
- 4 отдельных MCP
- freestyle без `quad-manifest.json`

Методология design code: `memory/cover/cover-design-code.json`
