"""11-24: Belgium, third pack: the two famous books held back as "place to be checked", hung on the nearest real place under
the rule for famous books (honest notes):
- Malpertuis (Jean Ray, 1943; in copyright, a scene note): the city of the house is never named, and no source found puts
  it in Ghent; hung at Ghent, where Ray was born, lived all his life and died (place type prototype, honest note).
- Happe-Chair (Camille Lemonnier, 1886; public domain): the town of the steelworks, le Culot, is invented and has not been
  matched to a real place. The novel names the Borinage, the coal country around Mons, where in chapter XXIX Clarinette
  recalls the riots between miners and troops as the strike begins: a quotation from French Wikisource, Happe-Chair
  (Lemonnier)/Chapitre XXIX. The edition's hard line breaks are joined with spaces, and its no-break spaces before ; are
  written as plain spaces.
Photos: tools/content/batches/add_photos_held_1124.py.

Usage: python3 -I tools/content/batches/add_be3.py <app_dir> tools/content/batches/coords/add_be3.json <wikisource_root>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP = sys.argv[1]
CO = json.load(open(sys.argv[2], encoding="utf-8")) if len(sys.argv) > 2 and sys.argv[2].endswith(".json") else {}
DATE = "2026-11-24"
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]
def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, lang, aliases, pd=False, src=None):
    return dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
                orig_lang=lang, public_domain=pd, source_url=src, author_orig=author_orig, aliases=aliases)
def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
def check(books, places, lines, ext=(), elsewhere=()):
    """ext: books already in the app (another country's books.js) that get a line here;
    elsewhere: books added here whose line goes into another country's data (another batch script)"""
    allb = set()
    for f in glob.glob(os.path.join(APP, "data", "*", "books.js")): allb |= ids_in(f)
    new = {x["id"] for x in books}
    assert not new & allb, new & allb
    assert set(ext) <= allb, set(ext) - allb
    assert not {p["id"] for p in places} & ids_in(b.data("places.js")) and {p["id"] for p in places} == set(CO)
    assert not {l["id"] for l in lines} & ids_in(b.data("lines.js"))
    bk = new | set(ext)
    for l in lines:
        assert l["book_id"] in bk and l["place_ids"][0] in {p["id"] for p in places}, l["id"]
    assert {l["book_id"] for l in lines} | set(elsewhere) == bk
    assert {l["place_ids"][0] for l in lines} == {p["id"] for p in places}
def run(books, places, lines, script):
    M = f"11-24: famous books hung on their nearest real place (tools/content/batches/{script})"
    for name, xs in (("books.js", books), ("places.js", places), ("lines.js", lines)):
        if xs: b.append(b.data(name), xs, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
import wikisource as ws
WSR = sys.argv[3]
WS = "https://fr.wikisource.org/wiki/"
def Q(id, book, place, loc, loc_zh, title, orig, hl_orig, en, hl_en, zh, hl_zh):
    assert "[" not in orig and "\xa0" not in orig and "\n" not in orig, id
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls: assert h in text, (id, h)
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh, text_orig=orig, highlight_orig=hl_orig,
                text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh, translation="own", status="draft",
                checked=f"French Wikisource, {title}, {DATE}")
b.init(APP, "", "be", DATE)
T_HC = "Happe-Chair (Lemonnier)/Chapitre XXIX"
HC = ws.block(os.path.join(WSR, "fr"), T_HC, "Clarinette, elle, dans son éternelle sottise, jubilait.",
              "faire tirer sur le peuple.").replace("\n", " ").replace("\xa0", " ")
books = [
    BK("malpertuis", "Malpertuis", "马尔佩蒂", "Malpertuis", "Jean Ray", "让·雷", "Jean Ray", "1943", "fr",
       ["Malpertuis: histoire d'une maison fantastique", "Cassave", "Jean-Jacques Grandsire", "John Flanders"]),
    BK("happe-chair", "Happe-Chair", "Happe-Chair", "Happe-Chair", "Camille Lemonnier", "卡米耶·勒莫尼耶", "Camille Lemonnier",
       "1886", "fr", ["Happe-chair", "Clarinette", "le Culot"], pd=True, src=WS + "Happe-Chair_(Lemonnier)"),
]
places = [
    b.PROTO("be-ghent", "Ghent", "根特", *C("be-ghent"),
            "the old Flemish city where the house Malpertuis stands in Jean Ray's Malpertuis (1943). The city is never named and no source we found places the house; Ray was born in Ghent in 1887, lived there all his life and died there in 1964, and the book is hung at Ghent as the nearest real place",
            "让·雷《马尔佩蒂》（1943）里那座宅子所在的佛兰德老城。书里始终没点城名，查到的资料也没有落实宅子在哪里；让·雷 1887 年生在根特，一辈子住在那里，1964 年也死在那里，这本书就近挂在根特"),
    b.PROTO("be-borinage", "The Borinage", "博里纳日", *C("be-borinage"),
            "the steelworks country of Camille Lemonnier's Happe-Chair (1886), a novel of the drudgery of mill workers. The book's own town, le Culot, is invented and has not been matched to a real place; the Borinage, the coal-mining district around Mons whose riots between miners and troops the book recalls, is the nearest real place it names",
            "卡米耶·勒莫尼耶《Happe-Chair》（1886）这部写钢铁厂工人苦役生活的小说里的工业地带。书里的小镇“勒屈洛”是虚构的，没有对上任何真实地点；博里纳日是蒙斯周围的煤矿区，书里回忆了那里矿工和军队的冲突，它是书中点名的离故事最近的真实地方"),
]
lines = [
    b.S("be-mp-1", "malpertuis", "be-ghent", "The novel as a whole", "全书",
        "Young Jean-Jacques Grandsire tells how he and a strange crowd of relatives and hangers-on gathered at Malpertuis, the gloomy house of his rich uncle Cassave, to wait at the old man's deathbed: the three Cormelon sisters, Cassave's friend and doctor Sambucque, and others odder still. Cassave's will leaves them his fortune on condition that they go on living in the house. Told through several manuscripts, the secret comes out piece by piece: Cassave had captured the dying gods of Olympus and trapped them in the shabby bodies of ordinary people. (The city is never named; Ray lived all his life in Ghent.)",
        "少年让-雅克·格朗西尔讲述：他和一群古怪的亲戚、食客聚到马尔佩蒂——他有钱的叔叔卡萨夫那座阴森的宅子，守在老人的临终床边：科尔梅隆家的三姐妹、卡萨夫的朋友兼医生桑比克，还有更怪的人。卡萨夫的遗嘱把财产留给他们，条件是他们必须继续住在这座宅子里。故事由几份手稿拼成，秘密一点点露出来：卡萨夫捉住了奄奄一息的奥林波斯众神，把他们关进了普通人寒酸的肉身里。（书里始终没点城名；让·雷一辈子住在根特。）",
        ["Ghent"], ["根特"],
        "https://www.goodreads.com/author_blog_posts/22703915-malpertuis-by-jean-ray; https://core.ac.uk/download/223978633.pdf; https://www.lalibre.be/culture/livres-bd/2016/05/30/jean-ray-admirablement-ressuscite-R4LCUB7RYVFJLCJNU6SL7XQQAY/; https://www.flagey.be/en/activity/255-malpertuis-cycle-de-films-orson-welles-sci-fi-drama"),
    Q("be-hc-1", "happe-chair", "be-borinage", "Chapter XXIX: the strike begins", "第二十九章：罢工开始", T_HC,
      HC, ["Borinage"],
      "Clarinette, in her everlasting foolishness, was jubilant. The idea of a social breakdown, of a disorder that would set master and worker at each other's throats, stirred up a murky anarchist depth in her. As a little girl she had heard tell of the scenes of looting and violence that had at times convulsed the Borinage; villages had been bloodied by clashes between the troops and the miners; everything in the collieries had been smashed; and she remembered Lerminia, her father, saying with a fierce gesture that if he had been there, he would have aimed at the heads of the officers rotten enough to have the people fired on.",
      ["Borinage"],
      "克拉丽内特呢，还是那副一贯的蠢相，高兴得不得了。想到社会要乱套，想到一场要让老板和工人拼个你死我活的大乱子，她心底那股浑浊的无政府念头就翻腾起来。她还很小的时候，就听人讲过博里纳日有时闹出的那些打砸和暴力：一个个村子在军队和矿工的冲突里流了血；煤矿里的东西全被砸烂了；她还记得她父亲莱尔米尼亚做着一个凶狠的手势说，要是他在场，那些坏到下令朝老百姓开枪的军官，他准瞄着他们的脑袋打。",
      ["博里纳日"]),
]
check(books, places, lines)
if __name__ == "__main__":
    run(books, places, lines, "add_be3.py")
