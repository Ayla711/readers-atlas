"""11-23: Russia, fifth pack: Siberia and the Far East. Books whose weight lies east of the Urals are pinned there:
Resurrection moves from Butyrka prison to Tomsk and the Siberian road (quotation, Part 3), Zuleikha gains the Angara,
Farewell to Matyora gains Rasputin's flooded village, Crime and Punishment gains its Siberian epilogue at Omsk.
New: Chekhov's From Siberia, Pushkin's message to the Decembrists, Korolenko's Makar's Dream, Yevtushenko, Rytkheu,
Yershov. 8 quotations from Russian and French Wikisource (own English and Chinese drafts), 4 scene notes.

Usage: python3 -I add_ru5.py <app_dir> <coords5.json> <wikisource_root>"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-23"
b.init(APP, "", "ru", DATE)
W = b.W
RUW = "https://ru.wikipedia.org/wiki/"
GAP = b.GAP

def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, pd=True, **kw):
    d = dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
             orig_lang=kw.pop("lang", "ru"), public_domain=pd, source_url=kw.pop("src", None), author_orig=author_orig)
    d.update(kw)
    return {k: v for k, v in d.items() if v is not None or k == "source_url"}

def C(pid):
    c = CO[pid]
    return c["lat"], c["lon"], c["st"], c["su"]

def ORIG(pid, name, zh, en_note, zh_note, **kw): return b.ORIG(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PROTO(pid, name, zh, en_note, zh_note, **kw): return b.PROTO(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PIL(pid, name, zh, en_note, zh_note, ids, **kw): return b.PIL(pid, name, zh, *C(pid), en_note, zh_note, ids, **kw)
S = b.S

def raw(title, start, end, lang="ru"):
    """the page's own text between two markers; the markers are matched with no-break and thin spaces read as spaces"""
    t = ws.text(os.path.join(WSR, lang), title)
    n = re.sub("[\xa0\u202f\u2009\u2007]", " ", t)
    i = n.find(start)
    assert i >= 0, (title, start)
    j = n.find(end, i)
    assert j >= 0, (title, start, end)
    return t[i:j + len(end)]

def flow(s):
    """a hard-wrapped plain-text page: lines joined, doubled spaces written as one"""
    return re.sub(r" {2,}", " ", s.replace("\n", " "))

def Q(id, book, place, loc, loc_zh, site, title, orig, hl_orig, en, hl_en, zh, hl_zh, note=""):
    if re.search("[\xa0   ]", orig):
        orig = re.sub("[\xa0   ]+", " ", orig)
        orig = re.sub(r" {2,}", " ", orig)
        note += " (no-break and thin spaces written as plain spaces)"
    if re.search(r"(?m)^ +", orig):
        orig = re.sub(r"(?m)^ +", "", orig)
        note += " (verse indent dropped)"
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls:
            assert h in text, (id, h)
    assert "  " not in orig and "[" not in orig, (id, "spacing or page mark")
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh,
                text_orig=orig, highlight_orig=hl_orig, text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh, translation="own",
                status="draft", checked=f"{site} Wikisource, {title}{note}, {DATE}")

from datafile import drop_entries
RU = lambda t: ws.url("ru", t)
T_RES = "Воскресение (Толстой)/Часть III/Глава I"
T_SIB = "Из Сибири (Чехов)"
T_RUD = "Во глубине сибирских руд (Пушкин)"
T_MAK = "Сон Макара (Короленко)/ПСС 1914 (ВТ:Ё)"
T_AVV = "Житие протопопа Аввакума, им самим написанное (Аввакум)"
T_DER = "Дерсу Узала/Полный текст/XXX. СМЕРТЬ ДЕРСУ"
T_CPE = "Преступление и наказание (Достоевский)/Эпилог/I"
T_MS2 = "Michel Strogoff/Partie 2/Chapitre 10"
RW, FW = "Russian", "French"
GAPPED = " (a gap marked …)"

