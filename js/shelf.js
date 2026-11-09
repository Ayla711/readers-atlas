/* The favourites bookshelf on the My books page (spec F9, 11-06; fixed places 11-07). Draws an SVG bookcase, two shelves a page, styled after the user's references: a pencil-drawn case with a thick top, thin posts and a footed
   base; outlined books with a blank label on the spine; warm browns with a few greyed cool spines.
   Books go on in the order they were favourited, like a real shelf being filled: each shelf from the left post, and a
   shelf is full only when the next book has no room on it (so about 10–13 standing books a shelf). Each book's size, colour, pose (standing, lying in a stack at the start of a shelf, or
   leaning back onto its neighbour or the post) and place are worked out from the books before it only, so adding a
   favourite never moves or recolours the books already there; it just goes on after the last one.
   window.RA_SHELF.html(items, page) returns the markup; after it is in the document call fit(root) so long titles shrink
   to their labels. items: [{ id, title, author }], oldest favourite first. */
window.RA_SHELF = (() => {
  "use strict";
  // spine colour, band colour, label tint: a warm brown set
  const PALETTE = [
    ["#a65a3a", "#7a3f27", "#f1dccb"], ["#c7a08a", "#9a7560", "#f6ebe0"], ["#5a3a2a", "#3d2619", "#e9d6c3"], ["#b07a4f", "#86593a", "#f3e3cf"],
    ["#8b4a2b", "#64331c", "#eed8c6"], ["#d4a574", "#a67b4e", "#f8ecd8"], ["#9c6b55", "#73493a", "#eedcd0"], ["#7d5a46", "#5a3f30", "#ecdccf"],
  ];
  // a few cool spines from the site's own colours (stamp blue, sea sage, ink slate, the "been" green), greyed down so they sit with the browns
  const COOL = [
    ["#7d93a3", "#5b7284", "#e9eef1"], ["#9cb0a5", "#768d81", "#eff3f0"], ["#7a8590", "#59646f", "#ebedef"], ["#869c8c", "#62786a", "#ecf1ed"],
  ];
  const W = 300, H = 330, IL = 26, IR = 274, LINE = "#5b4636";
  const FRAME = `stroke="${LINE}" stroke-width="1" stroke-linejoin="round"`;
  const THIN = `stroke="${LINE}" stroke-width=".55" stroke-linejoin="round"`;
  const WOOD = "#c9a37e", WOOD_DK = "#b8946f", BACK = "#e8d3b8", GRAIN = "#cdb08c";
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  // deterministic jitter so a book always looks the same
  const jit = (seed, amt) => { const x = Math.sin(seed * 9301 + 49297) * 233280; return (x - Math.floor(x) - 0.5) * 2 * amt; };
  const hash = (s) => { let h = 0; for (const c of s) h = (h * 31 + c.charCodeAt(0)) >>> 0; return h; };

  // Colours, worked out once over the whole shelf in the order books were added. Each author keeps one colour. Every fifth
  // new author (the 3rd, 8th, 13th…) gets a cool spine; the others a warm one picked from the author's name, moved on to the
  // next shade if it would match the book just before it.
  function colourMap(items) {
    const m = new Map();
    let n = 0, prev = null;
    for (const b of items) {
      if (!m.has(b.author)) {
        const set = n % 5 === 2 ? COOL : PALETTE;
        let i = hash(b.author) % set.length;
        if (prev && set[i] === prev) i = (i + 1) % set.length;
        m.set(b.author, set[i]);
        n++;
      }
      prev = m.get(b.author);
    }
    return m;
  }
  let colours = new Map();
  const colourOf = (author) => colours.get(author) || PALETTE[hash(author) % PALETTE.length];

  // A book's size never changes: thickness 16–28 and height 96–112 from its id, the same whether it stands or lies.
  const dims = (b) => { const k = hash(b.id); return { t: 22 + Math.round(jit(k % 977, 6)), h: 104 + Math.round(jit(k % 1223, 8)), k }; };
  const STACK_MAX = 108, ROW = [172, 294];
  const START = IL + 6, END = IR - 6;   // both shelves fill from the left post rightwards

  // Place every book in order. A shelf starts with a stack sometimes; a book may lean back onto the standing book before it,
  // or onto the post if it is first; a book that does not fit goes to the next shelf, and after the lower shelf to a new page.
  // (dir is kept so a right-to-left shelf could come back; both shelves now run left to right.)
  function layout(items) {
    const pages = [];
    let page = null, si = 0, cur = null;
    const newPage = () => { page = [[], []]; pages.push(page); si = 0; cur = shelf(0); };
    const shelf = (i) => ({ i, dir: 1, x: START, stack: [], stackDone: false, last: null, count: 0 });
    newPage();
    for (const b of items) {
      const d = dims(b);
      let placed = false;
      while (!placed) {   // a shelf is full only when the next book has no room on it
        const p = place(cur, b, d);
        if (p) { page[si].push(p); placed = true; break; }
        if (si === 0) { si = 1; cur = shelf(1); } else newPage();
      }
    }
    return pages;
  }
  // try to put book b on shelf state c; returns a placement or null when it does not fit
  function place(c, b, d) {
    const { dir } = c, y0 = ROW[c.i], room = (w) => dir > 0 ? c.x + w <= END : c.x - w >= END;
    // lying: only at the start of a shelf, up to three books, while nothing stands yet. A stack costs a book's length of
    // shelf, so it starts on about one shelf in three and, once started, usually grows to two or three
    const stacking = !c.stackDone && (c.stack.length ? d.k % 4 !== 0 : c.count === 0 && d.k % 3 === 0);
    if (stacking && c.stack.length < 3 && c.stack.reduce((a, e) => a + e.t, 0) + d.t <= STACK_MAX) {
      const len = d.h, sx = Math.round(jit(d.k % 311, 3));
      const base = c.stack.length ? c.stack[0].x0 : c.x;
      const xx = dir > 0 ? base + sx : base - len + sx;
      if (!c.stack.length && !room(len + 3)) return null;
      const y = y0 - c.stack.reduce((a, e) => a + e.t, 0) - d.t;
      c.stack.push({ t: d.t, len, x0: base, xx });
      c.count++;
      c.last = { kind: "lie" };
      return { b, kind: "lie", x: xx, y, w: len, h: d.t };
    }
    if (c.stack.length && !c.stackDone) {   // the stack is finished: standing books start after its widest book
      const edge = dir > 0 ? Math.max(...c.stack.map((e) => e.xx + e.len)) : Math.min(...c.stack.map((e) => e.xx));
      c.x = edge + dir * 3;
    }
    c.stackDone = true;
    // leaning back onto the standing book before it (or the post, if first), about one book in four
    const onPost = c.count === 0, prev = c.last;
    const lean = (onPost && d.k % 5 === 1) || (prev && prev.kind === "stand" && d.k % 4 === 0);
    if (lean) {
      const th = (9 + Math.abs(jit(d.k % 1409, 7))) * Math.PI / 180;
      const wall = onPost ? (dir > 0 ? IL + 0.5 : IR - 0.5) : prev.outer + (dir > 0 ? 0.5 : -0.5);
      const hp = onPost ? 999 : prev.h;
      // the pivot is the bottom corner nearest the support; the top corner rests on the support's face, or the book's edge on its top corner
      const off = d.h * Math.cos(th) <= hp ? d.h * Math.sin(th) : hp * Math.tan(th);
      const pivot = wall + dir * off;
      const reach = off + d.t * Math.cos(th) + 1.5;   // from the support to the far side of the book's base
      if (dir > 0 ? wall + reach <= END : wall - reach >= END) {   // no room to lean: it stands instead (below)
      c.x = pivot + dir * (d.t * Math.cos(th) + 1.5);
      c.count++;
      c.last = { kind: "lean" };
      const x0 = dir > 0 ? pivot : pivot - d.t;
      return { b, kind: "lean", x: x0, y: y0 - d.h, w: d.t, h: d.h, rot: -dir * th * 180 / Math.PI, px: pivot, py: y0 };
      }
    }
    if (!room(d.t + 1.5)) return null;
    const x0 = dir > 0 ? c.x : c.x - d.t;
    c.x += dir * (d.t + 1.5);
    c.count++;
    c.last = { kind: "stand", h: d.h, outer: dir > 0 ? x0 + d.t : x0 };
    return { b, kind: "stand", x: x0, y: y0 - d.h, w: d.t, h: d.h };
  }

  function html(items, page) {
    colours = colourMap(items);
    const pages = layout(items);
    page = Math.min(Math.max(0, page || 0), pages.length - 1);
    const pg = pages[page] || [[], []];
    let s = `<svg class="shelf" viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" role="list">`;
    s += `<rect x="${IL}" y="46" width="${IR - IL}" height="248" fill="${BACK}"/>`;
    for (let x = 38; x < 268; x += 13) s += `<line x1="${x + jit(x, 1)}" y1="47" x2="${x + jit(x + 1, 1)}" y2="293" stroke="${GRAIN}" stroke-width=".8"/>`;
    s += `<path d="M8 10 L292 9 L292 36 L8 37 Z" fill="${WOOD}" ${FRAME}/>`;
    s += `<path d="M18 37 L282 37 L279 47 L21 47 Z" fill="${WOOD_DK}" ${FRAME}/>`;
    s += `<path d="M18 46 L18 294 L26 294 L26 46 Z" fill="${WOOD}" ${FRAME}/>`;
    s += `<path d="M274 46 L274 294 L282 294 L282 46 Z" fill="${WOOD}" ${FRAME}/>`;
    for (const shelfBooks of pg) {
      for (const p of shelfBooks) {
        const sp = spine(p.b, p.x, p.y, p.w, p.h, p.kind === "lie");
        s += p.kind === "lean" ? `<g transform="rotate(${p.rot.toFixed(2)} ${p.px.toFixed(2)} ${p.py})">${sp}</g>` : sp;
      }
    }
    s += board(172, false) + board(294, true);
    s += `<path d="M14 310 L14 328 Q18 314 36 310 Z" fill="${WOOD_DK}" ${FRAME}/>`;
    s += `<path d="M286 310 L286 328 Q282 314 264 310 Z" fill="${WOOD_DK}" ${FRAME}/>`;
    s += `</svg>`;
    return { svg: s, page, pages: pages.length };
  }

  function board(yFront, full) {
    const x0 = full ? 4 : IL, x1 = full ? 296 : IR, t = full ? 16 : 7;
    return `<path d="M${x0} ${yFront} L${x1} ${yFront} L${x1} ${yFront + t} L${x0} ${yFront + t} Z" fill="${WOOD}" ${FRAME}/>`;
  }

  function spine(b, x, y, w, h, lying) {
    const [fill, dk, tint] = colourOf(b.author);
    const title = esc(b.title);
    let g = `<g class="shelf-book" role="listitem" tabindex="0" data-shelf-book="${esc(b.id)}"><title>${title} — ${esc(b.author)}</title>`;
    g += `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="1" fill="${fill}" ${THIN}/>`;
    if (!lying) {
      g += `<line x1="${x + 2.5}" y1="${y + 9}" x2="${x + w - 2.5}" y2="${y + 9}" stroke="${dk}" stroke-width="1"/><line x1="${x + 2.5}" y1="${y + 13}" x2="${x + w - 2.5}" y2="${y + 13}" stroke="${dk}" stroke-width="1"/>`;
      g += `<line x1="${x + 2.5}" y1="${y + h - 13}" x2="${x + w - 2.5}" y2="${y + h - 13}" stroke="${dk}" stroke-width="1"/><circle cx="${x + w / 2}" cy="${y + h - 6.5}" r="2" fill="none" stroke="${dk}" stroke-width=".8"/>`;
      const lx = x + 3.5, ly = y + 18, lw = w - 7, lh = h - 36;
      g += `<rect x="${lx}" y="${ly}" width="${lw}" height="${lh}" rx=".8" fill="${tint}" stroke="${dk}" stroke-width=".5"/>`;
      const fs = Math.min(10, lw - 1.5).toFixed(1);   // never wider than the label
      if (/[぀-ヿ㐀-鿿]/.test(b.title)) {
        g += `<text class="shelf-title" data-max="${lh - 6}" x="${lx + lw / 2}" y="${ly + lh / 2}" font-size="${fs}" style="writing-mode:vertical-rl;text-orientation:upright" text-anchor="middle">${title}</text>`;
      } else {
        g += `<text class="shelf-title" data-max="${lh - 6}" font-size="${Math.min(9.5, fs)}" transform="translate(${lx + lw / 2} ${ly + lh / 2}) rotate(90)" text-anchor="middle" dominant-baseline="central">${title}</text>`;
      }
    } else {
      g += `<line x1="${x + 9}" y1="${y + 2.5}" x2="${x + 9}" y2="${y + h - 2.5}" stroke="${dk}" stroke-width="1"/><line x1="${x + 13}" y1="${y + 2.5}" x2="${x + 13}" y2="${y + h - 2.5}" stroke="${dk}" stroke-width="1"/>`;
      g += `<line x1="${x + w - 13}" y1="${y + 2.5}" x2="${x + w - 13}" y2="${y + h - 2.5}" stroke="${dk}" stroke-width="1"/><circle cx="${x + w - 6.5}" cy="${y + h / 2}" r="2" fill="none" stroke="${dk}" stroke-width=".8"/>`;
      const lx = x + 18, ly = y + 2.5, lw = w - 36, lh = h - 5;
      g += `<rect x="${lx}" y="${ly}" width="${lw}" height="${lh}" rx=".8" fill="${tint}" stroke="${dk}" stroke-width=".5"/>`;
      g += `<text class="shelf-title" data-max="${lw - 6}" font-size="${Math.min(8, lh * 0.8).toFixed(1)}" x="${lx + lw / 2}" y="${ly + lh / 2 + 0.5}" text-anchor="middle" dominant-baseline="central">${title}</text>`;
    }
    return g + `</g>`;
  }

  // shrink long titles until they fit their label; squeeze as a last resort
  function fit(root) {
    for (const el of root.querySelectorAll("text.shelf-title")) {
      const max = parseFloat(el.dataset.max);
      let f = parseFloat(el.getAttribute("font-size"));
      while (el.getComputedTextLength() > max && f > 5.5) { f -= 0.5; el.setAttribute("font-size", f); }
      if (el.getComputedTextLength() > max) { el.setAttribute("textLength", max); el.setAttribute("lengthAdjust", "spacingAndGlyphs"); }
    }
  }
  return { html, fit };
})();
