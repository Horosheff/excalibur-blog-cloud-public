#!/usr/bin/env python3
"""Build preview.html for local article review (UTF-8, H1, cover, readable CSS)."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def project_root() -> Path:
    env_root = os.environ.get("EXCALIBUR_PROJECT_ROOT", "").strip()
    if env_root:
        return Path(env_root)
    return Path(__file__).resolve().parents[1]


def read_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def site_name(root: Path) -> str:
    brief = root / "memory/brief/site-brief.md"
    if not brief.is_file():
        return "Excalibur BLOG"
    for line in brief.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("- **site_name:**"):
            return line.split(":", 1)[1].strip()
    return "Excalibur BLOG"


def build_preview(article_dir: Path, root: Path) -> Path:
    article_dir = article_dir.resolve()
    article_html = article_dir / "article.html"
    meta_path = article_dir / "article.meta.json"
    cover_registry = article_dir / "cover/cover-registry.json"

    if not article_html.is_file():
        raise FileNotFoundError(f"article.html not found: {article_html}")

    meta = read_json(meta_path)
    cover = read_json(cover_registry)
    body = article_html.read_text(encoding="utf-8").strip()

    title = meta.get("title") or meta.get("h1") or "Preview"
    h1 = meta.get("h1") or title
    description = meta.get("description") or ""

    cover_block = ""
    cover_file = cover.get("file")
    if cover_file:
        cover_path = article_dir / cover_file
        if cover_path.is_file():
            alt = html.escape(cover.get("alt") or h1)
            cover_block = (
                f'<figure class="cover"><img src="{html.escape(cover_file, quote=True)}" '
                f'alt="{alt}" loading="eager"></figure>\n'
            )

    brand = site_name(root)
    out = article_dir / "preview.html"
    doc = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <style>
    :root {{
      color-scheme: light;
      --bg: #FAFAF7;
      --text: #1A1A2E;
      --muted: #5c5c72;
      --accent: #E85D4C;
      --line: #e8e8e0;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font: 18px/1.65 Georgia, "Times New Roman", serif;
    }}
    .wrap {{
      max-width: 720px;
      margin: 0 auto;
      padding: 2rem 1.25rem 4rem;
    }}
    .badge {{
      font: 600 12px/1 system-ui, sans-serif;
      letter-spacing: .04em;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: .75rem;
    }}
    h1 {{
      font: 700 clamp(1.75rem, 4vw, 2.35rem)/1.15 system-ui, sans-serif;
      margin: 0 0 1.25rem;
      color: var(--text);
    }}
    .cover img,
    .article .inline-quad img {{
      width: 100%;
      height: auto;
      aspect-ratio: 16 / 9;
      object-fit: cover;
      border-radius: 12px;
      display: block;
    }}
    .article .inline-quad {{
      margin: 1rem 0 1.25rem;
    }}
    .article :is(h2, h3) {{
      font-family: system-ui, sans-serif;
      line-height: 1.25;
      margin: 2rem 0 .75rem;
    }}
    .article h2 {{ font-size: 1.35rem; }}
    .article h3 {{ font-size: 1.1rem; color: var(--muted); }}
    .article p {{ margin: 0 0 1rem; }}
    .article a {{ color: var(--accent); }}
    .article table {{
      width: 100%;
      border-collapse: collapse;
      margin: 1rem 0 1.25rem;
      font-size: .95rem;
    }}
    .article th, .article td {{
      border: 1px solid var(--line);
      padding: .55rem .65rem;
      text-align: left;
      vertical-align: top;
    }}
    .article th {{ background: #fff; }}
    .article blockquote {{
      margin: 1rem 0 1.25rem;
      padding: .85rem 1rem;
      border-left: 4px solid var(--accent);
      background: #fff;
    }}
    .article ul, .article ol {{ margin: 0 0 1rem 1.25rem; padding: 0; }}
    .article li {{ margin: .35rem 0; }}
    .note {{
      margin-top: 2rem;
      padding: .75rem 1rem;
      border: 1px dashed var(--line);
      font: 14px/1.5 system-ui, sans-serif;
      color: var(--muted);
      background: #fff;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="badge">{html.escape(brand)} · preview</div>
    {cover_block}<h1>{html.escape(h1)}</h1>
    <div class="article">
{body}
    </div>
    <p class="note">Локальный preview Excalibur BLOG. В WordPress уходит только фрагмент <code>article.html</code>; H1 и тема — из WP.</p>
  </div>
</body>
</html>
"""
    out.write_text(doc, encoding="utf-8", newline="\n")
    return out


class Utf8Handler(SimpleHTTPRequestHandler):
    extensions_map = {
        **getattr(SimpleHTTPRequestHandler, "extensions_map", {}),
        ".html": "text/html; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".js": "application/javascript; charset=utf-8",
        ".json": "application/json; charset=utf-8",
    }

    def guess_type(self, path: str) -> str:
        base, _, encoding = super().guess_type(path).partition(";")
        if path.endswith((".html", ".htm")):
            return "text/html; charset=utf-8"
        if encoding:
            return f"{base}; charset=utf-8"
        return base


def serve(directory: Path, port: int) -> None:
    handler = lambda *args, **kwargs: Utf8Handler(  # noqa: E731
        *args, directory=str(directory), **kwargs
    )
    httpd = ThreadingHTTPServer(("127.0.0.1", port), handler)
    print(f"Serving {directory} at http://127.0.0.1:{port}/preview.html (UTF-8)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


def main() -> int:
    ap = argparse.ArgumentParser(description="Build/readable preview for article.html")
    ap.add_argument("--article-dir", required=True, help="memory/blog/articles/<id>-<slug>")
    ap.add_argument("--serve", action="store_true", help="Serve directory with UTF-8 headers")
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()

    root = project_root()
    article_dir = Path(args.article_dir)
    if not article_dir.is_absolute():
        article_dir = root / article_dir

    preview = build_preview(article_dir, root)
    print(f"OK preview={preview}")

    if args.serve:
        serve(article_dir, args.port)
    else:
        print(f"Open: http://127.0.0.1:{args.port}/preview.html")
        print("Tip: python scripts/excalibur_blog_preview.py --article-dir ... --serve")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
