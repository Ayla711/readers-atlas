"""11-28: Canada, rule-v2 re-check (tools/selection/ca.md), batch 2: Quebec.
- Lullabies for Little Criminals (Heather O'Neill): Saint-Laurent Boulevard at Saint Catherine Street, the old Red Light, the
  Montreal district where Baby and her father Jules drift from room to room;
- The Tin Flute / Bonheur d'occasion (Gabrielle Roy): Saint-Henri, the working-class Montreal district of the Lacasse family;
- Still Life (Louise Penny): Three Pines is invented; Knowlton, the Eastern Townships village where Penny lives, is the place most
  often named as its inspiration (Penny says Three Pines is not a copy of it); a prototype place, so stated;
- Solomon Gursky Was Here (Mordecai Richler): the existing Montreal place (ca-montreal), whose note gains a sentence on the Gursky
  brothers' mansions on the slope of Mount Royal.
All four are in copyright: scene notes, no quotation. Coordinates: coords/add_ca_v2_1128_2.json (en.wikipedia).
Usage: python3 -I tools/content/batches/add_ca_v2_1128_2.py <app_dir> tools/content/batches/coords/add_ca_v2_1128_2.json"""
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
    BK("lullabies-for-little-criminals", "Lullabies for Little Criminals", "给小罪犯的摇篮曲", "Heather O'Neill", "希瑟·奥尼尔", "2006",
       ["Lullabies for Little Criminals", "Baby", "Jules", "O'Neill"]),
    dict(id="the-tin-flute", title="The Tin Flute", title_zh="锡笛", title_orig="Bonheur d'occasion", author="Gabrielle Roy", author_zh="加布丽埃勒·罗伊",
         year="1945", orig_lang="fr", public_domain=False, source_url=None, author_orig="Gabrielle Roy",
         aliases=["The Tin Flute", "Bonheur d'occasion", "Florentine Lacasse", "Saint-Henri"]),
    BK("still-life-penny", "Still Life", "静物", "Louise Penny", "路易丝·彭妮", "2005",
       ["Still Life", "Three Pines", "Armand Gamache", "Gamache", "Jane Neal"]),
    BK("solomon-gursky", "Solomon Gursky Was Here", "所罗门·古尔斯基到此一游", "Mordecai Richler", "莫迪凯·里奇勒", "1989",
       ["Solomon Gursky Was Here", "Moses Berger", "Ephraim Gursky", "Gursky"]),
]

places = [
    b.ORIG("ca-saint-laurent", "Saint-Laurent Boulevard and the Red Light, Montreal", "蒙特利尔 · 圣洛朗大道与红灯区", *C("ca-saint-laurent"),
        "The Main, the long street that divides Montreal into east and west, and its crossing with Saint Catherine Street, the heart of the old Red Light district of cabarets and brothels. Heather O'Neill, who grew up in Montreal, set her Lullabies for Little Criminals (2006) in this district: twelve-year-old Baby and her father Jules drift between cheap rooms around it",
        "“大街”是把蒙特利尔分成东西两半的那条长街，它和圣凯瑟琳街的路口，就是老红灯区的中心，从前满是夜总会和妓院。在蒙特利尔长大的希瑟·奥尼尔把《给小罪犯的摇篮曲》（2006）放在这一带：十二岁的贝比和父亲朱尔斯在附近的廉价房间之间搬来搬去"),
    b.ORIG("ca-saint-henri", "Saint-Henri, Montreal", "蒙特利尔 · 圣亨利区", *C("ca-saint-henri"),
        "Working-class French-Canadian district of south-west Montreal, bounded on the south by the Lachine Canal. Gabrielle Roy set Bonheur d'occasion (1945; The Tin Flute) in its streets in the spring of 1940; the stark portrait of poverty here won the Prix Femina and is often said to have helped prepare Quebec's Quiet Revolution",
        "蒙特利尔西南部讲法语的工人街区，南边以拉欣运河为界。加布丽埃勒·罗伊把《锡笛》（法文名《二手的幸福》，1945）放在 1940 年春天的这些街道上；书中对贫穷毫不粉饰的描写赢得了费米娜奖，常被认为为魁北克的“寂静革命”做了铺垫"),
    b.PROTO("ca-knowlton", "Knowlton, Quebec", "魁北克 · 诺尔顿", *C("ca-knowlton"),
        "Three Pines, the invented village of Louise Penny's Chief Inspector Gamache mysteries, set just north of the Vermont border. Penny lives in Knowlton, on Brome Lake in the Eastern Townships, and it is the village most often named as Three Pines' model, with Brome Lake Books as the model for the village bookshop; Penny herself says Three Pines is not a copy of Knowlton but grew out of several Townships villages",
        "路易丝·彭妮“加马什探长”系列推理小说里虚构的三松村，就在佛蒙特边界以北。彭妮住在东镇布罗姆湖畔的诺尔顿，这里最常被说成三松村的原型，村里书店的原型是布罗姆湖书店；不过彭妮本人说，三松村并不是照着诺尔顿写的，而是从东镇好几个村子里长出来的"),
]

