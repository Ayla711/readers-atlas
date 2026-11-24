"""11-24: Algeria, first pack: 8 books, 8 places. Maupassant in the Casbah of Algiers, Gide's Biskra, Augustine's Thagaste
(Souk Ahras), Camus in Belcourt, Oran and Tipasa, Mohammed Dib's Tlemcen and Assia Djebar's Cherchell.

The map has the 48 provinces (wilayas) of before December 2019: the outlines (Natural Earth) do not yet show the ten
provinces since cut out of the southern ones. None of the eight places lies in a province that was divided.

Quotations (3 lines) are cut from French and Latin Wikisource pages (tools/content/wikisource.py); translations are our own
drafts. Books in copyright get scene notes with a fact source. What a cut changes is named in `checked`.

Coordinates are those of the place's English Wikipedia article (coords/add_dz1.json).

Usage: python3 -I add_dz1.py <app_dir> <coords.json> <wikisource_root>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-24"
b.init(APP, "", "dz", DATE)
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

T_AS = "Au soleil (recueil)/Alger"
T_IM = "L’Immoraliste/Première Partie/V"
T_CF = "Confessiones/Liber Quartus"
EXIST = set()

def once(title, s, lang):
    """the cut must start at the only place the words stand on the page"""
    n = ws.text(os.path.join(WSR, lang), title).count(s)
    assert n == 1, (title, s, n)
    return s

CAMUS = ("Albert Camus", "加缪", "Albert Camus")
books = [
    BK("au-soleil", "Au soleil", "在阳光下", "Au soleil", "Guy de Maupassant", "莫泊桑", "Guy de Maupassant", "1884", lang="fr",
       src=ws.url("fr", "Au soleil (recueil)"), aliases=["In the Sunlight", "African Wanderings", "Maupassant", "Alger"]),
    BK("the-immoralist", "The Immoralist", "背德者", "L’Immoraliste", "André Gide", "安德烈·纪德", "André Gide", "1902", lang="fr",
       src=ws.url("fr", "L’Immoraliste"), aliases=["L'Immoraliste", "Michel", "Marceline", "Gide", "纪德"]),
    BK("confessions-augustine", "Confessions", "忏悔录", "Confessiones", "Augustine of Hippo", "奥古斯丁", "Aurelius Augustinus", "c. 397–400", lang="la",
       src=ws.url("la", "Confessiones"), aliases=["Saint Augustine", "St Augustine", "Augustinus", "Thagaste", "圣奥古斯丁"]),
    BK("the-stranger", "The Stranger", "局外人", "L’Étranger", *CAMUS, "1942", lang="fr", pd=False,
       aliases=["The Outsider", "L'Étranger", "Meursault", "异乡人", "Camus"]),
    BK("the-plague", "The Plague", "鼠疫", "La Peste", *CAMUS, "1947", lang="fr", pd=False, aliases=["La Peste", "Rieux", "Camus"]),
    BK("nuptials", "Nuptials", "婚礼集", "Noces", *CAMUS, "1938", lang="fr", pd=False,
       aliases=["Noces", "Nuptials at Tipasa", "Noces à Tipasa", "蒂帕萨的婚礼", "Camus"]),
    BK("la-grande-maison", "La Grande Maison", "大房子", "La Grande Maison", "Mohammed Dib", "穆罕默德·狄布", "Mohammed Dib", "1952", lang="fr", pd=False,
       aliases=["The Great House", "The Big House", "Dar Sbitar", "Omar", "Dib"]),
    BK("fantasia-algerian-cavalcade", "Fantasia: An Algerian Cavalcade", "爱，幻想曲", "L’Amour, la fantasia", "Assia Djebar", "阿西娅·杰巴尔", "Assia Djebar", "1985",
       lang="fr", pd=False, aliases=["L'Amour, la fantasia", "Djebar"]),
]

places = [
    ORIG("dz-casbah", "Casbah of Algiers", "阿尔及尔卡斯巴",
         "The old walled town of Algiers, climbing the hill above the harbour. Maupassant spent two months in Algeria in 1881 and published Au soleil in 1884; the 'Arab town' he sees stacked above the French quarter is the Casbah",
         "阿尔及尔的老城，沿着港口上方的山坡层层向上。莫泊桑 1881 年在阿尔及利亚住了两个月，1884 年出版《在阳光下》；他看到的叠在法国人街区上方的“阿拉伯城”，就是卡斯巴"),
    ORIG("dz-biskra", "Biskra", "比斯克拉",
         "Oasis town on the northern edge of the Sahara, a winter resort in the late nineteenth century. Gide stayed here in the 1890s, and key parts of The Immoralist (1902) and of Les Nourritures terrestres (1897) are set here. In the novel Michel, close to death, is brought to Biskra by his wife Marceline and slowly recovers",
         "撒哈拉北缘的绿洲城镇，19 世纪末是冬季疗养地。纪德 19 世纪 90 年代在这里住过，《背德者》（1902）和《地粮》（1897）的重要段落都以这里为背景。小说里，奄奄一息的米歇尔被妻子玛塞琳带到比斯克拉，在这里慢慢康复"),
    ORIG("dz-thagaste", "Souk Ahras (Thagaste)", "苏格艾赫拉斯（塔加斯特）",
         "Souk Ahras stands on the site of Thagaste, the small Numidian town where Augustine was born in AD 354. In Book 4 of the Confessions he is back in his home town as a teacher when a close friend dies; grief makes the place unbearable, and he leaves for Carthage",
         "苏格艾赫拉斯建在塔加斯特的旧址上；奥古斯丁公元 354 年出生在这座努米底亚小城。《忏悔录》第四卷里，他回到家乡教书，一位挚友去世，悲痛让他无法再待下去，于是动身去了迦太基"),
    ORIG("dz-belcourt", "Belouizdad (Belcourt), Algiers", "贝鲁伊兹达德（贝尔库），阿尔及尔",
         "Working-class quarter of Algiers, called Belcourt under French rule, where Albert Camus grew up in poverty with his mother and her relatives. The Stranger names only Algiers; the pin stands in the quarter its author knew best",
         "阿尔及尔的工人街区，法国统治时期叫贝尔库；阿尔贝·加缪和母亲及母亲的亲戚在这里度过了贫困的童年。《局外人》里只说是阿尔及尔；图钉标在作者最熟悉的这个街区"),
    ORIG("dz-oran", "Oran", "奥兰",
         "Port city in western Algeria, the setting of The Plague. Camus drew on the cholera epidemic that killed a large part of Oran's population in 1849, but set the novel in the 1940s",
         "阿尔及利亚西部的港口城市，《鼠疫》的故事就发生在这里。加缪取材于 1849 年夺去奥兰大批居民性命的霍乱，却把小说放在 20 世纪 40 年代"),
    ORIG("dz-tipasa", "Tipasa", "蒂帕萨",
         "Town on the coast west of Algiers, with the ruins of a Roman city above the sea. 'Nuptials at Tipasa' is the best known of the essays in Camus's Nuptials",
         "阿尔及尔以西海岸上的小城，海边高处有一片罗马古城遗址。《蒂帕萨的婚礼》是加缪《婚礼集》里最有名的一篇"),
    ORIG("dz-tlemcen", "Tlemcen", "特莱姆森",
         "City in north-western Algeria, near the Moroccan border, where Mohammed Dib was born. La Grande Maison, his first novel, opens his Algerian trilogy",
         "阿尔及利亚西北部城市，靠近摩洛哥边境，穆罕默德·狄布出生在这里。《大房子》是他的第一部小说，也是他“阿尔及利亚三部曲”的第一部"),
    ORIG("dz-cherchell", "Cherchell", "舍尔沙勒",
         "Small port west of Algiers where Assia Djebar was born on 30 June 1936 and grew up",
         "阿尔及尔以西的小港，阿西娅·杰巴尔 1936 年 6 月 30 日出生在这里，并在这里长大"),
]

lines = [
    Q("dz-as-1", "au-soleil", "dz-casbah", "'Alger'", "“阿尔及尔”一章", T_AS,
      raw(T_AS, once(T_AS, "Féerie inespérée et qui ravit l’esprit", "fr"), "souterrains clairs.", "fr"), ["Alger"],
      "An unhoped-for enchantment, a delight to the mind! Algiers has surpassed my expectations. How pretty it is, the city of snow under the dazzling light! An immense terrace runs along the harbour, held up by elegant arcades. Above it rise big European hotels and the French quarter; higher still the Arab town climbs in tiers, a heap of small white houses, odd, tangled one into another, parted by streets that are like bright tunnels.",
      ["Algiers"],
      "意想不到的仙境，叫人心神俱醉！阿尔及尔超出了我的期待。这座雪一般的城市，在耀眼的阳光下多么漂亮！一道宽阔的平台沿着港口伸展，下面由优雅的拱廊托着。上面耸立着欧洲人的大旅馆和法国人的街区，再往上是层层叠起的阿拉伯城，一堆白色的小房子，奇形怪状，彼此交错纠缠，中间隔着一条条像明亮地道似的街巷。",
      ["阿尔及尔"], note=" (the opening of the chapter)", site="French"),
    Q("dz-im-1", "the-immoralist", "dz-biskra", "Part 1, chapter 5", "第一部第五章", T_IM,
      raw(T_IM, once(T_IM, "Notre séjour à Biskra ne devait pas", "fr"), "gronder au loin l’Oued débordé.", "fr"), ["Biskra"],
      "Our stay at Biskra was not to last much longer. Once the February rains were over, the heat broke out too fiercely. After several trying days spent under the downpour, one morning, all at once, I woke into blue sky. As soon as I was up I ran to the highest terrace. The sky was clear from one horizon to the other. Under the sun, already burning, mists were rising; the whole oasis was steaming; far off one could hear the roar of the Oued in flood.",
      ["Biskra"],
      "我们在比斯克拉不会再住多久了。二月的雨一过，炎热猛然袭来。在大雨里熬过难受的几天之后，一天早晨，我忽然在一片碧空中醒来。一起床我就跑上最高的那层平台。天空从这头到那头一片澄净。太阳已经很烈，水汽在阳光下升腾；整片绿洲都在冒着热气；远处传来干河涨水的轰鸣。",
      ["比斯克拉"], note=" (the opening of the chapter)", site="French"),
    Q("dz-au-1", "confessions-augustine", "dz-thagaste", "Book 4, 7.12", "第四卷 7.12", T_CF,
      raw(T_CF, once(T_CF, "quo enim cor meum fugeret a corde meo?", "la"), "veni Carthaginem.", "la"), ["Thagastensi oppido"],
      "For where could my heart flee from my heart? Where could I flee from myself? Where would I not follow myself? And yet I fled from my home town. For my eyes looked for him less where they were not used to seeing him, and from the town of Thagaste I came to Carthage.",
      ["town of Thagaste"],
      "我的心能逃到哪里去躲开我的心？我能逃到哪里去躲开我自己？哪里我不会跟着自己去？可我还是逃离了家乡。在不常见到他的地方，我的眼睛就不那么寻找他了；于是我从塔加斯特城来到了迦太基。",
      ["塔加斯特"], note=" (the end of section 4.7.12)", site="Latin"),
    S("dz-st-1", "the-stranger", "dz-belcourt", "The novel as a whole", "全书",
      "Meursault, a clerk in Algiers, learns that his mother has died in an old people's home in the country. The day after the funeral he is back in Algiers and takes up with Marie, who once worked in his office; some weeks later, on a beach outside the city, he kills an Arab man, and the second half of the book is his trial.",
      "默尔索是阿尔及尔的一个小职员，得知母亲在乡下的养老院去世。葬礼第二天他回到阿尔及尔，和从前在他公司做过事的玛丽好上了；几个星期后，在城外的海滩上，他杀了一个阿拉伯人，小说的后半部就是对他的审判。",
      ["Algiers"], ["阿尔及尔"], "https://en.wikipedia.org/wiki/The_Stranger_(Camus_novel)"),
    S("dz-pl-1", "the-plague", "dz-oran", "The novel as a whole", "全书",
      "Plague breaks out in Oran and the whole city is put under quarantine, its people cut off from everyone outside. The chronicle follows Dr Bernard Rieux and those around him as they go on doing their work through the months of the epidemic.",
      "奥兰爆发鼠疫，全城被封锁隔离，城里的人与外界断了联系。这部纪事跟着贝尔纳·里厄医生和他身边的人，写他们怎样在疫病流行的几个月里继续各尽其职。",
      ["Oran"], ["奥兰"], "https://en.wikipedia.org/wiki/The_Plague_(novel)"),
    S("dz-no-1", "nuptials", "dz-tipasa", "'Nuptials at Tipasa'", "《蒂帕萨的婚礼》",
      "The first essay of the book: a spring day at Tipasa, among the Roman ruins overgrown with flowers above the sea. Camus walks, swims and lies in the sun, and writes of the happiness of a body at one with sea, light and stone.",
      "全书的第一篇：春天在蒂帕萨的一天，在海边高处开满野花的罗马遗址之间。加缪散步、游泳、躺在阳光下，写下身体与大海、光线和石头融为一体的幸福。",
      ["Tipasa"], ["蒂帕萨"], "https://en.wikipedia.org/wiki/Nuptials_(essays)"),
    S("dz-gm-1", "la-grande-maison", "dz-tlemcen", "The novel as a whole", "全书",
      "Tlemcen in 1939. Omar, a boy of about ten who does not eat his fill every day, lives with his large and very poor family in a single room of Dar Sbitar, a house shared by many families who have the courtyard, the kitchen and the toilets in common.",
      "1939 年的特莱姆森。十来岁的男孩奥马尔不是每天都能吃饱，他和穷困的一大家人挤在“达尔斯比塔尔”的一间屋子里——这是一座住着许多户人家的大杂院，院子、厨房和厕所都是公用的。",
      ["Tlemcen"], ["特莱姆森"], "https://fr.wikipedia.org/wiki/La_Grande_Maison; https://en.wikipedia.org/wiki/Mohammed_Dib"),
    S("dz-af-1", "fantasia-algerian-cavalcade", "dz-cherchell", "The novel as a whole", "全书",
      "The novel moves between two stories: an Algerian girlhood that draws on Djebar's own, in Cherchell, and the French conquest of Algeria that began in 1830, retold from the invaders' own reports and letters.",
      "小说在两条线之间穿行：一条是取材于杰巴尔本人在舍尔沙勒的阿尔及利亚少女时代，另一条是 1830 年开始的法国对阿尔及利亚的征服，借入侵者自己的报告和书信重新讲述。",
      ["Cherchell"], ["舍尔沙勒"], "https://fr.wikipedia.org/wiki/L%27Amour,_la_fantasia; https://en.wikipedia.org/wiki/Assia_Djebar"),
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

HEAD = "// Algeria, hand-written content (tools/content/batches/add_dz1.py, 2026-11-24).\n"
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