books = [
    BK("from-siberia", "From Siberia", "寄自西伯利亚", "Из Сибири", "Anton Chekhov", "安东·契诃夫", "Антон Чехов", "1890", src=RU(T_SIB),
       aliases=["Across Siberia", "Chekhov in Siberia", "Yenisei", "西伯利亚行"]),
    BK("in-the-depths-of-siberian-mines", "Message to Siberia", "致西伯利亚的囚徒", "Во глубине сибирских руд", "Alexander Pushkin", "亚历山大·普希金", "Александр Пушкин", "1827",
       src=RU(T_RUD), aliases=["In the depths of Siberian mines", "Decembrists", "十二月党人", "在西伯利亚矿坑的深处"]),
    BK("makars-dream", "Makar's Dream", "马卡尔的梦", "Сон Макара", "Vladimir Korolenko", "弗拉基米尔·柯罗连科", "Владимир Короленко", "1885", src=RU("Сон Макара (Короленко)"),
       aliases=["Korolenko", "Yakutia", "Chalgan", "柯罗连科"]),
    BK("zima-junction", "Zima Junction", "济马站", "Станция Зима", "Yevgeny Yevtushenko", "叶夫根尼·叶夫图申科", "Евгений Евтушенко", "1956", pd=False,
       aliases=["Winter Station", "Yevtushenko", "Stantsiya Zima", "叶甫图申科"]),
    BK("dream-in-polar-fog", "A Dream in Polar Fog", "雾中的梦", "Сон в начале тумана", "Yuri Rytkheu", "尤里·雷特海乌", "Юрий Рытхэу", "1970", pd=False,
       aliases=["Rytkheu", "Chukotka", "John MacLennan", "楚科奇"]),
    BK("little-humpbacked-horse", "The Little Humpbacked Horse", "小驼马", "Конёк-Горбунок", "Pyotr Yershov", "彼得·叶尔绍夫", "Пётр Ершов", "1834",
       aliases=["Konyok-Gorbunok", "Yershov", "Ershov", "Ivan the Fool", "神驼马"]),
]

