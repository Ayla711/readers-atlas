"""11-27: North Macedonia, the book the user chose (tools/selection/mk.md): by selection rule v2 no Macedonian book qualifies
(no A list; the 2014 school-leaving exam canon and the post-1999 prizes never meet on one book; no book reaches 10,000
Goodreads ratings), and the user took Petre M. Andreevski's Pirej (1980) as an exception, as for Albania and Montenegro.
North Macedonia opens with this batch.
Place: the village of Jon and Velika is not named in the novel, only a small village in the mountains of Macedonia. Under the
rule for famous books it is hung at Sloeštica (Demir Hisar), the author's native village, where he grew up, where he is
buried, and where a memorial room for him opened in 2022 (honest note, prototype). The book is in copyright: a scene note.
Sources: https://en.wikipedia.org/wiki/Pirej; https://www.themodernnovelblog.com/?p=4012;
https://toniavramov.wordpress.com/2022/01/26/пиреј-петре-м-андреевски/; https://umno.mk/za-velikanot-petre-m-andreevski/;
https://zentralratdermakedonen.de/mk/романот-пиреј-од-петре-м-андреевски/ ; https://mk.wikipedia.org/wiki/Петре_М._Андреевски;
https://www.slobodenpecat.mk/nishto-ne-e-poprisutno-od-tvoeto-otsustvo-petre-m-andreevski-chovekot-shto-ni-go-podari-najubavoto-opevanje-na-ljubovta-kon-edna-zhena/
(memorial room, 2022); https://zenskimagazin.faktor.mk/na-rodenden-kaj-petre-m-andreevski-vo-sloeshtica-kje-go-chuvame-od-zaborav-likot-i-deloto-na-negovoto-velichie
(his grave in the village).
The map of North Macedonia (data/mk/geo.js) is the 8 statistical regions with their NUTS 3 codes, from geoBoundaries MKD
ADM1 (EuroGeographics and the State Statistical Office's NTES, CC BY 4.0; tools/eu-revision/mk_geo_build.py). Natural
Earth's 84 municipalities are the pre-2013 units, with wrong or missing region labels.
Photo: tools/content/batches/add_photos_mk_1127.py.
Usage: python3 -I tools/content/batches/add_mk1.py <app_dir> tools/content/batches/coords/add_mk1.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-27"
b.init(APP, "", "mk", DATE)
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]

books = [dict(id="pirej", title="Pirej (Couch Grass)", title_zh="偃麦草", title_orig="Пиреј", author="Petre M. Andreevski",
              author_zh="彼得雷·M·安德烈耶夫斯基", year="1980", orig_lang="mk", public_domain=False, source_url=None,
              author_orig="Петре М. Андреевски", aliases=["Пиреј", "Pirey", "Couch Grass", "Јон", "Велика", "Jon", "Velika"])]

places = [b.PROTO("mk-sloestica", "Sloeštica, Demir Hisar (Andreevski's native village)", "德米尔希萨尔 · 斯洛埃什蒂察（安德烈耶夫斯基家乡）", *C("mk-sloestica"),
    "The village of Jon and Velika in Pirej has no name in the novel: a small village in the mountains of Macedonia. Sloeštica, a hill village above the Crna in the Železnik area of Demir Hisar, is where Petre M. Andreevski was born in 1934 and went to school before the gymnasium in Bitola. He is buried here, and in 2022 a memorial room for him opened in the village. Under the rule for famous books the novel is hung at its author's native village",
    "《偃麦草》里约恩和韦利卡住的村子，书中没有名字，只说是马其顿山里的一个小村。斯洛埃什蒂察是德米尔希萨尔热列兹尼克地区、茨尔纳河畔山坡上的村子，彼得雷·M·安德烈耶夫斯基 1934 年生在这里，在村里读完小学才去比托拉上中学。他葬在村里，2022 年村里还开了一间他的纪念室。按“名著不漏”的规则，挂在作者的家乡")]

lines = [b.S("mk-pirej-1", "pirej", "mk-sloestica", "The novel as a whole", "全书",
    "The novel opens at Velika's funeral, attended by her son Roden Meglenoski, and then Jon and Velika, a couple from a small mountain village, tell their lives in alternating chapters through the Balkan Wars, the First World War and the years after. Armies come and go: Jon is pressed into the Serbian army while his brother Mirče serves in the Bulgarian one, and Velika, left alone, loses her five children one after another, most of them to cholera, and digs their graves herself. The title is couch grass, the weed that cannot be rooted out, and the novel's figure for a people that endures. Petre M. Andreevski was born at Sloeštica.",
    "小说从韦利卡的葬礼开场，她的儿子罗登·梅格莱诺斯基也在场；接着，住在一个小山村的约恩和韦利卡夫妇轮流讲述自己的一生，从巴尔干战争、第一次世界大战一直讲到战后。军队来了又走：约恩被抓去塞尔维亚军队，他的兄弟米尔切却在保加利亚军中；独自留下的韦利卡接连失去五个孩子，大多死于霍乱，是她亲手挖的坟。书名“偃麦草”是一种拔不尽的野草，小说用它比喻一个熬得下去的民族。彼得雷·M·安德烈耶夫斯基生在斯洛埃什蒂察。",
    ["Sloeštica"], ["斯洛埃什蒂察"],
    "https://en.wikipedia.org/wiki/Pirej; https://www.themodernnovelblog.com/?p=4012; https://toniavramov.wordpress.com/2022/01/26/пиреј-петре-м-андреевски/; https://umno.mk/za-velikanot-petre-m-andreevski/; https://mk.wikipedia.org/wiki/Петре_М._Андреевски")]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "books.js"))))
assert not {x["id"] for x in books} & all_books
assert {p["id"] for p in places} == set(CO)

HEAD = "// North Macedonia, hand-written content (tools/content/batches/add_mk1.py, 2026-11-27).\n"
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
