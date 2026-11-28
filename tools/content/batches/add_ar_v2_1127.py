"""11-27: Argentina, the new books of the selection re-check (tools/selection/ar.md, rule v2; the user took all seven on 11-27).
Six new book records go to the shared South American list (data/sa/books.js); Ficciones is already there (hung at Fray Bentos,
Uruguay) and gets its first Argentine line. Places, with the reason for each:
- Plaza Constitución (existing ar-constitucion) for Ficciones: in "The South" (1953, in Ficciones from 1956) Dahlmann takes the
  train south from the southern terminus, Constitución.
- Mar del Plata for The Tunnel: Hunter's estancia, where María goes and where Castel kills her, is at Mar del Plata.
- Recoleta Cemetery (existing ar-recoleta-cemetery) for Santa Evita: the novel follows the corpse's twenty-year journey; the
  real body was buried at Recoleta in 1976.
- Colastiné Norte for La grande: Saer's "zona" (Santa Fe, Rincón Norte, Colastiné, the Paraná).
- Buenos Aires (the city) for El pasado and El vuelo de la reina: both are set across the city.
- Resistencia for Santo oficio de la memoria: the Domeniconelle settle in the Chaco; Giardinelli was born and lives there.
All seven are in copyright: scene notes in our own words.
Usage: python3 -I tools/content/batches/add_ar_v2_1127.py <app_dir> tools/content/batches/coords/add_ar_v2_1127.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-27"
b.init(APP, "", "ar", DATE)
SA_BOOKS = os.path.join(APP, "data", "sa", "books.js")
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]

books = [
    dict(id="el-tunel", title="The Tunnel", title_zh="隧道", title_orig="El túnel", author="Ernesto Sabato", author_zh="埃内斯托·萨瓦托",
         year="1948", orig_lang="es", public_domain=False, source_url=None, aliases=["El túnel", "Juan Pablo Castel", "María Iribarne"]),
    dict(id="santa-evita", title="Santa Evita", title_zh="圣埃维塔", title_orig="Santa Evita", author="Tomás Eloy Martínez",
         author_zh="托马斯·埃洛伊·马丁内斯", year="1995", orig_lang="es", public_domain=False, source_url=None, aliases=["Eva Perón", "Evita"]),
    dict(id="la-grande-saer", title="La Grande", title_zh="伟大的", title_orig="La grande", author="Juan José Saer", author_zh="胡安·何塞·萨埃尔",
         year="2005", orig_lang="es", public_domain=False, source_url=None, aliases=["La grande"]),
    dict(id="el-pasado-pauls", title="The Past", title_zh="过去", title_orig="El pasado", author="Alan Pauls", author_zh="阿兰·保尔斯",
         year="2003", orig_lang="es", public_domain=False, source_url=None, aliases=["El pasado", "Rímini", "Sofía"]),
    dict(id="santo-oficio-de-la-memoria", title="Santo oficio de la memoria", title_zh="记忆的神圣职责", title_orig="Santo oficio de la memoria",
         author="Mempo Giardinelli", author_zh="门波·贾尔迪内利", year="1991", orig_lang="es", public_domain=False, source_url=None,
         aliases=["Domeniconelle"]),
    dict(id="el-vuelo-de-la-reina", title="The Queen's Flight", title_zh="女王的飞翔", title_orig="El vuelo de la reina", author="Tomás Eloy Martínez",
         author_zh="托马斯·埃洛伊·马丁内斯", year="2002", orig_lang="es", public_domain=False, source_url=None, aliases=["El vuelo de la reina", "Reina Remis"]),
]

places = [
    b.ORIG("ar-mar-del-plata", "Mar del Plata", "马德普拉塔", *C("ar-mar-del-plata"),
        "The great Atlantic seaside resort of Buenos Aires province. In Sabato's The Tunnel, the estancia of Hunter, the cousin of María's blind husband, lies at Mar del Plata: María keeps going there, Castel follows her there and grows sure she is unfaithful, and in the end he drives out to it through the night and kills her",
        "布宜诺斯艾利斯省大西洋岸边的海滨大城。在萨瓦托的《隧道》里，玛丽亚的盲人丈夫的表兄亨特，庄园就在马德普拉塔：玛丽亚一次次去那里，卡斯特尔跟去，越来越认定她不忠，最后连夜开车赶到庄园杀了她"),
    b.ORIG("ar-buenos-aires", "Buenos Aires", "布宜诺斯艾利斯", *C("ar-buenos-aires"),
        "Argentina's capital, on the Río de la Plata. Two novels in the atlas are set across the whole city rather than in one corner of it: Alan Pauls's The Past (2003), the long aftermath of a twelve-year love, and Tomás Eloy Martínez's The Queen's Flight (2002), set at the top of one of its great newspapers",
        "阿根廷首都，在拉普拉塔河畔。地图上有两部小说写的是整座城，而不是某一个角落：阿兰·保尔斯的《过去》（2003），写一段十二年的爱情分手后漫长的余波；托马斯·埃洛伊·马丁内斯的《女王的飞翔》（2002），写一家大报社的掌门人"),
    b.ORIG("ar-resistencia", "Resistencia, Chaco", "查科 · 雷西斯滕西亚", *C("ar-resistencia"),
        "The capital of Chaco province, in Argentina's north-east. Mempo Giardinelli was born in the Chaco in 1947 and still lives there; his Santo oficio de la memoria follows the Domeniconelle, Italian immigrants who came to Buenos Aires in 1884 and later settled in the Chaco",
        "阿根廷东北部查科省的首府。门波·贾尔迪内利 1947 年生在查科，至今住在这里；他的《记忆的神圣职责》写的是多梅尼科内列一家：意大利移民，1884 年到布宜诺斯艾利斯，后来在查科落脚"),
    b.ORIG("ar-colastine", "Colastiné Norte, Santa Fe", "圣菲 · 北科拉斯廷", *C("ar-colastine"),
        "A riverside settlement on the Paraná's coast east of the city of Santa Fe. Juan José Saer, born in Serodino in Santa Fe province, set nearly all his fiction in what he called the zone: the city, the river and its islands, and the shacks along the coast at Colastiné and Rincón Norte. His last novel, La Grande, brings Gutiérrez back to it",
        "圣菲城东边巴拉那河岸上的一个河边小镇。胡安·何塞·萨埃尔生在圣菲省的塞罗迪诺，几乎所有小说都发生在他所说的“地带”：圣菲城、大河和河中的岛，还有科拉斯廷、北林孔沿岸的棚屋。他的最后一部小说《伟大的》让古铁雷斯回到了这里"),
]

lines = [
    b.S("ar-fic-s1", "ficciones", "ar-constitucion", "“The South” (“El Sur”)", "《南方》",
        "Juan Dahlmann, a secretary in a Buenos Aires library, is proud of his criollo grandfather killed on the pampas. Rushing upstairs with a new copy of the Arabian Nights, he gashes his head on an open window and barely survives septicaemia. Discharged, he takes a taxi at dawn to the southern railway terminus at Constitución, stops in a café near the station where a cat lets itself be stroked, and boards the train for the small estate in the South he has never had time to visit; at a country store on the plain he ends up accepting a knife fight. First printed in La Nación in 1953, the story joined Ficciones in its 1956 edition, and Borges called it perhaps his best.",
        "胡安·达尔曼是布宜诺斯艾利斯一家图书馆的秘书，以死在潘帕斯草原上的土生白人祖父为荣。他捧着新得的《一千零一夜》冲上楼，被开着的窗框划破了头，得了败血症，死里逃生。出院那天黎明，他坐出租车到宪法区的南方铁路总站，在站旁一家咖啡馆里摸了摸任人抚摸的猫，然后坐上火车，去南方那座他一直没空去看的小庄园；在草原上的一家杂货铺里，他最后接受了一场刀斗。这篇小说 1953 年先登在《民族报》上，1956 年收进《虚构集》，博尔赫斯说它也许是自己最好的小说。",
        ["Constitución"], ["宪法区"],
        "https://en.wikipedia.org/wiki/The_South_(short_story); https://es.wikipedia.org/wiki/El_Sur_(cuento)"),
    b.S("ar-tunel-s1", "el-tunel", "ar-mar-del-plata", "The novel as a whole", "全书",
        "The painter Juan Pablo Castel opens the book by confessing that he killed María Iribarne. At the Salón de Primavera of 1946 she was the only visitor who noticed a small window in one of his paintings; he hunts for her through Buenos Aires, learns that she is married to the blind Allende, and comes to suspect her visits to an estancia at Mar del Plata owned by Allende's cousin Hunter. When she fails to come back to the city, he drives out to the estancia and kills her, then goes to tell Allende, who turns out to have known. It was Sabato's first novel, published by Sur in 1948.",
        "画家胡安·巴勃罗·卡斯特尔一开篇就承认，是他杀了玛丽亚·伊里巴内。1946 年的春季沙龙上，她是唯一注意到他一幅画里那扇小窗的观众；他在布宜诺斯艾利斯满城找她，得知她嫁给了盲人阿连德，又开始怀疑她常去马德普拉塔的那座庄园——庄园的主人是阿连德的表兄亨特。她没有按时回城，他就开车赶到庄园杀了她，再去告诉阿连德，却发现阿连德早就知道。这是萨瓦托的第一部小说，1948 年由《南方》出版社出版。",
        ["Mar del Plata"], ["马德普拉塔"],
        "https://en.wikipedia.org/wiki/The_Tunnel_(Sabato_novel); https://www.ecured.cu/El_túnel; https://www.ingenieria.unam.mx/dcsyhfi/material_didactico/Literatura_Hispanoamericana_Contemporanea/Autores_S/SABATO/El.pdf; https://revistas.upb.edu.co/index.php/escritos/article/download/257/150/282"),
    b.S("ar-evita-s1", "santa-evita", "ar-recoleta-cemetery", "The novel as a whole", "全书",
        "A blend of fact and fiction about the corpse of Eva Perón, who died of cancer at 33 in 1952. The Spanish doctor Pedro Ara embalms the body in a laboratory on the second floor of the CGT union building in Azopardo street; after Perón's fall in 1955 the army seizes it, and Colonel Moori Koenig, charged with hiding it, grows obsessed with it as it is moved from one hiding place to another. The novel follows a journey of some twenty years; the real body was laid to rest here at Recoleta in 1976. The book is estimated to have sold more than ten million copies, and was made into a television series in 2022.",
        "一部虚实交织的小说，写的是 1952 年 33 岁死于癌症的埃娃·庇隆的遗体。西班牙医生佩德罗·阿拉在阿索帕尔多街总工会大楼二楼的实验室里给遗体做了防腐；1955 年庇隆倒台，军方夺走遗体，奉命藏匿它的莫里·柯尼希上校在一次次转移中对它着了魔。小说追随的这段旅程长达二十年左右；真实的遗体 1976 年才安葬在这里的雷科莱塔公墓。据估计这本书卖了一千多万册，2022 年拍成了电视剧。",
        ["Recoleta"], ["雷科莱塔"],
        "https://en.wikipedia.org/wiki/Santa_Evita; https://www.aacademica.org/of/30.pdf; https://www.publico.es/internacional/robo-cadaver-eva-peron-paso-cuerpo-primera-dama-peronismo.html; https://dialnet.unirioja.es/descarga/articulo/5228689.pdf; https://dlib.si/stream/URN:NBN:SI:DOC-FV4OQIKH/58519d72-f87c-4ae0-9feb-47af1ead590f/PDF"),
    b.S("ar-grande-s1", "la-grande-saer", "ar-colastine", "The novel as a whole", "全书",
        "Saer's last novel, about twenty pages short of its end when he died in 2005, takes place over one rainy week in early April in the 1990s. Willy Gutiérrez comes back to Santa Fe after some thirty years away, and Nula, a 29-year-old wine seller who is writing notes towards an ontology of becoming, tries to find out why he left so suddenly in the 1960s; old friends such as Tomatis reappear, and the week ends with a long asado. The zone is drawn from real places: Santa Fe, Rincón Norte, Colastiné and the Paraná with its islands.",
        "这是萨埃尔的最后一部小说，2005 年他去世时离写完还差二十来页。故事发生在 90 年代四月初一个下雨的星期：威利·古铁雷斯离开三十年左右后回到圣菲，二十九岁的葡萄酒推销员努拉正在写一部《生成本体论札记》，想弄清他 60 年代为什么突然出走；托马蒂斯等老朋友也一一重现，这个星期以一场漫长的烤肉聚会收尾。小说里的“地带”取自真实的地方：圣菲、北林孔、科拉斯廷，还有布满小岛的巴拉那河。",
        ["Colastiné"], ["科拉斯廷"],
        "https://www.nybooks.com/articles/2014/11/20/subtle-minds-santa-fe/; https://www.elboomeran.com/upload/ficheros/obras/extracto_la_grande.pdf; https://editoriales.facultades.unc.edu.ar/index.php/publicacionesffyh/catalog/download/325/395/7755?inline=1; https://libros.uam.es/tfm/catalog/download/907/1589/1551?inline=1; https://www.wordswithoutborders.org/book-review/juan-jose-saers-la-grande; https://fh.mdp.edu.ar/revistas/index.php/etl/article/download/2916/3541"),
    b.S("ar-pasado-s1", "el-pasado-pauls", "ar-buenos-aires", "The novel as a whole", "全书",
        "Rímini and Sofía, together since their teens, split up after twelve years, amicably at first. He moves on, working as an interpreter, and falls in love again, with Vera, then Carmen, then Nancy, but Sofía keeps coming back: with her letters, with the box of their photographs, with her claim on the life they shared. A long chronicle of late twentieth-century Buenos Aires, the novel won the Herralde Prize in 2003 and was filmed by Héctor Babenco.",
        "里米尼和索菲亚从少年时就形影不离，在一起十二年后分手，起初还算和气。他开始新生活，当口译，又先后爱上薇拉、卡门和南希，可索菲亚总是回来：带着她的信，带着装满两人照片的盒子，要回她在两人过去里的那一份。这部小说是 20 世纪末布宜诺斯艾利斯的一部长篇编年史，2003 年获埃拉尔德奖，后来由埃克托尔·巴本科拍成电影。",
        ["Buenos Aires"], ["布宜诺斯艾利斯"],
        "https://margins.app/el-pasado/w/1239f67289d54ff3ae62dcb682ab3223; https://www.redalyc.org/pdf/237/23739873004.pdf; https://fh.mdp.edu.ar/revistas/index.php/etl/article/download/9699/pdf; https://cms.anagrama-ed.es/view/10745/The%20Past-The%20Independent.pdf; https://www.goodreads.com/book/show/25417089"),
    b.S("ar-vuelo-s1", "el-vuelo-de-la-reina", "ar-buenos-aires", "The novel as a whole", "全书",
        "G. M. Camargo, the all-powerful editor of El Diario, one of the great Buenos Aires newspapers, and a man of the Argentine elite, becomes obsessed with Reina Remis, a gifted reporter half his age; their passion turns into a dangerous game of obsession, desire and power. Two stories from different times alternate and turn out to be bound together. The novel won the Alfaguara Prize in 2002 and stayed for weeks near the top of the Argentine bestseller lists.",
        "G. M. 卡马尔戈是布宜诺斯艾利斯大报《日报》权势滔天的社长，阿根廷上流社会的一员。他迷上了年纪只有他一半的才华横溢的记者蕾伊娜·雷米斯，两人的激情变成一场危险的执念、欲望与权力的游戏。两个不同时间的故事交替展开，最后发现彼此紧紧相连。小说 2002 年获阿尔法瓜拉奖，在阿根廷畅销榜前列待了好几个星期。",
        ["Buenos Aires"], ["布宜诺斯艾利斯"],
        "https://www.lecturalia.com/libro/10534/el-vuelo-de-la-reina; https://scenicrights.com/en/?p=20334; https://quelibroleo.com/el-vuelo-de-la-reina; https://www.pagina12.com.ar/diario/suplementos/libros/10-278-2002-09-15.html"),
    b.S("ar-santo-s1", "santo-oficio-de-la-memoria", "ar-resistencia", "The novel as a whole", "全书",
        "A family saga across ninety years of Argentine history: the Domeniconelle, Italian immigrants who reached Buenos Aires in 1884 and later settled in the Chaco. Gathered by a homecoming, twenty-four narrators, the dead among them, speak in 106 short sections, from an undying matriarch to a feminist granddaughter. Giardinelli, born in the Chaco in 1947, worked on it for nine years; it won the Rómulo Gallegos Prize in 1993.",
        "一部横跨阿根廷九十年历史的家族史诗：多梅尼科内列一家是意大利移民，1884 年到布宜诺斯艾利斯，后来在查科定居。因为一次归来，二十四个叙述者——包括已经去世的人——在 106 个小节里轮流开口，从长生不死的老祖母到信奉女性主义的孙女。贾尔迪内利 1947 年生在查科，这本书写了九年，1993 年获罗慕洛·加列戈斯奖。",
        ["Chaco"], ["查科"],
        "https://www.goodreads.com/book/show/2881172; https://revistas.ucentral.edu.co/index.php/hojasUniv/article/download/783/719/2877; https://journals.newprairiepress.org/sttcl/article/12971/galley/12840/download/; https://cuadernoscanela.org/index.php/cuadernos/article/view/8/7"),
]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "books.js"))))
all_places = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "places.js"))))
all_lines = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "lines.js"))))
assert not {x["id"] for x in books} & all_books
assert "ficciones" in all_books
assert {p["id"] for p in places} == set(CO) and not set(CO) & all_places
assert not {l["id"] for l in lines} & all_lines
assert {"ar-constitucion", "ar-recoleta-cemetery"} <= all_places
if __name__ == "__main__":
    note = "11-27 selection re-check, rule v2 (add_ar_v2_1127.py)"
    b.append(SA_BOOKS, books, note)
    b.append(b.data("places.js"), places, note)
    b.append(b.data("lines.js"), lines, note)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
