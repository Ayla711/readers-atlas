"""11-07: coverage check, category 2 — the BBC Big Read titles still missing, one book per writer (14 writers), plus Dahl's
The BFG and Matilda. Two are public domain (The Ragged Trousered Philanthropists, The Woman in White): excerpts cut from the
downloaded Project Gutenberg files (#3608, #583). The rest are in copyright: scene notes in our own words only, and only where
a source says what happens there; four books get a place but no scene note (Shell Seekers, Faraway Tree, Cold Comfort Farm,
Katherine). Facts from the pages named in each place's source and in docs/week1-uk-spec.md; photos from Commons.
Usage: python3 -I add_batch18.py <app_dir> <pg_texts_dir> <photo_work_dir>"""
import importlib.util, json, re, sys
from PIL import Image
APP, TX, PW = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("b5", __file__.replace("add_batch18.py", "add_batch5.py"))
b5 = importlib.util.module_from_spec(spec)
_argv, sys.argv = sys.argv, [sys.argv[0], APP, TX]
spec.loader.exec_module(b5)
sys.argv = _argv
b5.D = ", 2026-11-07"
append, prose, B, P, PIL, PROTO, ORIG, L, W = b5.append, b5.prose, b5.B, b5.P, b5.PIL, b5.PROTO, b5.ORIG, b5.L, b5.W

def CB(id, title, title_zh, author, author_zh, year, aliases=()):
    """a book still in copyright: no source text, scene notes only"""
    return dict(id=id, title=title, title_zh=title_zh, author=author, author_zh=author_zh, year=year, orig_lang="en",
                public_domain=False, source_url=None, aliases=list(aliases))

books = [
    CB("hitchhikers-guide", "The Hitchhiker's Guide to the Galaxy", "银河系漫游指南", "Douglas Adams", "道格拉斯·亚当斯", "1979", ["银河便车指南"]),
    CB("pillars-of-the-earth", "The Pillars of the Earth", "圣殿春秋", "Ken Follett", "肯·福莱特", "1989", ["Pillars of the Earth", "地球之柱"]),
    CB("goodnight-mister-tom", "Goodnight Mister Tom", "晚安，汤姆先生", "Michelle Magorian", "米歇尔·马戈里安", "1981", ["Goodnight Mr Tom"]),
    CB("shell-seekers", "The Shell Seekers", "拾贝人", "Rosamunde Pilcher", "罗莎蒙德·皮尔彻", "1987"),
    CB("swallows-and-amazons", "Swallows and Amazons", "燕子号与亚马逊号", "Arthur Ransome", "亚瑟·兰塞姆", "1930"),
    CB("magic-faraway-tree", "The Magic Faraway Tree", "魔法树", "Enid Blyton", "伊妮德·布莱顿", "1943", ["Faraway Tree", "遥远的魔法树"]),
    # written with Neil Gaiman; the app keeps one author per book, so he is searchable through the aliases
    CB("good-omens", "Good Omens", "好兆头", "Terry Pratchett", "特里·普拉切特", "1990", ["Neil Gaiman", "尼尔·盖曼", "好预兆"]),
    B("ragged-trousered", "The Ragged Trousered Philanthropists", "穿破裤子的慈善家", "Robert Tressell", "罗伯特·特雷塞尔", "1914", 3608),
    CB("bridget-jones", "Bridget Jones's Diary", "BJ 单身日记", "Helen Fielding", "海伦·菲尔丁", "1996", ["布里奇特·琼斯的日记", "BJ单身日记"]),
    B("woman-in-white", "The Woman in White", "白衣女人", "Wilkie Collins", "威尔基·柯林斯", "1859–1860", 583),
    CB("i-capture-the-castle", "I Capture the Castle", "我的秘密城堡", "Dodie Smith", "多迪·史密斯", "1948"),
    CB("brave-new-world", "Brave New World", "美丽新世界", "Aldous Huxley", "阿道司·赫胥黎", "1932"),
    CB("cold-comfort-farm", "Cold Comfort Farm", "寒冷舒适农场", "Stella Gibbons", "斯黛拉·吉本斯", "1932", ["令人难以宽慰的农庄"]),
    CB("katherine-seton", "Katherine", "凯瑟琳", "Anya Seton", "安雅·塞顿", "1954"),
    CB("the-bfg", "The BFG", "好心眼儿巨人", "Roald Dahl", "罗尔德·达尔", "1982", ["BFG", "圆梦巨人"]),
    CB("matilda", "Matilda", "玛蒂尔达", "Roald Dahl", "罗尔德·达尔", "1988", ["玛蒂达"]),
]

