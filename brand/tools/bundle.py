#!/usr/bin/env python3
"""HTML document → one self-contained HTML file (styles and brand fonts inside).

Usage: python3 brand/tools/bundle.py <input.html> <output.html>
Needs fontTools (`pip install fonttools`).

Every local <link rel="stylesheet"> and <script src> (charts.js) is inlined. Every local font in that
CSS is cut down to the characters the document and its scripts use and embedded as a data URI, so the file stays small (about 400 KB for
a two-page report) and opens anywhere with the same look as the PDF.
"""
import base64
import html
import io
import re
import string
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

from fontTools import subset
from fontTools.ttLib import TTFont

LINK = re.compile(r'<link\b[^>]*\brel="stylesheet"[^>]*>', re.I)
HREF = re.compile(r'\bhref="([^"]+)"', re.I)
SCRIPT = re.compile(r'<script\b[^>]*\bsrc="([^"]+)"[^>]*>\s*</script>', re.I)
FONT_URL = re.compile(r'url\("?([^")]+\.(?:ttf|otf|woff2?))"?\)', re.I)


def local_path(ref, base):
    """Resolve a relative path or file:// URL; None for anything remote."""
    url = urlparse(ref)
    if url.scheme == "file":
        return Path(unquote(url.path))
    if url.scheme:
        return None
    return (base / unquote(ref)).resolve()


def subset_font(path, text):
    font = TTFont(path)
    options = subset.Options()
    options.layout_features = ["*"]
    subsetter = subset.Subsetter(options)
    subsetter.populate(text=text)
    subsetter.subset(font)
    buf = io.BytesIO()
    font.save(buf)
    return "data:font/ttf;base64," + base64.b64encode(buf.getvalue()).decode()


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: python3 brand/tools/bundle.py <input.html> <output.html>")
    src_path = Path(sys.argv[1]).resolve()
    src = src_path.read_text(encoding="utf-8")

    # Characters to keep: everything in the document and its styles (CSS `content:` text such as the
    # classification mark), plus ASCII so small later edits still render.
    sheets = []
    for tag in LINK.findall(src):
        href = HREF.search(tag)
        path = local_path(href.group(1), src_path.parent) if href else None
        if path is None:
            continue
        if not path.is_file():
            sys.exit(f"stylesheet not found: {path}")
        sheets.append((tag, path, path.read_text(encoding="utf-8")))
    text = html.unescape(src) + "".join(css for _, _, css in sheets) + string.printable
    for m in SCRIPT.finditer(src):  # labels a script draws, such as "표로 보기"
        path = local_path(m.group(1), src_path.parent)
        if path is not None and path.is_file():
            text += path.read_text(encoding="utf-8")

    out = src
    for tag, path, css in sheets:
        def embed(m, base=path.parent):
            font = local_path(m.group(1), base)
            if font is None:
                return m.group(0)
            if not font.is_file():
                sys.exit(f"font not found: {font}")
            return f'url("{subset_font(font, text)}")'

        out = out.replace(tag, "<style>\n" + FONT_URL.sub(embed, css) + "\n</style>", 1)

    scripts = 0
    for m in list(SCRIPT.finditer(out)):
        path = local_path(m.group(1), src_path.parent)
        if path is None:
            continue
        if not path.is_file():
            sys.exit(f"script not found: {path}")
        code = path.read_text(encoding="utf-8").replace("</script", "<\\/script")
        out = out.replace(m.group(0), "<script>\n" + code + "\n</script>", 1)
        scripts += 1

    Path(sys.argv[2]).write_text(out, encoding="utf-8")
    print(f"wrote {sys.argv[2]} ({len(out.encode('utf-8')) // 1024} KB, "
          f"{len(sheets)} stylesheet(s) and {scripts} script(s) inlined)")


if __name__ == "__main__":
    main()
