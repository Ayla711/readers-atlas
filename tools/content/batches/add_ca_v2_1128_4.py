"""11-28: Canada, rule-v2 re-check (tools/selection/ca.md), batch 4: the rest of Ontario with a clear place.
- Sunshine Sketches of a Little Town (Stephen Leacock, 1912, US public domain): Orillia, the model of Mariposa; one verbatim
  passage, the opening of chapter I, from English Wikisource ("Sunshine Sketches of a Little Town/Chapter I", fetched with
  tools/content/wikisource.py); the page's hard line ends inside a paragraph become single spaces;
- The Best Laid Plans (Terry Fallis): Parliament Hill, where Daniel Addison works and Angus McLintock ends up as an MP;
- The Orenda (Joseph Boyden): Sainte-Marie among the Hurons, the Jesuit mission in Wendake co-founded in 1639 by Jean de Brébeuf,
  the model for the novel's Christophe; the novel does not name its mission, and the note says so;
- Essex County (Jeff Lemire): Essex County, Ontario, where the three graphic stories are set;
- Three Day Road (Joseph Boyden): the existing Moose Factory place (Xavier and Elijah grow up in the bush around it; Niska meets
  Xavier off the train in an unnamed town and paddles him home), whose note gains a sentence;
- Lives of Girls and Women and Who Do You Think You Are? (Alice Munro): the existing Wingham place, model of Jubilee and Hanratty;
  its note named Dance of the Happy Shades, removed on 11-28, and now names these two books instead.
Copyright books: scene notes, no quotation. Coordinates: coords/add_ca_v2_1128_4.json (en.wikipedia).
Usage: python3 -I tools/content/batches/add_ca_v2_1128_4.py <app_dir> tools/content/batches/coords/add_ca_v2_1128_4.json <wikisource_dir>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WS = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
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

SUN = "Sunshine Sketches of a Little Town/Chapter I"
def para(title, start, end):
    """one paragraph, from `start` to the end of `end`; the page's hard line ends inside it become single spaces"""
    t = ws.text(WS, title)
    i = t.find(start); assert i >= 0, (title, start)
    assert t.find(start, i + 1) < 0, (title, start, "not unique")
    j = t.find(end, i); assert j >= 0, (title, start, end)
    s = t[i:j + len(end)].replace("\n", " ")
    assert "  " not in s and "\xa0" not in s and "[" not in s, (title, start)
    return s

books = [
    dict(id="sunshine-sketches", title="Sunshine Sketches of a Little Town", title_zh="小镇艳阳录", title_orig="Sunshine Sketches of a Little Town",
         author="Stephen Leacock", author_zh="斯蒂芬·里柯克", year="1912", orig_lang="en", public_domain=True,
         source_url=ws.url("en", "Sunshine Sketches of a Little Town"), author_orig="Stephen Leacock",
         aliases=["Sunshine Sketches of a Little Town", "Mariposa", "Mariposa Belle", "Josh Smith", "Leacock"]),
    BK("the-best-laid-plans", "The Best Laid Plans", "人算不如天算", "Terry Fallis", "特里·法利斯", "2007",
       ["The Best Laid Plans", "Daniel Addison", "Angus McLintock", "Cumberland-Prescott"]),
    BK("the-orenda", "The Orenda", "奥伦达", "Joseph Boyden", "约瑟夫·博伊登", "2013",
       ["The Orenda", "Bird", "Snow Falls", "Christophe", "Wendat", "Huronia"]),
    BK("essex-county", "The Collected Essex County", "埃塞克斯县", "Jeff Lemire", "杰夫·勒米尔", "2009",
       ["Essex County", "The Collected Essex County", "Tales from the Farm", "Ghost Stories", "The Country Nurse", "Lester", "Lou LeBeuf"]),
    BK("three-day-road", "Three Day Road", "三日之路", "Joseph Boyden", "约瑟夫·博伊登", "2005",
       ["Three Day Road", "Xavier Bird", "Elijah Whiskeyjack", "Niska"]),
    BK("lives-of-girls-and-women", "Lives of Girls and Women", "女孩和女人的生活", "Alice Munro", "艾丽丝·门罗", "1971",
       ["Lives of Girls and Women", "Del Jordan", "Jubilee", "Flats Road"]),
    BK("who-do-you-think-you-are", "Who Do You Think You Are?", "你以为你是谁？", "Alice Munro", "艾丽丝·门罗", "1978",
       ["Who Do You Think You Are?", "The Beggar Maid", "Rose", "Flo", "Hanratty"]),
]

