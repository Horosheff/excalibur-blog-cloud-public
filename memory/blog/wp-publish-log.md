# Excalibur BLOG — WP publish log

## 2026-06-11 — B02 avtomatizaciya-n8n-ai-agents

| Field | Value |
|-------|-------|
| topic_id | B02 |
| slug | avtomatizaciya-n8n-ai-agents |
| verdict | **FAIL** |
| post_id | — |
| permalink | — |

### Preconditions

- article-qa.md: PASS (93/100)
- link-verify.json: pass
- schema.jsonld: present
- cover/cover.png + alt: present
- EXCALIBUR_BLOG_ALLOW_PUBLISH: yes

### Attempt

```bash
python scripts/excalibur_blog_wp_publish.py --article-dir memory/blog/articles/B02-avtomatizaciya-n8n-ai-agents --dry-run  # OK
python scripts/excalibur_blog_wp_publish.py --article-dir memory/blog/articles/B02-avtomatizaciya-n8n-ai-agents       # FAIL
```

### Blockers

1. **Network:** HTTPS к `[REDACTED]:443` недоступен из локальной среды (WinError 10060). Legacy upload path was available locally, HTTP bootstrap trigger was not.
2. **SSH path:** аккаунт `***_blog` видит только `/index.php` + `/cgi-bin/`, **без** `wp-load.php`. WordPress на `[REDACTED]/blog/` — другой document root.
3. **Bootstrap 404:** загруженный `excalibur-blog-publish-once.php` (и тестовый `excalibur-test-once.php`) отдают HTTP 404 снаружи, хотя `index.php` в том же SSH root отдаётся на главной.

### Cleanup

Временные bootstrap-файлы удалены после диагностики.

### Next steps (для оператора)

1. Обновить `memory/site.env.local`: SSH_USER/SSH_PASS + `SSH_ROOT=/` (корень SSH после login, где `wp-load.php`). Путь панели хостинга: `SSH_PANEL_PATH=/your-account.beget.tech/public_html/`.
2. Либо запустить publish с машины/сети, где `curl [REDACTED]` отвечает < 5 с.
3. Альтернатива: WP Application Password + REST API / MCP WordPress blob publish.

---

## 2026-06-11 (retry) — B02 avtomatizaciya-n8n-ai-agents — **PASS**

| Field | Value |
|-------|-------|
| topic_id | B02 |
| slug | avtomatizaciya-n8n-ai-agents |
| verdict | **PASS** |
| post_id | 13324 |
| featured_image_id | 13325 |
| permalink | [REDACTED]/avtomatizaciya-n8n-ai-agents/ |
| SSH_ROOT | `/` |

### Fix applied

- Обновлены SSH credentials в `memory/site.env.local` (локально, не в git)
- `SSH_ROOT=/` (wp-load.php в корне аккаунта после login)
- `excalibur_blog_wp_publish.py` — поддержка `SSH_ROOT` из env

### Result

```
OK post=13324 slug=avtomatizaciya-n8n-ai-agents
OK featured_image=13325
OK schema_meta=1
permalink=[REDACTED]/avtomatizaciya-n8n-ai-agents/
```

---

## 2026-06-11 — B03 podklyuchenie-mcp-cursor — **PASS**

| Field | Value |
|-------|-------|
| topic_id | B03 |
| slug | podklyuchenie-mcp-cursor |
| verdict | **PASS** |
| post_id | 13335 |
| featured_image_id | 13336 |
| inline_images | 13337, 13338, 13339 |
| permalink | [REDACTED]/podklyuchenie-mcp-cursor/ |
| trigger | `/excalibur-blog-run topic_id: B03 publish: yes` (publish вручную после fix оркестратора) |

### Result

```
OK post=13335 slug=podklyuchenie-mcp-cursor
OK featured_image=13336
OK schema_meta=1
OK inline_image_upload=13337 src=cover/inline-01.png
OK inline_image_upload=13338 src=cover/inline-02.png
OK inline_image_upload=13339 src=cover/inline-03.png
permalink=[REDACTED]/podklyuchenie-mcp-cursor/
```

---