TRAIL = "https://www.roalddahlmuseum.org/wp-content/uploads/2024/01/Roald-Dahl-Museum-village-trail.pdf"
places = [
    PIL("adams-grave", "Douglas Adams's grave, Highgate Cemetery", "海格特公墓 · 道格拉斯·亚当斯墓", 0, 0, "", "",
        "Adams (1952–2001) is buried in the East Cemetery at Highgate. The grave is easy to spot by the pot of pens in front of it",
        "亚当斯（1952–2001）葬在海格特公墓东园。墓前放着一罐笔，很好认", ["hitchhikers-guide"]),
    ORIG("guildford", "Guildford", "吉尔福德", 0, 0, "", "",
         "The county town of Surrey, south-west of London. In the book it is only a cover story: Ford Prefect has let everyone believe he is an out-of-work actor from here",
         "伦敦西南、萨里郡的郡治。书里它只是个幌子：福特·普里菲克特一直让人以为他是从这里来的失业演员"),
    PROTO("wells-cathedral", "Wells Cathedral", "韦尔斯大教堂", 51.2104, -2.6437, "Wells Cathedral (Wikipedia)", W + "Wells_Cathedral",
          "Kingsbridge Cathedral in The Pillars of the Earth is based on the cathedrals of Wells and Salisbury",
          "《圣殿春秋》里的王桥大教堂，原型是韦尔斯大教堂和索尔兹伯里大教堂"),
    ORIG("deptford", "Deptford", "德特福德", 0, 0, "", "",
         "A district on the south bank of the Thames in south-east London, once the site of a royal dockyard. William Beech comes from here",
         "伦敦东南、泰晤士河南岸的一片街区，过去有皇家造船厂。威廉·比奇就是从这里来的"),
    PIL("lelant", "Lelant, Cornwall", "康沃尔 · 莱兰特", 0, 0, "", "",
        "Pilcher was born in this village on the Hayle estuary, near St Ives, in 1924. The South West Coast Path's page on her Cornwall says The Shell Seekers is set in London and Lelant",
        "皮尔彻 1924 年生在这个村子，村子在圣艾夫斯附近的海尔河口。西南海岸步道介绍她的康沃尔的页面说，《拾贝人》的故事发生在伦敦和莱兰特",
        ["shell-seekers"]),
    PROTO("peel-island", "Peel Island, Coniston Water", "科尼斯顿湖 · 皮尔岛", 0, 0, "", "",
          "One of the models for Wild Cat Island. Ransome first met the Collingwood family at a picnic here when he was eight, and their grandchildren helped shape the Swallows. The island belongs to the National Trust",
          "野猫岛的原型之一。兰塞姆八岁时在这座岛上野餐，第一次认识了科林伍德一家；后来这家人的孙辈成了“燕子号”孩子们的原型之一。岛属于国民信托"),
    PIL("green-hedges", "Site of Green Hedges, Beaconsfield", "比肯斯菲尔德 · 绿篱旧址", 0, 0, "", "",
        "Blyton moved to Green Hedges on Penn Road in 1938, and English Heritage says most of her books were written there; the Faraway Tree books came out between 1939 and 1951, while she lived here. The house was pulled down in 1973 and Blyton Close now stands on the site",
        "布莱顿 1938 年搬进彭路上的“绿篱”，英格兰遗产委员会说她的大部分书是在这里写的；魔法树系列 1939 至 1951 年陆续出版，正是她住在这里的时候。房子 1973 年拆掉，原址现在是布莱顿巷",
        ["magic-faraway-tree"]),
    PROTO("hastings", "Hastings", "黑斯廷斯", 50.8550, 0.5833, "Hastings (Wikipedia)", W + "Hastings",
          "Mugsborough, the town in The Ragged Trousered Philanthropists, is Hastings. Tressell worked for builders and decorators here and wrote most of the novel in a top-floor flat at 241 London Road, St Leonards, which has a plaque",
          "《穿破裤子的慈善家》里的马格斯伯勒就是黑斯廷斯。特雷塞尔在这里给建筑和装修商做工，小说大部分写在圣伦纳兹伦敦路 241 号的顶层公寓里，门边有纪念牌"),
    P("globe-borough", "The Globe, Bedale Street, Borough", "博罗 · 环球酒馆", 0, 0, "", "", "film_location",
      adaptation={"title": "Bridget Jones's Diary", "year": 2001, "kind": "电影"}, scene="布里奇特的公寓（酒馆楼上）",
      scene_en="Bridget's flat, above the pub", book_ids=["bridget-jones"]),
    ORIG("platts-lane", "Platt's Lane, Hampstead", "汉普斯特德 · 普拉茨巷", 0, 0, "", "",
         "The Wilkie Collins Society traced Walter Hartright's night walk across Hampstead Heath to this junction, where Pratts Lane (now Platt's Lane) meets Finchley Road",
         "威尔基·柯林斯学会按书中的路线考证，沃尔特·哈特赖特穿过汉普斯特德荒野的那次夜行，就走到了这个路口：当年写作 Pratts Lane、今天叫普拉茨巷的小路，在这里接上芬奇利路"),
    PROTO("wingfield-castle", "Wingfield Castle, Suffolk", "萨福克 · 温菲尔德城堡", 52.3479, 1.2595, "Wingfield Castle (Wikipedia)", W + "Wingfield_Castle",
          "The inspiration for Godsend Castle, the Mortmain family's home in I Capture the Castle. It is a private house and not open to the public",
          "《我的秘密城堡》里莫特曼一家住的“天赐城堡”，原型就是这座城堡。现在是私宅，不对外开放"),
    ORIG("puttenham-common", "Puttenham Common, Surrey", "萨里 · 帕特纳姆公地", 0, 0, "", "",
         "Heath and woodland between Farnham and Guildford, south of Puttenham village and towards Elstead. The Savage's lighthouse in the book is made up, but it stands on a hill between Puttenham and Elstead, with the Hog's Back to the north",
         "法纳姆和吉尔福德之间的一片荒地和树林，在帕特纳姆村南边，往埃尔斯特德方向。书里野人住的灯塔是虚构的，但书里说它在帕特纳姆和埃尔斯特德之间的山头上，北面是猪背岭"),
    PIL("the-lady-offices", "The Lady, 39–40 Bedford Street, Covent Garden", "考文特花园 · 《淑女》杂志旧址", 0, 0, "", "",
        "Gibbons was an editorial assistant on The Lady and wrote Cold Comfort Farm in spare moments at the magazine's Covent Garden offices; a colleague remembered her neglecting her duties for the novel. The Lady was at 39–40 Bedford Street until 2019",
        "吉本斯在《淑女》杂志做编辑助理，《寒冷舒适农场》就是她在杂志社考文特花园办公室里抽空写的；一位同事记得她为了写小说常常耽误本职工作。《淑女》杂志在贝德福德街 39–40 号一直待到 2019 年",
        ["cold-comfort-farm"]),
    PROTO("lincoln-cathedral", "Lincoln Cathedral", "林肯大教堂", 53.23444, -0.53611, "Lincoln Cathedral (Wikipedia)", W + "Lincoln_Cathedral",
          "The real Katherine Swynford, heroine of Anya Seton's Katherine, lived in the cathedral close in later life. She is buried here with her daughter Joan Beaufort, on the south side of the Angel Choir",
          "安雅·塞顿《凯瑟琳》的主人公凯瑟琳·斯温福德确有其人，晚年住在大教堂的教堂区里。她和女儿琼·博福特合葬在这里，墓在天使唱诗堂的南侧"),
    PROTO("crown-house-missenden", "Crown House, Great Missenden", "大米森登 · 皇冠屋", 0, 0, "", "",
          "The Roald Dahl Museum's village trail says this timber-framed house at 70 High Street inspired Sophie's orphanage in The BFG. It is a private home",
          "罗尔德·达尔博物馆的村庄步道说，高街 70 号这座木结构老房子是《好心眼儿巨人》里苏菲那家孤儿院的原型。现在是私宅"),
    PROTO("missenden-library", "Great Missenden Library", "大米森登图书馆", 0, 0, "", "",
          "The museum's village trail says this is the library Matilda visited while her mother went off to Aylesbury to play bingo. The building dates from 1970",
          "博物馆的村庄步道说，这就是玛蒂尔达常来的那座图书馆：妈妈去艾尔斯伯里打宾果，她就到这里来。现在的房子建于 1970 年"),
]
SRC = {   # where the fact on each place comes from, when it is not the coordinate source
    "adams-grave": "https://highgatecemetery.org/explore/douglas-adams",
    "lelant": "https://www.southwestcoastpath.org.uk/pilcher/",
    "green-hedges": "https://www.english-heritage.org.uk/visit/blue-plaques/enid-blyton/",
    "hastings": "https://hastingshistory.net/features/tressel-and-mugsborough",
    "globe-borough": "https://exploring-london.com/tag/bridget-jones/",
    "platts-lane": "https://wilkiecollinssociety.org/wp/wp-content/uploads/2024/03/2010-08-Walters-Walk.pdf",
    "the-lady-offices": "https://www.camdennewjournal.co.uk/article/cold-comfort-farm-author-stella-gibbons-be-honoured-plaque-former-hampstead-home",
    "lincoln-cathedral": "https://www.visitlincolnshire.com/be-inspired/did-you-know/katherine-swynford/",
    "crown-house-missenden": TRAIL, "missenden-library": TRAIL,
}
for p in places:
    if p["id"] in SRC:
        p["fact_source"] = SRC[p["id"]]

