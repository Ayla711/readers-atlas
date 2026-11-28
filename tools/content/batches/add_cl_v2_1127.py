"""11-27: Chile, the new books of the selection re-check (tools/selection/cl.md, rule v2; the user took all five on 11-27). All
five came in through the Emol 2006 readers' vote for an ideal bicentenary library (first or second in their category).
The book records go to the shared South American list (data/sa/books.js). Places, with the reason for each:
- The former Valparaíso prison (now the Parque Cultural de Valparaíso) for Hijo de ladrón: the novel opens as Aniceto Hevia
  walks out of the Valparaíso jail; the city's public jail stood on Cerro Cárcel from 1906 to 1999.
- Santiago for Papelucho: the diary does not dwell on its city; Marcela Paz was born and died in Santiago (A-24, said in the note).
- Temuco (existing cl-temuco-railway-museum) for Confieso que he vivido: the memoirs open with Neruda's childhood in Temuco.
- Concepción (existing cl-concepcion) for Putas asesinas: of its thirteen stories only "Carnet de baile" touches Chile, recalling
  Bolaño's arrest after the 1973 coup, on a bus bound for Concepción (A-24, said in the note).
- Isla Negra (existing cl-isla-negra) for Ardiente paciencia: Mario is the postman of Isla Negra, with one client, Neruda.
All five are in copyright: scene notes, no quotation.
Usage: python3 -I tools/content/batches/add_cl_v2_1127.py <app_dir> tools/content/batches/coords/add_cl_v2_1127.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-27"
b.init(APP, "", "cl", DATE)
SA_BOOKS = os.path.join(APP, "data", "sa", "books.js")
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]

books = [
    dict(id="hijo-de-ladron", title="Born Guilty", title_zh="小偷的儿子", title_orig="Hijo de ladrón", author="Manuel Rojas",
         author_zh="曼努埃尔·罗哈斯", year="1951", orig_lang="es", public_domain=False, source_url=None, aliases=["Hijo de ladrón", "Son of a Thief", "Aniceto Hevia"]),
    dict(id="papelucho", title="Papelucho", title_zh="帕佩卢乔", title_orig="Papelucho", author="Marcela Paz", author_zh="马塞拉·帕斯",
         year="1947", orig_lang="es", public_domain=False, source_url=None, aliases=["Papelucho"]),
    dict(id="confieso-que-he-vivido", title="Memoirs", title_zh="我承认，我曾历尽沧桑", title_orig="Confieso que he vivido", author="Pablo Neruda",
         author_zh="巴勃罗·聂鲁达", year="1974", orig_lang="es", public_domain=False, source_url=None, aliases=["Confieso que he vivido", "I Confess That I Have Lived"]),
    dict(id="putas-asesinas", title="Putas asesinas", title_zh="杀人的婊子", title_orig="Putas asesinas", author="Roberto Bolaño",
         author_zh="罗贝托·波拉尼奥", year="2001", orig_lang="es", public_domain=False, source_url=None, aliases=["Putas asesinas", "Carnet de baile", "Last Evenings on Earth", "The Return"]),
    dict(id="ardiente-paciencia", title="Burning Patience", title_zh="火热的耐心", title_orig="Ardiente paciencia", author="Antonio Skármeta",
         author_zh="安东尼奥·斯卡尔梅达", year="1985", orig_lang="es", public_domain=False, source_url=None,
         aliases=["Ardiente paciencia", "The Postman", "El cartero de Neruda", "Il Postino", "邮差"]),
]

places = [
    b.ORIG("cl-ex-carcel-valparaiso", "Former Valparaíso Prison (Parque Cultural)", "瓦尔帕莱索 · 旧监狱（文化公园）", *C("cl-ex-carcel-valparaiso"),
        "On Cerro Cárcel, the hill named after it, the city's public jail stood from 1906 to 1999, the main prison of the Valparaíso region and long a place of political detention; a colonial powder magazine of 1807-09 survives inside the walls. Since 2011 it has been the Parque Cultural de Valparaíso, with a terrace looking over the bay. Manuel Rojas, jailed in Valparaíso in 1915, opened his Hijo de ladrón at the door of the Valparaíso jail",
        "这座山就叫“监狱山”，1906 到 1999 年城市的公共监狱就在山顶，是瓦尔帕莱索大区最主要的监狱，长期关押政治犯；围墙里还保存着一座 1807 至 1809 年的殖民时代火药库。2011 年起这里改成瓦尔帕莱索文化公园，有一处平台可以俯瞰海湾。曼努埃尔·罗哈斯 1915 年曾在瓦尔帕莱索坐牢，他的《小偷的儿子》就从瓦尔帕莱索监狱门口开始"),
    b.ORIG("cl-santiago", "Santiago", "圣地亚哥", *C("cl-santiago"),
        "Chile's capital, on the Mapocho river between the Andes and the coastal range. Marcela Paz was born here in 1902 and died here in 1985; her Papelucho, an eight-year-old boy who writes a diary of life at home, with his friends and at school, is the most read children's character in Chile. The diaries hardly name their city; they are hung here, on the writer's own",
        "智利首都，坐落在安第斯山和海岸山脉之间的马波乔河畔。马塞拉·帕斯 1902 年生在这里，1985 年也死在这里；她笔下写日记的八岁男孩帕佩卢乔，记下自己在家里、和朋友们、在学校的日子，是智利读者最多的儿童文学人物。日记里几乎不写城市的名字；这里把它放在作家自己的城市"),
]

lines = [
    b.S("cl-hijo-s1", "hijo-de-ladron", "cl-ex-carcel-valparaiso", "The novel as a whole", "全书",
        "The novel opens with Aniceto Hevia standing outside the Valparaíso jail, free at last after serving time for a robbery he did not commit. Born in Buenos Aires, son of a professional thief, the Gallego, he goes back over some twenty years, through prison and the long journey to Chile. From the prison door he sees the bay; he walks down the hill to the sea, to the Caleta del Membrillo, where two men are combing the beach, Cristián and Echeverría, 'the Philosopher', whom he falls in with. Rojas, who had himself been jailed in Valparaíso in 1915, told the story through long flashbacks; the jury of the 1950 contest thought the manuscript disordered and gave it only an honourable mention.",
        "小说一开头，阿尼塞托·埃维亚站在瓦尔帕莱索监狱门外，他因一桩没犯过的抢劫坐了牢，终于自由了。他生在布宜诺斯艾利斯，父亲“加利西亚人”是职业小偷；他回想将近二十年的事：坐牢，一路辗转来到智利。从监狱门口能望见海湾，他走下山到海边，来到梅姆布里略渔湾，海滩上有两个人在来回搜寻东西，克里斯蒂安和外号“哲学家”的埃切维里亚，他从此和两人结伴。罗哈斯自己 1915 年也在瓦尔帕莱索坐过牢；他用大段倒叙来讲这个故事，1950 年参加征文时评委以为手稿颠三倒四，只给了荣誉奖。",
        ["Valparaíso"], ["瓦尔帕莱索"],
        "https://es.wikipedia.org/wiki/Hijo_de_ladr%C3%B3n; https://revistaliteratura.uchile.cl/index.php/RCL/article/view/63989/68300; https://www.goodreads.com/book/show/791695; https://revistas.udec.cl/index.php/atenea/article/download/23264/20301/64685; https://revistas.pucsp.br/index.php/teoliteraria/article/download/22908/16577/58807; https://www.memoriachilena.gob.cl/602/w3-article-95845.html; https://es.wikipedia.org/wiki/Parque_Cultural_de_Valpara%C3%ADso"),
    b.S("cl-papelucho-s1", "papelucho", "cl-santiago", "The first book", "第一本",
        "Papelucho, a boy of eight, thinks he has accidentally poisoned Domitila, the family's maid, and the fright sets him writing a diary of his everyday life at home, with his friends and at school. His adventures happen mostly inside his head: every time he tries to fix a problem, he leaves things worse than before. Marcela Paz drew on her own childhood; the diary's misspellings and turns of speech give it its life, the parents are no models of virtue, and the book never moralises. The series ran to twelve books by 1974, and they are still the most read books of Chilean schoolchildren, some on the compulsory reading list. Marcela Paz was born in Santiago.",
        "八岁的帕佩卢乔以为自己不小心毒死了家里的女佣多米蒂拉，吓得开始写日记，记下在家里、和朋友们、在学校的日常生活。他的冒险大多发生在自己的脑袋里：每次想解决一个问题，结果都把事情弄得更糟。马塞拉·帕斯取材于自己的童年；日记里的错别字和口头语让它生气勃勃，父母也不是什么道德榜样，书从不说教。这个系列一直写到 1974 年，共十二本，至今仍是智利学龄孩子读得最多的书，有几本列入必读书目。马塞拉·帕斯生在圣地亚哥。",
        ["Santiago"], ["圣地亚哥"],
        "https://es.wikipedia.org/wiki/Papelucho; https://es.wikipedia.org/wiki/Marcela_Paz"),
    b.S("cl-confieso-s1", "confieso-que-he-vivido", "cl-temuco-railway-museum", "The memoirs as a whole", "全书",
        "Neruda's memoirs, written over many years and published after his death in 1974, begin with his boyhood in Temuco, in the rain-soaked forest country of the south, where his father drove a ballast train on the railway. From there they follow the poet around the world: the opium dens of the East and the Burma of the British, his consulate in Republican Spain and the ship Winnipeg that carried Spanish refugees to exile in Chile, talks with Che Guevara, journeys to Mexico and the Soviet Union. They break off with the coup of 11 September 1973 and the death of his friend Salvador Allende, a few days before the poet's own. The chapter on his consulship in Ceylon also contains his account of raping a Tamil woman who cleaned his house in Colombo in 1929.",
        "聂鲁达的回忆录写了很多年，1974 年他死后才出版，开头是他在泰穆科的少年时代：南方多雨的森林地带，父亲在铁路上开道砟车。从那里开始，它跟着诗人走遍世界：东方的鸦片馆、英国统治下的缅甸，他在共和国时期的西班牙当领事，用“温尼伯号”把西班牙难民送到智利流亡，和切·格瓦拉的谈话，去墨西哥和苏联的旅行。回忆录在 1973 年 9 月 11 日政变和他的朋友萨尔瓦多·阿连德之死处戛然而止，几天后诗人自己也去世了。书中写他在锡兰当领事的一章里，也有他自述 1929 年在科伦坡强暴一名为他打扫房子的泰米尔女人的经过。",
        ["Temuco"], ["泰穆科"],
        "https://es.wikipedia.org/wiki/Confieso_que_he_vivido; https://es.wikipedia.org/wiki/Pablo_Neruda; https://core.ac.uk/download/296294252.pdf; https://www.memoriachilena.gob.cl/archivos2/pdfs/mc0015100.pdf"),
    b.S("cl-putas-s1", "putas-asesinas", "cl-concepcion", "“Carnet de baile”", "《舞会记事本》",
        "Bolaño's second book of stories, thirteen in all, moves between Mexico City, Acapulco, Barcelona, Paris, Berlin and Liberia, often in the company of his alter ego Arturo Belano. Chile comes closest in \"Carnet de baile\", 69 short sections in which Bolaño muses on Pablo Neruda and recalls episodes of his own life, among them his detention in the 1973 coup. In his biography that detention came in November 1973, when he was taken off a bus going from Los Ángeles to Concepción and held for eight days, freed thanks to an old schoolfriend among the police; since 2009 some of his Mexican friends have doubted that he was in Chile in 1973 at all.",
        "这是波拉尼奥的第二部短篇集，共十三篇，在墨西哥城、阿卡普尔科、巴塞罗那、巴黎、柏林和利比里亚之间来回，常常由他的化身阿图罗·贝拉诺出场。离智利最近的是《舞会记事本》：分成 69 个短小节，波拉尼奥谈论巴勃罗·聂鲁达，也回想自己一生的片段，其中有他在 1973 年政变时被拘押。按他的生平，这次拘押发生在 1973 年 11 月：他在从洛斯安赫莱斯去康塞普西翁的长途车上被带走，关了八天，因为看守的警察里有个老同学才得以获释；不过 2009 年以来，他当年在墨西哥的一些朋友怀疑他 1973 年是否真的去过智利。",
        ["Concepción"], ["康塞普西翁"],
        "https://es.wikipedia.org/wiki/Putas_asesinas; https://es.wikipedia.org/wiki/Roberto_Bola%C3%B1o; https://en.wikipedia.org/wiki/Roberto_Bola%C3%B1o"),
    b.S("cl-ardiente-s1", "ardiente-paciencia", "cl-isla-negra", "The novel as a whole", "全书",
        "June 1969. Mario Jiménez, seventeen, does not want to be a fisherman like his father, so he becomes a postman, assigned to Isla Negra with a single client: Pablo Neruda. Day after day he brings the poet his letters; slowly they start to talk about metaphors and become friends, and Mario, who wants to be a poet too, falls for Beatriz, the daughter of a widow who wants nothing to do with him. Neruda goes to Paris as ambassador and sends Mario a tape recorder to record the sounds he misses, among them the cry of Mario's newborn son, Pablo Neftalí. After the coup of 11 September 1973 the poet's house is guarded and no letters get in, so Mario learns them by heart and passes them on to the ailing Neruda. Skármeta's radio play became a film in 1983, a novel in 1985, and Michael Radford's Il Postino in 1994.",
        "1969 年 6 月。十七岁的马里奥·希门内斯不想像父亲一样当渔夫，于是当了邮差，被派到黑岛，只有一个收信人：巴勃罗·聂鲁达。他天天给诗人送信，两人慢慢谈起隐喻，成了朋友；也想当诗人的马里奥爱上了贝阿特丽丝，她守寡的母亲却不待见他。聂鲁达去巴黎当大使，给马里奥寄来一台录音机，请他录下自己思念的声音，其中有马里奥刚出生的儿子巴勃罗·内夫塔利的哭声。1973 年 9 月 11 日政变后，诗人的房子被看守起来，信件送不进去，马里奥就把信背下来，转述给病中的聂鲁达。斯卡尔梅达的广播剧 1983 年拍成电影，1985 年写成小说，1994 年又被迈克尔·莱德福拍成《邮差》。",
        ["Isla Negra"], ["黑岛"],
        "https://es.wikipedia.org/wiki/Ardiente_paciencia"),
]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "books.js"))))
all_places = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "places.js"))))
all_lines = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "lines.js"))))
assert not {x["id"] for x in books} & all_books
assert {p["id"] for p in places} == set(CO) and not set(CO) & all_places
assert not {l["id"] for l in lines} & all_lines
assert {"cl-temuco-railway-museum", "cl-concepcion", "cl-isla-negra"} <= all_places
if __name__ == "__main__":
    note = "11-27 selection re-check, rule v2 (add_cl_v2_1127.py)"
    b.append(SA_BOOKS, books, note)
    b.append(b.data("places.js"), places, note)
    b.append(b.data("lines.js"), lines, note)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
