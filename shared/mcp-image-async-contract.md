# MCP Image Async Contract

Для image generation в Cursor Cloud нельзя полагаться на один долгий sync MCP call: Cursor MCP client может оборвать соединение раньше, чем backend дождётся Kie.ai.

## Required tools

Рекомендуемый контракт для `user-mcp-kv`:

1. `gpt-image-2-create` / `gpt-image-2-start`
   - input: тот же JSON, что у sync `gpt-image-2` (`prompt`, `input_urls`, `aspect_ratio`, `resolution`)
   - output за короткое время: `{ "task_id": "...", "status": "queued|running" }`
   - должен быть idempotent по `request_id`/hash prompt+input_urls, чтобы агент не создавал дубли

2. `gpt-image-2-status` / `gpt-image-2-result`
   - input: `{ "task_id": "..." }`
   - output: `{ "status": "queued|running|succeeded|failed", "url": "...", "error": "..." }`
   - агент вызывает каждые 10–15 секунд до `status=succeeded` и `url`

## Agent rule

Cover agent:

- предпочитает async tools, если они есть в Cursor `Available Tools`;
- sync `gpt-image-2` вызывает только один раз, если async tools недоступны;
- после `HTTP MCP -32001 Request timed out` не делает blind retry sync create;
- если нет `url`, `task_id` и status/result tool — возвращает `COVER MCP ASYNC BLOCKER`.

## Why

`KIE_IMAGE_MAX_WAIT_SECONDS` и nginx `proxy_read_timeout` не гарантируют, что Cursor MCP client будет держать один tool call так же долго. Async start/status/result убирает зависимость от длинного соединения и позволяет агенту получить URL через время без дублей.
