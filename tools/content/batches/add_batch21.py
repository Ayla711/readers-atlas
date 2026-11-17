"""11-17: the UK selection round (sel/uk, rubric 学界30/奖项25/读者25/教育10/国际10). The user kept almost every
book the rubric proposed to drop, removed only the two least known (Thackeray's Irish Sketch Book, Borrow's Lavengro),
and added the rubric's suggestions plus a few world-famous near misses. Game of Thrones stays a film location only.
In-copyright books get scene notes only. Gutenberg is down (503), so public-domain books also get scene notes for now;
the one quotation (Hamlet) is cut from the downloaded Project Gutenberg text.
Usage: python3 -I add_batch21.py <app_dir> <pg_texts_dir>"""
import json, re, sys
sys.path.insert(0, __file__.rsplit("/", 2)[0])
import batchlib as b
APP, TX = sys.argv[1], sys.argv[2]
b.init(APP, TX, "uk", "2026-11-17")
W, G = b.W, b.G
C = "https://commons.wikimedia.org/wiki/"
ORIG, PROTO, PIL, S = b.ORIG, b.PROTO, b.PIL, b.S

def cat(name):
    return f"Category:{name} (Wikimedia Commons)", C + "Category:" + name.replace(" ", "_")

# ---------------------------------------------------------------- removals
DROP_BOOKS = ["irish-sketch-book", "lavengro"]
DROP_LINES = ["isb-1", "isb-2", "isb-3", "isb-4", "lav-1"]
DROP_PLACES = ["carrickfergus-castle", "glenarm", "norwich"]

def remove_objects(path, ids):
    """drop `{ id: "x", ... }` objects (one or more lines, nested braces allowed) and their trailing comma"""
    s = open(path, encoding="utf-8").read()
    for i in ids:
        m = re.search(r'\n[ \t]*\{ id: "' + re.escape(i) + r'"', s)
        assert m, (path, i)
        j, depth, instr = m.start() + 1, 0, False
        k = j
        while True:
            c = s[k]
            if instr:
                if c == "\\": k += 1
                elif c == '"': instr = False
            elif c == '"': instr = True
            elif c == "{": depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0: break
            k += 1
        k += 1
        if s[k] == ",": k += 1
        s = s[:m.start()] + s[k:]
    open(path, "w", encoding="utf-8").write(s)

# ---------------------------------------------------------------- books
def BK(id, title, title_zh, author, author_zh, year, pg=None, pd=True, **kw):
    d = dict(id=id, title=title, title_zh=title_zh, author=author, author_zh=author_zh, year=year, orig_lang="en",
             public_domain=pd, source_url=(G + str(pg)) if pg else None)
    d.update(kw)
    return d

books = [
    BK("hamlet", "Hamlet", "哈姆雷特", "William Shakespeare", "莎士比亚", "c. 1600", 1524, aliases=["哈姆莱特", "王子复仇记", "The Tragedy of Hamlet, Prince of Denmark"]),
    BK("shakespeares-sonnets", "Shakespeare's Sonnets", "莎士比亚十四行诗", "William Shakespeare", "莎士比亚", "1609", 1041, aliases=["Sonnets", "十四行诗", "Sonnet 18"]),
    BK("tom-jones", "Tom Jones", "汤姆·琼斯", "Henry Fielding", "亨利·菲尔丁", "1749", 6593, aliases=["The History of Tom Jones, a Foundling", "弃儿汤姆·琼斯史"]),
    BK("natural-history-of-selborne", "The Natural History of Selborne", "塞耳彭自然史", "Gilbert White", "吉尔伯特·怀特", "1789", 1408, aliases=["Selborne", "塞尔彭自然史"]),
    BK("justified-sinner", "The Private Memoirs and Confessions of a Justified Sinner", "一个清白罪人的私人回忆与自白", "James Hogg", "詹姆斯·霍格", "1824", 2276,
       aliases=["Confessions of a Justified Sinner", "Justified Sinner", "称义罪人的忏悔"]),
    BK("opium-eater", "Confessions of an English Opium-Eater", "一个英国鸦片吸食者的自白", "Thomas De Quincey", "托马斯·德·昆西", "1821", 2040, aliases=["瘾君子自白", "Opium-Eater"]),
    BK("vanity-fair", "Vanity Fair", "名利场", "William Makepeace Thackeray", "萨克雷", "1847–1848", 599, aliases=["Becky Sharp", "蓓基·夏泼"]),
    BK("villette", "Villette", "维莱特", "Charlotte Brontë", "夏洛蒂·勃朗特", "1853", 9182, aliases=["维莱特", "Lucy Snowe"]),
    BK("daniel-deronda", "Daniel Deronda", "丹尼尔·德龙达", "George Eliot", "乔治·艾略特", "1876", 7469, aliases=["丹尼尔·狄隆达"]),
    BK("barchester-towers", "Barchester Towers", "巴彻斯特大教堂", "Anthony Trollope", "安东尼·特罗洛普", "1857", 3409, aliases=["巴塞特郡", "Barsetshire", "巴彻斯特塔"]),
    BK("way-we-live-now", "The Way We Live Now", "如今世道", "Anthony Trollope", "安东尼·特罗洛普", "1875", 5231, aliases=["我们现在的生活方式", "Melmotte"]),
    BK("origin-of-species", "On the Origin of Species", "物种起源", "Charles Darwin", "查尔斯·达尔文", "1859", 1228, aliases=["The Origin of Species", "Origin of Species"]),
    BK("jude-the-obscure", "Jude the Obscure", "无名的裘德", "Thomas Hardy", "哈代", "1895", 153, aliases=["Christminster", "基督寺"]),
    BK("mayor-of-casterbridge", "The Mayor of Casterbridge", "卡斯特桥市长", "Thomas Hardy", "哈代", "1886", 143, aliases=["Casterbridge", "Henchard"]),
    BK("adventures-of-sherlock-holmes", "The Adventures of Sherlock Holmes", "福尔摩斯冒险史", "Arthur Conan Doyle", "柯南·道尔", "1892", 1661,
       aliases=["A Scandal in Bohemia", "The Speckled Band", "The Red-Headed League", "波希米亚丑闻", "斑点带子案", "红发会"]),
    BK("de-profundis", "De Profundis", "自深深处", "Oscar Wilde", "奥斯卡·王尔德", "1905", 921, aliases=["Epistola: In Carcere et Vinculis"]),
    BK("importance-of-being-earnest", "The Importance of Being Earnest", "不可儿戏", "Oscar Wilde", "奥斯卡·王尔德", "1895", 844, aliases=["认真的重要", "Earnest", "A handbag?"]),
    BK("new-grub-street", "New Grub Street", "新寒士街", "George Gissing", "乔治·吉辛", "1891", 1709, aliases=["新格拉布街"]),
    BK("heart-of-darkness", "Heart of Darkness", "黑暗的心", "Joseph Conrad", "约瑟夫·康拉德", "1899", 219, aliases=["黑暗之心", "Marlow", "Kurtz"]),
    BK("nostromo", "Nostromo", "诺斯特罗莫", "Joseph Conrad", "约瑟夫·康拉德", "1904", 2021, aliases=["Costaguana"]),
    BK("women-in-love", "Women in Love", "恋爱中的女人", "D. H. Lawrence", "劳伦斯", "1920", 4240, aliases=["恋爱中的妇女"]),
    BK("of-human-bondage", "Of Human Bondage", "人性的枷锁", "W. Somerset Maugham", "毛姆", "1915", pd=False, aliases=["Philip Carey"]),
    BK("room-of-ones-own", "A Room of One's Own", "一间自己的房间", "Virginia Woolf", "伍尔夫", "1929", aliases=["自己的一间屋", "一间自己的屋子"]),
    BK("passage-to-india", "A Passage to India", "印度之行", "E. M. Forster", "E. M. 福斯特", "1924", pd=False, aliases=["Marabar Caves"]),
    BK("howards-end", "Howards End", "霍华德庄园", "E. M. Forster", "E. M. 福斯特", "1910", pd=False, aliases=["Only connect", "霍华兹庄园"]),
    BK("end-of-the-affair", "The End of the Affair", "恋情的终结", "Graham Greene", "格雷厄姆·格林", "1951", pd=False, aliases=["爱情的尽头", "恋情的终结"]),
    BK("heart-of-the-matter", "The Heart of the Matter", "问题的核心", "Graham Greene", "格雷厄姆·格林", "1948", pd=False, aliases=["命运的内核"]),
    BK("murder-of-roger-ackroyd", "The Murder of Roger Ackroyd", "罗杰疑案", "Agatha Christie", "阿加莎·克里斯蒂", "1926", pd=False, aliases=["罗杰·艾克罗伊德谋杀案", "Ackroyd"]),
    BK("north-heaney", "North", "北方", "Seamus Heaney", "谢默斯·希尼", "1975", pd=False, aliases=["Mossbawn", "Punishment", "Sunlight"]),
    BK("sea-the-sea", "The Sea, the Sea", "大海啊，大海", "Iris Murdoch", "艾丽丝·默多克", "1978", pd=False, aliases=["大海，大海"]),
    BK("midnights-children", "Midnight's Children", "午夜之子", "Salman Rushdie", "萨尔曼·拉什迪", "1981", pd=False, aliases=["午夜的孩子"]),
    BK("satanic-verses", "The Satanic Verses", "撒旦诗篇", "Salman Rushdie", "萨尔曼·拉什迪", "1988", pd=False, aliases=["魔鬼诗篇"]),
    BK("never-let-me-go", "Never Let Me Go", "别让我走", "Kazuo Ishiguro", "石黑一雄", "2005", pd=False, aliases=["莫失莫忘", "Hailsham"]),
    BK("possession-byatt", "Possession", "隐之书", "A. S. Byatt", "A. S. 拜厄特", "1990", pd=False, aliases=["Possession: A Romance", "占有"]),
    BK("white-teeth", "White Teeth", "白牙", "Zadie Smith", "扎迪·史密斯", "2000", pd=False, aliases=["Willesden"]),
    BK("small-island", "Small Island", "小岛", "Andrea Levy", "安德烈娅·利维", "2004", pd=False, aliases=["Windrush"]),
    BK("line-of-beauty", "The Line of Beauty", "美丽曲线", "Alan Hollinghurst", "艾伦·霍林赫斯特", "2004", pd=False, aliases=["美丽线条"]),
    BK("wolf-hall", "Wolf Hall", "狼厅", "Hilary Mantel", "希拉里·曼特尔", "2009", pd=False, aliases=["Thomas Cromwell", "托马斯·克伦威尔"]),
    BK("bring-up-the-bodies", "Bring Up the Bodies", "提堂", "Hilary Mantel", "希拉里·曼特尔", "2012", pd=False, aliases=["Anne Boleyn", "安妮·博林"]),
    BK("sense-of-an-ending", "The Sense of an Ending", "终结的感觉", "Julian Barnes", "朱利安·巴恩斯", "2011", pd=False),
    BK("birthday-letters", "Birthday Letters", "生日信札", "Ted Hughes", "特德·休斯", "1998", pd=False, aliases=["St Botolph's", "Sylvia Plath"]),
    BK("lord-of-the-flies", "Lord of the Flies", "蝇王", "William Golding", "威廉·戈尔丁", "1954", pd=False),
    BK("clockwork-orange", "A Clockwork Orange", "发条橙", "Anthony Burgess", "安东尼·伯吉斯", "1962", pd=False, aliases=["发条橘子"]),
    BK("curious-incident", "The Curious Incident of the Dog in the Night-Time", "深夜小狗神秘事件", "Mark Haddon", "马克·哈登", "2003", pd=False,
       aliases=["The Curious Incident", "深夜小狗离奇事件"]),
    BK("war-of-the-worlds", "The War of the Worlds", "世界大战", "H. G. Wells", "H. G. 威尔斯", "1898", 36, aliases=["星际战争", "Martians"]),
    BK("hamnet", "Hamnet", "哈姆奈特", "Maggie O'Farrell", "玛吉·奥法雷尔", "2020", pd=False),
    BK("milkman", "Milkman", "送奶工", "Anna Burns", "安娜·伯恩斯", "2018", pd=False),
]

