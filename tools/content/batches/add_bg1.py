"""11-25: Bulgaria, the 6 books that selection rule v2 adds (tools/selection/bg.md). Bulgaria opens with this batch.
Two quotations are cut from Bulgarian Wikisource (Vazov and Konstantinov are out of copyright; translations are our own
drafts); the other four are scene notes in our own words. Places, with the reason for each:
- Under the Yoke: Sopot. Byala Cherkva ("White Church", Ottoman Akche Klise) is the name under which Sopot was recorded
  until 1878 and under which it appears in the novel (Bulgarian Wikipedia, "Сопот"; English Wikipedia, "Under the Yoke").
  The quotation is from "The Performance", one of the chapters the school curriculum names.
- Time of Parting: Chepino, now a quarter of Velingrad. The valley of Elindenya and its three villages are invented;
  Chepino, burnt in the novel, is real. Coordinates from Wikidata (the Bulgarian Wikipedia article gives none).
- Tobacco: Plovdiv. Dimov gathered his ideas in Plovdiv's tobacco warehouses; the Nikotiana warehouse is modelled on the
  Orient Tabacco warehouse at 8 Odrin Street (bulgarianhistory.org). City-level pin.
- Bay Ganyo: Kazanlak, the town of Ganyu Somov, the rose-oil trader who is one of Bay Ganyo's two models (Bulgarian
  Wikipedia, "Бай Ганьо"). No Bulgarian town is named in the travel stories; the quotation is the rose-oil scene of
  "Bay Ganyo Travels" (school curriculum, grade 7), so its highlight is the rose oil, not a place name.
- Ballad for Georg Henig: Sofia (city-level pin); the house on Iskar Street is not pinned.
- Time Shelter: the National Palace of Culture, Sofia, where Demby's troupe rehearses (excerpt published by Literary Hub).
Usage: python3 -I tools/content/batches/add_bg1.py <app_dir> tools/content/batches/coords/add_bg1.json <wikisource_dir>"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-25"
b.init(APP, "", "bg", DATE)
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]
def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, aliases, pd=False, src=None):
    return dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
                orig_lang="bg", public_domain=pd, source_url=src, author_orig=author_orig, aliases=aliases)
def Q(id, book, place, loc, loc_zh, title, orig, hl_orig, en, hl_en, zh, hl_zh):
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls:
            assert h in text, (id, h)
    assert "[" not in orig and "\xa0" not in orig and "  " not in orig, (id, "page mark or odd space")
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh,
                text_orig=orig, highlight_orig=hl_orig, text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh,
                translation="own", status="draft", checked=f"Bulgarian Wikisource, {title}, {DATE}")
WS = "https://bg.wikisource.org/wiki/"

books = [
    BK("under-the-yoke", "Under the Yoke", "轭下", "Под игото", "Ivan Vazov", "伊万·伐佐夫", "Иван Вазов", "1894",
       ["Pod igoto", "Под игото", "Byala Cherkva"], pd=True, src=WS + "Под_игото"),
    BK("time-of-parting", "Time of Parting", "分离的时刻", "Време разделно", "Anton Donchev", "安东·东切夫", "Антон Дончев", "1964",
       ["Vreme razdelno", "Време разделно", "Time of Violence"]),
    BK("tobacco-dimov", "Tobacco", "烟草", "Тютюн", "Dimitar Dimov", "迪米塔尔·迪莫夫", "Димитър Димов", "1951",
       ["Tyutyun", "Тютюн", "Nikotiana"]),
    BK("bay-ganyo", "Bay Ganyo", "巴伊·甘纽", "Бай Ганьо", "Aleko Konstantinov", "阿列科·康斯坦丁诺夫", "Алеко Константинов", "1895",
       ["Bai Ganyo", "Бай Ганьо"], pd=True, src=WS + "Бай_Ганьо"),
    BK("ballad-georg-henig", "Ballad for Georg Henig", "格奥尔格·赫尼希谣曲", "Балада за Георг Хених", "Viktor Paskov", "维克托·帕斯科夫",
       "Виктор Пасков", "1987", ["Balada za Georg Henih", "Балада за Георг Хених"]),
    BK("time-shelter", "Time Shelter", "时间庇护所", "Времеубежище", "Georgi Gospodinov", "格奥尔基·戈斯波季诺夫", "Георги Господинов",
       "2020", ["Vremeubezhishte", "Времеубежище"]),
]

places = [
    b.PROTO("bg-sopot", "Sopot", "索波特", *C("bg-sopot"),
        "Vazov's home town is the Byala Cherkva of Under the Yoke: Byala Cherkva, 'White Church' (Ottoman Akche Klise), is the name under which Sopot was recorded until 1878. Grandpa Stoyan's watermill from the novel still works on the north-western edge of the town, and the house where Vazov was born is a museum",
        "伐佐夫的家乡就是《轭下》里的白教堂镇：“白教堂”（奥斯曼语叫阿克切克利塞）是索波特在 1878 年以前的登记名。小说里斯托扬爷爷的水磨坊至今还在镇子西北边转着，伐佐夫出生的房子是一座博物馆"),
    b.PROTO("bg-chepino", "Chepino, Velingrad", "切皮诺（韦林格勒）", *C("bg-chepino"),
        "Chepino is now a quarter of Velingrad in the western Rhodopes. In Time of Parting the janissary Karaibrahim rides into the Rhodope valley of Elindenya in the spring of 1668 to convert its Orthodox villagers to Islam. The valley and its three villages are invented; Chepino, which is burnt in the novel, is real",
        "切皮诺今天是西罗多彼山区韦林格勒的一个区。《分离的时刻》里，1668 年春天，近卫军骑兵卡拉易卜拉欣来到罗多彼山中的埃林德尼亚谷，要逼信东正教的村民改信伊斯兰教。山谷和谷里的三个村子是虚构的；小说里被烧毁的切皮诺村是真实的"),
    b.PROTO("bg-plovdiv", "Plovdiv", "普罗夫迪夫", *C("bg-plovdiv"),
        "Dimov gathered much of the material for Tobacco in Plovdiv, talking with workers, managers and merchants in its tobacco warehouses. The warehouse of the novel's Nikotiana company is modelled on that of Orient Tabacco at 8 Odrin Street, Plovdiv, which stood for nearly a century",
        "迪莫夫写《烟草》的许多素材来自普罗夫迪夫，他在城里的烟草仓库跟工人、经理和商人交谈。小说里尼科蒂亚纳公司的仓库，原型是普罗夫迪夫奥德林街 8 号东方烟草公司的仓库，那座楼存在了将近一百年"),
    b.PROTO("bg-kazanlak", "Kazanlak", "卡赞勒克", *C("bg-kazanlak"),
        "Bay Ganyo travels round Europe with his rose oil. According to the Bulgarian Wikipedia he has two main real-life models: Ganyu Somov, a small rose-oil trader from Kazanlak whom Aleko Konstantinov met at the World's Fair in Chicago, where Somov tried to sell fake rose oil (To Chicago and Back), and the prosecutor Ganyu Cholakov",
        "巴伊·甘纽带着玫瑰油游遍欧洲。据保加利亚文维基百科，他主要有两个原型：一个是卡赞勒克的小玫瑰油商甘尤·索莫夫，阿列科·康斯坦丁诺夫在芝加哥世界博览会上见过他，他在那里摆摊卖假玫瑰油（见《去芝加哥又回来》）；另一个是检察官甘尤·乔拉科夫"),
    b.ORIG("bg-sofia", "Sofia", "索非亚", *C("bg-sofia"),
        "Ballad for Georg Henig remembers the narrator's poor childhood in Sofia after 1944, in the house on Iskar Street, and the old Czech-born violin-maker Georg Henig. It is the first of three strongly autobiographical books by Viktor Paskov, and has been on the Bulgarian school curriculum for grade 12 since 2021",
        "《格奥尔格·赫尼希谣曲》回忆 1944 年以后叙述者在索非亚度过的贫穷童年，回忆伊斯克尔街的那栋房子，和捷克裔老琴师格奥尔格·赫尼希。这是维克托·帕斯科夫三本自传色彩很浓的书里的第一本，2021 年起列入保加利亚 12 年级的课程"),
    b.ORIG("bg-ndk", "National Palace of Culture, Sofia", "索非亚国家文化宫", *C("bg-ndk"),
        "The huge 1980s congress and culture centre in Sofia, with Mount Vitosha behind it. In Time Shelter the narrator's old friend Demby, who stages historical reenactments, takes him down to a basement here to watch his troupe rehearse",
        "索非亚一座 20 世纪 80 年代的巨大会议和文化中心，背后就是维托沙山。《时间庇护所》里，叙述者的老朋友戴姆比专门排演历史“重演”，他带叙述者下到这里的一间地下室，看他的剧团排练"),
]

T_UY = "Под игото/Част първа/XVII. Представлението"
T_BG = "Бай Ганьо/Бай Ганьо пътува"
lines = [
    Q("bg-uy-1", "under-the-yoke", "bg-sopot", "Part One, XVII. The Performance", "第一部第十七章《演出》", T_UY,
      ws.cut(WSR, T_UY, "Ето защо довечерашното представление", "за сол или сапун."), ["Бяла черква"],
      "That was why tonight's performance had kept the townsfolk astir for days. They were waiting for it impatiently, as for some great event that would bring a pleasant change into the monotonous life of Byala Cherkva. Everyone was getting ready to go to the theatre. The rich ladies were preparing their finery, while the poor women sold their yarn at the market and bought a ticket on the spot, so that the money should not go on salt or soap.",
      ["Byala Cherkva"],
      "所以，好些天来，今晚的演出一直让镇上的人激动不已。大家急切地盼着它，就像盼一件大事——它会给白教堂单调的生活添一点愉快的变化。人人都打算去看戏。有钱的太太们准备好了盛装，穷人家的女人把纱线拿到集市上卖了，马上买一张票，免得这钱又花在盐和肥皂上。",
      ["白教堂"]),
    Q("bg-bg-1", "bay-ganyo", "bg-kazanlak", "I. Bay Ganyo Travels", "第一篇《巴伊·甘纽旅行》", T_BG,
      ws.block(WSR, T_BG, "Тъй като розовото масло", "ама сигур."), ["розовото масло"],
      "Since the rose oil that Bay Ganyo was carrying was indeed a rather valuable article, I advised him to hand it in to the cash office for safekeeping.\n'The cash office?' he exclaimed, in a tone that pitied my naivety. 'You learned folk are a strange lot! How do you know what sort they are at the cash office? He pockets your rose oil and off he goes round the corner… And then? What do you do? Forget it! See this sash?' And Bay Ganyo lifted his wide waistcoat. 'I'll stuff all the phials in here. True, it's a bit heavy, but it's safe.'",
      ["rose oil"],
      "因为巴伊·甘纽带的玫瑰油确实是相当值钱的东西，我劝他交给账房保管。\n“交给账房？”他叫道，那口气像是可怜我太天真，“你们这些读书人真怪！你怎么知道账房里是些什么人？把你的玫瑰油一收，人往哪儿一拐就没了……然后呢？你能怎么办？算了吧！看见这条腰带没有？”巴伊·甘纽撩起他宽大的背心，“我把所有小瓶子都塞在这里面。是有点沉，可是保险。”",
      ["玫瑰油"]),
    b.S("bg-tp-1", "time-of-parting", "bg-chepino", "Spring 1668", "1668 年春",
        "In the spring of 1668 the janissary Karaibrahim rides into the Rhodope valley of Elindenya with a troop of 120 horsemen, sent to bring its Orthodox Bulgarians to Islam. The village of Chepino is burnt and its people flee into the neighbouring mountains. The shepherd Manol asks Suleiman Agha, the master of the valley, to lead them against the janissaries, but the agha cannot rise against the sultan. The village notables gather in the agha's konak and tell Karaibrahim that they will not give up their faith: a time of parting has come.",
        "1668 年春天，近卫军骑兵卡拉易卜拉欣带着一百二十名骑兵来到罗多彼山中的埃林德尼亚谷，奉命让这里信东正教的保加利亚人改信伊斯兰教。切皮诺村被烧毁，村民逃进邻近的山里。牧羊人马诺尔请山谷的主人苏莱曼阿迦带领大家对抗近卫军，可阿迦不能起来反抗苏丹。各村的头面人物聚到阿迦的宅邸，对卡拉易卜拉欣说，他们不会放弃自己的信仰：分离的时刻到了。",
        ["Chepino"], ["切皮诺"], "https://bg.wikipedia.org/wiki/Време_разделно"),
    b.S("bg-tob-1", "tobacco-dimov", "bg-plovdiv", "Nikotiana", "尼科蒂亚纳",
        "Tobacco follows two lives in Bulgaria before 1944. Irina sets her heart on medicine from her school days, while she still lives in the country, and works her way to becoming a doctor; Boris Morev rises to be a magnate of the tobacco trade, with the firm Nikotiana. Their love is not the centre of the book; the world of tobacco is. Dimov gathered his material in Plovdiv, talking to the workers, managers and merchants of its tobacco warehouses, and Nikotiana's warehouse is modelled on the Orient Tabacco building at 8 Odrin Street.",
        "《烟草》讲 1944 年以前保加利亚的两种人生。伊里娜还住在乡下、还在上学的时候就立志学医，一步步成了医生；鲍里斯·莫雷夫则靠尼科蒂亚纳公司成了烟草业的大亨。两人的爱情不是这本书的中心，烟草的世界才是。迪莫夫的素材来自普罗夫迪夫，他在城里的烟草仓库跟工人、经理和商人交谈；尼科蒂亚纳公司的仓库，原型是奥德林街 8 号东方烟草公司的那座楼。",
        ["Plovdiv"], ["普罗夫迪夫"],
        "https://bg.wikipedia.org/wiki/Тютюн_(роман); https://en.wikipedia.org/wiki/Tobacco_(novel); https://bulgarianhistory.org/tutuneviat-sviat-na-dimitar-dimov/; https://journals.azbuki.bg/bel/tyutyun-mezdu-politiceskite-pristrastiya-i-bibleiskata-problematika/pdf"),
    b.S("bg-ball-1", "ballad-georg-henig", "bg-sofia", "The house on Iskar Street", "伊斯克尔街的房子",
        "The narrator, who bears the author's own name, remembers growing up poor in Sofia after 1944, among the people living in the house on Iskar Street. No small violin for the boy can be found anywhere, so he is taken to the old master Georg Henig, a luthier of Czech origin; in Henig's workshop the master makes a violin unlike any other, which he calls a viola d'amore.",
        "叙述者用的是作者本人的名字，他回忆 1944 年以后在索非亚度过的贫穷童年，回忆伊斯克尔街那栋房子里的人们。哪儿都找不到适合孩子的小提琴，于是他被带到捷克裔老琴师格奥尔格·赫尼希那里；在赫尼希的作坊里，老师傅做出一把跟谁都不一样的琴，他管它叫“柔音中提琴”。",
        ["Sofia"], ["索非亚"],
        "https://bg.wikipedia.org/wiki/Балада_за_Георг_Хених; https://journals.azbuki.bg/bel/zanrovi-paradigmi-v-balada-za-georg-xenix/pdf; https://journals.azbuki.bg/bel/tvorcestvoto-kato-askeza-i-gorest-balada-za-georg-xenix-viktor-paskov/pdf; https://doi.uni-plovdiv.bg/bitstreams/21a0a8c1-1c79-4bfa-ad73-ee09a3735e6b/download; https://www.capital.bg/light/neshta/2018/08/31/3303861_viktor_paskov_avtorut_sreshtu_choveka/"),
    b.S("bg-ts-1", "time-shelter", "bg-ndk", "Sofia, before the referendum", "公投前的索非亚",
        "Every country in Europe is to hold a referendum on which decade of its past it will go back to live in. The narrator, G.G., returns to Bulgaria to watch the run-up to the vote and looks up his old friend Demby, who now stages historical reenactments. Demby takes him down to a basement under the National Palace of Culture, the huge 1980s building with Mount Vitosha behind it, where his troupe rehearses staged protests: the chanting, the stone-throwing, a fake police charge, and an actor playing an injured demonstrator for the cameras.",
        "欧洲每个国家都要举行公投，决定回到过去哪一个十年里生活。叙述者 G.G. 回到保加利亚，看这场投票之前的种种，找到老朋友戴姆比——他现在专门排演历史“重演”。戴姆比把他带到国家文化宫底下的一间地下室，这座 20 世纪 80 年代的庞然大物背后就是维托沙山。剧团正在那里排练抗议的场面：喊口号，扔石头，假装警察冲上来，还有一个演员扮演受伤的示威者，演给摄像机看。",
        ["National Palace of Culture"], ["国家文化宫"],
        "https://lithub.com/time-shelter/; https://lareviewofbooks.org/article/a-referendum-on-nostalgia-on-georgi-gospodinovs-time-shelter; https://theconversation.com/time-shelter-international-bookers-first-bulgarian-winner-is-a-rich-experiment-in-style-structure-and-ideas-205895"),
]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set()
for f in glob.glob(os.path.join(APP, "data", "*", "books.js")):
    all_books |= ids_in(f)
new_b, new_p = {x["id"] for x in books}, {x["id"] for x in places}
assert len(new_b) == len(books) and len(new_p) == len(places) and len({l["id"] for l in lines}) == len(lines)
assert not new_b & all_books, new_b & all_books
assert new_p == set(CO), new_p ^ set(CO)
for l in lines:
    assert l["book_id"] in new_b and l["place_ids"][0] in new_p, l["id"]
assert {l["book_id"] for l in lines} == new_b and {l["place_ids"][0] for l in lines} == new_p

HEAD = "// Bulgaria, hand-written content (tools/content/batches/add_bg1.py, 2026-11-25).\n"
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
