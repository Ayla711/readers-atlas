"""Label rules from docs/map-layers.md (3, 3.2, 10): no overlaps between shown labels, pins, map furniture and the panel."""
import sys
from playwright.sync_api import sync_playwright
APP = sys.argv[1]
RECTS = """(sel) => [...document.querySelectorAll(sel)].filter(e => e.checkVisibility({opacityProperty: true, visibilityProperty: true}))
  .map(e => { const r = e.getBoundingClientRect(); return {t: (e.textContent || e.className.baseVal || e.className || '').toString().slice(0, 30), x: r.left, y: r.top, w: r.width, h: r.height}; })
  .filter(r => r.w > 0 && r.h > 0)"""
def ov(a, b, pad=0):
    return a["x"] < b["x"] + b["w"] - pad and b["x"] < a["x"] + a["w"] - pad and a["y"] < b["y"] + b["h"] - pad and b["y"] < a["y"] + a["h"] - pad
fails = []
with sync_playwright() as p:
    br = p.chromium.launch()
    # 3.2: region names on the UK overview
    for w, h in [(1280, 800), (1440, 900), (1920, 1080)]:
        for lang in ["en", "zh"]:
            pg = br.new_page(viewport={"width": w, "height": h})
            pg.goto(f"file://{APP}/index.html?intro=0#/uk"); pg.wait_for_timeout(900)
            if lang == "zh": pg.click("#lang-toggle"); pg.wait_for_timeout(700)
            R = pg.evaluate(RECTS, ".region-label")
            others = [("pin", r) for r in pg.evaluate(RECTS, ".marker .m-shape")]
            for sel in [".titleblock", ".legend", ".map-controls", ".compass", ".attribution", "#panel"]:
                others += [(sel, r) for r in pg.evaluate(RECTS, sel)]
            bad = [(a["t"], b["t"]) for i, a in enumerate(R) for b in R[i + 1:] if ov(a, b)]
            bad += [(a["t"], k + ":" + b["t"]) for a in R for k, b in others if ov(a, b)]
            print(f"UK {w}x{h} {lang}: {len(R)} region names shown, overlaps: {bad or 'none'}")
            if len(R) < 11 or bad: fails.append((w, h, lang))
            pg.close()
    # 3 / 10: county names never cover place names; shown place names never cover each other
    pg = br.new_page(viewport={"width": 1440, "height": 900})
    for route in ["#/region/TLI", "#/place/baker-street", "#/region/TLE", "#/region/TLH", "#/region/TLM", "#/region/TLD",
                  "#/region/TLJ", "#/region/TLK", "#/region/TLF", "#/region/TLG", "#/region/TLL", "#/place/bath", "#/place/oxford", "#/book/three-men-in-a-boat"]:
        pg.goto(f"file://{APP}/index.html?intro=0{route}"); pg.wait_for_timeout(1100)
        U, M = pg.evaluate(RECTS, ".unit-label"), pg.evaluate(RECTS, ".marker-label")
        bad = [(u["t"], m["t"]) for u in U for m in M if ov(u, m)] + [(a["t"], b["t"]) for i, a in enumerate(M) for b in M[i + 1:] if ov(a, b, 1)]
        print(f"{route:28} county names {len(U):2}, place names {len(M):2}, overlaps: {bad or 'none'}")
        if bad: fails.append(route)
    br.close()
print("\nRESULT:", "all clear" if not fails else f"FAIL {fails}")
