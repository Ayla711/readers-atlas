"""11-24: South Africa, first pack: 8 new books (The Lusiads shared with Portugal), 8 places. Adamastor at the Cape of Good Hope
(Camoes), Quatermain's house on the Berea (Haggard), Gandhi at Pietermaritzburg station, Paton's Ixopo, Mandela on Robben
Island and in Soweto, Olive Schreiner's house in Cradock and Sol Plaatje's in Kimberley. The map has the nine provinces.

Quotations (3 lines) are cut from Portuguese and English Wikisource pages (tools/content/wikisource.py); translations are
our own drafts. Books in copyright get scene notes with a fact source. What a cut changes is named in `checked`.

Coordinates are those of the place's English Wikipedia article, Schreiner House's from Wikidata (coords/add_za1.json).

Fix of 11-24 (the atlas's rule: a book worth having is hung on the nearest real place even when its exact spot cannot be
found): Disgrace is added at Salem, Mhudi is quoted at Thaba Nchu (English Wikisource does have it), and The Story of an
African Farm and Native Life in South Africa get scene notes on the Schreiner and Plaatje houses (neither text is on
English Wikisource, and Project Gutenberg could not be reached from here).

Usage: python3 -I add_za1.py <app_dir> <coords.json> <wikisource_root>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-24"
b.init(APP, "", "za", DATE)
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

T_LU = "Os Lusíadas (grafia atualizada)/V"
T_KS = "King Solomon's Mines/Chapter III"
T_GA = "The Story of My Experiments with Truth/Volume 1/Part 2/Chapter 8"
EXIST = {"pt-lusiadas"}

def once(title, s, lang):
    """the cut must start at the only place the words stand on the page"""
    n = ws.text(os.path.join(WSR, lang), title).count(s)
    assert n == 1, (title, s, n)
    return s

def TR(id, book, place, loc, loc_zh, title, text, hl, zh, hl_zh, translator, note=""):
    """a book quoted in a public-domain English translation (the book carries orig_note); Chinese our own"""
    assert "[" not in text and "]" not in text and "\\xa0" not in text and "  " not in text, (id, text[:40])
    for h in hl: assert h in text, (id, h)
    for h in hl_zh: assert h in zh, (id, h)
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh, text_en=text, highlight_en=hl, translation=translator,
                text_zh=zh, highlight_zh=hl_zh, status="draft", checked=f"English Wikisource, {title}{note}; Chinese our own, {DATE}")

books = [
    BK("king-solomons-mines", "King Solomon's Mines", "所罗门王的宝藏", "King Solomon's Mines", "H. Rider Haggard", "亨利·赖德·哈格德", "H. Rider Haggard", "1885",
       lang="en", src=ws.url("en", "King Solomon's Mines"), aliases=["Allan Quatermain", "Quatermain", "Kukuanaland", "Haggard", "哈格德"]),
    BK("experiments-with-truth", "The Story of My Experiments with Truth", "我体验真理的故事", "સત્યના પ્રયોગો અથવા આત્મકથા", "Mahatma Gandhi", "甘地",
       "મોહનદાસ કરમચંદ ગાંધી", "1925–1929", lang="gu", src=ws.url("en", "The Story of My Experiments with Truth"),
       orig_note="Written in Gujarati and first printed in instalments in Navajivan, 1925–1929; quoted in Mahadev Desai's English translation",
       aliases=["An Autobiography", "Gandhi's autobiography", "Satyana Prayogo", "Mohandas Gandhi", "甘地自传"]),
    BK("cry-the-beloved-country", "Cry, the Beloved Country", "哭吧，亲爱的祖国", "Cry, the Beloved Country", "Alan Paton", "艾伦·佩顿", "Alan Paton", "1948",
       lang="en", pd=False, aliases=["Stephen Kumalo", "Ndotsheni", "Absalom", "Paton"]),
    BK("long-walk-to-freedom", "Long Walk to Freedom", "漫漫自由路", "Long Walk to Freedom", "Nelson Mandela", "纳尔逊·曼德拉", "Nelson Mandela", "1994",
       lang="en", pd=False, aliases=["Mandela's autobiography", "Madiba", "曼德拉自传"]),
    BK("story-of-an-african-farm", "The Story of an African Farm", "一个非洲庄园的故事", "The Story of an African Farm", "Olive Schreiner", "奥利芙·施赖纳",
       "Olive Schreiner", "1883", lang="en", src="https://www.gutenberg.org/ebooks/1441", aliases=["Ralph Iron", "Lyndall", "Waldo", "Karoo", "Schreiner"]),
    BK("native-life-in-south-africa", "Native Life in South Africa", "南非土著生活", "Native Life in South Africa", "Sol Plaatje", "索尔·普拉杰", "Sol Plaatje", "1916",
       lang="en", src="https://www.gutenberg.org/ebooks/1452", aliases=["Natives' Land Act", "Plaatje", "Solomon Plaatje"]),
    BK("mhudi", "Mhudi", "姆胡迪", "Mhudi", "Sol Plaatje", "索尔·普拉杰", "Sol Plaatje", "1930", lang="en", src=ws.url("en", "Mhudi"),
       aliases=["An Epic of South African Native Life a Hundred Years Ago", "Plaatje", "Solomon Plaatje"]),
]

places = [
    ORIG("za-cape", "Cape of Good Hope", "好望角",
         "Rocky headland at the south-western tip of the Cape Peninsula. Bartolomeu Dias rounded it in 1488 and called it the Cape of Storms, Cabo das Tormentas. In Canto V of The Lusiads (1572) the cape rises before Vasco da Gama's ships as the giant Adamastor, a figure Camões invented, who foretells the wrecks awaiting the Portuguese and then names himself",
         "开普半岛西南端的岩石岬角。1488 年巴尔托洛梅乌·迪亚士绕过这里，把它叫作风暴角。《卢济塔尼亚人之歌》（1572）第五章里，这座海角在达·伽马的船队面前化作巨人阿达马斯托尔——卡蒙斯自己创造的形象——预言葡萄牙人日后的海难，然后报出自己的名字"),
    ORIG("za-berea", "The Berea, Durban", "贝里亚，德班",
         "The ridge above the centre of Durban, looking out over the city and the Indian Ocean. Allan Quatermain, the narrator of King Solomon's Mines, has his small house here, and the expedition sets out from it. Rider Haggard came to Natal in 1875, aged nineteen, on the staff of the Lieutenant-Governor, Sir Henry Bulwer, and stayed in southern Africa until 1882",
         "德班市中心上方的山脊，俯瞰全城和印度洋。《所罗门王的宝藏》的叙述者艾伦·夸特梅因的小屋就在这里，探险队也从这里出发。赖德·哈格德 1875 年十九岁时来到纳塔尔，在副总督亨利·布尔沃爵士手下做事，在南部非洲一直待到 1882 年"),
    ORIG("za-pmb-station", "Pietermaritzburg railway station", "彼得马里茨堡火车站",
         "The station where, in 1893, the young lawyer M. K. Gandhi, travelling from Durban to Pretoria on a first-class ticket, was put off the train because a white passenger objected to sharing the compartment with him. He spent the winter night in the waiting room, and in his autobiography he dates his resolve to fight colour prejudice from that night",
         "1893 年，年轻的律师甘地持头等车票从德班去比勒陀利亚，因为一名白人乘客不愿与他同处一个包厢，在这座车站被赶下火车。他在候车室里度过了那个冬夜；他在自传里说，自己与肤色歧视抗争的决心就是从那一夜开始的"),
    ORIG("za-ixopo", "Ixopo, KwaZulu-Natal", "伊克索波，夸祖鲁-纳塔尔",
         "Small town in the hills of southern KwaZulu-Natal. Alan Paton began his working life as a teacher at Ixopo High School. Cry, the Beloved Country opens here; Ndotsheni, the village of the priest Stephen Kumalo, is invented but lies near by",
         "夸祖鲁-纳塔尔南部山间的小镇。艾伦·佩顿大学毕业后先在伊克索波中学教书。《哭吧，亲爱的祖国》从这里写起；牧师斯蒂芬·库马洛的村子恩多切尼是虚构的，就在附近"),
    ORIG("za-robben", "Robben Island", "罗本岛",
         "Island in Table Bay off Cape Town, a prison for political prisoners under apartheid and a UNESCO World Heritage Site since 1999. Nelson Mandela was held here from 1964 to 1982, the first eighteen of his twenty-seven years in prison; in 1975 he began to write his memoirs here in secret",
         "开普敦外桌湾里的小岛，种族隔离时期关押政治犯的监狱，1999 年列入联合国教科文组织世界遗产。纳尔逊·曼德拉 1964 年至 1982 年被关在这里，他二十七年牢狱生涯的头十八年就在岛上度过；1975 年他开始在这里秘密写回忆录",
         offshore_island=True),
    PIL("za-mandela-house", "Mandela House, Vilakazi Street, Soweto", "曼德拉故居，索韦托维拉卡齐街",
        "The small brick house at 8115 Orlando West where Nelson Mandela lived from 1946 to 1962; he gave it to the Soweto Heritage Trust in 1997 and it opened as a museum in December that year. Desmond Tutu's house is a short way along the same street",
        "奥兰多西区 8115 号的小砖房，纳尔逊·曼德拉 1946 年至 1962 年住在这里；1997 年他把房子捐给索韦托遗产信托基金，同年 12 月作为博物馆开放。德斯蒙德·图图的家就在同一条街上不远处",
        ["long-walk-to-freedom"]),
    PIL("za-schreiner-house", "Schreiner House, Cradock (Nxuba)", "施赖纳故居，克拉多克（恩克苏巴）",
        "The house at 9 Cross Street where Olive Schreiner lived as a girl, after her brother Theo became a headmaster in Cradock in 1867; now a museum of her life, a branch of the national literary museum. She went on to work as a governess on farms in the Karoo, which gave her the setting of The Story of an African Farm (1883, as 'Ralph Iron'). She died in 1920 and lies on top of Buffelskop, a mountain near the town. Cradock was officially renamed Nxuba in 2022",
        "克罗斯街 9 号的房子。1867 年哥哥西奥到克拉多克当校长，少女时代的奥利芙·施赖纳随他住在这里；现在是介绍她生平的博物馆，属国家文学博物馆的分馆。后来她到卡鲁的几家农场当家庭教师，《一个非洲庄园的故事》（1883，署名“拉尔夫·艾恩”）的背景就来自那里。她 1920 年去世，葬在镇子附近的布法尔斯科普山顶。克拉多克 2022 年正式改名恩克苏巴",
        ["story-of-an-african-farm"]),
    PIL("za-plaatje-house", "Sol Plaatje Museum, 32 Angel Street, Kimberley", "索尔·普拉杰博物馆，金伯利天使街 32 号",
        "The house where Sol Plaatje, journalist, translator and a founder of the organisation that became the ANC, lived in his last years; declared a national monument in 1992 and now a museum and library. Native Life in South Africa (1916) is his account of what the Natives' Land Act of 1913 did to black farmers; Mhudi, finished in 1920 and published in 1930, was the first novel written in English by a black South African. He died in 1932 and is buried in Kimberley",
        "索尔·普拉杰晚年的住所；他是记者、翻译家，也是后来的非国大的创建者之一。房子 1992 年被列为国家纪念物，现在是博物馆和图书馆。《南非土著生活》（1916）记下了 1913 年《土著土地法》给黑人农民带来的遭遇；《姆胡迪》1920 年写成、1930 年出版，是南非黑人用英语写的第一部长篇小说。他 1932 年去世，葬在金伯利",
        ["native-life-in-south-africa", "mhudi"]),
]

lines = [
    Q("za-lus-1", "pt-lusiadas", "za-cape", "Canto V, stanza 50", "第五章第 50 节", T_LU,
      raw(T_LU, '"' + once(T_LU, "Eu sou aquele oculto e grande Cabo,", "pt"), "A quem vossa ousadia tanto ofende.", "pt"), ["Tormentório"],
      "'I am that great and hidden Cape\nwhich you people call the Cape of Storms,\nnever known to Ptolemy, Pomponius, Strabo,\nPliny, or any who came before.\nHere I bring the whole coast of Africa to an end\nin this my Promontory, never seen till now,\nwhich stretches out towards the Antarctic Pole\nand which your daring so offends.",
      ["Cape of Storms"],
      "“我就是那座隐秘的大海角，\n你们这些人把我叫作风暴角；\n托勒密、庞波尼乌斯、斯特拉波、\n普林尼和所有前人，都不曾知道我。\n整条非洲海岸在这里由我收束，\n就在我这座从未有人见过的岬角，\n它一直伸向南极，\n你们的大胆冒犯了它。",
      ["风暴角"], note=" (the dash that opens the speech left out; Adamastor goes on speaking in stanza 51)", site="Portuguese"),
    EN("za-ks-1", "king-solomons-mines", "za-berea", "Chapter 3", "第三章", T_KS,
       flow(raw(T_KS, once(T_KS, "When we came up again the moon was out", "en"), "sparkled a hundred lights.", "en")) + "\n…\n"
       + flow(raw(T_KS, once(T_KS, "Next day we went ashore", "en"), "which I call my home.", "en")),
       ["Berea"],
       "我们再上甲板时，月亮已经出来了，把海面和岸上照得通亮，连灯塔那一下下又快又大的闪光都几乎显得暗淡。岸上飘来一阵阵甜甜的香料气味，总让我想起赞美诗和传教士；贝里亚山坡上人家的窗子里，闪着上百点灯火。\n…\n第二天我们上了岸，我把亨利爵士和古德上校安顿在我盖在贝里亚的那间小棚屋里，我管它叫我的家。",
       ["贝里亚"], note=" (two passages; Chinese is our own)"),
    TR("za-ga-1", "experiments-with-truth", "za-pmb-station", "Part 2, chapter 8, 'On the Way to Pretoria'", "第二部第八章“去比勒陀利亚途中”", T_GA,
       raw(T_GA, once(T_GA, "The train reached Maritzburg, the capital of Natal,", "en"), "at about 9 p.m.", "en") + "\n…\n"
       + raw(T_GA, once(T_GA, "It was winter, and winter in the higher regions", "en"), "so I sat and shivered.", "en") + "\n…\n"
       + raw(T_GA, once(T_GA, "I began to think of my duty.", "en"), "without fulfilling my obligation.", "en"),
       ["Maritzburg"],
       "火车晚上九点左右到达纳塔尔的首府马里茨堡。\n…\n那是冬天，南非高地的冬天冷得厉害。马里茨堡地势高，更是冷得刺骨。我的外套在行李里，可我不敢去要，怕再受一次侮辱，只好坐在那里发抖。\n…\n我开始思考自己的责任。我是该为自己的权利抗争，还是回印度去？还是不理会这些侮辱，先去比勒陀利亚，办完案子再回印度？没有尽到责任就跑回印度，那是懦弱。",
       ["马里茨堡"], "Mahadev Desai (1927)", note=" (three passages)"),
    S("za-cb-1", "cry-the-beloved-country", "za-ixopo", "Book 1, chapters 1–2", "第一卷第一至二章",
      "The novel opens on the road that runs from Ixopo into the hills. In the village of Ndotsheni the Zulu priest Stephen Kumalo receives a letter from a fellow priest, Theophilus Msimangu, in Johannesburg, and sets out for the city to look for his sister and for his son Absalom.",
      "小说从伊克索波通进山里的那条路写起。在恩多切尼村，祖鲁族牧师斯蒂芬·库马洛收到约翰内斯堡的同道西奥菲勒斯·姆西曼古的来信，于是动身进城，去找自己的妹妹和儿子押沙龙。",
      ["Ixopo"], ["伊克索波"], "https://en.wikipedia.org/wiki/Cry,_the_Beloved_Country"),
    S("za-lw-1", "long-walk-to-freedom", "za-robben", "The Robben Island chapters", "罗本岛各章",
      "After the Rivonia Trial Mandela and his fellow accused are flown to Robben Island in 1964. He describes the damp concrete cell, about eight feet by seven, with a straw mat to sleep on; the days spent breaking stones in the yard and then, from 1965, working in the lime quarry; and the memoirs he began in 1975, a copy of which was smuggled out while the buried pages were found by the warders.",
      "瑞佛尼亚审判之后，1964 年曼德拉和同案的人被用飞机送到罗本岛。他写到那间潮湿的水泥牢房，大约八英尺长、七英尺宽，睡在一张草垫上；写到在院子里砸石头的日子，以及 1965 年起在石灰石矿场的劳动；还有 1975 年动笔的回忆录——一份抄本被偷运出岛，埋在地下的手稿却被看守发现。",
      ["Robben Island"], ["罗本岛"], "https://en.wikipedia.org/wiki/Nelson_Mandela; https://en.wikipedia.org/wiki/Long_Walk_to_Freedom"),
]

# ---- 11-24 fix: famous books hung even without an exact spot (user rule) ----
T_MH = "Mhudi/Chapter 10"
books += [
    BK("disgrace", "Disgrace", "耻", "Disgrace", "J. M. Coetzee", "J. M. 库切", "J. M. Coetzee", "1999", lang="en", pd=False,
       aliases=["David Lurie", "Lucy", "Salem", "Coetzee", "库切"]),
]
places += [
    ORIG("za-salem", "Salem, Eastern Cape", "塞勒姆，东开普省",
         "Small village in the Eastern Cape, founded by a party of the 1820 Settlers. In Disgrace (1999) David Lurie leaves Cape Town for his daughter Lucy's smallholding at Salem; she sells her produce at a market stall in nearby Grahamstown. The smallholding itself is invented; the pin is the village's point",
         "东开普省的小村子，由 1820 年移民中的一批人建立。《耻》（1999）里，戴维·卢里离开开普敦，来到女儿露西在塞勒姆的小农场；她在附近格雷厄姆斯敦的集市上摆摊卖自家种的东西。农场本身是虚构的，图钉标在村子的位置"),
    ORIG("za-thaba-nchu", "Thaba Nchu", "塔巴恩丘",
         "Town in the Free State, east of Bloemfontein. In Mhudi, the Barolong who survive the sacking of their capital Kunana by the Matebele rebuild their lives at Thaba Nchu (the book spells it Thaba Ncho) under Chief Moroka, and it is here that the first party of Voortrekkers reaches them",
         "自由邦省的小镇，在布隆方丹以东。《姆胡迪》里，巴罗隆人的都城库纳纳被马塔贝莱人攻破，幸存者在莫罗卡酋长带领下在塔巴恩丘（书中拼作 Thaba Ncho）重建家园；第一批迁徙的布尔人也是在这里来到他们中间"),
]
lines += [
    S("za-di-1", "disgrace", "za-salem", "The chapters on the smallholding", "写小农场的各章",
      "David Lurie, a professor in Cape Town who loses his post after an affair with a student, goes to his daughter Lucy's smallholding at Salem, where she grows flowers and vegetables and boards dogs, and he helps her friend Bev Shaw at the animal clinic. Three men attack the farm: they set Lurie on fire and rape Lucy.",
      "开普敦的教授戴维·卢里与学生发生关系后丢了职位，来到女儿露西在塞勒姆的小农场；露西种花种菜，还替人寄养狗，他则去给她的朋友贝芙·肖的动物诊所帮忙。三个男人袭击了农场：他们放火烧卢里，强暴了露西。",
      ["Salem"], ["塞勒姆"],
      "https://www.lrb.co.uk/the-paper/v21/n20/elizabeth-lowry/like-a-dog; https://www.ebsco.com/research-starters/literature-and-writing/disgrace-j-m-coetzee; https://swisseduc.ch/english/readinglist/coetzee_jm/disgrace/summary.html"),
    EN("za-mh-1", "mhudi", "za-thaba-nchu", "Chapter 10, 'Arrival of the Voortrekkers'", "第十章“迁徙者到来”", T_MH,
       raw(T_MH, once(T_MH, "Thus, for a second time, their dramatic arrival", "en"), "each carried a rifle.", "en"),
       ["Thaba Ncho"],
       "于是，他俩戏剧性的到来，又一次成了塔巴恩丘内外人们围着火堆闲谈的好话题。此后好几个月，女人们在家里、在玉米地里干活时，总也说不够他们这段传奇。男人们晚上讲他们的故事打发时间，白天在树荫下鞣皮子、缝皮毯时也讲。人们远道而来看他们，还给他们带来许多礼物。看来他们的“死而复生”真要成为一个经久不衰的话题，压过其他一切，直到有一天，一队白人来到了塔巴恩丘，才把它比了下去。\n他们骑着马，每人都背着一支枪。",
       ["塔巴恩丘"], note=" (Chinese is our own)"),
    S("za-af-1", "story-of-an-african-farm", "za-schreiner-house", "The novel as a whole", "全书",
      "Three children, Waldo, Em and Lyndall, grow up on a farm in the Karoo; the novel follows them first as children and then as adults, and is in part autobiographical, Waldo and Lyndall sharing much of Schreiner's own life and thought. The farm is not a real one that can be found; the line hangs on the house where Schreiner lived as a girl.",
      "瓦尔多、埃姆和林德尔三个孩子在卡鲁的一座农场上长大；小说先写他们的童年，再写他们长大成人，带有自传色彩，瓦尔多和林德尔身上有许多施赖纳本人的经历和思想。那座农场找不到真实的对应地点，这一条挂在施赖纳少女时代住过的房子上。",
      ["Karoo"], ["卡鲁"], "https://en.wikipedia.org/wiki/The_Story_of_an_African_Farm"),
    S("za-nl-1", "native-life-in-south-africa", "za-plaatje-house", "The book as a whole", "全书",
      "Plaatje's account, published in London in 1916 under the title Native Life in South Africa, Before and Since the European War and the Boer Rebellion, of the Natives' Land Act of 1913 and what it did to black farmers. The line hangs on his house in Kimberley.",
      "普拉杰的记述，1916 年在伦敦出版，全名《欧洲战争与布尔叛乱前后的南非土著生活》，写 1913 年《土著土地法》以及它给黑人农民带来的遭遇。这一条挂在他在金伯利的故居。",
      ["South Africa"], ["南非"], "https://en.wikipedia.org/wiki/Sol_Plaatje; https://en.wikipedia.org/wiki/Native_Life_in_South_Africa"),
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

HEAD = "// South Africa, hand-written content (tools/content/batches/add_za1.py, 2026-11-24).\n"
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
