"""11-26: Slovakia, the 2 books the user chose: the two Slovak works in the top 10 of Slovak Television's 2010 viewers' poll
"Moja naj kniha" (tools/selection/sk.md), plus one line for a book already in the app (A Time of Gifts, data/at), which
qualifies by the rule and which the user chose to hang at Štúrovo. Slovakia opens with this batch. Places, with the reason
for each:
- Drienčany (Rimavská Sobota) for Dobšinský's Slovak tales: the tales have no real places, so under the rule for famous
  books the collection is hung where Dobšinský was pastor from 1861 to his death in 1885 and where he lies buried. The
  book is in the public domain, but no line of it names Drienčany, so the line is a scene note.
- Bratislava for Ja, malkáč: the sources we read do not name the town where the book's family lives; it is hung at the
  author's native city, with an honest note. In copyright: a scene note.
- Štúrovo for A Time of Gifts: the book ends on the Mária Valéria Bridge between Štúrovo (then Parkan, Párkány) and
  Esztergom. The bridge's own coordinates fall mid-stream on the Hungarian side, so the place uses the town's. In
  copyright: a scene note. The book stays in data/at; the place and the line go into data/sk.
The map of Slovakia (data/sk/geo.js) is Natural Earth's eight self-governing regions (kraje).
Usage: python3 -I tools/content/batches/add_sk1.py <app_dir> tools/content/batches/coords/add_sk1.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-26"
b.init(APP, "", "sk", DATE)
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]

books = [
    dict(id="prostonarodne-slovenske-povesti", title="Slovak Folk Tales", title_zh="斯洛伐克民间故事",
         title_orig="Prostonárodné slovenské povesti", author="Pavol Dobšinský", author_zh="帕沃尔·多布欣斯基", year="1880–1883",
         orig_lang="sk", public_domain=True, source_url="https://sk.wikisource.org/wiki/Prostonárodné_slovenské_povesti",
         aliases=["Slovenské rozprávky", "Prostonárodné slovenské povesti", "Zlatá kniha rozprávok Pavla Dobšinského", "Slovenské povesti", "Dobšinský"]),
    dict(id="ja-malkac", title="I, the Little One", title_zh="我，小不点", title_orig="Ja, malkáč",
         author="Ľubo Dobrovoda", author_zh="柳博·多布罗沃达", year="2005", orig_lang="sk", public_domain=False, source_url=None,
         aliases=["Ja malkáč", "Ja, malkáč", "Román smutno-srandovinový", "malkáč"]),
]

places = [
    b.ORIG("sk-driencany", "Drienčany", "德里恩恰尼", *C("sk-driencany"),
        "A village in Gemer, in Rimavská Sobota district, where Pavol Dobšinský was the Lutheran pastor from 1861 until his death in 1885; his tombstone stands in the walled grounds of its Lutheran church, among those of the village's pastors. His Slovak folk tales name no real places; under the rule for famous books the collection is hung here, where he lived and worked while he brought it out",
        "盖梅尔地区里马夫斯卡索博塔县的一个村子，帕沃尔·多布欣斯基 1861 年起在这里当路德宗牧师，直到 1885 年去世；他的墓碑立在村里路德宗教堂带围墙的院子里，和历任牧师的墓碑在一起。他整理的斯洛伐克民间故事里没有真实地名；按“名著不漏”的规则，这部故事集挂在他编成它时生活和工作的地方"),
    b.ORIG("sk-bratislava", "Bratislava", "布拉迪斯拉发", *C("sk-bratislava"),
        "The capital of Slovakia, where Ľubo Dobrovoda was born in 1962, to a Czech mother and a Slovak father. Ja, malkáč tells of a Czech–Slovak family like his own, but the sources we read do not name the town where the book's family lives; under the rule for famous books it is hung at the author's native city",
        "斯洛伐克首都，柳博·多布罗沃达 1962 年生在这里，母亲是捷克人，父亲是斯洛伐克人。《我，小不点》写的也是这样一个捷克—斯洛伐克家庭，但我们读到的资料没有写出这家人住在哪个城市；按“名著不漏”的规则，挂在作者出生的城市"),
    b.ORIG("sk-sturovo", "Štúrovo (Mária Valéria Bridge)", "什图罗沃（玛丽亚·瓦莱里娅桥）", *C("sk-sturovo"),
        "A town on the Danube opposite Esztergom, Párkány in Hungarian; its official Slovak name was Parkan until it was renamed after Ľudovít Štúr in 1948. The Mária Valéria Bridge, opened in 1895, joins it to Esztergom; since the Treaty of Trianon the border runs mid-stream. A Time of Gifts ends on this bridge",
        "多瑙河边与匈牙利埃斯泰尔戈姆隔河相望的小城，匈牙利语叫帕尔卡尼；斯洛伐克语的正式名称原是帕尔坎，1948 年改为纪念卢德维特·什图尔的今名。1895 年建成的玛丽亚·瓦莱里娅桥把它和埃斯泰尔戈姆连在一起；《特里亚农条约》之后，国界就在河中央。《时光的礼物》在这座桥上结束"),
]

lines = [
    b.S("sk-dob-1", "prostonarodne-slovenske-povesti", "sk-driencany", "The collection as a whole", "全集",
        "Prostonárodné slovenské povesti, ninety tales in eight issues (1880–1883), is the core of what Slovaks know as Dobšinský's tales; with A. H. Škultéty he had already brought out Slovenské povesti, 64 tales in six issues (1858–1861). He wrote down songs, proverbs, riddles, games, customs and beliefs as well as tales, and before printing them he took out their original eroticism and earthy humour, which is how stories first told to adults became children's favourites. He brought out the collection in his years as pastor of Drienčany. In 2010 Slovak viewers voted 'Dobšinský's tales' their favourite book in Slovak Television's poll Moja naj kniha.",
        "《斯洛伐克民间故事》（1880–1883）共八册、九十篇，是斯洛伐克人所说的“多布欣斯基童话”的主体；此前他已和什库尔泰蒂合编过《斯洛伐克故事》（1858–1861），六册六十四篇。除了故事，他还记录民歌、谚语、谜语、游戏、风俗和迷信；故事付印前，他删去了原本的情色成分和粗俗的笑料，本来讲给大人听的故事就这样成了孩子们最爱读的书。这部故事集是他在德里恩恰尼当牧师的那些年里出版的。2010 年斯洛伐克电视台“我最爱的书”观众投票，“多布欣斯基童话”得了第一。",
        ["Drienčany"], ["德里恩恰尼"],
        "https://sk.wikipedia.org/wiki/Pavol_Dobšinský; https://sk.wikipedia.org/wiki/Drienčany; https://onas.martinus.sk/blog/2010/11/vitazom-ankety-moja-naj-kniha-sa-stava"),
    b.S("sk-mal-1", "ja-malkac", "sk-bratislava", "The novel as a whole", "全书",
        "Subtitled 'a sad-and-funny novel', Ja, malkáč is told by a five-year-old boy watching his Czechoslovak family at the end of the 1960s: a father who drinks and turns violent, a mother who goes back to Bohemia, a domineering grandmother. He loves them all and cannot accept that they no longer live as a family, while working out whether he is Czech or Slovak. Ľubo Dobrovoda, born in Bratislava in 1962 to a Czech mother and a Slovak father, published it at his own expense in 2005; Prague's Divadlo v Řeznické staged it in 2009, and it came second in Slovak Television's 2010 poll Moja naj kniha. The sources we read do not name the town where the family lives.",
        "这部副题为“又悲又好笑的小说”的书，由一个五岁男孩讲他 1960 年代末的捷克斯洛伐克家庭：父亲酗酒、动手打人，母亲回了波希米亚，祖母专横跋扈。他爱他们每一个，却接受不了一家人再也不能一起生活，同时还要弄明白自己到底是捷克人还是斯洛伐克人。柳博·多布罗沃达 1962 年生在布拉迪斯拉发，母亲是捷克人，父亲是斯洛伐克人；他 2005 年自费出版了这本书，2009 年布拉格的雷兹尼茨卡剧院把它搬上舞台，2010 年斯洛伐克电视台“我最爱的书”投票中它排第二。我们读到的资料没有写出这家人住在哪个城市。",
        ["Bratislava"], ["布拉迪斯拉发"],
        "https://www.litcentrum.sk/autor/lubo-dobrovoda; https://www.sme.sk/c/3087569/spisovatel-lubo-dobrovoda-mam-rad-slovenske-fanfaronstvo.html; https://bookbot.com/a/243367; https://www.i-divadlo.cz/divadlo/divadlo-v-reznicke/ja-malkac-dvr; https://www.goodreads.com/author/show/4614512._ubo_Dobrovoda"),
    b.S("sk-fermor-1", "at-time-of-gifts", "sk-sturovo", "The last pages", "全书结尾",
        "On Holy Saturday 1934, four months after setting out from the Hook of Holland, the nineteen-year-old Leigh Fermor stands in the middle of the bridge from Párkány, today Štúrovo, looking across the Danube at Esztergom and its great cathedral, the seat of Hungary's primate. A Time of Gifts ends here, in mid-stream; the second volume, Between the Woods and the Water, begins with his crossing into Hungary. The bridge he stood on was blown up by retreating German troops in December 1944 and was not rebuilt until 2001.",
        "1934 年复活节前的圣星期六，从荷兰角港出发四个月后，十九岁的利·弗莫尔站在从帕尔卡尼（今天的什图罗沃）伸出去的大桥中央，隔着多瑙河望向埃斯泰尔戈姆和那座匈牙利首席主教的大教堂。《时光的礼物》就在这里、在河中央结束；第二卷《林木与流水之间》从他走进匈牙利开始。他当年站过的那座桥 1944 年 12 月被撤退的德军炸毁，直到 2001 年才重建通车。",
        ["Štúrovo"], ["什图罗沃"],
        "https://cdn.waterstones.com/special/pdf/9780719566967.pdf; https://en.wikipedia.org/wiki/Mária_Valéria_Bridge; https://patrickleighfermor.org/2010/04/04/easter-1934-paddy-reaches-the-hungarian-border-at-esztergom/; https://en.wikipedia.org/wiki/Štúrovo"),
]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set()
for f in glob.glob(os.path.join(APP, "data", "*", "books.js")):
    all_books |= ids_in(f)
new_b, new_p = {x["id"] for x in books}, {x["id"] for x in places}
assert len(books) == 2 and not new_b & all_books, new_b & all_books
assert "at-time-of-gifts" in ids_in(os.path.join(APP, "data", "at", "books.js"))
assert new_p == set(CO), new_p ^ set(CO)
for l in lines:
    assert l["book_id"] in new_b | {"at-time-of-gifts"} and l["place_ids"][0] in new_p, l["id"]
assert {l["place_ids"][0] for l in lines} == new_p

HEAD = "// Slovakia, hand-written content (tools/content/batches/add_sk1.py, 2026-11-26).\n"
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
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