lines = [
    b.S("lullabies-s1", "lullabies-for-little-criminals", "ca-saint-laurent", "Throughout", "全书",
        "Baby is twelve. Her mother died soon after she was born, and her father Jules, who was still a teenager then, is slipping deeper into heroin; the two move from one cheap room to the next around Montreal's red-light district, among junkies, pimps and abused children, and Jules leaves her alone for weeks at a time. While he is in hospital with tuberculosis she is put into a foster home; back with him, she runs away from his rages and falls in with a pimp, Alphonse, who draws her into prostitution and heroin, and she spends a month in juvenile detention. Baby tells it all with a child's eye. The novel won Canada Reads in 2007.",
        "贝比十二岁。母亲在她出生后不久就死了，父亲朱尔斯那时自己还是个少年，如今海洛因越吸越深；父女俩在蒙特利尔红灯区一带从一个廉价房间搬到另一个，身边是瘾君子、皮条客和受虐的孩子，朱尔斯常常一走就把她丢下好几个星期。他因肺结核住院时，她被送进寄养家庭；回到他身边后，她躲开他的暴脾气跑了出去，落到皮条客阿方斯手里，被他拖进卖身和海洛因，还在少年拘留所里待了一个月。这一切都是透过贝比孩子的眼睛讲出来的。这本书获得了 2007 年“加拿大共读”冠军。",
        ["Montreal"], ["蒙特利尔"],
        "https://en.wikipedia.org/wiki/Lullabies_for_Little_Criminals; https://mtlreviewofbooks.ca/reviews/lullabies-for-little-criminals/; https://kirkusreviews.com/book-reviews/heather-oneill/lullabies-for-little-criminals/"),
    b.S("tinflute-s1", "the-tin-flute", "ca-saint-henri", "Throughout", "全书",
        "Montreal, February to May 1940: the war has begun but Saint-Henri is still sunk in the Depression. Florentine Lacasse, nineteen, a waitress at the Five and Ten, keeps her large family afloat; her mother Rose-Anna looks after the children, and her father Azarius drifts from one failed job to the next. Florentine dreams of a better life and falls for Jean Lévesque, an ambitious, well-off young machinist; he tires of her and passes her on to his friend Emmanuel Létourneau, a soldier on leave, who falls in love with her. Jean forces himself on Florentine and leaves her pregnant; she keeps it secret and marries Emmanuel, who has promised to look after her. The book won the Prix Femina in 1947.",
        "蒙特利尔，1940 年 2 月到 5 月：战争已经开始，圣亨利区却还陷在大萧条里。十九岁的弗洛朗蒂娜·拉卡斯在“五分一毛”店当女招待，靠她撑着一大家子；母亲罗丝-安娜照看孩子们，父亲阿扎里于斯一份差事接一份地丢。弗洛朗蒂娜盼着过上更好的日子，爱上了野心勃勃、手头宽裕的年轻机修工让·莱韦克；他厌了她，把她推给朋友、休假的士兵埃马纽埃尔·莱图尔诺，埃马纽埃尔爱上了她。让强行占有了弗洛朗蒂娜，让她怀了孕；她瞒住此事，嫁给了答应照顾她的埃马纽埃尔。这本书 1947 年获得费米娜奖。",
        ["Saint-Henri", "Montreal"], ["圣亨利", "蒙特利尔"],
        "https://en.wikipedia.org/wiki/The_Tin_Flute"),
    b.S("stilllife-s1", "still-life-penny", "ca-knowlton", "Throughout", "全书",
        "In the early morning mist of Thanksgiving Sunday, Jane Neal, seventy-six, a retired schoolteacher, is found dead on a deer path in the woods outside Three Pines, a village south of Montreal so small it has no police of its own, killed by an arrow through the heart. Everyone takes it for a hunting accident. Chief Inspector Armand Gamache of the Sûreté du Québec, sent with his team from Montreal, is not so sure; Jane had only just agreed to show one of her paintings, Fair Day, in an exhibition for the first time, and her friend and neighbour, the painter Clara Morrow, notices the slight difference between Fair Day and Jane's murals that holds the key. The book introduced Gamache and Three Pines.",
        "感恩节星期天清晨的薄雾里，七十六岁的退休教师简·尼尔被发现死在三松村外树林里的一条鹿径上，一支箭穿心而过；三松村在蒙特利尔以南，小到连自己的警察都没有。人人都以为是狩猎意外。魁北克省警的首席探长阿尔芒·加马什带着手下从蒙特利尔赶来，却不这么看：简刚刚第一次答应把自己的一幅画《集市日》拿去参展，她的朋友和邻居、画家克拉拉·莫罗注意到《集市日》和简的壁画之间一处细小的差别，那正是破案的钥匙。加马什和三松村都是从这本书开始的。",
        ["Three Pines"], ["三松村"],
        "https://kirkusreviews.com/book-reviews/louise-penny/still-life-3; https://www.powells.com/biblio/74-9780312948559-0; https://www.supersummary.com/still-life/summary; https://www.shelf-awareness.com/theshelf/2006-08-16/mandahla_i_still_life_i_reviewed.html; https://thecanadianencyclopedia.ca/en/article/louise-penny"),
    b.S("gursky-s1", "solomon-gursky", "ca-montreal", "Throughout", "全书",
        "Moses Berger, a brilliant Montreal scholar ruined by drink and son of the failed poet L. B. Berger, has been obsessed since boyhood with the Gurskys: the three brothers Bernard, Solomon and Morrie, bootleggers turned whisky barons, whose McTavish distillery empire many readers take for the Bronfmans' Seagram. Solomon, the boldest, vanished in a plane crash; Moses suspects he is still alive. Tracing the family back, Moses finds the patriarch Ephraim, a small-time London criminal who talked his way onto Franklin's doomed 1845 Arctic expedition, survived it, and set himself up as a messiah among the Inuit, some of whom still bear the name Gor-ski. The story ranges from the London underworld through the Arctic and the Prohibition prairies to the Eastern Townships and the brothers' neighbouring mansions on the slope of Mount Royal.",
        "摩西·伯格是蒙特利尔一位被酒毁掉的才子，失意诗人 L. B. 伯格的儿子，从小就迷上了古尔斯基家族：伯纳德、所罗门、莫里三兄弟，先是私酒贩子，后来成了威士忌大亨，许多读者认为他们的麦克塔维什酒业帝国写的就是布朗夫曼家族的施格兰。最大胆的所罗门死于一场空难，摩西却怀疑他还活着。顺着家族往上追，摩西找到了始祖以法莲：伦敦的一个小毛贼，混上了富兰克林 1845 年那支注定覆灭的北极探险队，居然活了下来，在因纽特人中间做起了弥赛亚，至今还有因纽特人姓“戈尔斯基”。故事从伦敦的黑社会，经过北极、禁酒令时期的草原，一直写到东镇，写到三兄弟在皇家山坡上比邻而建的豪宅。",
        ["Montreal", "Mount Royal"], ["蒙特利尔", "皇家山"],
        "https://en.wikipedia.org/wiki/Solomon_Gursky_Was_Here; https://www.kirkusreviews.com/book-reviews/a/mordecai-richler-3/solomon-gursky-was-here; https://publishersweekly.com/9780394539959; https://www.ebsco.com/research-starters/literature-and-writing/solomon-gursky-was-here-mordecai-richler; https://ojs.library.ubc.ca/index.php/canlit/article/view/192830/189343; https://banq.overdrive.com/media/1762254; https://fiftybooksproject.blogspot.com/2020/11/solomon-gursky-was-here-by-mordecai.html"),
]

