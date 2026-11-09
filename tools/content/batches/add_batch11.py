"""11-04 night: classics batch. Fourteen public-domain books with excerpts cut out of the downloaded Project Gutenberg
files; Winnie-the-Pooh (in UK copyright until the end of 2026, public domain in the US) quoted from Gutenberg like
The Waste Land and marked public_domain: false; scene notes in our own words for three books still in copyright
(Rebecca, The Hobbit, The Lion, the Witch and the Wardrobe). Coordinates from Geograph / Commons / Wikipedia;
photos from Commons for every real-life model and pilgrimage place.
Usage: python3 -I add_batch11.py <app_dir> <pg_texts_dir> <photo_work_dir>"""
import importlib.util, json, sys
from PIL import Image
APP, TX, PW = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("b5", __file__.replace("add_batch11.py", "add_batch5.py"))
b5 = importlib.util.module_from_spec(spec)
_argv, sys.argv = sys.argv, [sys.argv[0], APP, TX]
spec.loader.exec_module(b5)
sys.argv = _argv
prose, append, B, ORIG, PROTO, PIL, L, D, W = b5.prose, b5.append, b5.B, b5.ORIG, b5.PROTO, b5.PIL, b5.L, b5.D, b5.W
GEO = "https://www.geograph.org.uk/photo/"
COM = "https://commons.wikimedia.org/wiki/"

books = [
    B("oliver-twist", "Oliver Twist", "雾都孤儿", "Charles Dickens", "狄更斯", "1838", 730),
    B("christmas-carol", "A Christmas Carol", "圣诞颂歌", "Charles Dickens", "狄更斯", "1843", 46),
    B("frankenstein", "Frankenstein", "弗兰肯斯坦", "Mary Shelley", "玛丽·雪莱", "1818", 84),
    B("middlemarch", "Middlemarch", "米德尔马契", "George Eliot", "乔治·艾略特", "1871–1872", 145),
    B("sense-and-sensibility", "Sense and Sensibility", "理智与情感", "Jane Austen", "奥斯汀", "1811", 161),
    B("far-from-the-madding-crowd", "Far from the Madding Crowd", "远离尘嚣", "Thomas Hardy", "哈代", "1874", 107),
    B("treasure-island", "Treasure Island", "金银岛", "Robert Louis Stevenson", "史蒂文森", "1883", 120),
    B("jekyll-and-hyde", "Strange Case of Dr Jekyll and Mr Hyde", "化身博士", "Robert Louis Stevenson", "史蒂文森", "1886", 43),
    B("ivanhoe", "Ivanhoe", "艾凡赫", "Walter Scott", "司各特", "1819", 82),
    B("thirty-nine-steps", "The Thirty-Nine Steps", "三十九级台阶", "John Buchan", "约翰·巴肯", "1915", 558),
    B("secret-garden", "The Secret Garden", "秘密花园", "Frances Hodgson Burnett", "弗朗西丝·霍奇森·伯内特", "1911", 113),
    B("peter-rabbit", "The Tale of Peter Rabbit", "彼得兔的故事", "Beatrix Potter", "比阿特丽克斯·波特", "1902", 14838),
    B("robinson-crusoe", "Robinson Crusoe", "鲁滨逊漂流记", "Daniel Defoe", "笛福", "1719", 521),
    B("gullivers-travels", "Gulliver's Travels", "格列佛游记", "Jonathan Swift", "斯威夫特", "1726", 829),
    # Milne died in January 1956: in UK copyright until the end of 2026; public domain in the US (1926), hence Gutenberg
    B("winnie-the-pooh", "Winnie-the-Pooh", "小熊维尼", "A. A. Milne", "A. A. 米尔恩", "1926", 67098, pd=False),
    dict(id="rebecca", title="Rebecca", title_zh="蝴蝶梦", author="Daphne du Maurier", author_zh="达芙妮·杜穆里埃", year="1938", orig_lang="en", public_domain=False, source_url=None),
    dict(id="the-hobbit", title="The Hobbit", title_zh="霍比特人", author="J. R. R. Tolkien", author_zh="托尔金", year="1937", orig_lang="en", public_domain=False, source_url=None),
    dict(id="lion-witch-wardrobe", title="The Lion, the Witch and the Wardrobe", title_zh="狮子、女巫和魔衣橱", author="C. S. Lewis", author_zh="C. S. 刘易斯", year="1950", orig_lang="en", public_domain=False, source_url=None, aliases=["Narnia", "纳尼亚"]),
]

