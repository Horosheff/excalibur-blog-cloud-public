#!/usr/bin/env python3
"""Robust image download helpers for MCP/CDN asset URLs."""
from __future__ import annotations

import re
import time
import urllib.error
import urllib.request


DEFAULT_HEADERS = {
    "User-Agent": "ExcaliburBlogAssetDownloader/1.0",
    "Cache-Control": "no-cache",
}


def _request(url: str, *, headers: dict[str, str] | None = None, timeout: int = 20) -> urllib.response.addinfourl:
    merged = dict(DEFAULT_HEADERS)
    if headers:
        merged.update(headers)
    return urllib.request.urlopen(urllib.request.Request(url, headers=merged), timeout=timeout)


def _range_matches(value: str | None, start: int, end: int) -> bool:
    if not value:
        return False
    match = re.search(r"bytes\s+(\d+)-(\d+)/(\d+|\*)", value, flags=re.I)
    if not match:
        return False
    return int(match.group(1)) == start and int(match.group(2)) == end


def _read_exact_range(url: str, start: int, end: int, *, retries: int, timeout: int) -> bytes:
    expected = end - start + 1
    last_error: Exception | None = None

    for attempt in range(1, retries + 1):
        try:
            with _request(url, headers={"Range": f"bytes={start}-{end}"}, timeout=timeout) as response:
                content_range = response.headers.get("content-range")
                if response.status != 206 or not _range_matches(content_range, start, end):
                    raise RuntimeError(
                        f"server did not honor Range {start}-{end}: "
                        f"status={response.status}, content-range={content_range!r}"
                    )
                data = response.read(expected)
                if len(data) != expected:
                    raise TimeoutError(f"short range read {start}-{end}: got {len(data)} of {expected}")
                return data
        except Exception as exc:  # noqa: BLE001 - retry network/CDN failures.
            last_error = exc
            time.sleep(min(2.0, 0.25 * attempt))

    raise RuntimeError(f"failed to read range {start}-{end} from {url}: {last_error}")


def _content_range_total(value: str | None) -> int | None:
    if not value:
        return None
    match = re.search(r"/(\d+)\s*$", value)
    if not match:
        return None
    return int(match.group(1))


def probe_url(url: str, *, timeout: int = 15, retries: int = 3) -> dict[str, str | int | bool | None]:
    """Return cheap evidence about a remote asset without reading the full body."""
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            with _request(url, headers={"Range": "bytes=0-15"}, timeout=timeout) as response:
                first = response.read(16)
                content_range = response.headers.get("content-range")
                return {
                    "status": response.status,
                    "content_type": response.headers.get("content-type"),
                    "content_length": response.headers.get("content-length"),
                    "content_range": content_range,
                    "range_supported": response.status == 206 and _range_matches(content_range, 0, 15),
                    "total_bytes": _content_range_total(content_range),
                    "signature_hex": first.hex(),
                }
        except Exception as exc:  # noqa: BLE001 - transient CDN/proxy errors.
            last_error = exc
            time.sleep(min(2.0, 0.25 * attempt))
    raise RuntimeError(f"failed to probe {url}: {last_error}")


def download_url_bytes(
    url: str,
    *,
    timeout: int = 20,
    retries: int = 4,
    chunk_size: int = 8 * 1024,
    max_bytes: int = 25 * 1024 * 1024,
) -> tuple[bytes, dict[str, str | int | bool | None]]:
    """Download URL bytes using Range chunks when the CDN is unstable.

    Some MCP/CDN URLs return a useful HEAD/Range response but hang on a full
    GET or larger ranges. 8KB chunks are intentionally conservative for
    tempfile.aiquickdraw.com and keep partial downloads detectable.
    """
    evidence = probe_url(url, timeout=timeout)
    total = evidence.get("total_bytes")

    if evidence.get("range_supported") and isinstance(total, int) and total > 0:
        if total > max_bytes:
            raise RuntimeError(f"remote asset is too large: {total} bytes > {max_bytes}")

        chunks: list[bytes] = []
        for start in range(0, total, chunk_size):
            end = min(total - 1, start + chunk_size - 1)
            chunks.append(_read_exact_range(url, start, end, retries=retries, timeout=timeout))
        data = b"".join(chunks)
        if len(data) != total:
            raise RuntimeError(f"range download length mismatch: got {len(data)} of {total}")
        return data, evidence

    # Fallback for servers without Range support.
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            with _request(url, timeout=timeout) as response:
                content_length = response.headers.get("content-length")
                if content_length and content_length.isdigit() and int(content_length) > max_bytes:
                    raise RuntimeError(f"remote asset is too large: {content_length} bytes > {max_bytes}")
                data = response.read(max_bytes + 1)
                if len(data) > max_bytes:
                    raise RuntimeError(f"remote asset exceeds max_bytes={max_bytes}")
                evidence.update(
                    {
                        "status": response.status,
                        "content_type": response.headers.get("content-type"),
                        "content_length": response.headers.get("content-length"),
                    }
                )
                return data, evidence
        except Exception as exc:  # noqa: BLE001 - retry network/CDN failures.
            last_error = exc
            time.sleep(min(2.0, 0.25 * attempt))

    raise RuntimeError(f"failed to download {url}: {last_error}")

