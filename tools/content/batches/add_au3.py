"""11-24: Australia, third pack (second half of the 27 books that selection rule v2 adds; tools/selection/au.md).
Scene notes in our own words (all in copyright). Places, with the reason for each:
- True History of the Kelly Gang: Glenrowan, the last stand of June 1880, with which the novel opens.
- Boy Swallows Universe: Darra, Brisbane, where Eli Bell grows up.
- The Dry: Kiewarra is invented; shown at Beulah, renamed Kiewarra for Robert Connolly's 2020 film (film location).
  Sources: https://visitwimmeramallee.com.au/business-listing/self-drive-tour-of-the-dry-movie-locations/;
  https://editorial.rottentomatoes.com/article/eric-bana-hit-aussie-thriller-the-dry-will-transport-audiences-to-an-australia-rarely-seen-on-screen;
  https://vicscreen.vic.gov.au/news/the-dry; https://www.armidaleexpress.com.au/story/7010282/how-the-dry-is-set-to-make-this-town-and-its-residents-movie-stars/;
  https://en.wikipedia.org/wiki/The_Dry_(novel)
- Big Little Lies: the Pirriwee Peninsula is invented; Moriarty says it was inspired by the beaches north of Sydney, where
  she lived. Place: the Northern Beaches (prototype). Wikipedia: Pirriwee Public School "in Sydney's Northern Beaches".
- Remembering Babylon: the settlement is unnamed; Malouf drew on James Morrill, who came back to the settlers in 1863 at the
  Jarvisfield sheep station on the Burdekin. Place: the present locality of Jarvisfield (prototype, honest note).
- Tomorrow, When the War Began: Wirrawee is invented; shown at Raymond Terrace, whose King Street became Wirrawee's main
  street in Stuart Beattie's 2010 film (film location). Sources: https://en.wikipedia.org/wiki/Raymond_Terrace;
  https://en.wikipedia.org/wiki/Tomorrow,_When_the_War_Began_(film); https://en.wikipedia.org/wiki/Tomorrow,_When_the_War_Began
- Jasper Jones: Corrigan is invented; shown at Pemberton, where Rachel Perkins's 2017 film was shot (film location).
  Sources: https://www.screenwest.com.au/?p=13851; https://manjimup.wa.gov.au/our-places-and-spaces/jasperjones;
  https://australianbookreview.com.au/abr-arts/arts/3820-jasper-jones; https://en.wikipedia.org/wiki/Jasper_Jones;
  https://en.wikipedia.org/wiki/Jasper_Jones_(film)
- The Rosie Project: set in Melbourne; Don Tillman teaches genetics at a Melbourne university, which readers take as the
  University of Melbourne, where Simsion took his PhD (prototype, honest note).
- The Light Between Oceans: Janus Rock and Partageuse are invented; shown at Stanley, Tasmania, which stood in for
  Partageuse in Derek Cianfrance's 2016 film (film location). Sources: https://qantas.com/travelinsider/en/trending/hollywood-comes-to-the-historic-port-of-stanley.html;
  https://tasmaniantimes.com/?p=67810; https://d23.com/disney-a-to-z/light-between-oceans-the-film/;
  https://nzherald.co.nz/entertainment/movie-review-the-light-between-oceans/S5UVJQHGSZMCLYSB627WBXXIWE;
  https://penguin.com.au/books/the-light-between-oceans-9780857989888/extracts/1025-light-between-oceans
- Wild Dark Shore: Shearwater Island is invented, based on Macquarie Island, which McConaghy visited. The island lies about
  1,500 km south-south-east of Tasmania, outside the map's outline of Australia (validate.js allows 6 km at most), so the
  book is pinned at the Australian Antarctic Division at Kingston, near Hobart (prototype, honest note).
- Looking for Alibrandi: Glebe, Sydney, where Josie lives.
- The Magic Pudding: no real place in the story; the Norman Lindsay Gallery at Faulconbridge, the house (Springwood) where
  Lindsay wrote and drew it (pilgrimage).
- A Town Like Alice: Willstown is invented; Shute's own notes name Burketown as its prototype (prototype).
Photos: tools/content/batches/add_photos_au_1124.py.

Usage: python3 -I tools/content/batches/add_au3.py <app_dir> tools/content/batches/coords/add_au3.json"""
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
b.init(APP, "", "au", DATE)
FILM = lambda title, year: {"title": title, "year": year, "kind": "电影"}
books = [
    BK("true-history-kelly-gang", "True History of the Kelly Gang", "凯利帮真史", "True History of the Kelly Gang", "Peter Carey", "彼得·凯里",
       "Peter Carey", "2000", "en", ["Ned Kelly", "Kelly Gang", "Glenrowan"]),
    BK("boy-swallows-universe", "Boy Swallows Universe", "男孩吞下宇宙", "Boy Swallows Universe", "Trent Dalton", "特伦特·多尔顿", "Trent Dalton",
       "2018", "en", ["Eli Bell", "August Bell", "Slim Halliday", "Tytus Broz"]),
    BK("the-dry-harper", "The Dry", "旱", "The Dry", "Jane Harper", "简·哈珀", "Jane Harper", "2016", "en",
       ["Aaron Falk", "Kiewarra", "Luke Hadler"]),
    BK("big-little-lies", "Big Little Lies", "大小谎言", "Big Little Lies", "Liane Moriarty", "莉安·莫里亚蒂", "Liane Moriarty", "2014", "en",
       ["Pirriwee", "Madeline", "Celeste", "Jane", "Ziggy"]),
    BK("remembering-babylon", "Remembering Babylon", "忆巴比伦", "Remembering Babylon", "David Malouf", "戴维·马洛夫", "David Malouf", "1993", "en",
       ["Gemmy Fairley", "the McIvors", "Lachlan Beattie"]),
    BK("tomorrow-when-the-war-began", "Tomorrow, When the War Began", "明天，战争爆发时", "Tomorrow, When the War Began", "John Marsden",
       "约翰·马斯登", "John Marsden", "1993", "en", ["Tomorrow When the War Began", "Ellie Linton", "Wirrawee", "Hell", "Tomorrow series"]),
    BK("jasper-jones", "Jasper Jones", "贾斯珀·琼斯", "Jasper Jones", "Craig Silvey", "克雷格·西尔维", "Craig Silvey", "2009", "en",
       ["Charlie Bucktin", "Corrigan", "Eliza Wishart"]),
    BK("the-rosie-project", "The Rosie Project", "罗茜计划", "The Rosie Project", "Graeme Simsion", "格雷姆·辛普森", "Graeme Simsion", "2013", "en",
       ["Don Tillman", "Rosie Jarman", "Wife Project", "Father Project"]),
    BK("light-between-oceans", "The Light Between Oceans", "大洋之间的灯光", "The Light Between Oceans", "M. L. Stedman", "M. L. 斯特德曼",
       "M. L. Stedman", "2012", "en", ["Tom Sherbourne", "Isabel Sherbourne", "Janus Rock", "Partageuse"]),
    BK("wild-dark-shore", "Wild Dark Shore", "狂野黑暗的海岸", "Wild Dark Shore", "Charlotte McConaghy", "夏洛特·麦康纳吉", "Charlotte McConaghy",
       "2025", "en", ["Shearwater Island", "Dominic Salt", "Rowan"]),
    BK("looking-for-alibrandi", "Looking for Alibrandi", "寻找阿利布兰迪", "Looking for Alibrandi", "Melina Marchetta", "梅丽娜·马尔凯塔",
       "Melina Marchetta", "1992", "en", ["Josie Alibrandi", "Josephine Alibrandi", "Jacob Coote"]),
    BK("magic-pudding", "The Magic Pudding", "魔法布丁", "The Magic Pudding", "Norman Lindsay", "诺曼·林赛", "Norman Lindsay", "1918", "en",
       ["Bunyip Bluegum", "Bill Barnacle", "Sam Sawnoff", "Albert the Magic Pudding"]),
    BK("a-town-like-alice", "A Town Like Alice", "像爱丽丝那样的小镇", "A Town Like Alice", "Nevil Shute", "内维尔·舒特", "Nevil Shute", "1950", "en",
       ["The Legacy", "Jean Paget", "Joe Harman", "Willstown"]),
]
places = [
    b.ORIG("au-glenrowan", "Glenrowan", "格伦罗万", *C("au-glenrowan"),
           "Small town in north-eastern Victoria where, in June 1880, the Kelly Gang made its last stand in armour against the police. Peter Carey's True History of the Kelly Gang (2000), winner of the Booker Prize, opens with an account of that siege, and Ned's 'history' is presented as papers recovered from its smouldering ruins",
           "维多利亚州东北部的小镇。1880 年 6 月，凯利帮在这里披着铁甲同警察作最后一战。彼得·凯里获布克奖的《凯利帮真史》（2000）就以这场围攻的记述开篇，内德的“历史”被说成是从那片还在冒烟的废墟里找回来的手稿"),
    b.ORIG("au-darra", "Darra, Brisbane", "达拉，布里斯班", *C("au-darra"),
           "Outer suburb in south-western Brisbane. In Trent Dalton's Boy Swallows Universe (2018), drawn half from his own 1980s childhood, it is where twelve-year-old Eli Bell lives with his mute brother August and their mother Frankie; Dalton has called Darra's Vietnamese restaurants sacred spaces to him",
           "布里斯班西南的外围郊区。特伦特·多尔顿的《男孩吞下宇宙》（2018）一半取材于他自己 20 世纪 80 年代的童年；书里十二岁的伊莱·贝尔就和不说话的哥哥奥古斯特、母亲弗兰基住在这里。多尔顿说，达拉的越南餐馆对他来说是神圣的地方"),
    b.P("au-beulah", "Beulah, Victoria", "比尤拉（维多利亚州）", *C("au-beulah"), "film_location",
        adaptation=FILM("The Dry", 2020),
        scene="罗伯特·康诺利 2020 年把简·哈珀的《旱》拍成电影，几乎全在维多利亚州西北部的温默拉和马利地区拍摄：比尤拉在片中被改名为“基瓦拉”，是主人公家乡的核心，米尼普、霍普顿、沃拉克纳比尔、杰帕里特等小镇也被拼接进来。小说里的基瓦拉是虚构的农业小镇，正被大旱折磨。澳大利亚联邦警察阿伦·福克回乡参加儿时好友卢克·哈德勒一家的葬礼——人人都以为卢克杀了妻儿后自杀；卢克的父母请福克再查一查。二十年前，一个女孩死去，福克被怀疑，和父亲一起离开了小镇；那桩旧事和眼前的案子缠在了一起。摘句不能挂在影视取景地上，所以这本书通过这部电影出现在这里",
        book_ids=["the-dry-harper"],
        scene_en="Robert Connolly's 2020 film of Jane Harper's The Dry was shot almost entirely in the Wimmera and Mallee of north-western Victoria: Beulah, renamed Kiewarra for the film, stood at its centre, with towns such as Minyip, Hopetoun, Warracknabeal and Jeparit stitched in. In the novel Kiewarra is an invented farming town in the grip of drought. Aaron Falk, a federal police agent, comes home for the funeral of his childhood friend Luke Hadler and Luke's wife and son; everyone believes Luke killed his family and himself, but Luke's parents ask Falk to look again. Twenty years earlier, after the death of a girl of which he was suspected, Falk and his father left the town, and the old case and the new are bound together. Excerpts cannot be hung on a film location, so the book is shown here through the film"),
    b.PROTO("au-northern-beaches", "Northern Beaches, Sydney", "北部海滩，悉尼", *C("au-northern-beaches"),
            "the beaches north of Sydney, which inspired the fictional Pirriwee Peninsula of Liane Moriarty's Big Little Lies (2014). Moriarty has said the peninsula's physical features came from the beaches north of Sydney, where she once lived; the television series moved the story to Monterey, California",
            "启发莉安·莫里亚蒂《大小谎言》（2014）里虚构的皮里威半岛的悉尼以北海滩。莫里亚蒂说过，半岛的样子来自她曾经住过的悉尼以北那一带海滩；电视剧把故事搬到了加州的蒙特雷"),
    b.PROTO("au-jarvisfield", "Jarvisfield, Burdekin", "贾维斯菲尔德，伯德金", *C("au-jarvisfield"),
            "the Burdekin district where James Morrill, the castaway on whom David Malouf drew for Remembering Babylon (1993), came back to the settlers in 1863. After seventeen years with Aboriginal people he climbed onto the boundary fence of the new Jarvisfield sheep station and called to the stockmen not to shoot: he was a British object. The novel's settlement is unnamed; the pin is at the present locality of Jarvisfield",
            "伯德金地区。戴维·马洛夫写《忆巴比伦》（1993）时所依据的漂流者詹姆斯·莫里尔，1863 年就是在这里回到移民中间的：他和原住民一起生活了十七年，爬上新建的贾维斯菲尔德牧羊站的围栏，冲着牧工喊别开枪，说自己是“英国物件”。小说里的定居点没有名字；图钉标在今天叫贾维斯菲尔德的地方"),
    b.P("au-raymond-terrace", "Raymond Terrace", "雷蒙德台地", *C("au-raymond-terrace"), "film_location",
        adaptation=FILM("Tomorrow, When the War Began", 2010),
        scene="斯图尔特·比蒂 2010 年把约翰·马斯登的《明天，战争爆发时》拍成电影，把亨特地区雷蒙德台地的老主街国王街改成了维拉威镇的主街，片中的“维拉威电影院”等场景都搭在这里；另有部分在梅特兰、蓝山和拉斯金泰尔桥拍摄。小说里的维拉威是虚构的乡下小镇。埃莉·林顿和朋友们到丛林深处一个被当地人叫作“地狱”的偏僻山谷露营；回到家，镇上的人都不见了，被外国侵略者扣押，国家遭到了入侵。这群少年开始打游击。摘句不能挂在影视取景地上，所以这本书通过这部电影出现在这里",
        book_ids=["tomorrow-when-the-war-began"],
        scene_en="Stuart Beattie's 2010 film of John Marsden's Tomorrow, When the War Began turned King Street, the old main street of Raymond Terrace in the Hunter, into the main street of Wirrawee, with sets such as the Wirrawee Cinema; other scenes were shot at Maitland, in the Blue Mountains and at the Luskintyre bridge. In the novel Wirrawee is an invented country town. Ellie Linton and her friends go camping in a remote valley in the bush that the locals call Hell; when they come back, the townspeople have vanished, held captive by an unidentified force that has invaded the country, and the teenagers begin a guerrilla war. Excerpts cannot be hung on a film location, so the book is shown here through the film"),
    b.P("au-pemberton", "Pemberton, Western Australia", "彭伯顿（西澳）", *C("au-pemberton"), "film_location",
        adaptation=FILM("Jasper Jones", 2017),
        scene="蕾切尔·珀金斯 2017 年把克雷格·西尔维的《贾斯珀·琼斯》拍成电影，在西澳西南森林里的老伐木镇彭伯顿拍摄，用它来演小说里虚构的科里根镇（书里是个炎热的沙漠小镇）。小说写的是 1965 年的夏天：爱读书的十三岁男孩查理·巴克廷，一天夜里，贾斯珀·琼斯突然找上门来——贾斯珀因为原住民血统和不服管束的作风被全镇排斥——他需要查理帮忙，领着查理走进丛林里的一片空地，那里有一个女孩的尸体。怕自己被当成凶手，贾斯珀说服查理先藏起尸体，两人自己去查真相。摘句不能挂在影视取景地上，所以这本书通过这部电影出现在这里",
        book_ids=["jasper-jones"],
        scene_en="Rachel Perkins's 2017 film of Craig Silvey's Jasper Jones was shot in Pemberton, an old timber town in the forests of south-western Western Australia, which stood in for the novel's invented town of Corrigan (in the book a hot desert town). The novel is set in the summer of 1965: Charlie Bucktin, a bookish boy of thirteen, is visited one night by Jasper Jones, shunned by the town for his Aboriginal heritage and his wild ways, who asks for his help and leads him to a clearing in the bush where a girl lies dead. Sure that he will be blamed, Jasper persuades Charlie to hide the body while the two of them look for the truth. Excerpts cannot be hung on a film location, so the book is shown here through the film"),
    b.PROTO("au-unimelb", "University of Melbourne", "墨尔本大学", *C("au-unimelb"),
            "the Melbourne university where Don Tillman teaches genetics in Graeme Simsion's The Rosie Project (2013). The novel is set in Melbourne; readers place Don at the University of Melbourne, where Simsion took his PhD",
            "格雷姆·辛普森《罗茜计划》（2013）里唐·蒂尔曼教遗传学的那所墨尔本大学。小说的背景是墨尔本；读者通常认为唐就在墨尔本大学——辛普森本人在那里读的博士"),
    b.P("au-stanley", "Stanley, Tasmania", "斯坦利（塔斯马尼亚）", *C("au-stanley"), "film_location",
        adaptation=FILM("The Light Between Oceans", 2016),
        scene="德里克·西安弗朗斯 2016 年把 M. L. 斯特德曼的《大洋之间的灯光》拍成电影：灯塔的戏在新西兰的坎贝尔角拍，小镇的外景则在塔斯马尼亚西北的斯坦利拍，用它来演小说里虚构的海边小镇帕塔吉斯。小说里，从一战前线归来的汤姆·谢尔本到西澳外海一个虚构的小岛“雅努斯岩”当灯塔看守，娶了帕塔吉斯姑娘伊莎贝尔。一天，一条小船漂上岸，船上有一个死去的男人和一个活着的婴儿；他们决定把孩子当作自己的骨肉养大——这个决定带来了毁灭性的后果。摘句不能挂在影视取景地上，所以这本书通过这部电影出现在这里",
        book_ids=["light-between-oceans"],
        scene_en="Derek Cianfrance's 2016 film of M. L. Stedman's The Light Between Oceans shot its lighthouse scenes at Cape Campbell in New Zealand and its town scenes at Stanley, in north-west Tasmania, which stood in for the novel's invented coastal town of Partageuse. In the novel Tom Sherbourne, back from the First World War, becomes keeper of the light on Janus Rock, an invented island off the coast of Western Australia, and marries Isabel of Partageuse. One day a boat washes up carrying a dead man and a living baby; they decide to raise the child as their own, a choice with devastating consequences. Excerpts cannot be hung on a film location, so the book is shown here through the film"),
    b.PROTO("au-antarctic-division", "Australian Antarctic Division, Kingston (for Macquarie Island)", "澳大利亚南极局，金斯顿（代麦夸里岛）",
            *C("au-antarctic-division"),
            "Macquarie Island, the subantarctic island on which Charlotte McConaghy based the fictional Shearwater Island of Wild Dark Shore (2025), and which she visited on a research trip for the novel. The island lies some 1,500 km south-south-east of Tasmania, beyond the outline of Australia on this map, so the book is pinned at the Australian Antarctic Division at Kingston, near Hobart, which maintains Australia's presence in its Antarctic and subantarctic lands",
            "夏洛特·麦康纳吉《狂野黑暗的海岸》（2025）里虚构的剪水鹱岛的原型是亚南极的麦夸里岛，她为写这部小说专门去那里考察过。这座岛在塔斯马尼亚东南偏南约 1500 公里，超出了地图上澳大利亚的轮廓，所以图钉标在霍巴特附近金斯顿的澳大利亚南极局——它负责维持澳大利亚在南极和亚南极地区的存在"),
    b.ORIG("au-glebe", "Glebe, Sydney", "格利布，悉尼", *C("au-glebe"),
           "Inner-western suburb of Sydney. In Melina Marchetta's Looking for Alibrandi (1992), seventeen-year-old Josie Alibrandi lives here with her mother; the 2000 film shot the Alibrandi house on the corner of Cardigan and Bellevue Streets",
           "悉尼内西区的郊区。梅丽娜·马尔凯塔的《寻找阿利布兰迪》（1992）里，十七岁的乔茜·阿利布兰迪和母亲就住在这里；2000 年的电影把阿利布兰迪家拍在卡迪根街与贝尔维尤街的拐角"),
    b.PIL("au-norman-lindsay", "Norman Lindsay Gallery, Faulconbridge", "诺曼·林赛美术馆，福尔肯布里奇", *C("au-norman-lindsay"),
          "Norman Lindsay's home at Faulconbridge in the Blue Mountains, which he called Springwood, now the Norman Lindsay Gallery of the National Trust. He wrote and illustrated The Magic Pudding (1918) here; visitors can step into the painting studio where he made it",
          "诺曼·林赛在蓝山福尔肯布里奇的家，他称之为“斯普林伍德”，如今是国民信托的诺曼·林赛美术馆。他在这里写作并绘制了《魔法布丁》（1918）；参观者可以走进他当年创作这本书的画室",
          ["magic-pudding"]),
    b.PROTO("au-burketown", "Burketown", "伯克敦", *C("au-burketown"),
            "the small town near the Gulf of Carpentaria in north-western Queensland that Nevil Shute, who visited the Gulf country in 1948, named as the prototype of Willstown in A Town Like Alice (1950)",
            "昆士兰西北、卡奔塔利亚湾附近的小镇。内维尔·舒特 1948 年到过海湾地区，他说《像爱丽丝那样的小镇》（1950）里威尔斯敦的原型就是伯克敦"),
]
lines = [
    b.S("au-kg-1", "true-history-kelly-gang", "au-glenrowan", "The last stand", "最后一战",
        "Ned Kelly tells his own story, in rough, unpunctuated parcels of writing addressed to the daughter he will never see: the third of eight children of poor Irish parents, his father a transported convict; a boyhood of poverty and police harassment in north-eastern Victoria; the killings at Stringybark Creek, the raids on Euroa and Jerilderie; and, at last, the gang's stand in armour at Glenrowan in June 1880. There Thomas Curnow, a schoolmaster who has won Ned's trust, slips away to warn the police. The novel opens with an account of that siege, and presents Ned's pages as papers saved from its ruins.",
        "内德·凯利亲口讲自己的故事，写在一包包没有标点、文法粗糙的稿纸上，写给他永远见不到的女儿：他是贫穷的爱尔兰移民八个孩子里的老三，父亲是流放来的罪犯；在维多利亚州东北部，童年里只有贫困和警察的骚扰；后来是斯特林吉巴克溪的枪杀、对尤罗厄和杰里尔德里的劫掠；最后，是 1880 年 6 月凯利帮在格伦罗万披甲死守。在那里，取得内德信任的教师托马斯·柯诺悄悄溜走，给警察报了信。小说以这场围攻的记述开篇，把内德的手稿说成是从那片废墟里抢救出来的文件。",
        ["Glenrowan"], ["格伦罗万"],
        "https://www.encyclopedia.com/arts/educational-magazines/true-history-kelly-gang; https://www.ebsco.com/research-starters/literature-and-writing/true-history-kelly-gang-peter-carey; https://slv.vic.gov.au/sites/default/files/Creative-Acts_labels_PETER-CAREY.pdf; https://readingaustralia.com.au/lesson/true-history-of-the-kelly-gang/; https://www.inkl.com/news/a-thoroughly-white-novel-of-national-mythmaking-peter-carey-s-true-history-of-the-kelly-gang-at-25"),
    b.S("au-bsu-1", "boy-swallows-universe", "au-darra", "The novel as a whole", "全书",
        "Brisbane in the 1980s. Twelve-year-old Eli Bell lives in the outer suburb of Darra with his mute older brother August and their mother Frankie, a former heroin addict, and her boyfriend Lyle. Their babysitter is Arthur 'Slim' Halliday, a real convicted criminal famous for escaping from Boggo Road Gaol. Eli dreams of becoming a journalist, but life keeps throwing obstacles in his way, above all Tytus Broz, Brisbane's legendary drug dealer, and his last trial comes at the clock tower of Brisbane City Hall. Dalton and his mother agreed the novel was half fact and half fantasy; like Frankie, his mother served time in jail.",
        "20 世纪 80 年代的布里斯班。十二岁的伊莱·贝尔住在外围郊区达拉，和他不说话的哥哥奥古斯特、曾经吸海洛因的母亲弗兰基，还有母亲的男友莱尔在一起。帮他们看孩子的是阿瑟·“瘦子”·哈利迪——一个真实存在的罪犯，以从博戈路监狱越狱出名。伊莱梦想当记者，生活却不断给他设障碍，最大的一个是布里斯班的传奇毒枭泰特斯·布罗兹；他最后的考验发生在布里斯班市政厅的钟楼上。多尔顿和母亲都认为这部小说一半是事实、一半是幻想；和弗兰基一样，他的母亲也坐过牢。",
        ["Darra"], ["达拉"],
        "https://www.weekendnotes.com/boy-swallows-universe-book-review/; https://www.slq.qld.gov.au/blog/brisbane-boy-swallows-television-universe; https://www.pressreader.com/australia/the-saturday-paper/20210911/282011855479723; https://blackwells.co.uk/bookshop/product/Boy-Swallows-Universe-by-Trent-Dalton/9780062898104; https://www.brisbane.qld.gov.au/things-to-see-and-do/things-to-do-blog/discover-brisbane-through-boy-swallows-universe; https://www.thenewdaily.com.au/travel/experiences/2024/01/19/boy-swallows-universe-tourist-magnet"),
    b.S("au-bll-1", "big-little-lies", "au-northern-beaches", "The novel as a whole", "全书",
        "On the Pirriwee Peninsula, a beachside place on Sydney's Northern Beaches, Jane, a young single mother, takes her son Ziggy to his first day at Pirriwee Public School and is befriended by two other mothers, the fierce, funny Madeline and the beautiful Celeste, whose wealthy husband Perry beats her behind closed doors. When Ziggy is accused of bullying a classmate, the parents take sides. The story is told in the months before a school trivia night that ends with someone dead, and in police interviews with the parents afterwards. (Pirriwee is invented; Moriarty took its look from the beaches north of Sydney.)",
        "在悉尼北部海滩一个叫皮里威半岛的海滨地方，年轻的单身母亲简送儿子齐吉去皮里威公立学校上学的第一天，结识了另外两位母亲：泼辣风趣的玛德琳，和美丽的瑟莱斯特——她有钱的丈夫佩里关起门来对她拳脚相加。齐吉被指控欺负同学，家长们分成了两派。故事讲的是学校知识竞赛之夜前的那几个月——那一夜以一个人的死亡收场——穿插着事后警察对家长们的问话。（皮里威是虚构的；莫里亚蒂说它的样子取自悉尼以北的海滩。）",
        ["Northern Beaches"], ["北部海滩"],
        "https://en.wikipedia.org/wiki/Big_Little_Lies_(novel); https://itsoutnow.co/blog/where-is-pirriwee; https://thebooktrail.com/?p=6690; https://www.atlasofwonders.com/2017/02/big-little-lies-filming-locations.html"),
    b.S("au-rb-1", "remembering-babylon", "au-jarvisfield", "The figure on the fence", "围栏上的人",
        "One day in the middle of the nineteenth century, when settlement in Queensland had advanced little more than halfway up the coast, three children playing at the edge of a paddock see something extraordinary balanced on a fence: Gemmy Fairley, an English boy cast ashore years before and raised by Aboriginal people, who cries out that he is a British object. Taken in by the McIvor family in a small, wary community of Scottish settlers, he stands between two worlds, and the settlers' fear of what he may know of the country and of the people who raised him turns into suspicion and hostility. (The settlement is unnamed; Malouf drew on James Morrill, who came back to the settlers at Jarvisfield in 1863.)",
        "十九世纪中叶的某一天，昆士兰的移民才往北推进到海岸的一半，三个在牧场边上玩耍的孩子看见围栏上蹲着一个不可思议的身影：吉米·费尔利，一个多年前被冲上岸、由原住民养大的英国男孩，他大喊自己是“英国物件”。他被麦基弗一家收留，住进一个小小的、处处提防的苏格兰移民社区，夹在两个世界之间；移民们害怕他知道这片土地和养大他的那些人的什么事，这份恐惧渐渐变成了猜疑和敌意。（定居点没有名字；马洛夫取材于 1863 年在贾维斯菲尔德回到移民中间的詹姆斯·莫里尔。）",
        ["Jarvisfield"], ["贾维斯菲尔德"],
        "https://australianbookreview.com.au/abr-online/archive/1993/518-may-1993-no-150/7142-catherine-kenneally-reviews-remembering-babylon-by-david-malouf; https://www.litcharts.com/lit/remembering-babylon/summary; https://www.themodernnovel.org/?p=776; https://www.librarycat.org/lib/Themis-Athena/item/167277229; https://en.wikipedia.org/wiki/Remembering_Babylon; https://en.wikipedia.org/wiki/James_Morrill_(castaway)"),
    b.S("au-rp-1", "the-rosie-project", "au-unimelb", "The Wife Project", "妻子计划",
        "Don Tillman, a brilliant and socially awkward professor of genetics in Melbourne who runs his week on a strict timetable, decides it is time to find a wife and devises the Wife Project: a sixteen-page questionnaire to screen out drinkers, smokers and late arrivals. His friend Gene, a psychology professor, sends him Rosie, a PhD student who works as a barmaid and fails every test. She wants help to find her biological father, and Don, secretly running DNA tests in the university laboratory, takes on the Father Project instead, which leads them overseas and back. (The novel is set in Melbourne; readers place Don at the University of Melbourne.)",
        "唐·蒂尔曼是墨尔本的遗传学教授，才华横溢却不善交际，一周的生活全按严格的时间表过。他决定是时候找个妻子了，于是设计出“妻子计划”：一份十六页的问卷，用来筛掉喝酒的、抽烟的和爱迟到的。他的朋友、心理学教授吉恩给他介绍了罗茜——一个在酒吧打工的博士生，问卷上的每一项她都不合格。她想找到自己的亲生父亲；唐偷偷在大学实验室里做 DNA 检测，接下了“父亲计划”，两人还为此出了一趟国。（小说的背景是墨尔本；读者通常把唐放在墨尔本大学。）",
        ["University of Melbourne"], ["墨尔本大学"],
        "https://en.wikipedia.org/wiki/The_Rosie_Project; https://www.microsoft.com/en-us/research/?p=190021; https://www.yorku.ca/edu/campuslit/the-rosie-project; https://www.penguin.co.uk/books/193470/the-rosie-project-by-simsion-graeme/9780718178550; https://www.goodreads.com/book/show/25353087; https://www.stylist.co.uk/books/live-web-chat-graeme-simsion/126193"),
    b.S("au-wds-1", "wild-dark-shore", "au-antarctic-division", "The novel as a whole", "全书",
        "Dominic Salt and his three children are the last caretakers of Shearwater, a tiny island not far from Antarctica, once full of researchers and home to the world's largest seed bank. During the worst storm the island has ever seen, a woman, Rowan, washes up on the shore. Rowan is not telling the whole truth about why she set out for Shearwater, and when she finds sabotaged radios and a freshly dug grave, she realises that Dominic is keeping dark secrets of his own. The last ship is weeks away. (Shearwater is invented; McConaghy based it on Macquarie Island, which lies beyond this map; the pin is at the Australian Antarctic Division near Hobart.)",
        "多米尼克·索尔特和他的三个孩子，是剪水鹱岛最后的看守人。这座离南极不远的小岛，从前满是研究人员，岛上还有世界上最大的种子库。在小岛经历过的最猛烈的一场风暴里，一个叫罗恩的女人被冲上了岸。罗恩没有说出自己来剪水鹱岛的全部真相；而当她发现被破坏的无线电和一座新挖的坟，她意识到多米尼克也藏着自己的秘密。最后一班船还要好几个星期才来。（剪水鹱岛是虚构的；麦康纳吉以麦夸里岛为原型，那座岛在这张地图之外，图钉标在霍巴特附近的澳大利亚南极局。）",
        ["Macquarie Island"], ["麦夸里岛"],
        "https://www.qbd.com.au/product/9781761620003.htm; https://en.wikivoyage.org/wiki/Tasmania; https://en.wikipedia.org/wiki/Australian_Antarctic_Division; https://www.kirkusreviews.com/news-and-features/articles/best-fiction-of-2025-charlotte-mcconaghy; https://www.booksandpublishing.com.au/articles/2025/01/21/263706/wild-dark-shore-%E2%80%A6cconaghy-penguin/; https://lsj.com.au/?p=27423"),
    b.S("au-la-1", "looking-for-alibrandi", "au-glebe", "Josie's last year at school", "乔茜的毕业年",
        "Josephine 'Josie' Alibrandi, an outspoken, ambitious Italian-Australian of seventeen, lives in Glebe with her mother Christina, who had her out of wedlock at seventeen and was cast off by her own father. A scholarship girl at St Martha's, an exclusive Catholic girls' school, Josie feels like an outsider, and in her final year of school everything changes at once: her father, Michael Andretti, comes back to Sydney, and she falls for Jacob Coote, a boy from the local state school. The novel follows her through family, identity and growing up in inner-western Sydney.",
        "十七岁的意大利裔澳大利亚姑娘乔瑟芬·“乔茜”·阿利布兰迪心直口快、志向远大，和母亲克里斯蒂娜住在格利布——母亲十七岁时未婚生下她，被自己的父亲赶出了家门。乔茜拿着奖学金在一所名贵的天主教女校圣玛莎读书，觉得自己格格不入；毕业那一年，一切同时发生了变化：她的父亲迈克尔·安德烈蒂回到悉尼，她也爱上了公立学校的男孩雅各布·库特。小说陪她穿过悉尼内西区的家庭、身份与成长。",
        ["Glebe"], ["格利布"],
        "https://en.wikipedia.org/wiki/Looking_for_Alibrandi_(novel); https://en.wikipedia.org/wiki/Looking_for_Alibrandi_(film); https://www.austlit.edu.au/austlit/page/6644159; https://glebesociety.org.au/who-filmed-in-your-street/"),
    b.S("au-mp-1", "magic-pudding", "au-norman-lindsay", "The Noble Society of Pudding Owners", "布丁主人高尚协会",
        "The gentlemanly koala Bunyip Bluegum sets out to see the world and falls in with Bill Barnacle, a sailor, and Sam Sawnoff, a penguin, the owners of Albert, a magic pudding: gruff, gravy-voiced and rude, he turns from steak-and-kidney to jam roll or apple dumpling in a moment and, however much is eaten, never runs out. Together the three, as the Noble Society of Pudding Owners, defend Albert against pudding thieves. Lindsay wrote it to win an argument with his friend Bertram Stevens, who held that children would rather read about fairies than food. (The story's road is imaginary; Lindsay wrote and drew it at his home at Faulconbridge.)",
        "温文有礼的考拉本伊普·布鲁加姆出门见世面，结识了水手比尔·巴纳克尔和企鹅山姆·索诺夫——他们是阿尔伯特的主人。阿尔伯特是一只魔法布丁，脾气暴躁，嗓音像肉汁一样浑厚，说话无礼，转眼就能从牛排腰子布丁变成果酱卷或苹果布丁，不管吃掉多少都吃不完。三位以“布丁主人高尚协会”的名义，一起保护阿尔伯特不被布丁贼偷走。林赛写这本书，是为了跟朋友伯特伦·史蒂文斯争个输赢——史蒂文斯认为孩子们更爱读仙女，而不是吃的。（故事里的路是虚构的；林赛在福尔肯布里奇的家中写作并画下了它。）",
        ["Faulconbridge"], ["福尔肯布里奇"],
        "https://www.sl.nsw.gov.au/node/170076; https://flic.kr/photos/130281204@N06/54990449572 (National Trust text); https://en.wikipedia.org/wiki/Norman_Lindsay; https://collections.museumsvictoria.com.au/articles/3017; https://www.nsw.gov.au/visiting-and-exploring-nsw/locations-and-attractions/norman-lindsay-gallery; https://canadabayheritage.asn.au/the-magic-pudding/"),
    b.S("au-tla-1", "a-town-like-alice", "au-burketown", "Willstown", "威尔斯敦",
        "In Malaya, when the Japanese invade, Jean Paget, a young Englishwoman, is taken prisoner with a group of women and children whom the Japanese march from village to village. She meets Joe Harman, an Australian sergeant and fellow prisoner, who steals food and medicine for them; when he takes the blame for stealing the Japanese commander's chickens, he is beaten and crucified, and the women march on believing him dead. After the war an inheritance lets Jean go back to build a well for the village that sheltered them, and there she learns that Joe survived. She follows him to Australia, first to Alice Springs and then to Willstown, a run-down town in the Gulf country, which she sets out to make into 'a town like Alice'. (Willstown is invented; Shute named Burketown as its prototype.)",
        "日军入侵马来亚时，年轻的英国女子琼·佩吉特和一群妇女儿童一起被俘，日本人押着她们从一个村子走到另一个村子。她认识了同为俘虏的澳大利亚中士乔·哈曼，他替她们偷来食物和药品；后来他为偷了日本指挥官的鸡一事揽下罪责，被毒打后钉上十字架，妇女们以为他死了，继续被押着往前走。战后，一笔遗产让琼得以回去，为当年收留她们的村子打一口井，也正是在那里，她得知乔还活着。她追到澳大利亚，先到爱丽丝泉，再到海湾地区破败的威尔斯敦，决心把它建成“像爱丽丝那样的小镇”。（威尔斯敦是虚构的；舒特说它的原型是伯克敦。）",
        ["Burketown"], ["伯克敦"],
        "https://en.wikipedia.org/wiki/A_Town_Like_Alice; https://insidestory.org.au/?p=68059; https://www.nevilshute.org/atlanotes.php; https://www.examiner.com.au/story/6706502/alice-through-the-looking-glass/"),
]
check(books, places, lines)
if __name__ == "__main__":
    run(books, places, lines, "add_au3.py")