def G(n, what):
    return (f"{what} (Geograph photo {n}, subject location)", GEO + str(n))
places = [
    ORIG("barnet", "Barnet", "巴尼特", 51.6558, -0.2015, *G(369802, "Barnet High Street"),
         "The old market town on the Great North Road at London's northern edge, where Oliver, walking to London, meets the Artful Dodger",
         "伦敦北缘大北路上的老集镇，奥利弗步行去伦敦，在这里遇见了“机灵鬼”"),
    ORIG("cornhill", "Cornhill", "康希尔街", 51.5133, -0.0842, *G(1767459, "St Peter upon Cornhill, Cornhill"),
         "A street in the City of London, near the Bank of England and Scrooge's counting-house", "伦敦城的一条街，靠近英格兰银行，也就是斯克鲁奇账房所在的一带"),
    ORIG("orkney", "Orkney", "奥克尼群岛", 58.9870, -2.9674, *G(5726878, "Kirkwall, Orkney Mainland"),
         "The islands off the north coast of Scotland; Victor Frankenstein chooses one of the remotest of them. The marker is at Kirkwall, the main town",
         "苏格兰北岸外的群岛，维克多·弗兰肯斯坦选了其中最偏远的一个小岛。标记放在主城柯克沃尔", offshore_island=True),
    ORIG("exeter", "Exeter", "埃克塞特", 50.7225, -3.5299, "Exeter Cathedral (Commons photo 'Exeter (Devon, UK), Cathedral Church of Saint Peter -- 2013 -- 1417', object location)",
         COM + "File:Exeter_(Devon,_UK),_Cathedral_Church_of_Saint_Peter_--_2013_--_1417.jpg",
         "The cathedral city of Devon; the Dashwoods' Barton Cottage lies four miles north of it", "德文郡的大教堂城市；达什伍德一家住的巴顿小屋就在城北四英里", city=True),
    ORIG("bristol-harbour", "Bristol harbour", "布里斯托尔港", 51.4495, -2.6078, *G(1858154, "Floating Harbour, Bristol"),
         "The docks in the heart of Bristol, where the squire fits out the Hispaniola for Treasure Island", "布里斯托尔市中心的港口，乡绅在这里给“伊斯班袅拉号”装备出海"),
    ORIG("portland-place", "Portland Place", "波特兰坊", 51.5198, -0.1447, *G(4675256, "Portland Place, Central London"),
         "A broad street in Marylebone; Richard Hannay has a flat near it, where the story begins", "马里波恩区的一条宽街，理查德·汉内租的公寓就在附近，故事从这里开始"),
    ORIG("york", "York", "约克", 53.9623, -1.0825, "York Minster (Commons photo 'York Minster Nave 2, Nth Yorkshire, UK - Diliff', camera location)",
         COM + "File:York_Minster_Nave_2,_Nth_Yorkshire,_UK_-_Diliff.jpg",
         "The walled cathedral city of Yorkshire, where Robinson Crusoe is born in 1632", "约克郡有城墙的大教堂城市，鲁滨逊 1632 年生在这里", city=True),
    ORIG("emmanuel-college", "Emmanuel College, Cambridge", "剑桥 · 伊曼纽尔学院", 52.2036, 0.1238, "Emmanuel College (Commons photo 'Emmanuel College Front Court, Cambridge, UK - Diliff', camera location)",
         COM + "File:Emmanuel_College_Front_Court,_Cambridge,_UK_-_Diliff.jpg",
         "A Cambridge college founded in 1584, where Gulliver studies for three years from the age of fourteen", "剑桥的一所学院，1584 年创办；格列佛十四岁进这里读了三年书"),
    PROTO("coventry-middlemarch", "Coventry", "考文垂", 52.4083, -1.5077, *G(1065743, "Two spires, Coventry"),
          "Probably the model for Middlemarch: George Eliot lived in Coventry before moving to London, and like Middlemarch it was a silk-ribbon town",
          "很可能是米德尔马契的原型：乔治·艾略特去伦敦之前住在考文垂，这里和米德尔马契一样以丝带业为生"),
    PROTO("dorchester-casterbridge", "Dorchester", "多切斯特", 50.7152, -2.4385, *G(1834521, "Dorchester, View of High West Street"),
          "Hardy's home town, called Casterbridge in his novels", "哈代的家乡小城，在他的小说里叫卡斯特桥"),
    PROTO("great-maytham", "Great Maytham Hall, Rolvenden", "罗尔文登 · 大梅瑟姆庄园", 51.0450, 0.6344, *G(228928, "Great Maytham Hall Garden"),
          "Burnett lived here from 1898 to 1907 and found its walled garden of 1721 overgrown and neglected; it inspired The Secret Garden",
          "伯内特 1898 至 1907 年住在这里，发现庄园里建于 1721 年的围墙花园荒废多年、杂草丛生；《秘密花园》就由此而来"),
    PROTO("ashdown-pooh", "Poohsticks Bridge, Ashdown Forest", "阿什当森林 · 噗噗棍桥", 51.0854, 0.0977, *G(3937589, "Poohsticks Bridge"),
          "Ashdown Forest, where Milne walked with his son Christopher Robin, is the Forest of the stories, and its Five Hundred Acre Wood the Hundred Acre Wood. The marker is at Poohsticks Bridge, just outside the forest near Hartfield, where the Milnes had their country home at Cotchford Farm",
          "米尔恩常带儿子克里斯托弗·罗宾在阿什当森林散步，这里就是故事里的森林，林中的“五百英亩林”就是“百亩林”。标记放在森林外缘哈特菲尔德附近的噗噗棍桥，米尔恩家的乡间住所科奇福德农场就在旁边"),
    PROTO("menabilly", "Menabilly and Polridmouth, near Fowey", "福伊附近 · 梅纳比利", 50.3297, -4.6706, "Menabilly (Wikipedia)", W + "Menabilly",
          "Du Maurier discovered this hidden house as a teenager and later lived in it until 1969; with Milton Hall in Cambridgeshire it was the model for Manderley, which like Menabilly lay hidden in woods out of sight of the shore. The house is private; the photo shows Polridmouth cove below it",
          "杜穆里埃少女时代发现了这座藏在林中的宅子，后来在这里一直住到 1969 年；它和剑桥郡的米尔顿庄园一起成了曼陀丽的原型——曼陀丽也像它一样藏在树林里，从海边看不见。宅子是私产，照片拍的是宅子下面的波利德茅斯小海湾"),
    PROTO("sarehole-mill", "Sarehole Mill, Birmingham", "伯明翰 · 萨尔霍尔磨坊", 52.4341, -1.8558, "Sarehole Mill (Wikipedia), grid ref SP1005381833", W + "Sarehole_Mill",
          "Tolkien lived within a few hundred yards of this watermill as a small boy, and said he used it as the model for the Mill at Hobbiton; he called the countryside around it 'a kind of lost paradise'",
          "托尔金小时候就住在这座水磨坊几百码外，他说霍比屯的磨坊就是照它写的；他把这一带的乡野称作“一种失落的乐园”"),
    PROTO("rostrevor", "Rostrevor and Carlingford Lough", "罗斯特雷沃与卡林福德湾", 54.0943, -6.1830, *G(687576, "Rostrevor and Carlingford Lough"),
          "Lewis wrote to his brother that the part of Rostrevor overlooking Carlingford Lough was his idea of Narnia; he grew up in Belfast and also named the Mourne Mountains above it",
          "刘易斯在给哥哥的信里写道，罗斯特雷沃俯瞰卡林福德湾的那一带，就是他心中的纳尼亚；他在贝尔法斯特长大，也提到过这里背后的莫恩山"),
    PIL("hill-top-sawrey", "Hill Top, Near Sawrey", "近索里 · 山顶农场", 54.3517, -2.9705, "Hill Top, Cumbria (Wikipedia)", W + "Hill_Top,_Cumbria",
        "The farmhouse Beatrix Potter bought in 1905 with the money from her first books, Peter Rabbit among them; she left it to the National Trust, which opens it as a writer's house",
        "比阿特丽克斯·波特 1905 年买下的农舍；她把它留给了国民信托，现在作为作家故居开放", ["peter-rabbit"]),
]
PHOTOS = {
    "coventry-middlemarch": (0, "The spires of Holy Trinity and St Michael's, Coventry", "考文垂圣三一教堂和圣米迦勒教堂的尖塔"),
    "dorchester-casterbridge": (2, "High West Street, Dorchester", "多切斯特的高西街"),
    "great-maytham": (2, "The garden at Great Maytham Hall", "大梅瑟姆庄园的花园"),
    "ashdown-pooh": (2, "Poohsticks Bridge over a stream near Hartfield", "哈特菲尔德附近小溪上的噗噗棍桥"),
    "menabilly": (3, "Polridmouth, the cove and pool below Menabilly", "梅纳比利下方的波利德茅斯海湾和水塘"),
    "sarehole-mill": (3, "Sarehole Mill reflected in its mill pond", "倒映在磨坊水塘里的萨尔霍尔磨坊"),
    "rostrevor": (0, "Rostrevor and Carlingford Lough from the forest above", "从山上的林子里俯瞰罗斯特雷沃和卡林福德湾"),
    "hill-top-sawrey": (2, "Hill Top and its garden", "山顶农场和它的花园"),
}
cands = json.load(open(f"{PW}/candidates.json"))
for p in places:
    if p["id"] not in PHOTOS:
        continue
    n, en, zh = PHOTOS[p["id"]]
    c = cands[p["id"]]["candidates"][n]
    im = Image.open(f"{PW}/dl/{p['id']}__{n}.jpg").convert("RGB")
    if im.width > 800:
        im = im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS)
    assert im.width >= im.height, p["id"]
    rel = f"images/places/{p['id']}.jpg"
    im.save(f"{APP}/{rel}", "JPEG", quality=82, optimize=True, progressive=True)
    p["photo"] = {"file": rel, "width": im.width, "height": im.height, "author": c["author"].strip(), "license": c["license"].strip(),
                  "license_url": c["license_url"].strip(), "source": c["page"], "alt_en": en, "alt_zh": zh}