## 2026-06-11 — B04 geo-optimizaciya-sajta-2026 — **PASS**

| Field | Value |
|-------|-------|
| topic_id | B04 |
| slug | geo-optimizaciya-sajta-2026 |
| verdict | **PASS** |
| post_id | 13361 |
| featured_image_id | 13362 |
| inline_images | 13363, 13364, 13365 |
| permalink | [REDACTED]/geo-optimizaciya-sajta-2026/ |
| trigger | `/excalibur-blog-run topic_id: B04 publish: yes` |

### Preconditions

- article-qa.md: PASS (94/100)
- link-verify.json: pass (5/5)
- schema.jsonld: present
- cover/cover.png + alt: present
- EXCALIBUR_BLOG_ALLOW_PUBLISH: yes

### Result

```
OK post=13361 slug=geo-optimizaciya-sajta-2026
OK featured_image=13362
OK schema_meta=1
OK skip_theme_faq_meta=1
OK inline_image_upload=13363 src=cover/inline-01.png url=[REDACTED]/wp-content/uploads/2026/06/geo-optimizaciya-sajta-2026-inline-01.jpg
OK inline_image_upload=13364 src=cover/inline-02.png url=[REDACTED]/wp-content/uploads/2026/06/geo-optimizaciya-sajta-2026-inline-02.jpg
OK inline_image_upload=13365 src=cover/inline-03.png url=[REDACTED]/wp-content/uploads/2026/06/geo-optimizaciya-sajta-2026-inline-03.jpg
permalink=[REDACTED]/geo-optimizaciya-sajta-2026/
```

### Post-publish

- interlinker --apply: 0 new opportunities (B01 inbound already applied at indexer step)

---

## 2026-06-11 — B05 avtonomnyj-kontent-zavod-nejroseti — **PASS**

| Field | Value |
|-------|-------|
| topic_id | B05 |
| slug | avtonomnyj-kontent-zavod-nejroseti |
| verdict | **PASS** |
| post_id | 13369 |
| featured_image_id | 13370 |
| inline_images | 13371, 13372, 13373 |
| permalink | [REDACTED]/avtonomnyj-kontent-zavod-nejroseti/ |
| trigger | `/excalibur-blog-run topic_id: B05 publish: yes` |

### Preconditions

- article-qa.md: PASS (95/100)
- link-verify.json: pass (5/5)
- schema.jsonld: present
- cover/cover.png + alt: present
- EXCALIBUR_BLOG_ALLOW_PUBLISH: yes

### Result

```
OK post=13369 slug=avtonomnyj-kontent-zavod-nejroseti
OK featured_image=13370
OK schema_meta=1
OK skip_theme_faq_meta=1
OK inline_image_upload=13371 src=cover/inline-01.png url=[REDACTED]/wp-content/uploads/2026/06/avtonomnyj-kontent-zavod-nejroseti-inline-01.jpg
OK inline_image_upload=13372 src=cover/inline-02.png url=[REDACTED]/wp-content/uploads/2026/06/avtonomnyj-kontent-zavod-nejroseti-inline-02.jpg
OK inline_image_upload=13373 src=cover/inline-03.png url=[REDACTED]/wp-content/uploads/2026/06/avtonomnyj-kontent-zavod-nejroseti-inline-03.jpg
permalink=[REDACTED]/avtonomnyj-kontent-zavod-nejroseti/
```

---

## 2026-06-16 — B06 make-ai-agents-mcp-avtomatizaciya — **BLOCKER**

| Field | Value |
|-------|-------|
| topic_id | B06 |
| slug | make-ai-agents-mcp-avtomatizaciya |
| verdict | **BLOCKER** |
| post_id | — |
| permalink | — |

### Preconditions (local)

- article-qa.md: PASS (94/100)
- link-verify.json: pass (3/3, re-run preflight 2026-06-16)
- schema.jsonld: present
- cover/cover.png + alt: present
- dry-run: OK (slug, title, PHP bytes 8037450)

### Blocker

`EXCALIBUR_BLOG_ALLOW_PUBLISH != yes` — Cursor Cloud Secrets / env vars не инжектированы в VM:

