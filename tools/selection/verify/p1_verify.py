"""Patch 1 (11-24 evening): verify every book already in the app that had 0 or 1 evidence item.
- Goodreads counts: verify/gr_1124.tsv (Goodreads autocomplete endpoint, largest work by that author, read 11-24)
- thegreatestbooks overall ranks 1-2000: verify/tgb_1124.tsv (read 11-24 from /page/1..80)
- genre sources found for poems/sagas: Norway literary canon 2007, Swedish culture canon 2025, Hungarian 2020 curriculum
Run in tools/selection: python3 -I verify/p1_verify.py   (then rebuild the 20 countries)"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import specio
def tier(n): return 3 if n >= 1_000_000 else 2 if n >= 100_000 else 1 if n >= 10_000 else 0
def dpts(r): return 2 if r <= 500 else 1 if r <= 2000 else 0
fmt = lambda n: format(n, ",")
# spec title -> tgb rank (only flagged rows; others were not in the top 2000)
TGB = {"William Tell":1325,"Little Dorrit":1434,"The Prelude":1575,"Pelle the Conqueror":1479,"Beowulf":642,"Confessions":118,
 "The Immoralist":477,"Njáls saga":1518,"The Interesting Narrative":1888,"The Fall":941,"Erewhon":704,"Dracula":56,
 "Murder on the Orient Express":470,"Anabasis":925,"Evenings on a Farm Near Dikanka":1656,"The White Guard":1742,
 "The Story of My Experiments with Truth":1541,"King Solomon's Mines":672}
EXTRA = {  # (cc, title): (points to add, note)
 ("hu","By the Danube (A Dunánál)"): ({"B":2}, "2020 年高中课程框架（9–12 年级）约瑟夫·阿蒂拉一节点名《在多瑙河边》（ELTE 网站上的框架文本）"),
 ("hu","The Great Plain (Az Alföld)"): ({"B":1}, "按 2020 课程框架写的学校课程里，5 年级“故乡、风景”单元的推荐篇目有《平原》（巴托尼亚罗姆学校课程）；框架原文没能打开，按推荐篇目记 1"),
 ("no","Peer Gynt"): ({"A2":3}, ""),
 ("no","Heimskringla"): ({"A2":3}, "挪威文学正典第 2 部《国王萨迦》"),
 ("no","Kristin Lavransdatter"): ({"A2":3}, "正典选的是第一部《花冠》"),
 ("no","The Alberta Trilogy"): ({"A2":3}, "正典选的是第二部《阿尔贝塔与自由》"),
 ("se","Fredman's Epistles"): ({"A2":3}, "文化正典收第 30 首《干了你的杯》"),
 ("se","Sara Videbeck (Det går an)"): ({"A2":3}, ""),
 ("se","Gösta Berling's Saga"): ({"A2":3}, ""),
 ("se","Pippi Longstocking"): ({"A2":3,"D":2}, "D 283"),
 ("se","The Emigrants"): ({"A2":3}, ""),
 ("se","Kallocain"): ({"A2":3,"D":1}, "D 1756"),
}
NEW = {  # new candidate rows from the two new canons
 "no": [("Mysteries","Knut Hamsun","本国",{"A2":3,"D":1},"","汉姆生；D 1800；Goodreads 8,685；书里的海边小镇没写地名，地点待查"),
        ("The Birds (Fuglane)","Tarjei Vesaas","本国",{"A2":3},"","Goodreads 9,419；不在 D 前 2000"),
        ("The District Governor's Daughters","Camilla Collett","本国",{"A2":3},"","Goodreads 836"),
        ("Norwegian Folk Tales","Asbjørnsen & Moe","本国",{"A2":3},"","Goodreads 1,037"),
        ("The Trumpet of Nordland","Petter Dass","本国",{"A2":3},"","Goodreads 28"),
        ("Peace (Fred)","Arne Garborg","本国",{"A2":3},"","Goodreads 137；耶伦"),
        ("Erasmus Montanus","Ludvig Holberg","本国（写丹麦）",{"A2":3},"不算挪威","故事发生在丹麦乡村")],
 "se": [("The Abominable Man","Sjöwall & Wahlöö","本国",{"A2":3},"","Goodreads 6,341；不在 D 前 2000；两位作者另一本《大笑的警察》已在表里"),
        ("Getting Married (Giftas)","August Strindberg","本国",{"A2":3},"","Goodreads 545"),
        ("Lapland Journey","Carl Linnaeus","本国",{"A2":3},"","Goodreads 2"),
        ("An Account of the Sámi","Johan Turi","本国",{"A2":3},"","Goodreads 84"),
        ("Katitzi","Katarina Taikon","本国",{"A2":3},"","Goodreads 479")],
}
SRC = {
 "no": ("A2", "挪威文学正典（Norsk litterær kanon，2007，利勒哈默尔文学节 10 人评审团选 25 部，按年代排列，不分名次）— litteraturfestival.no 的正典单页（PDF）"),
 "se": ("A2", "瑞典文化正典（En kulturkanon för Sverige，SOU 2025:92，2025-09-02 交政府，100 项，按领域排列，不分名次）文学部分 — svt.se、all-things-nordic.com 转述全表"),
}
places = {}
for line in open(os.path.join(HERE, "place_notes.tsv"), encoding="utf-8"):
    cc, t, p = line.rstrip("\n").split("\t"); places[(cc, t)] = p
specs = {}
def S_(cc): return specs.setdefault(cc, specio.load(cc))
for line in open(os.path.join(HERE, "gr_1124.tsv"), encoding="utf-8"):
    cc, t, n, what = line.rstrip("\n").split("\t")
    S = S_(cc); row = next(r for r in S["rows"] if r[0] == t)
    pts = {k: v for k, v in row[3].items() if k not in ("E", "D")}
    ev = []
    if t in TGB:
        r = TGB[t]; pts["D"] = dpts(r); ev.append("D %d" % r)
    else:
        ev.append("不在 D 前 2000")
    if n == "-": ev.append("Goodreads 查不到")
    else:
        n = int(n); e = tier(n)
        if e: pts["E"] = e
        g = "Goodreads " + fmt(n)
        if "Heaney" in what: g += "（海尼译本）"
        if "Doyle" in what: g += "（单篇条目；收在《福尔摩斯全集》里，全集 D 209）"
        elif "essay" in what: g += "（单篇条目）"
        ev.append(g)
    extra = EXTRA.get((cc, t))
    if extra: pts.update(extra[0]); ev.insert(0, extra[1]) if extra[1] else None
    note = "；".join([x for x in [places[(cc, t)]] + ev if x])
    specio.setrow(S, t, pts=pts, note=note)
for (cc, t), (add, nt) in EXTRA.items():
    S = S_(cc); row = next(r for r in S["rows"] if r[0] == t)
    if not all(row[3].get(k) == v for k, v in add.items()):  # rows not in the gr list
        note = row[5] + ("；" + nt if nt and nt not in row[5] else "")
        specio.setrow(S, t, add=add, note=note.strip("；"))
for cc, rows in NEW.items():
    S = S_(cc)
    for r in rows:
        if not any(x[0] == r[0] for x in S["rows"]): S["rows"].append(r)
for cc, (k, v) in SRC.items():
    S = S_(cc); src = dict(S["sources"])
    keys = list(src); i = keys.index("A1") + 1
    S["sources"] = {kk: src[kk] for kk in keys[:i]} | {k: v} | {kk: src[kk] for kk in keys[i:] if kk != k}
S = S_("hu"); S["sources"]["B"] = S["sources"]["B"] + "；诗歌篇目另查 2020 高中课程框架（9–12 年级）和按框架写的学校课程"
S = S_("se"); S["sources"]["D"] = "thegreatestbooks.org 总榜名次（11-24 逐页读前 2000 名）"
S = S_("no"); S["sources"]["D"] = "thegreatestbooks.org 总榜名次（11-24 逐页读前 2000 名）"
for cc, S in specs.items(): specio.save(cc, S)
print("patched:", " ".join(sorted(specs)))
