"""Colour-contrast check (WCAG 2.1 AA: 4.5:1 for text, 3:1 for large text ≥ 24 px or ≥ 18.66 px bold, 3:1 for UI borders is
NOT checked here). Walks every visible element with its own text in a set of views, in both languages, resolves the
effective background by climbing ancestors (alpha composited), and reports every text/background pair under the limit.
Pairs over a background image or gradient are listed separately for a manual look.
Usage: python3 -I check_contrast.py <app_dir> [out.json]"""
import json, sys
from playwright.sync_api import sync_playwright
APP = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else "contrast.json"

JS = r"""
() => {
  const parse = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const v = m[1].split(",").map(parseFloat); return {r:v[0],g:v[1],b:v[2],a:v.length>3?v[3]:1}; };
  const lum = c => { const f = x => { x/=255; return x<=0.03928? x/12.92 : Math.pow((x+0.055)/1.055,2.4); }; return 0.2126*f(c.r)+0.7152*f(c.g)+0.0722*f(c.b); };
  const over = (fg, bg) => ({ r: fg.r*fg.a + bg.r*(1-fg.a), g: fg.g*fg.a + bg.g*(1-fg.a), b: fg.b*fg.a + bg.b*(1-fg.a), a: 1 });
  const ratio = (a, b) => { const l1 = lum(a), l2 = lum(b); return (Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05); };
  const hex = c => "#" + [c.r,c.g,c.b].map(x => Math.round(x).toString(16).padStart(2,"0")).join("");
  const visible = el => { const r = el.getBoundingClientRect(); if (r.width < 1 || r.height < 1) return false;
    let e = el; while (e && e.nodeType === 1) { const s = getComputedStyle(e); if (s.display === "none" || s.visibility === "hidden" || parseFloat(s.opacity) === 0) return false; e = e.parentElement; } return true; };
  const bgOf = el => {
    // climb until an opaque colour is reached; note any image/gradient on the way
    let e = el, acc = null, img = null;
    while (e && e.nodeType === 1) {
      const s = getComputedStyle(e);
      if (s.backgroundImage && s.backgroundImage !== "none") img = img || (e.className && typeof e.className === "string" ? e.className.split(" ")[0] : e.tagName.toLowerCase());
      const c = parse(s.backgroundColor);
      if (c && c.a > 0) { acc = acc ? over(acc, c) : c; if (acc.a >= 0.999) break; }
      e = e.parentElement;
    }
    if (!acc) acc = {r:255,g:255,b:255,a:1}; else if (acc.a < 0.999) acc = over(acc, {r:255,g:255,b:255,a:1});
    return {bg: acc, img};
  };
  const out = [];
  const seen = new Set();
  const all = document.querySelectorAll("body *");
  for (const el of all) {
    if (["SCRIPT","STYLE","svg","path","circle","rect","line","polyline","polygon","g","defs","use","IMG","CANVAS"].includes(el.tagName)) continue;
    let own = ""; for (const n of el.childNodes) if (n.nodeType === 3) own += n.textContent;
    own = own.trim(); if (!own) continue;
    if (!visible(el)) continue;
    const s = getComputedStyle(el);
    let fg = parse(s.color); if (!fg) continue;
    const {bg, img} = bgOf(el);
    if (fg.a < 1) fg = over(fg, bg);
    // text-shadow or stroke can help; just note it
    const size = parseFloat(s.fontSize), weight = parseInt(s.fontWeight) || 400;
    const large = size >= 24 || (size >= 18.66 && weight >= 700);
    const need = large ? 3 : 4.5;
    const r = ratio(fg, bg);
    const cls = (typeof el.className === "string" && el.className) ? "." + el.className.trim().split(/\s+/).slice(0,2).join(".") : "";
    const key = el.tagName.toLowerCase() + cls + "|" + hex(fg) + "|" + hex(bg) + "|" + (img||"");
    if (seen.has(key)) continue; seen.add(key);
    out.push({ el: el.tagName.toLowerCase() + cls, text: own.slice(0, 40), fg: hex(fg), bg: hex(bg), ratio: Math.round(r*100)/100, need, size: Math.round(size*10)/10, weight, img, shadow: s.textShadow !== "none", ok: r >= need });
  }
  // SVG text (map labels): fill against paper; stroke/halo noted
  for (const t of document.querySelectorAll("svg text")) {
    if (!visible(t)) continue;
    const s = getComputedStyle(t); const fg = parse(s.fill); if (!fg || fg.a === 0) continue;
    const {bg} = bgOf(t.ownerSVGElement || t);
    const r = ratio(fg.a < 1 ? over(fg, bg) : fg, bg);
    const cls = (t.getAttribute("class")||"").split(/\s+/).slice(0,2).join(".");
    const key = "svgtext." + cls + "|" + hex(fg) + "|" + hex(bg);
    if (seen.has(key)) continue; seen.add(key);
    const size = parseFloat(s.fontSize), weight = parseInt(s.fontWeight) || 400;
    const need = (size >= 24 || (size >= 18.66 && weight >= 700)) ? 3 : 4.5;
    out.push({ el: "svg text." + cls, text: (t.textContent||"").trim().slice(0,40), fg: hex(fg), bg: hex(bg), ratio: Math.round(r*100)/100, need, size, weight, img: "map", shadow: s.stroke !== "none" && parseFloat(s.strokeWidth) > 0, ok: r >= need });
  }
  return out;
}
"""

