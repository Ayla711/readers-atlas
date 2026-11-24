"""11-24: Finland, second pack: books that selection rule v2 adds (tools/selection/fi.md), as far as their places are found.
All four are in copyright in Finland and get scene notes in our own words. Three villages or islands in them are invented or
unnamed, so the pin is the real place the sources tie them to (place type prototype): Urjala for Pentinkulma, the Pellinge
archipelago for the island of The Summer Book, Suomussalmi for the backwoods of The Red Line. My First Murder is set in Vuosaari.
Not yet added: True (Helsinki, no particular place found), Meek Heritage (the parish is left unnamed) and The Unknown Soldier
(its main places, such as Petrozavodsk, are now in Russia: where to hang it is for the user to decide). Not added, no real
place: Tales from Moominvalley, Mr Boo. No photos yet.

Usage: python3 -I tools/content/batches/add_fi2.py <app_dir> tools/content/batches/coords/add_fi2.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-24"
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]
def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, lang, aliases, pd=False, src=None):
    return dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
                orig_lang=lang, public_domain=pd, source_url=src, author_orig=author_orig, aliases=aliases)
def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
def check(books, places, lines):
    allb = set()
    for f in glob.glob(os.path.join(APP, "data", "*", "books.js")): allb |= ids_in(f)
    assert not {x["id"] for x in books} & allb, {x["id"] for x in books} & allb
    assert not {p["id"] for p in places} & ids_in(b.data("places.js")) and {p["id"] for p in places} == set(CO)
    assert not {l["id"] for l in lines} & ids_in(b.data("lines.js"))
    for l in lines:
        assert l["book_id"] in {x["id"] for x in books} and l["place_ids"][0] in {p["id"] for p in places}, l["id"]
    assert {l["book_id"] for l in lines} == {x["id"] for x in books}
    assert {l["place_ids"][0] for l in lines} == {p["id"] for p in places}
b.init(APP, "", "fi", DATE)
books = [
    BK("under-the-north-star", "Under the North Star", "北极星下", "Täällä Pohjantähden alla", "Väinö Linna", "瓦伊诺·林纳", "Väinö Linna",
       "1959–1962", "fi", ["Täällä Pohjantähden alla", "Here Beneath the North Star", "Pentinkulma", "Jussi Koskela", "Akseli Koskela", "Linna"]),
    BK("my-first-murder", "My First Murder", "我的第一桩谋杀案", "Ensimmäinen murhani", "Leena Lehtolainen", "莉娜·莱赫托莱宁", "Leena Lehtolainen",
       "1993", "fi", ["Ensimmäinen murhani", "Maria Kallio", "Lehtolainen"]),
    BK("the-summer-book", "The Summer Book", "夏日书", "Sommarboken", "Tove Jansson", "托芙·扬松", "Tove Jansson", "1972", "sv",
       ["Sommarboken", "Kesäkirja", "Sophia", "Jansson"]),
    BK("the-red-line", "The Red Line", "红线", "Punainen viiva", "Ilmari Kianto", "伊尔马里·基扬托", "Ilmari Kianto", "1909", "fi",
       ["Punainen viiva", "Topi Romppainen", "Riika", "Kianto"]),
]
places = [
    b.PROTO("fi-urjala", "Urjala, Pirkanmaa", "乌尔亚拉，皮尔卡区", *C("fi-urjala"),
            "Pentinkulma, the village of Väinö Linna's Under the North Star (1959–1962). The village is invented, but it lies in Häme and resembles Linna's home parish of Urjala, where he was born in 1920; a Väinö Linna tour in Urjala shows the landscape of the trilogy",
            "瓦伊诺·林纳《北极星下》（1959–1962）里的彭廷库尔马村。村子是虚构的，但它在海门地区，像林纳 1920 年出生的家乡乌尔亚拉；乌尔亚拉的“林纳之旅”带人去看三部曲里的风景"),
    b.ORIG("fi-vuosaari", "Vuosaari, Helsinki", "武奥萨里，赫尔辛基", *C("fi-vuosaari"),
           "Seaside district at the eastern edge of Helsinki. In Leena Lehtolainen's My First Murder (1993), the first Maria Kallio novel, a student choir's rehearsal weekend at a villa out here ends when one of the singers is found dead in the water by the shore",
           "赫尔辛基东缘的海滨城区。莉娜·莱赫托莱宁的《我的第一桩谋杀案》（1993）是玛丽亚·卡利奥系列的第一本：一个学生合唱团在这里的别墅排练周末，结果一名团员被发现死在岸边的水里"),
    b.PROTO("fi-pellinki", "Pellinki (Pellinge) archipelago, Porvoo", "佩林基群岛，波尔沃", *C("fi-pellinki"),
            "the islet of Tove Jansson's The Summer Book (1972), where the girl Sophia and her grandmother spend their summers. The book draws on the Jansson family's summers in the Pellinge archipelago off Porvoo, where they built a house on the islet of Bredskär in 1947",
            "托芙·扬松《夏日书》（1972）里的那座小岛，小女孩索菲亚和祖母在那里过夏天。书里写的是扬松一家在波尔沃外海佩林基群岛的夏天——1947 年，他们在布雷兹谢尔小岛上盖了房子"),
    b.PROTO("fi-suomussalmi", "Suomussalmi, Kainuu", "苏奥穆萨尔米，凯努区", *C("fi-suomussalmi"),
            "the backwoods of Ilmari Kianto's The Red Line (1909), where Topi and Riika Romppainen live with their children in the deep forests along the Russian border. Kianto lived most of his life in Suomussalmi and wrote about its people; the novel does not name a parish",
            "伊尔马里·基扬托《红线》（1909）里的偏远林区，托皮和里卡·龙派宁一家住在俄国边境的深林里。基扬托一生大半住在苏奥穆萨尔米，写的就是这里的人；小说没有点出是哪个教区"),
]
lines = [
    b.S("fi-pt-1", "under-the-north-star", "fi-urjala", "The trilogy as a whole", "三部曲全书",
        "A family of crofters and workers in the village of Pentinkulma, from the 1880s to the years after the Second World War. Volume one begins with Jussi Koskela clearing a swamp into a croft and runs to the eve of the First World War; volume two runs from that war to November 1919, through the Civil War of 1918; volume three reaches the Second World War and after.",
        "彭廷库尔马村里一个佃农和工人的家族，从 1880 年代写到二战之后。第一卷从尤西·科斯凯拉把一片沼泽开垦成佃农地写起，一直到第一次世界大战前夕；第二卷从那场大战写到 1919 年 11 月，其间是 1918 年的内战；第三卷写到第二次世界大战和战后。",
        ["Pentinkulma"], ["彭廷库尔马"],
        "https://snl.no/V%C3%A4in%C3%B6_Linna; https://bookbeat.com/dk/book/taalla-pohjantahden-alla-1-296678; https://bookbeat.com/mt/book/taalla-pohjantahden-alla-2-296676; https://visittampere.fi/en/destination/vaino-linna-tour/"),
    b.S("fi-mf-1", "my-first-murder", "fi-vuosaari", "The case", "案件",
        "Maria Kallio, a 23-year-old law student taken on for a temporary post with the Helsinki police, gets her first murder case: a student choir's lively rehearsal weekend at a villa in Vuosaari is cut short when the first bass is found dead in the water off the shore. The dead man is someone from her own past.",
        "二十三岁的法律系学生玛丽亚·卡利奥临时进了赫尔辛基警局，接手了她的第一桩谋杀案：一个学生合唱团在武奥萨里的别墅里热热闹闹地排练度周末，第一男低音却被发现死在岸边的水里。死者是她过去认识的人。",
        ["Vuosaari"], ["武奥萨里"],
        "https://www.goodreads.com/book/show/18720575; https://www.prisma.fi/tuotteet/110380388/lehtolainen-ensimmainen-murhani-maria-kallio-1-110380388; https://www.publishersweekly.com/9781612184371; https://complete-review.com/reviews/trcrime/lehtoll.htm"),
    b.S("fi-sb-1", "the-summer-book", "fi-pellinki", "The book as a whole", "全书",
        "Short chapters about one summer after another on a small island in the Gulf of Finland, where the little girl Sophia and her grandmother spend the summers together, with her father in the background. The two are Tove Jansson's niece Sophia and her own mother, Ham, on the family's islet in the Pellinge archipelago; Sophia's mother is not in the book.",
        "一篇篇短章，写芬兰湾一座小岛上的一个又一个夏天：小女孩索菲亚和祖母一起度过一个个夏天，父亲只是个配角。这两人就是托芙·扬松的侄女索菲亚和扬松自己的母亲哈姆，地点是一家人在佩林基群岛的小岛；书里没有索菲亚的母亲。",
        ["Pellinge"], ["佩林基"],
        "https://yle.fi/a/7-10083222; https://www.inkl.com/news/travels-in-moominland-summer-in-tove-jansson-s-finland; https://visitpellinge.fi/en/tove-jansson/"),
    b.S("fi-rl-1", "the-red-line", "fi-suomussalmi", "The novel as a whole", "全书",
        "Topi and Riika Romppainen and their children live in poverty in the deep forests along the Russian border. In 1907, the year of the first Finnish parliamentary election, held after the general strike of 1905, social democratic agitators come to the backwoods and and their propaganda takes hold of Topi and Riika, whom the gentry have always called lazy. Kianto wrote about the people of Suomussalmi, where he lived.",
        "托皮和里卡·龙派宁带着一群孩子，穷困地住在俄国边境的深林里。1907 年，1905 年大罢工之后芬兰举行第一次议会选举，社会民主党的鼓动者来到这片林区，他们的宣传打动了一向被老爷们骂作懒汉的托皮和里卡。基扬托写的，就是他所住的苏奥穆萨尔米的人。",
        ["Suomussalmi"], ["苏奥穆萨尔米"],
        "https://caponeu.ffzg.unizg.hr/cdp/novels/punainen-viiva; https://en.wikipedia.org/wiki/The_Red_Line; https://viakarelia.fi/en/themes/military-history/winter-war-30-november-1939-13-march-1940/battles-in-suomussalmi-30-november-1939-7-january-1940/ilmari-kianto-turjanlinna-and-the-winter-war/; https://jyx.jyu.fi/bitstreams/0c5018ed-e11a-4187-9ed3-88f16091d439/download"),
]
check(books, places, lines)
if __name__ == "__main__":
    M = "11-24: second pack, books added under selection rule v2 (tools/content/batches/add_fi2.py)"
    b.append(b.data("books.js"), books, M); b.append(b.data("places.js"), places, M); b.append(b.data("lines.js"), lines, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
