# Excalibur BLOG — incident memory and fixer loop

This contract prevents the same pipeline failure from being paid for with tokens again and again.

## Canonical files

| File | Purpose |
|------|---------|
| `memory/pipeline-fix-queue.md` | durable incident memory visible to the Director and fixer |
| `agents/excalibur-blog-fixer.md` | fixer agent contract |
| `skills/fixer-excalibur-blog/SKILL.md` | detailed fixer runbook |
| `shared/agent-pipeline-pitfalls.md` | stable lessons that should be known before every run |

Runtime handoff/fragments remain runtime-only. Durable repeatable problems go to `memory/pipeline-fix-queue.md`.

## When any agent must write an incident

Every Excalibur BLOG agent must append an incident when it encounters any of these:

- blocker, timeout, tool/API auth failure, schema mismatch, missing dependency or missing env var;
- retry loop, manual workaround, fallback path, or non-obvious recovery;
- generated artifact had to be rewritten because a contract was unclear or wrong;
- agent discovered stale docs/instructions/scripts that made it waste steps;
- validation failed and the agent had to infer a fix not already documented;
- user correction revealed that the prompt/contract was too rigid or ambiguous.

Do not write incidents for normal expected PASS checks with no corrective action.

## Incident block format

Append to `memory/pipeline-fix-queue.md`:

```markdown
## INC-YYYYMMDD-HHMM-<role>-<short-slug>
status: open
run_date: YYYY-MM-DD
role: excalibur-blog-<role>
topic_id: Bxx | n/a
article_dir: memory/blog/articles/<topic_id>-<slug> | n/a
severity: low | medium | high | blocker
category: prompt | script | docs | env | api | handoff | qa | publish | other

### What went wrong
- ...

### How the agent recovered this run
- ...

### Durable fix needed before next run
- ...

### Suggested files to inspect/change
- `path/to/file`

### Secrets
- none recorded

### Fixer resolution
- pending
```

## Agent end-of-task duty

At the end of each task, the agent must include one line in its handoff/fragment:

```text
incident_report: none
```

or:

```text
incident_report: memory/pipeline-fix-queue.md#INC-YYYYMMDD-HHMM-role-slug
```

Never include secrets, tokens, private URLs, absolute Windows/macOS paths, or raw credentials in the incident memory.

## Director duty

After `=== EXCALIBUR BLOG (PIPELINE DONE) ===` or after a terminal blocker, the Director must:

1. Read `memory/pipeline-fix-queue.md`.
2. If there are `status: open` incidents from the current run, launch `Task(excalibur-blog-fixer)`.
3. If typed Task is unavailable, launch a separate `Task(generalPurpose)` with:
   - `.cursor/agents/excalibur-blog-fixer.md`
   - `.cursor/skills/fixer-excalibur-blog/SKILL.md`
   - this contract path.
4. Do not start a new article run while current-run blocker incidents remain open, unless the user explicitly says to skip the fixer loop.

## Fixer duty

The fixer agent converts incident reports into repository changes so the next run avoids the same failure:

- change durable sources only: `agents/`, `.cursor/agents/`, `skills/`, `.cursor/skills/`, `shared/`, `scripts/`, templates, stable `memory/` configs;
- prefer fixing the contract/script/prompt that caused the failure, not just the one article artifact;
- run targeted validation after edits;
- mark each handled incident as `status: fixed` with summary, files changed, checks run, and commit hash if available;
- if no safe durable fix exists, mark `status: needs-human` with the exact missing decision or secret/env setup.

Fixer must not publish, must not create or edit runtime handoff/fragments as final artifacts, and must not expose secrets.