places = [
    ORIG("ru-tomsk", "Tomsk", "托木斯克",
         "Tomsk was a main stage of the convict road into Siberia: convicts were brought this far by rail and river barge, and from here the parties went on eastwards on foot. Half of Resurrection is this road. In Part 3 Maslova's party has already walked from Tomsk for weeks, with Nekhlyudov following in a hired carriage",
         "托木斯克是流放犯进入西伯利亚的主要站点之一：犯人们坐火车和驳船被运到这里，再从这里一队队徒步向东走去。《复活》有一半篇幅写的就是这条路：第三部开始时，玛丝洛娃所在的那一队已经从托木斯克走了好几个星期，聂赫留朵夫坐着雇来的马车跟在后面"),
    ORIG("ru-yenisei-krasnoyarsk", "The Yenisei at Krasnoyarsk", "克拉斯诺亚尔斯克的叶尼塞河",
         "Chekhov crossed Siberia by carriage in the spring of 1890 on his way to Sakhalin and sent travel sketches to a Petersburg newspaper. The last of them is about the Yenisei, which he reached at Krasnoyarsk",
         "1890 年春天，契诃夫坐马车横穿西伯利亚前往萨哈林，一路给彼得堡的报纸寄旅途随笔。最后一篇写的是叶尼塞河，他是在克拉斯诺亚尔斯克见到这条河的"),
    ORIG("ru-chita-decembrists", "Decembrists' Church, Chita", "十二月党人教堂，赤塔",
         "From 1827 to 1830 the Decembrists condemned to hard labour were held together in a stockade at Chita. Pushkin's poem to them was carried here in 1827 by Alexandra Muravyova, who was following her husband into exile. The wooden church where the prisoners and their wives prayed is a museum of the Decembrists",
         "1827 年到 1830 年，被判服苦役的十二月党人集中关押在赤塔的栅栏监狱里。普希金写给他们的这首诗，是 1827 年由追随丈夫流放的亚历山德拉·穆拉维约娃带到这里的。囚徒和他们的妻子做祷告的那座木教堂，今为十二月党人博物馆"),
    PROTO("ru-amga", "Amga ('Chalgan')", "阿姆加（“恰尔甘”）",
          "The settlement on the Amga river, east of Yakutsk, where Korolenko spent three years of exile from 1881 to 1884. He wrote the story here, and its settlement of Chalgan is Amga",
          "雅库茨克以东阿姆加河畔的村落，柯罗连科 1881 年到 1884 年在这里度过了三年流放生活。这篇小说写于此地，小说里的恰尔甘村就是阿姆加"),
    ORIG("ru-baikal", "Lake Baikal", "贝加尔湖",
         "The deepest lake in the world. The archpriest Avvakum, exiled to Dauria with his family, crossed it twice by boat and nearly drowned in it; his Life describes the fishermen who welcomed him on its shore on the way home. Two centuries later Jules Verne brought his courier of the Tsar across it on a raft",
         "世界上最深的湖。大司祭阿瓦库姆全家被流放到达斡尔地区，两次乘船横渡贝加尔湖，差点淹死在湖里；他的《行传》写到回程时在湖边迎接他的渔夫们。两个世纪以后，凡尔纳让他那位沙皇的信使乘木筏渡过了这个湖"),
    ORIG("ru-korfovsky", "Korfovsky (Dersu Uzala's grave)", "科尔福夫斯基（德尔苏·乌扎拉之墓）",
         "The railway settlement south of Khabarovsk, at the foot of the Khekhtsir range. In March 1908 the old hunter Dersu, on his way back from the town to the taiga, was murdered near the station; Arsenyev buried him in the forest and could not find the grave again two years later. A monument to Dersu stands in the settlement",
         "哈巴罗夫斯克以南、赫赫齐尔山脚下的铁路小镇。1908 年 3 月，老猎人德尔苏离开城市返回森林途中，在车站附近被人杀害；阿尔谢尼耶夫把他葬在林中，两年后再来已找不到墓。镇上立有一座德尔苏纪念碑"),
    ORIG("ru-zima", "Zima", "济马",
         "A station town on the Trans-Siberian railway west of Irkutsk. Yevtushenko was born here, by most accounts, and spent his childhood here; the long poem that made his name is about coming back to it from Moscow after Stalin's death",
         "西伯利亚大铁路上伊尔库茨克以西的车站小城。一般认为叶夫图申科生于此地，并在这里度过童年；让他成名的那首长诗写的就是斯大林死后他从莫斯科回到这里"),
    PIL("ru-anadyr", "Anadyr", "阿纳德尔",
        "The capital of Chukotka. Yuri Rytkheu, the first Chukchi novelist, was born in 1930 at Uelen on the Bering Strait, the easternmost village of Eurasia; it lies beyond the edge of this map, so the pin stands in the capital of his people's land. His books are set in villages on that coast",
        "楚科奇的首府。第一位楚科奇族小说家尤里·雷特海乌 1930 年生于白令海峡边的乌厄连，那是欧亚大陆最东端的村庄；它落在这张地图的边界之外，所以图钉标在他故土的首府。他的书写的都是那片海岸上的村子",
        ["dream-in-polar-fog"]),
    PIL("ru-tobolsk", "Tobolsk Kremlin", "托博尔斯克克里姆林",
        "The white stone kremlin of the old capital of Siberia. Pyotr Yershov, who wrote The Little Humpbacked Horse as a nineteen-year-old student in St Petersburg, came back to Tobolsk in 1836, taught at its gymnasium and later ran it, and is buried in the town",
        "西伯利亚旧首府的白石克里姆林。彼得·叶尔绍夫十九岁在圣彼得堡读大学时写出了《小驼马》，1836 年回到托博尔斯克，在当地的中学教书，后来当了校长，死后也葬在这座城里",
        ["little-humpbacked-horse"]),
    ORIG("ru-angara", "The Angara (mouth, at the Yenisei)", "安加拉河（汇入叶尼塞河处）",
         "Most of Zuleikha is set not in Tatarstan but on the Angara, where the deported 'kulaks' are put ashore in 1930 and build the settlement of Semruk. The settlement is invented, so the pin stands at the mouth of the river, where the barges from Krasnoyarsk turned into it",
         "《祖列伊哈睁开了眼睛》的大部分篇幅不在鞑靼斯坦，而在安加拉河上：1930 年被流放的“富农”们在这里被赶下船，建起了谢姆鲁克村。这个村子是虚构的，所以图钉标在安加拉河口，从克拉斯诺亚尔斯克来的驳船就是从这里拐进安加拉河的"),
    PROTO("ru-atalanka", "Atalanka", "阿塔兰卡",
          "Valentin Rasputin grew up in this village on the Angara. When the Bratsk dam flooded the valley in the 1960s the old village went under water and was rebuilt higher up the bank, the experience behind Farewell to Matyora",
          "瓦连京·拉斯普京在安加拉河畔的这个村子长大。1960 年代布拉茨克水电站蓄水淹没河谷，老村沉入水底，在更高的岸上重建——《告别马焦拉》写的就是这段经历"),
]