VIEWS = [
    ("world", "#/", []),
    ("uk", "#/uk", []),
    ("region", "#/region/TLI", []),
    ("place", "#/place/baker-street", []),
    ("place-photo", "#/place/tintagel-castle", []),
    ("book", "#/book/persuasion", []),
    ("book-orig", "#/book/sir-gawain-green-knight", ["click:.orig-toggle"]),
    ("author", "#/author/Jane%20Austen", []),
    ("travel", "#/travel", []),
    ("reading", "#/reading", []),
    ("search", "#/uk", ["fill:#search-input:Dickens"]),
    ("legend", "#/uk", ["click:.legend-flags-head"]),
    ("shelf", "#/reading", ["seed-faves"]),
    ("open-book", "#/reading", ["seed-faves", "click:.shelf-book"]),
]

SEED = """() => { localStorage.setItem('ra.faves', JSON.stringify(['persuasion','jane-eyre','wuthering-heights','great-expectations']));
  localStorage.setItem('ra.wishlist', JSON.stringify(['baker-street'])); localStorage.setItem('ra.visited', JSON.stringify(['tintagel-castle']));
  localStorage.setItem('ra.shelf', JSON.stringify({'persuasion':'read','dracula':'want'})); }"""

def run_steps(pg, steps):
    for st in steps:
        try:
            if st == "seed-faves":
                pg.evaluate(SEED); pg.reload(); pg.wait_for_timeout(900)
            elif st.startswith("click:"):
                pg.click(st[6:], timeout=3000); pg.wait_for_timeout(1500)
            elif st.startswith("fill:"):
                _, sel, val = st.split(":", 2); pg.fill(sel, val); pg.wait_for_timeout(900)
        except Exception as e:
            print("  step failed:", st, str(e).split("\n")[0][:80])

results = {}
with sync_playwright() as p:
    br = p.chromium.launch()
    for lang in ("en", "zh"):
        pg = br.new_page(viewport={"width": 1440, "height": 900})
        pg.goto(f"file://{APP}/index.html?intro=0#/uk"); pg.wait_for_timeout(900)
        if lang == "zh":
            pg.click("#lang-toggle"); pg.wait_for_timeout(700)
        for name, route, steps in VIEWS:
            pg.goto(f"file://{APP}/index.html?intro=0{route}"); pg.wait_for_timeout(1300)
            run_steps(pg, steps)
            rows = pg.evaluate(JS)
            results[f"{lang}/{name}"] = rows
            bad = [r for r in rows if not r["ok"]]
            print(f"{lang}/{name}: {len(rows)} pairs, {len(bad)} under AA")
        pg.close()
    br.close()

json.dump(results, open(OUT, "w"), ensure_ascii=False, indent=1)
# summary: unique failing pairs across views
agg = {}
for v, rows in results.items():
    for r in rows:
        if r["ok"]: continue
        k = (r["el"], r["fg"], r["bg"], r["img"] or "")
        a = agg.setdefault(k, dict(r, views=[]))
        a["views"].append(v)
print("\nFAILING PAIRS (unique):", len(agg))
for k, a in sorted(agg.items(), key=lambda kv: kv[1]["ratio"]):
    print(f'{a["ratio"]:5.2f} (need {a["need"]})  {a["el"]:42s} fg {a["fg"]} on {a["bg"]}' + (f'  [over {a["img"]}]' if a["img"] else "") + (" shadow" if a["shadow"] else "") + f'  {a["size"]}px/{a["weight"]}  e.g. "{a["text"]}"  in {len(a["views"])} views')
