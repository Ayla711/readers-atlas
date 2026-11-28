"""11-28: Canada, rule-v2 re-check (tools/selection/ca.md), first batch of the 42 new books: Atlantic Canada.
- Fall on Your Knees (Ann-Marie MacDonald): New Waterford, the Cape Breton coal town where the Pipers live (191 Water Street);
- The Birth House (Ami McKay): Scots Bay on the Bay of Fundy, where the novel is set and where McKay lives in the old "birth house";
- The Colony of Unrequited Dreams (Wayne Johnston) and Annabel (Kathleen Winter): St. John's. Smallwood grows up on the Brow in
  St. John's; Wayne, born in the invented Labrador village of Croydon Harbour, moves to St. John's after school;
- The Shipping News (Annie Proulx): Killick-Claw and Quoyle's Point are invented; the 2001 film was shot in Trinity Bight, with
  Trinity among its locations and New Bonaventure standing in for Killick-Claw, so the book is shown through the film at Trinity
  (no excerpt or scene note may hang on a film location).
Galore (Michael Crummey) waits: Paradise Deep and the Gut are invented and no real place carries the book; the user decides.
All five are in copyright: scene notes, no quotation. Coordinates: coords/add_ca_v2_1128_1.json (en.wikipedia).
Usage: python3 -I tools/content/batches/add_ca_v2_1128_1.py <app_dir> tools/content/batches/coords/add_ca_v2_1128_1.json"""
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
    BK("fall-on-your-knees", "Fall on Your Knees", "跪下", "Ann-Marie MacDonald", "安-玛丽·麦克唐纳", "1996",
       ["Fall on Your Knees", "James Piper", "Materia", "Kathleen Piper", "Frances Piper", "New Waterford"]),
    BK("the-birth-house", "The Birth House", "接生屋", "Ami McKay", "艾米·麦凯", "2006",
       ["The Birth House", "Dora Rare", "Miss Babineau", "Scots Bay"]),
    BK("colony-of-unrequited-dreams", "The Colony of Unrequited Dreams", "未竟之梦的殖民地", "Wayne Johnston", "韦恩·约翰斯顿", "1998",
       ["The Colony of Unrequited Dreams", "Joey Smallwood", "Sheilagh Fielding", "Smallwood"]),
    BK("annabel-winter", "Annabel", "安娜贝尔", "Kathleen Winter", "凯瑟琳·温特", "2010",
       ["Annabel", "Wayne Blake", "Croydon Harbour", "Treadway", "Thomasina"]),
    BK("the-shipping-news", "The Shipping News", "船讯", "Annie Proulx", "安妮·普鲁", "1993",
       ["The Shipping News", "Quoyle", "Killick-Claw", "Gammy Bird", "Proulx"]),
]