places = [
    b.PROTO("ca-orillia", "Orillia, Ontario", "安大略 · 奥里利亚", *C("ca-orillia"),
        "Mariposa, the little town on Lake Wissanotti in Stephen Leacock's Sunshine Sketches of a Little Town (1912). Leacock drew it from his years in Orillia, on Lake Couchiching, and many of its characters from Orillia people, whose names were only thinly disguised when the sketches first ran in the Montreal Star; Leacock himself wrote that Mariposa was seventy or eighty towns. Orillia still calls itself the Sunshine City, and his summer house is now the Leacock Museum, a National Historic Site",
        "斯蒂芬·里柯克《小镇艳阳录》（1912）里维萨诺蒂湖畔的小镇马里波萨。里柯克是从他在库奇钦湖畔奥里利亚的岁月里取的材，书中许多人物也取自奥里利亚的镇民，这些速写最初在《蒙特利尔星报》连载时，人名只是稍加改动；不过里柯克自己说，马里波萨其实是七八十个小镇。奥里利亚至今自称“阳光之城”，他的夏日别墅如今是里柯克博物馆，属国家历史遗址"),
    b.ORIG("ca-parliament-hill", "Parliament Hill, Ottawa", "渥太华 · 国会山", *C("ca-parliament-hill"),
        "The hill above the Ottawa River where the Parliament of Canada sits. In Terry Fallis's comic novel The Best Laid Plans (2007) the burnt-out speechwriter Daniel Addison quits his job here, and comes back with Angus McLintock, the cranky engineering professor who agreed to run in a hopeless riding and, to everyone's horror, was elected",
        "渥太华河上方的山岗，加拿大议会所在地。特里·法利斯的喜剧小说《人算不如天算》（2007）里，心力交瘁的演讲撰稿人丹尼尔·艾迪生在这里辞了职，后来又陪着安格斯·麦克林托克回到这里：这位脾气古怪的工程学教授答应去一个毫无希望的选区挂名参选，结果出乎所有人意料，竟当选了"),
    b.ORIG("ca-sainte-marie", "Sainte-Marie among the Hurons", "休伦人中的圣玛丽", *C("ca-sainte-marie"),
        "The French Jesuit mission in Wendake, the country of the Wendat (Huron), near present-day Midland, founded in 1639 by Jérôme Lalemant and Jean de Brébeuf and abandoned in 1649; the first European settlement in Ontario, now a reconstructed living museum. Joseph Boyden's The Orenda (2013) is set in this country in the years of the mission; its Jesuit, Christophe, is modelled on Brébeuf and founds a mission near the village of the Wendat warrior Bird, though the novel does not name it Sainte-Marie",
        "法国耶稣会在温达特人（休伦人）的土地温达克建的传教站，在今天米德兰附近，1639 年由热罗姆·拉勒芒和让·德·布雷伯夫创建，1649 年废弃；这是安大略第一个欧洲人定居点，如今复建成活态博物馆。约瑟夫·博伊登的《奥伦达》（2013）就发生在传教站那些年的这片土地上；书里的耶稣会士克里斯托夫以布雷伯夫为原型，在温达特战士伯德的村子附近建了一座传教站，不过小说没有把它叫作圣玛丽"),
    b.ORIG("ca-essex-county", "Essex County, Ontario", "安大略 · 埃塞克斯县", *C("ca-essex-county"),
        "The flat farm county at the south-western tip of Ontario, between Lake St. Clair and Lake Erie, where Jeff Lemire grew up. His graphic trilogy Essex County (2008–2009) follows the LeBeuf family and their neighbours across generations among its fields, barns and gas stations",
        "安大略西南端圣克莱尔湖和伊利湖之间一片平坦的农业县，杰夫·勒米尔在这里长大。他的图像小说三部曲《埃塞克斯县》（2008–2009）在这里的农田、谷仓和加油站之间，跟着勒伯夫一家和邻居们走过几代人"),
]

