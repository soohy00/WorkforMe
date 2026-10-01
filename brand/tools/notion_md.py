#!/usr/bin/env python3
"""Notion template (plain Markdown) → Notion-flavored Markdown for the Notion API / MCP.

Usage: python3 brand/tools/notion_md.py <template.md>
Prints JSON: {"title": ..., "content": ...}

The templates in brand/notion/templates/ are plain Markdown so they import into any Notion
workspace (가져오기 > Markdown). When Claude creates them through a Notion connector, this script
turns them into Notion's own blocks:
- a quote block becomes a callout; its first emoji picks the color (see COLORS)
- a pipe table becomes a Notion table with a header row
- special characters in text are escaped as Notion requires
"""
import json
import re
import sys

# Brand → Notion colors. Notion has no custom colors or fonts, so the accent maps to green.
COLORS = {
    "📌": "green_bg",   # first screen: 보고 요지, 승인 요청, 요약 (.lead)
    "✍️": "gray_bg",    # 작성 안내 — deleted before sending
    "✅": "default",     # 건의 (.proposal)
    "ℹ️": "blue_bg",     # .callout.info
    "⚠️": "yellow_bg",   # .callout.warn
    "⛔": "red_bg",      # .callout.danger
}
LIST = re.compile(r"^(\s*)(- \[[ x]\] |- |\d+\. )(.*)$")


def esc(text):
    """Escape Notion-markdown specials; keep **bold**."""
    return re.sub(r"([\\~`$\[\]<>{}|^])", r"\\\1", text)


def line_block(line, indent=""):
    m = LIST.match(line)
    if m:
        depth = len(m.group(1)) // 2
        return indent + "\t" * depth + m.group(2) + esc(m.group(3))
    if line.startswith("#"):
        hashes, _, rest = line.partition(" ")
        return indent + hashes + " " + esc(rest)
    return indent + esc(line)


def callout(lines):
    first = lines[0]
    icon = next((e for e in COLORS if first.startswith(e)), None)
    head = first[len(icon):].strip() if icon else first
    color = COLORS.get(icon, "gray_bg")
    attrs = (f' icon="{icon}"' if icon else "") + (f' color="{color}"' if color != "default" else "")
    out = [f"<callout{attrs}>", "\t" + esc(head)]
    out += [line_block(l, "\t") for l in lines[1:]]
    out.append("</callout>")
    return out


def table(lines):
    rows = [l.strip().strip("|").split("|") for l in lines if not re.match(r"^\|(\s*:?-+:?\s*\|)+$", l.strip())]
    out = ['<table header-row="true">']
    for row in rows:
        out.append("\t<tr>")
        out += [f"\t\t<td>{esc(cell.strip())}</td>" for cell in row]
        out.append("\t</tr>")
    out.append("</table>")
    return out


def convert(src):
    lines = src.splitlines()
    title = ""
    if lines and lines[0].startswith("# "):
        title, lines = lines[0][2:].strip(), lines[1:]
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
        elif line.startswith(">"):
            group = []
            while i < len(lines) and lines[i].startswith(">"):
                group.append(lines[i][1:].strip())
                i += 1
            out += callout(group)
        elif line.startswith("|"):
            group = []
            while i < len(lines) and lines[i].startswith("|"):
                group.append(lines[i])
                i += 1
            out += table(group)
        else:
            out.append(line_block(line))
            i += 1
    return {"title": title, "content": "\n".join(out)}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python3 brand/tools/notion_md.py <template.md>")
    with open(sys.argv[1], encoding="utf-8") as f:
        print(json.dumps(convert(f.read()), ensure_ascii=False))
