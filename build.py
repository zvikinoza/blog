#!/usr/bin/env python3
"""Tiny static blog generator: posts/*.md -> site/

Post format (front matter, then Markdown):

    ---
    title: Why XLA fuses what it fuses
    date: 2026-09-11
    tags: xla, compilers
    description: One-line summary shown on the index and in the RSS feed.
    math: true          # optional, loads KaTeX
    draft: true         # optional, skipped by the build
    ---
    Body...

Run:  python3 build.py        (output in site/)
      python3 build.py serve  (build + local server on :8000)
"""
import datetime as dt
import html
import re
import shutil
import sys
from pathlib import Path

import markdown
from pygments.formatters import HtmlFormatter

ROOT = Path(__file__).parent
POSTS = ROOT / "posts"
STATIC = ROOT / "static"
TEMPLATES = ROOT / "templates"
OUT = ROOT / "site"

# ---- site config -----------------------------------------------------------
SITE = {
    "title": "zviki's blog",
    "tagline": "AI compilers, chips, and programming",
    "url": "https://zvikinoza.github.io/blog",   # change to your domain when set
    "author": "Zviki",
}
# ----------------------------------------------------------------------------

MD_EXTENSIONS = [
    "fenced_code", "codehilite", "tables", "footnotes", "toc",
    "attr_list", "smarty", "md_in_html",
]
MD_CONFIG = {
    "codehilite": {"css_class": "highlight", "guess_lang": False},
    "toc": {"permalink": "#", "permalink_class": "anchor", "toc_depth": "2-3"},
}


def parse_post(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not m:
        raise SystemExit(f"{path}: missing front matter")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip().lower()] = v.strip()
    body = m.group(2)

    md = markdown.Markdown(extensions=MD_EXTENSIONS, extension_configs=MD_CONFIG)
    content = md.convert(body)

    date = dt.date.fromisoformat(meta["date"])
    slug = meta.get("slug") or re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
    tags = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
    return {
        "title": meta["title"],
        "date": date,
        "date_iso": date.isoformat(),
        "date_human": date.strftime("%B %-d, %Y"),
        "tags": tags,
        "description": meta.get("description", ""),
        "math": meta.get("math", "").lower() in ("true", "yes", "1"),
        "draft": meta.get("draft", "").lower() in ("true", "yes", "1"),
        "slug": slug,
        "url": f"{SITE['url']}/{slug}/",  # note: SITE["url"] may be overridden in serve mode
        "content": content,
        "toc": "",  # [TOC] in the body renders inline via the toc extension
        "source": path,
    }


def render(template: str, **ctx) -> str:
    """Minimal {{ var }} substitution. Values are inserted as-is (already HTML)."""
    tpl = (TEMPLATES / template).read_text(encoding="utf-8")
    ctx = {**SITE, **ctx}
    return re.sub(r"\{\{\s*(\w+)\s*\}\}", lambda m: str(ctx.get(m.group(1), "")), tpl)


def page(title, body, *, head="", path=""):
    return render(
        "base.html",
        page_title=f"{title} · {SITE['title']}" if title != SITE["title"] else title,
        body=body,
        head=head,
        year=dt.date.today().year,
        canonical=f"{SITE['url']}/{path}",
    )


def post_html(p):
    tags = " ".join(f'<a class="tag" href="{SITE["url"]}/tags/{t}/">{t}</a>' for t in p["tags"])
    body = render(
        "post.html",
        title=html.escape(p["title"]),
        date_iso=p["date_iso"],
        date_human=p["date_human"],
        tags=tags,
        toc=p["toc"],
        content=p["content"],
    )
    head = ""
    if p["description"]:
        head += f'<meta name="description" content="{html.escape(p["description"])}">\n'
    if p["math"]:
        head += KATEX
    return page(p["title"], body, head=head, path=f"{p['slug']}/")


def post_list(posts, heading=None):
    items = "\n".join(
        f'<li><time datetime="{p["date_iso"]}">{p["date_iso"]}</time> '
        f'<a href="{p["url"]}">{html.escape(p["title"])}</a>'
        + (f'<p class="desc">{html.escape(p["description"])}</p>' if p["description"] else "")
        + "</li>"
        for p in posts
    )
    h = f"<h1>{html.escape(heading)}</h1>" if heading else ""
    return f'{h}<ul class="posts">{items}</ul>'


def rss(posts):
    items = "\n".join(
        f"""  <item>
    <title>{html.escape(p["title"])}</title>
    <link>{p["url"]}</link>
    <guid>{p["url"]}</guid>
    <pubDate>{dt.datetime.combine(p["date"], dt.time()).strftime("%a, %d %b %Y 00:00:00 +0000")}</pubDate>
    <description>{html.escape(p["description"] or p["title"])}</description>
    <content:encoded><![CDATA[{p["content"]}]]></content:encoded>
  </item>"""
        for p in posts
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
<channel>
  <title>{html.escape(SITE["title"])}</title>
  <link>{SITE["url"]}/</link>
  <description>{html.escape(SITE["tagline"])}</description>
  <atom:link href="{SITE["url"]}/feed.xml" rel="self" type="application/rss+xml"/>
{items}
</channel>
</rss>
"""


KATEX = """<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}]})"></script>
"""


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(STATIC, OUT / "static")
    # Pygments CSS: light theme by default, dark under prefers-color-scheme
    light = HtmlFormatter(style="friendly").get_style_defs(".highlight")
    dark = HtmlFormatter(style="monokai").get_style_defs(".highlight")
    (OUT / "static" / "highlight.css").write_text(
        light + "\n@media (prefers-color-scheme: dark) {\n" + dark + "\n}\n"
    )

    posts = [parse_post(p) for p in sorted(POSTS.glob("*.md"))]
    posts = [p for p in posts if not p["draft"]]
    posts.sort(key=lambda p: p["date"], reverse=True)

    for p in posts:
        d = OUT / p["slug"]
        d.mkdir(parents=True)
        (d / "index.html").write_text(post_html(p), encoding="utf-8")

    (OUT / "index.html").write_text(page(SITE["title"], post_list(posts)), encoding="utf-8")

    tags = sorted({t for p in posts for t in p["tags"]})
    for t in tags:
        d = OUT / "tags" / t
        d.mkdir(parents=True)
        tagged = [p for p in posts if t in p["tags"]]
        (d / "index.html").write_text(page(f"#{t}", post_list(tagged, heading=f"#{t}"), path=f"tags/{t}/"), encoding="utf-8")

    about = ROOT / "about.md"
    if about.exists():
        md = markdown.Markdown(extensions=MD_EXTENSIONS, extension_configs=MD_CONFIG)
        (OUT / "about").mkdir()
        (OUT / "about" / "index.html").write_text(
            page("About", md.convert(about.read_text(encoding="utf-8")), path="about/"), encoding="utf-8")

    (OUT / "feed.xml").write_text(rss(posts), encoding="utf-8")
    (OUT / ".nojekyll").write_text("")
    print(f"built {len(posts)} posts, {len(tags)} tags -> {OUT}")


if __name__ == "__main__":
    serve = len(sys.argv) > 1 and sys.argv[1] == "serve"
    if serve:
        SITE["url"] = "http://localhost:8000"
    build()
    if serve:
        import functools, http.server
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
        print("serving on http://localhost:8000")
        http.server.ThreadingHTTPServer(("", 8000), handler).serve_forever()
