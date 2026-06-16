# Excalibur BLOG Cloud Public Template

Public sanitized template of the Excalibur BLOG Cloud pipeline for Cursor Cloud Agents.

Private runtime data, generated articles, images, publication logs, credentials, real website URLs, and private author identity are intentionally not included.

## Setup

1. Copy `.env.example` values to your private environment or Cursor Cloud Secrets.
2. Replace `memory/brief/site-brief.md`, `memory/brief/conversion-map.md`, `shared/authors-registry.json`, and `memory/cover/blog-hero.json`.
3. Run `python3 -m pip install -r requirements.txt && python3 scripts/excalibur_blog_doctor.py`.
4. Use `CLOUD-AUTOMATION.md` as the Cursor Cloud automation prompt.

## Security

Do not commit real secrets, generated publication artifacts, private reference images, or local handoff files.
