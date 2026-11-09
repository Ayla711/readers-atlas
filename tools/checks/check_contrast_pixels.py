"""Pixel-level contrast for text drawn over the map (where the CSS background is not what the eye sees).
For each matching element: screenshot its box at 2x, split pixels into text (near the text colour) and background,
and report the contrast of the text colour against the median background and against the worst 10 % of background
pixels (the darkest or lightest patch the text actually crosses). Usage: python3 -I check_contrast_pixels.py <app_dir>"""
import io, sys, json
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
APP = sys.argv[1]

def lum(rgb):
    c = np.asarray(rgb, dtype=float) / 255
    c = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]
def ratio(l1, l2):
    hi, lo = np.maximum(l1, l2), np.minimum(l1, l2)
    return (hi + 0.05) / (lo + 0.05)
def hx(s):
    s = s.lstrip("#"); return tuple(int(s[i:i+2], 16) for i in (0, 2, 4))

TARGETS = [  # selector, nominal text colour, label
    (".crumbs button", "#5f6873", "breadcrumb links"),
    (".crumbs span:not(.sep)", "#2b343c", "breadcrumb current"),
    (".crumbs .sep", "#bcae92", "breadcrumb ›"),
    (".map-title", "#26313a", "map title"),
    (".attribution", "#5f6873", "attribution line"),
    (".cover-tagline", "#64453f", "cover tagline"),
    (".region-label", "#64453f", "region names"),
    (".unit-label", "#64453f", "county names"),
    (".marker-label", "#64453f", "place names"),
    (".compass .c-n", "#64453f", "compass N"),
    (".legend", "#2b343c", "legend text"),
]
VIEWS = [("world", "#/"), ("uk", "#/uk"), ("region", "#/region/TLI"), ("place", "#/place/baker-street"), ("region-sw", "#/region/TLK")]

rows = []
with sync_playwright() as p:
    br = p.chromium.launch()
    for lang in ("en", "zh"):
        pg = br.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
        pg.goto(f"file://{APP}/index.html?intro=0#/uk"); pg.wait_for_timeout(900)
        if lang == "zh": pg.click("#lang-toggle"); pg.wait_for_timeout(700)
        for vname, route in VIEWS:
            pg.goto(f"file://{APP}/index.html?intro=0{route}"); pg.wait_for_timeout(1500)
            shot = Image.open(io.BytesIO(pg.screenshot())).convert("RGB")
            A = np.asarray(shot)
            for sel, fgc, label in TARGETS:
                boxes = pg.evaluate("""(sel) => [...document.querySelectorAll(sel)].map(e => { const r = e.getBoundingClientRect();
                    const s = getComputedStyle(e); return {x:r.x,y:r.y,w:r.width,h:r.height, vis: r.width>0 && r.height>0 && s.visibility!=='hidden' && parseFloat(s.opacity)>0,
                    fg: s.fill && s.fill!=='none' && e.ownerSVGElement ? s.fill : s.color, fs: parseFloat(s.fontSize)}; }).filter(b => b.vis)""", sel)
                for b in boxes[:40]:
                    x0, y0 = int(b["x"] * 2), int(b["y"] * 2); x1, y1 = int((b["x"] + b["w"]) * 2), int((b["y"] + b["h"]) * 2)
                    x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, A.shape[1]), min(y1, A.shape[0])
                    if x1 - x0 < 4 or y1 - y0 < 4: continue
                    crop = A[y0:y1, x0:x1].reshape(-1, 3).astype(float)
                    import re as _re
                    m = _re.match(r"rgba?\(([^)]+)\)", b["fg"] or "")
                    fg = np.array([float(v) for v in m.group(1).split(",")[:3]]) if m else np.array(hx(fgc), dtype=float)
                    d = np.linalg.norm(crop - fg, axis=1)
                    text_px = crop[d < 60]; bg_px = crop[d >= 110]
                    if len(text_px) < 5 or len(bg_px) < 20: continue
                    lf = lum(fg); lb = lum(bg_px)
                    r = ratio(lf, lb)
                    rows.append(dict(view=f"{lang}/{vname}", what=label, sel=sel, n_text=int(len(text_px)), bg_median=[int(v) for v in np.median(bg_px, axis=0)],
                                     r_median=round(float(np.median(r)), 2), r_p10=round(float(np.percentile(r, 10)), 2), fs=b["fs"]))
        pg.close()
    br.close()

json.dump(rows, open("contrast_pixels.json", "w"), indent=1)
# summary per label: worst p10 and typical median
agg = {}
for r in rows:
    a = agg.setdefault(r["what"], dict(p10=[], med=[], views=set()))
    a["p10"].append(r["r_p10"]); a["med"].append(r["r_median"]); a["views"].add(r["view"])
print(f'{"text":22s} {"median":>7s} {"worst p10":>10s} {"min median":>11s}  samples')
for k, a in agg.items():
    print(f'{k:22s} {np.median(a["med"]):7.2f} {min(a["p10"]):10.2f} {min(a["med"]):11.2f}  {len(a["p10"])}')