# ---------------------------------------------------------------- new places (coordinates: the Commons category, or the camera location of a Commons photo)
COORD = json.load(open(sys.argv[3], encoding="utf-8")) if len(sys.argv) > 3 else {}

def at(pid, default):
    """coordinates and source for a place whose position comes from a geotagged photo (filled from COORD) or a category"""
    if pid in COORD:
        c = COORD[pid]
        return c["lat"], c["lon"], c["st"], c["su"]
    return default

places = [
    PIL("shakespeares-globe", "Shakespeare's Globe", "莎士比亚环球剧场", 51.5081, -0.0972, *cat("Shakespeare's Globe"),
        "A reconstruction of the open-air playhouse that Shakespeare's company built on Bankside in 1599, opened in 1997 about 230 metres from the original site. Hamlet was among the first plays written for the old Globe, with Richard Burbage as the prince, and a playgoer recorded seeing Macbeth there in 1611. The audience still stands in the open yard",
        "莎士比亚剧团 1599 年在南岸建起的露天剧场的复建版，1997 年开放，距原址约 230 米。《哈姆雷特》是为老环球剧场写的头几部戏之一，理查德·伯比奇演王子；1611 年有观众记下在这里看了《麦克白》。如今观众仍站在露天的场子里看戏",
        ["hamlet", "macbeth", "king-lear"]),
    PROTO("white-lion-upton", "The White Lion, Upton-upon-Severn", "塞文河畔厄普顿 · 白狮旅店", 52.063533, -2.217312, *cat("The White Lion, Upton upon Severn"),
          "The inn at Upton in Tom Jones. A coaching inn on the High Street of this small Severn town, rebuilt in the mid-18th century; its listing records the old claim that this is the inn where Fielding sets the night of farce at the centre of the novel. It still takes guests",
          "《汤姆·琼斯》里厄普顿客栈的原型。塞文河畔小镇大街上的驿站旅店，18 世纪中叶重建；英格兰历史建筑名录记着一个老说法：菲尔丁把全书正中那一夜的闹剧就放在这家店里。如今仍是旅馆"),
    ORIG("gilbert-whites-house", "Gilbert White's House, Selborne", "塞耳彭 · 吉尔伯特·怀特故居", 51.0976, -0.943397, *cat("The Wakes, Selborne"),
         "The Wakes, where Gilbert White lived nearly all his life and wrote the letters that became The Natural History of Selborne. Behind the house rises the Hanger, the beech wood he climbed by the Zig-Zag path that he and his brother John cut in 1753. The house and garden are now a museum",
         "韦克斯宅，吉尔伯特·怀特几乎一生都住在这里，写下后来编成《塞耳彭自然史》的那些信。屋后就是他常爬的山毛榉坡林“悬林”，那条“之字路”是他和弟弟约翰 1753 年开出来的。故居和花园现在是博物馆"),
    ORIG("arthurs-seat", "Arthur's Seat", "亚瑟王座", 55.944167, -3.161944, *cat("Arthur's Seat"),
         "The 251-metre summit of an extinct volcano in Holyrood Park, a stiff walk from the Royal Mile. Hogg sends George Colwan up it before dawn, and on the summit, in the mist, he meets his persecuting brother. Scott's Jeanie Deans keeps a midnight tryst below its crags, and in Frankenstein Clerval admires it on the way north",
         "荷里路德公园里的一座死火山，主峰海拔 251 米，从皇家英里大道走上去要费些力气。霍格让乔治·科尔万天亮前登顶，在山顶的雾里撞见一直纠缠他的弟弟。司各特让珍妮·迪恩斯半夜在山崖下赴约，《弗兰肯斯坦》里的克莱瓦尔北上时也在这里流连"),
    ORIG("pantheon-oxford-street", "Oxford Street at the Pantheon", "牛津街 · 万神殿旧址", 51.515058, -0.137988, *cat("The Pantheon (Marks & Spencer), 169-173 Oxford Street"),
         "Marks & Spencer's store at 173 Oxford Street stands on the site of the Pantheon, an 18th-century assembly room. On a wet Sunday in 1804 De Quincey, an Oxford student visiting London with toothache, bought his first opium from a druggist near here. Two years before, homeless at seventeen, he had walked this street night after night with Ann, a young girl of the streets who saved his life and then vanished",
         "牛津街 173 号的玛莎百货所在地，原是 18 世纪的万神殿舞厅。1804 年一个下雨的星期天，在牛津读书、来伦敦时正闹牙痛的德·昆西在这附近的药铺里买到第一份鸦片。两年前他十七岁流落伦敦，曾和街头少女安夜夜在这条街上游荡；她救过他的命，后来却再也找不到了"),
    PROTO("walpole-house", "Walpole House, Chiswick Mall", "奇斯威克林荫道 · 沃波尔宅", 51.4884, -0.246185, *cat("Walpole House, Chiswick Mall, London"),
          "Miss Pinkerton's academy for young ladies, where Vanity Fair opens. Thackeray went to school on Chiswick Mall as a boy, and this late-17th-century house on the Thames, where Charles II's mistress Barbara Villiers died, is the one usually named as the model. It is private; see it from the riverside lane",
          "《名利场》开篇平克顿女子学堂的原型。萨克雷小时候在奇斯威克林荫道上过学，这座泰晤士河边 17 世纪末的宅子——查理二世的情妇芭芭拉·维利尔斯死在这里——通常被认作学堂的样本。私宅，可以在河边小路上看"),
    ORIG("blackfriars-bridge", "Blackfriars Bridge", "黑衣修士桥", 51.509722, -0.104444, *cat("Blackfriars Bridge"),
         "A bridge has crossed the Thames here since 1769; the present one, iron arches on granite piers, opened in 1869. In Daniel Deronda the dying scholar Mordecai, who has long dreamed of a younger man who will come to him and carry on his vision, waits on the bridge at sunset and sees Deronda rowing towards him down the river",
         "这里自 1769 年起就有桥跨过泰晤士河，现在这座铁拱石墩的桥 1869 年通车。《丹尼尔·德龙达》里病重的学者莫德凯，多年来一直梦想有个年轻人会来继承他的理想；黄昏时他在桥上等候，看见德龙达从上游划船而来"),
    ORIG("grosvenor-square", "Grosvenor Square", "格罗夫纳广场", 51.511389, -0.151389, *cat("Grosvenor Square"),
         "A Mayfair square laid out in the 1720s and long one of London's grandest addresses; the old United States embassy fills its west side. Trollope gives a house here to Augustus Melmotte, the swindling financier of The Way We Live Now, who throws a great dinner for the Emperor of China just as the rumours of forgery begin",
         "梅费尔区的广场，1720 年代建成，向来是伦敦最显赫的地址之一，西侧是原美国大使馆。特罗洛普把这里的一栋宅子给了《如今世道》里的诈骗金融家梅尔莫特：他在这里大宴来访的中国皇帝，正赶上伪造文书的流言四起"),
    PIL("down-house", "Down House, Darwin's home", "唐恩宅 · 达尔文故居", 51.331389, 0.053333, *cat("Down House"),
        "Darwin's home for forty years, from 1842 until his death in 1882, in the Kent village of Downe. He wrote On the Origin of Species here, and walked the Sandwalk, the gravel path round a little wood at the bottom of the garden, every day to think. English Heritage keeps his study as he left it",
        "达尔文从 1842 年住到 1882 年去世，整整四十年，在肯特郡唐恩村。《物种起源》就在这里写成；他每天都沿花园尽头小树林外的“沙径”走上几圈，边走边想。英格兰遗产委员会把他的书房保留成原样",
        ["origin-of-species", "voyage-of-the-beagle"]),
    PROTO("weyhill", "Weyhill", "韦希尔", 51.217778, -1.546944, *cat("Weyhill"),
          "Weydon-Priors in The Mayor of Casterbridge. Weyhill Fair, held every autumn on the down here from the Middle Ages into the 20th century, was one of the great sheep and hiring fairs of England. Hardy made it the fair where the drunken hay-trusser Michael Henchard sells his wife and baby daughter to a sailor for five guineas",
          "《卡斯特桥市长》里韦敦普赖尔斯的原型。从中世纪到 20 世纪，每年秋天这里的丘地上都有韦希尔集市，是英格兰数一数二的羊市和雇工集市。哈代让醉酒的捆草工亨查德在这场集市上把妻子和襁褓中的女儿卖给一个水手，价钱五个畿尼"),
    ORIG("victoria-station", "London Victoria station", "伦敦维多利亚车站", 51.495005, -0.143577, *cat("London Victoria station"),
         "The terminus of the line to Brighton since 1860, now one of Britain's busiest stations. In The Importance of Being Earnest Jack Worthing admits that he was found as a baby in a handbag in the cloakroom here, on the Brighton line, and Lady Bracknell's horrified 'A handbag?' became one of the best-known lines in English comedy",
         "1860 年起就是去布莱顿的铁路的终点站，如今是全英最繁忙的车站之一。《不可儿戏》里杰克·沃辛承认，自己是婴儿时在这里布莱顿线的行李寄存处被人发现的，装在一只手提包里；布拉克内尔夫人那声惊愕的“手提包？”成了英国喜剧里最出名的台词之一"),
    ORIG("bm-reading-room", "British Museum Reading Room", "大英博物馆阅览室", 51.519444, -0.126944, *cat("British Museum Reading Room"),
         "The great round reading room under its huge dome, opened in 1857. For 140 years writers and scholars worked here, Marx and Gissing among them; the books moved to the new British Library in 1997, and the room now stands in the middle of the Great Court. In New Grub Street it is where hack writers grind out copy to stay alive",
         "1857 年开放的圆形大阅览室，顶上是一座巨大的穹顶。一百四十年间无数作家学者在这里埋头，马克思和吉辛都是常客；1997 年藏书搬去新的大英图书馆，阅览室如今立在大中庭中央。在《新寒士街》里，这是穷文人为糊口拼命赶稿的地方"),
    ORIG("gravesend", "Gravesend and the Thames estuary", "格雷夫森德 · 泰晤士河口", 51.4454, 0.3697, *cat("Gravesend Town Pier"),
         "The Kent town where the Thames widens into its sea-reach, and where for centuries outward-bound ships took on river pilots. Heart of Darkness opens on the cruising yawl Nellie, waiting at anchor for the tide as dusk falls over Gravesend, as Marlow begins his story. Pocahontas is buried in St George's church here",
         "肯特郡小镇，泰晤士河在这里变宽、通向入海口，几百年来出海的船都在这里雇领航员。《黑暗的心》开篇，游艇“内莉号”停在格雷夫森德外的河面上等潮水，暮色降临，马洛开始讲他的故事。宝嘉康蒂就葬在镇上的圣乔治教堂"),
    PIL("conrad-grave", "Joseph Conrad's grave, Canterbury", "坎特伯雷 · 康拉德墓", 51.28578, 1.06404,
        "Canterbury City Cemetery (Commons photo 'Joseph Conrad grave', camera location 51.28578, 1.06404)", C + "File:Joseph_Conrad_grave.jpg",
        "Conrad, born in Poland, spent twenty years at sea before settling in Kent, where he wrote his great novels. He died at Bishopsbourne in 1924 and lies in Canterbury City Cemetery under a granite stone carved with lines from Spenser: 'Sleep after toyle, port after stormie seas'",
        "康拉德生于波兰，航海二十年后定居肯特，在这里写出了他最重要的小说。1924 年他在毕晓普斯伯恩去世，葬在坎特伯雷市立公墓，花岗岩墓碑上刻着斯宾塞的诗句：“劳作后安眠，风浪后进港”",
        ["heart-of-darkness", "nostromo"]),
    PROTO("moorgreen-reservoir", "Moorgreen Reservoir", "穆尔格林水库", 53.035, -1.283, *cat("Moorgreen Reservoir"),
          "Willey Water in Women in Love. The reservoir was built to feed the Nottingham Canal, beside Lamb Close, the house of the colliery-owning Barber family, which Lawrence turned into the Criches' Shortlands. At the Criches' water-party Gerald's young sister Diana falls from the launch and drowns, dragging down the young man who dives in after her",
          "《恋爱中的女人》里“威利湖”的原型。水库当年是为诺丁汉运河供水而建，旁边的兰姆克洛斯宅属于开煤矿的巴伯家，劳伦斯把它写成克里奇家的肖特兰兹。克里奇家办水上宴会那晚，杰拉德的小妹黛安娜从汽艇上落水，把跳下去救她的年轻人也拖进了水底"),
    PROTO("whitstable", "Whitstable", "惠特斯特布尔", 51.3558, 1.03969, *cat("All Saints Church, Whitstable"),
          "Blackstable in Of Human Bondage. Orphaned at ten, Maugham was sent here in 1884 to live with his uncle, the vicar of All Saints, and was unhappy; the oyster town became Blackstable, and nearby Canterbury, where he boarded at the King's School, became Tercanbury. Philip Carey, his club-footed double, follows the same road",
          "《人性的枷锁》里布莱克斯泰布尔的原型。毛姆十岁成了孤儿，1884 年被送到这里跟当牧师的叔叔过，日子很不快活；这个产牡蛎的小镇成了“布莱克斯泰布尔”，附近他寄宿读书的坎特伯雷国王学校成了“特坎伯里”。跛足的菲利普·凯里走的正是他走过的路"),
    ORIG("newnham-college", "Newnham College, Cambridge", "剑桥纽纳姆学院", 52.2, 0.1075, *cat("Newnham College, Cambridge"),
         "Founded in 1871, one of the first Cambridge colleges for women. In October 1928 Virginia Woolf gave the talks here and at Girton that became A Room of One's Own; in the book Newnham becomes Fernham, where she eats a plain dinner after a lavish lunch at a men's college. Sylvia Plath studied here in 1955–57",
         "1871 年创立，剑桥最早的女子学院之一。1928 年 10 月伍尔夫在这里和格顿学院作了两场演讲，后来写成《一间自己的房间》；书里纽纳姆化名“芬纳姆”，她在男子学院吃过丰盛的午餐，晚上在这里只有一顿寒素的晚饭。普拉斯 1955—1957 年在这里读书"),
    PROTO("rooks-nest", "Rooks Nest House, Stevenage", "斯蒂夫尼奇 · 鲁克斯巢", 51.9251, -0.191778, *cat("Rooks Nest House, Stevenage"),
          "Howards End. Forster lived in this farmhouse on the edge of Stevenage from the age of four to fourteen, and rebuilt it in the novel down to the great wych elm with pigs' teeth driven into its bark, which country people chewed to cure toothache. The house is private, but the fields around it are still known as 'Forster Country'",
          "霍华德庄园的原型。福斯特四岁到十四岁住在斯蒂夫尼奇边上的这座农舍，后来把它原样写进小说，连那棵树皮里嵌着猪牙的大榆树都在——乡下人说嚼一嚼树皮能治牙痛。房子是私宅，四周的田野至今被称作“福斯特乡野”"),
    PIL("forster-kings", "King's College, Cambridge: E. M. Forster's college", "剑桥国王学院 · 福斯特的学院", 52.204167, 0.116667, *cat("King's College, Cambridge"),
        "Forster read classics and history at King's from 1897 to 1901, and came back in 1946 as an honorary fellow, making the college his home for the rest of his life; he died in 1970. His papers are kept in the college archive",
        "福斯特 1897 到 1901 年在国王学院读古典学和历史，1946 年作为荣誉院士回来，此后学院就是他的家，直到 1970 年去世。他的手稿和文件都收藏在学院档案馆",
        ["howards-end", "a-room-with-a-view", "passage-to-india"]),
    ORIG("cromer", "Cromer", "克罗默", 52.9343, 1.30162, *cat("Cromer Pier"),
         "A Victorian resort on the north Norfolk coast, known for its pier and its crabs. At Hailsham, Norfolk was 'England's lost corner', where the children believed lost things ended up. In Never Let Me Go the friends drive to Cromer to find Ruth's 'possible', and Kathy and Tommy go round the second-hand shops and find a copy of her lost tape",
         "诺福克北岸的维多利亚时代海滨小镇，以码头和螃蟹出名。在黑尔舍姆，诺福克被叫作“英格兰的失物角”，孩子们相信丢了的东西最后都会到那里。《别让我走》里几个朋友开车来克罗默寻找露丝的“原型”，凯茜和汤米在二手店里真的找到了她当年丢掉的那盘磁带"),
    ORIG("london-library", "The London Library", "伦敦图书馆", 51.50735, -0.13685, *cat("London Library"),
         "An independent lending library founded in 1841 at Thomas Carlyle's urging and in St James's Square since 1845, with more than a million books on open shelves. Possession begins here: Roland Michell takes down the poet Randolph Henry Ash's own copy of Vico and finds two drafts of a letter to an unknown woman folded inside, and slips them into his pocket",
         "1841 年在卡莱尔倡议下创办的独立借阅图书馆，1845 年起设在圣詹姆斯广场，开架藏书一百多万册。《隐之书》从这里开始：罗兰·米歇尔取下诗人艾许本人读过的那本维柯，发现里面夹着两份写给一位陌生女子的信稿，便揣进了自己的口袋"),
    ORIG("cricklewood-broadway", "Cricklewood Broadway", "克里克尔伍德大街", 51.55679, -0.21534, *cat("Cricklewood Broadway"),
         "A stretch of the Roman road Watling Street, now the A5, through north-west London. White Teeth opens here early on New Year's Day 1975, with Archie Jones trying to gas himself in his car outside a halal butcher's until the butcher hauls him out. Saved, Archie goes on to a party, meets Clara, and the long story of two Willesden families begins",
         "古罗马大道沃特林街的一段，如今是 A5 公路，穿过伦敦西北。《白牙》开篇是 1975 年元旦清早，阿奇·琼斯在这里一家清真肉铺门口的车里开煤气自杀，被肉铺老板拖了出来。捡回一命的阿奇去了一个派对，遇见克拉拉，威尔斯登两个家庭的长故事由此开始"),
    ORIG("nevern-square", "Nevern Square, Earls Court", "厄尔斯考特 · 内文广场", 51.49185, -0.19742,
         "Nevern Square (Commons photo 'Gates of Nevern Square, Earl's Court', object location 51.49185, -0.19742)", C + "File:Gates_of_Nevern_Square,_Earl%27s_Court_-_geograph.org.uk_-_2737980.jpg",
         "A garden square of tall Victorian houses by Earls Court station, part of a cluster of Nevern streets where rooms were cheap after the war. Small Island puts Queenie Bligh's lodging house at 21 Nevern Street: in 1948, her husband still missing, she takes in Jamaican lodgers, among them the ex-RAF man Gilbert Joseph, whose new wife Hortense arrives from Kingston expecting far more",
         "厄尔斯考特车站旁一座维多利亚式高楼围成的花园广场，周围几条街都以“内文”为名，战后这一带的房间很便宜。《小岛》把奎妮·布莱的出租屋放在内文街 21 号：1948 年，丈夫还下落不明，她把房间租给牙买加房客，其中有当过皇家空军的吉尔伯特·约瑟夫；他新婚的妻子霍滕丝从金斯敦赶来，期望可比这高得多"),
    ORIG("kensington-park-gardens", "Kensington Park Gardens, Notting Hill", "诺丁山 · 肯辛顿公园花园街", 51.51116, -0.20406, *cat("Kensington Park Gardens"),
         "A street of grand Italianate houses on the Ladbroke estate in Notting Hill. The Line of Beauty puts the Feddens here: in 1983 Nick Guest, just down from Oxford, moves into the top of their house, and at their silver-wedding party Margaret Thatcher herself dances with him",
         "诺丁山拉德布罗克庄园上一条意大利式豪宅街。《美丽曲线》把费登家安在这里：1983 年，刚从牛津毕业的尼克·盖斯特住进他们家的顶楼；在主人的银婚派对上，撒切尔夫人亲自和他跳了一支舞"),
    ORIG("putney", "Putney", "帕特尼", 51.46329, -0.21582, *cat("Putney High Street"),
         "A riverside village on the south bank of the Thames, where Thomas Cromwell was born around 1485, son of Walter, a brewer, blacksmith and brawler. Wolf Hall opens here in 1500, with the boy Thomas lying on the cobbles of his father's yard after a beating, and deciding to leave England",
         "泰晤士河南岸的河边村镇，托马斯·克伦威尔约 1485 年生在这里，父亲沃尔特酿酒、打铁，还爱打架。《狼厅》开篇是 1500 年的帕特尼：少年托马斯被父亲打得趴在院子的石子地上，决定离开英格兰"),
    ORIG("falcon-yard", "Falcon Yard (now Lion Yard), Cambridge", "剑桥鹰院（今狮院）", 52.2047, 0.12075, *cat("Lion Yard, Cambridge"),
         "On 25 February 1956 the student magazine St Botolph's Review held its launch party in a hall off Falcon Yard. Sylvia Plath, then at Newnham, met Ted Hughes there and bit his cheek hard enough to draw blood. Falcon Yard was demolished for the Lion Yard shopping centre in the 1970s; Hughes went back to that night in his poem 'St Botolph's'",
         "1956 年 2 月 25 日，学生刊物《圣博托尔夫评论》在鹰院旁的礼堂开创刊派对。当时在纽纳姆学院读书的普拉斯在这里认识了特德·休斯，一口咬在他脸上，咬出了血。鹰院 1970 年代被拆，建成狮院购物中心；休斯在《圣博托尔夫》一诗里重回那一夜"),
    PIL("bishop-wordsworths", "Bishop Wordsworth's School, Salisbury", "索尔兹伯里 · 主教华兹华斯学校", 51.0647, -1.7975, *cat("Bishop Wordsworth's School"),
        "A boys' grammar school in Salisbury's Cathedral Close, where William Golding taught English before and after his war service in the navy, until 1961. He wrote Lord of the Flies, published in 1954, while teaching here",
        "索尔兹伯里大教堂内院里的一所男子文法学校。威廉·戈尔丁战前就在这里教英语，战时去海军服役，战后回来一直教到 1961 年。1954 年出版的《蝇王》就是他在这里教书时写的",
        ["lord-of-the-flies"]),
    b.P("southmere", "Southmere Lake, Thamesmead", "泰晤士米德 · 南湖", 51.49974, 0.12621,
        "Southmere Lake (Commons photo 'Southmere Lake, Thamesmead', object location 51.49974, 0.12621)", C + "File:Southmere_Lake,_Thamesmead_-_geograph.org.uk_-_4820807.jpg", "film_location",
        adaptation=dict(title="A Clockwork Orange", year=1971, kind="电影"),
        scene="亚历克斯和他的“德鲁格”们沿湖边走，他突然出手把乔治和迪姆打进湖里，好让他们知道谁说了算，又在拉迪姆上岸时用刀划伤了他的手。泰晤士米德当年是刚建成的粗野主义新城",
        scene_en="the lakeside walk where Alex, to show his droogs who is in charge, suddenly knocks Georgie and Dim into the water, then slashes Dim's hand with his knife as he helps him out. Thamesmead was a brand-new Brutalist town at the time",
        book_ids=["clockwork-orange"]),
    ORIG("horsell-common", "Horsell Common, Woking", "沃金 · 霍塞尔公地", 51.3358, -0.548333, *cat("Horsell Common"),
         "Heath and pine woods just north of Woking, where Wells lived in 1895–96 while writing The War of the Worlds. The first Martian cylinder crashes into the sandpit here, and the crowd that gathers to stare is burned by the Heat-Ray. A seven-metre steel Martian fighting-machine stands in Woking town centre",
         "沃金北边的一片石楠荒地和松林，威尔斯 1895—1896 年住在沃金，写下《世界大战》。第一个火星人圆筒就砸进这里的沙坑，围观的人群被热射线烧死。沃金市中心如今立着一台七米高的不锈钢火星人战斗机器"),
]

