"""11-23: Finland, first pack: 7 new books, 7 places. Kivi's Nurmijarvi, Runeberg's Jutas, Lonnrot's Paikkari croft, the
Moomin Museum in Tampere, Paasilinna's Kittila, Leino's Paltaniemi and Minna Canth's Kuopio.

Quotations (2 lines) are cut from Finnish and Swedish Wikisource pages (tools/content/wikisource.py); translations are our
own drafts (translation: "own"). Books in copyright hang on a writer's place. What a cut changes is named in `checked`.

Coordinates are those of the place's English Wikipedia article (cache/fi/coords.json).

Usage: python3 -I add_fi1.py <app_dir> <coords.json> <wikisource_root>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-23"
b.init(APP, "", "fi", DATE)
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

T_SV, T_DJ = "Seitsemän veljestä: Ensimmäinen luku", "Döbeln vid Jutas"
EXIST = set()

books = [
    BK("seven-brothers", "Seven Brothers", "七兄弟", "Seitsemän veljestä", "Aleksis Kivi", "阿莱克西斯·基维", "Aleksis Kivi", "1870", lang="fi",
       src=ws.url("fi", "Seitsemän veljestä"), aliases=["Seitsemän veljestä", "Jukola", "Impivaara", "Toukola", "Juhani"]),
    BK("fanrik-stals-sagner", "The Tales of Ensign Stål", "旗手斯托尔的故事", "Fänrik Ståls sägner", "Johan Ludvig Runeberg", "鲁内贝里",
       "Johan Ludvig Runeberg", "1848–1860", lang="sv", src=ws.url("sv", "Fänrik Ståls sägner"),
       aliases=["Fänrik Ståls sägner", "Vänrikki Stoolin tarinat", "Döbeln vid Jutas", "Vårt land", "Runeberg"]),
    BK("kalevala", "Kalevala", "卡勒瓦拉", "Kalevala", "Elias Lönnrot", "埃利亚斯·伦罗特", "Elias Lönnrot", "1835 / 1849", lang="fi",
       src=ws.url("fi", "Kalevala"), aliases=["Väinämöinen", "Sampo", "Lönnrot", "卡莱瓦拉"]),
    BK("finn-family-moomintroll", "Finn Family Moomintroll", "魔法师的帽子", "Trollkarlens hatt", "Tove Jansson", "托芙·扬松", "Tove Jansson", "1948",
       lang="sv", pd=False, aliases=["Trollkarlens hatt", "Moomin", "Muumi", "Moominvalley", "姆明"]),
    BK("year-of-the-hare", "The Year of the Hare", "兔年", "Jäniksen vuosi", "Arto Paasilinna", "阿尔托·帕西林纳", "Arto Paasilinna", "1975",
       lang="fi", pd=False, aliases=["Jäniksen vuosi", "Vatanen", "Le Lièvre de Vatanen", "Lapland"]),
    BK("helkavirsia", "Whitsongs", "圣灵节之歌", "Helkavirsiä", "Eino Leino", "埃伊诺·莱诺", "Eino Leino", "1903", lang="fi",
       aliases=["Helkavirsiä", "Leino", "Paltaniemi"]),
    BK("tyomiehen-vaimo", "The Worker's Wife", "工人的妻子", "Työmiehen vaimo", "Minna Canth", "明娜·康特", "Minna Canth", "1885", lang="fi",
       aliases=["Työmiehen vaimo", "Johanna", "Risto", "Canth"]),
]

places = [
    ORIG("fi-palojoki", "Palojoki, Nurmijärvi (Aleksis Kivi's birth home)", "帕洛约基，努尔米耶尔维（基维故居）",
         "Village in Nurmijärvi, about 30 km north of Helsinki, where Aleksis Kivi was born in 1834; his birth home is a museum, set in the landscapes of Seven Brothers. The novel itself puts the Jukola farm in southern Häme, near the made-up village of Toukola. The seven heads in Nurmijärvi's coat of arms refer to the book",
         "努尔米耶尔维的一个村子，在赫尔辛基以北约 30 公里，阿莱克西斯·基维 1834 年生于此地；他的故居如今是博物馆，四周就是《七兄弟》的风景。小说本身把朱科拉农庄放在南海梅，靠近虚构的托科拉村。努尔米耶尔维市徽上的七个人头指的就是这本书"),
    ORIG("fi-jutas", "Jutas battlefield, Nykarleby", "尤塔斯战场，新卡勒比",
         "Site of the battle of 13 September 1808, south of Nykarleby, where Georg Carl von Döbeln's force beat the Russians; the main Swedish army was defeated at Oravais the next day. Runeberg's 'Döbeln at Jutas' in The Tales of Ensign Stål has the fevered Döbeln rise from his sickbed in Nykarleby to lead the fight",
         "1808 年 9 月 13 日战役的旧址，在新卡勒比以南，格奥尔格·卡尔·冯·多贝伦的部队在这里打败了俄军；第二天，瑞典主力在奥拉瓦伊斯战败。鲁内贝里《旗手斯托尔的故事》里的《多贝伦在尤塔斯》写发着高烧的多贝伦在新卡勒比从病床上起身，带兵上阵"),
    PIL("fi-paikkari", "Paikkari Croft, Sammatti", "派卡里小农舍，萨马蒂",
        "The croft where Elias Lönnrot was born in 1802 and spent his childhood, a house museum since 1887. Lönnrot's Old Kalevala of 1835 had 32 poems gathered on his collecting journeys; the New Kalevala of 1849, the one usually read, has 50",
        "埃利亚斯·伦罗特 1802 年出生并度过童年的小农舍，1887 年起成为故居博物馆。伦罗特 1835 年的《古卡勒瓦拉》收了他在采风旅行中搜集的 32 篇诗歌；1849 年的《新卡勒瓦拉》也就是通常读的版本，共 50 篇",
        ["kalevala"]),
    PIL("fi-moomin", "Moomin Museum, Tampere", "姆明博物馆，坦佩雷",
        "The world's only Moomin Museum, in Tampere Hall since 2017, shows the original Moomin illustrations that Tove Jansson and Tuulikki Pietilä gave to Tampere Art Museum in 1986, with tableaux and a Moomin House over two metres tall. Tove Jansson's first Moomin story came out in 1945",
        "世界上唯一的姆明博物馆，2017 年起设在坦佩雷会堂，展出托芙·扬松和图丽琪·皮耶蒂莱 1986 年捐给坦佩雷美术馆的姆明原画，还有立体场景和一座两米多高的姆明之家。托芙·扬松的第一个姆明故事出版于 1945 年",
        ["finn-family-moomintroll"]),
    PIL("fi-kittila", "Kittilä, Lapland", "基蒂莱，拉普兰",
        "Lapland municipality where Arto Paasilinna was born, in the village of Alakylä, in 1942. In his The Year of the Hare (1975), Vatanen leaves his life in Helsinki after his car hits a hare, and wanders with it across the Finnish countryside and up into Lapland",
        "拉普兰的一个市镇，阿尔托·帕西林纳 1942 年生于这里的阿拉基莱村。他的《兔年》（1975）里，瓦塔宁的车撞伤了一只野兔，他从此抛下在赫尔辛基的生活，带着兔子在芬兰乡间一路游荡，最后进了拉普兰",
        ["year-of-the-hare"]),
    PIL("fi-paltaniemi", "Paltaniemi, Kajaani", "帕尔塔涅米，卡亚尼",
        "Village where Eino Leino was born in 1878; his family lived in the Hövelö house, where Elias Lönnrot had lived and worked in 1834, the months when the Kalevala began to take shape. Leino's Whitsongs (Helkavirsiä, 1903) draws deeply on Finnish myth and folklore",
        "埃伊诺·莱诺 1878 年生于这个村子；他家住在霍维勒屋——1834 年埃利亚斯·伦罗特曾在这里居住、工作，正是《卡勒瓦拉》开始成形的那几个月。莱诺的《圣灵节之歌》（1903）大量取材于芬兰神话和民间传说",
        ["helkavirsia", "kalevala"]),
    PIL("fi-kuopio", "Kuopio (Minna Canth's Kanttila)", "库奥皮奥（明娜·康特的康蒂拉）",
        "Town where Minna Canth, widowed in 1879 with seven children, ran the family shop from her home, Kanttila, and wrote the plays that made her one of the leading writers of Finnish realism; her statue here was unveiled on 12 May 1937, forty years after her death. Her The Worker's Wife (1885), in which Johanna's drunken husband Risto squanders all her money, set off a debate in the press without precedent",
        "明娜·康特 1879 年丧夫，独自带着七个孩子，在自家的康蒂拉一边经营家里的商店，一边写剧本，成了芬兰现实主义文学最重要的作家之一；1937 年 5 月 12 日，她去世四十周年那天，这里为她立了雕像。她的《工人的妻子》（1885）写约翰娜的酒鬼丈夫里斯托把她的钱全都挥霍掉，在报刊上引起了前所未有的论战",
        ["tyomiehen-vaimo"]),
]

lines = [
    Q("fi-sv-1", "seven-brothers", "fi-palojoki", "Chapter 1, opening", "第一章开头", T_SV,
      raw(T_SV, "Jukolan talo, eteläisessä Hämeessä,", "aaltoili teräinen vilja.", "fi"), ["Jukolan talo", "eteläisessä Hämeessä", "Toukolan kylää"],
      "The house of Jukola, in southern Häme, stands on the northern slope of a hill, near the village of Toukola. Its nearest surroundings are a stony heath, but lower down the fields begin, where, before the house went to ruin, the grain once waved in the ear.",
      ["house of Jukola", "southern Häme", "village of Toukola"],
      "朱科拉农庄在南海梅，坐落在一座小山的北坡上，靠近托科拉村。农庄近旁是一片石头遍地的荒地，往下才是田地；在农庄败落以前，那里曾经麦穗起伏。",
      ["朱科拉农庄", "南海梅", "托科拉村"], note=" (the first two sentences)", site="Finnish"),
    Q("fi-dj-1", "fanrik-stals-sagner", "fi-jutas", "'Döbeln at Jutas', second stanza", "《多贝伦在尤塔斯》第二节", T_DJ,
      raw(T_DJ, "Men på sin bädd låg Döbeln,", "kommen till Ny-Karleby.", "sv"), ["Ny-Karleby"],
      "But on his bed lay Döbeln, worn by torment,\nhis breast was seen to struggle, his eye burned in flames,\nand fever's fires coloured his skin.\nHis troops had lately hurried north by forced marches,\nfor two days and nights, the last, had not rested;\nhe himself had come to Ny-Karleby.",
      ["Ny-Karleby"],
      "可是多贝伦躺在床上，受着病痛煎熬，\n胸膛起伏挣扎，眼里燃着火焰，\n高烧的火焰染红了他的脸。\n他的部队刚刚急行军向北赶路，\n最后这两天两夜都没有歇息；\n他自己也来到了新卡勒比。",
      ["新卡勒比"], site="Swedish"),
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

HEAD = "// Finland, hand-written content (tools/content/batches/add_fi1.py, 2026-11-23).\n"
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
