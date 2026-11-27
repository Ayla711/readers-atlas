"""11-27: Slovenia, the books the user chose (11-26): the top 5 of the 2024 survey of Slovene school librarians on the most
important Slovene novels (tools/selection/si.md), less Alamut, whose castle is in Iran (no map of Iran yet): 4 books. Plus
one line for a book already in the app (A Farewell to Arms, data/it), which qualifies by the rule and which the user chose
to hang on the Banjšice Plateau. Slovenia opens with this batch. Places and lines, with the reason for each:
- Muljava for The Tenth Brother: its manor (Slemenice) and villages are invented; under the rule for famous books it is hung
  at Jurčič's birth house, now a museum. The book is in the public domain, but no line of it names Muljava: a scene note.
- Visoko Manor for The Visoko Chronicle: the real house of the Kalan (Khallan) family; the novel opens "right here at
  Visoko". Quotation from Slovene Wikisource, our own translation.
- The Hippodrome of Constantinople (data/tr) for Under the Free Sun: Iztok wins the archery contest there and is known all
  over the city as its victor. Published 1906-07, in the public domain in the US: quotation from Slovene Wikisource, our
  own translation. The place and the line go into data/tr; the book stays in data/si.
- Strmol Castle for I Saw Her That Night: the real-life model; Jančar's novel tells, in fiction, the story of its owners,
  the Hribars. In copyright: a scene note.
- The Banjšice Plateau (the Bainsizza) for A Farewell to Arms: Chapter 27, the retreat of the army of the Bainsizza. The
  novel has been in the public domain in the US since 1 January 2025; English Wikisource has it. The book stays in data/it
  and is marked public domain there, with its Wikisource page.
The map of Slovenia (data/si/geo.js) is the 12 statistical regions, built from geoBoundaries SVN ADM2 (OpenStreetMap via
Wambacher, 2017, ODbL 1.0): its 213 municipality shapes are named and given their regions from sl.wikipedia's list of
municipalities (tools/eu-revision/si_municipality_regions.tsv). Natural Earth's Slovene units carry 2002 municipalities, old
region names and some wrong labels.
Usage: python3 -I tools/content/batches/add_si1.py <app_dir> tools/content/batches/coords/add_si1.json <wikisource_cache_dir>
(cache/si holds the Wikisource pages: sl "Deseti brat (Josip Jurčič, 1866)", "Visoška kronika", "Pod svobodnim soncem";
en "A Farewell to Arms/Chapter 27", "A Farewell to Arms"; fetched with tools/content/wikisource.py)"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-27"
b.init(APP, "", "si", DATE)
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]
def BK(id, title, title_zh, title_orig, author, author_zh, year, pd, src, aliases):
    return dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
                orig_lang="sl", public_domain=pd, source_url=src, aliases=aliases)
def Q(id, book, place, loc, loc_zh, source, orig, hl_orig, en, hl_en, zh, hl_zh):
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls:
            assert h in text, (id, h)
    assert "[" not in orig and "\xa0" not in orig and "  " not in orig, (id, "page mark or odd space")
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh,
                text_orig=orig, highlight_orig=hl_orig, text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh,
                translation="own", status="draft", checked=f"{source}, {DATE}")
SL = "https://sl.wikisource.org/wiki/"

books = [
    BK("deseti-brat", "The Tenth Brother", "第十个兄弟", "Deseti brat", "Josip Jurčič", "约瑟夫·尤尔奇奇", "1866", True,
       SL + "Deseti_brat_(Josip_Jurčič,_1866)", ["Deseti brat", "Martinek Spak", "Lovre Kvas", "Krjavelj", "Slemenice"]),
    BK("pod-svobodnim-soncem", "Under the Free Sun", "在自由的阳光下", "Pod svobodnim soncem", "Fran Saleški Finžgar",
       "弗兰·萨莱什基·芬兹加尔", "1906–1907", True, SL + "Pod_svobodnim_soncem",
       ["Pod svobodnim soncem", "Pod svobodnim solncem", "Iztok", "Irena", "Povest davnih dedov"]),
    BK("visoska-kronika", "The Visoko Chronicle", "维索科编年史", "Visoška kronika", "Ivan Tavčar", "伊万·塔夫查尔", "1919", True,
       SL + "Visoška_kronika", ["Visoška kronika", "Izidor Khallan", "Polikarp Khallan", "Visoko"]),
    BK("to-noc-sem-jo-videl", "I Saw Her That Night", "那晚我看见了她", "To noč sem jo videl", "Drago Jančar", "德拉戈·扬查尔",
       "2010", False, None, ["To noč sem jo videl", "Veronika Zarnik", "Strmol"]),
]

places = [
    b.ORIG("si-jurcic-muljava", "Jurčič's birth house, Muljava", "穆利亚瓦 · 尤尔奇奇故居", *C("si-jurcic-muljava"),
        "The farmhouse at Muljava, in the Dolenjska hills of Ivančna Gorica municipality, where Josip Jurčič was born in 1844; it is now an ethnographic open-air museum, on the Jurčič Trail that runs through the village to the source of the Krka. The Tenth Brother is set in Jurčič's native Dolenjska, but its manor of Slemenice and its villages are invented; under the rule for famous books it is hung at its author's birth house",
        "伊万奇纳戈里察市多伦尼斯卡丘陵上的穆利亚瓦村，约瑟夫·尤尔奇奇 1844 年生在这座农舍里；如今它是一座民俗露天博物馆，“尤尔奇奇小径”从村里经过，一直通到克尔卡河的源头。《第十个兄弟》写的是尤尔奇奇的家乡多伦尼斯卡，但书里的斯莱梅尼采庄园和几个村子都是虚构的；按“名著不漏”的规则，挂在作者的出生地"),
    b.ORIG("si-visoko", "Visoko Manor (Tavčar's estate), Visoko pri Poljanah", "波利亚内附近的维索科庄园（塔夫查尔庄园）", *C("si-visoko"),
        "A great farmhouse manor at Visoko in the Poljane valley, the house of the rich Kalan (Khallan) family, counted among Slovenia's most important monuments of the building of its wealthiest peasants in the later 18th century. Ivan Tavčar bought it in 1893 from Anton Hafner, son of Ana Hafner née Kalan; his bronze statue and the family tomb stand on the estate. The Visoko Chronicle is the story of the Khallans who first held it, told by Izidor Khallan, born here in 1664",
        "波利亚内河谷维索科村的一座大农庄宅院，原是富裕的卡兰家族（书中写作 Khallan）的家，是斯洛文尼亚 18 世纪下半叶最富裕的农民阶层建筑中最重要的古迹之一。伊万·塔夫查尔 1893 年从安娜·哈夫纳（娘家姓卡兰）的儿子安东·哈夫纳手里买下了它；庄园里有他的青铜像和家族墓。《维索科编年史》讲的就是最早拥有这里的卡兰一家，由 1664 年生在这里的伊西多尔·卡兰讲述"),
    b.PROTO("si-strmol", "Strmol Castle, near Cerklje na Gorenjskem", "切尔克列附近的斯特莫尔城堡", *C("si-strmol"),
        "The manor of the Zarniks in I Saw Her That Night. From 1936 Strmol belonged to the Ljubljana industrialist Rado Hribar and his wife Ksenija, who lived here almost to the end of the war; on 6 January 1944 both were killed by the VOS, the security service of the Liberation Front. Jančar's novel is his literary reading of their story. The castle now serves the Slovene government for official occasions",
        "《那晚我看见了她》里扎尔尼克家的庄园。1936 年起，斯特莫尔归卢布尔雅那的实业家拉多·赫里巴尔和妻子克塞尼娅所有，两人在这里一直住到战争快结束；1944 年 1 月 6 日，二人被解放阵线的安全情报机构 VOS 杀害。扬查尔的小说就是他对这段往事的文学演绎。城堡如今是斯洛文尼亚政府举行礼仪活动的场所"),
    b.ORIG("si-banjsice", "Banjšice Plateau (the Bainsizza)", "班什契高原（贝因西扎）", *C("si-banjsice"),
        "A karst plateau above the Soča, about 5 km north of Nova Gorica, called the Bainsizza in Italian. In the Eleventh Battle of the Isonzo, from August to September 1917, the Italian and Austro-Hungarian armies fought on it. In A Farewell to Arms Frederic Henry's ambulances serve here in the autumn of 1917, and the retreat begins when the army of the Bainsizza comes down off the plateau",
        "索查河上方的一片喀斯特高原，在新戈里察以北约 5 公里，意大利语叫贝因西扎。1917 年 8 月到 9 月的第十一次伊松佐河战役中，意大利军和奥匈军在高原上交战。《永别了，武器》里，1917 年秋天弗雷德里克·亨利的救护车队就在这里，大撤退从“贝因西扎的军队”撤下高原开始"),
]

hippodrome = b.ORIG("tr-hippodrome", "Hippodrome of Constantinople (Sultanahmet Square), Istanbul", "伊斯坦布尔 · 君士坦丁堡赛马场（苏丹艾哈迈德广场）", *C("tr-hippodrome"),
    "The circus that was the sporting and social centre of Constantinople, now Sultanahmet Square. In Finžgar's Under the Free Sun, set in Justinian's time, the young Slav Iztok wins the archery contest here before the emperor and Theodora and is known all over the city as its victor; the hippodrome comes up in the novel more than forty times",
    "君士坦丁堡的体育和社交中心，如今是苏丹艾哈迈德广场。芬兹加尔的《在自由的阳光下》写查士丁尼时代，年轻的斯拉夫人伊兹托克在这里当着皇帝和狄奥多拉的面赢下射箭比赛，成了全城皆知的赛马场得胜者；小说里赛马场出现了四十多次", country="tr")

FTA = ws.cut(WSR, "A Farewell to Arms/Chapter 27", "It rained steadily", "in the spring of that year.")
lines = [
    b.S("si-db-1", "deseti-brat", "si-jurcic-muljava", "The novel as a whole", "全书",
        "Lovre Kvas, a poor young man fresh from the Ljubljana lyceum, comes as tutor to the son of the squire of Slemenice and falls in love with the squire's daughter Manica. On the way there he meets Martinek Spak, who calls himself the tenth brother, after the folk belief that a tenth child brings misfortune; he is the unacknowledged son of a neighbouring squire, Piškav, and the mystery of his mother's story drives the plot. The village scenes, with the comic villager Krjavelj, are told in a lively spoken Slovene. Published as a serial in 1866, it is taken to be the first Slovene novel. Josip Jurčič was born at Muljava.",
        "刚从卢布尔雅那中学毕业的穷青年洛弗雷·克瓦斯，到斯莱梅尼采庄园给庄园主的儿子当家庭教师，爱上了庄园主的女儿玛尼察。路上他遇见马丁内克·斯帕克——此人自称“第十个兄弟”，源自民间说法：家里的第十个孩子会带来不幸。他是邻近庄园主皮什卡夫不认的私生子，他母亲往事里的谜团推动着整个故事。村里的场景和滑稽的村民克里亚维尔，用的是活泼的口语斯洛文尼亚语。小说 1866 年连载发表，被认为是第一部斯洛文尼亚语长篇小说。约瑟夫·尤尔奇奇生在穆利亚瓦。",
        ["Muljava"], ["穆利亚瓦"],
        "https://sl.wikipedia.org/wiki/Deseti_brat; https://en.wikipedia.org/wiki/The_Tenth_Brother; https://sl.wikipedia.org/wiki/Muljava; https://en.wikipedia.org/wiki/Josip_Jurčič; https://www.dobreknjige.si/knjige/deseti-brat-5/"),
    Q("si-vk-1", "visoska-kronika", "si-visoko", "Chapter I (1664), the opening", "第一章（1664），开篇", "Slovene Wikisource, Visoška kronika",
      ws.cut(WSR, "Visoška kronika", "Rodil sem se v Gospodovem letu 1664", "kmetovalca Vovka Wulffinga."), ["Visokem"],
      "I was born in the year of Our Lord 1664, on St Isidore's day, and that right here at Visoko. My father was Polikarp Khallan, also Khallain, owner of two farms at Visoko, and my mother was Barbara Khallanin, also Khallainin, born at Suha, the second daughter of the farmer there, Vovk Wulffing.", ["Visoko"],
      "我生于主历 1664 年圣伊西多尔节那天，就生在这维索科。我父亲是波利卡普·卡兰，也写作卡莱因，在维索科有两处农庄；我母亲是芭芭拉·卡兰宁，也写作卡莱宁，生在苏哈，是那里的农户沃夫克·乌尔芬格的二女儿。", ["维索科"]),
    b.S("si-tn-1", "to-noc-sem-jo-videl", "si-strmol", "The novel as a whole", "全书",
        "Veronika Zarnik, a young, vain and eccentric woman of Ljubljana's well-to-do society who cares more for her own pleasures than for the war, never speaks for herself: five people who knew her tell her story in turn. They are her former lover, a Serbian officer of the Royal Yugoslav Army in a prison camp at Palmanova in 1945; her ailing mother, waiting for her to come home; a German army doctor; the family housekeeper; and the partisan Jeranek, once a farmhand, who had secretly longed for her. Jančar built the novel on the real story of the Hribars of Strmol. It won the Kresnik award, his third, and in 2020 was named the best Kresnik-winning novel of the decade.",
        "维罗妮卡·扎尔尼克是卢布尔雅那上流社会一个年轻、自恋又古怪的女人，战争当前，她只在乎自己的享乐。她自始至终没有开口，她的故事由五个认识她的人轮流讲出来：她从前的情人——1945 年关在帕尔马诺瓦战俘营里的一名南斯拉夫王国军塞尔维亚军官；她病弱的母亲，一直在等她回家；一名德国占领军军医；家里的女管家；还有游击队员耶兰克——他战前是庄园的雇工，一直暗暗渴慕着她。扬查尔把小说建立在斯特莫尔城堡赫里巴尔夫妇的真实遭遇上。这部小说为他第三次赢得 Kresnik 奖，2020 年又被评为十年来最好的 Kresnik 获奖小说。",
        ["Strmol"], ["斯特莫尔"],
        "https://sl.wikipedia.org/wiki/To_noč_sem_jo_videl; https://sl.wikipedia.org/wiki/Grad_Strmol"),
    dict(id="si-fta-1", book_id="farewell-to-arms", place_ids=["si-banjsice"], location="Book Three, Chapter 27", location_zh="第三部第 27 章",
         text_en=FTA, highlight_en=["Bainsizza"],
         text_zh="雨下个不停，贝因西扎的军队冒着十月的雨撤下高原，渡过那条河——那年春天，伟大的胜利正是从那里开始的。", highlight_zh=["贝因西扎"],
         translation="original", status="draft", checked=f"English Wikisource, A Farewell to Arms/Chapter 27, {DATE}"),
]
abroad = [("tr", hippodrome, Q("tr-psv-1", "pod-svobodnim-soncem", "tr-hippodrome", "Book One", "第一部", "Slovene Wikisource, Pod svobodnim soncem",
      ws.cut(WSR, "Pod svobodnim soncem", "Obstala je gruča sprehajalcev", "zmagalca iz hipodroma."), ["hipodroma"],
      "A knot of strollers stopped and greeted him, the victor of the Hippodrome, known all over Byzantium.", ["Hippodrome"],
      "一群散步的人停下来向他致意——他是赛马场上的得胜者，全拜占庭都知道他。", ["赛马场"]))]
for h in ["Bainsizza"]:
    assert h in FTA

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set()
for f in glob.glob(os.path.join(APP, "data", "*", "books.js")):
    all_books |= ids_in(f)
new_b, new_p = {x["id"] for x in books}, {x["id"] for x in places} | {p["id"] for _, p, _ in abroad}
assert len(books) == 4 and not new_b & all_books, new_b & all_books
assert "farewell-to-arms" in ids_in(os.path.join(APP, "data", "it", "books.js"))
assert new_p == set(CO), new_p ^ set(CO)
assert not new_p & set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "places.js"))))
for l in lines + [l for _, _, l in abroad]:
    assert l["book_id"] in new_b | {"farewell-to-arms"} and l["place_ids"][0] in new_p, l["id"]
assert {l["book_id"] for l in lines + [l for _, _, l in abroad]} == new_b | {"farewell-to-arms"}

IT_OLD = 'id: "farewell-to-arms", title: "A Farewell to Arms", title_zh: "永别了，武器", author: "Ernest Hemingway", author_zh: "欧内斯特·海明威", year: "1929", orig_lang: "en", public_domain: false, source_url: null,'
IT_NEW = 'id: "farewell-to-arms", title: "A Farewell to Arms", title_zh: "永别了，武器", author: "Ernest Hemingway", author_zh: "欧内斯特·海明威", year: "1929", orig_lang: "en", public_domain: true, source_url: "https://en.wikisource.org/wiki/A_Farewell_to_Arms",'

HEAD = "// Slovenia, hand-written content (tools/content/batches/add_si1.py, 2026-11-27).\n"
def write(name, key, entries, extra=""):
    os.makedirs(os.path.dirname(b.data(name)), exist_ok=True)
    with open(b.data(name), "w", encoding="utf-8") as fh:
        fh.write(HEAD + extra + "window.RA_DATA = window.RA_DATA || {};\nwindow.RA_DATA." + key + " = [\n"
                 + ",\n".join("  " + b.obj(e) for e in entries) + "\n];\n")
if __name__ == "__main__":
    for f in ("books.js", "places.js", "lines.js"):
        assert not os.path.exists(b.data(f)), ("already there", f)
    itb = os.path.join(APP, "data", "it", "books.js"); s = open(itb, encoding="utf-8").read()
    assert s.count(IT_OLD) == 1, "it/books.js: A Farewell to Arms entry changed"
    open(itb + ".new", "w", encoding="utf-8").write(s.replace(IT_OLD, IT_NEW)); os.replace(itb + ".new", itb)
    write("books.js", "books", books)
    write("places.js", "places", places, "// Each place's admin-1 region is worked out from its coordinates by app.js.\n")
    write("lines.js", "lines", lines)
    M = "11-27: Slovene books set here (tools/content/batches/add_si1.py)"
    for cc, p, l in abroad:
        b.append(os.path.join(APP, "data", cc, "places.js"), [p], M)
        b.append(os.path.join(APP, "data", cc, "lines.js"), [l], M)
    print(len(books), "books,", len(places) + len(abroad), "places,", len(lines) + len(abroad), "lines")
