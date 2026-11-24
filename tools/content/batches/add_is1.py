"""11-23: Iceland, first pack: 8 new books and Heimskringla from the Norway pack, 9 places. Gunnar's slope at Hlidarendi,
Verne's Snaefellsjokull, Snorri's Reykholt, Laxness's Gljufrasteinn, Burial Rites at Thristapar, Jar City's Nordurmyri,
Nonni's Akureyri, Gunnarsson's Skriduklaustur and Grettir's Reykir, facing Drangey.

Quotations (2 lines) are cut from Icelandic and French Wikisource pages (tools/content/wikisource.py); translations are our
own drafts (translation: "own"). Books in copyright, and PD books whose text we did not reach, have scene notes in our own
words or hang on a writer's place. What a cut changes is named in `checked`.

Coordinates are those of the place's Wikipedia article (cache/is/coords.json); Gljufrasteinn and Thristapar have none of
their own, so they use the articles of Mosfellsbaer and Vatnsdalsholar, and the place names say so.

Usage: python3 -I add_is1.py <app_dir> <coords.json> <wikisource_root>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-23"
b.init(APP, "", "is", DATE)
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

T_NJ, T_VE = "Brennu-Njáls saga/75", "Voyage au centre de la Terre/Chapitre 5"
EXIST = {"heimskringla"}

books = [
    BK("njals-saga", "Njáls saga", "尼亚尔萨迦", "Brennu-Njáls saga", "Anonymous", "佚名", "Anonymous", "13th century", lang="non",
       src=ws.url("is", "Brennu-Njáls saga"), aliases=["Brennu-Njáls saga", "Njála", "Gunnar of Hlíðarendi", "Hallgerður", "Bergþórshvoll"]),
    BK("journey-to-the-centre-of-the-earth", "Journey to the Centre of the Earth", "地心游记", "Voyage au centre de la Terre", "Jules Verne",
       "儒勒·凡尔纳", "Jules Verne", "1864", lang="fr", src=ws.url("fr", "Voyage au centre de la Terre"),
       aliases=["Voyage au centre de la Terre", "Lidenbrock", "Axel", "Arne Saknussemm", "Snæfellsjökull"]),
    BK("grettis-saga", "Grettir's Saga", "格雷蒂尔萨迦", "Grettis saga Ásmundarsonar", "Anonymous", "佚名", "Anonymous", "14th century", lang="non",
       aliases=["Grettis saga", "Grettla", "Grettir the Strong", "Drangey"]),
    BK("independent-people", "Independent People", "独立的人们", "Sjálfstætt fólk", "Halldór Laxness", "哈尔多尔·拉克斯内斯", "Halldór Laxness",
       "1934–1935", lang="is", pd=False, aliases=["Sjálfstætt fólk", "Laxness"]),
    BK("burial-rites", "Burial Rites", "葬礼", "Burial Rites", "Hannah Kent", "汉娜·肯特", "Hannah Kent", "2013", lang="en", pd=False,
       aliases=["Agnes Magnúsdóttir", "Þrístapar", "Illugastaðir"]),
    BK("jar-city", "Jar City", "瓶中城", "Mýrin", "Arnaldur Indriðason", "阿纳德·英德里达松", "Arnaldur Indriðason", "2000", lang="is", pd=False,
       aliases=["Mýrin", "Tainted Blood", "Erlendur", "Holberg", "Norðurmýri"]),
    BK("nonni", "Nonni", "农尼", "Nonni. Erlebnisse eines jungen Isländers, von ihm selbst erzählt", "Jón Sveinsson", "约恩·斯文松", "Jón Svensson",
       "1913", lang="de", aliases=["Nonni", "Nonni und Manni", "Jón Svensson", "Akureyri"]),
    BK("advent-gunnarsson", "Advent", "将临期", "Advent", "Gunnar Gunnarsson", "贡纳尔·贡纳松", "Gunnar Gunnarsson", "1936", lang="da", pd=False,
       aliases=["Aðventa", "The Good Shepherd", "Advent im Hochgebirge", "Benedikt"]),
]

places = [
    ORIG("is-hlidarendi", "Hlíðarendi, Fljótshlíð", "赫利达伦迪，弗廖茨赫利德",
         "Farm on the slopes of Fljótshlíð in south Iceland, home of Gunnar Hámundarson in Njáls saga. Sentenced to leave the country, Gunnar rides off to his ship, looks back at the slope, and turns home again; he is later killed defending his house here",
         "冰岛南部弗廖茨赫利德山坡上的农庄，《尼亚尔萨迦》里贡纳尔·哈蒙达松的家。他被判离开冰岛，骑马去上船时回头望了一眼山坡，便又回家了；后来他就在这里保卫自己的家时被杀"),
    ORIG("is-snaefellsjokull", "Snæfellsjökull", "斯奈菲尔冰川",
         "Glacier-capped volcano at the tip of the Snæfellsnes peninsula. In Journey to the Centre of the Earth, Professor Lidenbrock deciphers a message from the alchemist Arne Saknussemm telling him to go down its crater to reach the centre of the earth",
         "斯奈山半岛顶端一座冰川覆盖的火山。《地心游记》里，李登布洛克教授破译了炼金术士阿恩·萨克努塞姆留下的密信，信里说从它的火山口下去就能到达地心"),
    PIL("is-reykholt", "Reykholt", "雷克霍尔特",
        "Snorri Sturluson's home from 1206 until 1241; the medieval hot pool Snorralaug is named after him, and the Snorrastofa centre for medieval studies stands here. Snorri wrote Heimskringla, the sagas of the Norwegian kings",
        "斯诺里·斯图鲁松从 1206 年到 1241 年住在这里；中世纪的温泉池“斯诺里池”以他命名，这里还有研究中世纪的斯诺里中心。斯诺里写了挪威诸王的萨迦《挪威王列传》",
        ["heimskringla"]),
    PIL("is-gljufrasteinn", "Gljúfrasteinn, Mosfellsbær", "格柳夫拉斯泰恩，莫斯费德斯拜尔",
        "The house Halldór Laxness and his wife Auður built in 1945 by the river Kaldakvísl in Mosfellsdalur, near his childhood home Laxnes; a museum since 2004. Laxness won the Nobel Prize in 1955. (The pin is that of Mosfellsbær, the municipality the house is in)",
        "哈尔多尔·拉克斯内斯和妻子奥迪 1945 年在莫斯费德斯谷的卡尔达克维斯尔河边盖的房子，离他童年的家拉克斯内斯不远；2004 年起成为博物馆。拉克斯内斯 1955 年获得诺贝尔文学奖。（图钉位置是房子所在的莫斯费德斯拜尔镇）",
        ["independent-people"]),
    ORIG("is-thristapar", "Þrístapar, Vatnsdalshólar", "三丘，瓦特斯达尔丘陵",
         "Hillocks by Vatnsdalshólar in northwest Iceland where on 12 January 1830 Agnes Magnúsdóttir and Friðrik Sigurðsson were beheaded for the murder of two men, the last execution in Iceland. Plaques along the path carry lines from Hannah Kent's Burial Rites",
         "冰岛西北部瓦特斯达尔丘陵旁的几座小丘。1830 年 1 月 12 日，阿格妮丝·马格努斯多蒂尔和弗里德里克·西于尔扎松因谋杀两人在这里被斩首，这是冰岛最后一次执行死刑。小路边的牌子上刻着汉娜·肯特《葬礼》里的句子"),
    ORIG("is-nordurmyri", "Norðurmýri, Reykjavík", "北沼区，雷克雅未克",
         "Reykjavík neighbourhood where Jar City opens, with an old man found murdered in his flat; it gave the novel its Icelandic title, Mýrin",
         "雷克雅未克的一个街区，《瓶中城》开篇，一个老人在这里的公寓里被人杀死；小说的冰岛文书名《沼地》就取自这里"),
    PIL("is-nonnahus", "Nonnahús, Akureyri", "农尼之家，阿克雷里",
        "The childhood home of Jón Sveinsson, 'Nonni' (1857–1944), built around 1850 and one of the oldest houses in Akureyri; a museum since 1957. He left Iceland as a boy, became a Jesuit, and wrote twelve books in German about his Icelandic childhood and his brother Manni, the first in 1913",
        "约恩·斯文松（“农尼”，1857—1944）童年的家，约建于 1850 年，是阿克雷里最古老的房子之一，1957 年起成为博物馆。他少年时离开冰岛，后来成了耶稣会士，用德文写了十二本书，讲他在冰岛的童年和弟弟曼尼，第一本出版于 1913 年",
        ["nonni"]),
    PIL("is-skriduklaustur", "Skriðuklaustur", "斯克里祖修道院",
        "House with basalt walls and turf roof built in 1939 by Gunnar Gunnarsson (1889–1975) on the site of a late-medieval monastery; now a cultural centre dedicated to him. His novella Advent (1936), about the shepherd Benedikt who goes into the snowbound mountains of east Iceland each December to bring back lost sheep, first came out in German",
        "贡纳尔·贡纳松（1889—1975）1939 年在一座中世纪晚期修道院遗址上盖的房子，玄武岩墙、草皮屋顶，如今是纪念他的文化中心。他的中篇小说《将临期》（1936）写牧羊人本尼迪克特每年十二月走进冰岛东部积雪的群山，去找回走失的羊；这本书最早是用德文出版的",
        ["advent-gunnarsson"]),
    ORIG("is-reykir", "Reykir and Grettislaug (facing Drangey)", "雷基尔与格雷蒂尔池（对着德朗盖岛）",
         "Abandoned farm on the Skagafjörður shore facing the cliff island of Drangey, where the outlaw Grettir spent his last years with his brother Illugi and was killed in late autumn 1031. By the saga, Grettir swam from Drangey to Reykir and warmed himself in its hot spring; the rebuilt pool is called Grettislaug. (The island itself lies off the simplified coastline of our map, so the pin is on the shore)",
         "斯卡加湾岸边一座废弃的农庄，正对着峭壁环绕的德朗盖岛——亡命者格雷蒂尔和弟弟伊卢吉在岛上度过了最后几年，1031 年深秋在那里被杀。照萨迦的说法，格雷蒂尔从德朗盖岛游到雷基尔，在这里的温泉里取暖；重建的温泉池就叫“格雷蒂尔池”。（岛本身在我们简化过的海岸线以外，所以图钉放在岸上）"),
]

lines = [
    Q("is-nj-1", "njals-saga", "is-hlidarendi", "Chapter 75", "第七十五章", T_NJ,
      raw(T_NJ, "Þeir ríða fram að Markarfljóti.", "og fara hvergi.“", "is"), ["Hlíðarenda", "hlíðin"],
      "They rode down to the Markarfljót. Then Gunnar's horse stumbled and he sprang from the saddle.\nHis eyes turned up to the slope and to the farm at Hlíðarendi. Then he said: 'Fair is the slope, so fair that it has never seemed so fair to me, pale cornfields and mown hayfields, and I will ride back home and go nowhere.'",
      ["Hlíðarendi", "slope"],
      "他们骑马来到马卡尔河边。这时贡纳尔的马失了前蹄，他从马鞍上跳下来。\n他抬眼望向山坡，望向赫利达伦迪的农庄。于是他说：“这山坡真美，我从没觉得它这样美过：金黄的麦田，割过的草场。我要骑马回家，哪儿也不去了。”",
      ["赫利达伦迪", "山坡"], note=" (from the middle of a paragraph)", site="Icelandic"),
    Q("is-ve-1", "journey-to-the-centre-of-the-earth", "is-snaefellsjokull", "Chapter 5", "第五章", T_VE,
      raw(T_VE, "Il était conçu en ces termes", "j’ai fait.\nArne Saknussemm.", "fr"), ["Sneffels"],
      "It was worded thus:\nIn Sneffels Yoculis craterem kem delibat\numbra Scartaris Julii intra calendas descende,\naudas viator, et terrestre centrum attinges.\nKod feci. Arne Saknussem.\nWhich bad Latin may be translated as follows:\nGo down into the crater of the Yocul\nof Sneffels, which the shadow of Scartaris\ncomes to caress before the kalends of July,\nbold traveller, and you will reach\nthe centre of the Earth. Which I have done.\nArne Saknussemm.",
      ["Sneffels"],
      "原文是这样写的：\nIn Sneffels Yoculis craterem kem delibat\numbra Scartaris Julii intra calendas descende,\naudas viator, et terrestre centrum attinges.\nKod feci. Arne Saknussem.\n这几句蹩脚的拉丁文可以这样翻译：\n大胆的旅行者，七月初一以前，\n斯卡塔利斯的影子会来抚摸\n斯奈菲尔冰峰的火山口，\n从那里下去，你就能到达\n地心。我已经到过了。\n阿恩·萨克努塞姆。",
      ["斯奈菲尔"], site="French"),
]
lines += [
    S("is-burial-s1", "burial-rites", "is-thristapar", "Throughout", "全书",
      "In northern Iceland in 1829, Agnes Magnúsdóttir, condemned to death for the murder of two men, is sent to wait for her execution on an isolated farm, living with the farmer's family. The book ends with her beheading at Þrístapar in January 1830.",
      "1829 年，冰岛北部，阿格妮丝·马格努斯多蒂尔因谋杀两人被判死刑，被送到一座偏僻的农庄，和农庄主一家住在一起等待行刑。小说结尾，她于 1830 年 1 月在三丘被斩首。",
      ["Þrístapar"], ["三丘"], W + "Agnes_Magn%C3%BAsd%C3%B3ttir"),
    S("is-jar-s1", "jar-city", "is-nordurmyri", "Opening", "开篇",
      "An old man named Holberg is found in his basement flat in Norðurmýri, killed with a blow from a glass ashtray. Inspector Erlendur's search leads back to a rape decades before and to 'Jar City', an old collection of preserved organs.",
      "一个叫霍尔贝里的老人被发现死在北沼区的地下室公寓里，是被一只玻璃烟灰缸砸死的。埃伦杜尔探长追查下去，线索引向几十年前的一桩强奸案，也引向“瓶中城”——一批早年保存下来的器官标本。",
      ["Norðurmýri"], ["北沼区"], W + "Jar_City"),
    S("is-grettir-s1", "grettis-saga", "is-reykir", "The last chapters", "最后几章",
      "Outlawed and hunted, Grettir settles on the cliff island of Drangey with his brother Illugi and the slave Glaumur. When their fire goes out he swims to the mainland farm of Reykir, warms himself in a hot spring and brings fire back. In the end, lying wounded, he is killed on the island by Þorbjörn Öngull and his men.",
      "被宣布为亡命者、四处被追捕的格雷蒂尔，和弟弟伊卢吉、奴隶格劳穆尔一起在峭壁环绕的德朗盖岛上安身。他们的火熄了，他便游到对岸的雷基尔农庄，在温泉里暖过身子，把火带回岛上。最后，他负伤卧床时，在岛上被索尔比约恩·厄恩居尔一伙人杀死。",
      ["Drangey", "Reykir"], ["德朗盖岛", "雷基尔"], W + "Reykir"),
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

HEAD = "// Iceland, hand-written content (tools/content/batches/add_is1.py, 2026-11-23).\n"
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
