/*
 * WorkforMe charts — dependency-free SVG charts for documents (HTML and PDF).
 * Use with document.css + viz.css. Rules follow the dataviz method: thin marks, one axis,
 * colour by job (slot order fixed), legend for 2+ series, selective direct labels,
 * hover/focus tooltips, and a table view for every chart.
 *
 * Markup:
 *   <figure class="viz" data-chart="line">
 *     <figcaption><span class="viz-title">…</span><span class="viz-sub">…</span></figcaption>
 *     <script type="application/json">{ …spec… }</script>
 *   </figure>
 *
 * Spec (all charts):
 *   x        category labels, e.g. ["9/21(월)", …]
 *   series   [{ "name": "예약", "values": [..], "slot": 1 }]   slot = palette slot 1–8, fixed per entity
 *   unit     unit shown after numbers ("건", "%")
 *   note     definition and source line under the chart
 *   table    "print" → the table view is also printed
 * line:     emphasis (a series name or a list, drawn in colour; others grey) · target { value, label }
 * bar:      vertical columns (one or more series, grouped)
 * hbar:     horizontal bars (one series; long category names); emphasis = category name(s)
 * slot "muted" draws a series in grey (for "기타")
 * stacked:  horizontal stacked bars; percent: true for 100% bars
 * diverge:  horizontal bars around zero (above = --viz-pos, below = --viz-neg)
 * Sparkline in a stat tile: <svg class="spark" data-values="3,4,5,…"></svg>
 *
 * Labels are inserted with textContent only (data may come from files or tools).
 */
