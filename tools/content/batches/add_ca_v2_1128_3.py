"""11-28: Canada, rule-v2 re-check (tools/selection/ca.md), batch 3: Toronto.
- In the Skin of a Lion (Michael Ondaatje): the Prince Edward (Bloor Street) Viaduct, whose building opens the novel and where a
  passage from it became the first Project Bookmark Canada plaque in 2009;
- Fifteen Dogs (André Alexis): High Park, where the fifteen dogs set up their society;
- Station Eleven (Emily St. John Mandel): the Elgin Theatre, where Arthur Leander dies on stage as King Lear on the first night of
  the pandemic;
- The Robber Bride (Margaret Atwood): the Toronto Islands, where Charis lives in a cottage;
- The Engineer of Human Souls (Josef Škvorecký): Edenvale College, modelled on Erindale College (now the University of Toronto
  Mississauga), where Škvorecký taught; a prototype place, so stated;
- Cat's Eye (Atwood), Bloodletting & Miraculous Cures (Vincent Lam) and Scott Pilgrim's Precious Little Life (Bryan Lee O'Malley):
  the existing Toronto place (ca-toronto), whose note gains a sentence on them. Scott Pilgrim first sees Ramona at the Wychwood
  branch of the Toronto Public Library, but neither Wikipedia nor Wikidata gives that library coordinates, so the book hangs on
  the city.
All are in copyright: scene notes, no quotation. Coordinates: coords/add_ca_v2_1128_3.json (en.wikipedia).
Usage: python3 -I tools/content/batches/add_ca_v2_1128_3.py <app_dir> tools/content/batches/coords/add_ca_v2_1128_3.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-28"
b.init(APP, "", "ca", DATE)
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]

def append(path, entries, marker):
    s = open(path, encoding="utf-8").read()
    i = s.rstrip().rfind("];")
    head = s[:i].rstrip()
    sep = "\n" if head.endswith("[") else ",\n"
    s = head.rstrip(",") + sep + "  // —— " + marker + " ——\n" + ",\n".join("  " + b.obj(e) for e in entries) + "\n];\n"
    open(path + ".new", "w", encoding="utf-8").write(s); os.replace(path + ".new", path)

def BK(id, title, zh, author, author_zh, year, aliases):
    return dict(id=id, title=title, title_zh=zh, title_orig=title, author=author, author_zh=author_zh, year=year, orig_lang="en",
                public_domain=False, source_url=None, author_orig=author, aliases=aliases)

books = [
    BK("in-the-skin-of-a-lion", "In the Skin of a Lion", "身着狮皮", "Michael Ondaatje", "迈克尔·翁达杰", "1987",
       ["In the Skin of a Lion", "Patrick Lewis", "Nicholas Temelcoff", "Bloor Street Viaduct", "Ondaatje"]),
    BK("fifteen-dogs", "Fifteen Dogs", "十五只狗", "André Alexis", "安德烈·亚历克西斯", "2015",
       ["Fifteen Dogs", "Majnoun", "Prince", "Atticus", "Alexis"]),
    BK("station-eleven", "Station Eleven", "第十一站", "Emily St. John Mandel", "艾米莉·圣约翰·曼德尔", "2014",
       ["Station Eleven", "Kirsten Raymonde", "Arthur Leander", "Traveling Symphony", "Mandel"]),
    BK("the-robber-bride", "The Robber Bride", "强盗新娘", "Margaret Atwood", "玛格丽特·阿特伍德", "1993",
       ["The Robber Bride", "Zenia", "Tony", "Charis", "Roz", "The Toxique"]),
    dict(id="engineer-of-human-souls", title="The Engineer of Human Souls", title_zh="人类灵魂工程师", title_orig="Příběh inženýra lidských duší",
         author="Josef Škvorecký", author_zh="约瑟夫·什克沃雷茨基", year="1977", orig_lang="cs", public_domain=False, source_url=None,
         author_orig="Josef Škvorecký", aliases=["The Engineer of Human Souls", "Příběh inženýra lidských duší", "Danny Smiřický", "Edenvale College", "Škvorecký"]),
    BK("cats-eye", "Cat's Eye", "猫眼", "Margaret Atwood", "玛格丽特·阿特伍德", "1988",
       ["Cat's Eye", "Elaine Risley", "Cordelia", "Atwood"]),
    BK("bloodletting-miraculous-cures", "Bloodletting & Miraculous Cures", "放血与奇迹疗法", "Vincent Lam", "林伟健", "2006",
       ["Bloodletting & Miraculous Cures", "Bloodletting and Miraculous Cures", "Fitzgerald", "Ming", "Chen", "Sri"]),
    BK("scott-pilgrim", "Scott Pilgrim's Precious Little Life", "斯科特·皮尔格林的宝贵小生活", "Bryan Lee O'Malley", "布赖恩·李·奥马利", "2004",
       ["Scott Pilgrim's Precious Little Life", "Scott Pilgrim", "Ramona Flowers", "Knives Chau", "Sex Bob-Omb"]),
]

places = [
    b.ORIG("ca-bloor-viaduct", "Prince Edward Viaduct (Bloor Street Viaduct)", "爱德华王子高架桥（布卢尔街高架桥）", *C("ca-bloor-viaduct"),
        "The steel-arch bridge that carries Bloor Street and the subway across the Don Valley, opened in 1918. Michael Ondaatje's In the Skin of a Lion (1987) tells the story of its building through the immigrant workers who built it, among them the Macedonian bridge-worker Nicholas Temelcoff; in 2009 a passage from the novel was set up at the viaduct, the first Project Bookmark Canada plaque on the country's literary trail",
        "把布卢尔街和地铁架过当河谷的钢拱桥，1918 年通车。迈克尔·翁达杰的《身着狮皮》（1987）透过建桥的移民工人讲这座桥的修建，其中就有马其顿桥工尼古拉斯·泰梅尔科夫；2009 年小说里的一段文字被立在高架桥边，成为“加拿大文学书签计划”在这条全国文学路线上的第一块牌子"),
    b.ORIG("ca-high-park", "High Park, Toronto", "多伦多 · 海伊公园", *C("ca-high-park"),
        "Toronto's largest park, in the west of the city, with woods, ravines and Grenadier Pond. In André Alexis's Fifteen Dogs (2015) the fifteen dogs whom Hermes and Apollo give human language escape from a veterinary clinic and set up their own new society here",
        "多伦多最大的公园，在城西，有树林、谷地和掷弹兵池。安德烈·亚历克西斯的《十五只狗》（2015）里，被赫尔墨斯和阿波罗赋予人类语言的十五只狗从兽医诊所逃出来，就在这里建起了它们自己的新社会"),
    b.ORIG("ca-elgin-theatre", "Elgin Theatre, Toronto", "多伦多 · 埃尔金剧院", *C("ca-elgin-theatre"),
        "The lower house of the Elgin and Winter Garden Theatres on Yonge Street, a stacked pair of Edwardian theatres. Station Eleven (2014) opens here: during a production of King Lear the actor Arthur Leander dies on stage of a heart attack, on the night a flu pandemic begins that will end the old world",
        "央街上的埃尔金与冬园剧院是上下叠在一起的两座爱德华时代剧院，埃尔金在下层。《第十一站》（2014）就从这里开场：演出《李尔王》时，演员亚瑟·利安德心脏病发，死在舞台上；同一个夜里，一场流感大流行开始了，旧世界将就此终结"),
    b.ORIG("ca-toronto-islands", "Toronto Islands", "多伦多群岛", *C("ca-toronto-islands"),
        "The chain of small islands across the harbour from downtown Toronto, reached by ferry, with parkland and a small community of cottages on Ward's and Algonquin islands. In Margaret Atwood's The Robber Bride (1993) the gentle, New Age Charis lives in a ramshackle cottage on the Island, from where the city seems to float on the morning mist",
        "隔着港湾与多伦多市中心相望的一串小岛，要坐渡轮去，岛上是公园，沃兹岛和阿尔冈昆岛上还有一小片村舍。玛格丽特·阿特伍德的《强盗新娘》（1993）里，温柔又“新时代”的查丽丝就住在岛上一座破旧的小屋里，从那里望去，城市仿佛浮在晨雾之上"),
    b.PROTO("ca-erindale", "Erindale College (University of Toronto Mississauga)", "伊林代尔学院（多伦多大学密西沙加校区）", *C("ca-erindale"),
        "Edenvale College, near Toronto, where Danny Smiřický, Czech writer in exile, teaches American literature in Josef Škvorecký's The Engineer of Human Souls (1977). Škvorecký, who left Czechoslovakia in 1968 like his narrator, taught English at Erindale College of the University of Toronto, now the University of Toronto Mississauga",
        "约瑟夫·什克沃雷茨基《人类灵魂工程师》（1977）里多伦多附近的伊登维尔学院：流亡的捷克作家丹尼·斯米日茨基在那里教美国文学。什克沃雷茨基和他的叙述者一样在 1968 年离开捷克斯洛伐克，他在多伦多大学的伊林代尔学院教英文，那里就是今天的多伦多大学密西沙加校区"),
]

lines = [
    b.S("skinlion-s1", "in-the-skin-of-a-lion", "ca-bloor-viaduct", "Book One, “The Bridge”, and throughout", "第一部《桥》，及全书",
        "Toronto in the early twentieth century, told through the immigrants who built it but were left out of its official history. The Bloor Street Viaduct is going up across the Don Valley to carry traffic, water and electricity into the city; the Commissioner of Public Works, R. C. Harris, often visits it at night. One night five nuns wander onto the unfinished bridge and one falls; Nicholas Temelcoff, a Macedonian bridge-worker who speaks little English, catches her in mid-air and dislocates his arm. Patrick Lewis, who grew up in the logging village of Depot Creek, comes to the city to search for the vanished theatre millionaire Ambrose Small, falls for his mistress Clara Dickens and later for Alice Gull, works as a dynamiter on the tunnel under Lake Ontario for Harris's water filtration plant, and at last turns on Harris himself. Hana and Caravaggio go on into The English Patient.",
        "二十世纪初的多伦多，由那些建起这座城、却被正史遗忘的移民来讲。布卢尔街高架桥正在当河谷上架起来，要把车流、水和电送进城；公共工程专员 R. C. 哈里斯常在夜里来桥上看看。一天夜里，五个修女走上没有完工的桥，其中一个掉了下去；不太会说英语的马其顿桥工尼古拉斯·泰梅尔科夫在半空中接住了她，自己的胳膊却脱了臼。在伐木村德波溪长大的帕特里克·刘易斯来到城里，寻找失踪的剧院富豪安布罗斯·斯莫尔，爱上了他的情妇克拉拉·狄更斯，后来又爱上爱丽丝·古尔；他在安大略湖底为哈里斯的滤水厂挖隧道当爆破工，最后把矛头对准了哈里斯本人。哈娜和卡拉瓦乔后来又走进了《英国病人》。",
        ["Bloor Street Viaduct", "Don Valley"], ["布卢尔街高架桥", "当河谷"],
        "https://en.wikipedia.org/wiki/In_the_Skin_of_a_Lion; https://en.wikipedia.org/wiki/Prince_Edward_Viaduct"),
    b.S("fifteendogs-s1", "fifteen-dogs", "ca-high-park", "Throughout", "全书",
        "Over drinks at the Wheat Sheaf Tavern in Toronto, the gods Hermes and Apollo argue whether animals given human intelligence and language would be happier or unhappier than humans, and wager a year's servitude on it. They give the gift to fifteen dogs kennelled at a nearby veterinary clinic. The dogs escape and make their way to High Park, where they set up a new society; Atticus, a Neapolitan mastiff, becomes its leader, while Prince, a mongrel, takes to the new language and becomes a poet, and Majnoun, a black poodle, forms a bond with a woman named Nira. The new language divides the pack, and the gods watch to see whether the gift can make any of the dogs happy.",
        "在多伦多的麦捆酒馆里喝着酒，赫尔墨斯和阿波罗两位神争论起来：如果动物有了人的智力和语言，它们会比人更幸福还是更不幸？他们押上一年的奴役打了个赌，把这份礼物给了附近一家兽医诊所里寄养的十五只狗。狗们逃了出来，来到海伊公园，在那里建起了一个新社会：那不勒斯獒阿提克斯当了首领；杂种狗普林斯迷上了新语言，成了诗人；黑色贵宾犬马吉努和一个叫妮拉的女人结下了情谊。新语言让狗群起了纷争，两位神在一旁看着，看这份礼物能不能让哪只狗幸福。",
        ["High Park", "Toronto"], ["海伊公园", "多伦多"],
        "https://en.wikipedia.org/wiki/Fifteen_Dogs"),
    b.S("stationeleven-s1", "station-eleven", "ca-elgin-theatre", "Opening chapters", "开头几章",
        "During a production of King Lear at the Elgin Theatre in Toronto, the actor playing Lear, Arthur Leander, has a heart attack on stage. Jeevan Chaudhary, a former paparazzo training as a paramedic, rushes to the stage and tries in vain to revive him, then comforts Kirsten Raymonde, an eight-year-old girl in the cast. Walking home through the snow, Jeevan gets a call from a doctor friend: the Georgia Flu is spreading fast and kills almost everyone it touches. Twenty years later Kirsten travels the Great Lakes region with the Traveling Symphony, a troupe that performs Shakespeare and music for the scattered survivors, still carrying the two comic books, Station Eleven, that Arthur gave her before he died.",
        "多伦多的埃尔金剧院正在上演《李尔王》，扮演李尔的演员亚瑟·利安德在台上心脏病发作。曾经当过狗仔、正在受训做急救员的吉万·乔杜里冲上舞台，徒劳地抢救他，随后安慰剧组里八岁的小演员柯尔斯滕·雷蒙德。吉万踏着雪走回家时，一个当医生的朋友打来电话：“格鲁吉亚流感”正迅速蔓延，染上的人几乎无一幸存。二十年后，柯尔斯滕跟着“旅行交响乐团”在五大湖一带巡演，为四散的幸存者演莎士比亚、奏音乐，身上一直带着亚瑟死前送给她的两本漫画，《第十一站》。",
        ["Elgin Theatre", "Toronto"], ["埃尔金剧院", "多伦多"],
        "https://en.wikipedia.org/wiki/Station_Eleven"),
    b.S("robberbride-s1", "the-robber-bride", "ca-toronto-islands", "Throughout", "全书",
        "Toronto, 23 October 1990: three women in their late forties, friends since their student days at the University of Toronto, are having their monthly lunch at the Toxique, a restaurant on Queen Street, when in walks Zenia, the beautiful, lying friend who betrayed each of them and whose funeral they attended five years earlier. Tony is a military historian at the university, Roz a successful businesswoman, and Charis a gentle, New Age yoga teacher who lives in a cottage on the Toronto Island. In flashbacks each remembers how Zenia came into her life with a story made to measure and took her man: to Charis she came in 1970, claiming to be fleeing a violent man and dying of cancer, and Charis took her into her island home. Atwood recast the Grimms' tale of the robber bridegroom as a woman.",
        "多伦多，1990 年 10 月 23 日：三个快五十岁的女人，从多伦多大学读书时就是朋友，正在皇后街的“托克西克”餐馆吃她们每月一次的午饭，泽尼亚走了进来。这个美丽又满口谎言的朋友背叛过她们每一个人，五年前她们还去参加过她的葬礼。托妮在大学里研究军事史，罗兹是成功的女商人，查丽丝是温柔、讲“新时代”的瑜伽老师，住在多伦多岛上的一座小屋里。在回忆里，三个人各自想起泽尼亚怎样带着为她量身编好的故事走进自己的生活，夺走了自己的男人：1970 年她来找查丽丝，说自己在躲一个暴力的男人，又得了癌症快死了，查丽丝便把她接进了岛上的家。阿特伍德把格林童话里的强盗新郎改写成了一个女人。",
        ["Toronto Island", "Toronto"], ["多伦多岛", "多伦多"],
        "https://en.wikipedia.org/wiki/The_Robber_Bride; https://www.nybooks.com/?p=20197; https://journals.lib.unb.ca/index.php/IFR/article/download/14386/15463/19122; https://readinggroupguides.com/reviews/the-robber-bride; https://www.supersummary.com/the-robber-bride/summary"),
    b.S("engineer-s1", "engineer-of-human-souls", "ca-erindale", "Throughout", "全书",
        "Toronto, winter 1976 to spring 1977. Danny Smiřický, the Czech writer and jazz saxophonist of Škvorecký's earlier novels, left Czechoslovakia in 1968 and now teaches American literature at Edenvale College near Toronto, watching the snow swirl over the campus. The chapters take the names of the writers he lectures on, and his classes of earnest, puzzled Canadian students alternate with letters from friends behind the Iron Curtain, the Czech exile community in Toronto, and memories of his youth in wartime Kostelec, where he chased girls and played the saboteur. Škvorecký called it an entertainment on the old themes of life, women, fate, dreams, the working class, secret agents, love and death; it won the Governor General's Award in 1984.",
        "多伦多，1976 年冬到 1977 年春。丹尼·斯米日茨基就是什克沃雷茨基早先几部小说里那个捷克作家兼爵士萨克斯手，1968 年离开捷克斯洛伐克，如今在多伦多附近的伊登维尔学院教美国文学，望着雪花在校园上空打旋。各章以他讲授的作家命名：他班上认真又困惑的加拿大学生，和铁幕后朋友们的来信、多伦多的捷克流亡圈、战时故乡科斯泰莱茨的青春回忆交替出现，那时他追女孩，也当过一回“破坏分子”。什克沃雷茨基称它是“一部关于生活、女人、命运、梦想、工人阶级、特务、爱情与死亡这些老题目的消遣之作”；它获得了 1984 年的总督奖。",
        ["Edenvale College", "Toronto"], ["伊登维尔学院", "多伦多"],
        "https://www.cmreviews.ca/cm/cmarchive/vol13no1/revengineerofhuman.html; https://cbra.library.utoronto.ca/items/show/37175; https://themodernnovel.org/?p=2644; https://nybooks.com/?p=23573; https://www.ebsco.com/research-starters/literature-and-writing/engineer-human-souls-josef-skvorecky; https://www.goodreads.com/book/show/6977371"),
    b.S("catseye-s1", "cats-eye", "ca-toronto", "Throughout", "全书",
        "The painter Elaine Risley comes back to Toronto, the city she grew up in, for a retrospective of her work, and the city brings back her childhood. After a wandering early life with her family, she settles into school in Toronto and is taken up by three girls, Carol, Grace and the clever, domineering Cordelia, who turn her into the object of a slow, smiling cruelty, always presented as an effort to improve her. One winter they throw her hat into a ravine and leave her in the half-frozen creek, where a vision of the Virgin Mary seems to lead her out; only then does she break away. In high school the tables turn on Cordelia, whose life later comes apart, and the cat's-eye marble Elaine kept as a child becomes a motif of her paintings.",
        "画家伊莱恩·里斯利回到她长大的多伦多参加自己的作品回顾展，这座城把她的童年带了回来。随家人四处漂泊过一阵后，她在多伦多入了学，被三个女孩拉进圈子：卡罗尔、格蕾丝和聪明又专横的科迪莉亚。三人对她施以缓慢的、笑眯眯的折磨，嘴上总说是为了让她变好。一个冬天，她们把她的帽子扔进峡谷，任她留在半冻的溪水里，一个圣母玛利亚的幻影似乎领着她爬了出来；直到这时她才挣脱了她们。上了中学，处境反了过来，科迪莉亚后来的生活也四分五裂；伊莱恩小时候珍藏的那颗猫眼弹珠，成了她画里反复出现的意象。",
        ["Toronto"], ["多伦多"],
        "https://en.wikipedia.org/wiki/Cat%27s_Eye_(novel)"),
    b.S("bloodletting-s1", "bloodletting-miraculous-cures", "ca-toronto", "Throughout", "全书",
        "Twelve linked stories follow four young doctors, Ming, Fitzgerald, Chen and Sri, from cramming for medical school in Ottawa to the anatomy lab, the wards and the emergency rooms of Toronto. Ming is accepted to medical school and Fitzgerald is not; she drops him and later marries her lab partner Chen, while Fitz, who follows her into medicine, drifts from job to job, including an air ambulance, and drinks. Near the end comes the SARS outbreak of 2003, with two of them in an isolation ward after treating infected patients. Vincent Lam, a Toronto emergency physician, worked in the emergency department of one of the hospitals hit by SARS.",
        "十二个相互勾连的短篇，跟着四个年轻医生明、菲茨杰拉德、陈和斯里，从在渥太华拼命备考医学院，到解剖室、病房和多伦多的急诊室。明考上了医学院，菲茨杰拉德没考上；她甩了他，后来嫁给了实验搭档陈。菲茨后来也追着她学了医，却在一份份工作之间漂荡，包括空中救护，还酗酒。书的末尾写到 2003 年的非典疫情：他们中两人因为救治病人被关进了隔离病房。作者林伟健就是多伦多的急诊科医生，非典时在一家受疫情冲击的医院急诊室工作。",
        ["Toronto"], ["多伦多"],
        "https://en.wikipedia.org/wiki/Bloodletting_%26_Miraculous_Cures; https://medhum.med.nyu.edu/view/12677; https://www.kirkusreviews.com/book-reviews/vincent-lam/bloodletting-miraculous-cures/; https://journals.library.ualberta.ca/jchla/index.php/jchla/article/download/24051/17875/59476; https://mjm.mcgill.ca/article/download/471/311"),
    b.S("scottpilgrim-s1", "scott-pilgrim", "ca-toronto", "Volume 1", "第一册",
        "In “the mysterious land of Toronto, Canada”, twenty-three-year-old Scott Pilgrim shares a cheap apartment with his gay roommate Wallace, plays bass in the garage band Sex Bob-Omb and is casually dating Knives Chau, a seventeen-year-old high-school girl. Then he dreams of a pink-haired girl on rollerblades and sees her for real at the library, the Wychwood branch of the Toronto Public Library on Bathurst Street: Ramona Flowers, newly arrived from New York, who delivers parcels for Amazon by a shortcut through people's dreams. To date her, he learns, he must defeat her seven evil exes, and at a battle of the bands the first of them, Matthew Patel, crashes through the ceiling. Bryan Lee O'Malley drew the city's real streets, shops and venues into the comic.",
        "在“神秘的国度——加拿大多伦多”，二十三岁的斯科特·皮尔格林和同性恋室友华莱士合住一间廉价公寓，在车库乐队“炸弹鲍勃”里弹贝斯，和十七岁的高中女生诺芙斯·周随便约着会。后来他梦见一个踩着旱冰鞋的粉头发女孩，又在图书馆里见到了真人，那是多伦多公共图书馆在巴瑟斯特街的威奇伍德分馆：她叫拉蒙娜·弗劳尔斯，刚从纽约搬来，替亚马逊送货，抄的近路穿过人们的梦。他得知，要和她交往，就得打败她的七个邪恶前任；在一场乐队比赛上，第一个前任马修·帕特尔破顶而入。布赖恩·李·奥马利把这座城真实的街道、店铺和演出场所都画进了漫画。",
        ["Toronto"], ["多伦多"],
        "https://en.wikipedia.org/wiki/Scott_Pilgrim; https://scottpilgrim.fandom.com/wiki/Toronto_Public_Library; https://movie-locations.com/movies/s/Scott-Pilgrim-Vs-The-World.php; https://amp.cbc.ca/lite/story/1.3984171"),
]

TOR_EN = "and Robertson Davies's Boy Staunton is found dead in its harbour."
TOR_ZH = "罗伯逊·戴维斯笔下的博伊·斯汤顿也被发现死在这里的港口。"
def toronto_note(path):
    s = open(path, encoding="utf-8").read()
    assert s.count(TOR_EN) == 1 and s.count(TOR_ZH) == 1
    s = s.replace(TOR_EN, TOR_EN + " Atwood's painter Elaine Risley comes home to it for a retrospective in Cat's Eye, Vincent Lam's young doctors work its emergency rooms through SARS in Bloodletting & Miraculous Cures, and Scott Pilgrim fights Ramona Flowers's evil exes across its streets.")
    s = s.replace(TOR_ZH, TOR_ZH + "《猫眼》里阿特伍德的画家伊莱恩·里斯利回到这里办回顾展，《放血与奇迹疗法》里林伟健笔下的年轻医生在这里的急诊室熬过非典，斯科特·皮尔格林则在这座城的大街小巷里迎战拉蒙娜·弗劳尔斯的邪恶前任。")
    open(path + ".new", "w", encoding="utf-8").write(s); os.replace(path + ".new", path)

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "books.js"))))
all_places = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "places.js"))))
all_lines = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "lines.js"))))
assert not {x["id"] for x in books} & all_books
assert {p["id"] for p in places} == set(CO) and not set(CO) & all_places and "ca-toronto" in all_places
assert not {l["id"] for l in lines} & all_lines
if __name__ == "__main__":
    note = "11-28 Canada rule-v2 re-check, batch 3: Toronto (add_ca_v2_1128_3.py)"
    append(b.data("books.js"), books, note)
    append(b.data("places.js"), places, note)
    append(b.data("lines.js"), lines, note)
    toronto_note(b.data("places.js"))
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
