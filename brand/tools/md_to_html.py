#!/usr/bin/env python3
"""Report Markdown (the form `ready`/`go` write) → brand HTML that uses document.css.

Usage: python3 brand/tools/md_to_html.py <input.md> <output.html>

No Markdown library is needed. It reads the shape the writing guide produces:
  - first line "<등급>[(잠정)] · 받는 사람: …"   → the marking line with its badge, and the grade on every page
  - "# 제목 (초안)"                              → h1 (a trailing "(초안)" becomes a draft badge)
  - "작성: …" right under the title              → the meta line
  - "## 보고 요지" (and 요약, 한 줄 요약, 승인 요청, 이 회의가 끝나면) → the .lead box
  - "## 건의"                                    → heading + the .proposal box
  - "## 관련 문서"                               → ul.related; a `[경로: ?]` or `노션 > …` code span → .path
  - nested "-" and "1." lists, pipe tables, **bold**, `code`, [links](url), paragraphs, "---"
A table whose first header cell is empty or "구분" is a side-by-side comparison (table.compare: equal
columns, no option stands out). A column whose cells are all numbers, or that the writer marked "---:",
is right-aligned (.num). A long 건의 box may continue on the next page instead of leaving a gap.
The stylesheet link is written relative to the output file, so keep the output inside the workspace
(or bundle it with bundle.py, which inlines everything).
"""
import html
import os
import re
import sys
from pathlib import Path

CSS = Path(__file__).resolve().parent.parent / "document.css"

LEVELS = {  # label → (badge class, page-corner colour from document.css)
    "공개": ("public", "#5a5a5c"),
    "사내한정": ("internal", "#007a5c"),
    "대외비": ("confidential", "#8a5a00"),
    "극비": ("secret", "#b23b3b"),
}
MARKING = re.compile(r"^(공개|사내한정|대외비|극비)(\s*\(잠정\))?\s*(?:·\s*(.*))?$")
LEAD = {"보고 요지", "요약", "한 줄 요약", "승인 요청", "이 회의가 끝나면", "핵심 요약"}
PROPOSAL = {"건의"}
LONG_PROPOSAL = 400  # characters; a longer 건의 box may break across pages instead of jumping whole
RELATED = {"관련 문서", "관련 회의록·문서", "관련 자료"}
DATE_HEAD = {"일자", "일정", "날짜", "기한"}
NUM = re.compile(r"^[+\-−▲▼]?\s*\d[\d,]*(\.\d+)?\s*(%p|%|건|명|곳|개|원|만 원|억 원|시간|분|일|주)?$")
LIST = re.compile(r"^(\s*)([-*]|\d+[.)])\s+(.*)$")


def inline(text):
    """Escape, then code spans, links, bold. Code spans are protected from the other rules."""
    codes = []

    def keep(m):
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", keep, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
                  lambda m: f'<a href="{html.escape(m.group(2))}">{m.group(1)}</a>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{html.escape(codes[int(m.group(1))])}</code>", text)


def plain(text):
    return re.sub(r"[`*]", "", text)


# ── Blocks ───────────────────────────────────────────────────────────────────

def parse_list(lines, i):
    """Parse a (possibly nested) list starting at lines[i]. Returns (html, next index)."""
    first = LIST.match(lines[i])
    base = len(first.group(1))
    ordered = first.group(2)[0].isdigit()
    start = int(re.match(r"\d+", first.group(2)).group()) if ordered else 1
    items = []  # [own text lines, child html]
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            # a blank line ends the list unless the next line continues it
            nxt = next((l for l in lines[i + 1:] if l.strip()), None)
            m = LIST.match(nxt) if nxt else None
            if m and len(m.group(1)) >= base and (len(m.group(1)) > base or m.group(2)[0].isdigit() == ordered):
                i += 1
                continue
            break
        m = LIST.match(line)
        indent = len(line) - len(line.lstrip())
        if m and len(m.group(1)) == base:
            if m.group(2)[0].isdigit() != ordered:
                break
            items.append([[m.group(3)], ""])
            i += 1
        elif m and len(m.group(1)) > base and items:
            child, i = parse_list(lines, i)
            items[-1][1] += child
        elif indent > base and items:  # wrapped continuation of the item text
            items[-1][0].append(line.strip())
            i += 1
        else:
            break
    tag = "ol" if ordered else "ul"
    attr = f' start="{start}"' if ordered and start != 1 else ""
    body = "".join(f"<li>{inline(' '.join(t))}{c}</li>" for t, c in items)
    return f"<{tag}{attr}>{body}</{tag}>", i


def split_row(line):
    cells = line.strip().strip("|").split("|")
    return [c.strip() for c in cells]


def parse_table(lines, i):
    head = split_row(lines[i])
    align = split_row(lines[i + 1])  # "---:" marks a column the writer right-aligned
    i += 2  # header + separator
    rows = []
    while i < len(lines) and lines[i].strip().startswith("|"):
        rows.append(split_row(lines[i]))
        i += 1
    n = len(head)
    rows = [r + [""] * (n - len(r)) for r in rows]
    compare = head[0] in ("", "구분")
    num = [j > 0 and ((j < len(align) and align[j].endswith(":") and not align[j].startswith(":"))
                      or (all(NUM.match(r[j]) for r in rows if r[j]) and any(r[j] for r in rows)))
           for j in range(n)]
    out = ['<table class="compare">' if compare else "<table>"]
    if compare:
        out.append('<colgroup><col class="label">' + "<col>" * (n - 1) + "</colgroup>")
    elif head[0] in DATE_HEAD:
        out.append('<colgroup><col style="width:17%">' + "<col>" * (n - 1) + "</colgroup>")
    th = []
    for j, c in enumerate(head):
        cls = ' class="num"' if num[j] else ""
        th.append(f'<th scope="col"{cls}>{inline(c or ("구분" if compare else ""))}</th>')
    out.append("<thead><tr>" + "".join(th) + "</tr></thead><tbody>")
    for r in rows:
        cells = []
        for j, c in enumerate(r):
            if compare and j == 0:
                cells.append(f'<th scope="row">{inline(c)}</th>')
            else:
                cls = ' class="num"' if num[j] else ""
                cells.append(f"<td{cls}>{inline(c)}</td>")
        out.append("<tr>" + "".join(cells) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out), i


