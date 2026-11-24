"""11-23: Hungary, first pack: 8 new books, 7 places. Gardonyi's Eger, Attila Jozsef's Danube bank, Petofi's Great Plain and
his National Song at the National Museum, Molnar's Paul Street Boys, Jokai's Balatonfured, Moricz's Debrecen College and
Krasznahorkai's Gyula.

Quotations (3 lines) are cut from Hungarian Wikisource pages (tools/content/wikisource.py); translations are our own drafts
(translation: "own"). Books in copyright, and PD books whose text we did not reach, have scene notes in our own words or
hang on a writer's place. What a cut changes is named in `checked`.

Coordinates are those of the place's Hungarian Wikipedia article (cache/hu/coords.json).

Usage: python3 -I add_hu1.py <app_dir> <coords.json> <wikisource_root>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-23"
b.init(APP, "", "hu", DATE)
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

HUW = "https://hu.wikipedia.org/wiki/"
T_EG, T_DU, T_AF = "Egri csillagok/4. rész", "A Dunánál", "Az Alföld"
EXIST = set()

books = [
    BK("egri-csillagok", "Eclipse of the Crescent Moon", "埃格尔之星", "Egri csillagok", "Géza Gárdonyi", "加尔多尼·盖佐", "Gárdonyi Géza", "1899",
       lang="hu", src=ws.url("hu", "Egri csillagok"), aliases=["Egri csillagok", "Stars of Eger", "Dobó István", "Bornemissza Gergely", "Eger"]),
    BK("a-dunanal", "By the Danube", "在多瑙河畔", "A Dunánál", "Attila József", "尤若夫·阿蒂拉", "József Attila", "1936", lang="hu",
       src=ws.url("hu", "A Dunánál"), aliases=["A Dunánál", "József Attila", "Danube"]),
    BK("az-alfold", "The Great Plain", "阿尔弗德", "Az Alföld", "Sándor Petőfi", "裴多菲", "Petőfi Sándor", "1844", lang="hu",
       src=ws.url("hu", "Az Alföld"), aliases=["Az Alföld", "Alföld", "Kiskunság", "Petőfi"]),
    BK("nemzeti-dal", "National Song", "民族之歌", "Nemzeti dal", "Sándor Petőfi", "裴多菲", "Petőfi Sándor", "1848", lang="hu",
       src=ws.url("hu", "Nemzeti dal"), aliases=["Nemzeti dal", "Talpra magyar", "Petőfi", "15 March 1848"]),
    BK("pal-utcai-fiuk", "The Paul Street Boys", "帕尔街的孩子们", "A Pál utcai fiúk", "Ferenc Molnár", "莫尔纳·费伦茨", "Molnár Ferenc", "1906",
       lang="hu", aliases=["A Pál utcai fiúk", "Nemecsek", "Boka", "grund", "Józsefváros"]),
    BK("az-arany-ember", "The Man with the Golden Touch", "金人", "Az arany ember", "Mór Jókai", "约卡伊·莫尔", "Jókai Mór", "1872", lang="hu",
       src=ws.url("hu", "Az arany ember"), aliases=["Az arany ember", "Timár Mihály", "Tímea", "Jókai"]),
    BK("legy-jo-mindhalalig", "Be Faithful Unto Death", "至死不渝", "Légy jó mindhalálig", "Zsigmond Móricz", "莫里茨·日格蒙德", "Móricz Zsigmond",
       "1920", lang="hu", aliases=["Légy jó mindhalálig", "Nyilas Misi", "Debrecen", "Móricz"]),
    BK("satantango", "Satantango", "撒旦探戈", "Sátántangó", "László Krasznahorkai", "克拉斯诺霍尔卡伊·拉斯洛", "Krasznahorkai László", "1985",
       lang="hu", pd=False, aliases=["Sátántangó", "Krasznahorkai", "Béla Tarr"]),
]

places = [
    ORIG("hu-eger-castle", "Eger Castle", "埃格尔城堡",
         "The castle whose defenders under István Dobó held out against the Ottoman army in the siege of 1552, the story of Gárdonyi's Eclipse of the Crescent Moon. Gárdonyi moved to Eger in 1897, lived there until his death in 1922 and is buried in the castle",
         "1552 年，伊什特万·多博率领守军在这座城堡里顶住了奥斯曼大军的围攻，加尔多尼的《埃格尔之星》写的就是这场围城战。加尔多尼 1897 年迁居埃格尔，在这里一直住到 1922 年去世，死后葬在城堡里"),
    ORIG("hu-kossuth-ter", "Attila József statue, Kossuth tér (Danube bank)", "尤若夫·阿蒂拉像，科苏特广场（多瑙河岸）",
         "The square by the Parliament on the Pest bank of the Danube, where László Marton's bronze statue of Attila József, sitting as in the opening of By the Danube and itself called A Dunánál, has stood since 1980",
         "佩斯一侧多瑙河岸、国会大厦旁的广场。马尔东·拉斯洛塑造的尤若夫·阿蒂拉铜像 1980 年在这里落成，诗人坐着，正如《在多瑙河畔》开头那样，雕像本身也叫《在多瑙河畔》"),
    ORIG("hu-bugac", "Bugac (Kiskunság)", "布加奇（基什昆沙格）",
         "Village on the Great Plain between the Danube and the Tisza, about 40 km south of Kecskemét, much of whose land lies in the Kiskunság National Park: the puszta of herds, draw-wells and mirages that Petőfi's The Great Plain (1844) celebrates",
         "多瑙河与蒂萨河之间大平原上的村庄，在凯奇凯梅特以南约 40 公里，大片土地属于基什昆沙格国家公园——正是裴多菲《阿尔弗德》（1844）歌颂的那片有牛群、吊杆井和海市蜃楼的草原"),
    PIL("hu-museum", "Hungarian National Museum, Budapest", "匈牙利国家博物馆，布达佩斯",
        "On 15 March 1848 Petőfi recited his National Song, written two days before, at the Pilvax café and elsewhere in Pest; in the afternoon a great crowd gathered at the Museum, where printed copies of the poem and the Twelve Points were handed out. The picture of Petőfi reciting it on the Museum steps is a later legend, but the national day is still marked there each year. In The Paul Street Boys, the marbles are taken from Nemecsek and his friends in the Museum garden",
        "1848 年 3 月 15 日，裴多菲在佩斯的皮尔瓦克斯咖啡馆等地朗诵了两天前写成的《民族之歌》；下午，大批群众聚集到博物馆前，印好的诗和《十二条》在这里分发。说裴多菲站在博物馆台阶上朗诵这首诗，是后来的传说，但每年的国庆纪念仍在这里举行。《帕尔街的孩子们》里，内梅切克和朋友们的玻璃球就是在博物馆的花园里被抢走的",
        ["nemzeti-dal"]),
    PIL("hu-jokai-villa", "Jókai Memorial House, Balatonfüred", "约卡伊纪念馆，巴拉顿菲赖德",
        "The villa by Lake Balaton built in 1870, where Mór Jókai and his wife, the actress Róza Laborfalvi, spent their summers for some twenty years. Here he wrote The Man with the Golden Touch, part of which takes place on the Balaton shore",
        "巴拉顿湖畔 1870 年建成的别墅，约卡伊·莫尔和妻子、女演员拉博尔法尔维·罗饶在这里度过了大约二十个夏天。他在这里写了《金人》，书中有一部分就发生在巴拉顿湖岸",
        ["az-arany-ember"]),
    ORIG("hu-debrecen-kollegium", "Reformed College, Debrecen", "德布勒森归正会学院",
         "The great Protestant school of Debrecen, where Be Faithful Unto Death is set in 1892. Móricz was himself a pupil of its gymnasium for four years",
         "德布勒森著名的新教学校，《至死不渝》的故事 1892 年就发生在这里。莫里茨本人也在它的文科中学读过四年书"),
    PIL("hu-gyula", "Gyula", "久洛",
        "Small town in southeast Hungary near the Romanian border, where László Krasznahorkai, winner of the 2025 Nobel Prize in Literature, was born in 1954. His first novel, Satantango (1985), is set on a nearly abandoned collective farm in a similarly remote rural area",
        "匈牙利东南部靠近罗马尼亚边境的小城，2025 年诺贝尔文学奖得主克拉斯诺霍尔卡伊·拉斯洛 1954 年生于此地。他的第一部小说《撒旦探戈》（1985）就发生在一处同样偏远的乡下、一个几乎被遗弃的集体农庄里",
        ["satantango"]),
]

lines = [
    Q("hu-eg-1", "egri-csillagok", "hu-eger-castle", "Part 4 'The Peril of Eger', section 4: Dobó's oath", "第四部《埃格尔的危难》第 4 节：多博的誓言", T_EG,
      raw(T_EG, "- Esküdjetek velem", "zúgták egy hanggal.", "hu"), ["az egri vár"],
      "'Swear with me,' said Dobó.\nEveryone in the hall stretched out a hand towards the crucifix.\n'I swear by the one living God...'\n'I swear by the one living God,' came the solemn murmur.\n'...that I devote my blood and my life to the homeland and the king, to the defence of the castle of Eger. Neither force nor cunning shall frighten me. Neither money nor promise shall sway me. I will neither speak nor listen to a word about the surrender of the castle. I will not give myself up alive, neither inside the castle nor outside it. In the defence of the castle I will submit my will, from beginning to end, to the command of those above me. So help me God!'\n'So help me God!' they thundered with one voice.",
      ["castle of Eger"],
      "“跟我一起宣誓。”多博说。\n大厅里每个人都向十字架伸出手。\n“我向唯一永生的上帝起誓……”\n“我向唯一永生的上帝起誓。”响起一片庄严的低语。\n“……我把我的鲜血和生命献给祖国和国王，献给埃格尔城堡的防守。武力和诡计都吓不倒我。金钱和许诺都动摇不了我。关于交出城堡，我一句话也不说，一句话也不听。无论在城堡里还是城堡外，我都绝不活着投降。在城堡的防守中，我自始至终服从上级的命令。愿上帝帮助我！”\n“愿上帝帮助我！”众人齐声高呼。",
      ["埃格尔城堡"], site="Hungarian"),
    Q("hu-du-1", "a-dunanal", "hu-kossuth-ter", "Part 1, first stanza", "第一部分第一节", T_DU,
      raw(T_DU, "A rakodópart alsó kövén ültem,", "nagy volt a Duna.", "hu"), ["A rakodópart", "Duna"],
      "I sat on the lowest stone of the quay\nand watched a melon rind float away.\nSunk in my fate, I hardly heard\nhow the surface chatters and the depths are still.\nAs if it had flowed on out of my heart,\nmurky, wise and great was the Danube.",
      ["quay", "Danube"],
      "我坐在码头最低的石阶上，\n看着一块瓜皮漂走。\n我沉在自己的命运里，几乎没听见\n水面在喋喋不休，深处却一声不响。\n仿佛是从我心里流出去的，\n多瑙河浑浊、睿智而又宏大。",
      ["码头", "多瑙河"], site="Hungarian"),
    Q("hu-af-1", "az-alfold", "hu-bugac", "Stanzas 2–4 and the last", "第二至四节和最后一节", T_AF,
      raw(T_AF, "Lenn az alföld tengersík vidékin", "kettős ága várja.", "hu") + GAP + raw(T_AF, "Szép vagy, alföld,", "a sír is fölöttem.", "hu"),
      ["alföld", "Kis-Kunságnak"],
      "Down on the sea-flat lands of the Alföld,\nthere I am at home, there is my world;\nmy eagle soul is freed from its prison\nwhen I see the endlessness of the plains.\nThen in my thoughts I fly up\nbeyond the earth, close to the clouds,\nand smiling at me from the Danube\nto the Tisza lies the picture of the plain.\nUnder the sky of mirages the hundred fat herds\nof the Kiskunság clang their bells;\nat noon, by the long-sweep well,\nthe wide double trough awaits them.\n…\nYou are beautiful, Alföld, to me at least you are beautiful!\nHere my cradle was rocked, here I was born.\nHere let the shroud cover me, here\nlet the grave be heaped over me.",
      ["Alföld", "Kiskunság"],
      "在下面阿尔弗德海一样平坦的原野上，\n那里才是我的家，那里才是我的世界；\n每当我望见无边无际的平原，\n我那鹰一样的灵魂就挣脱了牢笼。\n这时我在想象中飞起，\n飞离大地，飞近云端，\n从多瑙河一直铺到蒂萨河的\n平原的景色向我微笑。\n海市蜃楼的天空下，\n基什昆沙格的上百群肥牛摇响铃铛；\n正午歇晌时，长杆吊井旁，\n宽宽的双槽在等着它们。\n…\n你真美，阿尔弗德，至少对我是美的！\n我的摇篮在这里摇过，我在这里出生。\n就让裹尸布在这里盖住我，\n就让坟墓也在这里隆起在我身上。",
      ["阿尔弗德", "基什昆沙格"], note=" (two passages: stanzas 2–4 and the last stanza)", site="Hungarian"),
]
lines += [
    S("hu-pal-s1", "pal-utcai-fiuk", "hu-museum", "Chapter 2, the 'einstand'", "第二章，“缴械”",
      "In 1889 the boys of Pál utca in Budapest's Józsefváros defend their 'grund', a vacant lot, against the Redshirts. Early in the book little Nemecsek and two friends are playing marbles in the garden of the National Museum when the Pásztor brothers take the marbles off them. A bronze group of the scene by Péter Szanyi has stood in Práter utca since 2007.",
      "1889 年，布达佩斯约瑟夫城帕尔街的孩子们保卫他们的“空场”，同红衫队对抗。故事开头不久，小内梅切克和两个朋友正在国家博物馆的花园里打玻璃球，帕斯托尔兄弟俩把球抢走了。2007 年起，普拉特街上立着萨尼·彼得塑造的这一幕的青铜群像。",
      ["National Museum"], ["国家博物馆"], W + "The_Paul_Street_Boys"),
    S("hu-legy-s1", "legy-jo-mindhalalig", "hu-debrecen-kollegium", "Throughout", "全书",
      "The novel follows Misi Nyilas, a young pupil of the Reformed College in Debrecen, through the year 1892. Móricz drew on his own school years there, though the story is not simply his own memories.",
      "小说写的是德布勒森归正会学院的小学生尼拉什·米希在 1892 年这一年的经历。莫里茨借用了自己在这里读书的经历，但故事并不只是他本人的回忆。",
      ["Debrecen"], ["德布勒森"], "https://mnl.gov.hu/download/file/fid/629032"),
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

HEAD = "// Hungary, hand-written content (tools/content/batches/add_hu1.py, 2026-11-23).\n"
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
