import sys, re, json
from playwright.sync_api import sync_playwright
APP = sys.argv[1]
CJK = re.compile(r"[぀-ヿ㐀-鿿＀-￯　-〿]")
# text outside the original-language quote blocks, which are meant to stay in the source language
JS = """() => { const r = document.body;
  const skip = [...r.querySelectorAll('[lang]:not([lang=en]), #lang-toggle')];
  skip.forEach(n => n.dataset.cjkHide = n.style.display, skip.forEach(n => n.style.display = 'none'));
  const t = r.innerText; skip.forEach(n => n.style.display = n.dataset.cjkHide); return t; }"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(f"file://{APP}/index.html?intro=0"); pg.wait_for_timeout(500)
    ids = pg.evaluate("() => ({r: window.RA_GEO.regions.map(r=>r.id), p: window.RA_DATA.places.map(p=>p.id), b: window.RA_DATA.books.map(b=>b.id)})")
    hits = {}
    def scan(route):
        pg.evaluate(f"() => {{ location.hash = '{route}'; }}"); pg.wait_for_timeout(120)
        txt = pg.evaluate(JS)
        for line in txt.split("\n"):
            if CJK.search(line): hits.setdefault(line.strip(), set()).add(route)
    for r in ids["r"]: scan(f"#/region/{r}")
    for x in ids["p"]: scan(f"#/place/{x}")
    for x in ids["b"]: scan(f"#/book/{x}")
    scan("#/travel"); scan("#/reading"); scan("#/uk")
    pg.goto(f"file://{APP}/index.html?intro=0"); pg.wait_for_timeout(600); scan("")
    # hover tooltips on every visible marker in the UK view
    pg.evaluate("() => location.hash = '#/uk'"); pg.wait_for_timeout(800)
    for m in pg.locator(".marker .m-shape").all()[:80]:
        try:
            m.hover(timeout=500); tip = pg.inner_text("#tooltip") if pg.locator("#tooltip").count() else ""
            if CJK.search(tip): hits.setdefault("tooltip: " + tip, set()).add("hover")
        except Exception: pass
    for q in ["London", "Cam", "Lao", "Tower", "Brontë", "Harry"]:
        pg.fill("#search-input", q); pg.wait_for_timeout(200)
        for t in pg.locator("#search-results li").all_inner_texts():
            if CJK.search(t): hits.setdefault(t.replace("\n", " | "), set()).add("search " + q)
    pg.fill("#search-input", "")
    print("lang:", pg.evaluate("document.documentElement.lang"))
    for k, v in sorted(hits.items()): print(repr(k[:110]), "<-", sorted(v)[:3], len(v))
    print("TOTAL distinct lines with CJK:", len(hits))
    b.close()
