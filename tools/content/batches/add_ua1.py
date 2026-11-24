"""11-24: Ukraine, first pack: 9 new books, 9 places. Shevchenko's grave at Kaniv, Lesya Ukrainka's Nechymne, Gogol's
Sorochyntsi, the Khan's Palace at Bakhchysarai, Bulgakov's house in Kyiv, Kyiv Zoo (Kurkov), Pripyat (Alexievich),
Trochenbrod (Foer) and Kotliarevsky's Poltava.

The map follows China's point of view (decision A-22): Crimea and Sevastopol are Ukrainian regions (tools/build_geo.py
"pov_units"), and the two Chekhov places in Yalta move here from data/ru (cache/ua/move.py, run after this script).

Quotations (5 lines) are cut from Ukrainian and Russian Wikisource pages (tools/content/wikisource.py); translations are our
own drafts (translation: "own"). Books in copyright get scene notes with a fact source. What a cut changes is named in
`checked`.

Coordinates are those of the place's English (or, where noted, Ukrainian) Wikipedia article (cache/ua/coords.json).

Usage: python3 -I add_ua1.py <app_dir> <coords.json> <wikisource_root>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-24"
b.init(APP, "", "ua", DATE)
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

T_ZP = "Струни/1/Заповіт"
T_LP = "Лісова пісня"
T_SF = "Сорочинская ярмарка (Гоголь)/I"
T_BF = "Бахчисарайский фонтан (Пушкин)"
T_WG = "Белая гвардия (Булгаков)/Глава 1"
EXIST = set()

def fixed(s, old, new):
    assert s.count(old) == 1, old
    return s.replace(old, new)

books = [
    BK("zapovit", "Testament", "遗嘱", "Заповіт", "Taras Shevchenko", "塔拉斯·舍甫琴科", "Тарас Шевченко", "1845", lang="uk",
       src=ws.url("uk", "Заповіт"), aliases=["Zapovit", "My Testament", "Kobzar", "Shevchenko", "Як умру, то поховайте", "科布扎尔"]),
    BK("forest-song", "The Forest Song", "森林之歌", "Лісова пісня", "Lesya Ukrainka", "莱霞·乌克兰卡", "Леся Українка", "1911", lang="uk",
       src=ws.url("uk", "Лісова пісня"), aliases=["Lisova pisnia", "Mavka", "Lukash", "Volyn", "Lesia Ukrainka"]),
    BK("sorochyntsi-fair", "The Fair at Sorochyntsi", "索罗钦集市", "Сорочинская ярмарка", "Nikolai Gogol", "果戈理", "Николай Гоголь", "1831",
       lang="ru", src=ws.url("ru", "Сорочинская ярмарка (Гоголь)"),
       aliases=["Sorochintsy Fair", "Evenings on a Farm Near Dikanka", "Вечера на хуторе близ Диканьки", "狄康卡近乡夜话", "Mykola Hohol"]),
    BK("fountain-of-bakhchisaray", "The Fountain of Bakhchisaray", "巴赫奇萨赖的泪泉", "Бахчисарайский фонтан", "Alexander Pushkin", "普希金",
       "Александр Пушкин", "1824", lang="ru", src=ws.url("ru", T_BF),
       aliases=["Fountain of Tears", "Bakhchysarai", "Girei", "Maria", "Zarema", "泪泉"]),
    BK("the-white-guard", "The White Guard", "白卫军", "Белая гвардия", "Mikhail Bulgakov", "米哈伊尔·布尔加科夫", "Михаил Булгаков", "1925",
       lang="ru", src=ws.url("ru", "Белая гвардия (Булгаков)"), aliases=["Belaya gvardiya", "Turbin", "The Days of the Turbins", "Andriivskyi Descent"]),
    BK("death-and-the-penguin", "Death and the Penguin", "企鹅的忧郁", "Смерть постороннего", "Andrey Kurkov", "安德烈·库尔科夫", "Андрей Курков",
       "1996", lang="ru", pd=False, aliases=["Smert postoronnego", "Viktor", "Misha", "Penguin Lost", "Kurkov"]),
    BK("voices-from-chernobyl", "Voices from Chernobyl", "切尔诺贝利的悲鸣", "Чернобыльская молитва", "Svetlana Alexievich", "斯韦特兰娜·阿列克谢耶维奇",
       "Светлана Алексиевич", "1997", lang="ru", pd=False, aliases=["Chernobyl Prayer", "Chernobyl", "Pripyat", "Lyudmila Ignatenko", "Alexievich"]),
    BK("everything-is-illuminated", "Everything Is Illuminated", "了了", "Everything Is Illuminated", "Jonathan Safran Foer", "乔纳森·萨福兰·弗尔",
       "Jonathan Safran Foer", "2002", lang="en", pd=False, aliases=["Trachimbrod", "Trochenbrod", "Augustine", "Alex Perchov", "Foer"]),
    BK("eneida", "Eneida", "埃涅伊达", "Енеїда", "Ivan Kotliarevsky", "伊万·科特利亚列夫斯基", "Іван Котляревський", "1798", lang="uk",
       aliases=["Aeneid travestied", "Kotliarevsky", "Kotlyarevsky", "Poltava"]),
]

places = [
    ORIG("ua-kaniv", "Taras Hill, Kaniv (Shevchenko's grave)", "塔拉斯山，卡尼夫（舍甫琴科墓）",
         "Chernecha Hora, the hill above the Dnieper near Kaniv where Taras Shevchenko was reburied on 22 May 1861, two months after his death in St Petersburg; it has been called Taras Hill since, and is the heart of the Shevchenko National Reserve. Shevchenko wrote 'Testament' in Pereiaslav in December 1845, when he was gravely ill; it asks to be buried on a mound above the Dnieper",
         "切尔内恰山，卡尼夫附近第聂伯河岸上的山丘。塔拉斯·舍甫琴科在圣彼得堡去世两个月后，1861 年 5 月 22 日迁葬于此，此后这座山就叫塔拉斯山，是舍甫琴科国家保护区的中心。舍甫琴科 1845 年 12 月在佩列亚斯拉夫病重时写下《遗嘱》，要人们把他葬在第聂伯河上方的坟丘上"),
    ORIG("ua-nechymne", "Nechymne Lake, Volyn", "内奇姆内湖，沃伦",
         "Karst lake in a 40-hectare protected tract of oak wood and bog near Skulyn, north of Kovel, where Lesya Ukrainka stayed as a child at her uncle's house; it is taken to be the model for the world of The Forest Song, and a Forest Song museum stands there. She wrote the play in 1911 in Kutaisi, in ten to twelve days, and told her mother it came from remembering and missing 'our forests'",
         "沃伦州科韦利以北、斯库林附近的一个喀斯特湖，周围是 40 公顷受保护的橡树林和沼泽。莱霞·乌克兰卡小时候曾在这里的叔叔家住过，一般认为这里就是《森林之歌》那个世界的原型，湖边建有“森林之歌”博物馆。她 1911 年在库塔伊西用十到十二天写成这部剧，对母亲说，这是因为想起了“我们的森林”，心里想念"),
    ORIG("ua-sorochyntsi", "Velyki Sorochyntsi, Poltava region", "大索罗钦齐，波尔塔瓦州",
         "Village near Myrhorod where Nikolai Gogol (Mykola Hohol) was born in 1809, home since the 18th century of the Sorochyntsi Fair, still held every year. The Fair at Sorochyntsi opens Evenings on a Farm Near Dikanka (1831), the book that made Gogol's name. 'Little Russia' (Malorossiya) was the old imperial name for much of Ukraine",
         "米尔霍罗德附近的村子，尼古拉·果戈理 1809 年生于此地；18 世纪以来这里就举办索罗钦集市，今天每年仍在举行。《索罗钦集市》是《狄康卡近乡夜话》（1831）的开篇，果戈理凭这本书成名。“小俄罗斯”是沙俄时代对乌克兰大部分地区的旧称"),
    ORIG("ua-khansaray", "Khan's Palace, Bakhchysarai", "巴赫奇萨赖汗宫",
         "Palace of the Crimean khans in Bakhchysarai. Its Fountain of Tears dates from 1764 and was moved to the fountain courtyard in 1787. Pushkin saw it in September 1820 and wrote The Fountain of Bakhchisaray (1824) on the legend of Khan Girei and his captive Maria; visitors still lay two roses on it, after the opening of his later lyric 'To the Fountain of the Bakhchisaray Palace'",
         "克里米亚汗国历代汗王在巴赫奇萨赖的宫殿。宫中的“泪泉”建于 1764 年，1787 年移到喷泉庭院。普希金 1820 年 9 月来看过它，后来根据吉列伊汗和女俘玛丽亚的传说写成《巴赫奇萨赖的泪泉》（1824）；他后来又写了一首小诗《致巴赫奇萨赖宫的泪泉》，开头说给泉水献上两朵玫瑰，如今游客仍会在泉上放两朵玫瑰"),
    ORIG("ua-bulgakov", "Bulgakov House, 13 Andriivskyi Descent, Kyiv", "布尔加科夫故居，基辅安德烈坡道 13 号",
         "The house where Mikhail Bulgakov's family lived from 1906 to 1919, and where he set the Turbins of The White Guard at the same address, 'No. 13 Alekseevsky Descent'. A museum since 1989–1991; the plaque on the door uses the street name from the novel",
         "米哈伊尔·布尔加科夫一家 1906 年至 1919 年住在这栋房子里；他把《白卫军》里的图尔宾一家安排在同一个门牌，“阿列克谢耶夫斯基坡道 13 号”。1989 至 1991 年间辟为博物馆，门上的门牌用的是小说里的街名"),
    ORIG("ua-kyiv-zoo", "Kyiv Zoo", "基辅动物园",
         "The city zoo of Kyiv. In Andrey Kurkov's Death and the Penguin, written in Russian and set in Kyiv in the mid-1990s, the hard-up zoo has given its animals away to anyone who could feed them, which is how Viktor came to have a king penguin",
         "基辅的城市动物园。在安德烈·库尔科夫用俄语写的《企鹅的忧郁》里，故事发生在 20 世纪 90 年代中期的基辅，捉襟见肘的动物园把动物送给养得起的人，维克多就这样领回了一只王企鹅"),
    ORIG("ua-prypiat", "Pripyat", "普里皮亚季",
         "The town built for the workers of the Chernobyl nuclear power plant, evacuated after the reactor explosion of 26 April 1986 and empty since, inside the exclusion zone. Svetlana Alexievich interviewed more than 500 people for Voices from Chernobyl (1997)",
         "为切尔诺贝利核电站职工修建的城市，1986 年 4 月 26 日反应堆爆炸后全城撤离，此后一直空无一人，位于隔离区内。斯韦特兰娜·阿列克谢耶维奇为写《切尔诺贝利的悲鸣》（1997）采访了五百多人"),
    ORIG("ua-trochenbrod", "Trochenbrod (site), Volyn", "特罗亨布罗德旧址，沃伦",
         "Site of Trochenbrod (Zofiówka), an all-Jewish shtetl in the woods of Volyn, wiped out in the Holocaust. Jonathan Safran Foer's grandfather was born there; it is the model for the Trachimbrod of Everything Is Illuminated",
         "特罗亨布罗德（佐菲夫卡）的旧址，沃伦林中一个全是犹太人的小镇，在大屠杀中被毁灭。乔纳森·萨福兰·弗尔的祖父生在这里；这里就是《了了》中特拉钦布罗德的原型"),
    PIL("ua-kotliarevsky", "Kotliarevsky Museum, Poltava", "科特利亚列夫斯基纪念馆，波尔塔瓦",
        "Literary-memorial museum of Ivan Kotliarevsky (1769–1838), opened in Poltava in 1952 on the site of the family's small estate. The first three parts of his Eneida, a burlesque of Virgil's Aeneid, came out in St Petersburg in 1798 without his permission; it is counted as the first literary work published wholly in modern Ukrainian",
        "伊万·科特利亚列夫斯基（1769–1838）文学纪念馆，1952 年在波尔塔瓦他家小庄园的旧址上开馆。他戏仿维吉尔《埃涅阿斯纪》的长诗《埃涅伊达》，前三部分 1798 年未经他同意在圣彼得堡出版，被认为是第一部完全用现代乌克兰语出版的文学作品",
        ["eneida"]),
]

lines = [
    Q("ua-zp-1", "zapovit", "ua-kaniv", "First stanza", "第一节", T_ZP,
      raw(T_ZP, "Як умру, то поховайте", "Як реве ревучий!", "uk"), ["Вкраїні", "Дніпро"],
      "When I die, then bury me\nOn a grave mound\nAmid the wide steppe\nIn my dear Ukraine,\nSo that the broad fields,\nThe Dnieper and its steep banks\nCould be seen, could be heard,\nHow the roaring river roars!",
      ["Ukraine", "Dnieper"],
      "我死了以后，请把我埋葬\n在一座坟丘上，\n在辽阔的草原中间，\n在亲爱的乌克兰：\n好让那宽广的田野，\n第聂伯河和它的陡岸\n都看得见，听得见\n奔腾的河水怎样咆哮！",
      ["乌克兰", "第聂伯河"], note=" (Bohdan Lepky's anthology Struny, 1922)", site="Ukrainian"),
    Q("ua-fs-1", "forest-song", "ua-nechymne", "Prologue, opening stage direction", "序幕，开头的舞台说明", T_LP,
      raw(T_LP, "Старезний, густий, предковічний ліс на Волині.", "з великим прастарим дубом.", "uk"), ["Волині"],
      "An ancient, dense, primeval forest in Volyn. In the middle of the forest, a wide clearing with a weeping birch and a great, very old oak.",
      ["Volyn"],
      "沃伦一片古老、茂密的原始森林。森林当中是一片宽阔的空地，长着一棵垂枝白桦和一棵高大的老橡树。",
      ["沃伦"], note=" (the first two sentences)", site="Ukrainian"),
    Q("ua-sf-1", "sorochyntsi-fair", "ua-sorochyntsi", "Chapter I, opening", "第一章开头", T_SF,
      raw(T_SF, "Как упоителен, как роскошен летний день в Малороссии!", "в воздушных объятиях своих!", "ru"), ["Малороссии"],
      "How intoxicating, how luxuriant is a summer day in Little Russia! How languidly hot are those hours when midday glitters in stillness and heat, and the blue, immeasurable ocean, bent over the earth like a voluptuous dome, seems to have fallen asleep, all drowned in bliss, embracing and pressing the fair one in its airy arms!",
      ["Little Russia"],
      "小俄罗斯的夏日多么醉人，多么绚丽！正午在寂静和炎热中闪耀的那几个钟头多么闷热难熬，那蔚蓝无边的海洋像一座充满情欲的穹顶俯向大地，仿佛睡着了，整个沉浸在安乐之中，用它空气般的臂膀拥抱着、搂紧了这美人！",
      ["小俄罗斯"], note=" (the first two sentences)", site="Russian"),
    Q("ua-bf-1", "fountain-of-bakhchisaray", "ua-khansaray", "The Fountain of Tears, and the poet's visit", "泪泉，以及诗人来访", T_BF,
      fixed(raw(T_BF, "Опустошив огнем войны", "В забвенье дремлющий дворец.", "ru"), "Вовдвигнул", "Воздвигнул"), ["Тавриду", "Бахчисарая"],
      "Having laid waste with the fire of war\nThe lands that border the Caucasus\nAnd the peaceful villages of Russia,\nThe khan returned to Tauris\nAnd in memory of sorrowful Maria\nRaised up a marble fountain\nIn a secluded corner of the palace.\nAbove it the Mohammedan crescent\nIs overshadowed by a cross\n(A daring symbol, to be sure,\nThe sorry fault of ignorance).\nThere is an inscription: the corroding years\nHave not yet worn it smooth.\nBehind its foreign letters\nWater murmurs in the marble\nAnd drips in cold tears,\nNever falling silent.\nSo a mother weeps in days of grief\nFor her son, fallen in the war.\nThe young maidens of that land\nLearned the legend of old times,\nAnd that sombre monument\nThey named the Fountain of Tears.\nLeaving the north at last,\nForgetting feasts for a long while,\nI visited Bakhchisaray's\nPalace, slumbering in oblivion.",
      ["Tauris", "Bakhchisaray"],
      "在高加索附近的国土\n和俄罗斯安宁的村庄\n燃起战火、洗劫之后，\n可汗回到了塔夫里达，\n为了纪念悲伤的玛丽亚，\n建起一座大理石喷泉，\n在宫殿一个僻静的角落。\n泉上，伊斯兰的新月\n被十字架荫护着\n（这象征当然大胆，\n是无知的可怜过错）。\n泉上有铭文：侵蚀的岁月\n还没有把它磨平。\n在那陌生的字迹后面，\n泉水在大理石里潺潺流淌，\n化作冰冷的泪珠滴落，\n从来不曾停息。\n就像母亲在悲痛的日子里\n哭她战死的儿子。\n那地方的少女们\n听说了这古老的传说，\n就把这阴郁的纪念物\n称作“泪泉”。\n终于，我离开北方，\n把宴饮长久抛在脑后，\n来到巴赫奇萨赖\n在遗忘中沉睡的宫殿。",
      ["塔夫里达", "巴赫奇萨赖"], note=" (Wikisource's misprint 'Вовдвигнул' corrected to 'Воздвигнул')", site="Russian"),
    Q("ua-wg-1", "the-white-guard", "ua-bulgakov", "Chapter 1: the house on Alekseevsky Descent", "第一章：阿列克谢耶夫斯基坡道上的房子", T_WG,
      raw(T_WG, "Много лет до смерти, в доме", "совсем крошечного Николку.", "ru"), ["Алексеевскому спуску"],
      "For many years before her death, in the house at No. 13 Alekseevsky Descent, the tiled stove in the dining room warmed and raised little Elena, Alexei the eldest and tiny Nikolka.",
      ["Alekseevsky Descent"],
      "母亲去世前的许多年里，在阿列克谢耶夫斯基坡道 13 号的房子里，餐厅那座瓷砖壁炉温暖着、养育着小叶莲娜、老大阿列克谢和还很小很小的尼科尔卡。",
      ["阿列克谢耶夫斯基坡道"], site="Russian"),
    S("ua-dp-1", "death-and-the-penguin", "ua-kyiv-zoo", "The novel as a whole", "全书",
      "Viktor, a would-be writer in Kyiv, lives alone with Misha, a king penguin he took in when the city zoo, unable to feed its animals, gave them away. To keep Misha in fish he takes a newspaper job writing obituaries of public figures who are still alive, until the people he writes about begin to die.",
      "基辅一个想当作家的年轻人维克多，独自和一只王企鹅米沙住在一起；城里的动物园养不起动物，把它们送了人，米沙就是这样到他家的。为了让米沙有鱼吃，他在一家报社找了份差事，给还活着的知名人物写讣告，直到他写过的人一个接一个死去。",
      ["Kyiv"], ["基辅"], "https://en.wikipedia.org/wiki/Death_and_the_Penguin; https://www.penguinrandomhouse.com/books/643170/death-and-the-penguin-by-andrey-kurkov/"),
    S("ua-vc-1", "voices-from-chernobyl", "ua-prypiat", "Prologue: A Solitary Human Voice", "序章：一个孤独的声音",
      "The book opens with Lyudmila Ignatenko, a young wife from Pripyat. Her husband Vasily, a fireman, was among the first sent to the burning reactor on the night of the explosion; she stayed by him in a radiation hospital through the fourteen days it took him to die.",
      "全书从柳德米拉·伊格纳坚科开始，她是普里皮亚季的一位年轻妻子。她的丈夫瓦西里是消防员，爆炸当夜最早被派去扑救燃烧的反应堆的人之一；她在辐射病医院守在他身边，陪他度过了走向死亡的十四天。",
      ["Pripyat"], ["普里皮亚季"], "https://www.npr.org/5355520; https://www.supersummary.com/voices-from-chernobyl/prologue-and-part-1-chapters-1-4-summary"),
    S("ua-ei-1", "everything-is-illuminated", "ua-trochenbrod", "The novel as a whole", "全书",
      "Jonathan, a young American, comes to Ukraine with a photograph of Augustine, the woman said to have saved his grandfather from the Nazis, to look for his grandfather's shtetl, Trachimbrod. His guide Alex, Alex's 'blind' grandfather, who drives, and their dog Sammy Davis, Junior, Junior take him out into the countryside, while other chapters tell Trachimbrod's invented history up to its destruction in 1942.",
      "年轻的美国人乔纳森带着一张照片来到乌克兰，照片上是据说从纳粹手里救过他祖父的女人奥古斯丁；他要找祖父出生的犹太小镇特拉钦布罗德。导游亚历克斯、亚历克斯那位自称“失明”却负责开车的祖父，还有他们的狗“小小萨米·戴维斯”，陪他深入乡间；另一些章节则讲述特拉钦布罗德虚构的历史，直到它 1942 年被毁灭。",
      ["Trachimbrod"], ["特拉钦布罗德"], "https://en.wikipedia.org/wiki/Everything_Is_Illuminated; https://www.gradesaver.com/everything-is-illuminated/study-guide/summary"),
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

HEAD = "// Ukraine, hand-written content (tools/content/batches/add_ua1.py, 2026-11-24).\n"
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
