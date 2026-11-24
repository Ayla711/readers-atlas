"""11-24: Romania, second pack: the five books that selection rule v2 adds (tools/selection/ro.md).
The Lucky Mill (Slavici, died 1925: public domain) gets a quotation, the opening of chapter II, cut from Romanian Wikisource
(tools/content/wikisource.py); English and Chinese are our own drafts. The other four are in copyright: scene notes.
The inn of the Lucky Mill is invented; the story puts it on the country road out of Ineu, so the book hangs at Ineu.
Strada Antim, where The Enigma of Otilia opens, has no article; the pin is Antim Monastery, which gives the street its name.
No photos yet for the five places.

Usage: python3 -I tools/content/batches/add_ro2.py <app_dir> tools/content/batches/coords/add_ro2.json <wikisource_root>"""
import glob, json, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-24"
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]
def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, lang, aliases, pd=False, src=None):
    return dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
                orig_lang=lang, public_domain=pd, source_url=src, author_orig=author_orig, aliases=aliases)
def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
def check(books, places, lines):
    allb = set()
    for f in glob.glob(os.path.join(APP, "data", "*", "books.js")): allb |= ids_in(f)
    assert not {x["id"] for x in books} & allb, {x["id"] for x in books} & allb
    oldp = ids_in(b.data("places.js"))
    assert not {p["id"] for p in places} & oldp and {p["id"] for p in places} == set(CO)
    assert not {l["id"] for l in lines} & ids_in(b.data("lines.js"))
    for l in lines:
        assert l["book_id"] in {x["id"] for x in books} and l["place_ids"][0] in {p["id"] for p in places}, l["id"]
    assert {l["book_id"] for l in lines} == {x["id"] for x in books}
    assert {l["place_ids"][0] for l in lines} == {p["id"] for p in places}
def restore_photo(pid, row):
    src = os.path.join(APP, "_to_delete", "photos_del_v2_1124", pid + ".jpg"); dst = os.path.join(APP, "images", "places", pid + ".jpg")
    if not os.path.exists(dst): shutil.copyfile(src, dst)
    cred = os.path.join(APP, "docs", "photo-credits.md"); t = open(cred, encoding="utf-8").read()
    if row not in t:
        open(cred + ".new", "w", encoding="utf-8").write(t.rstrip("\n") + "\n" + row + "\n"); os.replace(cred + ".new", cred)
import wikisource as ws
WSR = sys.argv[3]
b.init(APP, "", "ro", DATE)
T_MN = "Moara cu noroc"
def raw(title, start, end, lang="ro"):
    t = ws.text(os.path.join(WSR, lang), title)
    i = t.find(start); assert i >= 0, (title, start)
    j = t.find(end, i); assert j >= 0, (title, end)
    return t[i:j + len(end)]
def flow(s): return re.sub(r" {2,}", " ", s.replace("\n", " "))
def Q(id, book, place, loc, loc_zh, title, orig, hl_orig, en, hl_en, zh, hl_zh, note=""):
    assert "[" not in orig and "\xa0" not in orig, id
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls: assert h in text, (id, h)
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh, text_orig=orig, highlight_orig=hl_orig,
                text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh, translation="own", status="draft",
                checked=f"Romanian Wikisource, {title}{note}, {DATE}")