MTL_EN = "Mordecai Richler's Barney Panofsky drinks and quarrels his way through the same city"
MTL_ZH = "里奇勒笔下的巴尼·帕诺夫斯基也在这座城里喝酒、吵架、过完一生"
def montreal_note(path):
    s = open(path, encoding="utf-8").read()
    assert s.count(MTL_EN) == 1 and s.count(MTL_ZH) == 1
    s = s.replace(MTL_EN, MTL_EN + ", and in his Solomon Gursky Was Here the three Gursky brothers, bootleggers turned whisky barons, build neighbouring fieldstone mansions on the slope of Mount Royal")
    s = s.replace(MTL_ZH, MTL_ZH + "；他的《所罗门·古尔斯基到此一游》里，从私酒贩子变成威士忌大亨的古尔斯基三兄弟，在皇家山坡上比邻盖起了石砌豪宅")
    open(path + ".new", "w", encoding="utf-8").write(s); os.replace(path + ".new", path)

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "books.js"))))
all_places = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "places.js"))))
all_lines = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "lines.js"))))
assert not {x["id"] for x in books} & all_books
assert {p["id"] for p in places} == set(CO) and not set(CO) & all_places and "ca-montreal" in all_places
assert not {l["id"] for l in lines} & all_lines
if __name__ == "__main__":
    note = "11-28 Canada rule-v2 re-check, batch 2: Quebec (add_ca_v2_1128_2.py)"
    append(b.data("books.js"), books, note)
    append(b.data("places.js"), places, note)
    append(b.data("lines.js"), lines, note)
    montreal_note(b.data("places.js"))
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
