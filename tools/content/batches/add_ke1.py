"""11-24: Kenya, first pack: 5 new books (Out of Africa shared with Denmark, The Lusiads with Portugal), 7 places. Karen
Blixen's farm at the foot of the Ngong Hills, Ngugi's Limuru, Elspeth Huxley's Thika, Beryl Markham's Njoro, the Tsavo of
the man-eating lions, Camoes's Malindi and the Obama homestead at Kogelo.

The map has the eight provinces of before 2013 (Natural Earth), not the 47 counties that replaced them: a decision
taken with the atlas's owner on 2026-11-24.

Quotations (2 lines) are cut from Portuguese and English Wikisource pages (tools/content/wikisource.py); translations are
our own drafts. Books in copyright get scene notes with a fact source. What a cut changes is named in `checked`.

Coordinates are those of the place's English Wikipedia article (coords/add_ke1.json). The Tsavo point is the article's
point for the river; no source gave coordinates for the railway bridge itself.

Usage: python3 -I add_ke1.py <app_dir> <coords.json> <wikisource_root>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-24"
b.init(APP, "", "ke", DATE)
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

T_L2 = "Os Lusíadas (grafia atualizada)/II"
T_ME = "The Man-Eaters of Tsavo/Chapter 2"
EXIST = {"pt-lusiadas", "out-of-africa"}

def once(title, s, lang):
    """the cut must start at the only place the words stand on the page"""
    n = ws.text(os.path.join(WSR, lang), title).count(s)
    assert n == 1, (title, s, n)
    return s

books = [
    BK("man-eaters-of-tsavo", "The Man-Eaters of Tsavo", "察沃的食人狮", "The Man-Eaters of Tsavo", "John Henry Patterson", "约翰·亨利·帕特森",
       "John Henry Patterson", "1907", lang="en", src=ws.url("en", "The Man-Eaters of Tsavo"), aliases=["Tsavo lions", "Uganda Railway", "Patterson", "食人狮"]),
    BK("weep-not-child", "Weep Not, Child", "孩子，你别哭", "Weep Not, Child", "Ngũgĩ wa Thiong'o", "恩古吉·瓦·提安哥", "Ngũgĩ wa Thiong'o", "1964",
       lang="en", pd=False, aliases=["James Ngugi", "Ngugi wa Thiong'o", "Njoroge", "Mau Mau", "恩古吉"]),
    BK("flame-trees-of-thika", "The Flame Trees of Thika", "锡卡的火焰树", "The Flame Trees of Thika", "Elspeth Huxley", "埃尔斯佩思·赫胥黎", "Elspeth Huxley", "1959",
       lang="en", pd=False, aliases=["Memories of an African Childhood", "Thika", "Huxley"]),
    BK("west-with-the-night", "West with the Night", "夜航西飞", "West with the Night", "Beryl Markham", "柏瑞尔·马卡姆", "Beryl Markham", "1942",
       lang="en", pd=False, aliases=["Markham", "Njoro", "Beryl Clutterbuck"]),
    BK("dreams-from-my-father", "Dreams from My Father", "我父亲的梦想", "Dreams from My Father", "Barack Obama", "贝拉克·奥巴马", "Barack Obama", "1995",
       lang="en", pd=False, aliases=["A Story of Race and Inheritance", "Obama", "奥巴马", "Kogelo", "Alego"]),
]

places = [
    ORIG("ke-blixen", "Karen Blixen Museum, Nairobi", "卡伦·布里克森博物馆，内罗毕",
         "The farmhouse 'at the foot of the Ngong Hills', about 10 km from the centre of Nairobi, built in 1912 and bought with its land by Karen Blixen and her husband in 1917. She ran the coffee plantation here until she went back to Denmark for good in 1931; Out of Africa (1937) is her account of those years. The house opened as a national museum in 1986. The film of 1985 was shot not here but at her earlier farmhouse near by",
         "“恩贡山脚下”的农庄宅子，离内罗毕市中心约 10 公里，建于 1912 年，1917 年连同土地被卡伦·布里克森夫妇买下。她在这里经营咖啡种植园，直到 1931 年永久返回丹麦；《走出非洲》（1937）写的就是这些年。房子 1986 年作为国家博物馆开放。1985 年的电影不是在这里拍的，而是在附近她更早住过的另一处农舍"),
    ORIG("ke-limuru", "Limuru", "利穆鲁",
         "Town in the Kikuyu highlands north-west of Nairobi. Ngũgĩ wa Thiong'o was born in 1938 at Kamiriithu, close by; he wrote Weep Not, Child, the first novel in English published by an East African, as a student at Makerere in Uganda",
         "内罗毕西北基库尤高地上的小镇。恩古吉·瓦·提安哥 1938 年出生在附近的卡米里图；《孩子，你别哭》是东非人出版的第一部英语长篇小说，是他在乌干达马凯雷雷大学读书时写的"),
    ORIG("ke-thika", "Thika", "锡卡",
         "Town north-east of Nairobi. Elspeth Huxley's parents came here in 1912 to plant coffee, and she joined them in December 1913, aged six; The Flame Trees of Thika is the book she made of that childhood",
         "内罗毕东北的城镇。1912 年埃尔斯佩思·赫胥黎的父母来这里种咖啡，1913 年 12 月六岁的她来和他们团聚；《锡卡的火焰树》就是她根据这段童年写成的"),
    ORIG("ke-njoro", "Njoro", "恩乔罗",
         "Farming town on the western side of the Rift Valley, where Beryl Markham's father built his horse-racing farm and where she grew up",
         "裂谷西侧的农业小镇，柏瑞尔·马卡姆的父亲在这里建起赛马农场，她就在这里长大"),
    ORIG("ke-tsavo", "The Tsavo River", "察沃河",
         "River in what is now Tsavo West National Park. In March 1898 the builders of the railway from the coast to Uganda began a bridge over it under J. H. Patterson; between March and December two male lions killed many of the workmen, until Patterson shot them both. The pin is the river's point on the map, not the bridge",
         "河在今天的察沃西国家公园境内。1898 年 3 月，从海岸通往乌干达的铁路在帕特森主持下开始在河上架桥；3 月到 12 月间，两头雄狮咬死了许多工人，最后被帕特森先后射杀。图钉标的是这条河在地图上的位置，不是桥的位置"),
    ORIG("ke-malindi", "Malindi", "马林迪",
         "Old Swahili port on the Indian Ocean. Vasco da Gama came here in 1498, was well received, found a pilot for the crossing to India and set up the stone pillar that still stands on the shore. In The Lusiads the king of Malindi is the listener to whom da Gama tells the history of Portugal",
         "印度洋边古老的斯瓦希里港口。1498 年达·伽马来到这里，受到款待，找到了横渡印度洋的领航员，并立下一根石柱，至今还在海边。《卢济塔尼亚人之歌》里，达·伽马正是对着马林迪国王讲述葡萄牙的历史"),
    ORIG("ke-kogelo", "Nyang'oma Kogelo, Siaya", "尼扬奥马·科盖洛，锡亚亚",
         "Village in Siaya County, near Lake Victoria, where Barack Obama Sr. was raised. The last part of Dreams from My Father is his son's first journey to Kenya, in the 1980s, and to the family's homestead here",
         "维多利亚湖附近锡亚亚郡的村子，老贝拉克·奥巴马在这里长大。《我父亲的梦想》最后一部分写的是他的儿子 20 世纪 80 年代第一次来肯尼亚，回到这里的家族老宅"),
]

lines = [
    S("ke-oa-1", "out-of-africa", "ke-blixen", "The book as a whole", "全书",
      "Blixen's memoir of her coffee farm at the foot of the Ngong Hills: the Kikuyu who lived on its land, her cook Kamante and her Somali steward Farah, the flights over the hills with Denys Finch Hatton, and in the end the failure of the farm, its sale and her departure.",
      "布里克森对恩贡山脚下咖啡农场的回忆：住在农场土地上的基库尤人，她的厨子卡曼特和索马里管家法拉，与丹尼斯·芬奇·哈顿一起飞越群山，以及最后农场经营失败、被卖掉，她离开非洲。",
      ["Ngong Hills"], ["恩贡山"], "https://en.wikipedia.org/wiki/Karen_Blixen_Museum,_Kenya; https://en.wikipedia.org/wiki/Out_of_Africa"),
    S("ke-wn-1", "weep-not-child", "ke-limuru", "The novel as a whole", "全书",
      "Ngũgĩ, born near Limuru, sets his first novel in the Kikuyu country of his boyhood. Part one follows Njoroge, the first of his family to go to school; part two the rise of the Mau Mau movement and the years of the Emergency, which take the land, the family and the schooling away from him.",
      "出生在利穆鲁附近的恩古吉，把自己的第一部小说放在他少年时代的基库尤乡间。第一部写恩乔罗格——家里第一个上学的孩子；第二部写茅茅运动兴起和紧急状态的年月，土地、家人和学业一样样从他手里被夺走。",
      ["Limuru"], ["利穆鲁"], "https://en.wikipedia.org/wiki/Weep_Not,_Child; https://en.wikipedia.org/wiki/Ng%C5%A9g%C4%A9_wa_Thiong%27o"),
    S("ke-ft-1", "flame-trees-of-thika", "ke-thika", "The book as a whole", "全书",
      "The life of British settlers around Thika from 1913 to the outbreak of the First World War, seen through the eyes of a small girl whose parents have come to make a coffee farm out of bare bush.",
      "1913 年到第一次世界大战爆发之间锡卡一带英国移民的生活，由一个小女孩的眼睛看去——她的父母来到这里，要在一片荒野灌丛里开出咖啡农场。",
      ["Thika"], ["锡卡"], "https://en.wikipedia.org/wiki/The_Flame_Trees_of_Thika; https://en.wikipedia.org/wiki/Elspeth_Huxley"),
    S("ke-ww-1", "west-with-the-night", "ke-njoro", "The book as a whole", "全书",
      "Markham's memoir of growing up on her father's farm at Njoro in what was then British East Africa, of training racehorses and flying as a bush pilot, and of the flight of September 1936 that made her the first person to cross the Atlantic alone, non-stop, from east to west.",
      "马卡姆的回忆录：在当时的英属东非、父亲在恩乔罗的农场上长大，训练赛马，当丛林飞行员；1936 年 9 月，她成为第一个独自不着陆由东向西飞越大西洋的人。",
      ["Njoro"], ["恩乔罗"], "https://en.wikipedia.org/wiki/West_with_the_Night; https://en.wikipedia.org/wiki/Beryl_Markham"),
    S("ke-df-1", "dreams-from-my-father", "ke-kogelo", "Part 3, 'Kenya'", "第三部“肯尼亚”",
      "Obama comes to Kenya for the first time, meets his half-brothers and half-sisters in Nairobi and travels west with them to the family compound at Kogelo. There his grandmother tells him the story of his grandfather and his father, and he sits down between their two graves.",
      "奥巴马第一次来到肯尼亚，在内罗毕见到同父异母的兄弟姐妹，和他们一起西行，回到科盖洛的家族院落。祖母在那里给他讲祖父和父亲的故事，他在两人的坟墓之间坐了下来。",
      ["Kogelo"], ["科盖洛"], "https://en.wikipedia.org/wiki/Dreams_from_My_Father; https://en.wikipedia.org/wiki/Nyang%27oma_Kogelo"),
    Q("ke-lus-1", "pt-lusiadas", "ke-malindi", "Canto II, stanza 73", "第二章第 73 节", T_L2,
      raw(T_L2, once(T_L2, "Quando chegava a frota àquela parte,", "pt"), "E assim entravam ledos e guerreiros.", "pt"), ["Melinde"],
      "When the fleet came to that part\nfrom which the kingdom of Malindi could now be seen,\nit was decked with awnings, and gay in such a fashion\nas showed it honoured the holy day.\nThe flag trembles, the standard flies,\nthe crimson colour showed from afar;\ndrums and tambourines sound,\nand so they entered, glad and warlike.",
      ["Malindi"],
      "船队来到那一带海面，\n马林迪王国已经在望，\n船上张起彩篷，装点得喜气洋洋，\n显见是在敬重这神圣的日子。\n旗帜飘抖，军旗飞扬，\n远远就望见一片绛红；\n战鼓和铃鼓齐鸣，\n他们就这样欢欣又威武地驶入。",
      ["马林迪"], site="Portuguese"),
    EN("ke-ts-1", "man-eaters-of-tsavo", "ke-tsavo", "Chapter 2, 'The First Appearance of the Man-Eaters'", "第二章“食人狮初次出现”", T_ME,
       flow(raw(T_ME, once(T_ME, "Unfortunately this happy state of affairs did", "en"), "for about three\nweeks.", "en")), ["Tsavo"],
       "可惜好景不长，我们的工程很快就被粗暴而惊人地打断了。两头贪得无厌的食人狮出现了，在九个多月里，它们断断续续地袭击察沃一带的铁路和所有与铁路有关的人。到 1898 年 12 月，这终于演变成一场十足的恐怖统治，它们竟让铁路工程整整停顿了大约三个星期。",
       ["察沃"], note=" (the opening of the chapter; the page's hard line breaks joined; Chinese is our own)"),
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

HEAD = "// Kenya, hand-written content (tools/content/batches/add_ke1.py, 2026-11-24).\n"
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