books = [
    BK("moara-cu-noroc", "The Lucky Mill", "幸运磨坊", "Moara cu noroc", "Ioan Slavici", "伊昂·斯拉维支", "Ioan Slavici", "1881", "ro",
       ["Moara cu noroc", "The Mill of Good Luck", "Ghiță", "Lică Sămădăul", "Slavici", "Novele din popor"], pd=True,
       src="https://ro.wikisource.org/wiki/Moara_cu_noroc"),
    BK("enigma-otiliei", "The Enigma of Otilia", "奥蒂莉亚之谜", "Enigma Otiliei", "George Călinescu", "乔治·克林内斯库", "George Călinescu", "1938", "ro",
       ["Enigma Otiliei", "Felix Sima", "Otilia", "Costache Giurgiuveanu", "Pascalopol", "Calinescu"]),
    BK("baltagul", "The Hatchet", "斧头", "Baltagul", "Mihail Sadoveanu", "米哈伊尔·萨多维亚努", "Mihail Sadoveanu", "1930", "ro",
       ["Baltagul", "Vitoria Lipan", "Nechifor Lipan", "Sadoveanu"]),
    BK("ultima-noapte", "The Last Night of Love, the First Night of War", "爱情的最后一夜，战争的第一夜", "Ultima noapte de dragoste, întâia noapte de război",
       "Camil Petrescu", "卡米尔·彼特雷斯库", "Camil Petrescu", "1930", "ro",
       ["Ultima noapte de dragoste", "Ștefan Gheorghidiu", "Ela", "Petrescu"]),
    BK("morometii", "The Moromete Family", "莫罗米特一家", "Moromeții", "Marin Preda", "马林·普雷达", "Marin Preda", "1955", "ro",
       ["Morometii", "Ilie Moromete", "Niculae", "Preda"]),
]
places = [
    b.ORIG("ro-ineu", "Ineu", "伊内乌", *C("ro-ineu"),
           "Small town in Arad County, in the west of Romania. Slavici's The Lucky Mill (1881) begins on the country road out of it: an hour and a half on, then over a rise, and in the next valley stands the mill turned inn, where the cobbler Ghiță comes to make money and falls in with Lică, chief of the swineherds. The inn is invented; the pin is the town",
           "罗马尼亚西部阿拉德县的小镇。斯拉维支的《幸运磨坊》（1881）从出镇的乡间大路写起：走一个半钟头，翻过一道坡，下一个山谷里就是由磨坊改成的客店——鞋匠吉策来这里挣钱，同猪倌头子利克搅到了一起。客店是虚构的，图钉标在镇上"),
    b.ORIG("ro-antim", "Antim Monastery and Strada Antim, Bucharest", "安蒂姆修道院与安蒂姆街，布加勒斯特", *C("ro-antim"),
           "Early eighteenth-century monastery in the old centre of Bucharest, and the street named after it. The Enigma of Otilia opens on Strada Antim on an evening at the beginning of July 1909, with the student Felix Sima looking for the house of his guardian, old Costache Giurgiuveanu. The pin is the monastery; the house is invented",
           "布加勒斯特老城里一座十八世纪初的修道院，以及因它得名的那条街。《奥蒂莉亚之谜》开篇就在安蒂姆街：1909 年 7 月初的一个傍晚，大学生费利克斯·西马在找监护人、老头科斯塔凯·久尔久韦亚努的家。图钉标的是修道院；那座房子是虚构的"),
    b.ORIG("ro-sabasa", "Sabasa, Neamț", "萨巴萨，尼亚姆茨县", *C("ro-sabasa"),
           "Mountain village in the Borca commune, on the upper Bistrița in Moldavia. In The Hatchet Vitoria Lipan, searching for her husband along the shepherds' road to Dorna, finds his body in a ravine near the Stânișoara Pass above the village, and it is at the funeral feast here that she faces the two men who killed him",
           "摩尔达维亚比斯特里察河上游、博尔卡乡的山村。《斧头》里，维多利亚·利潘沿着牧人去多尔纳的路寻找丈夫，在村子上方斯特尼绍阿拉山口附近的山沟里找到了他的尸体；她就是在这里的丧宴上，当面指出了杀他的两个人"),
    b.ORIG("ro-campulung", "Câmpulung", "肯普隆格", *C("ro-campulung"),
           "Town at the foot of the Carpathians in Argeș County. In The Last Night of Love, the First Night of War Ștefan Gheorghidiu's regiment is posted near by in the summer of 1916, and his wife Ela takes lodgings in the town to be near him; he gets leave to come down to her on the eve of Romania's entry into the war",
           "阿尔杰什县喀尔巴阡山脚下的小城。《爱情的最后一夜，战争的第一夜》里，1916 年夏天什特凡·格奥尔基迪乌的团驻扎在附近，妻子埃拉搬到城里住下，好离他近些；罗马尼亚参战前夕，他请了假下山来见她"),
    b.ORIG("ro-silistea", "Siliștea-Gumești, Teleorman", "锡利什泰亚-古梅什蒂，特列奥尔曼县", *C("ro-silistea"),
           "Village on the Wallachian Plain, in Teleorman County, the setting of Marin Preda's The Moromete Family: the first volume (1955) in the late 1930s, the second (1967) in the years of collectivisation after the war",
           "瓦拉几亚平原上特列奥尔曼县的村庄，马林·普雷达《莫罗米特一家》的故事就发生在这里：第一卷（1955）写 1930 年代末，第二卷（1967）写战后农业集体化的年代"),
]
lines = [
    Q("ro-mn-1", "moara-cu-noroc", "ro-ineu", "Chapter II, opening", "第二章开头", T_MN,
      flow(raw(T_MN, "De la Ineu drumul de țară", "Aici în vale e Moara cu noroc.")), ["Ineu"],
      "From Ineu the country road runs through woods and across ploughland, leaving to right and left the villages set in the corners of the valleys. For an hour and a half the road is good; then comes a steep rise, which you climb, and when you have come down into the valley again you must make a halt, water the horse or the ox from the yoke and give them time to get their breath, for the road has been rather hard, and further on the country is bad. Here in the valley is the Lucky Mill.",
      ["Ineu"],
      "从伊内乌出来，乡间大路穿过树林，越过田地，把坐落在山谷角落里的村庄撇在左右两边。头一个半钟头路好走；接着是一道陡坡，得爬上去，等你再下到谷里，就该歇一歇，饮饮马或者驾辕的牛，让它们喘口气，因为这段路不大好走，再往前的地方又不太平。就在这谷里，是幸运磨坊。",
      ["伊内乌"], note=" (line ends of the page joined; English and Chinese are our own)"),
    b.S("ro-eo-1", "enigma-otiliei", "ro-antim", "The opening and the novel as a whole", "开篇与全书",
        "Felix Sima, an orphan, comes from Iași to Bucharest to study medicine and to live with his guardian, the miser Costache Giurgiuveanu, in an old house on Strada Antim. There he meets Otilia, the old man's stepdaughter, and falls in love with her. Around them the Tulea clan, Costache's relatives, manoeuvre for his inheritance and to push Otilia out, and the older Pascalopol courts her. Whether she loves Felix is the enigma of the title.",
        "孤儿费利克斯·西马从雅西来到布加勒斯特学医，住进监护人、吝啬鬼科斯塔凯·久尔久韦亚努在安蒂姆街的老房子。他在那里遇见老人的继女奥蒂莉亚，爱上了她。在他们周围，科斯塔凯的亲戚图莱亚一家为他的遗产钩心斗角，要把奥蒂莉亚挤出去；年长的帕斯卡洛波尔也在追求她。她到底爱不爱费利克斯，就是书名里的那个谜。",
        ["Strada Antim"], ["安蒂姆街"], "https://www.themodernnovel.org/?p=5739; https://www.goodreads.com/book/show/41048792; https://en.wikipedia.org/wiki/George_C%C4%83linescu"),
    b.S("ro-ba-1", "baltagul", "ro-sabasa", "The end of the search", "寻找的终点",
        "The shepherd Nechifor Lipan goes to Dorna to buy sheep and does not come back. His wife Vitoria, sure that he is dead, sets out with their son Gheorghiță, who carries a hatchet, to follow his road from village to village. She learns that two shepherds who rode with him have grown suddenly richer. The family dog leads her to the body, the skull broken, in a ravine near the Stânișoara Pass; at the funeral feast in Sabasa she tells the story of the murder to the two men's faces, and they confess.",
        "牧人内基福尔·利潘去多尔纳买羊，一去不回。妻子维多利亚认定他已经死了，带着背斧头的儿子格奥尔基策上路，一个村一个村地沿着他走过的路打听。她得知同他一道骑马的两个牧人忽然阔了起来。家里的狗把她领到斯特尼绍阿拉山口附近的山沟里，找到了头骨碎裂的尸体；在萨巴萨的丧宴上，她当着那两个人的面把凶杀的经过讲了出来，他们招认了。",
        ["Sabasa"], ["萨巴萨"], "https://en.wikipedia.org/wiki/Baltagul"),
    b.S("ro-un-1", "ultima-noapte", "ro-campulung", "The last night of love", "爱情的最后一夜",
        "Ștefan Gheorghidiu, a philosophy student who has married his fellow student Ela, is consumed by jealousy. In 1916, a reserve officer on the fortifications above the Prahova valley and at Dâmbovicioara, he obtains leave and comes down to Câmpulung, where Ela has moved to be near him; he means to settle with her and the man he suspects. The second book is his front diary of Romania's first weeks at war, after which the jealousy no longer matters to him.",
        "哲学系学生什特凡·格奥尔基迪乌娶了同学埃拉，却被嫉妒吞没了。1916 年，他是后备军官，在普拉霍瓦河谷上方和登博维乔阿拉修筑工事。他请了假下山到肯普隆格——埃拉搬到那里，好离他近些——打算同她和他怀疑的那个男人做个了断。第二卷是罗马尼亚参战头几周他在前线的日记；经过这些，嫉妒对他已经无关紧要。",
        ["Câmpulung"], ["肯普隆格"], "https://www.themodernnovel.org/?p=31982; https://www.goodreads.com/author_blog_posts/8663167-ultima-noapte-de-dragoste-nt-ia-noapte-de-r-zboi-recenzie-rezumat"),
    b.S("ro-mo-1", "morometii", "ro-silistea", "Volume one", "第一卷",
        "Ilie Moromete, a respected peasant of Siliștea-Gumești, is sinking into debt: the land tax rises every year and the Depression has brought grain prices down. His three grown sons by his first marriage resent their stepmother and her children and want him to sell land so that they can leave for Bucharest. He refuses, and they go off with the horses and their sisters' dowry. He sells part of the land after all, to pay the tax and to send his youngest, Niculae, to school.",
        "伊利耶·莫罗米特是锡利什泰亚-古梅什蒂一个受人敬重的农民，却一步步陷进债里：土地税年年涨，大萧条又压低了粮价。前妻留下的三个成年儿子怨恨继母和她的孩子，要他卖地，好让他们去布加勒斯特。他不肯，他们就带着马和妹妹们的嫁妆走了。他终究还是卖掉一部分地，用来缴税，也供小儿子尼库拉耶上学。",
        ["Siliștea-Gumești"], ["锡利什泰亚-古梅什蒂"], "https://en.wikipedia.org/wiki/Morome%C8%9Bii"),
]
check(books, places, lines)
if __name__ == "__main__":
    M = "11-24: second pack, five books added under selection rule v2 (tools/content/batches/add_ro2.py)"
    b.append(b.data("books.js"), books, M); b.append(b.data("places.js"), places, M); b.append(b.data("lines.js"), lines, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
