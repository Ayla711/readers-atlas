"""11-27: Peru, the new books of the selection re-check (tools/selection/pe.md, rule v2; the user took all seven on 11-27).
The book records go to the shared South American list (data/sa/books.js). Places, with the reason for each:
- The Country Club Lima Hotel for Un mundo para Julius: Julius spends his long holidays at the Hotel Country Club.
- Huamachuco for El mundo es ancho y ajeno: the community of Rumi is invented, set by the novel in the high Andes of
  La Libertad; Alegría was born near Huamachuco, and readers have placed the novel's world in the provinces of Huamachuco
  and Cajabamba (A-24, said in the note).
- Abancay for Los ríos profundos: Ernesto is a boarder at the priests' school in Abancay for most of the novel.
- Huaca Pucllana (Huaca Juliana), Miraflores, for La palabra del mudo: Ribeyro's stories are set all over Lima; he grew up in
  Santa Cruz, by the huaca, the neighbourhood of his Relatos santacrucinos, where the boys climb the "huaca Juliana".
- Plaza San Martín for Los inocentes: the gang roams central Lima in the 1950s; the book's "living dead of the Plaza San Martín"
  is the one landmark the sources name (A-24, said in the note).
- The Hotel Paracas for Huerto cerrado: in "Con Jimmy, en Paracas" Manolo goes with his father to the luxury resort at Paracas.
- Huancayo for Lituma en los Andes: Naccos is imaginary, a mining camp the novel puts in Junín; Huancayo is Junín's capital
  (A-24, said in the note).
All seven are in copyright: scene notes, no quotation.
Usage: python3 -I tools/content/batches/add_pe_v2_1127.py <app_dir> tools/content/batches/coords/add_pe_v2_1127.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-27"
b.init(APP, "", "pe", DATE)
SA_BOOKS = os.path.join(APP, "data", "sa", "books.js")
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]

books = [
    dict(id="un-mundo-para-julius", title="A World for Julius", title_zh="胡里乌斯的世界", title_orig="Un mundo para Julius",
         author="Alfredo Bryce Echenique", author_zh="阿尔弗雷多·布里斯·埃切尼克", year="1970", orig_lang="es", public_domain=False,
         source_url=None, aliases=["Un mundo para Julius", "Julius"]),
    dict(id="el-mundo-es-ancho-y-ajeno", title="Broad and Alien Is the World", title_zh="广漠的世界", title_orig="El mundo es ancho y ajeno",
         author="Ciro Alegría", author_zh="西罗·阿莱格里亚", year="1941", orig_lang="es", public_domain=False, source_url=None,
         aliases=["El mundo es ancho y ajeno", "Rumi", "Rosendo Maqui"]),
    dict(id="los-rios-profundos", title="Deep Rivers", title_zh="深沉的河流", title_orig="Los ríos profundos", author="José María Arguedas",
         author_zh="何塞·马里亚·阿格达斯", year="1958", orig_lang="es", public_domain=False, source_url=None, aliases=["Los ríos profundos"]),
    dict(id="la-palabra-del-mudo", title="The Word of the Speechless", title_zh="哑巴的话", title_orig="La palabra del mudo",
         author="Julio Ramón Ribeyro", author_zh="胡里奥·拉蒙·里贝罗", year="1972", orig_lang="es", public_domain=False, source_url=None,
         aliases=["La palabra del mudo", "Los gallinazos sin plumas", "Relatos santacrucinos"]),
    dict(id="los-inocentes-reynoso", title="The Innocents", title_zh="无辜者", title_orig="Los inocentes", author="Oswaldo Reynoso",
         author_zh="奥斯瓦尔多·雷诺索", year="1961", orig_lang="es", public_domain=False, source_url=None,
         aliases=["Los inocentes", "Lima en rock", "Cara de Ángel"]),
    dict(id="huerto-cerrado", title="Huerto cerrado", title_zh="关闭的果园", title_orig="Huerto cerrado", author="Alfredo Bryce Echenique",
         author_zh="阿尔弗雷多·布里斯·埃切尼克", year="1968", orig_lang="es", public_domain=False, source_url=None,
         aliases=["Huerto cerrado", "Con Jimmy, en Paracas"]),
    dict(id="death-in-the-andes", title="Death in the Andes", title_zh="利图马在安第斯山", title_orig="Lituma en los Andes",
         author="Mario Vargas Llosa", author_zh="马里奥·巴尔加斯·略萨", year="1993", orig_lang="es", public_domain=False, source_url=None,
         aliases=["Lituma en los Andes", "Naccos"]),
]

places = [
    b.ORIG("pe-country-club-lima", "Country Club Lima Hotel, San Isidro", "利马 · 乡村俱乐部酒店", *C("pe-country-club-lima"),
        "Opened in 1927 as the most exclusive country club in Lima, in Californian colonial style, and later reorganised as a hotel; the oldest hotel still working in the city after the Gran Hotel Bolívar. In Alfredo Bryce Echenique's Un mundo para Julius (1970) the rich boy Julius spends his long holidays here",
        "1927 年开业，是当年利马最高档的乡村俱乐部，加州殖民风格，后来改成酒店；在利马仍在营业的酒店里，它的历史仅次于玻利瓦尔大酒店。阿尔弗雷多·布里斯·埃切尼克的《胡里乌斯的世界》（1970）里，富家男孩胡里乌斯在这里度过漫长的假期"),
    b.ORIG("pe-huamachuco", "Huamachuco", "瓦马丘科", *C("pe-huamachuco"),
        "A highland town in the La Libertad region of northern Peru, capital of the province of Sánchez Carrión. Ciro Alegría was born in 1909 on the Quilca estate near Huamachuco, by the Marañón, and spent his early childhood among the farm labourers. His El mundo es ancho y ajeno (1941) is set in the invented Andean community of Rumi in La Libertad; readers have placed the novel's world in the provinces of Huamachuco and Cajabamba, and it is hung here",
        "秘鲁北部拉利伯塔德大区的高原小城，桑切斯·卡里翁省省会。西罗·阿莱格里亚 1909 年生在瓦马丘科附近、马拉尼翁河边的基尔卡庄园，童年早期和庄园的雇工们一起度过。他的《广漠的世界》（1941）写拉利伯塔德安第斯山中虚构的鲁米村社；有研究者把小说的世界定在瓦马丘科和卡哈班巴两省，这里把它放在瓦马丘科"),
    b.ORIG("pe-abancay", "Abancay", "阿班凯", *C("pe-abancay"),
        "Capital of the Apurímac region, at about 2,300 m on the eastern slope of the Andes above the valley of the Pachachaca, at the foot of the snow peak of Ampay. José María Arguedas set most of Los ríos profundos (1958) here: fourteen-year-old Ernesto is left as a boarder at the priests' school in Abancay while his father travels on in search of work",
        "阿普里马克大区首府，海拔约 2300 米，在安第斯山东坡、帕查查卡河谷之上，安派雪山脚下。何塞·马里亚·阿格达斯的《深沉的河流》（1958）大半发生在这里：父亲继续四处找活干，十四岁的埃内斯托被留在阿班凯的教会学校寄宿"),
    b.ORIG("pe-huaca-pucllana", "Huaca Pucllana (Huaca Juliana), Miraflores", "利马米拉弗洛雷斯 · 普克亚纳神庙", *C("pe-huaca-pucllana"),
        "A great adobe pyramid of the Lima culture (AD 200-700), seven stepped platforms in the middle of Miraflores. Julio Ramón Ribeyro grew up around 1937 in the new neighbourhood of Santa Cruz next to it, then still among fields, ditches and cliffs; his late Relatos santacrucinos return to that barrio, where the children climb the \"huaca Juliana\"",
        "利马文化（公元 200 至 700 年）的一座巨大土坯金字塔，七层阶梯平台，就在米拉弗洛雷斯区中间。胡里奥·拉蒙·里贝罗 1937 年前后在旁边新建的圣克鲁斯街区长大，那时周围还是田地、水渠和悬崖；他晚年的《圣克鲁斯故事》回到这个街区，孩子们在那里爬“胡利亚纳神庙”"),
    b.ORIG("pe-plaza-san-martin", "Plaza San Martín, Lima", "利马 · 圣马丁广场", *C("pe-plaza-san-martin"),
        "The great square of 20th-century Lima, on Avenida La Colmena, joined to the Plaza Mayor by the Jirón de la Unión. Oswaldo Reynoso's Los inocentes (1961) follows a gang of teenagers through the streets, billiard halls and bars of 1950s Lima; the book mentions the \"living dead\" of the Plaza San Martín, and Reynoso himself was a fixture of the bars of nearby Jirón Quilca",
        "20 世纪利马的大广场，在科尔梅纳大道上，经联合街通到武器广场。奥斯瓦尔多·雷诺索的《无辜者》（1961）跟着一伙少年走过 1950 年代利马的街道、台球厅和酒吧；书里写到圣马丁广场上的“活死人”，雷诺索本人也是附近基尔卡街酒吧里的常客"),
    b.ORIG("pe-hotel-paracas", "Hotel Paracas", "帕拉卡斯酒店", *C("pe-hotel-paracas"),
        "A luxury resort founded in 1944 on the bay of Paracas, in the desert on the Pacific coast some 240 km south of Lima. Alfredo Bryce Echenique's story \"Con Jimmy, en Paracas\", in his first book Huerto cerrado (1968), takes thirteen-year-old Manolo there with his father on a business trip",
        "1944 年开在帕拉卡斯湾的豪华度假酒店，在利马以南约 240 公里的太平洋沿岸沙漠里。阿尔弗雷多·布里斯·埃切尼克第一本书《关闭的果园》（1968）里的短篇《和吉米在帕拉卡斯》，写十三岁的马诺洛跟着父亲出差来到这里"),
    b.ORIG("pe-huancayo", "Huancayo", "万卡约", *C("pe-huancayo"),
        "Capital of the Junín region, in the Mantaro valley of the central Peruvian highlands. Mario Vargas Llosa's Lituma en los Andes (1993) is set in Naccos, a remote mining and road-building camp that the novel places in Junín; Naccos matches no real community, so the book is hung here, on the region's capital",
        "胡宁大区首府，在秘鲁中部高原的曼塔罗河谷。马里奥·巴尔加斯·略萨的《利图马在安第斯山》（1993）发生在纳科斯，一个偏远的矿区兼筑路工地，小说把它放在胡宁大区；纳科斯不对应任何真实的村镇，这里把书放在大区首府"),
]

lines = [
    b.S("pe-julius-s1", "un-mundo-para-julius", "pe-country-club-lima", "The novel as a whole", "全书",
        "Julius, a lonely, curious and perceptive boy of a very rich Lima family, grows up between the family's palace on Avenida Salaverry, his schools, first the Inmaculado Corazón and then Markham College, the long holidays at the Hotel Country Club and the servants of the house; at the start of adolescence he wakes, painfully, to the cruel world of the adults. Bryce, who was born and grew up in the very mansion the novel describes, wrote most of it in Paris; it is a sharp, sometimes mocking look at the elegance, hypocrisy, racism and class division of aristocratic Lima. It won Peru's National Prize for Literature in 1972 and was filmed in 2021.",
        "胡里乌斯是利马一个巨富之家的孩子，孤独、好奇又敏感，在家里萨拉韦里大道上的宅邸、学校（先是圣心学校，后是马卡姆学校）、乡村俱乐部酒店的漫长假期和家里的仆人们之间长大；刚进入少年时，他痛苦地认识了成人世界的残酷。布里斯本人就生长在书中写的那座豪宅里，这本书大半写于巴黎，用尖锐、时而嘲弄的眼光看利马贵族的优雅、虚伪、种族歧视和阶级鸿沟。1972 年获秘鲁国家文学奖，2021 年拍成电影。",
        ["Country Club"], ["乡村俱乐部"],
        "https://es.wikipedia.org/wiki/Un_mundo_para_Julius; https://es.wikipedia.org/wiki/Hotel_Country_Club_de_Lima"),
    b.S("pe-mundo-s1", "el-mundo-es-ancho-y-ajeno", "pe-huamachuco", "The novel as a whole", "全书",
        "The Indigenous community of Rumi, high in the Andes of La Libertad, led by its mayor Rosendo Maqui, defends its land against the landowner Álvaro Amenábar, who with corrupt judges and false witnesses wants it for his estate and its people as labourers for his mines and coca fields. \"Go somewhere else, the world is wide,\" the dispossessors tell them: the world is wide, but for the comuneros it is always alien. Driven up to the stony heights of Yanañahui, the community holds on while many of its members scatter across Peru and suffer brutal exploitation. Alegría wrote it in four months in 1940, in exile in Chile, for a Latin American novel contest run from New York, which it won; it is one of the defining novels of indigenismo and Alegría's masterpiece. Rumi is invented; Alegría was born near Huamachuco.",
        "拉利伯塔德安第斯高山上的原住民村社鲁米，在村长罗森多·马基带领下，保卫自己的土地，对抗庄园主阿尔瓦罗·阿梅纳瓦尔：他靠贪官和假证人要夺走这片地扩大庄园，还想让村民去他的矿场和古柯园做苦工。夺地的人对他们说：“到别处去吧，世界大得很。”世界确实广阔，可对村民来说永远是陌生的。村社被赶到岩石遍布的亚纳纽伊高地，勉强维持下去，许多村民流散到秘鲁各地，受尽残酷剥削。阿莱格里亚 1940 年流亡智利时用四个月写成此书，参加由纽约发起的拉美小说比赛并获头奖；它是原住民主义文学的代表作之一，也是作者的巅峰之作。鲁米是虚构的；阿莱格里亚生在瓦马丘科附近。",
        ["La Libertad", "Huamachuco"], ["拉利伯塔德", "瓦马丘科"],
        "https://es.wikipedia.org/wiki/El_mundo_es_ancho_y_ajeno; https://es.wikipedia.org/wiki/Ciro_Alegr%C3%ADa; https://journal.upao.edu.pe/index.php/PuebloContinente/article/download/533/495/1976; https://beta.acuedi.org/book/2813/pdf; https://mercaba.org/SANLUIS/ALiteratura/Literatura%20Peruana/Alegr%C3%ADa,%20Ciro/El%20mundo%20es%20ancho%20y%20ajeno.PDF"),
    b.S("pe-rios-s1", "los-rios-profundos", "pe-abancay", "The novel as a whole", "全书",
        "Ernesto, fourteen, arrives in Cuzco with his father Gabriel, an itinerant lawyer, to ask a rich relative, \"the Old Man\", for work and protection; refused, they wander on through the towns of the southern Andes. In Abancay his father leaves him as a boarder at a religious school, a cruel and violent sample of Peruvian society, and moves on. Outside its walls the revolt of the chicheras, women who sell maize beer, demanding the hoarded salt, and the mass entry of the Indian colonos of the haciendas into the town to ask for a mass for the victims of a typhus epidemic, open Ernesto's eyes: torn between the Andean world of his childhood and the creole one, he chooses the Andean. The novel ends as he leaves Abancay for the Old Man's hacienda in the Apurímac valley. It is counted Arguedas's masterpiece.",
        "十四岁的埃内斯托跟着当流动律师的父亲加夫列尔来到库斯科，想求一位叫“老头”的富亲戚给份工作、给点庇护；被拒之后，他们继续在南部安第斯的城镇间漂泊。到了阿班凯，父亲把他送进一所教会学校寄宿，自己又上了路；学校里规矩残酷、充满暴力，像秘鲁社会的缩影。在校墙外，卖玉米酒的女人们为分发被囤积的盐而起事，庄园里的印第安佃农为斑疹伤寒的死者成群涌进城要求做弥撒，这些让埃内斯托睁开了眼睛：在童年的安第斯世界和克里奥尔世界之间，他选择了安第斯。小说结尾，他离开阿班凯，去“老头”在阿普里马克河谷的庄园。这本书被看作阿格达斯的代表作。",
        ["Abancay"], ["阿班凯"],
        "https://es.wikipedia.org/wiki/Los_r%C3%ADos_profundos"),
    b.S("pe-mudo-s1", "la-palabra-del-mudo", "pe-huaca-pucllana", "The collected stories, and “Relatos santacrucinos”", "全集及《圣克鲁斯故事》",
        "Ribeyro's collected stories, first gathered in 1972 and enlarged until they held all his books of stories from 1955 to 1992, give a voice to the voiceless of Lima: in \"Los gallinazos sin plumas\" two boys scavenge the city's rubbish dumps at dawn to feed their crippled grandfather's pig; in \"Al pie del acantilado\" a family of squatters settles at the foot of the sea cliffs. The last book, Relatos santacrucinos (1992), goes back to the Miraflores neighbourhood of Santa Cruz where Ribeyro grew up, by the Huaca Pucllana; he said that all his first-person stories of his childhood were true.",
        "里贝罗的短篇全集 1972 年初次结集，后来不断增补，收齐了他 1955 到 1992 年的全部短篇集，为利马说不出话的人发声：《没有羽毛的秃鹫》里，两个男孩天一亮就去城市的垃圾场翻捡，喂瘸腿祖父的猪；《在悬崖脚下》里，一家无地的人在海边悬崖下搭屋安身。最后一本《圣克鲁斯故事》（1992）回到他长大的米拉弗洛雷斯区圣克鲁斯街区，就在普克亚纳神庙旁；他说自己第一人称的童年故事都是真事。",
        ["Miraflores"], ["米拉弗洛雷斯"],
        "https://es.wikipedia.org/wiki/La_palabra_del_mudo; https://en.wikipedia.org/wiki/Julio_Ram%C3%B3n_Ribeyro; https://www.culturagenial.com/es/los-gallinazos-sin-plumas/; https://repositorio.pucp.edu.pe/bitstreams/57a4650b-5486-4aee-bdd8-a7a7e7686020/download; https://elcomercio.pe/eldominical/ninos-personajes-literatura-peruana-noticia-478297; https://www.dlibra.umcs.lublin.pl/Content/44999/download"),
    b.S("pe-inocentes-s1", "los-inocentes-reynoso", "pe-plaza-san-martin", "The book as a whole", "全书",
        "Five stories, each named after one of a gang of teenagers in 1950s Lima: Cara de Ángel, El Príncipe, Carambola, Colorete and El Rosquita, who wander the streets, billiard halls and bars, poor, restless and desperate to prove themselves men. Reynoso wrote them in five months of 1960 and was the first to bring the slang of young people of the big city into 20th-century Peruvian literature, in a prose with a poetic breath; the press called him a pornographer, while José María Arguedas praised the book. Retitled Lima en rock in a later edition, it has been filmed and staged several times. The book mentions the \"living dead\" of the Plaza San Martín.",
        "五个短篇，各以 1950 年代利马一伙少年中的一个命名：天使脸、王子、卡兰博拉、科洛雷特和小圈圈；他们穷，躁动，急着证明自己是男人，在街头、台球厅和酒吧里游荡。雷诺索 1960 年用五个月写成这些故事，第一次把大城市年轻人的黑话带进 20 世纪秘鲁文学，文字里有诗的气息；报界骂他写色情，何塞·马里亚·阿格达斯却称赞这本书。后来的版本改名《利马摇滚》，多次被拍成电影、搬上舞台。书里写到圣马丁广场上的“活死人”。",
        ["Lima", "Plaza San Martín"], ["利马", "圣马丁广场"],
        "https://es.wikipedia.org/wiki/Los_inocentes_(libro); https://revistas.lamolina.edu.pe/index.php/tnu/article/download/2042/2845/6573; https://andina.pe/agencia/galeria-los-inocentes-oswaldo-reynoso-es-llevada-al-teatro-17289.aspx; https://elperuano.pe/noticia/306635-angeles-con-la-cara-sucia; https://trome.com/actualidad/oswaldo-reynoso-lider-collera-15631/"),
    b.S("pe-huerto-s1", "huerto-cerrado", "pe-hotel-paracas", "“Con Jimmy, en Paracas”", "《和吉米在帕拉卡斯》",
        "Bryce's first book: twelve stories about episodes in the life of Manolo, a shy boy and then young man from Lima. In \"Con Jimmy, en Paracas\", thirteen-year-old Manolo goes with his father on a business trip to the luxury resort at Paracas, south of Lima, and there they meet Jimmy, a schoolmate whose family's higher position lets him treat the rules with contempt. The book already holds the themes of all Bryce's later work, shyness and the difficulty of reaching others, love, tenderness and friendship, told with humour and irony; it won an honourable mention in the 1968 Casa de las Américas Prize.",
        "这是布里斯的第一本书：十二个短篇，写利马少年马诺洛（后来是青年）生活里的片段。《和吉米在帕拉卡斯》里，十三岁的马诺洛跟着父亲去利马以南帕拉卡斯的豪华度假酒店出差，在那里碰到同学吉米；吉米家地位更高，他对规矩不屑一顾。布里斯后来作品的主题在书里都已出现：羞怯、和人相处的困难、爱、温柔和友谊，用幽默和反讽来写；1968 年获美洲之家奖荣誉提名。",
        ["Paracas"], ["帕拉卡斯"],
        "https://es.wikipedia.org/wiki/Huerto_cerrado; https://es.wikipedia.org/wiki/Hotel_Paracas"),
    b.S("pe-lituma-s1", "death-in-the-andes", "pe-huancayo", "The novel as a whole", "全书",
        "Corporal Lituma of the Guardia Civil, a man of the coast from Piura, is posted with the young guard Tomás Carreño to Naccos, a remote camp of road-builders by an abandoned mine in the highlands of Junín, at the height of the Shining Path terror. They must find three men who have vanished: the mute Pedrito Tinoco, the albino Casimiro Huarcaya and a foreman living under a false name. The workers say nothing; the innkeepers Dionisio and Adriana talk of the apus, the mountain spirits. Lituma's slow discovery is that the men were sacrificed and eaten by the workers, egged on by the innkeepers, to appease the mountain gods, and thrown down a mine shaft. The novel won the Premio Planeta in 1993. Naccos matches no real place.",
        "国民警卫队下士利图马是皮乌拉海边的人，和年轻警卫托马斯·卡雷尼奥一起被派到纳科斯：胡宁高原上一座废弃矿井旁的偏远筑路工地，正值“光辉道路”恐怖最猖獗的时候。他们要找三个失踪的人：哑巴佩德里托·蒂诺科、白化病人卡西米罗·瓦尔卡亚和一个化名藏身的工头。工人们一言不发，开小酒馆的迪奥尼西奥和阿德里亚娜大谈山神“阿普”。利图马一点点查明：为了平息山神，三人在酒馆夫妇的煽动下被工人们献祭、吃掉，尸骨扔进了矿井。小说获 1993 年行星奖。纳科斯不对应任何真实地点。",
        ["Junín"], ["胡宁"],
        "https://es.wikipedia.org/wiki/Lituma_en_los_Andes; https://revistas.ulima.edu.pe/index.php/lienzo/article/view/1136/1089; https://andina.pe/ingles/noticia-mario-vargas-llosa-estas-son-las-regiones-donde-acontece-su-obra-literaria-746854.aspx"),
]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "books.js"))))
all_places = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "places.js"))))
all_lines = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "lines.js"))))
assert not {x["id"] for x in books} & all_books
assert {p["id"] for p in places} == set(CO) and not set(CO) & all_places
assert not {l["id"] for l in lines} & all_lines
if __name__ == "__main__":
    note = "11-27 selection re-check, rule v2 (add_pe_v2_1127.py)"
    b.append(SA_BOOKS, books, note)
    b.append(b.data("places.js"), places, note)
    b.append(b.data("lines.js"), lines, note)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