lines = [
    L("ot-1", "oliver-twist", "barnet", "Chapter 8", "第 8 章", prose(730, "Early on the seventh morning", "upon a door-step."), ["Barnet"], 730),
    L("cc-1", "christmas-carol", "cornhill", "Stave 1, Marley's Ghost", "第一节《马利的鬼魂》", prose(46, "The office was closed in a", "at blindman's-buff."), ["Cornhill"], 46),
    L("fr-1", "frankenstein", "oxford", "Chapter 19", "第 19 章", prose(84, "From thence we proceeded to Oxford.", "Parliament and liberty."), ["Oxford"], 84),
    L("fr-2", "frankenstein", "orkney", "Chapter 19", "第 19 章", prose(84, "With this resolution I traversed", "beaten upon by the waves."), ["Orkneys"], 84),
    L("mm-1", "middlemarch", "coventry-middlemarch", "Chapter 15", "第 15 章", prose(145, "Middlemarch, in fact, counted", "very comfortably."), ["Middlemarch"], 145),
    L("ss-1", "sense-and-sensibility", "exeter", "Chapter 5", "第 5 章", prose(161, "Edward turned hastily towards her", "northward of Exeter."), ["Exeter", "Devonshire"], 161),
    L("ff-1", "far-from-the-madding-crowd", "dorchester-casterbridge", "Chapter 40, On Casterbridge Highway", "第 40 章《卡斯特桥大道上》", prose(107, "When the woman awoke", "the woman turned her eyes."), ["Casterbridge"], 107),
    L("ti-1", "treasure-island", "bristol-harbour", "Chapter 6, The Captain's Papers", "第 6 章《船长的文件》", prose(120, '"Amount, sir!" cried the squire.', 'if I search a year."'), ["Bristol dock"], 120),
    L("jh-1", "jekyll-and-hyde", "soho", "The Carew Murder Case", "《卡鲁谋杀案》", prose(43, "The dismal\nquarter of Soho".replace("\n", " "), "of some city in a nightmare."), ["Soho"], 43),
    L("iv-1", "ivanhoe", "doncaster", "Chapter 1", "第 1 章", prose(82, "In that pleasant district of merry England", "the pleasant town of Doncaster."), ["Doncaster"], 82),
    L("tns-1", "thirty-nine-steps", "portland-place", "Chapter 1, The Man Who Died", "第 1 章《死去的人》", prose(558, "The night was fine and clear", "near Portland Place."), ["Portland Place"], 558),
    L("sg-1", "secret-garden", "great-maytham", "Chapter 9", "第 9 章", prose(113, "It was the sweetest, most mysterious-looking place", "matted together."), ["mysterious-looking place"], 113),
    L("rc-1", "robinson-crusoe", "york", "Chapter 1, Start in Life", "第 1 章《人生起步》", prose(521, "I was born in the year 1632", "settled first at Hull."), ["York"], 521),
    L("gt-1", "gullivers-travels", "emmanuel-college", "Part I, Chapter 1", "第一卷第 1 章", prose(829, "My father had a small estate in Nottinghamshire", "applied myself close to my studies"), ["Emanuel College in Cambridge"], 829),
    L("pooh-1", "winnie-the-pooh", "ashdown-pooh", "Chapter 4", "第 4 章", prose(67098, "Through copse and spinney marched Bear", "that Owl lived."), ["Hundred Acre Wood"], 67098),
]
def S(id, book, place, loc, loc_zh, en, zh, hl_en, hl_zh):
    for h in hl_en: assert h in en, (id, h)
    for h in hl_zh: assert h in zh, (id, h)
    return dict(id=id, kind="scene", book_id=book, place_ids=[place], location=loc, location_zh=loc_zh, text_en=en, text_zh=zh,
                highlight_en=hl_en, highlight_zh=hl_zh, status="draft")
