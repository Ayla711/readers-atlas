"""11-24: Australia, second pack (first half of the 27 books that selection rule v2 adds; tools/selection/au.md).
Scene notes in our own words for the books in copyright; one quotation from English Wikisource for The Fortunes of
Richard Mahony (public domain), Australia Felix/Proem. Places, with the reason for each:
- Cloudstreet: Cloud Street is invented; West Leederville, where the 2011 television series (written by Winton) puts the
  house, and where a Perth reader placed it (Kimberley Street) (prototype, honest note).
- The Slap: Northcote, Melbourne, where Hector and Aisha hold the barbecue (JASAL, Bennett).
- Voss: Sydney, where the novel opens in 1845 in the merchant Bonner's house and where Laura waits.
- Oscar and Lucinda: Bellingen, on the Bellinger River, where the glass church is taken (named in the novel).
- Eucalyptus: the property in western New South Wales and its "one-horse town" are unnamed. Under the rule for famous books
  it is hung at Bellingen, where sets were built in 2005 for a film of the novel that was cancelled before shooting began.
  This is the weakest tie in the pack and is said so in the note.
- A Fortunate Life: Wickepin, where Facey worked as a youth and farmed in 1922–1934; his homestead stands in the main street.
- Breath: Sawyer is invented; shown at Denmark, WA, where Simon Baker's 2017 film was shot (film location; the novel's
  summary is in the film place's scene text). Sources: https://journal.wildbounds.com/journal/posts/wildbounds-must-read-breath;
  https://www.wikipedia.org/wiki/Breath_(novel); https://libraries.dlrcoco.ie/staff-picks/breath; https://www.nybooks.com/articles/21714;
  https://www.goodreads.com/book/show/6076974
- My Brother Jack: Elsternwick, Johnston's childhood home suburb (prototype, honest note).
- The Narrow Road to the Deep North: Cleveland, Tasmania, Dorrigo Evans's home hamlet (named in the novel).
- Dirt Music: White Point is invented; shown at Esperance, where Gregor Jordan's 2019 film stood it in (film location).
  Sources: https://esperancetide.com/now-showing-tim-wintons-dirt-music.html; https://en.wikipedia.org/wiki/Dirt_Music_(film);
  https://www.inkl.com/news/rednecks-of-the-outback; https://www.kirkusreviews.com/book-reviews/tim-winton/dirt-music/print/;
  https://literature.britishcouncil.org/writer/tim-winton; https://www.supersummary.com/dirt-music/background/
- Carpentaria: Desperance is invented; Normanton, which a review in Overland reads as its model (prototype, honest note).
- Monkey Grip: Fitzroy, Melbourne, the share houses and the Fitzroy baths.
- The Tree of Man: Durilgai is invented; Castle Hill, where White farmed from 1948 (prototype).
- The Fortunes of Richard Mahony: Ballarat, the goldfield of the first book (quotation).
Photos: tools/content/batches/add_photos_au_1124.py.

Usage: python3 -I tools/content/batches/add_au2.py <app_dir> tools/content/batches/coords/add_au2.json <wikisource_root>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP = sys.argv[1]
CO = json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-24"
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]
def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, lang, aliases, pd=False, src=None):
    return dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
                orig_lang=lang, public_domain=pd, source_url=src, author_orig=author_orig, aliases=aliases)
def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
def check(books, places, lines):
    """every book has a line or is carried by a film location (which takes no excerpt); every place has a line or is a film
    location"""
    allb = set()
    for f in glob.glob(os.path.join(APP, "data", "*", "books.js")): allb |= ids_in(f)
    bk = {x["id"] for x in books}
    assert not bk & allb, bk & allb
    assert not {p["id"] for p in places} & ids_in(b.data("places.js")) and {p["id"] for p in places} == set(CO)
    assert not {l["id"] for l in lines} & ids_in(b.data("lines.js"))
    film = {p["id"]: set(p["book_ids"]) for p in places if p["place_type"] == "film_location"}
    for l in lines:
        assert l["book_id"] in bk and l["place_ids"][0] in {p["id"] for p in places} and l["place_ids"][0] not in film, l["id"]
    assert {l["book_id"] for l in lines} | set().union(set(), *film.values()) == bk
    assert {l["place_ids"][0] for l in lines} | set(film) == {p["id"] for p in places}
def run(books, places, lines, script):
    M = f"11-24: Australia, books that selection rule v2 adds (tools/content/batches/{script})"
    for name, xs in (("books.js", books), ("places.js", places), ("lines.js", lines)):
        if xs: b.append(b.data(name), xs, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
import wikisource as ws
WSR = sys.argv[3]
def EN(id, book, place, loc, loc_zh, title, text, hl, zh, hl_zh):
    assert "[" not in text and "]" not in text and "\xa0" not in text and "  " not in text, (id, text[:40])
    for h in hl: assert h in text, (id, h)
    for h in hl_zh: assert h in zh, (id, h)
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh, text_en=text, highlight_en=hl, translation="original",
                text_zh=zh, highlight_zh=hl_zh, status="draft", checked=f"English Wikisource, {title}, {DATE}")
b.init(APP, "", "au", DATE)
T_RM = "Australia Felix/Proem"
_t = ws.text(os.path.join(WSR, "en"), T_RM)
assert _t.count("Thus the pale-eyed multitude worried the surface") == 1
RM = re.sub(r" {2,}", " ", ws.block(os.path.join(WSR, "en"), T_RM, "Thus the pale-eyed multitude worried the surface",
                                    "a stupendous discovery.").replace("\n", " "))
books = [
    BK("cloudstreet", "Cloudstreet", "云街", "Cloudstreet", "Tim Winton", "蒂姆·温顿", "Tim Winton", "1991", "en",
       ["Cloud Street", "the Pickles", "the Lambs", "Fish Lamb", "Quick Lamb", "Rose Pickles"]),
    BK("the-slap", "The Slap", "一巴掌", "The Slap", "Christos Tsiolkas", "克里斯托斯·齐奥尔卡斯", "Christos Tsiolkas", "2008", "en",
       ["Hector", "Aisha", "Harry", "Hugo"]),
    BK("voss", "Voss", "沃斯", "Voss", "Patrick White", "帕特里克·怀特", "Patrick White", "1957", "en",
       ["Johann Ulrich Voss", "Laura Trevelyan", "Leichhardt"]),
    BK("oscar-and-lucinda", "Oscar and Lucinda", "奥斯卡与露辛达", "Oscar and Lucinda", "Peter Carey", "彼得·凯里", "Peter Carey", "1988", "en",
       ["Oscar Hopkins", "Lucinda Leplastrier", "glass church"]),
    BK("eucalyptus-bail", "Eucalyptus", "桉树", "Eucalyptus", "Murray Bail", "默里·贝尔", "Murray Bail", "1998", "en",
       ["Ellen Holland", "Holland", "Mr Cave"]),
    BK("a-fortunate-life", "A Fortunate Life", "幸运人生", "A Fortunate Life", "A. B. Facey", "A. B. 费西", "Albert Facey", "1981", "en",
       ["Albert Facey", "Bert Facey"]),
    BK("breath-winton", "Breath", "呼吸", "Breath", "Tim Winton", "蒂姆·温顿", "Tim Winton", "2008", "en",
       ["Pikelet", "Bruce Pike", "Loonie", "Sando", "Sawyer"]),
    BK("my-brother-jack", "My Brother Jack", "我的兄弟杰克", "My Brother Jack", "George Johnston", "乔治·约翰斯顿", "George Johnston", "1964", "en",
       ["David Meredith", "Jack Meredith", "Meredith trilogy"]),
    BK("narrow-road-deep-north", "The Narrow Road to the Deep North", "深入北方的小路", "The Narrow Road to the Deep North",
       "Richard Flanagan", "理查德·弗兰纳根", "Richard Flanagan", "2013", "en", ["Dorrigo Evans", "Amy Mulvaney", "Burma railway"]),
    BK("dirt-music", "Dirt Music", "土乐", "Dirt Music", "Tim Winton", "蒂姆·温顿", "Tim Winton", "2001", "en",
       ["Georgie Jutland", "Luther Fox", "White Point"]),
    BK("carpentaria", "Carpentaria", "卡奔塔利亚", "Carpentaria", "Alexis Wright", "亚历克西斯·赖特", "Alexis Wright", "2006", "en",
       ["Desperance", "Normal Phantom", "Norm Phantom", "Will Phantom", "Elias Smith"]),
    BK("monkey-grip", "Monkey Grip", "猴握", "Monkey Grip", "Helen Garner", "海伦·加纳", "Helen Garner", "1977", "en",
       ["Nora", "Javo"]),
    BK("tree-of-man", "The Tree of Man", "人树", "The Tree of Man", "Patrick White", "帕特里克·怀特", "Patrick White", "1955", "en",
       ["Stan Parker", "Amy Parker", "Durilgai"]),
    BK("richard-mahony", "The Fortunes of Richard Mahony", "理查德·马奥尼的命运", "The Fortunes of Richard Mahony",
       "Henry Handel Richardson", "亨利·汉德尔·理查森", "Henry Handel Richardson", "1917–1929", "en",
       ["Australia Felix", "The Way Home", "Ultima Thule", "Richard Mahony", "Polly", "Mary Mahony"],
       pd=True, src="https://en.wikisource.org/wiki/Australia_Felix"),
]
places = [
    b.PROTO("au-west-leederville", "West Leederville, Perth", "西利德维尔，珀斯", *C("au-west-leederville"),
            "the Perth suburb where the great house at No. 1 Cloud Street is usually placed in Tim Winton's Cloudstreet (1991). Cloud Street is invented; the 2011 television series, which Winton co-wrote, puts the house in West Leederville, and a Perth reader has argued for Kimberley Street there",
            "蒂姆·温顿《云街》（1991）里那座云街一号大宅通常被放在的珀斯郊区。云街是虚构的；温顿参与编剧的 2011 年电视剧把这座房子放在西利德维尔，一位珀斯读者还考证说就在那里的金伯利街"),
    b.ORIG("au-northcote", "Northcote, Melbourne", "诺斯科特，墨尔本", *C("au-northcote"),
           "Inner-northern suburb of Melbourne. In Christos Tsiolkas's The Slap (2008) it is where Hector and Aisha live, and where, at their backyard barbecue, a man slaps another couple's child",
           "墨尔本北部内城郊区。克里斯托斯·齐奥尔卡斯的《一巴掌》（2008）里，赫克托和艾莎住在这里；就在他们家后院的烧烤聚会上，一个男人打了别人家的孩子一巴掌"),
    b.ORIG("au-sydney", "Sydney", "悉尼", *C("au-sydney"),
           "Capital of New South Wales. Patrick White's Voss (1957) opens here in 1845, in the house of the merchant Edmund Bonner, patron of the German Voss's expedition across the continent; while Voss goes into the desert, Bonner's niece Laura Trevelyan waits in Sydney",
           "新南威尔士州首府。帕特里克·怀特的《沃斯》（1957）就在这里开篇：1845 年，商人埃德蒙·邦纳的家中——他资助德国人沃斯横穿大陆的探险。沃斯走进沙漠，邦纳的侄女劳拉·特里维廉在悉尼等待"),
    b.ORIG("au-bellingen", "Bellingen and the Bellinger River", "贝林根与贝林格河", *C("au-bellingen"),
           "Small town on the Bellinger River, on the mid-north coast of New South Wales. In Peter Carey's Oscar and Lucinda (1988) it is the remote settlement to which Oscar Hopkins, on a bet with Lucinda, carries a church made of glass, and on whose river the church goes down. The 1997 film was shot here too. Murray Bail's Eucalyptus (1998) is also shown here, more loosely: its property is unnamed, and sets were built at Bellingen in 2005 for a film of the novel that was cancelled",
           "新南威尔士州中北海岸贝林格河畔的小镇。彼得·凯里的《奥斯卡与露辛达》（1988）里，奥斯卡·霍普金斯和露辛达打赌，要把一座玻璃教堂运到的那个偏远定居点就是这里，教堂最后也沉在这条河上。1997 年的电影也在这里拍过。默里·贝尔的《桉树》（1998）也挂在这里，关系更松一些：书里的庄园没有地名，2005 年为这部小说的电影在贝林根搭过布景，电影后来取消了"),
    b.ORIG("au-wickepin", "Wickepin", "威克平", *C("au-wickepin"),
           "Wheatbelt town south-east of Perth. A. B. Facey, author of A Fortunate Life (1981), worked as a youth on farms around Wickepin and farmed south of the town with his family from 1922 to 1934; the house he built now stands in the main street as the Albert Facey Homestead, and an Albert Facey Heritage Trail leads to the places of the book",
           "珀斯东南的麦带小镇。《幸运人生》（1981）的作者 A. B. 费西少年时在威克平一带的农场干活，1922 至 1934 年又带着一家人在镇南务农；他亲手盖的房子如今搬到了主街上，叫阿尔伯特·费西故居，还有一条“阿尔伯特·费西遗产小径”串起书里的地方"),
    b.P("au-denmark-wa", "Denmark, Western Australia", "丹麦（西澳）", *C("au-denmark-wa"), "film_location",
        adaptation={"title": "Breath", "year": 2017, "kind": "电影"},
        scene="西蒙·贝克 2017 年把蒂姆·温顿的《呼吸》拍成电影，在西澳南海岸的丹麦镇一带拍摄；书里的几处浪，原型就是那一带的秘密冲浪点。小说里的索耶镇是虚构的：二十世纪七十年代，海边一个伐木、养奶牛的小镇。布鲁斯·派克（外号“小煎饼”）和酒馆老板那没妈管、野性十足的儿子伊万·鲁恩（外号“疯子”）交上了朋友；两个男孩比赛在水下憋气，后来又被老练的大浪冲浪手桑多迷住，跟着他去冲越来越危险的浪。摘句不能挂在影视取景地上，所以这本书通过这部电影出现在这里",
        book_ids=["breath-winton"],
        scene_en="Simon Baker's 2017 film of Tim Winton's Breath was shot around Denmark, on the south coast of Western Australia, where some of the waves in the book were based on secret surf spots. The novel's town, Sawyer, is invented: a small logging and dairy town near the sea in the 1970s. Bruce Pike, 'Pikelet', befriends Ivan Loon, 'Loonie', the publican's wild, motherless son; the two boys dare each other to hold their breath under water, then fall under the spell of Sando, a veteran big-wave surfer, who leads them to ever more dangerous waves. Excerpts cannot be hung on a film location, so the book is shown here through the film"),
    b.PROTO("au-elsternwick", "Elsternwick, Melbourne", "埃尔斯特恩威克，墨尔本", *C("au-elsternwick"),
            "the Melbourne suburb where David Meredith and his elder brother Jack grow up between the wars in George Johnston's semi-autobiographical My Brother Jack (1964). Johnston himself grew up in the family home in Elsternwick, with his real brother Jack",
            "乔治·约翰斯顿半自传小说《我的兄弟杰克》（1964）里，大卫·梅瑞狄斯和哥哥杰克在两次大战之间长大的墨尔本郊区。约翰斯顿本人就在埃尔斯特恩威克的家中长大，他也真有一个哥哥叫杰克"),
    b.ORIG("au-cleveland-tas", "Cleveland, Tasmania", "克利夫兰（塔斯马尼亚）", *C("au-cleveland-tas"),
           "Hamlet in the Midlands of Tasmania. In Richard Flanagan's The Narrow Road to the Deep North (2013), which won the Booker Prize, it is the remote hamlet of some forty people where Dorrigo Evans grows up before he becomes a surgeon",
           "塔斯马尼亚中部的小村。理查德·弗兰纳根获布克奖的《深入北方的小路》（2013）里，这是多里戈·埃文斯长大的偏远小村，只有四十来口人；后来他成了外科医生"),
    b.P("au-esperance", "Esperance, Western Australia", "埃斯佩兰斯（西澳）", *C("au-esperance"), "film_location",
        adaptation={"title": "Dirt Music", "year": 2019, "kind": "电影"},
        scene="格雷戈尔·乔丹 2019 年把蒂姆·温顿的《土乐》拍成电影，主要在西澳南海岸的埃斯佩兰斯一带拍摄，用它来演小说里的怀特角，另有部分在金伯利和珀斯。小说里的怀特角是个虚构的渔镇，在珀斯以北几个小时车程的海岸上，靠龙虾热发了财，人也粗野。四十岁的前护士乔治·贾特兰跟丧偶的渔夫吉姆·巴克里奇和他的两个儿子住在一起；她爱上了卢瑟·福克斯——一个沉在悲伤里的外来人，靠偷吉姆的龙虾笼过活，守着回忆和音乐独自过日子。私情败露后，福克斯一路北逃，去了偏远海岸上一个虚构的“加冕湾”。摘句不能挂在影视取景地上，所以这本书通过这部电影出现在这里",
        book_ids=["dirt-music"],
        scene_en="Gregor Jordan's 2019 film of Tim Winton's Dirt Music was shot mainly around Esperance, on the south coast of Western Australia, which stood in for the novel's White Point, and partly in the Kimberley and Perth. In the novel, White Point is an invented fishing town some hours' drive north of Perth, grown rich and rough on a lobster boom. Georgie Jutland, a forty-year-old former nurse, lives there with Jim Buckridge, a widowed fisherman, and his two sons; she falls for Luther Fox, a grieving outsider who poaches Jim's pots and lives alone with his memories and his music. When the affair comes out, Fox flees far north to Coronation Gulf, an invented stretch of remote coast. Excerpts cannot be hung on a film location, so the book is shown here through the film"),
    b.PROTO("au-normanton", "Normanton, Queensland", "诺曼顿（昆士兰）", *C("au-normanton"),
            "the Gulf town that the fictional Desperance of Alexis Wright's Carpentaria (2006) appears to be modelled on. Desperance is invented; a review in Overland reads the name of the novel's leading figure, Norm Phantom, as a sign that it is based on Normanton, near the Gulf of Carpentaria in north-western Queensland",
            "亚历克西斯·赖特《卡奔塔利亚》（2006）里那个虚构小镇德斯佩兰斯看来所依据的海湾小镇。德斯佩兰斯是虚构的；《Overland》杂志的一篇书评从小说主角诺姆·范特姆的名字推断，它的原型是昆士兰西北、卡奔塔利亚湾边的诺曼顿"),
    b.ORIG("au-fitzroy", "Fitzroy, Melbourne", "菲茨罗伊，墨尔本", *C("au-fitzroy"),
           "Inner-city suburb of Melbourne. Helen Garner's Monkey Grip (1977) is set among the share houses of Fitzroy and Carlton in the mid-1970s, and its characters spend the summer at the Fitzroy Pool, where the sign over the deep end reads ACQUA PROFONDA",
           "墨尔本的内城郊区。海伦·加纳的《猴握》（1977）写的是 20 世纪 70 年代中期菲茨罗伊和卡尔顿一带的合租屋；书里的人整个夏天泡在菲茨罗伊泳池，池子深水区的牌子上写着 ACQUA PROFONDA（意大利语“深水”）"),
    b.PROTO("au-castle-hill", "Castle Hill, Sydney", "卡斯尔山，悉尼", *C("au-castle-hill"),
            "the district north-west of Sydney taken as the model of Durilgai, where Stan Parker clears his land in Patrick White's The Tree of Man (1955). White farmed at Castle Hill from 1948, on a small holding called Dogwoods much like the Parkers' place, and wrote the novel there",
            "帕特里克·怀特《人树》（1955）里斯坦·帕克开荒的杜里尔盖，通常认为原型就是悉尼西北的这一带。怀特从 1948 年起在卡斯尔山一块叫“山茱萸”的小农场上务农，跟帕克家的地很像，小说也是在那里写的"),
    b.ORIG("au-ballarat", "Ballarat", "巴拉瑞特", *C("au-ballarat"),
           "Gold-rush city in Victoria. Henry Handel Richardson's trilogy The Fortunes of Richard Mahony (1917–1929) opens on the Ballarat diggings in the 1850s, where Mahony, an Irish doctor trained in Edinburgh, keeps a store before going back to medicine; Richardson drew him from her own father",
           "维多利亚州的淘金城。亨利·汉德尔·理查森的三部曲《理查德·马奥尼的命运》（1917—1929）从 1850 年代巴拉瑞特的金矿工地开篇：在爱丁堡学过医的爱尔兰人马奥尼先在这里开店，后来重新行医；理查森以自己的父亲为原型写了他"),
]
lines = [
    b.S("au-cs-1", "cloudstreet", "au-west-leederville", "The novel as a whole", "全书",
        "In 1943, after separate disasters, two poor country families flee to Perth and come to share a huge, decaying house called Cloudstreet. The Pickles, who have inherited it, live on luck: Sam backs the bookies and his wife Dolly drinks. They let half the house to the Lambs, Lester and Oriel and their six children, devout and hard-working, who open a grocery shop on the ground floor. Over twenty years the two families, each the other's opposite, come to live as one tribe in the house, while Perth changes around them. (Cloud Street is invented; the television series puts the house in West Leederville.)",
        "1943 年，两户穷苦的乡下人家各自遭了难，逃到珀斯，合住进一座叫“云街”的破败大宅。继承了房子的皮克尔斯一家靠运气过日子：父亲山姆把钱押在赌马上，母亲多莉酗酒。他们把半座房子租给兰姆一家——莱斯特、奥丽尔和六个孩子，虔诚又勤快，在一楼开了家杂货铺。二十年里，这两家截然相反的人在这座房子里渐渐成了一个部落，珀斯也在他们身边变了样。（云街是虚构的；电视剧把房子放在西利德维尔。）",
        ["West Leederville"], ["西利德维尔"],
        "https://en.wikipedia.org/wiki/Cloudstreet; https://theory-practice.sydney.edu.au/?p=4391; https://en.wikipedia.org/wiki/Cloudstreet_(miniseries); https://www.wheelercentre.com/news-stories/2011/cloudstreet-takes-pride-of-place/"),
    b.S("au-sl-1", "the-slap", "au-northcote", "The barbecue", "烧烤聚会",
        "At a backyard barbecue at Hector and Aisha's house in Northcote, Hector's cousin Harry slaps Hugo, a small boy whose parents, Rosie and Gary, never check him. Rosie and Gary take Harry to court. The novel follows the fallout through eight people who were there, each chapter told from one of them — Hector, Aisha, Harry, Rosie, Hector's father, Connie, a schoolgirl who works in Aisha's veterinary clinic and is having an affair with Hector, and others — and through them shows the tensions of class, family and background in middle-class Melbourne.",
        "在诺斯科特赫克托和艾莎家后院的烧烤聚会上，赫克托的表兄哈利扇了小男孩雨果一巴掌——雨果的父母罗茜和加里从来不管他。罗茜和加里把哈利告上了法庭。小说透过当时在场的八个人追踪这件事的后果，每章换一个人的视角：赫克托、艾莎、哈利、罗茜、赫克托的父亲、在艾莎的兽医诊所打工并和赫克托有私情的中学女生康妮，等等；借着他们，写出了墨尔本中产生活里阶层、家庭和出身之间的种种紧张。",
        ["Northcote"], ["诺斯科特"],
        "https://openjournals.library.sydney.edu.au/JASAL/article/view/9831/9719; https://en.wikipedia.org/wiki/The_Slap_(novel); https://www.austlit.edu.au/austlit/page/C678611; https://tribune.com.pk/story/26307/a-barbecue-gone-bad; https://medhum.med.nyu.edu/view/18103"),
    b.S("au-vo-1", "voss", "au-sydney", "Sydney, 1845, and the desert", "1845 年的悉尼，与沙漠",
        "Sydney, 1845. Johann Ulrich Voss, a German, calls on the merchant Edmund Bonner, patron of his expedition to cross the continent, and meets Bonner's orphaned niece, Laura Trevelyan. The expedition sails to Newcastle, takes on more men at an outpost and heads into the desert, where it falls apart: some die, others turn back, and Voss is killed. Through the long separation Voss and Laura are bound to each other in visions, and in Sydney Laura adopts Mercy, the child of her servant Rose. White drew on the explorer Ludwig Leichhardt, who disappeared in the interior in 1848.",
        "1845 年的悉尼。德国人约翰·乌尔里希·沃斯去拜访商人埃德蒙·邦纳——他横穿大陆的探险的资助人，在那里结识了邦纳父母双亡的侄女劳拉·特里维廉。探险队乘船到纽卡斯尔，在一处边远站点又招了人，随后走进沙漠，在那里散了架：有人死去，有人折返，沃斯也被杀了。在漫长的分离里，沃斯和劳拉靠幻象彼此相连；在悉尼，劳拉收养了女仆罗丝的孩子默西。怀特笔下的沃斯取材于 1848 年在内陆失踪的探险家路德维希·莱希哈特。",
        ["Sydney"], ["悉尼"],
        "https://en.wikipedia.org/wiki/Voss_(novel); https://www.ebsco.com/research-starters/literature-and-writing/voss-patrick-white; https://www.themodernnovel.org/?p=863; https://www.penguinrandomhouse.com/books/300126/voss-by-patrick-white/readers-guide/"),
    b.S("au-ol-1", "oscar-and-lucinda", "au-bellingen", "The glass church", "玻璃教堂",
        "Oscar Hopkins, an Anglican clergyman and son of a Plymouth Brethren preacher in Devon, and Lucinda Leplastrier, a young Australian heiress who has bought a glass factory in Sydney, meet on the ship to New South Wales and are drawn together by a shared passion for gambling. Lucinda bets Oscar that he cannot carry a church made of glass from Sydney to a remote settlement at Bellingen, some 400 kilometres up the coast. The journey overland is brutal. At last the glass church is floated on the Bellinger River, and Oscar, praying inside it, drowns as it sinks.",
        "奥斯卡·霍普金斯是英国国教的牧师，父亲是德文郡普利茅斯弟兄会的传道人；露辛达·勒普拉斯特里耶是澳大利亚的年轻女继承人，在悉尼买下了一家玻璃厂。两人在开往新南威尔士的船上相遇，因为同样嗜赌而走到一起。露辛达跟奥斯卡打赌，说他没法把一座玻璃造的教堂从悉尼运到沿海岸往北四百来公里、贝林根的一个偏远定居点。陆上的路途十分残酷。最后，玻璃教堂被放到贝林格河上漂流，奥斯卡在里面祈祷，教堂沉没，他也淹死了。",
        ["Bellingen", "Bellinger River"], ["贝林根", "贝林格河"],
        "https://en.wikipedia.org/wiki/Oscar_and_Lucinda; https://victorianweb.org/neovictorian/carey/oscar/reactions.html; https://www.cornwall-calling.co.uk/film-television/oscar-and-lucinda.htm; https://aso.gov.au/titles/features/oscar-and-lucinda/map/"),
    b.S("au-eu-1", "eucalyptus-bail", "au-bellingen", "The novel as a whole", "全书",
        "On a property outside a one-horse town in western New South Wales, the widower Holland plants hundreds of species of eucalyptus, nearly every one there is. His daughter Ellen grows up into a 'speckled beauty' whose fame spreads far beyond the district, and when she is nineteen Holland announces that she will marry the man who can correctly name every tree on the property. Suitors come and fail, until Mr Cave, an expert on eucalypts, seems certain to win; meanwhile a young man Ellen meets among the trees tells her story after story. (The property is unnamed. The book is shown at Bellingen, where sets were built in 2005 for a film of the novel that was cancelled.)",
        "新南威尔士州西部，一个小得不能再小的镇子外有座庄园，鳏夫霍兰在上面种下了几百种桉树，几乎把所有的种都种全了。他的女儿埃伦长成了“满脸雀斑的美人”，名声远远传出了这一带；她十九岁那年，霍兰宣布：谁能把庄园里每一棵树的名字都叫对，就把女儿嫁给谁。求婚的人一个个来，一个个败下阵，直到桉树专家凯夫先生出现，眼看稳操胜券；与此同时，埃伦在树林里遇见一个年轻人，他给她讲了一个又一个故事。（庄园没有地名。这本书挂在贝林根：2005 年为这部小说的电影在那里搭过布景，后来电影取消了。）",
        ["Bellingen"], ["贝林根"],
        "https://en.wikipedia.org/wiki/Eucalyptus_(novel); https://www.everand.com/book/182526864/Eucalyptus-A-Novel; https://kirkusreviews.com/book-reviews/murray-bail/eucalyptus/print; https://herbdb.specify.csiro.au/asbs/newsletter/book-review-97c.html; https://wikimili.com/en/Eucalyptus_(novel)"),
    b.S("au-fl-1", "a-fortunate-life", "au-wickepin", "Wickepin years", "威克平的岁月",
        "Albert Facey's memoir of what he always counted a fortunate life. Born in 1894, he grew up on the Kalgoorlie goldfields and in the Western Australian wheatbelt, and as a youth worked on farms around Wickepin — the Meikles', the Phillipses', Moran's, the Bibbys' — clearing land for others. He fought at Gallipoli, and from 1922 to 1934 farmed with his family south of Wickepin, in a small house he built near Nomans Lake that now stands in the town's main street. He wrote the book in old age and died in 1982, nine months after it came out.",
        "阿尔伯特·费西的回忆录，写的是他始终认为“幸运”的一生。他生于 1894 年，在卡尔古利金矿区和西澳麦带长大；少年时在威克平一带的农场打工——米克尔家、菲利普斯家、莫兰家、比比家——替人开荒。他打过加里波利之战；1922 至 1934 年带着一家人在威克平南边务农，住在他自己在诺曼斯湖边盖的小房子里，那所房子如今就立在镇上的主街。他晚年才写成这本书，书出版九个月后去世，那是 1982 年。",
        ["Wickepin"], ["威克平"],
        "https://booktopia.com.au/a-fortunate-life-a-b-facey/book/9781925591385.html; https://en.wikipedia.org/wiki/Wickepin; https://trailswa.com.au/trails/trail/albert-facey-heritage-trail; https://visitwanderland.com.au/explore/golden-outback/albert-facey-homestead; https://aussietowns.com.au/?p=18872; https://www.foxeslair.org/uploads/5/4/9/1/54919621/spend_a_day_in_historic_wickepin_a3april_2024.pdf"),
    b.S("au-mbj-1", "my-brother-jack", "au-elsternwick", "A childhood between the wars", "两次大战之间的童年",
        "David Meredith tells of his childhood and youth in suburban Melbourne between the wars, in a house darkened by a father ruined by the Great War, and of his elder brother Jack: where David is tentative, Jack is fearless and takes the world head on. As they grow up, Jack shows loyalty and grit, while David, on his way to success as a journalist and war correspondent, betrays friends and family. The novel, Johnston's first directly autobiographical book, questions the suburban complacency and the idea of the typical Australian he grew up with. (Johnston himself grew up in Elsternwick.)",
        "大卫·梅瑞狄斯讲述他在两次大战之间墨尔本郊区的童年和少年：家里笼罩着被一战毁掉的父亲投下的阴影；还有他的哥哥杰克——大卫畏畏缩缩，杰克却天不怕地不怕，迎头撞向世界。长大以后，杰克忠诚而坚韧，大卫却在成为记者、战地记者的路上背叛了朋友和家人。这是约翰斯顿第一部直接写自己的小说，质疑了他从小身处的郊区自满，以及“典型澳大利亚人”的观念。（约翰斯顿本人在埃尔斯特恩威克长大。）",
        ["Elsternwick"], ["埃尔斯特恩威克"],
        "https://en.wikipedia.org/wiki/My_Brother_Jack; https://adb.anu.edu.au/biography/johnston-george-henry-10632; https://www.portrait.gov.au/people/george-johnston-1912; https://nadiawheatley.com/my-brother-jack"),
    b.S("au-nr-1", "narrow-road-deep-north", "au-cleveland-tas", "The novel as a whole", "全书",
        "Dorrigo Evans, a surgeon of seventy-seven, looks back on his life: a poor childhood in Cleveland, a Tasmanian hamlet of some forty souls; a love affair with Amy, his uncle's young wife; and the Second World War, when, as a prisoner of the Japanese, he and his fellow Australian prisoners were driven to build the Burma railway. Celebrated afterwards as a war hero, he lives on with what he cannot forget. Flanagan's own father was a prisoner on the railway.",
        "七十七岁的外科医生多里戈·埃文斯回望自己的一生：在塔斯马尼亚只有四十来口人的小村克利夫兰度过的穷苦童年；和叔叔的年轻妻子艾米的一段私情；还有第二次世界大战——他成了日本人的俘虏，和澳大利亚战俘同伴们一起被驱赶着修建缅甸铁路。战后他被奉为战争英雄，却一直带着无法忘却的东西活下去。弗兰纳根自己的父亲就是这条铁路上的战俘。",
        ["Cleveland"], ["克利夫兰"],
        "https://thebookerprizes.com/the-booker-library/features/an-extract-from-the-narrow-road-to-the-deep-north-by-richard-flanagan; https://search.icpl.org/Record/1442122; https://gulfnews.com/amp/story/general%2Flives-on-the-line-1.1367644; https://en.wikipedia.org/wiki/The_Narrow_Road_to_the_Deep_North_(novel)"),
    b.S("au-ca-1", "carpentaria", "au-normanton", "Desperance", "德斯佩兰斯",
        "Desperance, a coastal town on the Gulf of Carpentaria in north-western Queensland, lost its harbour early in the last century when, one Wet season, the river simply changed course. The town is split between the white Uptown and the Aboriginal Pricklebush people living on its edges, who are divided in their turn between Normal Phantom's Westend mob and old Joseph Midnight's renegade Eastend. When the mysterious Elias Smith, who walked out of the sea one day, is found murdered, old feuds wake up, and storms and cyclones suggest that the ancestors are stirring too. (Desperance is invented; a reviewer reads it as Normanton.)",
        "德斯佩兰斯是昆士兰西北、卡奔塔利亚湾边的一个海滨小镇；上世纪初的一个雨季，河流说改道就改道，小镇从此没了港口。镇子分成两半：白人住的“上城”，和住在镇子边缘的原住民“刺丛人”；刺丛人自己又分成诺默尔·范特姆的西头和老约瑟夫·米德奈特那伙不服管的东头。某天从海里走出来的神秘人物伊莱亚斯·史密斯被发现遭人杀害，旧仇随之苏醒，风暴和气旋也仿佛在说：祖先们同样不得安宁。（德斯佩兰斯是虚构的；有书评认为它就是诺曼顿。）",
        ["Normanton"], ["诺曼顿"],
        "https://en.wikipedia.org/wiki/Carpentaria_(novel); https://www.littlebrown.co.uk/titles/alexis-wright/carpentaria/9781845299484/; https://www.jcu.edu.au/__data/assets/pdf_file/0010/2367235/2026-Colin-Roderick-Memorial-Lecture-Ivor-Indyk.pdf; https://journals.jcu.edu.au/index.php/linq/article/download/2964/2918/5685; https://books.apple.com/book/isbn9781920882723; https://www.lrb.co.uk/v30/n08/elizabeth-lowry/the-fishman-lives-the-lore; https://www.staff.vu.edu.au/syson/187rev.pdf"),
    b.S("au-mg-1", "monkey-grip", "au-fitzroy", "Summer at the Fitzroy baths", "菲茨罗伊泳池的夏天",
        "Melbourne's inner north in the summer of 1975. Nora, a single mother in her thirties, lives in share houses among actors, musicians and other creative people, and falls in love with Javo, a young occasional actor and heroin addict who keeps drifting in and out of her life. Days begin with bacon at the kitchen table and play out on the hot concrete beside the Fitzroy baths; again and again Javo tries to get off heroin, and again and again Nora tries to get off him. Garner drew the novel from her own diaries of those years in Fitzroy and Carlton.",
        "1975 年夏天，墨尔本内城北区。三十多岁的单身母亲诺拉住在合租屋里，周围都是演员、乐手和各种搞创作的人；她爱上了贾沃——一个偶尔演演戏、染上海洛因的年轻人，总是在她的生活里来来去去。日子从厨房桌上的培根早餐开始，在菲茨罗伊泳池边滚烫的水泥地上消磨掉；贾沃一次又一次想戒掉海洛因，诺拉也一次又一次想戒掉他。加纳是根据自己那些年在菲茨罗伊和卡尔顿写的日记写成这部小说的。",
        ["Fitzroy"], ["菲茨罗伊"],
        "https://en.wikipedia.org/wiki/Monkey_Grip_(novel); https://overland.org.au/?p=71302; https://newleftreview.org/sidecar/posts/those-days; https://lrb.co.uk/v41/n06/merve-emre/on-the-dizzy-edge; https://en.wikipedia.org/wiki/Helen_Garner"),
    b.S("au-tm-1", "tree-of-man", "au-castle-hill", "The novel as a whole", "全书",
        "Early in the twentieth century Stan Parker, with only a horse and a dog for company, goes to a remote patch of scrub he has inherited in the hills outside Sydney, clears it, builds a rough house, and brings his wife Amy to the wilderness. Over a lifetime the two make a farm and a family and live through flood, fire and Stan's years at the war, while the bush around them becomes the settlement of Durilgai and at last the edge of the suburbs. (Durilgai is invented; White wrote the novel while farming at Castle Hill.)",
        "二十世纪初，斯坦·帕克只带着一匹马和一条狗，来到悉尼城外山里他继承的一片偏僻灌木地，开荒、盖起一座简陋的房子，再把妻子艾米接到这片荒野里。一辈子里，两人建起了农场，养大了孩子，熬过了洪水、大火和斯坦去打仗的那些年；他们周围的丛林也渐渐变成了杜里尔盖镇，最后成了郊区的边缘。（杜里尔盖是虚构的；怀特是在卡斯尔山务农时写下这部小说的。）",
        ["Castle Hill"], ["卡斯尔山"],
        "https://www.ebsco.com/research-starters/history/tree-man-analysis-setting; https://en.wikipedia.org/wiki/The_Tree_of_Man; https://trojanpress.com.au/wp-content/uploads/2019/06/Strangely-Humble-Ozlit-2.pdf; https://www.penguin.com.au/books/patrick-white/the-tree-of-man-9781741667707.aspx; https://goodreads.com/book/show/561413.The_Tree_of_Man"),
    EN("au-rm-1", "richard-mahony", "au-ballarat", "Australia Felix, Proem: the diggings", "《幸运的澳大利亚》序章：金矿工地", T_RM,
       RM, ["Ballarat"],
       "就这样，眼神黯淡的人群在地表上翻来刨去，又冒着丢命的风险、付出性命的代价往深处探。如今时兴深挖，淘金不再是绅士和外行的游戏；在这里苦干的，大多是吃过苦、经过磨炼的汉子。然而，尽管淘金已经沦为和别的行当一样艰辛而没准头的营生，早年那些神奇的大奖也难得再碰上，这座最有名的金矿却仍带着几分旧日的浪漫光彩，晃人眼睛，乱人心智。别处的淘洗槽边已经用上了马，人们也在议论碾碎石英的机器。可巴拉瑞特的淘金者抵制机器，生怕机器会把资本家带进来。他仍是那个做梦的人，那个心存戒备的个人主义者；他永远在一项惊天大发现的边缘徘徊。",
       ["巴拉瑞特"]),
]
check(books, places, lines)
if __name__ == "__main__":
    run(books, places, lines, "add_au2.py")