places = [
    b.ORIG("ca-new-waterford", "New Waterford, Cape Breton", "新沃特福德（布雷顿角）", *C("ca-new-waterford"),
        "Former coal-mining town on the Atlantic shore of Cape Breton Island, north-east of Sydney, once called Barrachois Cove; coal was dug around it from the 1850s, and its last mine closed in 2001. Ann-Marie MacDonald's father came from New Waterford and worked in the mines to put himself through university; her Fall on Your Knees (1996) begins with a picture of the town by moonlight, the collieries and the rows of miners' houses, and the Piper family's house on Water Street",
        "布雷顿角岛大西洋岸边的老煤矿镇，在悉尼东北，早先叫巴拉舒瓦湾；十九世纪五十年代起周围就开采煤炭，最后一座矿 2001 年关闭。安-玛丽·麦克唐纳的父亲是新沃特福德人，当年下矿挣学费读完了大学；她的《跪下》（1996）一开头就是这座小镇月夜的一张“照片”：矿井、一排排矿工房子，还有派珀一家在水街上的家"),
    b.ORIG("ca-scots-bay", "Scots Bay, Nova Scotia", "斯科茨湾（新斯科舍）", *C("ca-scots-bay"),
        "Small Bay of Fundy community in Kings County, near Cape Split, settled in 1764; it lived by fishing, farming, logging and shipbuilding, and its last schooner was launched in 1918. Ami McKay moved into an old farmhouse here and learned that it had been known as the birth house, where a local midwife delivered the village's babies in the early twentieth century; that history became her first novel, The Birth House (2006), set in Scots Bay",
        "芬迪湾边国王县的小村，靠近斯普利特角，1764 年有人定居；靠打鱼、种地、伐木和造船为生，最后一艘纵帆船 1918 年在这里下水。艾米·麦凯搬进这里一座老农舍，才知道它从前被叫作“接生屋”：二十世纪初，村里的接生婆在这里接下了全村的孩子。这段往事成了她的第一部小说《接生屋》（2006），故事就发生在斯科茨湾"),
    b.ORIG("ca-st-johns", "St. John's, Newfoundland", "圣约翰斯（纽芬兰）", *C("ca-st-johns"),
        "Capital of Newfoundland and Labrador, on the eastern tip of the Avalon Peninsula, the easternmost city in North America. In Wayne Johnston's The Colony of Unrequited Dreams (1998) the young Joey Smallwood grows up poor on the Brow in St. John's, and the journalist Sheilagh Fielding walks its streets; in Kathleen Winter's Annabel (2010) Wayne Blake leaves the Labrador coast for St. John's, the city his mother came from",
        "纽芬兰与拉布拉多省首府，在阿瓦隆半岛东端，是北美最东的城市。韦恩·约翰斯顿的《未竟之梦的殖民地》（1998）里，少年乔伊·斯莫尔伍德在圣约翰斯贫穷的“坡顶”长大，记者希拉·菲尔丁在这座城的街巷里游走；凯瑟琳·温特的《安娜贝尔》（2010）里，韦恩·布莱克离开拉布拉多海岸，来到母亲的故乡圣约翰斯"),
    b.P("ca-trinity", "Trinity, Trinity Bay", "三一镇（三一湾）", *C("ca-trinity"), "film_location",
        adaptation={"title": "The Shipping News", "year": 2001, "kind": "电影"},
        scene="莱塞·霍尔斯道姆 2001 年把安妮·普鲁的《船讯》拍成电影，凯文·史派西主演，大半在纽芬兰三一湾的三一湾角一带拍摄；三一镇是外景地之一，往南几公里的新博纳旺蒂尔演了书里的基利克-克劳镇。普鲁坚持电影必须在纽芬兰拍。书里的基利克-克劳和奎尔角都是虚构的：纽约州北部的报社小职员奎尔，父母双双自杀，妻子佩塔尔跟别的男人出车祸死了；姑妈阿格尼丝·哈姆劝他带着两个女儿回到祖先的纽芬兰，搬进奎尔角上一座荒废的老屋。他在小镇报纸《海鸥报》写车祸，也写港口船只进出的“船讯”，这一栏慢慢成了他的招牌；他交了朋友，和本地寡妇韦薇·普劳斯走到一起，也慢慢知道了祖先阴暗的往事。摘句不能挂在影视取景地上，所以这本书通过这部电影出现在这里",
        book_ids=["the-shipping-news"],
        scene_en="Lasse Hallström's 2001 film of Annie Proulx's The Shipping News, with Kevin Spacey, was shot largely in Trinity Bight on Trinity Bay, Newfoundland; Trinity is one of its locations, and New Bonaventure, a few kilometres south, stood in for the novel's Killick-Claw. Proulx held out for the film to be made in Newfoundland. The book's Killick-Claw and Quoyle's Point are invented: Quoyle, a newspaperman from upstate New York, loses his parents to a double suicide and his wife Petal to a car crash with another man; his aunt Agnis Hamm talks him into taking his two daughters to the family's Newfoundland, to the abandoned house on Quoyle's Point. On the local paper, the Gammy Bird, he covers car wrecks and the shipping news, the comings and goings of ships in port, which becomes his signature column; he makes friends, finds his way to the widow Wavey Prowse, and learns the dark secrets of his ancestors. Excerpts cannot be hung on a film location, so the book is shown here through the film"),
]

