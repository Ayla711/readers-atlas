"""11-24: Morocco, first pack: 5 new books (The Innocents Abroad shared with Italy), 5 places. Mark Twain's Tangier and
Mohamed Choukri's, Loti's first sight of Fez, Canetti on the Djema el Fna, Saint-Exupery at Cape Juby (Tarfaya).

The map follows China's standard map (decision A-22): Western Sahara is not part of it. Natural Earth draws the land
Morocco holds there as Moroccan regions, so tools/countries.json leaves out MA-16 and cuts MA-14 and MA-15 at 27 deg 40 min N
("pov_drop", "pov_min_lat"). The regions are the sixteen of before 2015, not today's twelve.

Quotations (2 lines) are cut from English and French Wikisource pages (tools/content/wikisource.py); translations are our
own drafts. Books in copyright get scene notes with a fact source. What a cut changes is named in `checked`.

Coordinates are those of the place's English Wikipedia article (coords/add_ma1.json).

Fix of 11-24 (the atlas's rule: a book worth having is hung on the nearest real place even when its exact spot cannot be
found): Ibn Battuta's Rihla is quoted from Arabic Wikisource at Tangier, his birthplace and starting point; his tomb in the
medina still has no place of its own (no source gave its coordinates).

Usage: python3 -I add_ma1.py <app_dir> <coords.json> <wikisource_root>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-24"
b.init(APP, "", "ma", DATE)
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

T_IA = "The Innocents Abroad/Chapter 8"
T_LO = "Au Maroc/18"
EXIST = {"innocents-abroad"}

def once(title, s, lang):
    """the cut must start at the only place the words stand on the page"""
    n = ws.text(os.path.join(WSR, lang), title).count(s)
    assert n == 1, (title, s, n)
    return s

books = [
    BK("au-maroc", "Au Maroc", "在摩洛哥", "Au Maroc", "Pierre Loti", "皮埃尔·洛蒂", "Pierre Loti", "1890", lang="fr",
       src=ws.url("fr", "Au Maroc"), aliases=["Into Morocco", "Morocco", "Loti", "洛蒂"]),
    BK("for-bread-alone", "For Bread Alone", "裸面包", "الخبز الحافي", "Mohamed Choukri", "穆罕默德·舒克里", "محمد شكري", "1973", lang="ar", pd=False,
       aliases=["Al-Khubz al-Hafi", "Le Pain nu", "Choukri", "Shukri"]),
    BK("voices-of-marrakesh", "The Voices of Marrakesh", "马拉喀什的声音", "Die Stimmen von Marrakesch", "Elias Canetti", "埃利亚斯·卡内蒂", "Elias Canetti", "1967",
       lang="de", pd=False, aliases=["Die Stimmen von Marrakesch", "谛听马拉喀什", "Canetti", "卡内蒂"]),
    BK("southern-mail", "Southern Mail", "南方邮航", "Courrier sud", "Antoine de Saint-Exupéry", "安托万·德·圣埃克苏佩里", "Antoine de Saint-Exupéry", "1929",
       lang="fr", pd=False, aliases=["Courrier sud", "Southern Carrier", "Cape Juby", "Cap Juby", "Saint-Exupéry", "圣埃克苏佩里"]),
]

places = [
    ORIG("ma-tangier", "Tangier", "丹吉尔",
         "Port on the Strait of Gibraltar. Mark Twain and a few fellow passengers of the Quaker City crossed from Gibraltar in the summer of 1867; it was the first place on the voyage that seemed to him wholly foreign, and he gives it two chapters of The Innocents Abroad. Ibn Battuta was born here in 1304 and set out from here in 1325 on the journeys he later dictated as the Rihla",
         "直布罗陀海峡边的港口。1867 年夏天，马克·吐温和“教友城号”的几位旅伴从直布罗陀渡海过来；这是他一路上第一个觉得彻底陌生的地方，《傻子出国记》里用了两章来写。伊本·白图泰 1304 年生于此地，1325 年从这里出发，开始了他晚年口述成《游记》的长途旅行"),
    ORIG("ma-petit-socco", "Petit Socco, Tangier", "小索科广场，丹吉尔",
         "Small square in the medina of Tangier, also called Souk Dakhel or, in Spanish, Zoco Chico; long the focal point of the old town. The Tangier of Mohamed Choukri's For Bread Alone is this old town and the port below it. He wrote the book in Arabic in 1972; it first appeared in Paul Bowles's English translation in 1973",
         "丹吉尔老城里的小广场，又叫内市场，西班牙语叫“小索科”，一向是老城的中心。穆罕默德·舒克里《裸面包》里的丹吉尔，就是这片老城和下面的港口。书是 1972 年用阿拉伯语写的，1973 年先以保罗·鲍尔斯的英译本问世"),
    ORIG("ma-fez", "Fes el Bali (old Fez)", "非斯老城",
         "The walled old city of Fez. Pierre Loti rode here from Tangier in the spring of 1889 with a French embassy to the sultan, and published Au Maroc the next year; this is the caravan's first sight of the city across the plain",
         "非斯有城墙环绕的老城。1889 年春天，皮埃尔·洛蒂随法国派往苏丹的使团从丹吉尔骑马来到这里，第二年出版《在摩洛哥》；这一段写的是旅队隔着平原第一眼望见这座城"),
    ORIG("ma-jemaa", "Jemaa el-Fnaa, Marrakesh", "杰马夫纳广场，马拉喀什",
         "The main square of Marrakesh, at the edge of the souks. Elias Canetti spent some weeks in the city in the 1950s with a film crew; The Voices of Marrakesh, his notes on that stay, came out in 1967. He writes the name Djema el Fna",
         "马拉喀什的中心广场，在露天市场边上。埃利亚斯·卡内蒂 20 世纪 50 年代随一个电影摄制组在城里住了几个星期；记下这次旅居的《马拉喀什的声音》1967 年出版。书里把广场写作 Djema el Fna"),
    ORIG("ma-tarfaya", "Tarfaya (Cape Juby)", "塔尔法亚（朱比角）",
         "Small town on the Atlantic coast at Cape Juby, in the 1920s a refuelling stop on the airmail line from Toulouse to Dakar. Antoine de Saint-Exupéry lived here in 1927 and 1928 as head of the airfield, and Southern Mail (1929), his first novel, comes out of those months. A museum to him opened in the town in 2004",
         "大西洋岸边朱比角上的小镇，20 世纪 20 年代是图卢兹至达喀尔航空邮路上的一个加油站。安托万·德·圣埃克苏佩里 1927 年至 1928 年在这里当航空站站长，他的第一部小说《南方邮航》（1929）就出自这段日子。镇上纪念他的博物馆 2004 年开放"),
]

lines = [
    EN("ma-ia-1", "innocents-abroad", "ma-tangier", "Chapter 8", "第 8 章", T_IA,
       raw(T_IA, once(T_IA, "Tangier is the spot we have been longing for all the time.", "en"), "And lo! in Tangier we have found it.", "en"), ["Tangier"],
       "丹吉尔正是我们一直向往的地方。在别处，我们见到的东西和人虽有异国模样，却总掺杂着我们早已熟悉的东西和人，新奇感也就大打折扣。我们要的是彻头彻尾、毫不含糊的异国情调——从上到下是异国，从中心到四周是异国，里里外外、前后左右全是异国——没有一样东西来冲淡它，没有一样东西让我们想起天底下别的民族、别的地方。瞧！我们在丹吉尔找到了。",
       ["丹吉尔"], note=" (Chinese is our own)"),
    Q("ma-lo-1", "au-maroc", "ma-fez", "Chapter 18", "第 18 章", T_LO,
      raw(T_LO, once(T_LO, "Et enfin, enfin, vers quatre heures du soir", "fr"), "la ville sainte lentement nous apparaît…", "fr"), ["Fez"],
      "And at last, at last, towards four in the afternoon, the immense emptiness opens before us once more: a new sea of grass, perfectly level, a green and yellow sea of barley and flowering fennel — the plain of Fez! Far off, the great Atlas girds it with an imposing belt of summits all white, all glittering with snow…\nTwo more leagues of road across this plain, and suddenly, coming out from behind a shoulder of mountain that draws back like a piece of scenery in a theatre, the holy city slowly appears to us…",
      ["Fez"],
      "终于，终于，下午四点左右，无边的空旷又一次在我们面前展开：又是一片平平整整的草海，一片大麦和开花的茴香铺成的黄绿色的海——非斯平原！远处，大阿特拉斯山给它围上一圈雄伟的山峰，一色雪白，雪光闪耀……\n在这平原上再走两里格路，忽然间，一面山坡像舞台上的侧幕那样向后退开，圣城从它背后慢慢出现在我们眼前……",
      ["非斯"], note=" (two paragraphs)", site="French"),
    S("ma-fb-1", "for-bread-alone", "ma-petit-socco", "The book as a whole", "全书",
      "Choukri's account of his own childhood and youth. The family flees the countryside for Tangier; he grows up on its streets among foreigners, prostitution, drugs and the underworld, sells cigarettes in the port and spends time in prison. At twenty he still cannot read, and the book ends with his decision to learn.",
      "舒克里对自己童年和青年时代的讲述。一家人从乡下逃到丹吉尔；他在街头长大，身边是外国人、妓女、毒品和黑道，在港口卖香烟，还坐过牢。二十岁时他仍然不识字，全书结束在他决定去学认字的时候。",
      ["Tangier"], ["丹吉尔"], "https://en.wikipedia.org/wiki/For_Bread_Alone; https://en.wikipedia.org/wiki/Petit_Socco"),
    S("ma-vm-1", "voices-of-marrakesh", "ma-jemaa", "The book as a whole", "全书",
      "Short chapters from a visit to Marrakesh: the camel market, where he finds something human in the animals and is shaken to learn they are being led to slaughter; the souks; the Jewish quarter, the Mellah; and the Djema el Fna, where he stands among the listeners round the storytellers without understanding a word.",
      "一次马拉喀什之行留下的一组短章：骆驼市场上，他在骆驼身上看出许多人性，得知它们是被牵去屠宰的，深受震动；露天市场；犹太人聚居的“梅拉”区；还有杰马夫纳广场——他站在围着说书人的听众当中，一个字也听不懂。",
      ["Djema el Fna"], ["杰马夫纳广场"], "https://de.wikipedia.org/wiki/Die_Stimmen_von_Marrakesch"),
    S("ma-sm-1", "southern-mail", "ma-tarfaya", "The novel as a whole", "全书",
      "The pilot Jacques Bernis flies the mail south from Toulouse along the African coast towards Dakar, while the story of his love for Geneviève is told in between. The radio posts along the line, Cape Juby among them, pass on word of his plane; south of Juby it is found wrecked in the desert.",
      "飞行员雅克·贝尔尼斯驾着邮机从图卢兹沿非洲海岸向南飞往达喀尔，其间穿插着他对热纳维耶芙的爱情故事。沿线的无线电站——朱比角就是其中之一——一站站传递着他飞机的消息；在朱比角以南，人们在沙漠里找到了坠毁的飞机。",
      ["Cape Juby"], ["朱比角"], "https://en.wikipedia.org/wiki/Courrier_sud_(novel); https://en.wikipedia.org/wiki/Tarfaya"),
]

# ---- 11-24 fix: famous books hung even without an exact spot (user rule) ----
T_RH = "تحفة النظار في غرائب الأمصار وعجائب الأسفار/الجزء الأول/فصل:بدء الرحلة والخروج من طنجة"
books += [
    BK("rihla", "The Travels of Ibn Battuta (Rihla)", "伊本·白图泰游记", "تحفة النظار في غرائب الأمصار وعجائب الأسفار", "Ibn Battuta", "伊本·白图泰", "ابن بطوطة",
       "14th century", lang="ar", src=ws.url("ar", "تحفة النظار في غرائب الأمصار وعجائب الأسفار"),
       aliases=["Rihla", "Tuhfat al-Nuzzar", "A Gift to Those Who Contemplate the Wonders of Cities", "Ibn Battutah", "伊本·巴图塔", "Tangier"]),
]
lines += [
    Q("ma-rh-1", "rihla", "ma-tangier", "The setting out from Tangier", "从丹吉尔出发", T_RH,
      raw(T_RH, once(T_RH, "كان خروجي من طنجة مسقط رأسي", "ar"), "وسني يومئذ اثنتان وعشرون سنة.", "ar"), ["طنجة"],
      "My setting out from Tangier, my birthplace, was on Thursday the second of the month of God, Rajab the unique, in the year seven hundred and twenty-five, with the purpose of making the pilgrimage to the Holy House of God and visiting the tomb of the Prophet, upon him be the best of blessings and peace. I went alone, with no companion whose company might cheer me and no caravan to travel with, moved by a strong urge within me and a longing, long hidden in my heart, for those noble sanctuaries. So I made up my mind to leave everyone I loved, women and men, and left my homeland as birds leave their nests. My parents were still alive, and parting from them weighed on me, as it weighed on them. I was then twenty-two years old.",
      ["Tangier"],
      "我从故乡丹吉尔出发，是在七二五年神圣的、独一无二的赖哲卜月初二，一个星期四，为的是去朝觐真主的圣殿，拜谒先知的陵墓，愿最好的祝福与平安归于他。我孤身一人，没有可以作伴解闷的同伴，也没有可以随行的商队，只凭心中一股强烈的冲动，和久藏胸中、对那些神圣之地的向往。于是我下定决心，离开所有亲爱的人，无论男女，像鸟儿离巢一样离开了故土。那时我的父母都还在世，与他们分别让我心情沉重，他们也同样难过。那年我二十二岁。",
      ["丹吉尔"], note=" (the year is of the Hijra: 725 AH, that is 1325; the opening words 'Shaykh Abu Abdallah said:' left out)", site="Arabic"),
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

HEAD = "// Morocco, hand-written content (tools/content/batches/add_ma1.py, 2026-11-24).\n"
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