def S(id, book_id, place, loc, loc_zh, en, zh, hl_en, hl_zh):
    for h in hl_en:
        assert h in en, (id, h)
    for h in hl_zh:
        assert h in zh, (id, h)
    return dict(id=id, kind="scene", book_id=book_id, place_ids=[place], location=loc, location_zh=loc_zh,
                text_en=en, text_zh=zh, highlight_en=hl_en, highlight_zh=hl_zh, status="draft")

lines = [
    S("hhg-s1", "hitchhikers-guide", "guildford", "Chapter 2", "第 2 章",
      "In the pub, Ford Prefect tells Arthur Dent that he is not from Guildford after all but from a small planet somewhere near Betelgeuse, and that the world is about to end.",
      "在酒馆里，福特·普里菲克特告诉亚瑟·邓特：他根本不是吉尔福德人，而是来自参宿四附近的一颗小行星；还有，世界马上就要完了。",
      ["Guildford"], ["吉尔福德"]),
    S("pote-s1", "pillars-of-the-earth", "wells-cathedral", "Part One", "第一部",
      "The old cathedral at Kingsbridge burns down. Tom Builder's stepson Jack set the fire so that Tom would have work, and the prospect of a new cathedral there excites both Prior Philip and Tom.",
      "王桥的老教堂被一把火烧了。放火的是汤姆的继子杰克，为的是让汤姆有活干；要在这里建一座新大教堂，菲利普院长和汤姆都为此激动不已。",
      ["Kingsbridge"], ["王桥"]),
    S("gmt-s1", "goodnight-mister-tom", "deptford", "Chapter 16, The Search", "第 16 章《寻找》",
      "When Willie's letters stop, Tom takes the train to London with his dog Sammy and searches Deptford for the Beech family's flat. The house seems empty, but Sammy runs to a locked cupboard under the stairs and scrabbles at the door.",
      "威利的信断了以后，汤姆带着狗萨米坐火车去伦敦，在德特福德一路打听比奇家的住处。屋里好像没人，萨米却冲到楼梯下一扇锁着的柜门前，拼命扒门。",
      ["Deptford"], ["德特福德"]),
    S("sa-s1", "swallows-and-amazons", "peel-island", "Chapter 1, The Peak in Darien", "第 1 章《达连峰》",
      "From the hill above the lake the Walker children look out at an island, and start planning to sail there in Swallow, the farm's little boat, and camp on it.",
      "沃克家的孩子们站在湖边的山上眺望湖中的小岛，开始盘算：驾着农场的小帆船“燕子号”开过去，在岛上扎营。",
      ["island"], ["小岛"]),
    S("go-s1", "good-omens", "soho", "Eleven Years Ago", "《十一年前》",
      "After lunch at the Ritz, Aziraphale and Crowley go back to Aziraphale's bookshop in Soho, which is really just a place to keep his books. There, very drunk, they agree to watch over the Antichrist's upbringing while cancelling out each other's influence.",
      "在丽兹饭店吃完午饭，亚茨拉斐尔和克鲁利回到亚茨拉斐尔在苏豪区的旧书店——那其实只是他放书的地方。两人喝得酩酊大醉，商定一起盯着敌基督长大，同时互相抵消对方的影响。",
      ["Soho"], ["苏豪区"]),
    S("ictc-s1", "i-capture-the-castle", "wingfield-castle", "Part 1, The Sixpenny Book, Chapter 1", "第一部《六便士本子》第 1 章",
      "Seventeen-year-old Cassandra Mortmain begins her journal sitting in the kitchen sink of the crumbling castle her family rents, writing it partly to teach herself speed-writing.",
      "十七岁的卡桑德拉·莫特曼坐在厨房水槽里，开始写日记；她家租住在一座破败的城堡里，她写日记一半是为了练速记。",
      ["castle"], ["城堡"]),
    S("bnw-s1", "brave-new-world", "puttenham-common", "Chapter 18", "第 18 章",
      "The Savage escapes from London to an old lighthouse on a hilltop between Puttenham and Elstead, with the Hog's Back to the north. He makes a bow and arrows and plants a garden, meaning to live there alone.",
      "野人逃离伦敦，躲进帕特纳姆和埃尔斯特德之间山头上的一座旧灯塔，北面就是猪背岭。他做了弓箭，开了一块菜园，打算一个人在那里过下去。",
      ["Puttenham"], ["帕特纳姆"]),
    S("bfg-s1", "the-bfg", "crown-house-missenden", "Chapter 1, The Witching Hour", "第 1 章《巫时》",
      "Sophie cannot sleep in the orphanage dormitory. Looking out at the moonlit street in the middle of the night, she sees a giant across the way blowing something like a trumpet into a bedroom window.",
      "苏菲在孤儿院的宿舍里睡不着。半夜她望向月光下的街道，看见对面有个巨人，正拿着一个像喇叭的东西往一扇卧室窗户里吹。",
      ["orphanage"], ["孤儿院"]),
    S("mat-s1", "matilda", "missenden-library", "Chapter 1, The Reader of Books", "第 1 章《读书的人》",
      "Left alone every afternoon, four-year-old Matilda walks to the village library by herself and asks Mrs Phelps for somewhere to read. She soon finishes the children's shelves, and Mrs Phelps starts her on grown-up classics.",
      "每天下午都没人管，四岁的玛蒂尔达自己走到村里的图书馆，问费尔普斯太太能不能找个地方读书。她很快读完了所有儿童书，费尔普斯太太便开始给她推荐大人看的名著。",
      ["village library"], ["图书馆"]),
    L("rtp-1", "ragged-trousered", "hastings", "Appendix, Mugsborough", "附录《马格斯伯勒》",
      prose(3608, "Mugsborough was a town of about eighty thousand inhabitants", "mild in winter."), ["Mugsborough"], 3608),
    L("wiw-c1", "woman-in-white", "platts-lane", "The First Epoch, The Story Begun by Walter Hartright, IV", "第一阶段，沃尔特·哈特赖特开始的叙述，第 4 节",
      prose(583, "I had now arrived at that particular point of my walk where four roads", "suddenly on my shoulder from behind me."), ["four roads"], 583),
    L("wiw-c2", "woman-in-white", "platts-lane", "The First Epoch, The Story Begun by Walter Hartright, IV", "第一阶段，沃尔特·哈特赖特开始的叙述，第 4 节",
      prose(583, "There, in the middle of the broad bright high-road", "as I faced her."), ["Woman, dressed from head to foot in white"], 583),
]

