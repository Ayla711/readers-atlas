"""11-27: Slovenia, one book more, at the user's request (tools/selection/si.md, "破例收"): Paulo Coelho's Veronika Decides
to Die (Veronika decide morrer, 1998), whose heroine lives in Ljubljana. The book has only one class of evidence
(Goodreads, 251,511 ratings), so it comes in as an exception, the user's choice.
Place: Prešeren Square, Ljubljana. From her rented room in a convent Veronika looks out on the small central square with
its statue of the poet; the novel names the statue as Prešeren's and tells how his gaze rests on the face of Julija carved
on a house across the square. The asylum, Villete, is invented, so it is not on the map. The book is in copyright: a scene
note in our own words.
Sources: https://en.wikipedia.org/wiki/Veronika_Decides_to_Die; https://litres.com/paulo-coelho/veronika-decides-to-die/read-online/
(the publisher's preview of the English translation, opening chapter); https://www.researchgate.net/publication/372348288
(a study quoting the Prešeren passage); https://en.wikipedia.org/wiki/Prešeren_Square;
https://en.wikipedia.org/wiki/Prešeren_Monument_(Ljubljana); https://www.ljubljana.si/en/news/preseren-square
Photo: tools/content/batches/add_photos_si_1127b.py.
Usage: python3 -I tools/content/batches/add_si2.py <app_dir> tools/content/batches/coords/add_si2.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-27"
b.init(APP, "", "si", DATE)
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]

books = [dict(id="veronika-decides-to-die", title="Veronika Decides to Die", title_zh="维罗妮卡决定去死",
              title_orig="Veronika decide morrer", author="Paulo Coelho", author_zh="保罗·柯艾略", year="1998", orig_lang="pt",
              public_domain=False, source_url=None, author_orig="Paulo Coelho",
              aliases=["Veronika decide morrer", "Veronika", "Villete", "Coelho", "维罗尼卡决定去死"])]

places = [b.ORIG("si-preseren-square", "Prešeren Square (Prešernov trg), Ljubljana", "卢布尔雅那 · 普雷舍伦广场", *C("si-preseren-square"),
    "Ljubljana's central square, at the Triple Bridge over the Ljubljanica, with the Franciscan Church of the Annunciation. The bronze statue of the national poet France Prešeren (1905) stands on its east side; across the square a likeness of Julija Primic, the woman he loved and could not marry, looks back at him from a house front in Wolfova ulica. In Veronika Decides to Die Veronika looks down on this square and its statue of the poet from her convent room, and the novel tells the story of Prešeren's gaze",
    "卢布尔雅那的中心广场，在卢布尔雅尼察河的三重桥边，旁边是方济各会天使报喜教堂。广场东侧立着国家诗人弗兰策·普雷舍伦的青铜像（1905 年）；广场对面沃尔夫街一栋房子的外墙上，有他爱而不得的尤利娅·普里米茨的像，与他遥遥相望。《维罗妮卡决定去死》里，维罗妮卡从修道院的房间往下看的就是这个立着诗人雕像的广场，小说也讲了普雷舍伦凝望的故事")]

lines = [b.S("si-vdd-1", "veronika-decides-to-die", "si-preseren-square", "The opening chapter, and the novel as a whole", "开篇一章，及全书",
    "Veronika, 24, a librarian in Ljubljana, lives in a rented room in a convent. On the morning of 11 November 1997 she swallows sleeping pills there. While she waits to die she reads a magazine article that opens by asking where Slovenia is, and looks out of her window at the small central square with its statue of the poet: Prešeren, whose eyes rest, across the square, on the face of his unattainable Julija carved on a house front. A stranger once gave her a flower in the middle of that square. She wakes in Villete, an asylum Coelho invented, and is told she has only days to live. Drawing on his own time in mental hospitals, Coelho makes the book a question of what makes a life worth living.",
    "24 岁的维罗妮卡是卢布尔雅那的图书馆员，租住在一座修道院的房间里。1997 年 11 月 11 日早上，她在房里吞下安眠药。等死的时候，她读到一篇开头就问“斯洛文尼亚在哪里”的杂志文章，又望向窗外那个立着诗人雕像的中心小广场——那是普雷舍伦，他的目光越过广场，落在对面房子外墙上雕着的、他终生不可得的恋人尤利娅的脸上。曾经有个陌生人在那广场正中送了她一朵花。她在维莱特醒来——这家精神病院是柯艾略虚构的——被告知只剩几天可活。柯艾略借自己住精神病院的经历，让这本书追问：怎样的人生才值得活下去。",
    ["Prešeren"], ["普雷舍伦"],
    "https://en.wikipedia.org/wiki/Veronika_Decides_to_Die; https://litres.com/paulo-coelho/veronika-decides-to-die/read-online/; https://www.researchgate.net/publication/372348288; https://en.wikipedia.org/wiki/Prešeren_Monument_(Ljubljana)")]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
allb = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "books.js"))))
allp = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "places.js"))))
assert not {x["id"] for x in books} & allb and not {p["id"] for p in places} & allp
assert {p["id"] for p in places} == set(CO) and not {l["id"] for l in lines} & ids_in(b.data("lines.js"))
if __name__ == "__main__":
    M = "11-27: Veronika Decides to Die, added at the user's request (tools/content/batches/add_si2.py)"
    for name, xs in (("books.js", books), ("places.js", places), ("lines.js", lines)):
        b.append(b.data(name), xs, M)
    print(len(books), "book,", len(places), "place,", len(lines), "line")
