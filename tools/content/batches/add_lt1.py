"""11-26: Lithuania, the 10 books the user chose (the top 9 of the 2026 LRT survey of 63 book people, plus, of the two
books tied at 10-11, the one with more Goodreads ratings; tools/selection/lt.md). Lithuania opens with this batch.
All ten are in copyright, so the lines are scene notes in our own words. Two books are set mainly abroad; following the
precedent of data/us (us-hs-1) and data/hr (hr-oe-1), their place and scene note go into the files of the country where
the place is (the user chose cross-country pins, 11-26):
- Stutthof (data/pl): Forest of the Gods is Sruoga's account of the camp, where he was held from 1943.
- 34th Street, Manhattan (data/us): White Shroud opens as Garšva comes out onto 34th Street on his way to his job as an
  elevator operator; the hotel is not named, so the pin is the street.
Places in Lithuania, with the reason for each:
- Rasos Cemetery, Vilnius (pilgrimage): Sruoga and Mykolaitis-Putinas are buried here (Wikidata P119).
- St Michael's Church, Vilnius: much of Silva Rerum I takes place in the Bernardine nuns' convent beside it.
- Lieporiai, Šiauliai: "Pietinis", the southern district of Southern Chronicles, is the name for Lieporiai, Dainai,
  Gytariai and Gegužiai; it has no encyclopedia coordinates of its own, so the pin is Lieporiai (said in the note).
- Pilotiškės: the hill Aušrakalnis of In the Shadow of the Altars rises in this village, the author's birthplace.
- St George's Church, Vilnius (prototype): the former Book Palace there is the likely prototype of Vargalys's library.
- Užupis, Vilnius: Tūla lives at Malūnų Street 3, and the narrator's life is woven into the quarter.
- Antakalnis Cemetery, Vilnius (pilgrimage): Ivanauskaitė, Gavelis and Kunčinas are buried here (Wikidata P119). The
  Witch and the Rain has no real place we could find in its text or in the sources, so it is carried by this place only.
- Mikytai near Pagėgiai: the memorial to the wolf children, the East Prussian children of In the Shadow of Wolves.
Beloved Bones (Mylimi kaulai) has no place: its district is not named in the novel (reviewers guess Fabijoniškės or
Pašilaičiai), and the user decided on 11-26 not to pin it.
The map of Lithuania (data/lt/geo.js) is built from geoBoundaries LTU ADM1 (OpenStreetMap contributors via Wambacher,
ODbL 1.0; tools/eu-revision/lt_admin1_geoboundaries_2017.geojson): the 10 counties. Natural Earth still draws the pre-2000
border that puts Pagėgiai municipality in Klaipėda County; it belongs to Tauragė County.
Usage: python3 -I tools/content/batches/add_lt1.py <app_dir> tools/content/batches/coords/add_lt1.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-26"
b.init(APP, "", "lt", DATE)
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]
def BK(id, title, title_zh, title_orig, author, author_zh, year, aliases):
    return dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
                orig_lang="lt", public_domain=False, source_url=None, aliases=aliases)

books = [
    BK("dievu-miskas", "Forest of the Gods", "众神之林", "Dievų miškas", "Balys Sruoga", "巴利斯·斯鲁奥加", "1957",
       ["Dievų miškas", "Forest of the Gods", "Stutthof"]),
    BK("silva-rerum", "Silva Rerum", "Silva Rerum", "Silva Rerum", "Kristina Sabaliauskaitė", "克里斯蒂娜·萨巴利奥斯凯特", "2008",
       ["Silva Rerum", "Norvaiša", "Norvaišos"]),
    BK("balta-drobule", "White Shroud", "白色裹尸布", "Balta drobulė", "Antanas Škėma", "安塔纳斯·什凯马", "1958",
       ["Balta drobulė", "White Shroud", "Antanas Garšva"]),
    BK("pietinia-kronikas", "Southern Chronicles", "南区纪事", "Pietinia kronikas", "Rimantas Kmita", "里曼塔斯·克米塔", "2016",
       ["Pietinia kronikas", "Pietinio kronikos", "Southern Chronicles"]),
    BK("altoriu-sesely", "In the Shadow of the Altars", "祭坛的阴影下", "Altorių šešėly", "Vincas Mykolaitis-Putinas",
       "温察斯·迈科拉伊蒂斯-普蒂纳斯", "1933", ["Altorių šešėly", "In the Shadow of the Altars", "Liudas Vasaris"]),
    BK("vilniaus-pokeris", "Vilnius Poker", "维尔纽斯扑克", "Vilniaus pokeris", "Ričardas Gavelis", "里查尔达斯·加韦利斯", "1989",
       ["Vilniaus pokeris", "Vilnius Poker", "Vytautas Vargalys"]),
    BK("mylimi-kaulai", "Beloved Bones", "亲爱的骨头", "Mylimi kaulai", "Kotryna Zylė", "科特丽娜·济列", "2024",
       ["Mylimi kaulai", "Beloved Bones"]),
    BK("tula", "Tūla", "图拉", "Tūla", "Jurgis Kunčinas", "尤尔吉斯·昆奇纳斯", "1993", ["Tūla", "Tula"]),
    BK("ragana-ir-lietus", "The Witch and the Rain", "女巫与雨", "Ragana ir lietus", "Jurga Ivanauskaitė", "尤尔加·伊万瑙斯凯特", "1993",
       ["Ragana ir lietus", "The Witch and the Rain"]),
    BK("mano-vardas-maryte", "In the Shadow of Wolves", "我的名字叫玛丽特", "Mano vardas – Marytė", "Alvydas Šlepikas",
       "阿尔维达斯·什列皮卡斯", "2012", ["Mano vardas – Marytė", "Mano vardas - Marytė", "My Name Is Marytė", "In the Shadow of Wolves"]),
]

# —— places in Lithuania ——
places = [
    b.PIL("lt-rasos", "Rasos Cemetery, Vilnius", "维尔纽斯拉索斯公墓", *C("lt-rasos"),
        "Vilnius's oldest cemetery. Balys Sruoga (1896–1947), the author of Forest of the Gods, and Vincas Mykolaitis-Putinas (1893–1967), the author of In the Shadow of the Altars, are buried here; the pin is the cemetery",
        "维尔纽斯最古老的公墓。《众神之林》的作者巴利斯·斯鲁奥加（1896—1947）和《祭坛的阴影下》的作者温察斯·迈科拉伊蒂斯-普蒂纳斯（1893—1967）都葬在这里；图钉在公墓",
        ["dievu-miskas", "altoriu-sesely"]),
    b.ORIG("lt-sv-mykolo", "St Michael's Church, Vilnius", "维尔纽斯圣米迦勒教堂", *C("lt-sv-mykolo"),
        "The church of the Bernardine nuns in the Old Town, built in 1594–1627 with money from Chancellor Leonas Sapiega as his family's mausoleum, with the convent beside it; since 2009 it houses the Church Heritage Museum. Much of the first Silva Rerum novel takes place in this convent and church",
        "老城里伯纳丁修女会的教堂，1594—1627 年由大法官列奥纳斯·萨皮耶加出资修建，作为他的家族墓堂，旁边就是修女院；2009 年起这里是教会遗产博物馆。《Silva Rerum》第一部的大部分情节发生在这座修女院和教堂里"),
    b.ORIG("lt-lieporiai", "Lieporiai, Šiauliai", "希奥利艾的利埃波里艾", *C("lt-lieporiai"),
        "A microdistrict of Soviet apartment blocks in the south-west of Šiauliai. With Dainai, Gytariai and Gegužiai it makes up Pietinis, the 'southern district' of Rimantas Kmita's Southern Chronicles; Pietinis has no encyclopedia coordinates of its own, so the novel is pinned here",
        "希奥利艾西南部的一片苏联时期公寓楼小区。它和代奈、吉塔里艾、盖古日艾合起来叫“南区”，就是里曼塔斯·克米塔《南区纪事》写的地方；“南区”本身没有百科坐标，所以小说挂在这里"),
    b.ORIG("lt-pilotiskes", "Pilotiškės", "皮洛蒂什凯斯", *C("lt-pilotiskes"),
        "A village in Prienai district, Vincas Mykolaitis-Putinas's birthplace. His native house is now a memorial museum, and the hill Aušrakalnis described in In the Shadow of the Altars rises in the village",
        "普里埃奈区的一个村子，温察斯·迈科拉伊蒂斯-普蒂纳斯的出生地。他的故居如今是纪念馆，《祭坛的阴影下》里写到的“曙光山”（Aušrakalnis）就在村子里"),
    b.PROTO("lt-sv-jurgio", "St George's Church, Vilnius", "维尔纽斯圣乔治教堂", *C("lt-sv-jurgio"),
        "the library where Vytautas Vargalys works in Vilnius Poker: from 1946 to 2015 the Book Palace (Knygų rūmai), an old-prints repository and bibliography centre, was housed in this church and monastery complex",
        "《维尔纽斯扑克》里维陶塔斯·瓦尔加利斯工作的图书馆：1946 到 2015 年，这座教堂和修道院建筑群里是“图书宫”，一个古籍库和书目中心"),
    b.ORIG("lt-uzupis", "Užupis, Vilnius", "维尔纽斯乌茹皮斯", *C("lt-uzupis"),
        "The quarter across the Vilnia from the Old Town, run-down in Soviet times and now an artists' district. In Jurgis Kunčinas's Tūla, Tūla lives here at Malūnų Street 3, and the narrator's life is woven into the streets of the quarter",
        "老城对岸、维尔尼亚河那一边的街区，苏联时期破败，如今是艺术家聚集的地方。在尤尔吉斯·昆奇纳斯的《图拉》里，图拉就住在这里的磨坊街 3 号，叙述者的一生和这片街巷交织在一起"),
    b.PIL("lt-antakalnis", "Antakalnis Cemetery, Vilnius", "维尔纽斯安塔卡尔尼斯公墓", *C("lt-antakalnis"),
        "The cemetery in the Antakalnis district of Vilnius where Jurga Ivanauskaitė (1961–2007), Ričardas Gavelis (1950–2002) and Jurgis Kunčinas (1947–2002) are buried; the pin is the cemetery. Ivanauskaitė's The Witch and the Rain (1993), the love of a young woman for a priest woven with the stories of a medieval witch and of Mary Magdalene, was banned from sale for two weeks when it appeared",
        "维尔纽斯安塔卡尔尼斯区的公墓，尤尔加·伊万瑙斯凯特（1961—2007）、里查尔达斯·加韦利斯（1950—2002）和尤尔吉斯·昆奇纳斯（1947—2002）都葬在这里；图钉在公墓。伊万瑙斯凯特的《女巫与雨》（1993）把一个年轻女子对神父的爱，和中世纪女巫、抹大拉的马利亚的故事交织在一起，刚出版时曾被禁售两周",
        ["ragana-ir-lietus", "vilniaus-pokeris", "tula"]),
    b.ORIG("lt-mikytai", "Wolf Children Memorial, Mikytai", "米基泰“狼孩”纪念碑", *C("lt-mikytai"),
        "A village 2 km south-east of Pagėgiai, near the Nemunas and the border with the Kaliningrad region. On 20 June 1992 the German community Edelweiss unveiled here a memorial to the East Prussians who died of hunger or were killed in 1944–1947 and to the 'wolf children', the East Prussian children who crossed the Nemunas into Lithuania; it was renewed in 2014",
        "帕盖盖伊东南 2 公里的村子，靠近涅曼河和加里宁格勒州边界。1992 年 6 月 20 日，德意志社团“雪绒花”在这里揭幕了一座纪念碑，纪念 1944—1947 年饿死、被杀的东普鲁士人，以及渡过涅曼河来到立陶宛的东普鲁士孩子——“狼孩”；2014 年纪念碑翻新"),
]

lines = [
    b.S("lt-sr-1", "silva-rerum", "lt-sv-mykolo", "Silva Rerum I", "《Silva Rerum》第一部",
        "The first Silva Rerum novel follows the Norvaiša family in seventeenth-century Vilnius, above all the twins Kazimieras and Uršulė; the family's town house is on Pilies Street. Uršulė chooses to live in the convent of the Bernardine nuns beside St Michael's Church, and much of the first book's action takes place in the convent and the church; there she falls in love with her brother's friend, Jonas Kirdėjus Birontas.",
        "《Silva Rerum》第一部写 17 世纪维尔纽斯的诺尔瓦伊沙一家，主要是孪生兄妹卡济米耶拉斯和乌尔叙莱；这家人的城里宅子在城堡街。乌尔叙莱选择住进圣米迦勒教堂旁的伯纳丁修女院，第一部的大部分情节发生在修女院和教堂里；她在那里爱上了哥哥的朋友约纳斯·基尔代尤斯·比龙塔斯。",
        ["St Michael's Church"], ["圣米迦勒教堂"],
        "https://neakivaizdinisvilnius.lt/studijos/literaturinis-vilnius; https://lt.wikipedia.org/wiki/Vilniaus_šv._arkangelo_Mykolo_bažnyčia; https://www.vle.lt/straipsnis/bernardines/"),
    b.S("lt-pk-1", "pietinia-kronikas", "lt-lieporiai", "The novel as a whole", "全书",
        "Rimas, a senior pupil in Pietinis, the southern district of Šiauliai, grows up in the first years of independence: friends, girls, first erotic experiences, attempts to earn money, rugby, and around him wild capitalism, criminal gangs, counterfeit goods and a craze for Eastern spiritual practices. At first he wants to be like everyone else, but he starts reading books and decides to go to university. The novel is written not in standard Lithuanian but in the Šiauliai speech of the late twentieth century. Pietinis is the name for the Soviet apartment-block microdistricts of Lieporiai, Dainai, Gytariai and Gegužiai. Ignas Miškinis's film of the novel, shot in Šiauliai, became the most-watched film in the history of independent Lithuania.",
        "高年级中学生里马斯在希奥利艾的“南区”度过独立后的头几年：朋友、女孩、最初的性经验、想办法挣钱、橄榄球，周围是野蛮的资本主义、黑帮、假货和对东方灵修的热衷。起初他只想和大家一样，后来开始读书，决定上大学。小说不是用标准立陶宛语写的，而是用 20 世纪末的希奥利艾土话。“南区”是利埃波里艾、代奈、吉塔里艾、盖古日艾几片苏联公寓楼小区的合称。伊格纳斯·米什基尼斯在希奥利艾拍的同名电影，成了立陶宛独立以来观众最多的影片。",
        ["Lieporiai"], ["利埃波里艾"],
        "https://lt.wikipedia.org/wiki/Pietinia_kronikas; https://shop.fotomuziejus.lt/en/parduotuve/knygos/butasis-pietinis/; https://en.wikipedia.org/wiki/The_Southern_Chronicles; https://www.tv3.lt/gaires/pietinia-kronikas"),
    b.S("lt-as-1", "altoriu-sesely", "lt-pilotiskes", "The novel as a whole", "全书",
        "In the Shadow of the Altars, the first modernist Lithuanian novel, follows Liudas Vasaris, a sensitive young seminarian who becomes a priest and a writer, and asks whether one man can be both priest and poet. It draws heavily on Vincas Mykolaitis-Putinas's own life: like Vasaris, he was a poet from Suvalkija who entered the seminary, went on to the Ecclesiastical Academy in St Petersburg and then to Western Europe, and left the priesthood after returning to Lithuania. Some place names are real: the hill Aušrakalnis named in the novel rises in the poet's native village of Pilotiškės, and Naujapolis is easily read as Marijampolė.",
        "《祭坛的阴影下》是立陶宛第一部现代主义长篇，写敏感的年轻修生柳达斯·瓦萨里斯成为神父和作家，追问一个人能不能既是神父又是诗人。小说取材于温察斯·迈科拉伊蒂斯-普蒂纳斯自己的经历：和瓦萨里斯一样，他是苏瓦乌基亚出身的诗人，进了神学院，后来去彼得堡神学院、再去西欧深造，回到立陶宛后脱下了神父袍。书里有些地名是真的：小说里的“曙光山”（Aušrakalnis）就在诗人的家乡皮洛蒂什凯斯村，“瑙亚波利斯”不难认出是马里扬泊列。",
        ["Aušrakalnis", "Pilotiškės"], ["曙光山", "皮洛蒂什凯斯"],
        "https://lt.wikipedia.org/wiki/Altorių_šešėly; https://lt.wikipedia.org/wiki/Pilotiškės"),
    b.S("lt-vp-1", "vilniaus-pokeris", "lt-sv-jurgio", "Part One: Vargalys", "第一部：瓦尔加利斯",
        "Vytautas Vargalys, a former partisan who was tortured by the KGB and survived the labour camps, heads a department of a library in Soviet Vilnius in the 1970s. He believes that a hidden power he calls only 'They' persecutes and destroys people, and he wants to use the information stored in the library to prove it; he walks the streets of the city, admiring and loathing it. The most likely prototype of his library is the former Book Palace, the old-prints repository and bibliography centre housed in the St George's Church complex from 1946 to 2015, where some books were hidden from the authorities in the church's niches. The novel has four narrators, one of them a dog.",
        "曾是游击队员、受过克格勃酷刑、从劳改营活下来的维陶塔斯·瓦尔加利斯，20 世纪 70 年代在苏联时期维尔纽斯的一座图书馆当部门主任。他相信有一股只被他称作“他们”的隐秘力量在迫害、摧毁人，想用图书馆里的资料证明这一点；他走遍城里的街巷，对这座城既着迷又厌恶。他那座图书馆最可能的原型，是 1946 到 2015 年设在圣乔治教堂建筑群里的“图书宫”，一个古籍库和书目中心，有些书曾被藏在教堂的壁龛里躲过当局。小说有四个叙述者，其中一个是狗。",
        ["St George's Church"], ["圣乔治教堂"],
        "https://neakivaizdinisvilnius.lt/studijos/literaturinis-vilnius; https://www.lrt.lt/en/news-in-english/19/1399293/a-game-of-chance-you-re-bound-to-lose-vilnius-poker-by-ricardas-gavelis"),
    b.S("lt-tu-1", "tula", "lt-uzupis", "The novel as a whole", "全书",
        "The nameless narrator of Tūla, a bohemian drinker and vagrant of Soviet Vilnius, wanders the streets and drinks in cafés, keeps ending up in the psychiatric hospital he calls the Drunkards' Hospital, and cannot let go of a week-long love affair with Tūla, a young graduate of the Art Institute. Tūla lives in Užupis, at Malūnų Street 3, in a house with an apse on the far bank of the Vilnelė, and the narrator's life is woven into the topography of this then run-down quarter; critics credit the novel with helping to create the legend of Užupis.",
        "《图拉》里没有名字的叙述者，是苏联时期维尔纽斯一个酗酒的波希米亚流浪者：他在街上游荡、在咖啡馆里喝酒，一次次被送进他叫作“酒鬼医院”的精神病院，忘不了和艺术学院刚毕业的年轻姑娘图拉那一周的恋情。图拉住在乌茹皮斯的磨坊街 3 号，维尔内莱河对岸一座带半圆后殿的房子里；叙述者的一生和这个当时破败的街区的地形交织在一起，评论家认为这部小说帮着造出了乌茹皮斯的传说。",
        ["Užupis"], ["乌茹皮斯"],
        "https://neakivaizdinisvilnius.lt/studijos/literaturinis-vilnius; https://vilniusreview.com/fiction/144-jurgis-kuncinas; https://vilniusreview.com/articles/adrift-in-uzupis/; https://www.lrt.lt/en/news-in-english/19/1566966/invented-woman-invented-city-tula-by-jurgis-kuncinas"),
    b.S("lt-mm-1", "mano-vardas-maryte", "lt-mikytai", "The novel as a whole", "全书",
        "At the end of the war and after it, German children from East Prussia, many of them orphans, crossed the Nemunas into Lithuania to survive: they worked on farms, begged, and tried to carry bread back across the river to their starving families. They came to be called wolf children, and helping them was forbidden under Soviet rule. Šlepikas's novel follows Renatė, a German girl who calls herself Marytė; it was the most-read Lithuanian novel of 2012. Near the Nemunas, at Mikytai by Pagėgiai, a memorial to the East Prussians who died of hunger or were killed in 1944–1947 and to the wolf children was unveiled in 1992; Lithuania now marks 14 September as Wolf Children Remembrance Day.",
        "战争末期和战后，东普鲁士的德国孩子——很多是孤儿——渡过涅曼河来到立陶宛求生：在农庄干活、乞讨，想办法把面包带回河对岸挨饿的家人。他们后来被叫作“狼孩”，在苏联统治下帮助他们是被禁止的。什列皮卡斯的小说写一个自称玛丽特的德国女孩蕾娜特；这是 2012 年立陶宛读者最多的小说。在涅曼河边帕盖盖伊附近的米基泰，1992 年立起了一座纪念碑，纪念 1944—1947 年饿死、被杀的东普鲁士人和狼孩；立陶宛如今把 9 月 14 日定为狼孩纪念日。",
        ["Mikytai"], ["米基泰"],
        "https://english.lithuanianculture.lt/?p=7149; https://15min.lt/m/id/en/society/novel-about-post-war-german-children-selected-book-of-the-year-528-309093; https://www2.publishersweekly.com/pw/print/20180326/76434-publishing-in-the-baltic-region-2018-lithuania-s-alvydas-lepikas-on-the-timeliness-of-history.html; https://lt.wikipedia.org/wiki/Mikytai_(Pagėgiai); https://www.lrt.lt/naujienos/lietuvoje/2/2360022/pagegiuose-pirma-karta-bus-minima-vilko-vaiku-diena"),
]

# —— places abroad, with their scene notes: they go into the files of that country ——
def ABROAD(cc, place, line):
    place["country"] = cc
    return cc, place, line
abroad = [
    ABROAD("pl",
        b.ORIG("pl-stutthof", "Stutthof Museum, Sztutowo", "什图托沃的施图特霍夫集中营旧址", *C("pl-stutthof"),
            "The Nazi concentration camp set up in 1939 in marshy woodland near the village of Stutthof (now Sztutowo), 34 km east of Danzig; most of its structures were destroyed after the war, and in 1962 the site became a memorial museum. The Lithuanian writer Balys Sruoga was held here from 1943; Forest of the Gods is his account of the camp",
            "纳粹 1939 年在施图特霍夫村（今什图托沃）附近的沼泽林地里建起的集中营，在但泽以东 34 公里；营里的设施战后大多被拆毁，1962 年旧址辟为纪念博物馆。立陶宛作家巴利斯·斯鲁奥加从 1943 年起被关在这里，《众神之林》就是他写这座集中营的书"),
        b.S("pl-dm-1", "dievu-miskas", "pl-stutthof", "The book as a whole", "全书",
            "In March 1943 the German occupiers sent the Lithuanian writer Balys Sruoga, with forty-seven other Lithuanian intellectuals, to the Stutthof concentration camp east of Danzig, in a campaign against possible anti-Nazi agitation in occupied Lithuania. Forest of the Gods is his memoir of the camp, told with sarcastic irony and black humour, the beatings of prisoners and the dragging of corpses included; the critic Algis Kalėda saw this as the only way to fence oneself off from a coldly rational system for destroying people. Sruoga wrote it in a few months in the summer of 1945, recovering in the Birštonas sanatorium after his return; Soviet censors stopped it, and it was first published in 1957, ten years after his death. Algimantas Puipa filmed it in 2005.",
            "1943 年 3 月，德国占领当局以防范被占领的立陶宛出现反纳粹鼓动为名，把立陶宛作家巴利斯·斯鲁奥加和另外 47 名立陶宛知识分子送进但泽以东的施图特霍夫集中营。《众神之林》是他写这座集中营的回忆录，通篇是尖刻的反讽和黑色幽默，连毒打囚犯、拖运尸体的场面也不例外；评论家阿尔吉斯·卡列达认为，这是在一套冷静算计的灭绝人的系统面前，唯一能让人稍稍隔开自己的办法。1945 年夏天，斯鲁奥加回国后在比尔什托纳斯疗养院养病，只用几个月就写完了这本书；苏联审查不许出版，直到 1957 年、他去世十年后才第一次印出来。2005 年阿尔吉曼塔斯·普伊帕把它拍成了电影。",
            ["Stutthof"], ["施图特霍夫"],
            "https://en.wikipedia.org/wiki/Balys_Sruoga; https://lt.wikipedia.org/wiki/Dievų_miškas; https://en.wikipedia.org/wiki/Stutthof_concentration_camp")),
    ABROAD("us",
        b.ORIG("us-ny-34th-street", "34th Street, Manhattan", "曼哈顿 34 街", *C("us-ny-34th-street"),
            "The crosstown street of Midtown Manhattan. Antanas Škėma's White Shroud, the Lithuanian modernist novel of an exiled poet, opens as Antanas Garšva comes out onto 34th Street on his way to work as an elevator operator in a hotel the novel does not name; Škėma himself did the same work in New York. The pin is on the street",
            "横贯曼哈顿中城的大街。安塔纳斯·什凯马的《白色裹尸布》是一部写流亡诗人的立陶宛现代主义小说，开头就是安塔纳斯·加尔什瓦走上 34 街，去一家没写名字的酒店当电梯工；什凯马本人在纽约也做过这份工作。图钉在街上"),
        b.S("us-bd-1", "balta-drobule", "us-ny-34th-street", "Opening", "开头",
            "Antanas Garšva, a Lithuanian poet who fled the returning Soviet regime after the war, works as an elevator operator in a large New York hotel in the early 1950s. The novel opens as he walks through an underground passage out to 34th Street, goes in at the door for employees, waves to the watchman in his glass booth and takes from the board the white card with his name and 'elevator operator' on it. The present action lasts little more than a day; through his memories and his notebooks it reaches back through his whole life, from childhood and the inter-war years to the occupations and the refugee camps of Europe, and ends in his madness. Škėma himself worked as an elevator operator in New York.",
            "战后为躲避卷土重来的苏联政权而出逃的立陶宛诗人安塔纳斯·加尔什瓦，20 世纪 50 年代初在纽约一家大酒店当电梯工。小说开头，他穿过地下通道走到 34 街，从员工门进去，朝玻璃岗亭里的看门人挥挥手，从板子上取下写着自己名字和“电梯工”的白卡片。眼前的情节只有一天多一点；借着他的回忆和笔记本，故事回溯他的一生，从童年、两次大战之间的岁月，到被占领的年代和欧洲的难民营，最后以他发疯收场。什凯马本人在纽约也当过电梯工。",
            ["34th Street"], ["34 街"],
            "https://is.muni.cz/el/phil/jaro2011/BA455/um/Antanas_Skema_Balta_drobule.pdf (opening of the novel); https://en.wikipedia.org/wiki/Antanas_Škėma; https://ojs.utlib.ee/index.php/methis/article/view/23313/17789")),
]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set()
for f in glob.glob(os.path.join(APP, "data", "*", "books.js")):
    all_books |= ids_in(f)
new_b, new_p = {x["id"] for x in books}, {x["id"] for x in places}
assert len(books) == 10 and len(new_b) == 10
assert not new_b & all_books, new_b & all_books
assert new_p | {p["id"] for _, p, _ in abroad} == set(CO), (new_p | {p["id"] for _, p, _ in abroad}) ^ set(CO)
for l in lines:
    assert l["book_id"] in new_b and l["place_ids"][0] in new_p, l["id"]
for cc, p, l in abroad:
    assert p["id"].startswith(cc + "-") and l["id"].startswith(cc + "-") and l["place_ids"] == [p["id"]] and l["book_id"] in new_b
    assert p["id"] not in ids_in(os.path.join(APP, "data", cc, "places.js")) and l["id"] not in ids_in(os.path.join(APP, "data", cc, "lines.js"))
linked = {l["book_id"] for l in lines} | {l["book_id"] for _, _, l in abroad} | {x for p in places for x in p.get("book_ids", [])}
assert linked == new_b - {"mylimi-kaulai"}, new_b ^ linked     # Beloved Bones: no place, by the user's decision (11-26)
assert {l["place_ids"][0] for l in lines} | {p["id"] for p in places if p.get("book_ids")} == new_p

HEAD = "// Lithuania, hand-written content (tools/content/batches/add_lt1.py, 2026-11-26).\n"
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
    M = "11-26: Lithuanian books set here (tools/content/batches/add_lt1.py)"
    for cc, p, l in abroad:
        b.append(os.path.join(APP, "data", cc, "places.js"), [p], M)
        b.append(os.path.join(APP, "data", cc, "lines.js"), [l], M)
    print(len(books), "books,", len(places) + len(abroad), "places,", len(lines) + len(abroad), "lines")