(function () {
  "use strict";
  var NS = "http://www.w3.org/2000/svg";
  var W = 640; // viewBox width = the figure's real width, set per chart so text stays at true size
  var FONT = 11;

  function el(tag, attrs, parent) {
    var n = document.createElementNS(NS, tag);
    for (var k in attrs) if (attrs[k] !== undefined) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  }
  function html(tag, cls, parent, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined) n.textContent = text;
    if (parent) parent.appendChild(n);
    return n;
  }
  // Text set inside a coloured fill: ink or white, whichever has more contrast with the fill.
  function onFill(cssVar) {
    var m = cssVar.match(/var\((--[\w-]+)\)/), hex = m ? getComputedStyle(document.documentElement).getPropertyValue(m[1]).trim() : cssVar;
    if (hex.indexOf("var(") === 0) hex = getComputedStyle(document.documentElement).getPropertyValue("--accent").trim() || "#00b48a";
    var c = hex.replace("#", ""), ch = [0, 2, 4].map(function (k) {
      var v = parseInt(c.substr(k, 2), 16) / 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    });
    var L = 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2];
    return (1.05) / (L + 0.05) >= (L + 0.05) / (0.003 + 0.05) ? "#ffffff" : "var(--ink)"; // ink #0a0a0a
  }
  function color(s, i) { return s.slot === "muted" ? "var(--viz-muted)" : "var(--viz-" + (s.slot || i + 1) + ")"; }
  // emphasis: one name or a list; everything else is drawn in the de-emphasis grey
  function emph(spec, name) { var e = spec.emphasis; return !e || (Array.isArray(e) ? e.indexOf(name) >= 0 : e === name); }
  function fmt(v, unit) {
    if (v === null || v === undefined || isNaN(v)) return "–";
    var r = Math.round(v * 10) / 10;
    return r.toLocaleString("ko-KR") + (unit ? unit : "");
  }
  function niceStep(span, count) {
    var raw = span / count, p = Math.pow(10, Math.floor(Math.log10(raw))), f = raw / p;
    return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 2.5 ? 2.5 : f <= 5 ? 5 : 10) * p;
  }
  function ticks(min, max, count) {
    if (min === max) max = min + 1;
    var step = niceStep(max - min, count || 4);
    var lo = Math.floor(min / step) * step, hi = Math.ceil(max / step) * step, out = [];
    for (var v = lo; v <= hi + step / 2; v += step) out.push(Math.round(v * 1e6) / 1e6);
    return out;
  }
  function textWidth(svg, s, size, weight) {
    var t = el("text", { x: -9999, y: -9999, "font-size": size || FONT, "font-weight": weight || 400 }, svg);
    t.textContent = s;
    var w = t.getComputedTextLength();
    svg.removeChild(t);
    return w;
  }
  function label(svg, x, y, s, o) {
    o = o || {};
    var t = el("text", {
      x: x, y: y, "font-size": o.size || FONT, "font-weight": o.weight || 400,
      "text-anchor": o.anchor || "start", "dominant-baseline": o.baseline || "middle",
    }, svg);
    t.style.fill = o.fill || "var(--steel)";
    t.textContent = s;
    return t;
  }
  // Column/bar with a 4px rounded data end and a square baseline end.
  function barPath(x, y, w, h, dir) {
    var r = Math.min(4, Math.abs(dir === "up" || dir === "down" ? w : h) / 2, Math.abs(dir === "up" || dir === "down" ? h : w));
    if (dir === "up") return "M" + x + "," + (y + h) + "V" + (y + r) + "Q" + x + "," + y + " " + (x + r) + "," + y + "H" + (x + w - r) + "Q" + (x + w) + "," + y + " " + (x + w) + "," + (y + r) + "V" + (y + h) + "Z";
    if (dir === "right") return "M" + x + "," + y + "H" + (x + w - r) + "Q" + (x + w) + "," + y + " " + (x + w) + "," + (y + r) + "V" + (y + h - r) + "Q" + (x + w) + "," + (y + h) + " " + (x + w - r) + "," + (y + h) + "H" + x + "Z";
    if (dir === "left") return "M" + (x + w) + "," + y + "H" + (x + r) + "Q" + x + "," + y + " " + x + "," + (y + r) + "V" + (y + h - r) + "Q" + x + "," + (y + h) + " " + (x + r) + "," + (y + h) + "H" + (x + w) + "Z";
    return "M" + x + "," + y + "H" + (x + w) + "V" + (y + h) + "H" + x + "Z";
  }

  // ── Shared pieces ──────────────────────────────────────────────────────
  function legend(fig, spec, kind) {
    if (spec.series.length < 2) return;
    var ul = html("ul", "viz-legend", fig);
    spec.series.forEach(function (s, i) {
      var li = html("li", "", ul);
      var k = html("span", "key " + kind, li);
      k.style.background = emph(spec, s.name) ? color(s, i) : "var(--viz-muted)";
      html("span", "", li, s.name);
    });
  }
  function tooltip(fig) {
    var tip = html("div", "viz-tip", fig);
    tip.setAttribute("role", "status");
    return {
      show: function (head, rows, px, py) {
        tip.textContent = "";
        html("span", "t-head", tip, head);
        rows.forEach(function (r) {
          var row = html("span", "t-row", tip);
          var key = html("span", "t-key", row);
          key.style.background = r.color;
          html("b", "", row, r.value);
          html("span", "", row, r.name);
        });
        var fw = fig.clientWidth, tw = tip.offsetWidth;
        tip.style.left = Math.max(4, Math.min(px + 12, fw - tw - 4)) + "px";
        tip.style.top = Math.max(4, py - 12) + "px";
        tip.classList.add("on");
      },
      hide: function () { tip.classList.remove("on"); },
    };
  }
  function toPx(svg, fig, x, y) {
    var r = svg.getBoundingClientRect(), f = fig.getBoundingClientRect(), s = r.width / W;
    return [r.left - f.left + x * s, r.top - f.top + y * s];
  }
  function table(fig, spec, rowsAreX) {
    var d = html("details", "viz-table", fig);
    if (spec.table === "print") { d.classList.add("print"); d.open = true; }
    html("summary", "", d, "표로 보기");
    var t = html("table", "", d), thead = html("thead", "", t), tr = html("tr", "", thead);
    html("th", "", tr, spec.xLabel || "구분");
    spec.series.forEach(function (s) { html("th", "num", tr, s.name + (spec.unit ? " (" + spec.unit + ")" : "")); });
    var tb = html("tbody", "", t);
    spec.x.forEach(function (x, i) {
      var r = html("tr", "", tb);
      html("td", "", r, x);
      spec.series.forEach(function (s) { html("td", "num", r, fmt(s.values[i])); });
    });
  }
  function note(fig, spec) { if (spec.note) html("p", "viz-note", fig, spec.note); }
  function yAxis(svg, sc, left, right, ticksArr, unit) {
    ticksArr.forEach(function (v) {
      var y = sc(v);
      el("line", { x1: left, x2: right, y1: y, y2: y, "stroke-width": 1, "shape-rendering": "crispEdges" }, svg).style.stroke = v === 0 ? "var(--viz-axis)" : "var(--viz-grid)";
      label(svg, left - 6, y, fmt(v, unit), { anchor: "end" });
    });
  }
  function leftMargin(svg, ticksArr, unit) {
    return Math.ceil(Math.max.apply(null, ticksArr.map(function (v) { return textWidth(svg, fmt(v, unit)); }))) + 10;
  }

  // ── Line ───────────────────────────────────────────────────────────────
  function line(fig, spec) {
    legend(fig, spec, "line");
    var H = spec.height || 220, top = 10, bottom = 24;
    var svg = el("svg", { class: "plot", viewBox: "0 0 " + W + " " + H, role: "img", tabindex: 0 }, fig);
    svg.setAttribute("aria-label", (spec.title || "") + " 선 그래프. 값은 아래 표로 볼 수 있습니다.");
    var all = [];
    spec.series.forEach(function (s) { all = all.concat(s.values.filter(function (v) { return v !== null; })); });
    if (spec.target) all.push(spec.target.value);
    var tk = ticks(Math.min(0, Math.min.apply(null, all)), Math.max.apply(null, all), 4);
    var left = leftMargin(svg, tk, spec.unit);
    // End labels: only when series separate at the right edge (no stacking).
    var n = spec.x.length, endLabels = spec.series.length <= 4;
    var right = W - 8;
    var plotTop = top, plotBottom = H - bottom;
    var sy = function (v) { return plotBottom - (v - tk[0]) / (tk[tk.length - 1] - tk[0]) * (plotBottom - plotTop); };
    var ends = spec.series.map(function (s, i) {
      var j = s.values.length - 1; while (j >= 0 && s.values[j] === null) j--;
      return { i: i, y: sy(s.values[j]), text: (spec.series.length > 1 ? s.name + " " : "") + fmt(s.values[j], spec.unit) };
    });
    if (endLabels) {
      var sorted = ends.slice().sort(function (a, b) { return a.y - b.y; });
      for (var q = 1; q < sorted.length; q++) if (sorted[q].y - sorted[q - 1].y < 14) { endLabels = false; break; }
    }
    if (endLabels) right = W - 8 - Math.max.apply(null, ends.map(function (e) { return textWidth(svg, e.text, FONT, 600); })) - 10;
    var step = (right - left) / Math.max(1, n - 1);
    var sx = function (i) { return n === 1 ? (left + right) / 2 : left + i * step; };
    yAxis(svg, sy, left, right, tk, spec.unit);
    var every = Math.ceil(n / 8);
    spec.x.forEach(function (x, i) {
      if (i % every === 0 || i === n - 1) label(svg, sx(i), H - 8, x, { anchor: i === 0 ? "start" : i === n - 1 ? "end" : "middle" });
    });
    if (spec.target) {
      var ty = sy(spec.target.value);
      el("line", { x1: left, x2: right, y1: ty, y2: ty, "stroke-width": 1 }, svg).style.stroke = "var(--steel)";
      label(svg, left + 4, ty + 9, spec.target.label || "목표 " + fmt(spec.target.value, spec.unit), { size: 10 });
    }
    var order = spec.series.map(function (s, i) { return i; });
    if (spec.emphasis) order.sort(function (a, b) { return emph(spec, spec.series[a].name) - emph(spec, spec.series[b].name); });
    var colOf = function (i) { var s = spec.series[i]; return emph(spec, s.name) ? color(s, i) : "var(--viz-muted)"; };
    order.forEach(function (i) {
      var s = spec.series[i], d = "", started = false;
      s.values.forEach(function (v, k) {
        if (v === null) { started = false; return; }
        d += (started ? "L" : "M") + sx(k).toFixed(1) + "," + sy(v).toFixed(1); started = true;
      });
      if (spec.series.length === 1) {
        var a = d + "L" + sx(s.values.length - 1) + "," + sy(tk[0]) + "L" + sx(0) + "," + sy(tk[0]) + "Z";
        var area = el("path", { d: a, "fill-opacity": 0.1 }, svg); area.style.fill = colOf(i);
      }
      var p = el("path", { d: d, fill: "none", "stroke-width": 2, "stroke-linejoin": "round", "stroke-linecap": "round" }, svg);
      p.style.stroke = colOf(i);
      var e = ends[i], last = s.values.length - 1; while (s.values[last] === null) last--;
      var dot = el("circle", { cx: sx(last), cy: e.y, r: 4, "stroke-width": 2 }, svg);
      dot.style.fill = colOf(i); dot.style.stroke = "var(--viz-surface)";
      if (endLabels && (emph(spec, s.name) || spec.series.length <= 2))
        label(svg, sx(last) + 8, e.y, e.text, { weight: 600, fill: "var(--ink)" });
    });
    // Crosshair + tooltip: snaps to the nearest x; keyboard arrows move it.
    var tip = tooltip(fig), cross = el("line", { y1: plotTop, y2: plotBottom, "stroke-width": 1, visibility: "hidden" }, svg);
    cross.style.stroke = "var(--viz-axis)";
    var cur = -1;
    function show(k) {
      cur = Math.max(0, Math.min(n - 1, k));
      cross.setAttribute("x1", sx(cur)); cross.setAttribute("x2", sx(cur)); cross.setAttribute("visibility", "visible");
      var pt = toPx(svg, fig, sx(cur), plotTop + 10);
      tip.show(spec.x[cur], spec.series.map(function (s, i) { return { name: s.name, value: fmt(s.values[cur], spec.unit), color: colOf(i) }; }), pt[0], pt[1]);
    }
    function hide() { cross.setAttribute("visibility", "hidden"); tip.hide(); }
    var hit = el("rect", { x: left - step / 2, y: 0, width: right - left + step, height: H, fill: "transparent" }, svg);
    hit.addEventListener("pointermove", function (ev) {
      var r = svg.getBoundingClientRect(), x = (ev.clientX - r.left) * W / r.width;
      show(Math.round((x - left) / step));
    });
    hit.addEventListener("pointerleave", hide);
    svg.addEventListener("focus", function () { show(cur < 0 ? n - 1 : cur); });
    svg.addEventListener("blur", hide);
    svg.addEventListener("keydown", function (ev) {
      if (ev.key === "ArrowLeft") { show(cur - 1); ev.preventDefault(); }
      if (ev.key === "ArrowRight") { show(cur + 1); ev.preventDefault(); }
    });
    table(fig, spec);
  }

  // ── Vertical columns (one or more series) ─────────────────────────────
  function bar(fig, spec) {
    legend(fig, spec, "box");
    var H = spec.height || 220, top = 16, bottom = 24;
    var svg = el("svg", { class: "plot", viewBox: "0 0 " + W + " " + H, role: "img" }, fig);
    svg.setAttribute("aria-label", (spec.title || "") + " 막대 그래프. 값은 아래 표로 볼 수 있습니다.");
    var all = [0];
    spec.series.forEach(function (s) { all = all.concat(s.values); });
    var tk = ticks(Math.min.apply(null, all), Math.max.apply(null, all), 4);
    var left = leftMargin(svg, tk, spec.unit), right = W - 8;
    var sy = function (v) { return (H - bottom) - (v - tk[0]) / (tk[tk.length - 1] - tk[0]) * (H - bottom - top); };
    yAxis(svg, sy, left, right, tk, spec.unit);
    var n = spec.x.length, m = spec.series.length, band = (right - left) / n;
    var bw = Math.min(24, (band * 0.6 - (m - 1) * 2) / m);
    var tip = tooltip(fig), single = m === 1 && n <= 12;
    spec.x.forEach(function (x, i) {
      var cx = left + band * i + band / 2, gx = cx - (m * bw + (m - 1) * 2) / 2;
      label(svg, cx, H - 8, x, { anchor: "middle" });
      spec.series.forEach(function (s, j) {
        var v = s.values[i], y0 = sy(0), y1 = sy(v);
        var g = el("g", { class: "hit", tabindex: 0 }, svg);
        g.setAttribute("aria-label", x + " " + s.name + " " + fmt(v, spec.unit));
        el("rect", { x: gx + j * (bw + 2) - 4, y: top, width: bw + 8, height: H - bottom - top, fill: "transparent" }, g);
        var mk = el("path", { class: "mark", d: v >= 0 ? barPath(gx + j * (bw + 2), y1, bw, y0 - y1, "up") : barPath(gx + j * (bw + 2), y0, bw, y1 - y0, "none") }, g);
        mk.style.fill = color(s, j);
        if (single) label(svg, gx + bw / 2, y1 - 8, fmt(v), { anchor: "middle", fill: "var(--ink)", weight: 600, size: 10 });
        var on = function () { var pt = toPx(svg, fig, gx + j * (bw + 2) + bw, y1); tip.show(x, [{ name: s.name, value: fmt(v, spec.unit), color: color(s, j) }], pt[0], pt[1]); };
        g.addEventListener("pointerenter", on); g.addEventListener("focus", on);
        g.addEventListener("pointerleave", tip.hide); g.addEventListener("blur", tip.hide);
      });
    });
    table(fig, spec);
  }

  // ── Horizontal bars: hbar (one series), stacked, diverge ──────────────
  function hbars(fig, spec, mode) {
    legend(fig, spec, "box");
    var rowH = 28, bh = 16, top = 4, n = spec.x.length;
    var H = top + n * rowH + (mode === "stacked" && spec.percent ? 4 : 22);
    var svg = el("svg", { class: "plot", viewBox: "0 0 " + W + " " + H, role: "img" }, fig);
    svg.setAttribute("aria-label", (spec.title || "") + " 가로 막대 그래프. 값은 아래 표로 볼 수 있습니다.");
    var catW = Math.ceil(Math.max.apply(null, spec.x.map(function (x) { return textWidth(svg, x); }))) + 12;
    var totals = spec.x.map(function (_, i) { return spec.series.reduce(function (a, s) { return a + (s.values[i] || 0); }, 0); });
    var vals = spec.series[0].values;
    var lo = 0, hi;
    if (mode === "stacked") hi = spec.percent ? 100 : Math.max.apply(null, totals);
    else { lo = Math.min(0, Math.min.apply(null, vals)); hi = Math.max(0, Math.max.apply(null, vals)); }
    var tipW = mode === "stacked" ? 0 : Math.max.apply(null, vals.map(function (v) { return textWidth(svg, (v > 0 && mode === "diverge" ? "+" : "") + fmt(v, spec.unit), 10, 600); })) + 8;
    // Negative bars carry their value on the left, so leave room between the names and the bars.
    var left = catW + (lo < 0 ? tipW : 0), right = W - 8 - tipW;
    var tk = mode === "stacked" && spec.percent ? [0, 25, 50, 75, 100] : ticks(lo, hi, Math.max(2, Math.min(5, Math.floor((right - left) / 70))));
    var sx = function (v) { return left + (v - tk[0]) / (tk[tk.length - 1] - tk[0]) * (right - left); };
    if (!(mode === "stacked" && spec.percent)) tk.forEach(function (v) {
      el("line", { x1: sx(v), x2: sx(v), y1: top, y2: top + n * rowH, "stroke-width": 1, "shape-rendering": "crispEdges" }, svg).style.stroke = v === 0 ? "var(--viz-axis)" : "var(--viz-grid)";
      label(svg, sx(v), H - 8, fmt(v, spec.unit), { anchor: "middle" });
    });
    var tip = tooltip(fig);
    spec.x.forEach(function (x, i) {
      var y = top + i * rowH + (rowH - bh) / 2;
      label(svg, 0, y + bh / 2, x, { fill: "var(--slate)" });
      if (mode === "stacked") {
        var acc = 0, segs = spec.series.length;
        spec.series.forEach(function (s, j) {
          var v = s.values[i] || 0, share = spec.percent ? v / totals[i] * 100 : v;
          var x0 = sx(acc) + (j ? 1 : 0), x1 = sx(acc + share) - (j < segs - 1 ? 1 : 0); acc += share;
          if (x1 - x0 <= 0) return;
          var g = el("g", { class: "hit", tabindex: 0 }, svg);
          g.setAttribute("aria-label", x + " " + s.name + " " + fmt(v, spec.unit));
          var dir = j === segs - 1 ? "right" : j === 0 ? "left" : "none";
          var mk = el("path", { class: "mark", d: barPath(x0, y, x1 - x0, bh, segs === 1 ? "right" : dir) }, g); mk.style.fill = color(s, j);
          var txt = spec.percent ? Math.round(share) + "%" : fmt(v);
          if (textWidth(svg, txt, 10, 600) + 10 < x1 - x0) {
            label(svg, (x0 + x1) / 2, y + bh / 2, txt, { anchor: "middle", size: 10, weight: 600, fill: onFill(color(s, j)) });
          }
          var on = function () { var pt = toPx(svg, fig, x1, y); tip.show(x, [{ name: s.name, value: fmt(v, spec.unit) + (spec.percent ? " (" + Math.round(share) + "%)" : ""), color: color(s, j) }], pt[0], pt[1]); };
          g.addEventListener("pointerenter", on); g.addEventListener("focus", on);
          g.addEventListener("pointerleave", tip.hide); g.addEventListener("blur", tip.hide);
        });
      } else {
        var v = vals[i], z = sx(0), xe = sx(v), s0 = spec.series[0];
        var fill = mode === "diverge" ? (v >= 0 ? "var(--viz-pos)" : "var(--viz-neg)") : (emph(spec, x) ? color(s0, 0) : "var(--viz-muted)");
        var g2 = el("g", { class: "hit", tabindex: 0 }, svg);
        g2.setAttribute("aria-label", x + " " + fmt(v, spec.unit));
        el("rect", { x: left, y: y - 4, width: right - left, height: bh + 8, fill: "transparent" }, g2);
        var mk2 = el("path", { class: "mark", d: v >= 0 ? barPath(z, y, xe - z, bh, "right") : barPath(xe, y, z - xe, bh, "left") }, g2);
        mk2.style.fill = fill;
        label(svg, v >= 0 ? xe + 6 : xe - 6, y + bh / 2, (mode === "diverge" && v > 0 ? "+" : "") + fmt(v, spec.unit), { anchor: v >= 0 ? "start" : "end", weight: 600, size: 10, fill: "var(--ink)" });
        var on2 = function () { var pt = toPx(svg, fig, xe, y); tip.show(x, [{ name: s0.name, value: fmt(v, spec.unit), color: fill }], pt[0], pt[1]); };
        g2.addEventListener("pointerenter", on2); g2.addEventListener("focus", on2);
        g2.addEventListener("pointerleave", tip.hide); g2.addEventListener("blur", tip.hide);
      }
    });
    table(fig, spec);
  }

  // ── Sparkline in a stat tile ───────────────────────────────────────────
  function spark(svg) {
    var v = svg.getAttribute("data-values").split(",").map(Number), n = v.length;
    var w = Math.round(svg.getBoundingClientRect().width) || 120, h = 28;
    svg.setAttribute("viewBox", "0 0 " + w + " " + h);
    svg.setAttribute("aria-hidden", "true");
    var lo = Math.min.apply(null, v), hi = Math.max.apply(null, v), span = hi - lo || 1;
    var px = function (i) { return 4 + i * (w - 8) / (n - 1); }, py = function (x) { return h - 4 - (x - lo) / span * (h - 8); };
    var d = v.map(function (x, i) { return (i ? "L" : "M") + px(i).toFixed(1) + "," + py(x).toFixed(1); }).join("");
    var p = el("path", { d: d, fill: "none", "stroke-width": 1.5, "stroke-linejoin": "round", "stroke-linecap": "round" }, svg);
    p.style.stroke = "var(--viz-muted)";
    var c = el("circle", { cx: px(n - 1), cy: py(v[n - 1]), r: 3 }, svg);
    c.style.fill = "var(--viz-1)";
  }

  function render() {
    document.querySelectorAll("figure.viz[data-chart]").forEach(function (fig) {
      var src = fig.querySelector('script[type="application/json"]');
      if (!src || fig.getAttribute("data-rendered")) return;
      var spec = JSON.parse(src.textContent);
      var t = fig.querySelector(".viz-title"); spec.title = t ? t.textContent : "";
      var kind = fig.getAttribute("data-chart");
      var cs = getComputedStyle(fig);
      W = Math.max(280, Math.round(fig.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight)));
      if (kind === "line") line(fig, spec);
      else if (kind === "bar") bar(fig, spec);
      else if (kind === "hbar" || kind === "stacked" || kind === "diverge") hbars(fig, spec, kind);
      note(fig, spec);
      fig.setAttribute("data-rendered", "1");
    });
    document.querySelectorAll("svg.spark[data-values]").forEach(function (s) { if (!s.childNodes.length) spark(s); });
  }
  (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(render);
})();
