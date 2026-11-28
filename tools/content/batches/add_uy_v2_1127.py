"""11-27: Uruguay, the new books of the selection re-check (tools/selection/uy.md, rule v2; the user took both on 11-27).
The book records go to the shared South American list (data/sa/books.js). Places, with the reason for each:
- Colonia del Sacramento for El astillero: Santa María is imaginary, a river port that critics see as built from pieces of
  Buenos Aires, Montevideo, Rosario and Colonia del Sacramento; Colonia is the Uruguayan river port among them (A-24, said
  in the note).
- Montevideo for La novela luminosa: Levrero wrote its "Diario de la beca" at home in Montevideo, his city.
Both are in copyright: scene notes, no quotation.
Usage: python3 -I tools/content/batches/add_uy_v2_1127.py <app_dir> tools/content/batches/coords/add_uy_v2_1127.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-27"
b.init(APP, "", "uy", DATE)
SA_BOOKS = os.path.join(APP, "data", "sa", "books.js")
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]

books = [
    dict(id="el-astillero", title="The Shipyard", title_zh="造船厂", title_orig="El astillero", author="Juan Carlos Onetti",
         author_zh="胡安·卡洛斯·奥内蒂", year="1961", orig_lang="es", public_domain=False, source_url=None,
         aliases=["El astillero", "Santa María", "Larsen"]),
    dict(id="la-novela-luminosa", title="The Luminous Novel", title_zh="发光的小说", title_orig="La novela luminosa", author="Mario Levrero",
         author_zh="马里奥·莱夫雷罗", year="2005", orig_lang="es", public_domain=False, source_url=None,
         aliases=["La novela luminosa", "Diario de la beca"]),
]

places = [
    b.ORIG("uy-colonia-del-sacramento", "Colonia del Sacramento", "科洛尼亚-德尔萨克拉门托", *C("uy-colonia-del-sacramento"),
        "An old Portuguese-founded river port on the Río de la Plata, facing Buenos Aires across the estuary. Juan Carlos Onetti's imaginary river town of Santa María, the setting of El astillero (1961) and most of his later fiction, has been described as built from pieces of Buenos Aires, Montevideo, Rosario and Colonia del Sacramento; Onetti himself said he made it out of nostalgia for his own city. It is hung here, on the Uruguayan river port among those pieces",
        "拉普拉塔河上一座由葡萄牙人建立的老河港，隔着河口与布宜诺斯艾利斯相望。胡安·卡洛斯·奥内蒂虚构的河港小城圣玛丽亚，是《造船厂》（1961）和他后来大部分小说的背景，被认为是用布宜诺斯艾利斯、蒙得维的亚、罗萨里奥和科洛尼亚-德尔萨克拉门托的碎片拼成的；奥内蒂自己说，他造出这座小城是出于对故乡的思念。这里把它放在这些碎片中属于乌拉圭的这座河港"),
    b.ORIG("uy-montevideo", "Montevideo", "蒙得维的亚", *C("uy-montevideo"),
        "Uruguay's capital, on the Río de la Plata. Mario Levrero was born here in 1940, lived here most of his life and died here in 2004; with a Guggenheim grant in 2000-01 he kept, at home in Montevideo, the diary that became the bulk of La novela luminosa",
        "乌拉圭首都，在拉普拉塔河畔。马里奥·莱夫雷罗 1940 年生在这里，一生大部分时间住在这里，2004 年也死在这里；2000 至 2001 年，他靠古根海姆奖金在蒙得维的亚家中写下了日记，这本日记成了《发光的小说》的主体"),
]

lines = [
    b.S("uy-astillero-s1", "el-astillero", "uy-colonia-del-sacramento", "The novel as a whole", "全书",
        "Five years after the Governor expelled him from Santa María, Larsen, once the town's pimp, gets off one morning at the stop of the buses from Colón and walks back in. He takes the post of general manager of Jeremías Petrus's shipyard at Puerto Astillero, a ruined, abandoned yard kept up by two almost ghostly employees, and courts Petrus's simple-minded daughter Angélica Inés. It ends in futility and unheroic defeat. Santa María is imaginary, a river town critics see as made from pieces of Buenos Aires, Montevideo, Rosario and Colonia del Sacramento.",
        "五年前，省长把拉尔森赶出了圣玛丽亚，这个当年的皮条客如今在一个早晨从科隆开来的公共汽车站下车，又走回城里。他接下了赫雷米亚斯·佩特鲁斯在“船厂港”的造船厂总经理一职：一个破败荒废的船厂，只剩两个几乎像幽灵的雇员；他还追求佩特鲁斯痴傻的女儿安赫利卡·伊内斯。故事以徒劳和毫无英雄气概的失败告终。圣玛丽亚是虚构的，评论家认为它是用布宜诺斯艾利斯、蒙得维的亚、罗萨里奥和科洛尼亚-德尔萨克拉门托的碎片拼成的河港小城。",
        ["Colonia del Sacramento"], ["科洛尼亚-德尔萨克拉门托"],
        "https://es.wikipedia.org/wiki/Juan_Carlos_Onetti; https://elhuron.uchile.cl/index.php/RCL/article/download/40135/41692/139181; https://www.ebsco.com/research-starters/history/shipyard-juan-carlos-onetti; https://www.britannica.com/topic/The-Shipyard; https://revistas.um.edu.uy/index.php/revistahumanidades/article/download/1318/1741/4352; https://www.gradesaver.com/el-astillero; https://www.revistadelauniversidad.mx/downloads/1c811d63-d74a-455d-8c0e-ebd7a2f024c0/rum-AGO.1990-art%c3%adculos-la-santa-maria-onettiana.pdf; https://www.cervantesvirtual.com/obra-visor/latinoamerica-el-astillero-astillado-una-lectura-de-la-santa-maria-de-onetti-como-metafora-de-latinoamerica--0/html/01bfe1b0-82b2-11df-acc7-002185ce6064_2.html"),
    b.S("uy-luminosa-s1", "la-novela-luminosa", "uy-montevideo", "The book as a whole", "全书",
        "In 2000 Mario Levrero received a Guggenheim grant to finish a \"luminous novel\" he had begun a decade before and abandoned. Instead, for a year, he kept a diary at home in Montevideo, the \"Diario de la beca\", some 450 pages about how he did not write it: the computer games he cannot stop playing, the dead pigeon outside his window, his obsessions, his search for second-hand books. Only at the end come the hundred-odd pages of the luminous novel itself, left unfinished. Published in 2005, a year after his death, it was voted in 2016 one of the best novels in Spanish of the previous 25 years.",
        "2000 年，马里奥·莱夫雷罗拿到古根海姆奖金，要写完一部十年前开了头又放下的“发光的小说”。结果他在蒙得维的亚的家里记了一年日记，即《奖金日记》，约 450 页，写的是他怎么没写成这部小说：停不下来的电脑游戏，窗外的死鸽子，种种执念，四处淘旧书。只有最后一百来页才是那部“发光的小说”本身，也没有写完。这本书 2005 年出版，那时他已去世一年；2016 年被评为此前 25 年最好的西班牙语小说之一。",
        ["Montevideo"], ["蒙得维的亚"],
        "https://es.wikipedia.org/wiki/Mario_Levrero; https://core.ac.uk/download/296294257.pdf; https://diariodecuba.com/cultura/1376094030_4579.html; https://drum.lib.umd.edu/bitstreams/5c0f67ca-9c92-495c-8470-a1702a6655ea/download; https://in-cubadora.com/wp-content/uploads/2016/11/inzaurraldelevrero.pdf"),
]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "books.js"))))
all_places = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "places.js"))))
all_lines = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "lines.js"))))
assert not {x["id"] for x in books} & all_books
assert {p["id"] for p in places} == set(CO) and not set(CO) & all_places
assert not {l["id"] for l in lines} & all_lines
if __name__ == "__main__":
    note = f"11-27 selection re-check, rule v2 ({os.path.basename(__file__)})"
    b.append(SA_BOOKS, books, note)
    b.append(b.data("places.js"), places, note)
    b.append(b.data("lines.js"), lines, note)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
