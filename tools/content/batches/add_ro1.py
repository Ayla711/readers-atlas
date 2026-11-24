"""11-24: Romania, first pack: 7 new books (Dracula shared with the UK), 8 places. Stoker's Bistritz, Creanga's Humulesti,
Ovid's Tomis, Rebreanu's Prislop, the Colt citadel (Verne), Eminescu's Ipotesti, Traian Square in Timisoara (Herta Muller)
and Colentina in Bucharest (Cartarescu). The map has Romania's eight development regions.

Quotations (5 lines) are cut from English, Romanian, Latin and French Wikisource pages (tools/content/wikisource.py);
translations are our own drafts. Books in copyright get scene notes with a fact source. What a cut changes is named in
`checked`.

Coordinates are those of the place's English or Romanian Wikipedia article (cache/ro/coords.json).

Usage: python3 -I add_ro1.py <app_dir> <coords.json> <wikisource_root>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-24"
b.init(APP, "", "ro", DATE)
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

T_DR = "Dracula/Chapter 1"
T_AM = "Amintiri din copilărie"
T_TR = "Tristia/Liber III"
T_IO = "Ion (Rebreanu)/1. Glasul pământului"
T_CC = "Le Château des Carpathes/1"
EXIST = {"dracula"}

books = [
    BK("amintiri-din-copilarie", "Memories of My Boyhood", "童年回忆", "Amintiri din copilărie", "Ion Creangă", "扬·克里昂格", "Ion Creangă", "1881–1892",
       lang="ro", src=ws.url("ro", T_AM), aliases=["Childhood Memories", "Recollections from Childhood", "Nică", "Humulești", "Creangă"]),
    BK("tristia", "Tristia", "哀歌集", "Tristia", "Ovid", "奥维德", "Publius Ovidius Naso", "AD 9–12", lang="la",
       src=ws.url("la", "Tristia"), aliases=["Sorrows", "Tomis", "Ovid's exile", "Ovidiu"]),
    BK("rebreanu-ion", "Ion", "伊昂", "Ion", "Liviu Rebreanu", "利维乌·雷布雷亚努", "Liviu Rebreanu", "1920", lang="ro",
       src=ws.url("ro", "Ion (Rebreanu)"), aliases=["Pripas", "Armadia", "Ion Pop al Glanetașului", "Ana", "Florica", "Rebreanu"]),
    BK("carpathian-castle", "The Carpathian Castle", "喀尔巴阡古堡", "Le Château des Carpathes", "Jules Verne", "儒勒·凡尔纳", "Jules Verne", "1892",
       lang="fr", src=ws.url("fr", "Le Château des Carpathes"), aliases=["The Castle of the Carpathians", "Werst", "Rodolphe de Gortz", "La Stilla"]),
    BK("luceafarul", "The Evening Star", "金星", "Luceafărul", "Mihai Eminescu", "爱明内斯库", "Mihai Eminescu", "1883", lang="ro",
       src=ws.url("ro", "Luceafărul (Eminescu)"), aliases=["Luceafărul", "Hyperion", "The Morning Star", "Eminescu", "Ipotești"]),
    BK("land-of-green-plums", "The Land of Green Plums", "心兽", "Herztier", "Herta Müller", "赫塔·米勒", "Herta Müller", "1994", lang="de",
       pd=False, aliases=["Herztier", "Lola", "Securitate", "Timișoara", "Temeswar"]),
    BK("solenoid", "Solenoid", "螺线管", "Solenoid", "Mircea Cărtărescu", "米尔恰·克尔特雷斯库", "Mircea Cărtărescu", "2015", lang="ro",
       pd=False, aliases=["Maica Domnului", "Colentina", "Cărtărescu", "Bucharest"]),
]

places = [
    ORIG("ro-bistrita", "Bistrița (Stoker's Bistritz)", "比斯特里察（斯托克笔下的比斯特里茨）",
         "Old Saxon town in north-eastern Transylvania. In Dracula, Jonathan Harker reaches 'Bistritz' on 3 May and spends his last night at the Golden Krone Hotel before the coach takes him up the Borgo Pass (today's Tihuța Pass) towards Bukovina and the Count",
         "特兰西瓦尼亚东北部的撒克逊老城。《德古拉》里，乔纳森·哈克 5 月 3 日来到“比斯特里茨”，在金冠旅馆住了最后一夜，第二天坐驿车上博尔戈山口（今蒂胡察山口），往布科维纳和伯爵那里去"),
    ORIG("ro-humulesti", "Ion Creangă House, Humulești", "胡穆列什蒂的克里昂格故居",
         "House in Humulești, now part of Târgu Neamț, built in 1830–31 by Creangă's grandfather Petre Ciubotariu; Ion Creangă was born here in 1837 and lived here until 1846, then on and off until 1855. It is a memorial museum, one of the most visited in Romania. Memories of My Boyhood begins with the village, 'across the Neamț water' from the market town",
         "胡穆列什蒂的一栋房子，胡穆列什蒂如今属于特尔古涅亚姆茨，房子是克里昂格的外祖父彼得雷·丘博塔留 1830–31 年建的；扬·克里昂格 1837 年生在这里，住到 1846 年，此后断断续续住到 1855 年。如今是纪念馆，在罗马尼亚是参观人数最多的纪念馆之一。《童年回忆》一开头写的就是这个村子，在镇子对面、“涅亚姆茨河那边”"),
    ORIG("ro-tomis", "Statue of Ovid, Constanța (Tomis)", "康斯坦察的奥维德像（托米斯）",
         "Bronze statue by Ettore Ferrari (1887) in Ovid Square in the old centre of Constanța, the ancient Tomis on the Black Sea, where Augustus banished Ovid in AD 8. He wrote the five books of Tristia here in AD 9–12. In Tristia III.9 he tells the legend behind the town's name: Medea, fleeing with the Argonauts, cut her brother Absyrtus to pieces here",
         "康斯坦察老城奥维德广场上的青铜像，埃托雷·费拉里 1887 年所作。康斯坦察就是黑海边的古城托米斯，公元 8 年奥古斯都把奥维德流放到这里，他在公元 9 至 12 年间在此写下五卷《哀歌集》。《哀歌集》第三卷第九首讲了城名的来历：美狄亚随阿尔戈英雄出逃，在这里把弟弟阿普绪耳托斯砍成碎块"),
    ORIG("ro-rebreanu", "Liviu Rebreanu (Prislop), near Năsăud", "利维乌·雷布雷亚努村（普里斯洛普），纳瑟乌德附近",
         "Village near Năsăud, formerly Prislop, renamed after the writer. Rebreanu spent decisive years here, and its people turn up in Ion (1920), counted as the first modern Romanian novel, where the village is Pripas; the house the villagers rebuilt in 1957 is a memorial museum",
         "纳瑟乌德附近的村子，原名普里斯洛普，后来以作家的名字命名。雷布雷亚努在这里度过了对他至关重要的几年，村里的人后来都写进了《伊昂》（1920），书中这个村子叫普里帕斯。这部小说被视为第一部现代罗马尼亚长篇小说；村民 1957 年重建的房子如今是纪念馆"),
    ORIG("ro-colt", "Colț Citadel, Hunedoara", "科尔茨城堡，胡内多阿拉",
         "Ruined fortress at the foot of the Retezat Mountains in the Hațeg country; it is thought to have inspired the castle of Verne's The Carpathian Castle (1892), which stands above the made-up village of Werst near the Vulkan pass",
         "哈采格地区雷泰扎特山脚下的城堡废墟；一般认为凡尔纳《喀尔巴阡古堡》（1892）里的城堡就是由它而来，小说里城堡俯临武尔坎山口附近虚构的韦尔斯特村"),
    PIL("ro-ipotesti", "Ipotești Memorial (Mihai Eminescu)", "伊波泰什蒂爱明内斯库纪念地",
        "Village near Botoșani where Mihai Eminescu (1850–1889) spent his childhood on his father's estate; the family house, rebuilt on the old foundations, the family church and his parents' graves make up the Ipotești Memorial and 'Mihai Eminescu' National Center for Studies. Whether he was born here or in Botoșani is disputed. His Luceafărul (1883) is one of the best-known poems in Romanian",
        "博托沙尼附近的村子，米哈伊·爱明内斯库（1850–1889）在父亲的庄园里度过童年；在旧地基上重建的故居、家族教堂和他父母的墓，组成了伊波泰什蒂纪念地暨“米哈伊·爱明内斯库”国家研究中心。他究竟生在这里还是博托沙尼，至今有争议。他的《金星》（1883）是罗马尼亚语最著名的诗篇之一",
        ["luceafarul"]),
    ORIG("ro-trajan", "Traian Square, Timișoara", "蒂米什瓦拉图拉真广场",
         "Square in Timișoara. The Land of Green Plums never names its university town, but its references to 'Trajanplatz' place it in Timișoara, where Herta Müller studied German and Romanian literature in 1973–1976",
         "蒂米什瓦拉的一个广场。《心兽》从不点出大学城的名字，但书里提到的“图拉真广场”把它定在蒂米什瓦拉；赫塔·米勒 1973 至 1976 年在这里读德语和罗马尼亚语文学"),
    ORIG("ro-colentina", "Colentina, Bucharest", "布加勒斯特科伦蒂纳区",
         "District in north-eastern Bucharest where Mircea Cărtărescu taught Romanian at School 86 in the 1980s, the school where the narrator of Solenoid (2015) teaches",
         "布加勒斯特东北部的城区，米尔恰·克尔特雷斯库 20 世纪 80 年代在这里的第 86 中学教罗马尼亚语，《螺线管》（2015）的叙述者就在这所学校教书"),
]

lines = [
    EN("ro-dr-1", "dracula", "ro-bistrita", "Chapter 1: Jonathan Harker's journal, 3 May", "第一章：乔纳森·哈克日记，5 月 3 日", T_DR,
       raw(T_DR, "It was on the dark side of twilight when we got to Bistritz,", "the ways of the country.", "en").replace("the  seventeenth", "the seventeenth"),
       ["Bistritz", "Golden Krone Hotel"],
       "我们到比斯特里茨时已是暮色将尽，这是个很有意思的古城。它几乎就在边境上——博尔戈山口从这里通往布科维纳——所以历来风波不断，也确实留下了痕迹。五十年前这里接连发生大火，先后五次造成可怕的破坏。十七世纪刚开始的时候，它被围困了三个星期，死了一万三千人，除了战争本身的伤亡，饥荒和疾病也推波助澜。\n德古拉伯爵让我去金冠旅馆，我高兴地发现它十分古色古香，因为我当然想尽量多看看这个国家的风土人情。",
       ["比斯特里茨", "金冠旅馆"], note=" (a doubled space written as one; Chinese is our own)"),
    Q("ro-am-1", "amintiri-din-copilarie", "ro-humulesti", "Part I, opening", "第一部开头", T_AM,
      raw(T_AM, "Stau câteodată și-mi aduc aminte", "Delenii și Bejenii.", "ro"), ["Humulești"],
      "I sometimes sit and remember what times and what people there were in our parts when I too, Lord bless me, was beginning to grow into a little boy at my parents' house, in the village of Humulești, just across the Neamț water from the market town; a big and merry village, divided into three parts that hold together as one: Vatra satului, Delenii and Bejenii.",
      ["Humulești"],
      "我有时坐着回想：当我也——仁慈的上帝啊——在父母家里开始长成一个小男孩的时候，我们那一带是什么样的年月、什么样的人。那时我住在胡穆列什蒂村，就在镇子对面、涅亚姆茨河那边；这是个又大又快活的村子，分成三部分，却连成一体：村中心、德莱尼和贝热尼。",
      ["胡穆列什蒂"], note=" (the first sentence)", site="Romanian"),
    Q("ro-tr-1", "tristia", "ro-tomis", "Book III, poem 9, lines 29–34", "第三卷第九首，第 29–34 行", T_TR,
      re.sub(r"\n[\xa0 ]+", "\n", raw(T_TR, "Neu pater ignoret, scopulo", "consecuisse sui.", "la")), ["Tomis"],
      "So that her father should not fail to see, she sets out on a high rock\nthe pale hands and the bloody head,\nthat the father might be slowed by this new grief and,\nwhile he gathers up the lifeless limbs, linger on his sad way.\nHence this place was called Tomis, because here, they say,\nthe sister cut her brother's body to pieces.",
      ["Tomis"],
      "为了让父亲看见，她把那苍白的双手和血淋淋的头颅\n摆在高高的岩石上，\n好让父亲为这新的悲痛停下脚步，\n在收拾那些死去的肢体时，耽误了悲伤的行程。\n这地方因此叫作托米斯，因为据说就在这里，\n姐姐把弟弟的身体砍成了碎块。",
      ["托米斯"], note=" (the indentation of the pentameters left out)", site="Latin"),
    Q("ro-io-1", "rebreanu-ion", "ro-rebreanu", "Chapter I, opening: the road to Pripas", "第一章开头：通往普里帕斯的路", T_IO,
      raw(T_IO, "Lăsând Jidovița, drumul urcă", "într-o scrântitură de coline.", "ro"), ["Pripasul"],
      "Leaving Jidovița, the road climbs at first with difficulty until it makes its way between the crowded hills, but then it runs on merrily and smoothly, now and then hiding among the young beeches of the Domnești Forest and resting a little at the Dead Man's Spring, where cool spring water drips for ever, then turns sharply under the Devil's Gullies to burst into Pripas, tucked away in a fold of the hills.",
      ["Pripas"],
      "离开吉多维察，路先是艰难地往上爬，直到在挤挤挨挨的山丘间挤出一条道来；随后却欢快、平坦地向前，时而藏进多姆内什蒂林的小山毛榉中间，在死人泉稍歇片刻——那里永远滴着清凉的泉水——然后在魔鬼崖下猛地一拐，一头撞进藏在山丘褶皱里的普里帕斯。",
      ["普里帕斯"], note=" (the second paragraph)", site="Romanian"),
    Q("ro-cc-1", "carpathian-castle", "ro-colt", "Chapter I: Frik the shepherd", "第一章：牧羊人弗里克", T_CC,
      raw(T_CC, "Le 29 mai de cette année-là", "et parfois de très près.", "fr"), ["Retyezat"],
      "On 29 May of that year a shepherd was watching his flock at the edge of a green plateau at the foot of the Retyezat, which overlooks a fertile valley, wooded with straight-stemmed trees and rich with fine crops. This high, open plateau, without shelter, is shaved in winter by the galernes, the north-west winds, as if with a barber's razor. In the country they say then that it is having a shave — and sometimes a very close one.",
      ["Retyezat"],
      "那年 5 月 29 日，一个牧羊人在雷泰扎特山脚下一片青翠高原的边上看着他的羊群；高原俯临一道肥沃的山谷，谷里树干笔直，庄稼长得很好。这片高原又高又空旷，无遮无挡，冬天西北风刮过，就像理发师的剃刀把它剃过一遍。当地人这时就说，高原在刮胡子——有时还刮得很干净。",
      ["雷泰扎特山"], note=" (one paragraph)", site="French"),
    S("ro-gp-1", "land-of-green-plums", "ro-trajan", "The novel as a whole", "全书",
      "The narrator, a young woman of Romania's German minority, shares a student dormitory room with Lola, who is found dead. With three friends drawn together by her death she lives under the eye of the Securitate in Ceaușescu's Romania, in a university town the book never names, though its Trajanplatz places it in Timișoara.",
      "叙述者是罗马尼亚德意志少数民族的一个年轻女子，和萝拉同住一间学生宿舍，后来萝拉被发现死了。她和因萝拉之死走到一起的三个朋友，在齐奥塞斯库统治下的罗马尼亚处处受秘密警察监视。书里从不说这座大学城叫什么，但提到的“图拉真广场”把它定在了蒂米什瓦拉。",
      ["Timișoara"], ["蒂米什瓦拉"], "https://en.wikipedia.org/wiki/The_Land_of_Green_Plums; https://www.cambridge.org/core/product/identifier/CBO9780511667558A019/type/BOOK_PART"),
    S("ro-so-1", "solenoid", "ro-colentina", "The novel as a whole", "全书",
      "The narrator, a failed poet born in Bucharest in 1956, teaches Romanian at a run-down school in the Colentina district in the 1980s and lives in a boat-shaped house on Maica Domnului street, built by the inventor of the solenoid hidden beneath it. The book is the manuscript he says he will never publish.",
      "叙述者是个失意的诗人，1956 年生于布加勒斯特，20 世纪 80 年代在科伦蒂纳区一所破旧的学校教罗马尼亚语，住在圣母街上一栋船形的房子里，房子是那台藏在地下的螺线管的发明者造的。全书就是他说永远不会发表的那部手稿。",
      ["Colentina"], ["科伦蒂纳区"], "https://en.wikipedia.org/wiki/Solenoid_(novel); https://ejlw.eu/article/download/37605/35205"),
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

HEAD = "// Romania, hand-written content (tools/content/batches/add_ro1.py, 2026-11-24).\n"
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