lines = [
    Q("res-tomsk-1", "resurrection-tolstoy", "ru-tomsk", "Part 3, chapter 1", "第三部第一章", RW, T_RES,
      raw(T_RES, "Партия, с которой шла Маслова, прошла около пяти тысяч верст.", "около пяти тысяч верст.") + GAP
      + raw(T_RES, "Помещаться на этапах Масловой разрешено было", "от самого Томска."), ["Томска"],
      "The party with which Maslova was travelling had covered about five thousand versts.\n…\nAt the halting stations Maslova was allowed to be lodged with the politicals, but as a healthy woman she had to walk with the criminals. So she had walked all the way from Tomsk.",
      ["Tomsk"],
      "玛丝洛娃所在的那一队犯人已经走了将近五千俄里。\n…\n在各个驿站上，玛丝洛娃获准同政治犯住在一起，可是她身体健康，走路时必须同刑事犯在一起。从托木斯克起，她就一直这样走着。",
      ["托木斯克"], note=GAPPED),
    Q("sib-1", "from-siberia", "ru-yenisei-krasnoyarsk", "Sketch IX", "第九篇", RW, T_SIB,
      raw(T_SIB, "Не в обиду будь сказано ревнивым почитателям Волги", "свои силы и молодость."), ["Енисея", "Енисей"],
      "Let it be said without offence to the jealous admirers of the Volga: in all my life I have never seen a river more magnificent than the Yenisei. The Volga may be a dressed-up, modest, melancholy beauty, but the Yenisei is a mighty, raging giant who does not know what to do with his strength and youth.",
      ["Yenisei"],
      "请伏尔加河那些爱吃醋的崇拜者不要见怪：我这辈子没有见过比叶尼塞河更壮丽的河。就算伏尔加河是一位盛装的、朴素的、忧郁的美人，叶尼塞河却是一个强壮而狂暴的勇士，不知道该把自己的力气和青春往哪里使。",
      ["叶尼塞河"]),
    Q("rud-1", "in-the-depths-of-siberian-mines", "ru-chita-decembrists", "Stanza 1", "第一节", RW, T_RUD,
      raw(T_RUD, "Во глубине сибирских руд\nХраните", "И дум высокое стремленье."), ["сибирских руд"],
      "Deep in the mines of Siberia\nkeep your proud patience;\nyour grievous toil will not be lost,\nnor the high striving of your thoughts.",
      ["mines of Siberia"],
      "在西伯利亚矿坑的深处，\n请保持你们高傲的忍耐，\n你们沉痛的劳役不会落空，\n思想的崇高追求也不会徒然。",
      ["西伯利亚矿坑"]),
    Q("mak-1", "makars-dream", "ru-amga", "Chapter 1", "第一章", RW, T_MAK,
      raw(T_MAK, "Его родина — глухая слободка Чалган", "они не унывали."), ["слободка Чалган"],
      "His home, the remote little settlement of Chalgan, lay lost in the far Yakut taiga. Makar's fathers and grandfathers had won from the taiga a patch of frozen earth, and although the sullen forest still stood all round like a hostile wall, they did not lose heart.",
      ["settlement of Chalgan"],
      "他的家乡——偏僻的小村恰尔甘——湮没在遥远的雅库特原始森林里。马卡尔的父辈和祖辈从森林手里夺下了一小块冻土，尽管阴沉的密林仍像一堵敌意的墙围在四周，他们并不灰心。",
      ["小村恰尔甘"]),
    Q("avv-bk1", "life-of-avvakum", "ru-baikal", "The return from Dauria", "从达斡尔返回途中", RW, T_AVV,
      raw(T_AVV, "Поехали из Даур, стало пищи скудать", "глядя на нас, а мы на них."), ["Байкалова моря"],
      "We set out from Dauria, and food began to run short, and with the brethren we prayed to God, and Christ gave us a great stag, a huge beast, and on that we floated as far as the Baikal sea. By the sea we came upon a band of Russians, sable hunters, catching fish; glad they were to see us, the dear souls, and Terentyushko and his comrades seized us, boat and all, out of the sea and carried us far up the hill; they wept, the dear souls, looking at us, and we at them.",
      ["Baikal sea"],
      "我们从达斡尔动身，粮食渐渐不够了，我同弟兄们向上帝祈祷，基督赐给我们一头马鹿，好大的一头野兽——靠着它，我们一路漂到了贝加尔海。在海边遇上一伙俄罗斯人，是捕貂的，正在打鱼；这些好人见了我们真高兴，捷连季和他的伙伴们把我们连人带船从海里抬起来，远远地抬到山坡上；这些好人看着我们直哭，我们看着他们也哭。",
      ["贝加尔海"]),
    Q("der-kf1", "dersu-uzala", "ru-korfovsky", "Chapter 30, 'The Death of Dersu'", "第三十章《德尔苏之死》", RW, T_DER,
      raw(T_DER, "В 1910 году, зимой, я вернулся в Хабаровск", "но напрасно…"), ["станцию Корфовскую"],
      "In the winter of 1910 I returned to Khabarovsk and went at once to Korfovskaya station to visit the grave that was dear to me. I did not recognise the place; everything had changed: a whole settlement had sprung up round the station, granite quarries had been opened in the foothills of the Khekhtsir, timber was being felled and sleepers cut. I. A. Dzyul and I set about looking for Dersu's grave several times, but in vain…",
      ["Korfovskaya station"],
      "1910 年冬天，我回到哈巴罗夫斯克，立刻赶往科尔福夫斯卡亚车站，去看那座我珍爱的坟墓。我认不出那个地方了——一切都变了：车站四周冒出了整整一个村镇，赫赫齐尔山脚下开了花岗岩采石场，人们在伐木、备枕木。我和伊·阿·久尔几次动手寻找德尔苏的墓，却都是徒劳……",
      ["科尔福夫斯卡亚车站"]),
    Q("cp-ep1", "crime-and-punishment", "ru-omsk-fortress", "Epilogue, chapter 1", "尾声第一章", RW, T_CPE,
      flow(raw(T_CPE, "Сибирь.", "в  крепости  острог.")), ["Сибирь"],
      "Siberia. On the bank of a broad, deserted river stands a town, one of the administrative centres of Russia; in the town there is a fortress, in the fortress a prison.",
      ["Siberia"],
      "西伯利亚。在一条宽阔而荒凉的大河岸上，有一座城，是俄国的行政中心之一；城里有一座要塞，要塞里有一座监狱。",
      ["西伯利亚"], note=" (hard-wrapped lines joined, doubled spaces written as one)"),
    Q("ms-bk1", "michael-strogoff", "ru-baikal", "Part 2, chapter 10", "第二部第十章", FW, T_MS2,
      raw(T_MS2, "Cet immense bassin d’eau douce", "en amont de la ville d’Yeniseïsk.", "fr"), ["l’Angara", "Irkoutsk"],
      "This immense basin of fresh water, fed by more than three hundred rivers, is framed in a magnificent circle of volcanic mountains. It has no other outlet than the Angara, which, after passing Irkutsk, goes on to join the Yenisei a little above the town of Yeniseisk.",
      ["Angara", "Irkutsk"],
      "这片巨大的淡水湖由三百多条河流注入，四周环绕着一圈壮丽的火山山脉。它唯一的出口是安加拉河，河水流过伊尔库茨克之后，在叶尼塞斯克城上游不远处汇入叶尼塞河。",
      ["安加拉河", "伊尔库茨克"]),
    S("zima-s1", "zima-junction", "ru-zima", "The whole poem", "全诗",
      "At twenty the poet takes the train home from Moscow to the Siberian station town for the first time in years. He goes berry-picking with his cousins, listens to his uncles argue about what has gone wrong in the country, meets a woman on a hayloft and a drunk who was once somebody, and leaves with the station's own voice telling him to go on searching and not to lose heart.",
      "二十岁的诗人多年来第一次从莫斯科坐火车回到西伯利亚的车站小城。他同表兄弟姐妹去采浆果，听舅舅们争论国家到底出了什么毛病，在干草棚上遇见一个女人，又遇见一个从前有头有脸的醉汉；临走时，车站用它自己的声音嘱咐他继续寻找，不要灰心。",
      ["the Siberian station town"], ["西伯利亚的车站小城"], W + "Yevgeny_Yevtushenko"),
    S("rytk-s1", "dream-in-polar-fog", "ru-anadyr", "The whole novel", "全书",
      "A Canadian sailor, John MacLennan, is badly injured aboard a ship off the Chukchi coast, and Chukchi hunters take him by sledge to their village, where his life is saved. The ship sails without him, and he stays, marries and learns to live as one of the village.",
      "加拿大水手约翰·麦克伦南在楚科奇海岸外的一艘船上受了重伤，楚科奇猎人用雪橇把他送到自己的村子，救了他的命。船没有等他就开走了，他留了下来，成了家，学会像村里人一样生活。",
      ["the Chukchi coast"], ["楚科奇海岸"], W + "Yuri_Rytkheu"),
    S("zul-s2", "zuleikha", "ru-angara", "Parts 2–4", "第二至第四部",
      "After months in a cattle wagon and a barge that sinks under them, some thirty survivors are put ashore on the empty bank of the Angara at the start of winter with one commandant, the Red Army man who shot Zuleikha's husband. She gives birth to a son, learns to hunt, and over sixteen years the dugout becomes the settlement of Semruk.",
      "在闷罐车里熬了几个月、乘坐的驳船又沉没之后，三十来个幸存者在入冬时被丢在安加拉河荒无人烟的岸上，身边只有一个管制员——就是开枪打死祖列伊哈丈夫的那个红军战士。她生下一个儿子，学会了打猎；十六年里，那个地窝子变成了谢姆鲁克村。",
      ["the Angara"], ["安加拉河"], W + "Zuleikha_(novel)"),
    S("mat-s2", "farewell-to-matyora", "ru-atalanka", "The whole novel", "全书",
      "In its last summer the island village is cleared for the reservoir: the graveyard crosses are pulled up by strangers, the young burn their own houses for the compensation, and old Darya whitewashes her hut one last time before it is set alight. She and a few other old people are still on the island when the fog comes down and the boat sent for them loses its way.",
      "在最后一个夏天，岛上的村子要为水库让路：墓地的十字架被外人拔掉，年轻人为了领补偿烧掉自家的房子，老达丽娅在木屋被点燃之前最后一次把它粉刷了一遍。大雾降下来的时候，她和另外几个老人还留在岛上，来接他们的船在雾里迷了路。",
      ["the island village"], ["岛上的村子"], W + "Farewell_to_Matyora"),
]

