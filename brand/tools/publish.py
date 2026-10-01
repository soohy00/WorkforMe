#!/usr/bin/env python3
"""Report Markdown → the two files a reader gets: a brand PDF and one self-contained HTML file.

Usage: python3 brand/tools/publish.py <document.md> [preview.png]

Writes next to the Markdown:
  <name>.pdf    A4, brand fonts embedded (render.js)
  <name>.html   one file with styles and fonts inside (bundle.py) — opens anywhere, looks like the PDF
The optional preview.png is a full-page picture of the HTML, for checking the look before handing it over.
The Markdown stays the source: edit it, then run this again.
Needs Node with Playwright (render.js) and fontTools (bundle.py).
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent


def main():
    if len(sys.argv) not in (2, 3):
        sys.exit("usage: python3 brand/tools/publish.py <document.md> [preview.png]")
    src = Path(sys.argv[1]).resolve()
    pdf, one = src.with_suffix(".pdf"), src.with_suffix(".html")
    env = dict(os.environ)
    if "NODE_PATH" not in env:
        root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
        env["NODE_PATH"] = root
    with tempfile.TemporaryDirectory(prefix=".publish-", dir=TOOLS) as tmp:  # inside the workspace, so the CSS link resolves
        linked = Path(tmp) / (src.stem + ".html")
        subprocess.run([sys.executable, TOOLS / "md_to_html.py", src, linked], check=True, stdout=subprocess.DEVNULL)
        render = ["node", TOOLS / "render.js", linked, pdf] + ([sys.argv[2]] if len(sys.argv) == 3 else [])
        subprocess.run([str(a) for a in render], check=True, env=env, stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable, TOOLS / "bundle.py", linked, one], check=True, stdout=subprocess.DEVNULL)
    print("wrote", pdf)
    print("wrote", one)


if __name__ == "__main__":
    main()
