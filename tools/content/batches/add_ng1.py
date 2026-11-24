"""11-24: Nigeria, first pack: 6 books, 6 places. Achebe's Ogidi and Lagos, Soyinka's Ake in Abeokuta, Adichie's Nsukka and
Enugu, Flora Nwapa's Oguta Lake. The map has the 36 states and the Federal Capital Territory.

All six books are in copyright, so every line is a scene note in our own words with a fact source; there is no quotation
in this pack.

Coordinates are those of the place's English Wikipedia article (coords/add_ng1.json); Ake has no article of its own, so
its point is Abeokuta's.

Left out: Equiano's Interesting Narrative (its "Essaka" is only thought to be Isseke, and no source gave coordinates for
Isseke), Soyinka's Death and the King's Horseman (the page checked did not name the town) and anything from the north.

Usage: python3 -I add_ng1.py <app_dir> <coords.json> <wikisource_root>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-24"
b.init(APP, "", "ng", DATE)
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

EXIST = set()
ACHEBE = ("Chinua Achebe", "钦努阿·阿契贝", "Chinua Achebe")
ADICHIE = ("Chimamanda Ngozi Adichie", "奇玛曼达·恩戈兹·阿迪契", "Chimamanda Ngozi Adichie")
books = [
    BK("things-fall-apart", "Things Fall Apart", "瓦解", "Things Fall Apart", *ACHEBE, "1958", lang="en", pd=False,
       aliases=["Okonkwo", "Umuofia", "Achebe", "阿契贝", "这个世界土崩瓦解了"]),
    BK("no-longer-at-ease", "No Longer at Ease", "再也不得安宁", "No Longer at Ease", *ACHEBE, "1960", lang="en", pd=False,
       aliases=["Obi Okonkwo", "Achebe", "阿契贝"]),
    BK("ake-years-of-childhood", "Aké: The Years of Childhood", "阿凯：童年岁月", "Aké: The Years of Childhood", "Wole Soyinka", "沃莱·索因卡", "Wole Soyinka", "1981",
       lang="en", pd=False, aliases=["Ake", "Soyinka", "索因卡", "Abeokuta"]),
    BK("half-of-a-yellow-sun", "Half of a Yellow Sun", "半轮黄日", "Half of a Yellow Sun", *ADICHIE, "2006", lang="en", pd=False,
       aliases=["Biafra", "Ugwu", "Odenigbo", "Olanna", "Adichie", "阿迪契"]),
    BK("purple-hibiscus", "Purple Hibiscus", "紫木槿", "Purple Hibiscus", *ADICHIE, "2003", lang="en", pd=False,
       aliases=["Kambili", "Aunty Ifeoma", "Adichie", "阿迪契"]),
    BK("efuru", "Efuru", "埃弗鲁", "Efuru", "Flora Nwapa", "弗洛拉·恩瓦帕", "Flora Nwapa", "1966", lang="en", pd=False,
       aliases=["Uhamiri", "Oguta", "Nwapa"]),
]

places = [
    ORIG("ng-ogidi", "Ogidi, Anambra", "奥吉迪，阿南布拉州",
         "Igbo town near Onitsha, the ancestral town of Chinua Achebe's father; the family moved back here when Achebe was a small child, he grew up here, and he is buried here. Umuofia, the clan of Things Fall Apart, is invented, drawn from the Igbo world he knew",
         "奥尼查附近的伊博族城镇，钦努阿·阿契贝父亲的祖籍；阿契贝年幼时全家搬回这里，他在这里长大，死后也葬在这里。《瓦解》里的乌姆奥菲亚部族是虚构的，取材于他熟悉的伊博世界"),
    ORIG("ng-lagos", "Lagos Island", "拉各斯岛",
         "The old centre of Lagos, the capital of colonial Nigeria, on an island in the lagoon; the Marina and the head offices of the banks are here. No Longer at Ease, set in the last years of British rule, follows a young civil servant in this city",
         "拉各斯的老城中心，在潟湖中的岛上，殖民时期尼日利亚首府的所在地；滨海大道和各大银行总部都在这里。《再也不得安宁》写的是英国统治最后几年里，一个年轻公务员在这座城市的遭遇"),
    ORIG("ng-ake", "Aké, Abeokuta", "阿凯，阿贝奥库塔",
         "Quarter of the Yoruba city of Abeokuta where Wole Soyinka was born on 13 July 1934 into an Anglican family and spent his first twelve years. The pin stands at the centre of Abeokuta",
         "约鲁巴城市阿贝奥库塔的一个街区，沃莱·索因卡 1934 年 7 月 13 日出生在这里一个圣公会家庭，并在这里度过了最初的十二年。图钉标在阿贝奥库塔市中心"),
    ORIG("ng-nsukka", "Nsukka", "恩苏卡",
         "University town in Enugu State; the University of Nigeria, founded in 1955, opened here on 7 October 1960, six days after independence. Chimamanda Ngozi Adichie grew up in Nsukka, and both her first two novels come here",
         "埃努古州的大学城；1955 年创办的尼日利亚大学于 1960 年 10 月 7 日在这里正式开学，正是独立后的第六天。奇玛曼达·恩戈兹·阿迪契在恩苏卡长大，她的头两部小说都写到这里"),
    ORIG("ng-enugu", "Enugu", "埃努古",
         "Capital of Enugu State in the Igbo south-east. The Achike family of Purple Hibiscus lives here",
         "伊博人聚居的东南部埃努古州的首府。《紫木槿》里的阿奇克一家就住在这里"),
    ORIG("ng-oguta", "Oguta Lake, Imo", "奥古塔湖，伊莫州",
         "The largest natural lake in Imo State; Uhamiri is the goddess of the lake. Flora Nwapa was born at Oguta and went to school here, and Efuru, the first novel by a Nigerian woman to be published in English, is the story of a woman of a lakeside town whom the goddess chooses",
         "伊莫州最大的天然湖；乌哈米里是这座湖的女神。弗洛拉·恩瓦帕出生在奥古塔，也在这里上学。《埃弗鲁》是第一部以英语出版的尼日利亚女作家长篇小说，写的是湖边小镇上一个被女神选中的女人"),
]

lines = [
    S("ng-tf-1", "things-fall-apart", "ng-ogidi", "The novel as a whole", "全书",
      "Okonkwo is a famous man in Umuofia, a wrestler and a farmer who has made himself great. After a killing he is exiled for seven years to Mbanta, his mother's village; while he is away the white men come to Umuofia with their religion, and his son Nwoye goes over to the missionaries. He comes home to a clan that will not fight.",
      "奥贡喀沃是乌姆奥菲亚的名人，摔跤手，也是白手起家的农夫。一次杀人之后，他被流放到母亲的村子姆班塔七年；他不在的时候，白人带着他们的宗教来到乌姆奥菲亚，他的儿子恩沃耶投向了传教士。他回到家乡，却发现族人已不肯起来抗争。",
      ["Umuofia"], ["乌姆奥菲亚"], "https://en.wikipedia.org/wiki/Things_Fall_Apart"),
    S("ng-nl-1", "no-longer-at-ease", "ng-lagos", "The novel as a whole", "全书",
      "The novel begins in a Lagos courtroom, where Obi Okonkwo is on trial for taking a bribe, and then goes back: the people of Umuofia living in the cities collect money to send him to study in England; he comes home to a post on the Scholarship Board in Lagos, is offered a bribe almost at once, and falls in love with Clara, a nurse he may not marry because she is an osu, an outcast by descent.",
      "小说从拉各斯的法庭写起，奥比·奥贡喀沃因受贿受审，然后倒叙：住在各大城市的乌姆奥菲亚同乡凑钱送他去英国读书；他回国后在拉各斯的奖学金委员会任职，几乎立刻就有人来行贿；他爱上了护士克拉拉，却因为她是“奥苏”——世袭的贱民——而不能娶她。",
      ["Lagos"], ["拉各斯"], "https://en.wikipedia.org/wiki/No_Longer_at_Ease"),
    S("ng-ak-1", "ake-years-of-childhood", "ng-ake", "The memoir as a whole", "全书",
      "Soyinka's memoir of his boyhood in Aké before and during the Second World War: the first twelve years of his life, ending in 1946 when he leaves for Government College in Ibadan.",
      "索因卡对自己在阿凯度过的童年的回忆，时间在第二次世界大战之前和战争期间：从出生写到十二岁，1946 年他离家去伊巴丹的政府学院为止。",
      ["Aké"], ["阿凯"], "https://en.wikipedia.org/wiki/Ak%C3%A9:_The_Years_of_Childhood"),
    S("ng-hy-1", "half-of-a-yellow-sun", "ng-nsukka", "Part 1, 'The Early Sixties', and after", "第一部“六十年代初”及其后",
      "In the early 1960s Ugwu, a thirteen-year-old village boy, comes to Nsukka to work as houseboy for Odenigbo, a radical mathematics lecturer whose house is full of arguing intellectuals; Olanna leaves Lagos to live with him. When the south-east secedes as Biafra and the war comes, they have to flee Nsukka, and end up in the refugee town of Umuahia.",
      "六十年代初，十三岁的乡下男孩乌古来到恩苏卡，给激进的数学讲师奥登尼博当男仆，主人家里总是坐满争论不休的知识分子；奥兰娜离开拉各斯来和他同住。东南部宣布独立成立比亚法拉、战争爆发后，他们被迫逃离恩苏卡，最后落脚在难民聚集的乌穆阿希亚。",
      ["Nsukka"], ["恩苏卡"], "https://en.wikipedia.org/wiki/Half_of_a_Yellow_Sun"),
    S("ng-ph-1", "purple-hibiscus", "ng-enugu", "The novel as a whole", "全书",
      "Fifteen-year-old Kambili Achike grows up in a wealthy household in Enugu ruled by her father Eugene, a businessman, philanthropist and devout Catholic who beats his wife and children. A stay with Aunty Ifeoma, a lecturer at the university in Nsukka, shows her and her brother Jaja a noisier, freer way of living.",
      "十五岁的康比丽·阿奇克生长在埃努古一个富裕的家庭，家里由父亲尤金说了算——他是商人、慈善家、虔诚的天主教徒，却对妻子儿女拳脚相加。在恩苏卡大学教书的伊菲欧玛姑妈家住过一阵之后，她和哥哥扎扎才见到另一种更热闹、更自由的日子。",
      ["Enugu"], ["埃努古"], "https://en.wikipedia.org/wiki/Purple_Hibiscus"),
    S("ng-ef-1", "efuru", "ng-oguta", "The novel as a whole", "全书",
      "Efuru, daughter of the respected Nwashike Ogene, runs away with Adizua, a poor farmer who has paid no bride price; he abandons her and their daughter Ogonim, and the child dies. In time she is chosen by Uhamiri, the goddess of the lake, who gives her worshippers wealth and beauty but few children.",
      "埃弗鲁是受人敬重的恩瓦希克·奥格内的女儿，她跟着没付聘礼的穷农夫阿迪祖阿私奔；他抛下她和女儿奥贡尼姆，孩子后来也死了。后来她被湖的女神乌哈米里选中——这位女神给信徒财富和美貌，却很少给她们孩子。",
      ["the lake"], ["湖"], "https://en.wikipedia.org/wiki/Efuru; https://en.wikipedia.org/wiki/Oguta_Lake"),
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

HEAD = "// Nigeria, hand-written content (tools/content/batches/add_ng1.py, 2026-11-24).\n"
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
