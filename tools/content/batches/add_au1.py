"""11-24: Australia, first pack: 8 books, 9 places. Marcus Clarke's Macquarie Harbour, Banjo Paterson's Snowy River and
Combo Waterhole ("Waltzing Matilda"), Miles Franklin's Brindabella, Hanging Rock, Ruth Park's Surry Hills and Kate
Grenville's Hawkesbury River, and Colleen McCullough's birthplace for The Thorn Birds, whose Drogheda is invented.

The map has the six states and two mainland territories; Jervis Bay Territory is drawn with the Australian Capital
Territory, Macquarie Island and Lord Howe Island are left off the map ("drop_rings_lon_gt": 155).

Quotations (3 lines) are cut from English Wikisource pages (tools/content/wikisource.py); Chinese is our own draft. Books
in copyright get scene notes with a fact source. What a cut changes is named in `checked`.

Coordinates are those of the place's English Wikipedia article (coords/add_au1.json).

Fix of 11-24 (the atlas's rule: a book worth having is hung on the nearest real place even when its exact spot cannot be
found): My Brilliant Career is quoted at Goulburn (the novel itself says 'Possum Gully is near Goulburn; no source says
its Bruggabrong is Brindabella, so Brindabella stays a pilgrimage place), and The Thorn Birds, whose Drogheda and
Gillanbone are invented, gets a scene note at Colleen McCullough's birthplace.

Usage: python3 -I add_au1.py <app_dir> <coords.json> <wikisource_root>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-24"
b.init(APP, "", "au", DATE)
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

T_NL = "For the Term of His Natural Life/Book II/Chapter I"
T_SR = "The Man from Snowy River and Other Verses/The Man from Snowy River"
T_WM = "Waltzing Matilda"
EXIST = set()

def once(title, s, lang="en"):
    """the cut must start at the only place the words stand on the page"""
    n = ws.text(os.path.join(WSR, lang), title).count(s)
    assert n == 1, (title, s, n)
    return s

def unindent(s):
    """a poem whose every second line the page indents with an em space"""
    return "\n".join(l.lstrip(" ") for l in s.split("\n"))

books = [
    BK("natural-life", "For the Term of His Natural Life", "无期徒刑", "For the Term of His Natural Life", "Marcus Clarke", "马库斯·克拉克", "Marcus Clarke",
       "1874", lang="en", src=ws.url("en", "For the Term of His Natural Life"), aliases=["His Natural Life", "Rufus Dawes", "Van Diemen's Land", "Clarke"]),
    BK("man-from-snowy-river", "The Man from Snowy River", "来自雪河的人", "The Man from Snowy River", "Banjo Paterson", "班卓·佩特森", "A. B. Paterson", "1890",
       lang="en", src=ws.url("en", T_SR), aliases=["Snowy River", "Clancy", "Kosciusko", "Paterson", "A. B. Paterson"]),
    BK("waltzing-matilda", "Waltzing Matilda", "丛林流浪", "Waltzing Matilda", "Banjo Paterson", "班卓·佩特森", "A. B. Paterson", "1895",
       lang="en", src=ws.url("en", T_WM), aliases=["swagman", "billabong", "jumbuck", "Combo Waterhole", "Paterson", "A. B. Paterson"]),
    BK("my-brilliant-career", "My Brilliant Career", "我的光辉生涯", "My Brilliant Career", "Miles Franklin", "迈尔斯·富兰克林", "Miles Franklin", "1901",
       lang="en", src=ws.url("en", "My Brilliant Career"), aliases=["Sybylla Melvyn", "Possum Gully", "Bruggabrong", "Caddagat", "Franklin"]),
    BK("picnic-at-hanging-rock", "Picnic at Hanging Rock", "悬崖下的野餐", "Picnic at Hanging Rock", "Joan Lindsay", "琼·林赛", "Joan Lindsay", "1967",
       lang="en", pd=False, aliases=["Appleyard College", "Miranda", "Hanging Rock", "Lindsay"]),
    BK("harp-in-the-south", "The Harp in the South", "南方的竖琴", "The Harp in the South", "Ruth Park", "露丝·帕克", "Ruth Park", "1948",
       lang="en", pd=False, aliases=["Darcy family", "Plymouth Street", "Surry Hills", "Park"]),
    BK("the-secret-river", "The Secret River", "神秘的河流", "The Secret River", "Kate Grenville", "凯特·格伦维尔", "Kate Grenville", "2005",
       lang="en", pd=False, aliases=["William Thornhill", "Hawkesbury", "Grenville"]),
    BK("the-thorn-birds", "The Thorn Birds", "荆棘鸟", "The Thorn Birds", "Colleen McCullough", "考琳·麦卡洛", "Colleen McCullough", "1977",
       lang="en", pd=False, aliases=["Drogheda", "Gillanbone", "Meggie Cleary", "Ralph de Bricassart", "McCullough", "麦卡洛"]),
]

places = [
    ORIG("au-sarah-island", "Sarah Island, Macquarie Harbour", "萨拉岛，麦夸里港",
         "Small island in Macquarie Harbour on the wild west coast of Tasmania, the site of a penal station from 1822 to 1833; the narrow mouth of the harbour is called Hells Gates. In For the Term of His Natural Life the convict Rufus Dawes is sent here; Book II opens with this description of the coast",
         "塔斯马尼亚荒凉西岸麦夸里港里的小岛，1822 年至 1833 年是流放犯监狱的所在地；港口狭窄的入口叫“地狱门”。《无期徒刑》里，囚犯鲁弗斯·道斯被押到这里；第二部就以这一段海岸描写开头"),
    ORIG("au-kosciuszko", "Mount Kosciuszko and the upper Snowy River", "科修斯科山与雪河上游",
         "Australia's highest mountain, in the Snowy Mountains of New South Wales; the Snowy River rises on its slopes. Paterson's poem, first printed in The Bulletin on 26 April 1890, tells of a mountain horse-chase; its hero 'hails from Snowy River, up by Kosciusko's side'. Corryong, on the Victorian side of the range, claims the stockman Jack Riley as the model for him",
         "澳大利亚最高峰，在新南威尔士州的雪山山脉；雪河就发源于它的山坡。佩特森这首诗 1890 年 4 月 26 日首刊于《公报》，写的是一场山间追马；主人公“来自雪河，就在科修斯科山边”。山脉另一侧维多利亚州的科里昂镇认为，牧人杰克·赖利就是他的原型"),
    ORIG("au-combo", "Combo Waterhole, Queensland", "孔博水塘，昆士兰州",
         "Waterhole on the Diamantina River near Kynuna in western Queensland. 'Waltzing Matilda', written by Paterson in 1895 to a tune played by Christina Macpherson, is probably based on a real incident here in the 1890s; the 'billabong' of the song is a waterhole such as this",
         "昆士兰西部基努纳附近迪亚曼蒂纳河上的水塘。《丛林流浪》是佩特森 1895 年按克里斯蒂娜·麦克弗森弹奏的曲调填的词，很可能取材于 19 世纪 90 年代这里发生的一件真事；歌里的“比拉邦”，就是这样一个水塘"),
    PIL("au-brindabella", "Brindabella Station", "布林达贝拉牧场",
        "Station in the Brindabella Valley, in the ranges west of Canberra, first taken up by the Franklin family in 1846. Miles Franklin, born at Talbingo in 1879, spent her first ten years here before the family moved to a small farm near Goulburn; My Brilliant Career (1901), written when she was about nineteen, draws on her own family",
        "布林达贝拉谷地里的牧场，在堪培拉以西的山间，富兰克林家族 1846 年最早在这里落脚。迈尔斯·富兰克林 1879 年生于塔尔宾戈，在这里度过了最初的十年，随后全家搬到古尔本附近的一个小农场；《我的光辉生涯》（1901）是她十九岁左右写的，取材于她自己的家庭",
        ["my-brilliant-career"]),
    PIL("au-wellington", "Wellington, New South Wales", "惠灵顿，新南威尔士州",
        "Country town at the junction of the Macquarie and Bell rivers, where Colleen McCullough was born on 1 June 1937. The Thorn Birds (1977) is set mostly on Drogheda, a sheep station in New South Wales, and in the nearby town of Gillanbone; both are invented, and no source we checked names a real station or town behind them. Drogheda takes its name from the town in Ireland",
        "麦夸里河与贝尔河交汇处的乡间小镇，考琳·麦卡洛 1937 年 6 月 1 日出生在这里。《荆棘鸟》（1977）的故事大半发生在新南威尔士的德罗海达牧场和附近的基兰博镇；两处都是虚构的，我们查到的资料里没有指出它们以哪座真实的牧场或小镇为原型。德罗海达的名字取自爱尔兰的同名城镇",
        ["the-thorn-birds"]),
    ORIG("au-hanging-rock", "Hanging Rock, Victoria", "悬岩，维多利亚州",
         "An old volcanic outcrop about 70 km north-west of Melbourne, a few kilometres north of Mount Macedon; it became widely known as the setting of Joan Lindsay's novel",
         "墨尔本西北约 70 公里处的一座古火山岩丘，在马斯顿山以北几公里；因琼·林赛的小说而广为人知"),
    ORIG("au-surry-hills", "Surry Hills, Sydney", "萨里山，悉尼",
         "Inner suburb of Sydney, in the 1940s a slum. Ruth Park's The Harp in the South won a newspaper's novel competition and was published in 1948; it follows an Irish Catholic family living here",
         "悉尼的内城区，20 世纪 40 年代是贫民窟。露丝·帕克的《南方的竖琴》赢得一家报纸的小说征文奖，1948 年出版，写的是住在这里的一户爱尔兰裔天主教家庭"),
    ORIG("au-wisemans-ferry", "Wisemans Ferry, Hawkesbury River", "怀斯曼渡口，霍克斯伯里河",
         "Village on the Hawkesbury River north-west of Sydney, named after Solomon Wiseman, a transported convict who settled here in the early nineteenth century. Kate Grenville set out to write about this ancestor of hers; the book became a novel about an invented convict, William Thornhill, who takes up land on the river",
         "悉尼西北霍克斯伯里河边的村子，以 19 世纪初在这里定居的流放犯所罗门·怀斯曼命名。凯特·格伦维尔本想写这位祖先，最后写成了一部小说，主人公是虚构的流放犯威廉·桑希尔，他在这条河边占了一块地"),
]

lines = [
    EN("au-nl-1", "natural-life", "au-sarah-island", "Book II, chapter 1, 'The Topography of Van Diemen's Land'", "第二部第一章“范迪门地的地形”", T_NL,
       re.sub(r" {2,}", " ", raw(T_NL, once(T_NL, "Navigation is dangerous, and the entrance", "en"), "stamped a perpetual frown.", "en")),
       ["Macquarie Harbour"],
       "航行十分危险；麦夸里港的入口“地狱门”——在我们所写的那个时候（1833 年），正是这处流放犯定居点恶名最盛的年月——只有风平浪静时才能试着进去。海岸线上满是沉船。暗礁都以被它们撞毁的船只命名，名字听来阴森。空气阴冷潮湿，土壤只长多刺的灌丛和毒草，沼泽里散出的恶臭紧贴着湿软的地面。四下一片荒凉；大自然的脸上永远刻着一道愁眉。",
       ["麦夸里港"], note=" (doubled spaces between sentences written as one; Chinese is our own)"),
    EN("au-sr-1", "man-from-snowy-river", "au-kosciuszko", "Clancy speaks for the stripling", "克兰西为年轻人说话", T_SR,
       unindent(raw(T_SR, once(T_SR, "So he waited sad and wistful", "en"), "such horsemen have I seen.'", "en")),
       ["Snowy River", "Kosciusko"],
       "他只好等着，又难过又不甘——只有克兰西站在他这边——\n“我想咱们该让他一起来，”他说，\n“我担保到了紧要关头他准顶得上，\n因为他和他的马都是山里长大的。\n“他来自雪河，就在科修斯科山边，\n那里的山陡上一倍，也险上一倍，\n马蹄每一步都在燧石上踏出火星，\n能在那里站得住脚的人就够格了。\n“雪河的骑手们以山为家，\n河水就在那些巨大的山岭间奔流；\n自从我开始四处闯荡，见过的骑手不计其数，\n可还从没见过这样的骑手。”",
       ["雪河", "科修斯科"], note=" (the em-space indent of every second line left out; Chinese is our own)"),
    EN("au-wm-1", "waltzing-matilda", "au-combo", "Verses 1 and 4", "第一段与第四段", T_WM,
       raw(T_WM, once(T_WM, "Oh there once was a swagman camped in the billabong,"), "Who’ll come a’waltzing Matilda with me\nWho’ll") [:-len("\nWho’ll")] + "\n…\n"
       + raw(T_WM, once(T_WM, "But the swagman he up & he jumped in the water-hole"), "as it sings by the billabong\nWho’ll come a’waltzing Matilda with me."),
       ["billabong"],
       "从前有个流浪汉在比拉邦边扎营，\n就在一棵库利巴树的树荫下，\n他望着那把老铁壶咕嘟作响，唱道：\n谁愿跟我一起去流浪，带着马蒂尔达？\n…\n可那流浪汉一下跳进了水塘，\n在那棵库利巴树旁淹死了，\n人们还能听见他的鬼魂在比拉邦边唱：\n谁愿跟我一起去流浪，带着马蒂尔达？",
       ["比拉邦"], note=" (the transcription of the original manuscript, spelling as written; the chorus lines left out; Chinese is our own)"),
    S("au-ph-1", "picnic-at-hanging-rock", "au-hanging-rock", "The novel as a whole", "全书",
      "On St Valentine's Day 1900 the girls of Appleyard College, a boarding school near Mount Macedon, are taken for a day's picnic at Hanging Rock. Several of them climb the rock and vanish, with one of their teachers; the book follows what the disappearances do to the school and the district.",
      "1900 年情人节，马斯顿山附近的寄宿学校阿普尔亚德学院带女学生们去悬岩野餐一天。几个女孩爬上岩山后不见了踪影，一位老师也随之失踪；小说接着写这些失踪给学校和当地带来的后果。",
      ["Hanging Rock"], ["悬岩"], "https://en.wikipedia.org/wiki/Picnic_at_Hanging_Rock_(novel); https://en.wikipedia.org/wiki/Hanging_Rock,_Victoria"),
    S("au-hs-1", "harp-in-the-south", "au-surry-hills", "The novel as a whole", "全书",
      "The Darcys, Hughie and Margaret and their daughters, live in a run-down terrace house in Surry Hills, then a slum of the inner city, among the poverty, the drink and the sly-grog shops of the neighbourhood.",
      "达西一家——休伊、玛格丽特和她们的女儿们——住在萨里山一栋破旧的联排房里。那时这里是内城的贫民窟，街坊间满是贫困、酗酒和私酒铺。",
      ["Surry Hills"], ["萨里山"], "https://en.wikipedia.org/wiki/The_Harp_in_the_South"),
    S("au-sr2-1", "the-secret-river", "au-wisemans-ferry", "The novel as a whole", "全书",
      "William Thornhill, a London waterman sentenced to death for stealing wood, has his sentence commuted to transportation to New South Wales in 1806. Once free, he takes up a hundred acres on the Hawkesbury River, land the Dharug people already live on, and the novel follows the conflict that ends in a massacre.",
      "伦敦船夫威廉·桑希尔因偷木头被判死刑，1806 年改判流放新南威尔士。获释后，他在霍克斯伯里河边占了一百英亩地，而达鲁格人早已生活在这片土地上；小说一路写到这场冲突以一场屠杀告终。",
      ["Hawkesbury River"], ["霍克斯伯里河"], "https://en.wikipedia.org/wiki/The_Secret_River"),
]

# ---- 11-24 fix: famous books hung even without an exact spot (user rule) ----
T_B2, T_B3 = "My Brilliant Career/Chapter 2", "My Brilliant Career/Chapter 3"
places += [
    ORIG("au-goulburn", "Goulburn", "古尔本",
         "City on the Southern Tablelands of New South Wales. When Miles Franklin was about ten her family left Brindabella for a small farm near Goulburn, and that district is the setting of My Brilliant Career, where the farm is called Possum Gully. The farm is not identified more closely; the pin is the city's point",
         "新南威尔士州南部高原上的城市。迈尔斯·富兰克林十岁左右时，全家离开布林达贝拉，搬到古尔本附近的一个小农场；《我的光辉生涯》就以这一带为背景，书中那个农场叫“负鼠谷”。农场的具体位置无从确认，图钉标在城区"),
]
lines += [
    EN("au-bc-1", "my-brilliant-career", "au-goulburn", "Chapters 2 and 3", "第二、三章", T_B3,
       raw(T_B2, once(T_B2, "He gave up Bruggabrong, Bin Bin East, and Bin Bin West,"), "to live near Goulburn.", "en") + "\n…\n"
       + raw(T_B3, once(T_B3, "’Possum Gully was stagnant"), "when they passed childhood.", "en"),
       ["’Possum Gully", "Goulburn"],
       "他放弃了布鲁加布朗、东宾宾和西宾宾，买下了“负鼠谷”——一个一千英亩的小农场，带着我们全家搬到古尔本附近住。\n…\n“负鼠谷”死气沉沉——老乡村地方普遍都有的那种狭隘的死气沉沉。\n这里住的大多是有家室的人和十六岁以下的孩子。男孩子一长大成人，就漂到内陆去剪羊毛、赶牲口，或者去占块地。他们嫌家里太慢；何况过了童年，家里也没有他们的位置了。",
       ["负鼠谷", "古尔本"], note=" (two passages, the end of chapter 2's account of the move and the opening of chapter 3; Chinese is our own)"),
    S("au-tb-1", "the-thorn-birds", "au-wellington", "The novel as a whole", "全书",
      "The story begins in New Zealand on 8 December 1915, Meggie Cleary's fourth birthday. The family moves to Drogheda, the huge sheep station in New South Wales owned by her father's widowed sister Mary Carson, where Meggie meets Ralph de Bricassart, a young priest sent to the remote parish of Gillanbone near by; the novel follows the Clearys to 1969. Drogheda and Gillanbone are invented, so the line hangs at the author's birthplace.",
      "故事从 1915 年 12 月 8 日的新西兰开始，那天是梅吉·克利里四岁的生日。全家后来搬到德罗海达——她父亲守寡的姐姐玛丽·卡森在新南威尔士的大牧场；在那里，梅吉遇见了被贬到附近偏远的基兰博教区的年轻神父拉尔夫·德·布里克萨特。小说一直写到 1969 年。德罗海达和基兰博都是虚构的，所以这一条挂在作者的出生地。",
      ["Drogheda"], ["德罗海达"], "https://en.wikipedia.org/wiki/The_Thorn_Birds"),
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

HEAD = "// Australia, hand-written content (tools/content/batches/add_au1.py, 2026-11-24).\n"
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