- `memory/site.env.local` отсутствует
- `python3 scripts/excalibur_blog_doctor.py --publish` → FAIL (PUBLIC_SITE_URL, SSH_*, ALLOW_PUBLISH)

### Attempt

```bash
python3 scripts/excalibur_blog_link_verify.py ... --site-base [REDACTED]  # pass
python3 scripts/excalibur_blog_wp_publish.py --article-dir ... --dry-run        # OK
python3 scripts/excalibur_blog_wp_publish.py --article-dir ...                # BLOCKER
```

### Next steps (оператор)

1. Добавить в Cursor Dashboard → Cloud Agents → Secrets: `PUBLIC_SITE_URL`, `SSH_*`, `SSH_ROOT`, `EXCALIBUR_BLOG_ALLOW_PUBLISH=yes`
2. Перезапустить `excalibur-blog-publish` для B06
3. Либо создать `memory/site.env.local` локально и publish с машины оператора

---

## 2026-06-16 (retry) — B06 make-ai-agents-mcp-avtomatizaciya — **PASS** (MCP)

| Field | Value |
|-------|-------|
| topic_id | B06 |
| slug (planned) | make-ai-agents-mcp-avtomatizaciya |
| slug (actual) | avtomatizacziya-make-s-ai-agents-i-mcp-workflow-dlya-biznesa |
| verdict | **PASS** (content live; images/schema pending) |
| post_id | 13467 |
| permalink | [REDACTED]/avtomatizacziya-make-s-ai-agents-i-mcp-workflow-dlya-biznesa/ |
| method | mcp-kv (`wordpress_content_blob_append` → `wordpress_create_post_from_blob`) |
| featured_image | pending |
| inline_images | pending (cover/inline-01..03.png) |
| schema_meta | pending |

### Context

- legacy upload blocked from Cloud VM: `425 Bad IP` (Beget)
- `memory/site.env.local` present locally with `EXCALIBUR_BLOG_ALLOW_PUBLISH=yes`
- Preflight link-verify: pass (3/3)

### Result

```
OK post=13467 (MCP create)
permalink=[REDACTED]/avtomatizacziya-make-s-ai-agents-i-mcp-workflow-dlya-biznesa/
featured_image=pending (no MCP media upload tool)
inline_images=pending
schema_meta=pending (_excalibur_blog_schema_jsonld, _excalibur_blog_skip_theme_faq)
slug_custom=pending (MCP update_post_from_blob has no slug param)
```

### Follow-up (оператор)

1. С машины с рабочим SSH: `python3 scripts/excalibur_blog_wp_publish.py --article-dir memory/blog/articles/B06-make-ai-agents-mcp-avtomatizaciya` — обновит post 13467 (slug, images, schema meta) или создаст дубль если slug не совпадёт — проверить вручную.
2. Либо в WP Admin: slug → `make-ai-agents-mcp-avtomatizaciya`, загрузить cover + inline, вставить schema meta.

---

## 2026-06-16 (SSH retry) — B06 make-ai-agents-mcp-avtomatizaciya — **PASS**

| Field | Value |
|-------|-------|
| topic_id | B06 |
| slug | make-ai-agents-mcp-avtomatizaciya |
| verdict | **PASS** |
| post_id | 13467 |
| featured_image_id | 13469 |
| permalink | [REDACTED]/make-ai-agents-mcp-avtomatizaciya/ |
| transport | SSH fallback (legacy upload `425 Bad IP` → SSH upload OK) |

### Result

```
OK post=13467 slug=make-ai-agents-mcp-avtomatizaciya
OK featured_image=13469
OK schema_meta=1
OK skip_theme_faq_meta=1
OK inline_image_upload=13470..13472
permalink=[REDACTED]/make-ai-agents-mcp-avtomatizaciya/
```

Historical note: this run used SSH fallback after legacy upload was blocked.

## 2026-06-16 (SSH direct transport) — publish script update

`scripts/excalibur_blog_wp_publish.py` now uploads the bootstrap file directly through SSH and deletes it through SSH after the HTTP trigger. Agents must not attempt SSH upload from Cursor Cloud. `SSH_*` env names remain supported only as compatibility aliases for existing Cursor Secrets.

