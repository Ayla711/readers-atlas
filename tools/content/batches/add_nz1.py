"""11-24: New Zealand, first pack: 5 books, 6 places. Katherine Mansfield's Crescent Bay (Days Bay) and her birthplace in
Thorndon, Butler's Mesopotamia Station behind Erewhon, Janet Frame's Oamaru, Whangara of The Whale Rider and the Hokitika of
The Luminaries.

The map has the sixteen regions; the Chatham Islands and the outlying subantarctic and northern islands are left off the
map ("skip_units").

Quotations (2 lines) are cut from English Wikisource pages (tools/content/wikisource.py); Chinese is our own draft. Books
in copyright get scene notes with a fact source. What a cut changes is named in `checked`.

Coordinates are those of the place's English Wikipedia article, the Mansfield house's from Wikidata (coords/add_nz1.json).
Oamaru's pin is the town's point; no source gave coordinates for Janet Frame's childhood house in Eden Street.

Usage: python3 -I add_nz1.py <app_dir> <coords.json> <wikisource_root>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-24"
b.init(APP, "", "nz", DATE)
W = b.W
GAP = b.GAP

def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, pd=True, **kw):
    d = dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
             orig_lang=kw.pop("lang", "nl"), public_domain=pd, source_url=kw.pop("src", None), author_orig=author_orig)
    d.update(kw)
    return {k: v for k, v in d.items() if v is not None or k == "source_url"}

def C(pid):
    c = CO[pid]
    return c["lat"], c["lon"], c["st"], c["su"]

def ORIG(pid, name, zh, en_note, zh_note, **kw): return b.ORIG(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PIL(pid, name, zh, en_note, zh_note, ids, **kw): return b.PIL(pid, name, zh, *C(pid), en_note, zh_note, ids, **kw)
S = b.S

def raw(title, start, end, lang="nl"):
    t = ws.text(os.path.join(WSR, lang), title)
    n = re.sub("[\xa0   ]", " ", t)
    i = n.find(start)
    assert i >= 0, (title, start)
    j = n.find(end, i)
    assert j >= 0, (title, start, end)
    return t[i:j + len(end)]

def flow(s):
    """a hard-wrapped paragraph: lines joined, doubled spaces written as one"""
    return re.sub(r" {2,}", " ", s.replace("\n", " "))

def Q(id, book, place, loc, loc_zh, title, orig, hl_orig, en, hl_en, zh, hl_zh, note="", site="Dutch"):
    if re.search("[\xa0   ]", orig):
        orig = re.sub("[\xa0   ]+", " ", orig)
        note += " (no-break spaces written as plain spaces)"
    if "  " in orig:
        orig = re.sub(" {2,}", " ", orig)
        note += " (a doubled space written as one)"
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls:
            assert h in text, (id, h)
    assert "[" not in orig and "Sjabloon" not in orig, (id, "page mark or broken template")
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh,
                text_orig=orig, highlight_orig=hl_orig, text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh, translation="own",
                status="draft", checked=f"{site} Wikisource, {title}{note}, {DATE}")

def EN(id, book, place, loc, loc_zh, title, text, hl, zh, hl_zh, note=""):
    assert "[" not in text and "]" not in text and "\xa0" not in text and "  " not in text, (id, text[:40])
    for h in hl: assert h in text, (id, h)
    for h in hl_zh: assert h in zh, (id, h)
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh, text_en=text, highlight_en=hl, translation="original",
                text_zh=zh, highlight_zh=hl_zh, status="draft", checked=f"English Wikisource, {title}{note}, {DATE}")

T_AB = "The Garden Party, and Other Stories/At the Bay"
T_ER = "Erewhon; or Over the Range (1872)/Chapter 1"
EXIST = set()

def once(title, s, lang="en"):
    """the cut must start at the only place the words stand on the page"""
    n = ws.text(os.path.join(WSR, lang), title).count(s)
    assert n == 1, (title, s, n)
    return s

def PROTO(pid, name, zh, en_note, zh_note, **kw): return b.PROTO(pid, name, zh, *C(pid), en_note, zh_note, **kw)

books = [
    BK("the-garden-party", "The Garden Party, and Other Stories", "园会", "The Garden Party, and Other Stories", "Katherine Mansfield", "凯瑟琳·曼斯菲尔德",
       "Katherine Mansfield", "1922", lang="en", src=ws.url("en", "The Garden Party, and Other Stories"),
       aliases=["At the Bay", "The Garden Party", "Crescent Bay", "Burnell", "Mansfield", "曼斯菲尔德"]),
    BK("erewhon", "Erewhon", "埃瑞璜", "Erewhon; or, Over the Range", "Samuel Butler", "塞缪尔·巴特勒", "Samuel Butler", "1872", lang="en",
       src=ws.url("en", "Erewhon; or Over the Range (1872)"), aliases=["Over the Range", "Erewhon", "Higgs", "Butler"]),
    BK("owls-do-cry", "Owls Do Cry", "猫头鹰在哭泣", "Owls Do Cry", "Janet Frame", "珍妮特·弗雷姆", "Janet Frame", "1957", lang="en", pd=False,
       aliases=["Waimaru", "Withers", "Daphne", "Frame"]),
    BK("the-whale-rider", "The Whale Rider", "鲸骑士", "The Whale Rider", "Witi Ihimaera", "威蒂·伊希马埃拉", "Witi Ihimaera", "1987", lang="en", pd=False,
       aliases=["Whale Rider", "Kahu", "Paikea", "Koro Apirana", "Ihimaera"]),
    BK("the-luminaries", "The Luminaries", "发光体", "The Luminaries", "Eleanor Catton", "埃莉诺·卡顿", "Eleanor Catton", "2013", lang="en", pd=False,
       aliases=["Walter Moody", "Hokitika", "Catton"]),
]

places = [
    ORIG("nz-days-bay", "Days Bay, Eastbourne", "戴斯湾，伊斯特本",
         "Bay on the eastern shore of Wellington Harbour. 'At the Bay' (1922) draws on Katherine Mansfield's childhood holidays here, when the name Days Bay also took in Rona Bay and Muritai, along the same shore; in the story the bay is called Crescent Bay",
         "惠灵顿港东岸的海湾。《在海湾》（1922）取材于凯瑟琳·曼斯菲尔德童年在这里度过的假期；那时“戴斯湾”这个名字还包括同一段海岸上的罗纳湾和穆里泰。小说里这片海湾叫“新月湾”"),
    PIL("nz-mansfield-house", "Katherine Mansfield House and Garden, Thorndon", "凯瑟琳·曼斯菲尔德故居，桑登",
        "The house at 25 Tinakori Road, Wellington, built in 1888 for Harold Beauchamp; his daughter Kathleen, who wrote as Katherine Mansfield, was born here on 14 October that year, a few months after the family moved in. It is now a museum, listed as a Category 1 Historic Place",
        "惠灵顿蒂纳科里路 25 号，1888 年为哈罗德·比彻姆建造；同年 10 月 14 日，全家搬进来几个月后，他的女儿凯瑟琳——笔名凯瑟琳·曼斯菲尔德——在这里出生。现在是博物馆，列为一级历史建筑",
        ["the-garden-party"]),
    PROTO("nz-mesopotamia", "Mesopotamia Station, upper Rangitata", "美索不达米亚牧场，朗伊塔塔河上游",
          "High-country sheep station in the upper Rangitata valley, Canterbury, where Samuel Butler farmed for four years, 1860–1864. The first chapters of Erewhon, in which the narrator works as a cadet on a remote station before crossing the range, are based on his own life here",
          "坎特伯雷朗伊塔塔河谷上游的高地牧羊场，塞缪尔·巴特勒 1860 年至 1864 年在这里经营了四年。《埃瑞璜》开头几章——叙述者在一处偏远牧场当学徒，后来翻过山岭——取材于他在这里的亲身经历"),
    ORIG("nz-oamaru", "Oamaru", "奥马鲁",
         "Coastal town in North Otago where Janet Frame's family settled when she was a child; it is recognisable as the 'Waimaru' of Owls Do Cry, her first novel, and of her later fiction. The pin is the town's point",
         "北奥塔哥的海滨小镇，珍妮特·弗雷姆童年时全家在这里定居；她的第一部小说《猫头鹰在哭泣》和此后小说里的“怀马鲁”，看得出就是这里。图钉标在镇中心"),
    ORIG("nz-whangara", "Whangara", "旺加拉",
         "Māori community on the East Coast of the North Island, north of Gisborne. The Whale Rider (1987) is set here in the 1980s and retells the story of Paikea, the ancestor who came to this coast on the back of a whale",
         "北岛东岸、吉斯伯恩以北的毛利人社区。《鲸骑士》（1987）的故事发生在 20 世纪 80 年代的这里，重述了祖先派凯亚骑着鲸鱼来到这片海岸的传说"),
    ORIG("nz-hokitika", "Hokitika", "霍基蒂卡",
         "Town on the West Coast of the South Island, founded in the gold rush of the 1860s. The Luminaries, which won the Booker Prize in 2013, is set here in 1866",
         "南岛西海岸的小镇，建于 19 世纪 60 年代的淘金热中。2013 年获布克奖的《发光体》，故事就发生在 1866 年的这里"),
]

lines = [
    EN("nz-ab-1", "the-garden-party", "nz-days-bay", "'At the Bay', section 1", "《在海湾》第一节", T_AB,
       raw(T_AB, once(T_AB, "Very early morning. The sun was not yet risen,"), "which was beach and where was the sea.", "en"),
       ["Crescent Bay"],
       "清晨，很早。太阳还没有升起，整个新月湾都藏在一片白色的海雾里。后面那些长满灌木的大山被闷住了，看不出山在哪里到头，牧场和平房又从哪里开始。沙路不见了，路那边的牧场和平房也不见了；再往外，那些长着红草的白色沙丘也没了；什么都分不清哪里是海滩，哪里是海。",
       ["新月湾"], note=" (the opening of the story; Chinese is our own)"),
    EN("nz-er-1", "erewhon", "nz-mesopotamia", "Chapter 1, 'Waste Lands'", "第一章“荒地”", T_ER,
       raw(T_ER, once(T_ER, "Men pushed farther and farther into the mountains"), "I was then just twenty-two years old.", "en"),
       ["a small and newly founded station"],
       "人们越来越深入群山，在前山之内找到了相当大的一片地，夹在前山和另一道更高的山岭之间——不过这道山岭也还不是最高的，最高的是从平原上就能望见的那道大雪山。然而这第二道山岭似乎就是牧区的尽头了；我正是在这里，在一处新建不久的小牧场上，被收作学徒，不久就正式受雇。那年我刚满二十二岁。",
       ["一处新建不久的小牧场"], note=" (Chinese is our own)"),
    S("nz-od-1", "owls-do-cry", "nz-oamaru", "The novel as a whole", "全书",
      "The story of the Withers children, growing up in a seaside town called Waimaru and followed over twenty years; much of it follows Daphne, who is sent to a mental hospital.",
      "威瑟斯家几个孩子在一个叫怀马鲁的海滨小镇长大的故事，前后跨越二十年；其中大半跟着被送进精神病院的达芙妮。",
      ["Waimaru"], ["怀马鲁"], "https://en.wikipedia.org/wiki/Owls_Do_Cry; https://en.wikipedia.org/wiki/Janet_Frame"),
    S("nz-wr-1", "the-whale-rider", "nz-whangara", "The novel as a whole", "全书",
      "Kahu is the eldest great-grandchild of Koro Apirana, the chief at Whangara; had she been a boy she would have been the future leader of the tribe, and her great-grandfather will not accept her. The novel retells the myth of Paikea, the ancestor who came to this coast on a whale.",
      "卡胡是旺加拉酋长科罗·阿皮拉纳最年长的曾孙辈；如果她是男孩，就会是部族未来的首领，可曾祖父不肯接受她。小说重述了祖先派凯亚骑鲸来到这片海岸的神话。",
      ["Whangara"], ["旺加拉"], "https://en.wikipedia.org/wiki/The_Whale_Rider"),
    S("nz-lu-1", "the-luminaries", "nz-hokitika", "The opening of the novel", "小说开头",
      "In 1866 Walter Moody, come to make his fortune on the goldfields, arrives in Hokitika and walks into the smoking room of the Crown Hotel, where he stumbles into a tense meeting of twelve local men; it draws him into a mystery of unsolved crimes.",
      "1866 年，想在金矿发财的沃尔特·穆迪来到霍基蒂卡，走进皇冠旅馆的吸烟室，撞上了十二个当地男人之间一场紧张的聚会，由此卷入一连串悬而未决的罪案之谜。",
      ["Hokitika"], ["霍基蒂卡"], "https://en.wikipedia.org/wiki/The_Luminaries"),
]

# ============================== checks ==============================
def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set()
for f in glob.glob(os.path.join(APP, "data", "*", "books.js")):
    if os.path.dirname(f) != os.path.dirname(b.data("books.js")):
        all_books |= ids_in(f)
new_b, new_p, new_l = {x["id"] for x in books}, {x["id"] for x in places}, {x["id"] for x in lines}
assert len(new_b) == len(books) and len(new_p) == len(places) and len(new_l) == len(lines)
assert not new_b & all_books, new_b & all_books
assert EXIST <= all_books, EXIST - all_books
assert new_p == set(CO), new_p ^ set(CO)
bids = new_b | EXIST
for l in lines:
    assert l["book_id"] in bids and all(p in new_p for p in l["place_ids"]), l["id"]
used = {p for l in lines for p in l["place_ids"]}
for p in places:
    assert p["id"] in used or p.get("book_ids"), p["id"]
    assert all(i in bids for i in p.get("book_ids", [])), p["id"]
covered = {l["book_id"] for l in lines} | {i for p in places for i in p.get("book_ids", [])}
assert not new_b - covered, new_b - covered
assert not EXIST - covered, EXIST - covered

HEAD = "// New Zealand, hand-written content (tools/content/batches/add_nz1.py, 2026-11-24).\n"
def write(name, key, entries, extra=""):
    os.makedirs(os.path.dirname(b.data(name)), exist_ok=True)
    with open(b.data(name), "w", encoding="utf-8") as fh:
        fh.write(HEAD + extra + "window.RA_DATA = window.RA_DATA || {};\nwindow.RA_DATA." + key + " = [\n"
                 + ",\n".join("  " + b.obj(e) for e in entries) + "\n];\n")
if __name__ == "__main__":
    for f in ("books.js", "places.js", "lines.js"):
        assert not os.path.exists(b.data(f)), ("already there", f)
    write("books.js", "books", books)
    write("places.js", "places", places, "// Each place's admin-1 region is worked out from its coordinates by app.js.\n")
    write("lines.js", "lines", lines)
    print(len(books), "books,", len(places), "places,", len(lines), "lines (", sum(1 for l in lines if l.get("kind") != "scene"), "quotations )")
