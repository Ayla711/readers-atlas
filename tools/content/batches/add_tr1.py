"""11-23: Turkey, first pack: 8 new books, 8 places. Troy, Abydos on the Hellespont, Trabzon (Trapezus), Pamuk's Museum of
Innocence and Kars, Yasar Kemal's Gokcedam, Sirkeci station and the Mevlana Museum in Konya.

Quotations (3 lines): Byron from English Wikisource; Homer and Xenophon in Greek from Greek Wikisource, with the English of
Samuel Butler (1898) and H. G. Dakyns (1890) from English Wikisource; the Chinese is our own. Books in copyright get scene
notes (no quotation) with a fact source. What a cut changes is named in `checked`.

Coordinates are those of the place's English Wikipedia article (cache/tr/coords.json).

Usage: python3 -I add_tr1.py <app_dir> <coords.json> <wikisource_root>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-23"
b.init(APP, "", "tr", DATE)
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

T_IL = "The Iliad (Butler)/Book VI"
T_BY = "The Works of Lord Byron (ed. Coleridge, Prothero)/Poetry/Volume 3/Written after swimming from Sestos to Abydos"
T_AN = "Anabasis (Dakyns)/Book 4/Chapter 8"
EXIST = set()

def GK(id, book, place, loc, loc_zh, title, orig, hl_orig, en_title, en, hl_en, zh, hl_zh, translator, note=""):
    """Greek original from Greek Wikisource; English from a public-domain translation on English Wikisource; Chinese our own"""
    assert "[" not in orig and "\xa0" not in orig and "  " not in orig, (id, orig[:40])
    assert "[" not in en and "\xa0" not in en and "  " not in en, (id, en[:40])
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls:
            assert h in text, (id, h)
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh,
                text_orig=orig, highlight_orig=hl_orig, text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh,
                translation=translator, status="draft",
                checked=f"Greek Wikisource, {title}{note}; English Wikisource, {en_title} (the hard line breaks joined); Chinese our own, {DATE}")

T_ILG, T_ANG = "Ιλιάς/Ζ", "Κύρου Ἀνάβασις Δ"

def stanzas(s):
    """a poem cut from Wikisource: the stanza numbers dropped, a blank line between stanzas"""
    out = re.split(r"\n?\d+\.\n", "\n" + s)
    return "\n\n".join(x.strip("\n") for x in out if x.strip())

books = [
    BK("iliad", "The Iliad", "伊利亚特", "Ἰλιάς", "Homer", "荷马", "Ὅμηρος", "c. 8th c. BC", lang="grc",
       src=ws.url("en", "The Iliad (Butler)"), aliases=["Ilias", "Troy", "Ilium", "Hector", "Andromache", "Achilles", "特洛伊", "赫克托耳"]),
    BK("sestos-to-abydos", "Written After Swimming from Sestos to Abydos", "从塞斯托斯游到阿拜多斯之后作", "Written After Swimming from Sestos to Abydos",
       "Lord Byron", "拜伦", "Lord Byron", "1810", lang="en", src=ws.url("en", T_BY),
       aliases=["Hellespont", "Dardanelles", "Leander", "Hero and Leander", "Byron"]),
    BK("anabasis", "Anabasis", "长征记", "Κύρου Ἀνάβασις", "Xenophon", "色诺芬", "Ξενοφῶν", "4th c. BC", lang="grc",
       src=ws.url("en", "Anabasis (Dakyns)"), aliases=["The March of the Ten Thousand", "The Persian Expedition", "Thalatta", "Ten Thousand", "Trapezus", "万人远征"]),
    BK("museum-of-innocence", "The Museum of Innocence", "纯真博物馆", "Masumiyet Müzesi", "Orhan Pamuk", "奥尔罕·帕慕克", "Orhan Pamuk", "2008",
       lang="tr", pd=False, aliases=["Masumiyet Müzesi", "Kemal", "Füsun", "Çukurcuma", "Pamuk"]),
    BK("pamuk-snow", "Snow", "雪", "Kar", "Orhan Pamuk", "奥尔罕·帕慕克", "Orhan Pamuk", "2002", lang="tr", pd=False,
       aliases=["Kar", "Ka", "Kars", "İpek", "Pamuk"]),
    BK("memed-my-hawk", "Memed, My Hawk", "瘦子麦麦德", "İnce Memed", "Yaşar Kemal", "亚沙尔·凯马尔", "Yaşar Kemal", "1955", lang="tr", pd=False,
       aliases=["İnce Memed", "Slim Memed", "Abdi Ağa", "Çukurova", "Taurus"]),
    BK("murder-on-the-orient-express", "Murder on the Orient Express", "东方快车谋杀案", "Murder on the Orient Express", "Agatha Christie",
       "阿加莎·克里斯蒂", "Agatha Christie", "1934", lang="en", pd=False,
       aliases=["Murder in the Calais Coach", "Orient Express", "Poirot", "Tokatlian", "Stamboul", "波洛"]),
    BK("masnavi", "Masnavi", "玛斯纳维", "مثنوی معنوی", "Rumi", "鲁米", "جلال‌الدین محمد بلخی", "13th century", lang="fa",
       aliases=["Mathnawi", "Masnavi-ye Ma'navi", "Mevlana", "Mevlânâ", "Rumi", "Konya"]),
]

places = [
    ORIG("tr-troy", "Troy (Hisarlık), Çanakkale", "特洛伊（希萨尔利克），恰纳卡莱",
         "The mound of Hisarlık, near the southern mouth of the Dardanelles, generally identified with Homer's Troy (Ilios, Ilium); excavated by Frank Calvert and Heinrich Schliemann from the 1870s, and a UNESCO World Heritage Site since 1998. In Book VI of the Iliad, Hector comes back from the battle into the city and meets Andromache and their baby son at the Scaean gates",
         "希萨尔利克土丘，在达达尼尔海峡南口附近，一般认为就是荷马笔下的特洛伊（伊利昂）；19 世纪 70 年代起由弗兰克·卡尔弗特和海因里希·谢里曼发掘，1998 年列入联合国教科文组织世界遗产。《伊利亚特》第六卷里，赫克托耳从战场回城，在斯卡亚门遇见安德洛玛刻和他们襁褓中的儿子"),
    ORIG("tr-abydos", "Abydos, on the Dardanelles (Hellespont)", "阿拜多斯，达达尼尔海峡（赫勒斯滂）",
         "Ancient city on the Asian shore of the Dardanelles, near Çanakkale, facing Sestos on the European shore. In the legend Leander swam from Abydos to Hero at Sestos every night. On 3 May 1810 Byron and Lieutenant Ekenhead of the frigate Salsette swam the strait the other way, from Sestos to Abydos, in about an hour and ten minutes; Byron wrote this poem on 9 May",
         "古城，在达达尼尔海峡的亚洲一岸，靠近恰纳卡莱，与欧洲一岸的塞斯托斯隔水相望。传说勒安得耳每夜从阿拜多斯游过海峡，去塞斯托斯找赫洛。1810 年 5 月 3 日，拜伦和萨尔塞特号护卫舰的埃肯黑德上尉反方向游过海峡，从塞斯托斯游到阿拜多斯，用了大约一小时十分钟；5 月 9 日拜伦写下这首诗"),
    ORIG("tr-trabzon", "Trabzon (Trapezus)", "特拉布宗（特拉佩祖斯）",
         "Black Sea port, the ancient Greek city of Trapezus, a colony of Sinope. Xenophon's Ten Thousand, marching north after the battle of Cunaxa in 401 BC, reached the sea here. Some days earlier, from the summit of Mount Theches in the Pontic Mountains behind the city, they had first caught sight of the sea and shouted 'Thalatta! Thalatta!', 'The sea! The sea!'; where Theches was is still debated",
         "黑海港口，古希腊城市特拉佩祖斯，锡诺普人的殖民地。公元前 401 年库纳克萨之战后，色诺芬的万人军向北撤退，在这里到达海边。此前，他们在城后本都山脉中的塞克斯山顶第一次望见大海，齐声高喊“大海！大海！”；塞克斯山究竟在哪里，至今仍有争论"),
    ORIG("tr-masumiyet", "The Museum of Innocence, Çukurcuma, Istanbul", "纯真博物馆，伊斯坦布尔楚库尔朱马",
         "A house of 1897 in the Çukurcuma quarter of Beyoğlu, bought by Orhan Pamuk in 1998 and opened in April 2012 as the museum his novel describes, with more than a thousand objects in displays that follow the novel's 83 chapters; the first display is a wall of 4,213 cigarette stubs smoked by Füsun",
         "贝伊奥卢区楚库尔朱马街区一栋 1897 年的房子，奥尔罕·帕慕克 1998 年买下，2012 年 4 月作为小说里写的那座博物馆开放，一千多件物品按小说的 83 章布展；进门第一件展品是一面墙，上面是菲森抽过的 4213 个烟头"),
    ORIG("tr-kars", "Kars", "卡尔斯",
         "City in north-eastern Turkey near the Armenian border, with an old quarter from the decades of Russian rule (1878–1918). Pamuk set Snow here; the name echoes the title, kar being Turkish for snow",
         "土耳其东北部城市，靠近亚美尼亚边境，老城区留有俄国统治时期（1878–1918）的建筑。帕慕克把《雪》放在这里；城名与书名相呼应，土耳其语里 kar 就是“雪”"),
    ORIG("tr-gokcedam", "Gökçedam, Osmaniye (Yaşar Kemal's birthplace)", "格克切达姆，奥斯曼尼耶（亚沙尔·凯马尔故乡）",
         "Village in the Çukurova, then called Hemite, where Yaşar Kemal was born in 1923. Memed, My Hawk, his first novel, tells of the hard life of the villagers of the Taurus and the Çukurova around Adana; Memed's own village, Değirmenoluk, is invented",
         "楚库罗瓦地区的一个村子，当时叫赫米特，亚沙尔·凯马尔 1923 年生在这里。他的第一部小说《瘦子麦麦德》写的是阿达纳一带托罗斯山和楚库罗瓦农民的苦日子；麦麦德自己的村子德伊尔门奥卢克是虚构的"),
    ORIG("tr-sirkeci", "Sirkeci station, Istanbul", "锡尔凯吉火车站，伊斯坦布尔",
         "Station by the Golden Horn, opened in 1890 as the eastern terminus of the Orient Express from Paris; ferries from the nearby piers crossed the Bosphorus to Haydarpaşa, where the lines into Asia began. Christie's novel only says the train leaves 'Stamboul'",
         "金角湾边的火车站，1890 年启用，是从巴黎开来的东方快车的东端终点站；旁边码头的渡船横渡博斯普鲁斯海峡，通往亚洲线路的起点海达尔帕夏站。克里斯蒂的小说里只说火车从“斯坦布尔”开出"),
    PIL("tr-mevlana", "Mevlâna Museum, Konya", "梅夫拉纳博物馆，科尼亚",
        "The former lodge of the Mevlevi order, the whirling dervishes, around the tomb of Jalal al-Din Rumi, who was buried here in 1273; the turquoise-tiled Green Dome over the tomb was finished in 1274. Its collection includes the oldest known copy of the Masnavi, made in 1278, five years after his death",
        "梅夫拉维教团（旋转托钵僧）的旧修道院，围绕着贾拉鲁丁·鲁米的陵墓；鲁米 1273 年葬在这里，墓上铺着青绿色瓷砖的“绿色穹顶”于 1274 年建成。馆藏中有现存最早的《玛斯纳维》抄本，抄于 1278 年，也就是鲁米去世后的第五年",
        ["masnavi"]),
]

lines = [
    GK("tr-il-1", "iliad", "tr-troy", "Book VI, lines 390–406: Hector meets Andromache", "第六卷第 390–406 行：赫克托耳与安德洛玛刻相会", T_ILG,
       re.sub(r" \d+$", "", raw(T_ILG, "Ἦ ῥα γυνὴ ταμίη,", "ἔν τ’ ἄρα οἱ φῦ χειρὶ", "el"), flags=re.M), ["Σκαιάς", "Ἴλιον"],
       T_IL, flow(raw(T_IL, "Hector hurried from the house when she had done speaking,", "taking his hand\nin her own.", "en")),
       ["Scaean gates", "Ilius"],
       "赫克托耳等她说完，就匆匆走出屋子，沿着来时的路走下街道。他穿过城市，来到斯卡亚门——他要从这道门出城到平原上去——这时他的妻子跑来迎他：安德洛玛刻，伟大的厄提翁的女儿；厄提翁在普拉科斯山林木茂密的山坡下统治忒拜，是西里西亚人的王。他的女儿嫁给了赫克托耳，这时带着一个保姆来迎他，保姆怀里抱着他们的小孩子——还只是个婴儿。这是赫克托耳的爱子，像星星一样可爱。赫克托耳给他取名斯卡曼德里奥斯，人们却叫他阿斯提阿那克斯，因为他的父亲独自一人守卫着伊利昂。赫克托耳看着孩子微笑，没有说话；安德洛玛刻站在他身边流着泪，握住他的手。",
       ["斯卡亚门", "伊利昂"], "Samuel Butler (1898)",
       note=" (the edition's line numbers left out; line 406 cut after χειρὶ, where Andromache's speech begins)"),
    EN("tr-by-1", "sestos-to-abydos", "tr-abydos", "The whole poem", "全诗", T_BY,
       stanzas(raw(T_BY, "If, in the month of dark December,", "I've the ague.", "en")), ["Hellespont"],
       "若是在幽暗的十二月，\n惯于夜夜渡水的勒安得耳\n（哪个姑娘记不起这个故事？）\n也要横渡你的流水，宽阔的赫勒斯滂！\n\n"
       "若是冬日的风暴怒号时，\n他也毫不迟疑奔向赫洛，\n而你的激流古时也这般奔涌，\n美丽的维纳斯！我多可怜他们俩！\n\n"
       "至于我，堕落的现代可怜虫，\n虽是在温和宜人的五月，\n也只能无力地伸展湿淋淋的四肢，\n还以为今天干了件壮举。\n\n"
       "可是既然他横渡湍急的潮水，\n照那可疑的传说所讲，\n是为了求爱——天知道还为了什么——\n他为爱而游，我为荣耀而游；\n\n"
       "很难说谁的结局更好：\n可悲的凡人！众神就这样作弄你们！\n他白费了力气，我白费了玩笑：\n因为他淹死了，我却打起了摆子。",
       ["赫勒斯滂"], note=" (stanza numbers left out; Chinese is our own)"),
    GK("tr-an-1", "anabasis", "tr-trabzon", "Book IV, 8.22–23: the Ten Thousand reach the sea", "第四卷 8.22–23：万人军到达海边", T_ANG,
       raw(T_ANG, "Ἐντεῦθεν δ’ ἐπορεύθησαν δύο σταθμοὺς", "ἐλῄζοντο τὴν Κολχίδα.", "el").replace("23\xa0", ""), ["Τραπεζοῦντα"],
       T_AN, flow(raw(T_AN, "From this place they marched on two stages", "whole territory\nof Colchis.", "en")),
       ["Trapezus"],
       "他们从这里又走了两程，共七帕拉桑，在特拉佩祖斯到达海边。这是攸克辛海（黑海）边一座人口众多的希腊城市，是锡诺普人的殖民地，位于科尔基斯人的地界。他们在这里科尔基斯人的村子里驻扎了大约三十天，以这些村子为据点，劫掠整个科尔基斯地区。",
       ["特拉佩祖斯"], "H. G. Dakyns (1890)",
       note=" (the section number 23 left out)"),
    S("tr-mi-1", "museum-of-innocence", "tr-masumiyet", "The novel as a whole", "全书",
      "In the spring of 1975 Kemal, a wealthy young man from Nişantaşı engaged to Sibel, falls in love with Füsun, a poor distant cousin who works in a shop. After she marries someone else he spends eight years visiting her family's house in Çukurcuma, taking away something of hers each time, and these things become his museum of innocence.",
      "1975 年春天，住在尼尚塔什、已与茜贝尔订婚的富家子凯末尔，爱上了在商店当店员的远房穷亲戚菲森。菲森嫁给别人以后，他八年间一次次去她家在楚库尔朱马的房子拜访，每次都带走一件她的东西，这些东西后来成了他的纯真博物馆。",
      ["Çukurcuma"], ["楚库尔朱马"], "https://en.wikipedia.org/wiki/The_Museum_of_Innocence_(museum); https://artsandculture.google.com/story/KAVxIqBekvaEKw"),
    S("tr-sn-1", "pamuk-snow", "tr-kars", "The novel as a whole", "全书",
      "Ka, a poet back from twelve years of political exile in Germany, comes to Kars by bus through a snowstorm to write about a wave of suicides among young women. The snow soon closes every road out of town; for three days Kars is cut off from the world, long enough for a coup staged in the town's theatre, and Ka, who has not written a poem in years, writes nineteen.",
      "诗人卡在德国政治流亡了十二年，刚回国，冒着暴风雪坐长途车来到卡尔斯，要报道一连串年轻女子自杀的事。大雪很快封住了出城的每一条路；三天里卡尔斯与世隔绝，足够在镇上的剧院里演出一场政变，而多年写不出一首诗的卡，写了十九首。",
      ["Kars"], ["卡尔斯"], "https://en.wikipedia.org/wiki/Snow_(Pamuk_novel)"),
    S("tr-mm-1", "memed-my-hawk", "tr-gokcedam", "The novel as a whole", "全书",
      "Slim Memed grows up with his mother in Değirmenoluk, a village in the Taurus Mountains, under the landlord Abdi Ağa, who takes two-thirds of their crops. He runs off with Hatçe, whom the Ağa means for his nephew, wounds Abdi Ağa, kills the nephew and becomes a bandit in the mountains above the Çukurova.",
      "瘦子麦麦德和母亲住在托罗斯山里的德伊尔门奥卢克村，受地主阿卜迪·阿迦压迫，每年三分之二的收成都被他拿走。阿迦要把哈杰嫁给自己的侄子，麦麦德带着她私奔，打伤了阿卜迪·阿迦，杀了他的侄子，在楚库罗瓦平原上方的山里当了土匪。",
      ["Taurus Mountains", "Çukurova"], ["托罗斯山", "楚库罗瓦"],
      "https://www.ebsco.com/research-starters/literature-and-writing/memed-my-hawk-yashar-kemal; https://en.wikipedia.org/wiki/Memed,_My_Hawk"),
    S("tr-oe-1", "murder-on-the-orient-express", "tr-sirkeci", "Part 1, chapters 1–2", "第一部第一至二章",
      "Poirot comes up from Aleppo on the Taurus Express, crosses the Bosphorus from Haydarpaşa and takes a room at the Tokatlian Hotel, meaning to spend a few days seeing Stamboul. A telegram calls him back to London; his old friend M. Bouc of the Wagon-Lit company finds him a berth on the Orient Express leaving that evening, and in the hotel restaurant Poirot first sees Ratchett.",
      "波洛乘托罗斯快车从阿勒颇北上，从海达尔帕夏渡过博斯普鲁斯海峡，住进托卡特良酒店，打算在斯坦布尔观光几天。一封电报要他立刻回伦敦；他的老朋友、国际卧铺车公司的布克先生给他在当晚开出的东方快车上找了个铺位，波洛也正是在酒店餐厅里第一次见到雷切特。",
      ["Stamboul"], ["斯坦布尔"], "https://en.wikipedia.org/wiki/Murder_on_the_Orient_Express; https://www.sparknotes.com/lit/orientexpress/section1/"),
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

HEAD = "// Turkey, hand-written content (tools/content/batches/add_tr1.py, 2026-11-23).\n"
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