# coordinates found for this batch (source title, source url), and the photo picks
COORDS = json.load(open(f"{PW}/coords.json", encoding="utf-8"))
for p in places:
    if p["id"] in COORDS:
        la, lo, st, su = COORDS[p["id"]]
        p["lat"], p["lon"], p["coord_checked"] = la, lo, f"{st} — {su}{b5.D}"
    assert p["lat"] and p["coord_checked"].split(" — ")[1].startswith("http"), p["id"]

PHOTOS = json.load(open(f"{PW}/choice.json", encoding="utf-8"))
cands = json.load(open(f"{PW}/candidates.json"))
for p in places:
    if p["id"] not in PHOTOS:
        continue
    n, en, zh, crop = PHOTOS[p["id"]]
    c = cands[p["id"]]["candidates"][n]
    im = Image.open(f"{PW}/dl/{p['id']}__{n}.jpg").convert("RGB")
    if crop:
        x0, y0, x1, y1 = crop
        im = im.crop((round(x0 * im.width), round(y0 * im.height), round(x1 * im.width), round(y1 * im.height)))
    if im.width > 800:
        im = im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS)
    assert im.width >= im.height, p["id"]
    rel = f"images/places/{p['id']}.jpg"
    im.save(f"{APP}/{rel}", "JPEG", quality=82, optimize=True, progressive=True)
    p["photo"] = {"file": rel, "width": im.width, "height": im.height, "author": c["author"].strip() or "Unknown author", "license": c["license"].strip(),
                  "license_url": c["license_url"].strip(), "source": c["page"], "alt_en": en, "alt_zh": zh}
    if crop:
        p["photo"]["cropped"] = True

