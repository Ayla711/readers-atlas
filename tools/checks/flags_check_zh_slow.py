import json, subprocess, sys
from playwright.sync_api import sync_playwright
APP=sys.argv[1]
ids=json.loads(subprocess.check_output(["node","-e",f"global.window=global;require('{APP}/data/uk/places.js');console.log(JSON.stringify(window.RA_DATA.places.map(p=>p.id)))"]))
R="""(sel)=>[...document.querySelectorAll(sel)].filter(e=>e.checkVisibility({opacityProperty:true,visibilityProperty:true})).map(e=>{const r=e.getBoundingClientRect();return {t:(e.closest('.marker')?.dataset.id||''),x:r.left,y:r.top,w:r.width,h:r.height}}).filter(r=>r.w&&r.h)"""
ov=lambda a,b: a["x"]<b["x"]+b["w"]-1 and b["x"]<a["x"]+a["w"]-1 and a["y"]<b["y"]+b["h"]-1 and b["y"]<a["y"]+a["h"]-1
with sync_playwright() as p:
    br=p.chromium.launch(); pg=br.new_page(viewport={"width":1440,"height":900})
    pg.goto(f"file://{APP}/index.html?intro=0#/uk"); pg.wait_for_timeout(400)
    # every place gets a flag, the three kinds in turn
    itin=[{"place_id":i,"date":"2026-12-01","note":""} for i in ids[1::3]]
    pg.evaluate(f"localStorage.setItem('ra.visited', JSON.stringify({json.dumps(ids[0::3])})); localStorage.setItem('ra.itinerary', JSON.stringify({json.dumps(itin)})); localStorage.setItem('ra.lang', JSON.stringify('zh')); localStorage.setItem('ra.wishlist', JSON.stringify({json.dumps(ids[2::3])}))"); pg.reload(); pg.wait_for_timeout(1200)
    print("flags:", pg.evaluate("[...document.querySelectorAll('.marker .m-flag')].reduce((a,f)=>(a[f.dataset.kind]=(a[f.dataset.kind]||0)+1,a),{})"))
    bad=[]; views=0; names=0
    for r in ["TLC","TLD","TLE","TLF","TLG","TLH","TLI","TLJ","TLK","TLL","TLM","TLN"]+["p:"+i for i in ids[::3]]:
        pg.evaluate(f"location.hash='#/{'place/'+r[2:] if r.startswith('p:') else 'region/'+r}'"); pg.wait_for_timeout(1800); views+=1
        L=pg.evaluate(R,".marker-label"); F=pg.evaluate(R,".marker .m-flag-cloth")+pg.evaluate(R,".marker .m-flag-pole"); names+=len(L)  # map flags only, not the legend icons
        bad+=[(r,l["t"],f["t"]) for l in L for f in F if ov(l,f)]
    print(views,"views,",names,"names shown, names over flags:", bad[:6], len(bad))
    br.close()