lines = [
    b.S("folyk-s1", "fall-on-your-knees", "ca-new-waterford", "Prologue, “Silent Pictures”, and throughout", "序章《无声的照片》，及全书",
        "At the turn of the twentieth century the piano tuner James Piper elopes with thirteen-year-old Materia Mahmoud, daughter of a wealthy Lebanese family, and settles in the coal town of New Waterford on Cape Breton Island. Their daughters are Kathleen, the gifted eldest, whom James adores and sends to New York to train as an opera singer, then Mercedes, Frances and Lily. The novel opens with the house at 191 Water Street, New Waterford, and Ma on the day she died, 23 June 1919, and follows the sisters through the First World War, the mines and the Depression to Jazz-Age Harlem, as they hold together around a terrible family secret.",
        "二十世纪初，钢琴调音师詹姆斯·派珀和十三岁的玛特丽娅·马哈茂德私奔；她出身富裕的黎巴嫩家庭。两人在布雷顿角岛的煤矿镇新沃特福德安了家，生下几个女儿：长女凯瑟琳天赋过人，詹姆斯对她宠爱有加，送她去纽约学唱歌剧；之后是梅塞德斯、弗朗西丝和莉莉。小说开篇是新沃特福德水街 191 号的那座房子，和“妈妈去世那天”：1919 年 6 月 23 日。故事跟着姐妹们走过第一次世界大战、矿井和大萧条，一直到爵士时代的哈莱姆；她们围着一个可怕的家族秘密，彼此依靠着活下去。",
        ["Cape Breton Island", "New Waterford"], ["布雷顿角岛", "新沃特福德"],
        "https://cbra.library.utoronto.ca/items/show/3992; https://www.simonandschuster.net/books/Fall-On-Your-Knees/Ann-Marie-MacDonald/9781451641653; https://en.wikipedia.org/wiki/Fall_on_Your_Knees; https://www.powells.com/book/fall-on-your-knees-9780770429379"),
    b.S("birthhouse-s1", "the-birth-house", "ca-scots-bay", "Throughout", "全书",
        "Dora Rare, the first daughter born to the Rare family in five generations, grows up in the isolated Bay of Fundy village of Scots Bay, where her family descends from a Scottish woman shipwrecked on the bay and a Mi'kmaq man called Silent Rare. As a girl she befriends Miss Marie Babineau, the outspoken Acadian midwife and healer, and at the outbreak of the First World War becomes her apprentice; together they help the women of Scots Bay through difficult labours, infertility and unwanted pregnancies. When the brash obstetrician Gilbert Thomas arrives promising fast, painless childbirth, some of the women begin to doubt Miss B.'s ways, and after Miss B.'s death Dora carries on alone, against a background of war, the influenza, the Halifax Explosion and the Boston Molasses Flood of 1919.",
        "多拉·雷尔是雷尔家五代人里头一个女儿，在芬迪湾边与世隔绝的斯科茨湾长大；她家的先人是一个在湾里遇上海难的苏格兰女人和一个人称“沉默的雷尔”的米克马克男人。她小时候就和直言不讳的阿卡迪亚接生婆兼草药医玛丽·巴比诺小姐交上了朋友，第一次世界大战开始时做了她的徒弟，两人一起帮斯科茨湾的女人们度过难产、不孕和不想要的怀孕。莽撞的产科医生吉尔伯特·托马斯来到村里，许诺又快又不疼地生孩子，一些女人开始怀疑巴比诺小姐的老办法；巴比诺小姐死后，多拉独自撑了下去。背景是战争、大流感、哈利法克斯大爆炸和 1919 年的波士顿糖蜜洪水。",
        ["Scots Bay"], ["斯科茨湾"],
        "https://quillandquire.com/review/the-birth-house/; https://www.goodreads.com/book/show/171102; https://www.4thestate.co.uk/products/the-birth-house-ami-mckay-9780007232826-2/; https://www.biblio.com/0676977731; https://www.thebookbag.co.uk/reviews/The_Birth_House; https://bac-lac.wayback.archive-it.org/web/20071114233355/http://www.cbc.ca/arts/books/birth.html"),
    b.S("colony-s1", "colony-of-unrequited-dreams", "ca-st-johns", "Throughout", "全书",
        "A fictionalised life of Joey Smallwood, the politician who brought Newfoundland into Confederation with Canada in 1949, told mostly in his own voice and intertwined with that of the invented journalist and satirist Sheilagh Fielding. Smallwood grows up on the Brow, the poorest part of St. John's, and goes to school in the city; he covers the seal hunt and sees men die in a storm on the ice, spends years in New York as a struggling socialist journalist, and comes home to walk the railway line across the whole island in 1925 to unionise the railway workers. The novel follows the first half of his life as he drives on into politics, pushing aside his love for Fielding, while the mystery of a letter attributed to her runs beneath it all.",
        "这是乔伊·斯莫尔伍德的小说化传记：1949 年正是这位政治家把纽芬兰带进了加拿大联邦。故事大半由他自己讲述，和虚构的记者、讽刺作家希拉·菲尔丁的声音交织在一起。斯莫尔伍德在圣约翰斯最穷的“坡顶”长大，在城里上学；他报道过猎海豹，亲眼看着人们在冰上的风暴里死去；在纽约做了几年潦倒的社会主义记者，回到纽芬兰后，1925 年沿着铁路徒步横穿全岛，去把铁路工人组织进工会。小说写的是他前半生：他一路闯进政坛，把对菲尔丁的爱搁在一边，而一封据说出自她手的信的谜团，一直潜伏在故事底下。",
        ["St. John's", "Newfoundland"], ["圣约翰斯", "纽芬兰"],
        "https://en.wikipedia.org/wiki/The_Colony_of_Unrequited_Dreams; https://bookpage.com/reviews/570-wayne-johnston-review-fiction/; https://quillandquire.com/?p=72737; https://www.themodernnovel.org/americas/other-americas/canada/johnston/colony/; https://openlibrary.org/isbn/0676971822"),
    b.S("annabel-s1", "annabel-winter", "ca-st-johns", "Later chapters", "后半部",
        "In March 1968, in the village of Croydon Harbour on the south-east Labrador coast, Jacinta Blake gives birth in her bathtub to a child with both male and female anatomy. Her husband Treadway, a trapper, decides to raise the child as a boy, Wayne; only the parents and their friend Thomasina, the midwife, know, and Thomasina privately calls the child Annabel, after her own drowned daughter. Wayne grows up in a hunting world, dreams of synchronized swimming, and at puberty a medical emergency puts him in hospital, though he learns its full causes only years later. After high school he moves to St. John's, the city his mother came from, to find out the truth; there he stops the masculinising medication, lets his body change, and comes to accept himself, later making peace with his father.",
        "1968 年 3 月，在拉布拉多东南海岸的克罗伊登港，杰辛塔·布莱克在浴缸里生下一个同时具有男女两种身体特征的孩子。丈夫特雷德韦是个设陷阱打猎的人，他决定把孩子当男孩养，取名韦恩；知道真相的只有父母和他们的朋友、接生的托马西娜，托马西娜私下叫这个孩子“安娜贝尔”，那是她自己淹死的女儿的名字。韦恩在一个打猎的男人世界里长大，却梦想着花样游泳；到了青春期，一场急病让他住进医院，个中原因他多年后才完全知道。高中毕业后，他搬到母亲的故乡圣约翰斯去弄清真相，在那里停掉了让自己男性化的药，任身体自然改变，慢慢接纳了真实的自己，后来也和父亲和解。",
        ["St. John's", "Labrador"], ["圣约翰斯", "拉布拉多"],
        "https://en.wikipedia.org/wiki/Annabel_(Winter_novel); https://quillandquire.com/review/annabel/; https://erudit.org/en/journals/scl/2014-v39-n1-scl04781/1062365ar.pdf; https://mtlreviewofbooks.ca/reviews/annabel/; https://www.theglobeandmail.com/arts/books-and-media/annabel-by-kathleen-winter/article4392478/"),
]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "books.js"))))
all_places = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "places.js"))))
all_lines = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "lines.js"))))
assert not {x["id"] for x in books} & all_books
assert {p["id"] for p in places} == set(CO) and not set(CO) & all_places
assert not {l["id"] for l in lines} & all_lines
if __name__ == "__main__":
    note = "11-28 Canada rule-v2 re-check, batch 1: Atlantic Canada (add_ca_v2_1128_1.py)"
    append(b.data("books.js"), books, note)
    append(b.data("places.js"), places, note)
    append(b.data("lines.js"), lines, note)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
