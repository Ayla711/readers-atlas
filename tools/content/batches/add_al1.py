"""11-25: Albania. Under selection rule v2 no Albanian book qualifies (tools/selection/al.md); the user chose to add the
single most famous and influential one, The General of the Dead Army (1963), Kadare's first novel and the book that
made him known abroad. It is in copyright: a scene note in our own words. The novel's villages and battlefields are not
named in the sources we can check; its opening chapter takes the Italian general from Tirana airport to the Hotel
Dajti in Tirana (first chapter as published in the Spanish and German editions' online samples), a real building, so
the book is pinned there.
Usage: python3 -I tools/content/batches/add_al1.py <app_dir> tools/content/batches/coords/add_al1.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-25"
b.init(APP, "", "al", DATE)
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]

books = [dict(id="general-of-the-dead-army", title="The General of the Dead Army", title_zh="亡军的将领", title_orig="Gjenerali i ushtrisë së vdekur",
              author="Ismail Kadare", author_zh="伊斯梅尔·卡达莱", year="1963", orig_lang="sq", public_domain=False, source_url=None,
              aliases=["Gjenerali i ushtrisë së vdekur", "Le Général de l'armée morte"])]

places = [
    b.ORIG("al-hotel-dajti", "Hotel Dajti, Tirana", "地拉那的达伊蒂饭店", *C("al-hotel-dajti"),
        "The former Hotel Dajti on Dëshmorët e Kombit Boulevard in central Tirana, built in the 1930s by the Italian architect Gherardo Bosio and the designer Gio Ponti. Under the socialist regime it was the hotel for foreign visitors and diplomats, its rooms bugged. In The General of the Dead Army the Italian general is driven here from the airport when he arrives in Albania",
        "地拉那市中心民族烈士大道上原来的达伊蒂饭店，20 世纪 30 年代由意大利建筑师格拉尔多·博西奥和设计师吉奥·庞蒂建造。社会主义时期这里专门接待外国客人和外交官，房间里装着窃听器。《亡军的将领》里，意大利将军一到阿尔巴尼亚，就从机场被送到这里"),
]

lines = [
    b.S("al-gd-1", "general-of-the-dead-army", "al-hotel-dajti", "Arrival in Tirana", "到达地拉那",
        "Some twenty years after the Second World War, an Italian general, accompanied by a priest who is also an army colonel, is sent to Albania to find the remains of the Italian soldiers who fell there and bring them home for burial. Met at the airport, they are driven into Tirana; at the Hotel Dajti the general feels in good spirits, changes his uniform and books a telephone call to his family. Then, with lists of names and maps, they go out into the Albanian countryside in rain and sleet, digging up old battlefields, and find that a German general is doing the same for his own dead.",
        "第二次世界大战过去大约二十年，一位意大利将军带着一个同时是陆军上校的神父被派到阿尔巴尼亚，要找回死在那里的意大利士兵的遗骨，运回国安葬。他们在机场被接上车，开进地拉那；到了达伊蒂饭店，将军心情好了起来，换了军装，在前台挂了一个打回家里的长途电话。随后他们带着名单和地图走进阿尔巴尼亚的乡间，在雨雪里挖开从前的战场，并发现一位德国将军也在为自己的阵亡士兵做同样的事。",
        ["Tirana", "Hotel Dajti"], ["地拉那", "达伊蒂饭店"],
        "https://en.wikipedia.org/wiki/The_General_of_the_Dead_Army_(novel); https://www.alianzaeditorial.es/primer_capitulo/el-general-del-ejercito-muerto.pdf; https://www.powells.com/book/general-of-the-dead-army-a-novel-9781611454185"),
]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set()
for f in glob.glob(os.path.join(APP, "data", "*", "books.js")):
    all_books |= ids_in(f)
assert not {x["id"] for x in books} & all_books
assert {x["id"] for x in places} == set(CO)

HEAD = "// Albania, hand-written content (tools/content/batches/add_al1.py, 2026-11-25).\n"
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