def parse_blocks(lines):
    """Body blocks (no headings). Returns a list of HTML strings."""
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s or s.startswith("<!--"):
            i += 1
        elif LIST.match(line):
            block, i = parse_list(lines, i)
            out.append(block)
        elif s.startswith("|") and i + 1 < len(lines) and re.match(r"^\|(\s*:?-+:?\s*\|)+$", lines[i + 1].strip()):
            block, i = parse_table(lines, i)
            out.append(block)
        elif re.match(r"^(-{3,}|\*{3,})$", s):
            out.append("<hr>")
            i += 1
        elif s.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip()[1:].strip())
                i += 1
            out.append(f"<blockquote><p>{inline(' '.join(quote))}</p></blockquote>")
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not LIST.match(lines[i]) \
                    and not lines[i].strip().startswith(("|", ">", "#")):
                para.append(lines[i].strip())
                i += 1
            out.append(f"<p>{inline(' '.join(para))}</p>")
    return out


def related(lines):
    items = []
    for line in lines:
        m = LIST.match(line)
        if not m:
            continue
        text = m.group(3)
        path = re.search(r"`([^`]*(?:경로|>)[^`]*)`\s*$", text)
        if path:
            text = text[:path.start()].rstrip(" —-")
            items.append(f'<li>{inline(text)}<span class="path">{html.escape(path.group(1))}</span></li>')
        else:
            items.append(f"<li>{inline(text)}</li>")
    return '<ul class="related">' + "".join(items) + "</ul>"


# ── Document ─────────────────────────────────────────────────────────────────

def convert(md, css_href):
    lines = md.replace("\r\n", "\n").split("\n")
    while lines and not lines[0].strip():
        lines.pop(0)
    marking, level = "", None
    m = MARKING.match(lines[0].strip()) if lines else None
    if m:
        level = m.group(1) + (m.group(2) or "").strip()
        badge = LEVELS[m.group(1)][0]
        rest = f"<span>{inline(m.group(3))}</span>" if m.group(3) else ""
        marking = f'<div class="marking"><span class="badge {badge}">{html.escape(level)}</span>{rest}</div>'
        lines = lines[1:]

    # split into sections at h1/h2; h3 stays inside its section
    title, meta, sections, cur = "", "", [], None
    for line in lines:
        h = re.match(r"^(#{1,2})\s+(.*)$", line)
        if h and h.group(1) == "#" and not title:
            title = h.group(2).strip()
        elif h and h.group(1) == "##":
            cur = [h.group(2).strip(), []]
            sections.append(cur)
        elif cur is None:
            if line.strip().startswith("작성:") and not meta:
                meta = line.strip()
            elif line.strip():
                sections.append(cur := [None, [line]])
        else:
            cur[1].append(line)

    def body(sec_lines):
        parts, chunk = [], []
        for line in sec_lines:
            h3 = re.match(r"^###\s+(.*)$", line)
            if h3:
                parts += parse_blocks(chunk)
                parts.append(f"<h3>{inline(h3.group(1))}</h3>")
                chunk = []
            else:
                chunk.append(line)
        return "".join(parts + parse_blocks(chunk))

    out = []
    for name, sec in sections:
        key = plain(name or "")
        if key in LEAD:
            out.append(f'<div class="lead"><span class="lead-label">{inline(name)}</span>{body(sec)}</div>')
        elif key in PROPOSAL:
            inner = body(sec)
            cls = "proposal long" if len(re.sub(r"<[^>]+>", "", inner)) > LONG_PROPOSAL else "proposal"
            out.append(f'<h2>{inline(name)}</h2><div class="{cls}">{inner}</div>')
        elif key in RELATED:
            out.append(f"<h2>{inline(name)}</h2>{related(sec)}")
        elif name is None:
            out.append(body(sec))
        else:
            out.append(f"<h2>{inline(name)}</h2>{body(sec)}")

    draft = re.search(r"\s*\(초안\)\s*$", title)
    h1 = inline(title[:draft.start()] if draft else title)
    if draft:
        h1 += ' <span class="badge draft">초안</span>'
    page = ""
    if level:
        colour = LEVELS[m.group(1)][1]
        page = (f'<style>@page {{ @top-right {{ content: "{level}"; font-family: "Paperlogy", sans-serif; '
                f"font-size: 8pt; color: {colour}; }} }}</style>\n")
    meta_html = f'<p class="meta">{inline(meta)}</p>' if meta else ""
    return (
        '<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{html.escape(plain(title))}</title>\n"
        f'<link rel="stylesheet" href="{html.escape(css_href)}">\n{page}</head>\n<body>\n'
        f'<article class="doc">\n{marking}\n<h1>{h1}</h1>\n{meta_html}\n'
        + "\n".join(out) + "\n</article>\n</body>\n</html>\n"
    )


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: python3 brand/tools/md_to_html.py <input.md> <output.html>")
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    href = os.path.relpath(CSS, dst.resolve().parent).replace(os.sep, "/")
    dst.write_text(convert(src.read_text(encoding="utf-8"), href), encoding="utf-8")
    print("wrote", dst)


if __name__ == "__main__":
    main()
