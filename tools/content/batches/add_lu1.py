"""11-27: Luxembourg, the books the user chose (tools/selection/lu.md): by selection rule v2 two Luxembourgish novels
qualify, both on the national lists and in the lycée reader, and the user took just these two. Luxembourg opens with this
batch. Places, with the reason for each:
- Esch-sur-Alzette for Jhemp Hoscheit's Perl oder Pica (1998): the novel is set in Esch in 1962-63, a twelve-year-old
  Esch boy's world, drawn from the author's own childhood there (Luxemburger Autorenlexikon). In copyright: a scene note.
- Dreiborn for Tullio Forgiarini's Amok (2011): the novel names neither the narrator's village nor his school; the real
  place it keeps returning to is Dreiborn, the state home for boys placed by the youth court, which the fifteen-year-old
  dreads being sent to (opening chapters, read in the Serbian translation's published extract). Hung here under A-24,
  with that said in the place note. In copyright: a scene note.
Sources: https://www.autorenlexikon.lu/page/author/510/5107/DEU/index.html; https://www.lovelybooks.de/autor/Jhemp-Hoscheit/;
https://luxembourg.public.lu/en/society-and-culture/artistic-creation/national-literary-competition-jhemp-hoscheit.html;
https://www.forum.lu/2019/07/07/forum_c-pol-cruchten-1963-2019/; https://m.imdb.com/title/tt0468834/;
https://lb.wikipedia.org/wiki/Perl_oder_Pica_(Film); http://www.videotheken-online.net/kleine-geheimnisse-perl-oder-pica/;
https://joel.lu/2006/10/26/perl-oder-pica/; https://www.c2dh.uni.lu/sites/default/files/8_wou_holz_net_mei_schwaetzt_jhemp_hoscheit.pdf;
https://odiseja.co.rs/__public/upload/2020/06/09/amok.pdf (extract of the Serbian translation, pp. 7-22);
https://euprizeliterature.eu/author/tullio-forgiarini; https://www.camelozampa.com/en/creative-europe/amok-en/;
https://www.autorenlexikon.lu/page/author/763/763/DEU/index.html; https://en.wikipedia.org/wiki/Tullio_Forgiarini;
https://men.public.lu/dam-assets/catalogue-publications/dossiers-de-presse/2017-2018/centre-socio-educatif-de-letat.pdf;
https://gouvernement.lu/fr/actualites/toutes_actualites/communiques/2017/11-novembre/07-centre-socio-educatif.html;
https://lb.wikipedia.org/wiki/Dräibuer
The map of Luxembourg (data/lu/geo.js) is the 12 cantons of geoBoundaries LUX ADM1 (OpenStreetMap via Wambacher, ODbL 1.0;
tools/eu-revision/lu_geo_build.py).
Photos: tools/content/batches/add_photos_luva_1127.py.
Usage: python3 -I tools/content/batches/add_lu1.py <app_dir> tools/content/batches/coords/add_lu1.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-27"
b.init(APP, "", "lu", DATE)
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]

books = [
    dict(id="perl-oder-pica", title="Perl oder Pica", title_zh="珍珠体还是派卡体", title_orig="Perl oder Pica", author="Jhemp Hoscheit",
         author_zh="杰姆·霍沙伊特", year="1998", orig_lang="lb", public_domain=False, source_url=None,
         author_orig="Jhemp Hoscheit", aliases=["Jean-Pierre Hoscheit", "Kleine Geheimnisse", "Petits secrets", "Norbi Welscheid"]),
    dict(id="amok-forgiarini", title="Amok: A Luxembourg Love Story", title_zh="狂乱：卢森堡爱情纪事", title_orig="Amok. Eng Lëtzebuerger Liebeschronik",
         author="Tullio Forgiarini", author_zh="图利奥·福尔贾里尼", year="2011", orig_lang="lb", public_domain=False, source_url=None,
         author_orig="Tullio Forgiarini", aliases=["Amok", "Amok. Eng Lëtzebuerger Liebeschronik", "Baby(a)lone"]),
]

places = [
    b.ORIG("lu-esch", "Esch-sur-Alzette", "阿尔泽特河畔埃施", *C("lu-esch"),
        "Luxembourg's second town, in the south-west on the French border, in the valley of the Alzette: the iron and steel town of the Minett, the ore country of the south. Jhemp Hoscheit was born here in 1951, went to the Lycée de garçons here and later taught at it. His novel Perl oder Pica (1998), drawn from his own childhood, is set in the Esch of 1962-63, and Pol Cruchten filmed it in the town in 2005, near the house Hoscheit grew up in",
        "卢森堡第二大城，在西南部阿尔泽特河谷，紧挨法国边境，是南部铁矿区“米内特”的钢铁城。杰姆·霍沙伊特 1951 年生在这里，在这里的男子中学读书，后来又回这所学校教书。他的小说《珍珠体还是派卡体》（1998）取材于自己的童年，写的就是 1962–63 年的埃施；2005 年波尔·克鲁赫滕把它拍成电影，就在城里、霍沙伊特长大的那栋房子附近取景"),
    b.ORIG("lu-dreiborn", "Dreiborn, the Centre socio-éducatif de l'État", "德赖博恩 · 国立社会教育中心", *C("lu-dreiborn"),
        "A hamlet in the commune of Wormeldange, near the Moselle, home chiefly to the Centre socio-éducatif de l'État, the state's home for minors entrusted to it by the youth court: boys here, girls at Schrassig, and since 2017 a closed security unit for up to twelve. In Tullio Forgiarini's Amok it is where the fifteen-year-old narrator dreads being sent. The novel names neither his village nor his school, so Dreiborn, which it keeps coming back to, is its nearest real place",
        "沃尔梅尔当日市镇的一个小村，靠近摩泽尔河，村里主要是国立社会教育中心：由少年法庭把未成年人交托给它的国家机构，男孩在这里，女孩在施拉西格，2017 年起还有一个最多收十二人的封闭安全单元。在图利奥·福尔贾里尼的《狂乱》里，这是十五岁的主人公最怕被送去的地方。小说没有写出他住的村子和上的学校的名字，书里反复提到的德赖博恩就是离它最近的真实地点"),
]

lines = [
    b.S("lu-pop-1", "perl-oder-pica", "lu-esch", "The novel as a whole", "全书",
        "Hoscheit's first novel, partly autobiographical, tells the world of a twelve-year-old boy of Esch, Norbi Welscheid, in 1962-63, in the year of the Cuban missile crisis. It draws on the author's own childhood in Esch in the fifties and sixties: a strict, Catholic upbringing in a town where the war and the Nazi occupation were still close, and where nobody explained war or sex to children. An aunt from America in it is drawn from the writer Margrit Schuler, his godmother. The novel won the Servais Prize in 1999 and began a trilogy on Esch in the 1960s, with Wootleche Krich (set in 1965) and Aacht Deeg an der Woch (May 1968). Pol Cruchten filmed it in Esch in 2005, with Hoscheit's son Ben as Norbi; the title names two typewriter typefaces of the time.",
        "这是霍沙伊特的第一部小说，带有自传色彩，写埃施一个十二岁男孩诺尔比·韦尔沙伊德在 1962–63 年、古巴导弹危机那一年里的世界。它取材于作者自己五六十年代在埃施的童年：严厉的天主教家教，战争和纳粹占领的记忆还近在眼前，没有人向孩子解释战争，也没有人解释性。书里那位从美国来的姨妈，原型是作家玛格丽特·舒勒，霍沙伊特的教母。小说 1999 年获塞尔瓦伊奖，并由此展开一部写六十年代埃施的三部曲，后两部是《Wootleche Krich》（写 1965 年）和《Aacht Deeg an der Woch》（《一周八天》，写 1968 年 5 月）。2005 年波尔·克鲁赫滕在埃施把它拍成电影，由霍沙伊特的儿子本饰演诺尔比；书名是当年打字机上的两种字体。",
        ["Esch"], ["埃施"],
        "https://www.autorenlexikon.lu/page/author/510/5107/DEU/index.html; https://www.lovelybooks.de/autor/Jhemp-Hoscheit/; https://luxembourg.public.lu/en/society-and-culture/artistic-creation/national-literary-competition-jhemp-hoscheit.html; https://www.forum.lu/2019/07/07/forum_c-pol-cruchten-1963-2019/; https://m.imdb.com/title/tt0468834/; https://joel.lu/2006/10/26/perl-oder-pica/"),
    b.S("lu-amok-1", "amok-forgiarini", "lu-dreiborn", "The opening chapters", "开头几章",
        "Forgiarini's first novel in Luxembourgish is told to a fifteen-year-old, in the second person, by a voice like an alter ego. He lives with his mother Sandra in a converted barn at the edge of a village, having moved from a flat in Pétange. After he attacks a classmate, a school council weighs sending him to Dreiborn, where friends who have been there say newcomers are always beaten; instead he and his mother sign him up for six weeks in a school \"time-out\" unit, and he tells himself that anything is better than Dreiborn. In the unit he meets a girl who says Dreiborn is bad but the youth psychiatric ward at Kirchberg is far worse. In seventeen short chapters, in often crude language with dream sequences, the novel follows his search for love and a place in society; it won the European Union Prize for Literature in 2013 and was filmed as Baby(a)lone.",
        "这是福尔贾里尼第一部用卢森堡语写的小说，用第二人称、由一个像是另一个自我的声音，讲给一个十五岁的少年听。他和母亲桑德拉住在村边一座改建的谷仓里，之前住在佩唐日的一套公寓。他袭击了一个同学之后，学校开会讨论要不要把他送去德赖博恩——去过的朋友说，新来的人总要挨打；最后他和母亲签字，让他去学校的“暂停”单元待六周，他心想，什么都比德赖博恩强。在那个单元里，他认识了一个女孩，她说德赖博恩已经够糟，基希贝格的青少年精神科病房还要糟得多。小说分十七个短章，语言常常粗野，穿插着梦境，写他寻找爱和自己在社会中的位置；2013 年获欧盟文学奖，后来拍成电影《Baby(a)lone》。",
        ["Dreiborn"], ["德赖博恩"],
        "https://odiseja.co.rs/__public/upload/2020/06/09/amok.pdf; https://euprizeliterature.eu/author/tullio-forgiarini; https://www.camelozampa.com/en/creative-europe/amok-en/; https://www.autorenlexikon.lu/page/author/763/763/DEU/index.html"),
]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "books.js"))))
assert not {x["id"] for x in books} & all_books
assert {p["id"] for p in places} == set(CO)

HEAD = "// Luxembourg, hand-written content (tools/content/batches/add_lu1.py, 2026-11-27).\n"
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