---

## 2026-06-16 — B07 postroenie-rag-sistemy-vektornaya-baza — **PASS**

| Field | Value |
|-------|-------|
| topic_id | B07 |
| slug | postroenie-rag-sistemy-vektornaya-baza |
| verdict | **PASS** |
| post_id | 13484 |
| featured_image_id | 13485 |
| permalink | [REDACTED]/postroenie-rag-sistemy-vektornaya-baza/ |
| transport | SSH direct (`SSH_ROOT=` — panel path invalid on SSH cwd) |

### Preconditions

- article-qa.md: PASS (93/100)
- link-verify.json: pass (3/3)
- schema.jsonld: present
- cover/cover.png + alt: present
- EXCALIBUR_BLOG_ALLOW_PUBLISH: yes

### Attempt

```bash
python3 scripts/excalibur_blog_link_verify.py ... --site-base [REDACTED]  # pass
python3 scripts/excalibur_blog_wp_publish.py --article-dir ... --dry-run        # OK (PHP bytes: 7834916)
SSH_ROOT= python3 scripts/excalibur_blog_wp_publish.py --article-dir ...  # PASS
python3 scripts/excalibur_blog_interlinker.py --apply ...  # 0 opportunities
```

### Result

```
OK post=13484 slug=postroenie-rag-sistemy-vektornaya-baza
OK featured_image=13485
OK schema_meta=1
OK skip_theme_faq_meta=1
OK inline_image_upload=13486..13488 (inline-01..03.png → wp-content/uploads/2026/06/*.jpg)
permalink=[REDACTED]/postroenie-rag-sistemy-vektornaya-baza/
```

### Note

Configured `SSH_ROOT` (panel path) does not exist on SSH; default cwd is already `public_html` with `wp-load.php`. Publish succeeded with empty `SSH_ROOT`. Recommend updating Cursor Secret `SSH_ROOT` to empty or `.` for Cloud runs.

---

## 2026-06-16 — B08 ii-chat-bot-dlya-biznesa-workflow — **PASS**

| Field | Value |
|-------|-------|
| topic_id | B08 |
| slug | ii-chat-bot-dlya-biznesa-workflow |
| verdict | **PASS** |
| post_id | 13490 |
| featured_image_id | 13493 |
| inline_images | 13494, 13495, 13496 |
| permalink | [REDACTED]/ii-chat-bot-dlya-biznesa-workflow/ |
| transport | SSH direct (`SSH_ROOT=` empty) |

### Preconditions

- article-qa.md: PASS (90/100)
- link-verify.json: pass (6/6)
- schema.jsonld: present
- cover/cover.png + cover.webp + alt: present
- EXCALIBUR_BLOG_ALLOW_PUBLISH: yes

### Attempt

```bash
python3 scripts/excalibur_blog_link_verify.py ... --site-base [REDACTED]  # pass
python3 scripts/excalibur_blog_wp_publish.py --article-dir ... --dry-run        # OK (PHP bytes: 2821484)
SSH_ROOT= python3 scripts/excalibur_blog_wp_publish.py --article-dir ...  # PASS (post only, no inline in HTML)
# inject inline figures → re-publish
SSH_ROOT= python3 scripts/excalibur_blog_wp_publish.py --article-dir ...  # PASS (inline uploads)
python3 scripts/excalibur_blog_interlinker.py --apply ...  # 0 opportunities
```

### Result

```
OK post=13490 slug=ii-chat-bot-dlya-biznesa-workflow
OK featured_image=13493
OK schema_meta=1
OK skip_theme_faq_meta=1
OK inline_image_upload=13494 src=cover/inline-01.png
OK inline_image_upload=13495 src=cover/inline-02.png
OK inline_image_upload=13496 src=cover/inline-03.png
permalink=[REDACTED]/ii-chat-bot-dlya-biznesa-workflow/
```

### Note