ids = lambda name: set(re.findall(r'\{ id: "([^"]+)"', open(b.data(name), encoding="utf-8").read()))
old_books, old_places, old_lines = ids("books.js"), ids("places.js"), ids("lines.js")
new_b, new_p, new_l = {x["id"] for x in books}, {x["id"] for x in places}, {x["id"] for x in lines}
assert not new_b & old_books and not new_p & old_places and not new_l & old_lines, (new_b & old_books, new_p & old_places, new_l & old_lines)
assert new_p == set(CO), new_p ^ set(CO)
bids, pids = new_b | old_books, new_p | old_places
for l in lines:
    assert l["book_id"] in bids and all(p in pids for p in l["place_ids"]), l["id"]
used = {p for l in lines for p in l["place_ids"]}
for p in places:
    assert p["id"] in used or p.get("book_ids"), p["id"]
covered = {l["book_id"] for l in lines} | {i for p in places for i in p.get("book_ids", [])}
assert not new_b - covered, new_b - covered

if __name__ == "__main__":
    # Resurrection moves from Butyrka to the Siberian road: the old scene note goes, the prison keeps the book as a prototype
    drop_entries(b.data("lines.js"), ["res-s1"])
    f = b.data("places.js"); s = open(f, encoding="utf-8").read()
    a = '{ id: "ru-butyrka", country: "ru", '
    assert s.count(a) == 1 and 'id: "ru-butyrka", country: "ru", book_ids' not in s
    open(f, "w", encoding="utf-8").write(s.replace(a, a + 'book_ids: ["resurrection-tolstoy"], '))
    M = "11-23: fifth pack, Siberia and the Far East (tools/content/batches/add_ru5.py)"
    b.append(b.data("books.js"), books, M)
    b.append(b.data("places.js"), places, M)
    b.append(b.data("lines.js"), lines, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