# ---------------------------------------------------------------- lines
def hamlet_line():
    raw = b.norm(open(f"{TX}/1524.txt", encoding="utf-8").read().replace("\r", ""))
    parts = [("HAMLET", "Ay, marry, why was he sent into England?"),
             ("FIRST CLOWN", "Why, because he was mad; he shall recover his wits there; or if he do not, it's no great matter there."),
             ("HAMLET", "Why?"),
             ("FIRST CLOWN", "'Twill not be seen in him there; there the men are as mad as he.")]
    flat = " ".join(raw.split())
    seq = " ".join(f"{who}. {what}" for who, what in parts)
    assert seq in flat, "Hamlet passage not found verbatim"
    return "\n".join(f"{who}. {what}" for who, what in parts)

ham = b.L("hml-1", "hamlet", "shakespeares-globe", "Act 5, Scene 1 (the gravedigger)", "第五幕第一场（掘墓人）", hamlet_line(), ["England"], 1524)

SB = "https://standardebooks.org/ebooks/"
lines = [ham,
    S("tj-s1", "tom-jones", "white-lion-upton", "Books 9–10", "第九至十卷",
      "Tom brings Mrs Waters, whom he has just rescued on Mazard Hill, to the inn at Upton. In one night an Irishman bursts into the wrong bedroom hunting for his runaway wife, and Sophia arrives, learns that Tom is upstairs with another woman, and leaves her muff on his bed as a sign that she has been there.",
      "汤姆把刚在马泽德山救下的沃特斯太太带到厄普顿的客栈。就在这一夜，一个爱尔兰人追着私逃的妻子闯错了卧房；苏菲亚也来了，听说汤姆正和别的女人在楼上，就把自己的手笼留在他床上，表示她来过。",
      ["inn at Upton"], ["厄普顿的客栈"], "https://historicengland.org.uk/listing/the-list/list-entry/1226619"),
    S("nhs-s1", "natural-history-of-selborne", "gilbert-whites-house", "Letter 1 to Thomas Pennant", "致彭南特第 1 封信",
      "White begins by describing his parish: the village lies under a chalk hill three hundred feet high, covered by a long hanging wood of beech called the Hanger, and the beech, he says, is the loveliest of all forest trees.",
      "怀特一开头先描绘自己的教区：村子卧在一座高三百英尺的白垩山下，山坡上是一片叫作“悬林”的狭长山毛榉林；他说山毛榉是林中最美的树。",
      ["the Hanger"], ["悬林"], G + "1408"),
    S("jsn-s1", "justified-sinner", "arthurs-seat", "The Editor's Narrative", "编者的叙述",
      "George climbs Arthur's Seat at dawn to be alone. On the summit the sun turns the mist into a bright halo, and in it looms a gigantic, distorted image of his brother Robert's face; he turns in terror and finds Robert himself creeping up behind him on the edge of the crag.",
      "乔治天刚亮就爬上亚瑟王座，想一个人待着。山顶上，阳光把雾气照成一圈光晕，光晕里浮现出弟弟罗伯特一张巨大而扭曲的脸；他吓得回身，发现罗伯特本人正从背后向崖边悄悄逼近。",
      ["Arthur's Seat"], ["亚瑟王座"], "https://jameshoggblog.blogspot.com/2014/10/in-footsteps-of-justified-sinner-part-2.html"),
    S("oe-s1", "opium-eater", "pantheon-oxford-street", "Preliminary Confessions", "初步的自白",
      "Sitting with Ann on a doorstep in Soho Square, the starving boy faints; she runs into Oxford Street and comes back with a glass of port wine and spices, paid for out of her own nearly empty purse. He leaves London for a few days, and when he comes back to look for her in the crowds of Oxford Street, she has gone for ever.",
      "饿坏了的少年和安坐在苏豪广场的门阶上，忽然昏了过去；她跑到牛津街，用自己少得可怜的钱买回一杯加了香料的波特酒。他离开伦敦几天，回来后在牛津街的人潮里找她，却再也没有找到。",
      ["Oxford Street"], ["牛津街"], W + "Confessions_of_an_English_Opium-Eater"),
    S("vf-s1", "vanity-fair", "walpole-house", "Chapter 1, Chiswick Mall", "第 1 章《奇斯威克林荫道》",
      "Becky Sharp and Amelia Sedley leave Miss Pinkerton's academy in the Sedleys' coach. Miss Jemima pushes a copy of Johnson's Dictionary through the window as a parting present for Becky, who flings it back into the garden as the coach drives off.",
      "蓓基·夏泼和爱米丽亚·赛特笠坐着赛特笠家的马车离开平克顿女子学堂。吉米玛小姐从车窗塞进一本约翰逊博士的《字典》送给蓓基，马车一动，蓓基就把它扔回了学堂的花园。",
      ["Miss Pinkerton's academy"], ["平克顿女子学堂"], "https://www.chiswickbookfestival.net/?p=4316"),
    S("vil-s1", "villette", "st-pauls", "Chapter 6, London", "第 6 章《伦敦》",
      "Lucy Snowe, alone in London for the first time, wakes in an old inn in the City and sees the dome of St Paul's from her window. She goes straight there, climbs up into the dome, and looks out over the river, the bridges and the Temple Gardens.",
      "露西·斯诺第一次独自来到伦敦，在城里一家老旅店醒来，从窗口望见圣保罗大教堂的穹顶。她当天就去了，一直爬上穹顶，俯瞰泰晤士河、一座座桥和圣殿花园。",
      ["St Paul's"], ["圣保罗大教堂"], SB + "charlotte-bronte/villette/text/chapter-6"),
    S("dd-s1", "daniel-deronda", "blackfriars-bridge", "Chapter 40", "第 40 章",
      "Deronda rows down from Chelsea in the fading afternoon, meaning to land at Blackfriars Bridge. Mordecai is waiting there, leaning on the parapet; the young man coming to him across the water at sunset is exactly the vision he has carried for years.",
      "暮色渐起，德龙达从切尔西划船顺流而下，打算在黑衣修士桥靠岸。莫德凯正倚着桥栏等候；夕阳中从水上向他而来的年轻人，正是他多年来心中的幻象。",
      ["Blackfriars Bridge"], ["黑衣修士桥"], SB + "george-eliot/daniel-deronda/text/chapter-40"),
    S("bt-s1", "barchester-towers", "salisbury", "Mrs Proudie's reception", "普劳迪夫人的招待会",
      "At the new bishop's reception in the palace at Barchester, Bertie Stanhope pushes the sofa on which his sister, the Signora Neroni, is reclining; a castor catches Mrs Proudie's lace train and tears it away. 'Unhand it, sir!' cries Mrs Proudie.",
      "新主教在巴彻斯特的主教府开招待会。伯蒂·斯坦诺普推动妹妹内罗尼夫人斜倚着的沙发，一只小脚轮钩住普劳迪夫人的蕾丝裙裾，把它整片扯了下来。“放手，先生！”普劳迪夫人大叫。",
      ["Barchester"], ["巴彻斯特"], W + "Barchester_Towers"),
    S("wwl-s1", "way-we-live-now", "grosvenor-square", "The dinner for the Emperor of China", "宴请中国皇帝",
      "Melmotte's banquet for the Emperor of China at his house in Grosvenor Square is meant to crown his triumph. But that afternoon the rumour runs through London that he has forged a deed, and many of the great guests stay away; the Emperor sits through it all in silence.",
      "梅尔莫特在格罗夫纳广场的宅子里宴请中国皇帝，本该是他的登峰之作。可就在当天下午，他伪造地契的流言传遍伦敦，许多显贵干脆没来；皇帝从头到尾一言不发。",
      ["Grosvenor Square"], ["格罗夫纳广场"], W + "The_Way_We_Live_Now"),
    S("oos-s1", "origin-of-species", "down-house", "Chapter 14, Recapitulation and Conclusion", "第 14 章《复述与结论》",
      "The book ends with an entangled bank: plants of many kinds, birds singing in the bushes, insects flitting about and worms crawling through the damp earth, so different and so dependent on one another, and all produced by the laws Darwin has set out. There is grandeur, he says, in this view of life.",
      "全书以一道“纠缠的河岸”收尾：岸上长满各种植物，鸟在灌木间歌唱，昆虫飞来飞去，蚯蚓在湿土里爬行；它们彼此如此不同、又如此相互依存，却都出自他在书里阐明的那些法则。他说，这样看待生命，自有一种壮丽。",
      ["entangled bank"], ["纠缠的河岸"], G + "1228"),
    S("jto-s1", "jude-the-obscure", "oxford", "Part 6, Chapter 2", "第六部第 2 章",
      "Back in Christminster with their children, Jude and Sue can find no lodgings that will take a family, and Sue tells the boy called Little Father Time that there are too many children. Next morning he has hanged the two little ones and himself, leaving a note: 'Done because we are too menny.'",
      "裘德和苏带着孩子回到基督寺，找不到肯收留一家人的住处；苏对那个叫“小时光老人”的男孩说，家里孩子太多了。第二天早上，他吊死了两个弟妹和自己，留下一张字条：“因为我们太多了。”",
      ["Christminster"], ["基督寺"], W + "Jude_the_Obscure"),
    S("moc-s1", "mayor-of-casterbridge", "weyhill", "Chapter 1", "第 1 章",
      "At the fair at Weydon-Priors, Henchard, drunk on rum-laced furmity in a tent, offers his wife Susan for sale. A sailor lays five guineas on the table and leads her and the baby away; next morning, sober, Henchard swears an oath not to touch strong drink for twenty-one years.",
      "在韦敦普赖尔斯的集市上，亨查德在帐篷里喝多了掺朗姆酒的麦粥，当众要把妻子苏珊卖掉。一个水手把五个畿尼拍在桌上，领着她和孩子走了；第二天酒醒，亨查德发誓二十一年滴酒不沾。",
      ["Weydon-Priors"], ["韦敦普赖尔斯"], W + "The_Mayor_of_Casterbridge"),
    S("moc-s2", "mayor-of-casterbridge", "dorchester-casterbridge", "Chapter 5", "第 5 章",
      "Years later Susan and her grown daughter Elizabeth-Jane walk into Casterbridge and, looking through the window of the King's Arms, see Henchard at the head of a public dinner. He is now the mayor.",
      "多年以后，苏珊和长大的女儿伊丽莎白－简走进卡斯特桥，隔着国王纹章旅店的窗子，看见亨查德坐在一场公宴的主位上——他已经是市长了。",
      ["Casterbridge"], ["卡斯特桥"], W + "The_Mayor_of_Casterbridge"),
    S("ash-s1", "adventures-of-sherlock-holmes", "baker-street", "A Scandal in Bohemia", "《波希米亚丑闻》",
      "Married and living elsewhere, Watson is returning from a patient one night in March 1888 when his way leads him through Baker Street. Passing the well-remembered door, he sees Holmes's tall, spare figure pacing the lit window, and goes up, in time for the King of Bohemia.",
      "华生婚后已经搬走。1888 年 3 月的一个夜晚，他出诊回来路过贝克街，望见那扇熟悉的门上方窗子亮着，福尔摩斯高瘦的身影在里面来回踱步，便上了楼——正赶上波希米亚国王来访。",
      ["Baker Street"], ["贝克街"], G + "1661"),
    S("dp-s1", "de-profundis", "reading-gaol", "Reading Gaol, January–March 1897", "雷丁监狱，1897 年 1—3 月",
      "Prisoner C.3.3 is at last allowed pen and paper, and over the first months of 1897 writes a long letter to Lord Alfred Douglas, reproaching him and examining his own fall. He carries it out of prison on his release and gives it to Robert Ross, who publishes part of it in 1905 as De Profundis.",
      "监狱终于允许 C.3.3 号囚犯用纸笔。1897 年头几个月，他在牢房里给阿尔弗雷德·道格拉斯勋爵写了一封长信，既责备对方，也审视自己的沉沦。出狱时他带着手稿，交给罗伯特·罗斯；1905 年罗斯把其中一部分以《自深深处》为题出版。",
      ["C.3.3"], ["C.3.3"], W + "De_Profundis_(letter)"),
    S("ibe-s1", "importance-of-being-earnest", "victoria-station", "Act 1", "第一幕",
      "Lady Bracknell interviews Jack as a possible husband for her daughter. Asked about his parents, he confesses that he was found in a handbag in the cloakroom at Victoria Station, on the Brighton line; she advises him to acquire some relations as soon as possible. In Act 3 it turns out that Miss Prism left the baby there by mistake, having put her three-volume novel in the pram instead.",
      "布拉克内尔夫人盘问杰克够不够格娶她女儿。问到父母，他只好坦白：自己是在维多利亚车站布莱顿线那边的行李寄存处，在一只手提包里被人发现的；她劝他赶紧去弄几个亲戚。到第三幕才揭晓，是普丽丝姆小姐一时糊涂，把三卷本小说稿放进了婴儿车，却把婴儿留在了那里。",
      ["Victoria Station"], ["维多利亚车站"], G + "844"),
    S("ngs-s1", "new-grub-street", "bm-reading-room", "Marian in the Reading Room", "玛丽安在阅览室",
      "On a day of yellow London fog, Marian Yule sits in the Reading Room gathering material for her father's articles. Looking round at the other readers, she sees them as flies caught in a vast web, and wonders why a machine should not be invented to turn out literature.",
      "伦敦起了黄雾的一天，玛丽安·尤尔坐在阅览室里替父亲搜集写文章的材料。她环顾四周的读者，觉得他们像困在一张大蛛网里的苍蝇，心想为什么不能发明一台机器来生产文学。",
      ["Reading Room"], ["阅览室"], G + "1709"),
    S("hod-s1", "heart-of-darkness", "gravesend", "Part 1", "第一部",
      "The Nellie lies at anchor in the sea-reach of the Thames, waiting for the tide to turn, while the sky darkens over Gravesend and the great city beyond. Marlow, sitting cross-legged on deck, says that this too has been one of the dark places of the earth, and begins the story of his journey up the Congo.",
      "“内莉号”停在泰晤士河口，等潮水转向，格雷夫森德和远处大都市的上空渐渐暗下来。马洛盘腿坐在甲板上，说这里也曾是地球上的黑暗之地，然后讲起他溯刚果河而上的那段旅程。",
      ["Gravesend"], ["格雷夫森德"], G + "219"),
    S("wil-s1", "women-in-love", "moorgreen-reservoir", "Chapter 14, Water-Party", "第 14 章《水上宴会》",
      "At dusk, during the Criches' water-party on Willey Water, a cry goes up: Diana Crich has fallen from the launch. Gerald dives again and again into the dark water but cannot find her; at dawn she is found drowned, her arms locked round the neck of the young doctor who tried to save her.",
      "黄昏，克里奇家在威利湖上办水上宴会，忽然有人惊叫：黛安娜·克里奇从汽艇上落水了。杰拉德一次次潜进黑水里，却找不到她；天亮时人们捞起她，她的双臂还死死箍着那个下水救她的年轻医生的脖子。",
      ["Willey Water"], ["威利湖"], G + "4240"),
    S("ohb-s1", "of-human-bondage", "whitstable", "Chapters 5–6", "第 5—6 章",
      "Philip Carey, nine years old and newly orphaned, arrives at the vicarage in Blackstable to live with his uncle, the childless vicar, and his timid Aunt Louisa. His club foot and the long, silent Sundays there shape the lonely boyhood that the rest of the book is an escape from.",
      "九岁的菲利普·凯里刚成孤儿，来到布莱克斯泰布尔的牧师宅，跟没有孩子的牧师伯父和胆小的路易莎伯母一起过。跛足和一个个漫长沉默的星期天，造就了他孤独的童年，此后整本书都是他挣脱的过程。",
      ["Blackstable"], ["布莱克斯泰布尔"], W + "Of_Human_Bondage"),
    S("roo-s1", "room-of-ones-own", "newnham-college", "Chapter 1", "第一章",
      "After a luncheon of sole, partridges and wine at a men's college, the narrator dines at Fernham on gravy soup, beef with greens and potatoes, and prunes and custard. The contrast leads to the book's argument: a woman must have money and a room of her own if she is to write fiction.",
      "在男子学院吃过比目鱼、山鹑和美酒的午餐，叙述者晚上在芬纳姆吃的是肉汁清汤、牛肉配青菜土豆，外加梅干蛋奶冻。两相对照，引出全书的论点：女人要写小说，就得有钱，还得有一间自己的房间。",
      ["Fernham"], ["芬纳姆"], W + "A_Room_of_One%27s_Own"),
    S("he-s1", "howards-end", "rooks-nest", "Chapter 44", "第 44 章",
      "At the end, Margaret, her husband Henry, and Helen with her baby son are living together at Howards End, the house Ruth Wilcox had left to Margaret in a pencilled note that the Wilcoxes burnt. The hay is being cut in the meadow, and Margaret learns that the house was meant to be hers all along.",
      "小说结尾，玛格丽特、她的丈夫亨利，还有海伦和她的小儿子，一起住在霍华德庄园。当初露丝·威尔科克斯用铅笔留下字条，把房子留给玛格丽特，威尔科克斯家却把字条烧了；此刻草场上正在割草，玛格丽特才知道这房子本来就该是她的。",
      ["Howards End"], ["霍华德庄园"], W + "Howards_End"),
    S("eoa-s1", "end-of-the-affair", "clapham-common", "Book 3 (Sarah's journal)", "第三卷（萨拉的日记）",
      "June 1944: a flying bomb hits the house on the south side of Clapham Common where Bendrix is with Sarah. Finding him under a fallen door and believing him dead, she kneels and promises God that she will give him up if he lives, and then he walks into the room.",
      "1944 年 6 月，一枚飞弹击中本德里克斯在克拉珀姆公园南边的住处，当时萨拉也在。她看见他被压在倒下的门下，以为他死了，便跪下向上帝发誓：只要他活着，她就离开他——接着他走进了房间。",
      ["Clapham Common"], ["克拉珀姆公园"], W + "The_End_of_the_Affair"),
    S("nlm-s1", "never-let-me-go", "cromer", "Part 2", "第二部",
      "The trip to Cromer to see Ruth's 'possible' ends in disappointment. Afterwards Kathy and Tommy wander the town's second-hand shops and find a copy of Judy Bridgewater's Songs After Dark, the tape Kathy lost at Hailsham: Norfolk really is England's lost corner.",
      "去克罗默看露丝的“原型”，结果令人失望。之后凯茜和汤米在镇上的二手店里闲逛，找到一盘朱迪·布里奇沃特的《Songs After Dark》——正是凯茜在黑尔舍姆丢掉的那盘；诺福克果然是英格兰的失物角。",
      ["Cromer"], ["克罗默"], "https://www.litcharts.com/lit/never-let-me-go/symbols/the-judy-bridgewater-tape"),
    S("pos-s1", "possession-byatt", "london-library", "Chapter 1", "第一章",
      "In the London Library, Roland Michell opens Ash's copy of Vico's Principj di Scienza Nuova and finds two drafts of a passionate letter to an unnamed lady. He steals them, and his search for the woman sets the whole novel going.",
      "在伦敦图书馆，罗兰·米歇尔翻开艾许读过的维柯《新科学》，发现两份写给一位无名女士的炽热信稿。他把它们偷偷带走，寻找这位女士的过程就此展开了整部小说。",
      ["London Library"], ["伦敦图书馆"], W + "Possession_(Byatt_novel)"),
    S("wt-s1", "white-teeth", "cricklewood-broadway", "Chapter 1", "第 1 章",
      "At 6.27 a.m. on 1 January 1975, Archie Jones sits face down on the steering wheel of his car on Cricklewood Broadway, a vacuum-cleaner hose feeding exhaust in through the window. Mo, outside whose halal butcher's he has parked, will not have a suicide on his premises and drags him out.",
      "1975 年 1 月 1 日早上 6 点 27 分，阿奇·琼斯趴在车子的方向盘上，车停在克里克尔伍德大街，一根吸尘器软管把废气引进车窗。车停在穆的清真肉铺门口，穆可不想有人死在他店前，把他拖了出来。",
      ["Cricklewood Broadway"], ["克里克尔伍德大街"], W + "White_Teeth"),
    S("smi-s1", "small-island", "nevern-square", "Hortense, 1948", "霍滕丝 · 1948 年",
      "Hortense arrives at 21 Nevern Street in her best hat and gloves, with a trunk, to join the husband she married in Jamaica, and finds that Gilbert's home in London is one cramped, shabby room.",
      "霍滕丝戴着最好的帽子和手套、带着一口大箱子来到内文街 21 号，投奔在牙买加娶了她的丈夫，却发现吉尔伯特在伦敦的家只是一个又挤又破的单间。",
      ["Nevern Street"], ["内文街"], "https://andrealevy.co.uk/books/small-island"),
    S("lob-s1", "line-of-beauty", "kensington-park-gardens", "Part 2 (1986)", "第二部（1986 年）",
      "At the Feddens' silver-wedding party in Kensington Park Gardens, the Prime Minister arrives. Nick, high on cocaine, asks her to dance, and she accepts: the giddy peak of his life inside the Feddens' world, a year before it falls apart.",
      "费登家在肯辛顿公园花园街办银婚派对，首相来了。吸了可卡因的尼克上前邀她跳舞，她竟答应了——这是他在费登家那个世界里最飘飘然的一刻，一年后一切都崩塌了。",
      ["Kensington Park Gardens"], ["肯辛顿公园花园街"], W + "The_Line_of_Beauty"),
    S("wh-s1", "wolf-hall", "putney", "Part 1: Putney, 1500", "第一部 · 帕特尼，1500 年",
      "Putney, 1500. Fifteen-year-old Thomas lies on the cobbles of his father's yard, half-blinded by blood, while Walter kicks him. He drags himself to his sister's house, and that night decides to run away across the sea to France and the wars.",
      "1500 年，帕特尼。十五岁的托马斯躺在父亲院子的石子地上，血糊住了眼睛，沃尔特还在踢他。他挣扎着爬到姐姐家，当晚就决定渡海去法国，投身战争。",
      ["Putney"], ["帕特尼"], W + "Wolf_Hall"),
    S("bub-s1", "bring-up-the-bodies", "tower-of-london", "The ending, May 1536", "结尾 · 1536 年 5 月",
      "On 19 May 1536 Cromwell stands inside the Tower to watch Anne Boleyn die. The executioner, fetched from Calais for his skill with the sword, takes off her head with a single stroke; the case against her was built by Cromwell himself.",
      "1536 年 5 月 19 日，克伦威尔站在伦敦塔里看安妮·博林受刑。特意从加来请来的剑手一剑斩下她的头——给她定罪的正是克伦威尔自己。",
      ["Tower"], ["伦敦塔"], W + "Bring_Up_the_Bodies"),
    S("bl-s1", "birthday-letters", "falcon-yard", "St Botolph's", "《圣博托尔夫》",
      "Hughes goes back to the night he met Plath at the St Botolph's party in Falcon Yard: the American girl who recited his own lines at him, and the kiss that ended in a bite on his cheek.",
      "诗里休斯回到他遇见普拉斯的那一夜：在鹰院的圣博托尔夫派对上，一个美国姑娘对着他背出他自己的诗句，接着一吻，在他脸上留下一道咬痕。",
      ["Falcon Yard"], ["鹰院"], W + "Sylvia_Plath"),
    S("wotw-s1", "war-of-the-worlds", "horsell-common", "Book 1, Chapters 2–5", "第一部第 2—5 章",
      "A falling star lands on Horsell Common, and in the morning a huge cylinder lies half-buried in the sandpit, its end slowly unscrewing. A crowd comes out from Woking to stare; when a deputation approaches with a white flag, the Martians turn the invisible Heat-Ray on them.",
      "一颗流星落在霍塞尔公地，第二天早上，一个巨大的圆筒半埋在沙坑里，顶盖正慢慢旋开。沃金的人们跑来围观；一支举着白旗的代表团走近时，火星人放出了看不见的热射线。",
      ["Horsell Common"], ["霍塞尔公地"], G + "36"),
    S("ci-s1", "curious-incident", "paddington-station", "Christopher's journey to London", "克里斯托弗去伦敦",
      "Christopher, fifteen, who has never travelled anywhere alone, takes the train from Swindon to London Paddington to find his mother. In the roaring station he follows the signs to the Underground, counting and doing maths in his head to shut out the noise and the crowds.",
      "十五岁、从没独自出过门的克里斯托弗，从斯温登坐火车到伦敦帕丁顿站去找妈妈。车站里人声轰鸣，他一边在心里数数、做算术挡住噪音和人群，一边跟着指示牌找地铁。",
      ["Paddington"], ["帕丁顿"], W + "The_Curious_Incident_of_the_Dog_in_the_Night-Time"),
    S("hn-s1", "hamnet", "shakespeare-birthplace", "Part 1", "第一部",
      "Summer 1596. In the narrow house on Henley Street beside his grandparents', eleven-year-old Hamnet finds his twin sister Judith in bed with a fever, and runs from room to room, and next door, looking for any grown-up to help. Nobody is there.",
      "1596 年夏天。亨利街上，十一岁的哈姆奈特发现双胞胎妹妹朱迪斯发着烧躺在床上，他在自家窄窄的房子和隔壁祖父母家里一间间跑着找大人帮忙，却一个人也没有。",
      ["Henley Street"], ["亨利街"], W + "Hamnet_(novel)"),
    S("mk-s1", "milkman", "belfast", "Opening", "开头",
      "In an unnamed city during the Troubles, eighteen-year-old 'middle sister' walks the streets reading Ivanhoe, a habit her neighbours find suspicious. One day a paramilitary known as the milkman pulls up beside her in his car, and the gossip that they are having an affair begins to close round her.",
      "动乱年代一座没有名字的城市里，十八岁的“中间的妹妹”边走路边读《艾凡赫》，邻居们觉得这习惯很可疑。有一天，一个人称“送奶工”的准军事组织成员开车停在她身边，说他俩有私情的流言从此把她越围越紧。",
      ["Ivanhoe"], ["《艾凡赫》"], W + "Milkman_(novel)"),
    S("nor-s1", "north-heaney", "heaney-homeplace", "Mossbawn: Sunlight", "《莫斯邦：阳光》",
      "North opens with two poems for Heaney's aunt Mary at Mossbawn, the farm a few miles from Bellaghy where he grew up. In 'Sunlight' the pump stands warm in the summer yard while she dusts the board with flour and bakes scones by the stove, in a kitchen full of love.",
      "《北方》开头是两首献给姑妈玛丽的诗，写的是希尼长大的莫斯邦农场，离贝拉吉不过几英里。在《阳光》里，夏日院子里的水泵被晒得发暖，姑妈在炉边给案板撒面粉、烤司康饼，整个厨房都是爱。",
      ["Mossbawn"], ["莫斯邦"], W + "North_(poetry_collection)"),
]