lines = [
    dict(id="sunshine-q1", book_id="sunshine-sketches", place_ids=["ca-orillia"], location="Chapter I, “The Hostelry of Mr. Smith”", location_zh="第一章《史密斯先生的旅馆》",
         text_en="\n".join([
             para(SUN, "I don't know whether you know Mariposa.", "a dozen towns just like it."),
             para(SUN, "There it lies in the sunlight,", "to and from the Local Option Townships."),
             para(SUN, "In point of geography the lake is called Lake Wissanotti", "and the county Missinaba County.")]),
         highlight_en=["Mariposa", "Lake Wissanotti"],
         text_zh="我不知道你知不知道马里波萨。不知道也没关系，因为只要你对加拿大稍有了解，大概就熟悉十来个跟它一模一样的小镇。\n它就躺在阳光里，从山坡脚下铺开的小湖边一路往坡上延伸，小镇就建在这片山坡上。湖边有一座码头，码头旁泊着一艘汽船，拴船的两根缆绳和“卢西塔尼亚号”上用的差不多粗。这艘汽船哪儿也不去，因为这湖四面不通外水，“马里波萨美人号”无处可航，只在七月一日和女王诞辰日“跑几趟”，再载着皮西厄斯骑士会和禁酒之子会的人，往返于那几个实行地方禁酒的镇区。\n从地理上说，这湖叫维萨诺蒂湖，从湖里流出去的河叫奥萨维皮河，正如马里波萨的大街叫米西纳巴街，这个县叫米西纳巴县。",
         highlight_zh=["马里波萨", "维萨诺蒂湖"], translation="original", status="draft", checked=f"English Wikisource, {SUN}, {DATE}"),
    b.S("bestlaid-s1", "the-best-laid-plans", "ca-parliament-hill", "Throughout", "全书",
        "Daniel Addison, a burnt-out speechwriter for the Liberal Leader of the Opposition on Parliament Hill, quits on the eve of an election to teach English at the University of Ottawa. As a last favour he must find a Liberal candidate for Cumberland-Prescott, a riding the party has no hope of winning against the popular Finance Minister, Eric Cameron. He rents the boathouse apartment of Angus McLintock, a crusty Scottish engineering professor mourning his wife and building a hovercraft, and strikes a deal: Daniel will teach Angus's hated English for Engineers class, and Angus will let his name stand, with no campaign and certain to lose. Then a scandal blows away Cameron, Angus is elected, and he decides to see what an honest MP who does not care about re-election can do in the House of Commons.",
        "丹尼尔·艾迪生是国会山上自由党反对党领袖的演讲撰稿人，心力交瘁，在大选前夕辞职，要去渥太华大学教英文。走前他得帮党最后一个忙：给坎伯兰-普雷斯科特选区找一个自由党候选人，在那里，党根本不可能赢过声望正隆的财政部长埃里克·卡梅伦。他租下了安格斯·麦克林托克船库上的公寓：这位脾气倔强的苏格兰工程学教授正为亡妻伤心，还在造一架气垫船。两人做了笔交易：丹尼尔替安格斯教他最讨厌的“工程师英语”课，安格斯则挂名参选，不拉票，稳输。不料一桩丑闻把卡梅伦掀翻，安格斯当选了；他决定看看，一个诚实又不在乎连任的议员，能在下议院里做成什么。",
        ["Parliament Hill", "Ottawa"], ["国会山", "渥太华"],
        "https://supersummary.com/the-best-laid-plans/summary; https://paperbackswap.com/Best-Laid-Plans-Terry-Fallis/book/059542872X; https://www.reddeeradvocate.com/columns/a-humorous-birds-eye-view-of-parliamentary-procedures/; https://www.penguinrandomhouse.com/books/47824/the-best-laid-plans-by-terry-fallis/; https://www.kfpl.ca/c/catalogue/record/1.592310; https://terryfallis.com/reviews-of-the-novel/"),
    b.S("orenda-s1", "the-orenda", "ca-sainte-marie", "Throughout", "全书",
        "Wendake, in the early seventeenth century. The story is told in turn by three voices: Bird, a Wendat warrior whose family was murdered by the Haudenosaunee; Snow Falls, a Haudenosaunee girl whose family Bird kills in revenge and whom he takes captive and raises as his daughter; and Christophe, a French Jesuit whom Bird also takes captive and calls the Crow. Christophe, mocked at first for his frailty and his poor grasp of the language, sets out to convert the Wendat; Champlain gives Bird a gun on condition that his village accept more priests, and more Jesuits come to help found a mission. Bird and Snow Falls grow into father and daughter as drought and war close in, until the Wendat face annihilation at the hands of the Haudenosaunee. Christophe is modelled on Jean de Brébeuf, co-founder of Sainte-Marie among the Hurons.",
        "十七世纪初的温达克。故事由三个声音轮流讲述：伯德，一个家人被豪德诺索尼人杀害的温达特战士；雪落，一个豪德诺索尼女孩，伯德为了复仇杀了她的家人，把她掳来当女儿养；还有克里斯托夫，一个同样被伯德俘虏、被叫作“乌鸦”的法国耶稣会士。克里斯托夫起初因为身子孱弱、话也说不好而遭人取笑，却一心要让温达特人皈依；尚普兰送给伯德一支枪，条件是他的村子接纳更多神父，又有耶稣会士来帮忙建传教站。干旱和战争步步逼近，伯德和雪落渐渐成了真正的父女，直到温达特人在豪德诺索尼人手下面临灭顶之灾。克里斯托夫的原型是休伦人中的圣玛丽传教站的创建者之一让·德·布雷伯夫。",
        ["Wendake"], ["温达克"],
        "https://en.wikipedia.org/wiki/The_Orenda; https://muse.jhu.edu/article/587822/summary; https://reviewcanada.ca/magazine/2013/10/the-terror-and-pity-of-contact/; https://www.penguinrandomhouse.com/books/228121/the-orenda-by-joseph-boyden/9780385350747; https://thecanadianencyclopedia.ca/article/a-small-detour-from-an-epic-story/; https://www.powells.com/biblio/1-9780345806451-0; https://en.wikipedia.org/wiki/Sainte-Marie_among_the_Hurons"),
    b.S("essex-s1", "essex-county", "ca-essex-county", "Throughout", "全书",
        "Three linked graphic stories set in the farm country of Essex County, Ontario. In Tales from the Farm, ten-year-old Lester, whose mother has died of cancer, goes to live with his uncle Ken on the farm, wears a mask and cape and draws his own comics, and against his uncle's wishes befriends Jimmy LeBeuf, who runs the local gas station after a head injury ended his career with the Toronto Maple Leafs in his first professional game. In Ghost Stories the deaf, aging Lou LeBeuf, Jimmy's great-uncle, looks back on the years when he and his brother Vince played hockey in Toronto. In The Country Nurse, Anne Quenneville makes her rounds of the county, looking in on Lou, Jimmy, Ken and Lester, and is more closely tied to the LeBeufs than she knows.",
        "三个相互勾连的图像故事，发生在安大略埃塞克斯县的农田之间。《农场故事》里，十岁的莱斯特母亲死于癌症，被送到舅舅肯的农场上生活；他戴着面具、披着斗篷，自己画漫画，不顾舅舅反对，和吉米·勒伯夫交上了朋友：吉米曾效力多伦多枫叶队，却在第一场职业比赛里伤了头，从此只能在当地经营加油站。《鬼故事》里，吉米的叔祖、又聋又老的卢·勒伯夫回想当年他和弟弟文斯在多伦多打冰球的日子。《乡村护士》里，安妮·克内维尔在全县巡诊，探望卢、吉米、肯和莱斯特，她和勒伯夫一家的牵连比她自己知道的还要深。",
        ["Essex County"], ["埃塞克斯县"],
        "https://www.ebsco.com/research-starters/literature-and-writing/complete-essex-county; https://blogs.tpl.ca/agincourt/2010/07/book-review-essex-county-trilogy-by-jeff-lemire; https://quillandquire.com/review/essex-county-vol-1-tales-from-the-farm/; https://www.goodreads.com/book/show/18867840; https://www.criticsatlarge.ca/2014/06/tragi-comic-jeff-lemires-essex-county.html; https://en.wikipedia.org/wiki/Essex_County_Trilogy"),
    b.S("threeday-s1", "three-day-road", "ca-moose-factory", "Throughout", "全书",
        "1919. Niska, an Oji-Cree healer and the last of her people to live off the land, has raised her nephew Xavier Bird and his friend Elijah Whiskeyjack in the old ways in the bush near Moose Factory. Told that Xavier has been killed in the war and Elijah is coming home, she paddles to meet the train in the town, and it is Xavier who steps off it, one leg gone and addicted to morphine. On the three-day canoe journey home she tells him the stories of her life to keep him alive, while he remembers how the two Cree boys enlisted in 1915, became feared snipers at Ypres and the Somme, and how Elijah changed. The title comes from Niska's teaching that those who are dying walk the three-day road.",
        "1919 年。尼斯卡是一位奥吉布瓦-克里族的医者，也是她那一族最后一个靠土地为生的人，她在穆斯工厂附近的林子里，用老法子把侄子泽维尔·伯德和他的朋友以利亚·威士忌杰克带大。她听说泽维尔已经战死、以利亚要回来了，便划着独木舟到镇上去接火车，下车的却是泽维尔：一条腿没了，还染上了吗啡瘾。在三天的独木舟归途上，她给他讲自己一生的故事，想让他活下去；他则回忆两个克里族男孩怎样在 1915 年参军，怎样在伊珀尔和索姆河成了令人生畏的狙击手，以利亚又怎样变了一个人。书名来自尼斯卡的教导：将死之人要走三日之路。",
        ["Moose Factory"], ["穆斯工厂"],
        "https://en.wikipedia.org/wiki/Three_Day_Road; https://quillandquire.com/review/three-day-road/; https://mhs.mb.ca/docs/mb_history/59/threedayroad.shtml; https://www.thecanadianencyclopedia.ca/en/article/three-day-road; https://reviewcanada.ca/magazine/2005/06/cree-heroes-in-a-european-war/; https://www.litcharts.com/lit/three-day-road/summary"),
    b.S("livesgirls-s1", "lives-of-girls-and-women", "ca-wingham", "Throughout", "全书",
        "Del Jordan grows up in the 1940s at the end of the Flats Road, outside the small Ontario town of Jubilee, where her father keeps silver foxes; the road, she says, is not part of town but not part of the country either. Her first companions are her younger brother Owen and Uncle Benny, an eccentric neighbour who is nobody's uncle. Her mother Ada, agnostic and opinionated, sells encyclopedias to the farmers and moves with Del into town, where Del lives among women: her mother, the boarder Fern Dogherty, her best friend Naomi. Through school, a search for a religion, the clever Jerry Storey and her first love, the Baptist Garnet French, Del works out what kind of woman she will be. Munro's only novel; Jubilee is drawn from Wingham, where she grew up.",
        "二十世纪四十年代，德尔·乔丹在安大略小镇朱比利外弗拉茨路的尽头长大，父亲在那里养银狐；她说，这条路既不算镇上，也不算乡下。她最早的伙伴是弟弟欧文和本尼叔叔，一个谁的叔叔也不是的古怪邻居。母亲艾达不信神、主意多，向农民们推销百科全书，后来带着德尔搬进了镇里；德尔从此生活在女人们中间：母亲、房客弗恩·多尔蒂、好朋友娜奥米。经过学校、对宗教的一番追寻、聪明的杰里·斯托里，还有初恋、浸信会教徒加尼特·弗伦奇，德尔慢慢想明白自己要做一个什么样的女人。这是门罗唯一的长篇小说；朱比利取材于她长大的温厄姆。",
        ["Jubilee", "Ontario"], ["朱比利", "安大略"],
        "https://en.wikipedia.org/wiki/Lives_of_Girls_and_Women; https://www.supersummary.com/lives-of-girls-and-women/summary; https://www.penguinrandomhouse.com/books/118611; https://www.ebsco.com/research-starters/literature-and-writing/lives-girls-and-women-alice-munro; https://www.supersummary.com/lives-of-girls-and-women/symbols-and-motifs"),
    b.S("whodoyou-s1", "who-do-you-think-you-are", "ca-wingham", "Throughout", "全书",
        "Ten linked stories of Rose, from girlhood to middle age, and her stepmother Flo. Rose grows up poor in West Hanratty, Ontario, with Flo and a father who beats her. At school in the better part of town she lies that she had half a grapefruit for breakfast, and the lie haunts her. A scholarship takes her to university, where Patrick, heir to a rich family, falls for her as a king falls for a beggar maid; she marries him, leaves him, becomes an actress, and at last comes home to Hanratty, where she finds an answer to the question the town has always asked: who do you think you are? It won the Governor General's Award in 1978 and was shortlisted for the Booker Prize in 1980 as The Beggar Maid.",
        "十个相互勾连的故事，写罗丝从少女到中年，以及她的继母弗洛。罗丝在安大略的西汉拉蒂贫穷地长大，身边是弗洛和一个会打她的父亲。在镇上较体面那一头的学校里，她谎称早饭吃了半个葡萄柚，这个谎言一直纠缠着她。一份奖学金把她送进了大学，富家子弟帕特里克像国王爱上乞丐少女那样爱上了她；她嫁给了他，又离开了他，当了演员，最后回到汉拉蒂，在那里找到了小镇一直在问的那个问题的答案：你以为你是谁？此书获 1978 年总督奖，1980 年以《乞丐少女》之名入围布克奖短名单。",
        ["West Hanratty", "Ontario"], ["西汉拉蒂", "安大略"],
        "https://en.wikipedia.org/wiki/Who_Do_You_Think_You_Are%3F_(short_story_collection); https://ojs.library.ubc.ca/index.php/canlit/article/view/194216/190124; https://canlitguides.ca/?p=53500; https://canlitguides.ca/nadine-fladd/an-introduction-to-the-short-story-in-canada-reading-alice-munros-who-do-you-think-you-are/literary-analysis-of-the-short-story/; https://mookseandgripes.com/reviews/2015/02/18/alice-munro-royal-beatings/"),
]

