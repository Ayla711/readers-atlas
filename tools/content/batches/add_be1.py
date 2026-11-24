"""11-23: Belgium, first pack: 7 new books and 4 from earlier packs, 10 places. Ouida's Antwerp cathedral, De Coster's
Damme, Rodenbach's Bruges, Conscience's heroes on the Bruges Markt, Hugo's Hougoumont, Thackeray's and Conrad's Brussels,
Charlotte Bronte's Villette, Claus's Kortrijk, Simenon's Liege and Timmermans's Lier.

Quotations (7 lines) are cut from French and English Wikisource pages (tools/content/wikisource.py); translations of the
French are our own drafts (translation: "own"). Books in copyright, and PD books whose text we did not reach, have scene
notes in our own words or hang on a writer's place. What a cut changes is named in `checked`.

Coordinates are those of the place's Wikipedia article (cache/be/coords.json).

Usage: python3 -I add_be1.py <app_dir> <coords.json> <wikisource_root>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-23"
b.init(APP, "", "be", DATE)
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

T_DOG, T_UL, T_BLM = "A Dog of Flanders", "La Légende d’Ulenspiegel/Livre 1", "Bruges-la-Morte/01"
T_LM, T_VF = "Les Misérables/Tome 2/Livre 1/02", "Vanity Fair (Thackeray)/Chapter 32"
T_HOD, T_VIL = "Youth: a Narrative, and Two Other Stories/Heart of Darkness/Section 1", "Villette (2nd American edition)/Chapter VII"
EXIST = {"villette", "vanity-fair", "heart-of-darkness", "fr-les-miserables"}

books = [
    BK("a-dog-of-flanders", "A Dog of Flanders", "佛兰德斯的狗", "A Dog of Flanders", "Ouida", "维达", "Ouida", "1872", lang="en",
       src=ws.url("en", "A Dog of Flanders"), aliases=["Nello", "Patrasche", "Antwerp", "法兰德斯之犬", "龙龙与忠狗"]),
    BK("ulenspiegel", "The Legend of Thyl Ulenspiegel", "乌兰斯匹格传奇", "La Légende d’Ulenspiegel", "Charles De Coster", "夏尔·德·科斯特",
       "Charles De Coster", "1867", lang="fr", src=ws.url("fr", "La Légende d’Ulenspiegel"),
       aliases=["Tijl Uilenspiegel", "Thyl Ulenspiegel", "Lamme Goedzak", "Nele", "Claes", "Damme"]),
    BK("bruges-la-morte", "Bruges-la-Morte", "死城布鲁日", "Bruges-la-Morte", "Georges Rodenbach", "乔治·罗登巴赫", "Georges Rodenbach", "1892",
       lang="fr", src=ws.url("fr", "Bruges-la-Morte"), aliases=["Hugues Viane", "Jane Scott", "Bruges", "Brugge"]),
    BK("lion-of-flanders", "The Lion of Flanders", "佛兰德斯的狮子", "De Leeuw van Vlaenderen, of de Slag der Gulden Sporen", "Hendrik Conscience",
       "亨德里克·孔西安斯", "Hendrik Conscience", "1838", aliases=["De Leeuw van Vlaanderen", "Breydel", "De Coninck", "Guldensporenslag", "Battle of the Golden Spurs"]),
    BK("sorrow-of-belgium", "The Sorrow of Belgium", "比利时的哀愁", "Het verdriet van België", "Hugo Claus", "雨果·克劳斯", "Hugo Claus", "1983",
       pd=False, aliases=["Het verdriet van België", "Louis Seynaeve", "Walle", "Kortrijk"]),
    BK("pedigree-simenon", "Pedigree", "血统", "Pedigree", "Georges Simenon", "乔治·西默农", "Georges Simenon", "1948", lang="fr", pd=False,
       aliases=["Roger Mamelin", "Liège", "Outremeuse", "Simenon"]),
    BK("pallieter", "Pallieter", "帕列特", "Pallieter", "Felix Timmermans", "费利克斯·蒂默曼斯", "Felix Timmermans", "1916",
       aliases=["Melk den dag", "Lier", "Nete", "Timmermans"]),
]

places = [
    ORIG("be-antwerp-cathedral", "Cathedral of Our Lady, Antwerp", "圣母大教堂，安特卫普",
         "The cathedral where Rubens's Elevation of the Cross and Descent from the Cross hang. In A Dog of Flanders the poor boy Nello longs to see the two paintings, kept veiled and shown only for a fee; on Christmas night he and his dog Patrasche die before them. Since 2016 a white marble statue by Batist Vermeulen of the two asleep under a blanket of cobblestones has lain on the Handschoenmarkt in front of the cathedral; the story is especially loved in Japan",
         "鲁本斯的《竖起十字架》和《卸下圣体》就挂在这座大教堂里。在《佛兰德斯的狗》中，穷孩子奈罗一心想看这两幅画，可画平时用幕布遮着，要付钱才能看；圣诞夜，他和狗帕特拉什死在了这两幅画前。2016 年起，大教堂前的手套市场广场上躺着巴蒂斯特·费尔默伦的白色大理石雕像：一人一狗盖着一床鹅卵石“被子”睡着了。这个故事在日本尤其受欢迎"),
    ORIG("be-damme", "Damme", "达默",
         "Small town near Bruges where, in De Coster's novel, Ulenspiegel is born, the son of the charcoal-burner Claes and his wife Soetkin. A statue of Tijl Uilenspiegel by Jef Claerhout stands in the town",
         "布鲁日附近的小城。在德·科斯特的小说里，乌兰斯匹格就生在这里，父亲是烧炭人克拉斯，母亲是苏特金。城里立着一尊杰夫·克拉尔豪特塑造的乌兰斯匹格像"),
    ORIG("be-rozenhoedkaai", "Rozenhoedkaai (Quai du Rosaire), Bruges", "玫瑰念珠码头，布鲁日",
         "Quay in the centre of Bruges, the Quai du Rosaire of Bruges-la-Morte, where the widower Hugues Viane lives in a house mirrored in the water. Rodenbach set dozens of photographs of Bruges into the book, which is thought to be the first novel illustrated with photographs",
         "布鲁日市中心的一段码头，就是《死城布鲁日》里的“玫瑰念珠码头”：丧妻的于格·维亚纳住在这里，房子倒映在水中。罗登巴赫在书里插入了几十张布鲁日的照片，一般认为这是第一部用照片作插图的小说"),
    PIL("be-bruges-markt", "Markt, Bruges (Breydel and De Coninck)", "布鲁日集市广场（布雷德尔与德·科宁克像）",
        "The market square of Bruges, where a statue by Paul De Vigne of Jan Breydel and Pieter de Coninck, leaders of the Bruges rising of 1302 that led to the Battle of the Golden Spurs, was unveiled in 1887. Hendrik Conscience's The Lion of Flanders (1838) did most to make the two men Flemish heroes",
        "布鲁日的集市广场。1887 年，这里揭幕了保罗·德·维涅塑造的扬·布雷德尔和彼得·德·科宁克像——两人领导了 1302 年布鲁日的起义，随后爆发了金马刺战役。把他们俩塑造成佛兰德英雄的，首先是亨德里克·孔西安斯的《佛兰德斯的狮子》（1838）",
        ["lion-of-flanders"]),
    ORIG("be-hougoumont", "Hougoumont, Waterloo", "乌古蒙农庄，滑铁卢",
         "Walled farm on the battlefield of Waterloo, where companies of British Guards held out against Napoleon's attacks on 18 June 1815. In Les Misérables, Hugo walks the battlefield and opens his account of the battle at this farm, which he spells Hougomont",
         "滑铁卢战场上一座带围墙的农庄。1815 年 6 月 18 日，英国近卫军的几个连在这里顶住了拿破仑的进攻。《悲惨世界》里，雨果走过这片战场，就从这座农庄写起他对这场战役的叙述"),
    ORIG("be-bozar", "Bozar (site of the Pensionnat Heger), Brussels", "布鲁塞尔美术宫（埃热寄宿学校旧址）",
         "The Centre for Fine Arts stands near the site of the Pensionnat Heger in the old Rue d'Isabelle, where Charlotte and Emily Brontë studied in 1842–43; a Brontë Society plaque of 1979 marks it. The city of Villette is Brussels in all but name, and Madame Beck's school is drawn from the Pensionnat",
         "布鲁塞尔美术宫一带原是老伊莎贝拉街上的埃热寄宿学校，夏洛蒂和艾米莉·勃朗特 1842 至 1843 年在那里读书；勃朗特学会 1979 年在这里立了一块纪念牌。《维莱特》里的维莱特城其实就是布鲁塞尔，贝克夫人的学校就以这所寄宿学校为原型"),
    ORIG("be-brussels", "Brussels (Grand-Place)", "布鲁塞尔（大广场）",
         "Brussels, where in Vanity Fair Amelia and the others wait out the battle of Waterloo, listening to the guns. The unnamed city 'that always makes me think of a whited sepulchre', where Marlow signs on with the Company in Heart of Darkness, is generally read as Brussels",
         "布鲁塞尔。《名利场》里，阿米莉亚等人就在这里一边听着炮声，一边等滑铁卢战役的结果。《黑暗的心》里，马洛去公司签约的那座没有点名、“总让我想起粉饰的坟墓”的城市，一般也被认为是布鲁塞尔"),
    ORIG("be-outremeuse", "Outremeuse, Liège", "乌特勒默斯，列日",
         "The Liège quarter where Georges Simenon grew up: his family moved to the rue Pasteur (now rue Georges Simenon) in 1905 and to the rue de la Loi in 1911, where his mother took in lodgers. His autobiographical novel Pedigree draws on these years",
         "列日的一个街区，乔治·西默农在这里长大：1905 年全家搬到巴斯德街（今西默农街），1911 年又搬到法律街，母亲在那里招房客。他的自传体小说《血统》就取材于这些年月"),
    ORIG("be-kortrijk", "Kortrijk", "科特赖克",
         "City in West Flanders, the 'Walle' of Hugo Claus's The Sorrow of Belgium, where most of the novel takes place; Claus's parents lived here. In 2018 the city launched an audio walk past the places in the book",
         "西佛兰德省的城市，就是雨果·克劳斯《比利时的哀愁》里的“瓦勒”，小说大部分情节都发生在这里；克劳斯的父母就住在这座城。2018 年，市里推出了一条走访书中地点的语音导览路线"),
    PIL("be-lier", "Lier", "利尔",
        "Town on the Nete where Felix Timmermans was born in 1886 and died in 1947. His Pallieter (1916), about a man who revels in the life of the fields and river around Lier, made him famous; its motto, 'Melk den dag!' (Milk the day!), is the only line Pallieter ever writes",
        "内特河畔的小城，费利克斯·蒂默曼斯 1886 年生于此，1947 年也死于此。他的《帕列特》（1916）写一个在利尔周围的田野和河边尽情享受生活的人，让他一举成名；书里的格言“榨干这一天！”是帕列特写下的唯一一句话",
        ["pallieter"]),
]

def nb(s):
    """double spaces in the page written as one"""
    return re.sub(r" {2,}", " ", s)
_dog = nb(raw(T_DOG, "The portals of the cathedral were unclosed", "he found Nello.", "en")) + GAP + nb(raw(T_DOG, "Suddenly through the darkness", "it is enough!\"", "en"))
_ul = raw(T_UL, "À Damme, en Flandre,", "doigt du diable.", "fr")
_blm = raw(T_BLM, "Le jour déclinait,", "mirée dans l’eau.", "fr") + GAP + raw(T_BLM, "Voilà cinq ans qu’il vivait ainsi,", "la mort de sa femme.", "fr")
lines = [
    EN("be-dog-1", "a-dog-of-flanders", "be-antwerp-cathedral", "Part 3, Christmas night", "第三部分，圣诞夜", T_DOG, _dog, ["cathedral"],
       "大教堂的大门在子夜弥撒之后没有关上。看守人只顾着回家过节或睡觉，或是困得不知道钥匙有没有转到位，竟有一扇门没有锁。就因为这个疏忽，帕特拉什寻找的那串脚印穿过门进了教堂，在黑色的石板地上留下了一个个白色的雪印。这条细细的白线一落下就冻住了，它循着这条线，穿过深深的寂静，穿过广阔的穹顶下的空间，一直走到圣坛的栏门前，在那里的石板上，它找到了奈罗。\n…\n忽然，一道巨大的白光穿过黑暗，洒满了宽阔的侧廊；高悬中天的月亮冲破了云层，雪已经停了，外面雪地反射的光像黎明一样明亮。光穿过拱门，正好照在上方那两幅画上——孩子进来时已经把遮画的幕布掀开了：《竖起十字架》和《卸下圣体》在这一刻像白天一样清清楚楚。\n奈罗站起身，向它们伸出双臂，苍白的脸上闪着狂喜的泪光。\n“我终于看到了！”他大声喊道，“上帝啊，这就够了！”",
       ["大教堂"], note=" (two passages, the first cut after its fourth sentence)"),
    Q("be-ul-1", "ulenspiegel", "be-damme", "Book 1, chapter 1, opening", "第一卷第一章开头", T_UL, _ul, ["Damme"],
      "At Damme, in Flanders, when May was opening the hawthorn blossoms, Ulenspiegel, son of Claes, was born.\nA gossip and midwife named Katheline wrapped him in warm swaddling clothes and, having looked at his head, pointed out a caul on it.\n'Born with a caul, born under a lucky star!' she said joyfully.\nBut soon, lamenting and pointing to a little black spot on the child's shoulder:\n'Alas!' she wept, 'it is the black mark of the devil's finger.'",
      ["Damme"],
      "在佛兰德的达默，五月让山楂花开放的时节，克拉斯的儿子乌兰斯匹格出生了。\n一位名叫卡特琳的接生婆用暖和的襁褓裹住他，看了看他的头，指给大家看头上的胎膜。\n“带着胎膜出生，是吉星高照！”她高兴地说。\n可是不一会儿，她又哀叹起来，指着孩子肩上的一个小黑点：\n“唉！”她哭着说，“这是魔鬼手指留下的黑印。”",
      ["达默"], note=" (the 1867 edition's long s and ampersands kept as printed)", site="French"),
    Q("be-blm-1", "bruges-la-morte", "be-rozenhoedkaai", "Chapter 1, opening", "第一章开头", T_BLM, _blm, ["quai du Rosaire", "Bruges"],
      "The day was declining, darkening the corridors of the great silent house, hanging screens of crape over the window-panes.\nHugues Viane got ready to go out, as was his daily habit at the end of the afternoon. Idle and solitary, he spent the whole day in his room, a vast chamber on the first floor whose windows looked out on the Quai du Rosaire, along which his house stood, mirrored in the water.\n…\nFor five years he had lived like this, ever since he had come to settle in Bruges, the day after his wife's death.",
      ["Quai du Rosaire", "Bruges"],
      "天色渐暗，大宅寂静的走廊越来越昏沉，窗玻璃上仿佛挂起了黑纱。\n于格·维亚纳准备出门，这是他每天傍晚的习惯。他无所事事，孤身一人，整天待在自己的房间里——二楼一间宽敞的屋子，窗户正对着玫瑰念珠码头，他的房子就沿着码头排开，倒映在水中。\n…\n他这样过日子已经五年了，自从妻子去世后第二天来到布鲁日定居以来，一直如此。",
      ["玫瑰念珠码头", "布鲁日"], note=" (two passages; the second is the first sentence of its paragraph)", site="French"),
    Q("be-lm-1", "fr-les-miserables", "be-hougoumont", "Part 2 (Cosette), Book 1 'Waterloo', chapter 2 'Hougomont'", "第二部（珂赛特）第一卷《滑铁卢》第二章《乌古蒙》",
      T_LM, raw(T_LM, "Hougomont, ce fut là", "qu’une ferme.", "fr"), ["Hougomont", "Waterloo"],
      "Hougomont: this was a place of death, the beginning of the obstacle, the first resistance that the great woodcutter of Europe who was called Napoleon met at Waterloo; the first knot under the blow of the axe.\nIt was a castle; it is now no more than a farm.",
      ["Hougomont", "Waterloo"],
      "乌古蒙，这是一个凄惨的地方，是障碍的开端，是那位叫作拿破仑的欧洲大樵夫在滑铁卢遇到的第一个抵抗，是斧头砍下去碰上的第一个树节。\n它从前是一座城堡，现在只是一座农庄了。",
      ["乌古蒙", "滑铁卢"], site="French"),
    EN("be-vf-1", "vanity-fair", "be-brussels", "Chapter 32, closing lines", "第三十二章结尾", T_VF,
       raw(T_VF, "No more firing was heard at Brussels", "through his heart.", "en"), ["Brussels"],
       "布鲁塞尔再也听不到炮声了——追击已经滚到好几英里以外。黑夜降临在战场上，也降临在城里；阿米莉亚正在为乔治祈祷，而乔治脸朝下躺着，已经死了，一颗子弹穿透了他的心。",
       ["布鲁塞尔"]),
    EN("be-hod-1", "heart-of-darkness", "be-brussels", "Part 1", "第一部分", T_HOD,
       raw(T_HOD, "In a very few hours I arrived", "coin by trade.", "en") + "\n" + raw(T_HOD, "A narrow and deserted street", "ponderously ajar.", "en"),
       ["a city that always makes me think of a whited sepulchre"],
       "没过几个钟头，我就到了一座总让我想起“粉饰的坟墓”的城市。这也许是偏见。我毫不费力就找到了公司的办事处。那是城里最大的一家，我遇到的每个人都满嘴说着它。他们要经营一个海外帝国，靠做买卖赚数不清的钱。\n一条狭窄、冷清、笼在深深阴影里的街，高高的房子，数不清的窗户挂着百叶帘，一片死寂，左右两边冒出了草，巨大的双扇门沉沉地半开着。",
       ["一座总让我想起“粉饰的坟墓”的城市"], note=" (the first paragraph from its third sentence; of the second, its first sentence only, without its opening quotation mark)"),
    EN("be-vil-1", "villette", "be-bozar", "Chapter 7, 'Villette'", "第七章《维莱特》", T_VIL,
       raw(T_VIL, "I had hoped we might reach Villette", "gained its suburbs.", "en"), ["Villette"],
       "我原希望天黑以前就能到达维莱特，那样，初到一个陌生地方时黑暗似乎总会添上的更深一层的窘迫，我也许就能躲过；可是，我们走得慢，又停得久，再加上浓雾和细密的雨，等我们到达城郊时，那种仿佛摸得着的黑暗已经笼罩了整座城。",
       ["维莱特"]),
]
lines += [
    S("be-sorrow-s1", "sorrow-of-belgium", "be-kortrijk", "Part 1", "第一部",
      "In 1939 Louis Seynaeve, a printer's son who turns eleven that April, is at a boarding school run by nuns in Haarbeke, a made-up village near the town the novel calls Walle, which is Kortrijk. The book follows him and his family through the war years.",
      "1939 年，印刷商的儿子路易·塞纳弗这年四月满十一岁，正在哈尔贝克一所修女办的寄宿学校读书。哈尔贝克是虚构的村子，靠近书中叫作“瓦勒”的城——也就是科特赖克。小说跟着他和他的家人走过了战争年代。",
      ["Walle"], ["瓦勒"], W + "The_Sorrow_of_Belgium"),
    S("be-pedigree-s1", "pedigree-simenon", "be-outremeuse", "Throughout", "全书",
      "Roger Mamelin, Simenon's double, grows up in Liège from the beginning of the twentieth century to the end of the First World War. Much of Simenon's own childhood in the Outremeuse quarter, where his mother took in lodgers, shows through the story.",
      "罗歇·马默兰是西默农的化身，他在列日长大，从二十世纪初一直写到第一次世界大战结束。西默农自己在乌特勒默斯街区度过的童年——包括母亲招房客的那些日子——有很多都透过这个故事显露出来。",
      ["Liège"], ["列日"], W + "Pedigree_(novel)"),
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

HEAD = "// Belgium, hand-written content (tools/content/batches/add_be1.py, 2026-11-23).\n"
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