# ---------------------------------------------------------------- edits to existing places
ADD_BOOKS = {  # pilgrimage places that gain books
    "shakespeare-birthplace": ["hamlet", "shakespeares-sonnets"],
    "dove-cottage": ["opium-eater"],
    "bronte-parsonage": ["villette"],
    "eliot-grave": ["daniel-deronda"],
    "max-gate": ["jude-the-obscure", "mayor-of-casterbridge"],
    "sherlock-museum": ["adventures-of-sherlock-holmes"],
    "reading-gaol": ["de-profundis"],
    "lawrence-birthplace": ["women-in-love"],
    "torquay": ["murder-of-roger-ackroyd"], "greenway": ["murder-of-roger-ackroyd"], "cholsey-church": ["murder-of-roger-ackroyd"],
}
NOTES = {
    "belfast": ("Northern Ireland's capital, built on linen and shipbuilding; the Titanic was launched here in 1911. C. S. Lewis grew up here and Seamus Heaney studied at Queen's. Anna Burns's Milkman never names its city, but its checkpoints, informers and gossip are Belfast's in the 1970s",
                "北爱尔兰首府，靠亚麻纺织和造船起家，泰坦尼克号 1911 年就在这里下水。C. S. 刘易斯在这里长大，希尼在女王大学读书。安娜·伯恩斯的《送奶工》从不点明城市的名字，但书里的检查站、告密者和闲言碎语都是 1970 年代的贝尔法斯特"),
    "salisbury": ("Trollope said he thought of the Barsetshire novels while wandering round this cathedral close one midsummer evening, and his Barchester owes much to Salisbury. In The Remains of the Day, Stevens spends the first night of his motoring trip here and admires the spire, the tallest in Britain",
                  "特罗洛普说，一个仲夏傍晚他在这座大教堂的内院里散步，想出了巴塞特郡系列小说，他的巴彻斯特有许多索尔兹伯里的影子。《长日将尽》里史蒂文斯开车旅行的第一晚也住在这里，赞叹那座全英最高的尖塔"),
    "clapham-common": ("In Atonement, Briony slips into Holy Trinity Church on Clapham Common to watch her cousin Lola marry Paul Marshall, the man who really attacked her years before. Graham Greene lived on the north side of the Common until the Blitz, and set The End of the Affair around it. In the early 1800s the church was home to the Clapham Sect, who campaigned to end the slave trade",
                       "《赎罪》里，布里奥妮悄悄走进克拉珀姆公园旁的圣三一教堂，看表姐罗拉嫁给保罗·马歇尔——当年真正侵犯罗拉的正是他。格雷厄姆·格林在公园北边住到大轰炸，《恋情的终结》就围着这片公园展开。19 世纪初，这座教堂是推动废除奴隶贸易的克拉珀姆派的据点"),
}