def link(pid, bids):
    path = f"{APP}/data/places.js"
    s = open(path, encoding="utf-8").read()
    m = re.search(r'(\{ id: "' + pid + r'".*?book_ids: )(\[[^\]]*\])', s)
    ids = json.loads(m.group(2))
    ids += [b for b in bids if b not in ids]
    s = s[:m.start(2)] + json.dumps(ids, ensure_ascii=False) + s[m.end(2):]
    open(path, "w", encoding="utf-8").write(s)

if __name__ == "__main__":
    append(f"{APP}/data/books.js", books, "11-07 Big Read 第二档：14 位作家各一本代表作，加达尔的《好心眼儿巨人》《玛蒂尔达》")
    append(f"{APP}/data/places.js", places, "11-07 Big Read 第二档（坐标和照片均有出处）")
    append(f"{APP}/data/lines.js", lines, "11-07 Big Read 第二档：两本公有领域书的古登堡原文摘句，其余为场景说明（草稿，待审核）")
    link("dahl-museum", ["the-bfg", "matilda"])
    rows = [f"| {p['name']} | {p['photo']['author']} | [{p['photo']['license']}]({p['photo']['license_url']}) | [Commons]({p['photo']['source']}) |" for p in places if "photo" in p]
    cr = open(f"{APP}/docs/photo-credits.md", encoding="utf-8").read().rstrip("\n") + "\n" + "\n".join(rows) + "\n"
    open(f"{APP}/docs/photo-credits.md", "w", encoding="utf-8").write(cr)
    for l in lines:
        print(l["id"], "|", l["text_en"][:110])