EDITS = [
    ("where her father kept silver foxes; the farm country of Huron County fills her first book, Dance of the Happy Shades.",
     "where her father kept silver foxes; in Lives of Girls and Women (1971) Del Jordan grows up on her father's fox farm at the end of the Flats Road outside Jubilee, and in Who Do You Think You Are? (1978) Rose grows up in West Hanratty."),
    ("父亲养银狐；休伦县的农庄田野写满了她的第一本书《快乐影子之舞》。",
     "父亲养银狐；《女孩和女人的生活》（1971）里，德尔·乔丹在朱比利镇外弗拉茨路尽头父亲的狐狸场上长大，《你以为你是谁？》（1978）里的罗丝则在西汉拉蒂长大。"),
    ("while his niece Annie tells him of her year in Toronto, Montreal and New York",
     "while his niece Annie tells him of her year in Toronto, Montreal and New York. In Boyden's first novel, Three Day Road, Xavier Bird and his friend Elijah grow up in the bush around Moose Factory before going to the First World War as snipers"),
    ("侄女安妮对他讲她在多伦多、蒙特利尔和纽约度过的一年",
     "侄女安妮对他讲她在多伦多、蒙特利尔和纽约度过的一年。博伊登的第一部小说《三日之路》里，泽维尔·伯德和朋友以利亚在穆斯工厂周围的林子里长大，后来一同去打第一次世界大战，当了狙击手"),
]
def edit_notes(path):
    s = open(path, encoding="utf-8").read()
    for a, c in EDITS:
        assert s.count(a) == 1, a
        s = s.replace(a, c)
    open(path + ".new", "w", encoding="utf-8").write(s); os.replace(path + ".new", path)

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "books.js"))))
all_places = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "places.js"))))
all_lines = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "lines.js"))))
assert not {x["id"] for x in books} & all_books
assert {p["id"] for p in places} == set(CO) and not set(CO) & all_places and {"ca-wingham", "ca-moose-factory"} <= all_places
assert not {l["id"] for l in lines} & all_lines
if __name__ == "__main__":
    note = "11-28 Canada rule-v2 re-check, batch 4: Ontario (add_ca_v2_1128_4.py)"
    append(b.data("books.js"), books, note)
    append(b.data("places.js"), places, note)
    append(b.data("lines.js"), lines, note)
    edit_notes(b.data("places.js"))
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