lines += [
    S("reb-s1", "rebecca", "menabilly", "Chapter 1", "第 1 章",
      "The narrator dreams she has gone back to Manderley: the iron gates are locked, the drive has been swallowed by the woods, and when she reaches the house it stands silent in the moonlight, an empty shell.",
      "叙述者梦见自己又回到了曼陀丽：铁门上了锁，车道早被树林吞没；她走到尽头，那座房子在月光下静静立着，只剩一个空壳。",
      ["Manderley"], ["曼陀丽"]),
    S("hob-s1", "the-hobbit", "sarehole-mill", "Chapter 1", "第 1 章",
      "Bilbo Baggins lives comfortably in a hole dug into the Hill at Hobbiton, until Gandalf and thirteen dwarves turn up for tea and talk him into setting off on an adventure.",
      "比尔博·巴金斯在霍比屯小山下的洞府里过着安稳日子，直到甘道夫和十三个矮人上门喝茶，把他拉上了冒险的路。",
      ["Hobbiton"], ["霍比屯"]),
    S("lww-s1", "lion-witch-wardrobe", "rostrevor", "Chapter 1", "第 1 章",
      "Exploring the old professor's house, Lucy climbs into a wardrobe, pushes past the fur coats and finds herself standing in a snowy wood at night, beside a lamp-post: she has come into Narnia.",
      "露西在老教授家里探险，钻进一只衣橱，拨开一件件毛皮大衣，发现自己站在夜晚的雪林里，身边是一盏路灯——她来到了纳尼亚。",
      ["Narnia"], ["纳尼亚"]),
]
if __name__ == "__main__":
    append(f"{APP}/data/books.js", books, "11-04 夜 名著批：14 本公有领域；《小熊维尼》照《荒原》办法；3 本有版权的书只写场景说明")
    append(f"{APP}/data/places.js", places, "11-04 夜 名著批（坐标和照片均有出处）")
    append(f"{APP}/data/lines.js", lines, "11-04 夜 名著批：古登堡原文摘句和场景说明（草稿，待审核）")
    rows = [f"| {p['name']} | {p['photo']['author']} | [{p['photo']['license']}]({p['photo']['license_url']}) | [Commons]({p['photo']['source']}) |" for p in places if "photo" in p]
    cr = open(f"{APP}/docs/photo-credits.md", encoding="utf-8").read().rstrip("\n") + "\n" + "\n".join(rows) + "\n"
    open(f"{APP}/docs/photo-credits.md", "w", encoding="utf-8").write(cr)
    for l in lines:
        print(f"{l['id']:7}", l["text_en"][:150].replace("\n", " / "))
