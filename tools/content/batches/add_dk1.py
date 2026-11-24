"""11-23: Denmark, first pack: 25 new books and Hamlet (already on the UK list), 24 places.
Andersen's Denmark (Kronborg, Børglum, the Silkeborg woods, Odense), Jacobsen and Blicher at Tjele, Pontoppidan,
Johannes V. Jensen, Holberg, Oehlenschläger's golden horns, Kierkegaard and Blixen, Bang's Als in 1864, Nexø's
Bornholm, Wollstonecraft in Copenhagen after the fire of 1795, Beowulf at Lejre, and the modern Copenhagen of
Ditlevsen and Høeg. Fictional settings hang on the real place the book names or is drawn from, and the note says which.

Quotations (10 lines) are cut from Wikisource pages (tools/content/wikisource.py): Danish and English Wikisource;
translations of the Danish are our own drafts (translation: "own"). Books in copyright, and PD books whose text we
could not reach, have scene notes in our own words or hang on a writer's place. What a cut changes, named in
`checked`: hard-wrapped lines are re-flowed (paragraphs kept); in Hamlet the editor's brackets round the place
heading and his line numbers are left out.

Coordinates are those of the place's Danish (once English) Wikipedia article (cache/dk/coords.json).

Usage: python3 -I add_dk1.py <app_dir> <coords.json> <wikisource_root>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-23"
b.init(APP, "", "dk", DATE)
W = b.W
DAW = "https://da.wikipedia.org/wiki/"
GAP = b.GAP

def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, pd=True, **kw):
    d = dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
             orig_lang=kw.pop("lang", "da"), public_domain=pd, source_url=kw.pop("src", None), author_orig=author_orig)
    d.update(kw)
    return {k: v for k, v in d.items() if v is not None or k == "source_url"}

def C(pid):
    c = CO[pid]
    return c["lat"], c["lon"], c["st"], c["su"]

def ORIG(pid, name, zh, en_note, zh_note, **kw): return b.ORIG(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PIL(pid, name, zh, en_note, zh_note, ids, **kw): return b.PIL(pid, name, zh, *C(pid), en_note, zh_note, ids, **kw)
S = b.S

def raw(title, start, end, lang="da"):
    t = ws.text(os.path.join(WSR, lang), title)
    n = re.sub("[\xa0   ]", " ", t)
    i = n.find(start)
    assert i >= 0, (title, start)
    j = n.find(end, i)
    assert j >= 0, (title, start, end)
    return t[i:j + len(end)]

def flow(s):
    """a hard-wrapped paragraph: lines joined, doubled spaces written as one"""
    return re.sub(r" {2,}", " ", s.replace("\n", " "))

def Q(id, book, place, loc, loc_zh, title, orig, hl_orig, en, hl_en, zh, hl_zh, note=""):
    if re.search("[\xa0   ]", orig):
        orig = re.sub("[\xa0   ]+", " ", orig)
        note += " (no-break spaces written as plain spaces)"
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls:
            assert h in text, (id, h)
    assert "  " not in orig and "[" not in orig, (id, "spacing or page mark")
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh,
                text_orig=orig, highlight_orig=hl_orig, text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh, translation="own",
                status="draft", checked=f"Danish Wikisource, {title}{note}, {DATE}")

def EN(id, book, place, loc, loc_zh, title, text, hl, zh, hl_zh, note=""):
    assert "[" not in text and "]" not in text and "\xa0" not in text and "  " not in text, (id, text[:40])
    for h in hl: assert h in text, (id, h)
    for h in hl_zh: assert h in zh, (id, h)
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh, text_en=text, highlight_en=hl, translation="original",
                text_zh=zh, highlight_zh=hl_zh, status="draft", checked=f"English Wikisource, {title}{note}, {DATE}")

AND = ("Hans Christian Andersen", "安徒生", "H.C. Andersen")
HOL = ("Ludvig Holberg", "霍尔堡", "Ludvig Holberg")
JPJ = ("J. P. Jacobsen", "延斯·彼得·雅各布森", "Jens Peter Jacobsen")
T_HOL, T_BOR, T_IB, T_BELL = "Holger Danske", "Bispen paa Børglum og hans Frænde", "Ib og lille Christine", "Klokkedybet"
T_GRU = "Fru Marie Grubbe. Interieurer fra det syttende Aarhundrede./1"
T_DEGN, T_PER, T_KF = "Brudstykker af en Landsbydegns Dagbog", "Lykke-Per/1", "Kongens Fald/2"
T_HAM = "Hamlet (1917) Yale/Text/Act I"
T_WOLL = "Letters Written during a Short Residence in Sweden, Norway, and Denmark/Letter XVIII"
HAMLET = "hamlet"
EXIST = {HAMLET}

books = [
    BK("holger-danske", "Holger the Dane", "丹麦人荷尔格", "Holger Danske", *AND, "1845", src=ws.url("da", T_HOL),
       aliases=["Holger Danske", "Ogier the Dane", "Kronborg", "Andersen"]),
    BK("bishop-of-borglum", "The Bishop of Børglum and His Kinsman", "博尔格隆的主教和他的亲族", "Bispen paa Børglum og hans Frænde", *AND, "1861",
       src=ws.url("da", T_BOR), aliases=["The Bishop of Börglum and his Men", "Børglum Kloster", "Andersen"]),
    BK("ib-and-christine", "Ib and Little Christine", "依卜和小克丽斯玎", "Ib og lille Christine", *AND, "1855", src=ws.url("da", T_IB),
       aliases=["Ib and Christine", "Gudenå", "Silkeborg", "Andersen"]),
    BK("the-bell-deep", "The Bell Deep", "钟渊", "Klokkedybet", *AND, "1856", src=ws.url("da", T_BELL),
       aliases=["Klokkedybet", "The Bell-Deep", "Odense Å", "Andersen"]),
    BK("little-mermaid", "The Little Mermaid", "小美人鱼", "Den lille Havfrue", *AND, "1837", src=ws.url("da", "Den lille Havfrue"),
       aliases=["Den lille Havfrue", "海的女儿", "Langelinie", "Andersen"]),
    BK("ugly-duckling", "The Ugly Duckling", "丑小鸭", "Den grimme Ælling", *AND, "1843", src=ws.url("da", "Den grimme Ælling"),
       aliases=["Den grimme Ælling", "Andersen", "Odense"]),
    BK("fairy-tale-of-my-life", "The Fairy Tale of My Life", "我的童话人生", "Mit Livs Eventyr", *AND, "1855",
       aliases=["Mit Livs Eventyr", "The True Story of My Life", "Andersen autobiography", "安徒生自传"]),
    BK("golden-horns", "The Golden Horns", "金角", "Guldhornene", "Adam Oehlenschläger", "奥伦施莱厄", "Adam Oehlenschläger", "1802",
       src=ws.url("da", "Guldhornene"), aliases=["Guldhornene", "Gallehus", "Oehlenschläger"]),
    BK("marie-grubbe", "Marie Grubbe", "玛丽·格鲁贝", "Fru Marie Grubbe", *JPJ, "1876",
       src=ws.url("da", "Fru Marie Grubbe. Interieurer fra det syttende Aarhundrede."), aliases=["Fru Marie Grubbe", "Tjele", "Jacobsen"]),
    BK("village-clerks-diary", "The Diary of a Parish Clerk", "乡村执事日记片段", "Brudstykker af en Landsbydegns Dagbog", "Steen Steensen Blicher",
       "布利克", "Steen Steensen Blicher", "1824", src=ws.url("da", T_DEGN),
       aliases=["Brudstykker af en Landsbydegns Dagbog", "Landsbydegnens Dagbog", "Morten Vinge", "Blicher", "Tjele"]),
    BK("lucky-per", "Lucky Per", "幸运的彼尔", "Lykke-Per", "Henrik Pontoppidan", "彭托皮丹", "Henrik Pontoppidan", "1898–1904",
       src=ws.url("da", "Lykke-Per"), aliases=["Lykke-Per", "Per Sidenius", "Pontoppidan", "幸运儿彼尔"]),
    BK("fall-of-the-king", "The Fall of the King", "国王的没落", "Kongens Fald", "Johannes V. Jensen", "约翰内斯·延森", "Johannes V. Jensen", "1900–1901",
       src=ws.url("da", "Kongens Fald"), aliases=["Kongens Fald", "Mikkel Thøgersen", "Christian II", "J. V. Jensen"]),
    BK("wollstonecraft-letters", "Letters Written in Sweden, Norway, and Denmark", "瑞典、挪威和丹麦短居书简", None, "Mary Wollstonecraft",
       "玛丽·沃斯通克拉夫特", "Mary Wollstonecraft", "1796", lang="en",
       src=ws.url("en", "Letters Written during a Short Residence in Sweden, Norway, and Denmark"),
       aliases=["Letters Written During a Short Residence in Sweden, Norway, and Denmark", "Wollstonecraft", "Scandinavian letters"]),
    BK("pelle-the-conqueror", "Pelle the Conqueror", "征服者佩勒", "Pelle Erobreren", "Martin Andersen Nexø", "马丁·安德森·尼克索",
       "Martin Andersen Nexø", "1906–1910", aliases=["Pelle Erobreren", "Lasse", "Bornholm", "Nexø"]),
    BK("smillas-sense-of-snow", "Smilla's Sense of Snow", "斯米拉小姐的雪感", "Frøken Smillas fornemmelse for sne", "Peter Høeg", "彼得·赫格",
       "Peter Høeg", "1992", pd=False, aliases=["Miss Smilla's Feeling for Snow", "Frøken Smillas fornemmelse for sne", "Christianshavn", "Isaiah"]),
    BK("copenhagen-trilogy", "The Copenhagen Trilogy", "哥本哈根三部曲", "Barndom · Ungdom · Gift", "Tove Ditlevsen", "托芙·迪特莱弗森", "Tove Ditlevsen",
       "1967–1971", pd=False, aliases=["Childhood", "Youth", "Dependency", "Barndom", "Ungdom", "Gift", "Vesterbro", "Hedebygade"]),
    BK("out-of-africa", "Out of Africa", "走出非洲", None, "Karen Blixen", "凯伦·布里克森", "Karen Blixen", "1937", lang="en", pd=False,
       aliases=["Den afrikanske Farm", "Isak Dinesen", "Rungstedlund", "Ngong"]),
    BK("either-or", "Either/Or", "非此即彼", "Enten – Eller", "Søren Kierkegaard", "克尔凯郭尔", "Søren Kierkegaard", "1843",
       aliases=["Enten-Eller", "Victor Eremita", "Kierkegaard"]),
    BK("jeppe-on-the-hill", "Jeppe on the Hill", "山上的耶珀", "Jeppe paa Bierget", *HOL, "1722",
       aliases=["Jeppe på Bjerget", "The Transformed Peasant", "Holberg"]),
    BK("peder-paars", "Peder Paars", "彼泽·帕尔斯", "Peder Paars", *HOL, "1719–1720", aliases=["Holberg", "Anholt", "Kalundborg"]),
    BK("niels-lyhne", "Niels Lyhne", "尼尔斯·伦奈", "Niels Lyhne", *JPJ, "1880", aliases=["Jacobsen", "Thisted"]),
    BK("we-the-drowned", "We, the Drowned", "我们这些溺水的人", "Vi, de druknede", "Carsten Jensen", "卡斯滕·延森", "Carsten Jensen", "2006", pd=False,
       aliases=["Vi, de druknede", "Marstal", "Laurids Madsen"]),
    BK("tine", "Tine", "蒂娜", "Tine", "Herman Bang", "赫尔曼·邦", "Herman Bang", "1889", aliases=["Herman Bang", "Als", "1864", "Dybbøl"]),
    BK("ordet", "The Word", "言语", "Ordet", "Kaj Munk", "凯·蒙克", "Kaj Munk", "1925", aliases=["Ordet", "Kaj Munk", "Vedersø", "Dreyer"]),
    BK("beowulf", "Beowulf", "贝奥武甫", "Beowulf", "Anonymous", "佚名", "Anonymous", "c. 700–1000", lang="ang",
       aliases=["Heorot", "Hrothgar", "Grendel", "Lejre", "贝奥武夫"]),
]

places = [
    ORIG("dk-kronborg", "Kronborg Castle, Helsingør", "克伦堡宫，赫尔辛格",
         "The Renaissance castle on the point at Helsingør that guards the narrow entrance to the Øresund; Frederick II rebuilt the medieval fortress here in 1574–1585. Shakespeare set Hamlet in the castle at 'Elsinore', the English name for Helsingør. In Andersen's tale Holger the Dane sleeps in its cellars, and a statue of him by H. P. Pedersen-Dan has sat in the casemates since 1907",
         "赫尔辛格海角上的文艺复兴式宫堡，扼守厄勒海峡狭窄的入口；弗雷德里克二世在 1574—1585 年间把这里的中世纪要塞改建成了宫殿。莎士比亚把《哈姆雷特》放在“埃尔西诺”——赫尔辛格的英文名——的城堡里。在安徒生的故事里，丹麦人荷尔格就睡在它的地窖中；1907 年起，城堡的地下暗堡里坐着一尊佩德森-丹雕刻的荷尔格像"),
    ORIG("dk-borglum", "Børglum Abbey", "博尔格隆修道院",
         "The former abbey on a high hill of sand in Vendsyssel, some 5 km east of Løkken. It was the seat of the bishops of Børglum and belonged to the Premonstratensian canons until the Reformation of 1536. Andersen's story takes the reader up to it on a light summer night, and back to the quarrels of a medieval bishop",
         "日德兰北部文叙瑟尔地区一座高高的沙丘上的旧修道院，在勒肯以东约 5 公里。这里曾是博尔格隆主教的驻地，直到 1536 年宗教改革前一直属于普雷蒙特雷修会。安徒生的故事在一个白夜把读者领上山来，又领回到一位中世纪主教的纷争中去"),
    ORIG("dk-silkeborg", "The Silkeborg woods by the Gudenå", "古曾河畔的锡尔克堡森林",
         "The great woods round Silkeborg on the river Gudenå in central Jutland. Ib and Little Christine begins at a poor farm under a ridge in these woods, where Ib's father carves clogs in winter",
         "日德兰中部古曾河畔锡尔克堡四周的大森林。《依卜和小克丽斯玎》从这片森林里一道土岗下的穷农舍开始，依卜的父亲冬天在那里削木鞋"),
    ORIG("dk-munkemose", "Munke Mose, Odense (the Bell Deep)", "蒙克莫瑟公园，欧登塞（钟渊）",
         "The park on the Odense river below the old town. In 'The Bell Deep' Andersen names the willows on the Munkemose side and puts the river's deepest spot off the old convent, where the river-man lives with the church bell that once flew out of St Alban's tower; the story, he wrote, grew from Odense's own folk belief",
         "欧登塞老城下方奥登塞河边的公园。在《钟渊》里，安徒生写到了蒙克莫瑟这边的柳树，又把河里最深的地方放在旧修道院对面：河人就住在那里，陪着那口当年从圣阿尔班教堂钟楼里飞出来的大钟。他说，这个故事来自欧登塞本地的民间传说"),
    PIL("dk-andersen-hus", "H. C. Andersen's House, Odense", "安徒生故居，欧登塞",
        "The corner house in Odense's old quarter that is officially regarded as Hans Christian Andersen's birthplace, although the records of his birth in 1805 do not prove it. The town bought it in 1905, a hundred years after his birth, and it became the museum of his life and work",
        "欧登塞老城区的一座街角小屋，官方认定是安徒生 1805 年出生的地方，不过他出生时的记录并不能证明这一点。1905 年，安徒生诞辰一百周年时，市政府买下了它，后来成了介绍他生平和作品的博物馆",
        ["ugly-duckling", "fairy-tale-of-my-life"]),
    PIL("dk-little-mermaid", "The Little Mermaid, Langelinie", "小美人鱼像，长堤公园",
        "Edvard Eriksen's bronze of Andersen's little mermaid, a gift from the brewer Carl Jacobsen, set on the rocks at Langelinie in Copenhagen harbour on 23 August 1913; Eriksen's wife Eline was his model",
        "爱德华·埃里克森为安徒生的小美人鱼铸的铜像，由酿酒商卡尔·雅各布森捐赠，1913 年 8 月 23 日安放在哥本哈根港长堤公园的岩石上；埃里克森的妻子埃莉娜是他的模特",
        ["little-mermaid"]),
    PIL("dk-gallehus", "Gallehus", "加勒胡斯",
        "Hamlet near Møgeltønder in South Jutland where the two golden horns were found, in 1639 and 1734. They were stolen and melted down in 1802; Oehlenschläger's poem about them made them a symbol of Danish national romanticism",
        "南日德兰默格尔滕讷附近的小村，1639 年和 1734 年先后在这里发现了两只金角。1802 年金角被盗，熔化掉了；奥伦施莱厄为它们写的诗，让金角成了丹麦民族浪漫主义的象征",
        ["golden-horns"]),
    ORIG("dk-tjele", "Tjele Manor", "蒂勒庄园",
         "Manor in central Jutland near Viborg, bought in 1635 by Erik Grubbe. His youngest daughter Marie Grubbe, whose wayward life ended as the wife of a ferryman on Falster, has been retold by Holberg, Blicher, Andersen and Jacobsen. Blicher's parish clerk comes here as a servant; Jacobsen's novel opens in its garden",
         "日德兰中部维堡附近的庄园，1635 年由埃里克·格鲁贝买下。他最小的女儿玛丽·格鲁贝一生放浪不羁，最后嫁给法尔斯特岛上的一个摆渡人，霍尔堡、布利克、安徒生和雅各布森都写过她。布利克笔下的教堂执事到这里来当仆人；雅各布森的小说就从庄园的花园里开始"),
    PIL("dk-randers", "Randers", "兰讷斯",
        "Henrik Pontoppidan's family moved to Randers in 1863, when his father became priest of St Morten's Church, and lived in a large vicarage in Brødregade. Lucky Per opens in a vicarage in an unnamed small town of East Jutland",
        "1863 年，亨里克·彭托皮丹的父亲出任兰讷斯圣莫滕教堂的牧师，全家搬到这里，住在兄弟街一座宽大的牧师住宅里。《幸运的彼尔》开篇写的就是东日德兰一座没有点名的小城里的牧师之家",
        ["lucky-per"]),
    ORIG("dk-gammeltorv", "Gammeltorv, Copenhagen", "旧广场，哥本哈根",
         "Copenhagen's oldest square, the market square of the medieval town. In 'Copenhagen by Night', a chapter of The Fall of the King, the student Mikkel Thøgersen roams the town around the square, and the next morning the citizens find a cart on the ridge of a tall house facing it, put there by Prince Christiern, the future Christian II",
         "哥本哈根最古老的广场，中世纪城里的集市广场。《国王的没落》里《夜晚的哥本哈根》一章，大学生米克尔·托格森在广场一带游荡；第二天早上，市民们发现一座临广场的高房子屋脊上骑着一辆车——是王子克里斯蒂安，也就是后来的克里斯蒂安二世干的"),
    ORIG("dk-indre-by", "Copenhagen old town (Indre By)", "哥本哈根老城",
         "The old town inside the former ramparts. The great fire that began on 5 June 1795 burned much of it; Mary Wollstonecraft came that year and found the homeless still camped in tents outside the city",
         "旧城墙以内的老城区。1795 年 6 月 5 日燃起的大火烧掉了老城的一大片；玛丽·沃斯通克拉夫特那年来到这里，看见无家可归的人还住在城外的帐篷里"),
    PIL("dk-nexo", "Nexø, Bornholm", "尼克索，博恩霍尔姆岛",
        "Town on the east coast of Bornholm. Martin Andersen, born in Copenhagen in 1869, grew up on the island and took the town's name as his own. Pelle the Conqueror begins with a Swedish father and son coming over to Bornholm to work",
        "博恩霍尔姆岛东岸的小城。马丁·安德森 1869 年生于哥本哈根，在这座岛上长大，后来把这个城名加进了自己的姓里。《征服者佩勒》就从一对瑞典父子渡海来博恩霍尔姆做工开始",
        ["pelle-the-conqueror"]),
    ORIG("dk-christianshavn", "Christianshavn, Copenhagen", "克里斯蒂安港，哥本哈根",
         "The quarter of canals and warehouses on islands across the harbour from the old town. Smilla lives alone here in a dreary block of flats, and the novel opens with the death of the Greenlandic boy Isaiah, fallen from the snowy roof of their building",
         "隔着港口与老城相望、建在几座岛上的运河和仓库区。斯米拉独自住在这里一座沉闷的公寓楼里，小说开篇，格陵兰男孩以赛亚从他们那栋楼积雪的屋顶上摔下来死了"),
    ORIG("dk-hedebygade", "Hedebygade, Vesterbro", "黑德比街，韦斯特布罗",
         "Street in Vesterbro, then a poor working-class district of Copenhagen. Tove Ditlevsen grew up here in a back-house flat at no. 30; the street of her childhood runs through her memoirs and her novel Barndommens gade",
         "哥本哈根韦斯特布罗区的一条街，当年是贫穷的工人区。托芙·迪特莱弗森在这里 30 号后院楼的一套公寓里长大；她童年的这条街贯穿了她的回忆录，也成了小说《童年的街》的主题",
         ),
    PIL("dk-rungstedlund", "Rungstedlund (Karen Blixen Museum)", "伦斯泰德隆德（凯伦·布里克森博物馆）",
        "Karen Blixen's family home on the Øresund coast at Rungsted, north of Copenhagen, where she lived after her years in Kenya and died in 1962. It is now her museum and the seat of the Danish Academy, and its grounds are a bird sanctuary",
        "凯伦·布里克森家在哥本哈根以北伦斯泰德、厄勒海峡岸边的宅子。她离开肯尼亚以后住在这里，1962 年在这里去世。如今这里是她的博物馆和丹麦学院的所在地，园子是一片鸟类保护区",
        ["out-of-africa"]),
    PIL("dk-assistens", "Assistens Cemetery, Copenhagen", "协助公墓，哥本哈根",
        "Copenhagen's great nineteenth-century cemetery in Nørrebro. Søren Kierkegaard and Hans Christian Andersen are both buried here",
        "哥本哈根北桥区十九世纪的大公墓。克尔凯郭尔和安徒生都葬在这里",
        ["either-or", "fairy-tale-of-my-life"]),
    PIL("dk-soro", "Sorø Abbey Church (Holberg's tomb)", "索勒修道院教堂（霍尔堡墓）",
        "The Cistercian abbey church at Sorø, begun in 1161 under Bishop Absalon, who is buried here. Ludvig Holberg left his estates and fortune to Sorø Academy, and his marble sarcophagus stands in the church",
        "索勒的熙笃会修道院教堂，1161 年在阿布萨隆主教主持下动工，阿布萨隆本人也葬在这里。路德维·霍尔堡把自己的庄园和财产留给了索勒学院，他的大理石石棺就在教堂里",
        ["jeppe-on-the-hill"]),
    ORIG("dk-anholt", "Anholt", "安霍尔特岛",
         "Remote island in the Kattegat. In Holberg's mock-epic Peder Paars, the grocer Peder Paars sails from Kalundborg to visit his betrothed Dorothea in Aarhus; a storm wrecks him on Anholt, whose people, the poem says, live as good Christians on the wrecks",
         "卡特加特海峡中一座偏远的小岛。在霍尔堡的戏仿史诗《彼泽·帕尔斯》里，杂货商彼泽·帕尔斯从卡伦堡出海，去奥胡斯看望未婚妻多罗特娅；一场风暴让他在安霍尔特岛搁浅，诗里说，岛上的人都过着虔诚的基督徒生活，靠沉船过日子"),
    PIL("dk-thisted", "Thisted", "锡斯泰兹",
        "Market town in Thy, north-west Jutland, where J. P. Jacobsen was born in 1847 and died in 1885",
        "日德兰西北部蒂地区的集镇，延斯·彼得·雅各布森 1847 年生于此地，1885 年也在这里去世",
        ["niels-lyhne"]),
    ORIG("dk-marstal", "Marstal, Ærø", "马斯塔尔，艾尔岛",
         "Seafaring town on the island of Ærø, Carsten Jensen's home town. We, the Drowned is its chronicle, from the war of 1848 to the end of the Second World War",
         "艾尔岛上的航海小城，卡斯滕·延森的故乡。《我们这些溺水的人》就是它的编年史，从 1848 年的战争一直写到第二次世界大战结束"),
    ORIG("dk-als", "Als", "阿尔斯岛",
         "Island in South Jutland, where Herman Bang was born in 1857 at Asserballe, the son of the parish priest. Tine takes place here from February to April 1864, while the Prussians shell Dybbøl and Sønderborg",
         "南日德兰的岛屿，赫尔曼·邦 1857 年生于岛上的阿瑟巴勒，父亲是当地教区的牧师。《蒂娜》的故事就发生在 1864 年 2 月到 4 月的阿尔斯岛上，那时普鲁士军队正在炮轰迪伯尔和森讷堡"),
    PIL("dk-vederso", "Vedersø", "韦泽瑟",
        "Village in West Jutland where Kaj Munk was parish priest from 1924 until his death in January 1944. He wrote The Word here in 1925, in six days, out of what he had seen as a priest, a woman dying in childbirth",
        "日德兰西部的村子，凯·蒙克从 1924 年起在这里当教区牧师，直到 1944 年 1 月去世。1925 年，他根据自己当牧师时看到的一个妇女死于难产的经历，用六天时间在这里写出了《言语》",
        ["ordet"]),
    ORIG("dk-lejre", "Gammel Lejre", "老莱尔",
         "Village west of Roskilde where Scandinavian tradition placed the seat of the legendary Skjoldung kings. Excavations here in 1986–88 and 2004–05 uncovered great royal halls, and the place is taken to be the site of Heorot in Beowulf",
         "罗斯基勒以西的村子，斯堪的纳维亚传说认为这里是传奇的斯约尔东王族的王座所在。1986—1988 年和 2004—2005 年的考古发掘在这里发现了几座大王厅，人们认为这里就是《贝奥武甫》中鹿厅的所在地"),
]

# ---------- quotations ----------
_hol = flow(raw(T_HOL, "Der er i Danmark et gammelt Slot", "“mange Tak!”")) + GAP + flow(raw(T_HOL, "Men Pragten i det Hele", "skeer heroppe i Danmark."))
_bell = flow(raw(T_BELL, "“Ding-dang! ding-dang!”", "hen under Træbroerne.")) + GAP + flow(raw(T_BELL, "Ud for det gamle Frøken-Kloster", "Maaneskin."))
_gru = flow(raw(T_GRU, "Lyden af Slagene", "slog\nDøren i efter sig.")) + "\n" + flow(raw(T_GRU, "Det var den fjortenaarige Marie Grubbe", "til Tjele Hovedgaard."))
_degn = raw(T_DEGN, "Thiele, d. 1ste Mai 1709.", "1709.") + "\n" + flow(raw(T_DEGN, "Saa er jeg da nu Tjener", "hverken sulte eller fryse."))
lines = [
    Q("dk-hol-1", "holger-danske", "dk-kronborg", "Opening", "开篇", T_HOL, _hol, ["Kronborg"],
      "In Denmark there is an old castle called Kronborg. It stands right out on the Øresund, where the great ships sail past by the hundred every day, English, Russian and Prussian; and they salute the old castle with their cannon: 'Boom!' and the castle answers with its cannon: 'Boom!' — for that is how cannon say 'Good day!' and 'Thank you kindly!'"
      + GAP + "But the finest thing of all is the old castle of Kronborg, and under it, in the deep dark cellar where no one goes, sits Holger the Dane. He is clad in iron and steel and rests his head on his strong arms; his long beard hangs down over the marble table and has grown fast into it; he sleeps and dreams, but in his dreams he sees everything that happens up here in Denmark.",
      ["Kronborg"],
      "丹麦有一座古老的宫堡，名叫克伦堡。它就伸在厄勒海峡边上，每天都有成百艘大船从这里驶过，有英国的、俄国的、普鲁士的；它们用大炮向古堡致敬：“轰！”古堡也用大炮回答：“轰！”——大炮就是这样说“您好！”和“多谢！”的。"
      + GAP + "不过最壮观的还是古老的克伦堡，丹麦人荷尔格就坐在它底下那间谁也不去的又深又黑的地窖里。他身披铁甲，把头靠在强壮的胳膊上；他的长胡子垂在大理石桌面上，已经长进桌子里去了。他睡着，做着梦，在梦里他看得见上面丹麦发生的一切。",
      ["克伦堡"], note=" (the page's line ends joined)"),
    Q("dk-bor-1", "bishop-of-borglum", "dk-borglum", "Opening", "开篇", T_BOR,
      flow(raw(T_BOR, "Nu ere vi oppe i Jylland", "det mørkeblaa Hav.")), ["Børglum Kloster"],
      "Now we are up in Jutland, far beyond the Wild Moor; we can hear the 'Vestervovvov', hear the sea rolling, it is quite near; but in front of us rises a great hill of sand, which we have seen for a long time, and we are still driving towards it, driving slowly through the deep sand. Up on the sandhill lies a large old manor: that is Børglum Abbey, and its biggest wing is still the church. We come up there late in the evening, but the weather is clear, these are the light nights; one can see far, far all around, over field and bog down to the Aalborg Fjord, over heath and meadow, right out over the dark-blue sea.",
      ["Børglum Abbey"],
      "现在我们到了日德兰北部，远在大荒沼的那一边；我们听得见“西海呜呜”的声音，听得见海浪翻滚，它就在近旁；可是在我们前面耸起一座大沙丘，我们老早就看见它了，现在还朝着它往前赶，在深深的沙子里慢慢地走。沙丘顶上有一座古老的大庄园，那就是博尔格隆修道院，最大的一翼至今还是教堂。我们在深夜里来到上面，不过天气晴朗，正是白夜的时节；人能看得很远很远，越过田野和沼泽，一直望到奥尔堡峡湾，越过荒原和草地，直到深蓝色的大海。",
      ["博尔格隆修道院"], note=" (the page's line ends joined)"),
    Q("dk-ib-1", "ib-and-christine", "dk-silkeborg", "Opening", "开篇", T_IB,
      raw(T_IB, "Nær ved Gudenaa", "Byg-Ager."), ["Gudenaa", "Silkeborg-Skov"],
      "Close to the Gudenå, deep in the Silkeborg woods, a ridge of land rises like a great rampart; it is called 'the Ås', and below it to the west there lay — indeed there still lies — a little farmhouse with poor land; the sand shines through the thin rye and barley.",
      ["Gudenå", "Silkeborg woods"],
      "在古曾河附近，锡尔克堡森林深处，有一道土岗像一堵大围墙似的隆起，人们管它叫“奥森”；在它西面的山脚下，从前有——不，现在还有——一座小小的农舍，田地很瘠薄，沙子从稀稀落落的黑麦和大麦地里透出亮光来。",
      ["古曾河", "锡尔克堡森林"]),
    Q("dk-bell-1", "the-bell-deep", "dk-munkemose", "Opening", "开篇", T_BELL, _bell, ["Klokkedybet"],
      "'Ding-dong! Ding-dong!' it rings up from the Bell Deep in the Odense river. What river is that? Every child in Odense town knows it; it runs along below the gardens, from the lock to the water-mill, under the wooden bridges."
      + GAP + "Off the old convent is the deepest spot; it is called the Bell Deep, and there the river-man lives. He sleeps by day, when the sun shines through the water, but comes out on starry nights and in the moonlight.",
      ["the Bell Deep"],
      "“叮当！叮当！”欧登塞河里的钟渊传来这样的声音。——这是一条什么河？欧登塞城里的每个孩子都认得它：它从花园下面流过，从水闸流到水磨坊，从木桥底下穿过。"
      + GAP + "在古老的修道院对面，是河水最深的地方，人们管它叫钟渊，河人就住在那里。白天太阳照进水里的时候他睡觉，到了满天星斗、月光明亮的夜里，他才出来。",
      ["钟渊"]),
    Q("dk-gru-1", "marie-grubbe", "dk-tjele", "Chapter 1", "第一章", T_GRU, _gru, ["Tjele Hovedgaard"],
      "The sound of the blows made an uncanny impression on the child; she held her hands over her ears and walked quickly up towards the house. The cellar door down to the brewhouse stood open; she slipped down and slammed the door behind her.\nThat was the fourteen-year-old Marie Grubbe, daughter of Herr Erik Grubbe of Tjele Manor.",
      ["Tjele Manor"],
      "鞭打的声音让这孩子感到一阵恐怖，她捂住耳朵，匆匆朝宅子走去。通往酿酒房的地窖门开着；她溜了下去，砰地关上了身后的门。\n这就是十四岁的玛丽·格鲁贝，蒂勒庄园主埃里克·格鲁贝老爷的女儿。",
      ["蒂勒庄园"], note=" (the page's line ends joined)"),
    Q("dk-degn-1", "village-clerks-diary", "dk-tjele", "Entry for 1 May 1709", "1709 年 5 月 1 日的日记", T_DEGN, _degn, ["Thiele"],
      "Tjele, 1 May 1709.\nSo now I am a servant to the gracious gentry! Farewell to the priesthood! Farewell to Latin! O my dear books! valete plurimum! vendidi libertatem — I have sold my freedom for twelve slette dalers. Eight of them my poor mother shall have, and the gracious master has promised her an allowance of firewood besides, so she will neither starve nor freeze.",
      ["Tjele"],
      "蒂勒，1709 年 5 月 1 日。\n这么说，我现在成了尊贵老爷家的仆人了！别了，牧师的前程！别了，拉丁文！啊，我亲爱的书本！valete plurimum！vendidi libertatem——我用十二块银元卖掉了我的自由。其中八块给我可怜的母亲，老爷还答应另外分给她柴火：这样她就既不会挨饿，也不会受冻了。",
      ["蒂勒"], note=" (the page's line ends joined)"),
    Q("dk-per-1", "lucky-per", "dk-randers", "Chapter 1, opening", "第一章开头", T_PER,
      flow(raw(T_PER, "I en af de østjyske Smaakøbstæder", "Johannes Sidenius.")), ["østjyske Smaakøbstæder"],
      "In one of the small market towns of East Jutland, tucked away among green slopes at the head of an overgrown fjord, there lived, in the years before and after our last war, a priest named Johannes Sidenius.",
      ["small market towns of East Jutland"],
      "在东日德兰的小城当中，有一座藏在一条淤塞的峡湾尽头、四周是绿色山坡的小城；在我们上一场战争前后的那些年里，城里住着一位名叫约翰内斯·西德尼乌斯的牧师。",
      ["东日德兰的小城"], note=" (the page's line ends joined)"),
    Q("dk-kf-1", "fall-of-the-king", "dk-gammeltorv", "'Copenhagen by Night'", "《夜晚的哥本哈根》", T_KF,
      flow(raw(T_KF, "Næste Dag saa Københavns Borgere", "Mester for det.")), ["Københavns"],
      "The next day the citizens of Copenhagen saw a cart riding with all four wheels astride the ridge of a tall house facing the market square. Someone had taken it apart in the night, dragged the pieces up on to the roof and put them together again there. Before noon the whole town knew that it was Prince Christiern who had been the master of it.",
      ["Copenhagen"],
      "第二天，哥本哈根的市民看见一辆车四个轮子骑跨在一座临广场的高房子的屋脊上。有人夜里把它拆开，把零件拖上屋顶，又在那里重新装好。不到中午，全城都知道了，这是克里斯蒂安王子的杰作。",
      ["哥本哈根"], note=" (the page's line ends joined)"),
]

_ham = raw(T_HAM, "Elsinore. A Platform of the Castle]", "And I am sick at heart.", "en")
_ham = _ham.replace("Castle]", "Castle", 1).replace("\n\xa0\n", "\n")
_ham = re.sub(r"(?m) \d+$", "", _ham)
_woll = flow(raw(T_WOLL, "Just before I reached Copenhagen", "by the late fire.", "en"))
lines += [
    EN("dk-ham-1", HAMLET, "dk-kronborg", "Act 1, Scene 1", "第一幕第一场", T_HAM, _ham, ["Elsinore"],
       "埃尔西诺。城堡前的露台。\n勃那多和弗兰西斯科两个哨兵上。\n勃：那边是谁？\n弗：不，你回答我；站住，说出你是谁。\n勃：国王万岁！\n弗：是勃那多吗？\n勃：是我。\n弗：你来得正是时候。\n勃：现在已经敲过十二点了；去睡吧，弗兰西斯科。\n弗：多谢你来替我；天冷得刺骨，\n我心里也不好受。",
       ["埃尔西诺"], note=" (the editor's brackets round the place heading, a blank line and his line numbers left out)"),
    EN("dk-woll-1", "wollstonecraft-letters", "dk-indre-by", "Letter XVIII", "第十八封信", T_WOLL, _woll, ["Copenhagen"],
       "快到哥本哈根的时候，我看见一片开阔的平地上搭着许多帐篷，起初以为扎营的风气也传到了这座城市；但我很快发现，这些帐篷是许多穷苦人家的栖身之所——他们是被不久前的那场大火赶出家门的。",
       ["哥本哈根"], note=" (the page's line ends joined)"),
]

lines += [
    S("dk-pelle-s1", "pelle-the-conqueror", "dk-nexo", "Part 1, 'Childhood'", "第一部《童年》",
      "In the late 1850s the old widower Lasse Karlsson and his small son Pelle leave Skåne, in southern Sweden, after the boy's mother has died, and cross to Bornholm to find work. They are taken on as hands on a big farm, and the boy grows up there through hard service and humiliation.",
      "十九世纪五十年代末，孩子的母亲死后，年老的鳏夫拉塞·卡尔松带着小儿子佩勒离开瑞典南部的斯科讷，渡海来到博恩霍尔姆岛找活干。他们在一座大农庄上当了雇工，孩子就在繁重的劳役和屈辱中长大。",
      ["Bornholm"], ["博恩霍尔姆岛"], W + "Pelle_the_Conqueror"),
    S("dk-smilla-s1", "smillas-sense-of-snow", "dk-christianshavn", "Part 1, 'The City'", "第一部《城市》",
      "Smilla Jaspersen, half Greenlandic, lives alone in a dreary block of flats in Christianshavn. Isaiah, the small Greenlandic son of a neighbour, whom she has befriended, is found dead in the snow under the roof of their building. The police call it an accident; Smilla, reading the tracks in the snow on the roof, does not believe them.",
      "斯米拉·雅斯珀森有一半格陵兰血统，独自住在克里斯蒂安港一座沉闷的公寓楼里。邻居家那个跟她交上朋友的格陵兰小男孩以赛亚，被发现死在他们那栋楼屋顶下的雪地里。警方说是意外；斯米拉看了屋顶积雪上的脚印，不相信这个说法。",
      ["Christianshavn"], ["克里斯蒂安港"], W + "Miss_Smilla%27s_Feeling_for_Snow"),
    S("dk-tove-s1", "copenhagen-trilogy", "dk-hedebygade", "Childhood", "《童年》",
      "Childhood, the first of the three books, tells of growing up in the 1920s in a back-house flat on Hedebygade in Vesterbro, with a father who is a stoker and often out of work, her mother and an older brother, Edvin; the girl writes poems in secret and means to be a poet.",
      "三部曲的第一部《童年》写的是二十年代在韦斯特布罗区黑德比街一座后院楼里长大的日子：父亲是司炉，常常失业，还有母亲和哥哥埃德温；小女孩偷偷地写诗，一心要当诗人。",
      ["Hedebygade"], ["黑德比街"], W + "The_Copenhagen_Trilogy"),
    S("dk-paars-s1", "peder-paars", "dk-anholt", "Books 1–2", "第一、二卷",
      "The grocer Peder Paars sets sail from Kalundborg to see his betrothed, Dorothea, in Aarhus. A storm wrecks his ship on Anholt, where the islanders make their living from wrecks; the short voyage becomes a mock Aeneid.",
      "杂货商彼泽·帕尔斯从卡伦堡起航，去奥胡斯看望未婚妻多罗特娅。一场风暴让他的船在安霍尔特岛搁浅——岛上的人就靠沉船过活；这趟短短的航程，成了一部戏仿的《埃涅阿斯纪》。",
      ["Anholt"], ["安霍尔特岛"], "https://www.bokselskap.no/wp-content/themes/bokselskap2/tekster/pdf/pederpaars.pdf"),
    S("dk-tine-s1", "tine", "dk-als", "Throughout", "全书",
      "In February 1864 war breaks out, and the forester's wife and her son are sent from Als to Copenhagen. Tine, the parish clerk's daughter, keeps house for the forester Berg, whom she has long loved in secret, while soldiers pass through and the Prussians shell Dybbøl and Sønderborg; the book ends in April, with the storming of Dybbøl.",
      "1864 年 2 月战争爆发，林务官的妻子和儿子被从阿尔斯岛送往哥本哈根。教堂执事的女儿蒂娜留下来替林务官贝格料理家务——她早就偷偷爱上了他；军队来来往往，普鲁士人炮轰迪伯尔和森讷堡；故事在 4 月迪伯尔失守时结束。",
      ["Als"], ["阿尔斯岛"], "https://da.wikipedia.org/wiki/Tine_(roman)"),
    S("dk-beo-s1", "beowulf", "dk-lejre", "The first part", "第一部分",
      "Hrothgar, king of the Danes, builds the great mead hall Heorot. Night after night for twelve years the monster Grendel comes from the moors to carry off and kill his men, until Beowulf, a hero of the Geats, sails over from Sweden and kills him in the hall.",
      "丹麦国王赫罗斯加建起了宏伟的蜜酒大厅“鹿厅”。十二年里，怪物格伦德尔一夜又一夜从沼地里来，把他的武士掳走杀死，直到耶阿特人的英雄贝奥武甫从瑞典渡海而来，在大厅里杀死了它。",
      ["Heorot"], ["鹿厅"], W + "Beowulf"),
    S("dk-drown-s1", "we-the-drowned", "dk-marstal", "Throughout", "全书",
      "Told by the town itself, the 'we' of the title, the novel follows the sailors of Marstal and the wives and children they leave behind, from 1848, when the young men go off to fight in the First Schleswig War, through three generations at sea, to the end of the Second World War.",
      "小说由这座小城自己——书名里的“我们”——来讲述，写马斯塔尔的水手们，以及被他们留在家里的妻子和孩子：从 1848 年年轻人出征第一次石勒苏益格战争写起，三代人在海上漂泊，一直写到第二次世界大战结束。",
      ["Marstal"], ["马斯塔尔"], "https://www.penguin.co.uk/books/396223/we-the-drowned-by-carsten-jensen/9780099512967"),
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

HEAD = "// Denmark, hand-written content (tools/content/batches/add_dk1.py, 2026-11-23).\n"
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
