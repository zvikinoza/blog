# blog

Static blog: Markdown in `posts/` → HTML in `site/`. No framework, one ~200-line script.

## Write a post

Create `posts/YYYY-MM-DD-slug.md`:

```
---
title: My post
date: 2026-09-11
tags: xla, tpu
description: One-liner for the index and RSS.
math: true       # optional: enables KaTeX ($...$ and $$...$$)
draft: true      # optional: excluded from the build
---
Markdown body. Put [TOC] on its own line to get a table of contents.
```

The file name after the date becomes the URL: `/slug/`.

## Preview locally

```
pip install -r requirements.txt
python3 build.py serve      # http://localhost:8000
```

## Deploy

Push to `main`. The GitHub Actions workflow builds and publishes to GitHub Pages.
One-time setup: repo → Settings → Pages → Source: **GitHub Actions**.

Set `SITE["url"]` in `build.py` to the real address (e.g. `https://<user>.github.io/blog`,
or a custom domain, in which case also add a `static/CNAME` file).