def edit_place_line(s, pid, fn):
    m = re.search(r'\n[ \t]*\{ id: "' + re.escape(pid) + r'",[^\n]*', s)
    assert m, pid
    new = fn(m.group(0))
    assert new != m.group(0), pid
    return s[:m.start()] + new + s[m.end():]

def main():
    bp, pp, lp = b.data("books.js"), b.data("places.js"), b.data("lines.js")
    have = lambda path: set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
    remove_objects(lp, DROP_LINES)
    remove_objects(pp, DROP_PLACES)
    remove_objects(bp, DROP_BOOKS)
    hb, hp, hl = have(bp), have(pp), have(lp)
    for x in books: assert x["id"] not in hb, x["id"]
    for x in places:
        assert x["id"] not in hp, x["id"]
        assert x["lat"] is not None, ("no coordinates", x["id"])
    for x in lines: assert x["id"] not in hl, x["id"]
    s = open(pp, encoding="utf-8").read()
    for pid, add in ADD_BOOKS.items():
        def f(line, add=add):
            m = re.search(r'book_ids: \[([^\]]*)\]', line)
            cur = json.loads("[" + m.group(1) + "]")
            return line[:m.start()] + "book_ids: " + json.dumps(cur + [a for a in add if a not in cur], ensure_ascii=False).replace('","', '", "') + line[m.end():]
        s = edit_place_line(s, pid, f)
    for pid, (en, zh) in NOTES.items():
        def f(line, en=en, zh=zh):
            line = re.sub(r'note: "(?:[^"\\]|\\.)*"', "note: " + b.js(zh), line, count=1)
            return re.sub(r'note_en: "(?:[^"\\]|\\.)*"', "note_en: " + b.js(en), line, count=1)
        s = edit_place_line(s, pid, f)
    open(pp, "w", encoding="utf-8").write(s)
    b.append(bp, books, "11-17 UK selection round: rubric additions and world-famous near misses")
    b.append(pp, places, "11-17 UK selection round")
    b.append(lp, lines, "11-17 UK selection round (scene notes; Gutenberg was down, quotations for the public-domain books to follow)")
    print(len(books), "books,", len(places), "places,", len(lines), "lines; removed", DROP_BOOKS, DROP_PLACES, DROP_LINES)

main()
