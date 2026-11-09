"""No shown place name may cover another place's marker; names may not cover each other (map-layers.md 3, rule 1)."""
import sys
from playwright.sync_api import sync_playwright
APP = sys.argv[1]
JS = """() => {
  const vis = (e) => e.checkVisibility({opacityProperty: true, visibilityProperty: true});
  const ms = [...document.querySelectorAll('#map .marker')].filter(g => g.style.display !== 'none' && vis(g.querySelector('.m-shape')));
  const dots = ms.map(g => ({id: g.dataset.id, r: g.querySelector('.m-shape').getBoundingClientRect()}));
  const names = ms.filter(g => g.querySelector('.marker-label').style.display !== 'none').map(g => ({id: g.dataset.id, r: g.querySelector('.marker-label').getBoundingClientRect()}));
  const ov = (a, b) => a.left < b.right - 1 && b.left < a.right - 1 && a.top < b.bottom - 1 && b.top < a.bottom - 1;
  const bad = [];
  for (const n of names) for (const d of dots) if (n.id !== d.id && ov(n.r, d.r)) bad.push(n.id + ' covers ' + d.id);
  for (let i = 0; i < names.length; i++) for (let j = i + 1; j < names.length; j++) if (ov(names[i].r, names[j].r)) bad.push(names[i].id + ' / ' + names[j].id);
  return {bad, names: names.length};
}"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, h in [(1000, 700), (1440, 900)]:
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.goto(f"file://{APP}/index.html?intro=0#/uk"); pg.wait_for_timeout(600)
        ids = pg.evaluate("window.RA_DATA.places.map(p => p.id)")
        routes = [f"#/region/{r}" for r in ["TLC","TLD","TLE","TLF","TLG","TLH","TLI","TLJ","TLK","TLL","TLM","TLN"]] + [f"#/place/{i}" for i in ids] + ["#/author/agatha-christie", "#/author/charles-dickens", "#/book/harry-potter-1"]
        bad, total = [], 0
        for r in routes:
            pg.evaluate(f"location.hash = '{r}'"); pg.wait_for_timeout(1100)
            res = pg.evaluate(JS); total += res["names"]
            bad += [(r, x) for x in res["bad"]]
        print(f"{w}x{h}: {len(routes)} views, {total} names shown, problems: {bad or 'none'}")
        pg.close()
    b.close()