First publish attempt failed: `SSH_ROOT=/` → SSH `FileNotFoundError` (panel path invalid). Retry with empty `SSH_ROOT` succeeded. Inline `<figure>` tags were missing from article.html at first publish; injected via `inject_figures` from quad-split-report, then re-published.

---

## 2026-06-16 — B09 sozdat-llms-txt-dlya-sajta — **PASS**

| Field | Value |
|-------|-------|
| topic_id | B09 |
| slug | sozdat-llms-txt-dlya-sajta |
| verdict | **PASS** |
| post_id | 13533 |
| featured_image_id | 13534 |
| inline_images | 13535, 13536, 13537 |
| permalink | [REDACTED]/sozdat-llms-txt-dlya-sajta/ |
| transport | SSH direct (`SSH_ROOT=.` root override; no SSH upload) |

### Preconditions

- article-qa.md: PASS (91/100)
- link-verify.json: pass (5/5)
- schema.jsonld: present
- cover/cover.png + cover-registry.json alt: present
- EXCALIBUR_BLOG_ALLOW_PUBLISH: yes

### Attempt

```bash
python3 scripts/excalibur_blog_link_verify.py ... --site-base [REDACTED]  # pass
python3 scripts/excalibur_blog_wp_publish.py --article-dir ... --dry-run        # OK (PHP bytes: 6208344)
python3 scripts/excalibur_blog_wp_publish.py --article-dir ...                 # failed before upload: SSH remote root ENOENT
SSH_ROOT=. python3 scripts/excalibur_blog_wp_publish.py --article-dir ...  # PASS
python3 scripts/excalibur_blog_interlinker.py --apply ...  # 0 opportunities
```

### Result

```text
OK post=13533 slug=sozdat-llms-txt-dlya-sajta
OK featured_image=13534
OK schema_meta=1
OK skip_theme_faq_meta=1
OK inline_image_upload=13535, 13536, 13537 src=cover/inline-01..03.png
permalink=[REDACTED]/sozdat-llms-txt-dlya-sajta/
```

### Note

Configured publish root path is invalid inside the SSH cwd for this Cloud run. Retrying with `SSH_ROOT=.` used the SSH login cwd as the WordPress root and succeeded. No SSH upload was attempted.

---

## 2026-06-17 — B10 ollama-lokalnaya-llm-dlya-biznesa — **PASS**

| Field | Value |
|-------|-------|
| topic_id | B10 |
| slug | ollama-lokalnaya-llm-dlya-biznesa |
| verdict | **PASS** |
| post_id | 13539 |
| featured_image_id | 13540 |
| inline_images | 13541, 13542, 13543 |
| permalink | [REDACTED]/ollama-lokalnaya-llm-dlya-biznesa/ |
| transport | SSH direct (auto root fallback to `.`; no SSH upload) |

### Preconditions

- article-qa.md: PASS (91/100)
- link-verify.json: pass (5/5)
- schema.jsonld: present
- cover/cover.png + cover-registry.json alt: present
- EXCALIBUR_BLOG_ALLOW_PUBLISH: yes

### Attempt

```bash
python3 scripts/excalibur_blog_link_verify.py ... --site-base [REDACTED]  # pass
python3 scripts/excalibur_blog_wp_publish.py --env-check                    # OK
python3 scripts/excalibur_blog_wp_publish.py --article-dir ... --dry-run  # OK (PHP bytes: 6518484)
python3 scripts/excalibur_blog_wp_publish.py --article-dir ...            # PASS (SSH root ENOENT → fallback `.`)
python3 scripts/excalibur_blog_interlinker.py --apply ...                   # 0 opportunities
```

### Result

```text
OK post=13539 slug=ollama-lokalnaya-llm-dlya-biznesa
OK featured_image=13540
OK schema_meta=1
OK skip_theme_faq_meta=1
OK inline_image_upload=13541, 13542, 13543 src=cover/inline-01..03.png
permalink=[REDACTED]/ollama-lokalnaya-llm-dlya-biznesa/
```

### Note

SSH configured remote root returned ENOENT; script auto-fallback to `.` succeeded on first attempt. Recommend updating `SSH_ROOT` to `.` in Cloud Secrets.
