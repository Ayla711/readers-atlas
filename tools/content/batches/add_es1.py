"""11-17: Spain, first pack (works before 1900). Books chosen with the scoring rubric (sel/es: RAE Biblioteca Clásica, El Mundo's
100 novels of the 20th century, Babelia's 50 books of 1975-2025, Spanish and international prizes, Goodreads, Bokklubben and
thegreatestbooks.org), with the user's changes: Yerma -> Romancero gitano, La tía Tula -> San Manuel Bueno, plus La sombra del
viento, La plaça del Diamant, La colmena and Luces de bohemia (those go in the second pack, add_es2.py).
Gutenberg is down, so every book gets scene notes for now; the public-domain ones can take quotations later.
Coordinates come from Commons categories or geotagged Commons photos (coords_es1.json).
Usage: python3 -I add_es1.py <app_dir> <coords_es1.json>"""
import json, os, sys
sys.path.insert(0, __file__.rsplit("/", 2)[0])
import batchlib as b
APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
b.init(APP, "", "es", "2026-11-17")
W = b.W
WES = "https://es.wikipedia.org/wiki/"

def BK(id, title, title_zh, title_orig, author, author_zh, year, pd=True, **kw):
    d = dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
             orig_lang=kw.pop("lang", "es"), public_domain=pd, source_url=None)
    d.update(kw)
    return d

def C(pid):
    c = CO[pid]
    return c["lat"], c["lon"], c["st"], c["su"]

def ORIG(pid, name, zh, en_note, zh_note, **kw): return b.ORIG(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PROTO(pid, name, zh, en_note, zh_note, **kw): return b.PROTO(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PIL(pid, name, zh, en_note, zh_note, ids, **kw): return b.PIL(pid, name, zh, *C(pid), en_note, zh_note, ids, **kw)
S = b.S

CERV, LOPE, GALD, PARDO = "Miguel de Cervantes", "Lope de Vega", "Benito Pérez Galdós", "Emilia Pardo Bazán"
books = [
    BK("cantar-de-mio-cid", "The Poem of the Cid", "熙德之歌", "Cantar de mio Cid", "Anonymous", "佚名", "c. 1200",
       aliases=["Poema de mio Cid", "El Cid", "Rodrigo Díaz de Vivar", "熙德"]),
    BK("libro-de-buen-amor", "The Book of Good Love", "真爱之书", "Libro de buen amor", "Juan Ruiz, Archpriest of Hita", "伊塔大司铎胡安·鲁伊斯", "1330–1343",
       author_orig="Juan Ruiz, Arcipreste de Hita", aliases=["Arcipreste de Hita", "Don Carnal", "Doña Cuaresma"]),
    BK("conde-lucanor", "Count Lucanor", "卢卡诺尔伯爵", "El conde Lucanor", "Don Juan Manuel", "唐胡安·曼努埃尔", "1335",
       aliases=["Libro de los ejemplos del conde Lucanor y de Patronio", "Patronio"]),
    BK("la-celestina", "La Celestina", "塞莱斯蒂娜", "La Celestina", "Fernando de Rojas", "费尔南多·德罗哈斯", "1499",
       aliases=["Tragicomedia de Calisto y Melibea", "Calisto", "Melibea", "卡利斯托与梅利维娅"]),
    BK("lazarillo-de-tormes", "Lazarillo de Tormes", "小癞子", "La vida de Lazarillo de Tormes", "Anonymous", "佚名", "1554",
       aliases=["The Life of Lazarillo de Tormes", "托美思河上的小拉撒路"]),
    BK("libro-de-la-vida", "The Book of Her Life", "圣女大德兰自传", "Libro de la vida", "Teresa of Ávila", "阿维拉的特蕾莎", "1565",
       author_orig="Teresa de Jesús", aliases=["Saint Teresa of Avila", "圣女大德兰", "Life of Saint Teresa"]),
    BK("cantico-espiritual", "The Spiritual Canticle", "灵歌", "Cántico espiritual", "John of the Cross", "十字若望", "1578",
       author_orig="San Juan de la Cruz", aliases=["San Juan de la Cruz", "Saint John of the Cross", "圣十字若望", "Noche oscura"]),
    BK("don-quixote", "Don Quixote", "堂吉诃德", "El ingenioso hidalgo don Quijote de la Mancha", CERV, "米格尔·德·塞万提斯", "1605–1615",
       aliases=["Don Quijote", "Sancho Panza", "Dulcinea", "La Mancha", "桑丘·潘沙", "杜尔西内娅", "唐·吉诃德"]),
    BK("novelas-ejemplares", "Exemplary Novels", "惩恶扬善故事集", "Novelas ejemplares", CERV, "米格尔·德·塞万提斯", "1613",
       aliases=["Exemplary Stories", "El coloquio de los perros", "Rinconete y Cortadillo", "双狗对话", "训诫小说集"]),
    BK("fuenteovejuna", "Fuenteovejuna", "羊泉村", "Fuenteovejuna", LOPE, "洛佩·德维加", "1619", aliases=["Fuente Ovejuna"]),
    BK("caballero-de-olmedo", "The Knight from Olmedo", "奥尔梅多的骑士", "El caballero de Olmedo", LOPE, "洛佩·德维加", "1620"),
    BK("burlador-de-sevilla", "The Trickster of Seville", "塞维利亚的嘲弄者", "El burlador de Sevilla y convidado de piedra", "Tirso de Molina", "蒂尔索·德莫利纳", "1630",
       aliases=["Don Juan", "唐璜", "The Stone Guest", "石客"]),
    BK("el-buscon", "The Swindler", "骗子外传", "Historia de la vida del Buscón", "Francisco de Quevedo", "弗朗西斯科·德克维多", "1626",
       aliases=["El Buscón", "Pablos", "Dómine Cabra", "The Life of the Swindler"]),
    BK("alcalde-de-zalamea", "The Mayor of Zalamea", "萨拉梅亚的镇长", "El alcalde de Zalamea", "Pedro Calderón de la Barca", "佩德罗·卡尔德隆·德拉巴尔卡", "1636",
       aliases=["Pedro Crespo"]),
    BK("si-de-las-ninas", "The Maidens' Consent", "姑娘们的允诺", "El sí de las niñas", "Leandro Fernández de Moratín", "莱安德罗·费尔南德斯·德莫拉廷", "1806",
       aliases=["A Daughter's Consent", "女孩们的“是”"]),
    BK("don-alvaro", "Don Álvaro, or the Force of Fate", "唐阿尔瓦罗，或命运的力量", "Don Álvaro o la fuerza del sino", "Duke of Rivas", "里瓦斯公爵", "1835",
       author_orig="Ángel de Saavedra, duque de Rivas", aliases=["La forza del destino", "命运之力"]),
    BK("don-juan-tenorio", "Don Juan Tenorio", "唐璜·特诺里奥", "Don Juan Tenorio", "José Zorrilla", "何塞·索里利亚", "1844",
       aliases=["Doña Inés", "唐璜"]),
    BK("rimas-y-leyendas", "Rhymes and Legends", "抒情诗与传说", "Rimas y leyendas", "Gustavo Adolfo Bécquer", "古斯塔沃·阿道弗·贝克尔", "1858–1871",
       aliases=["El monte de las ánimas", "亡魂山", "Rimas", "Leyendas"]),
    BK("pepita-jimenez", "Pepita Jiménez", "佩皮塔·希梅内斯", "Pepita Jiménez", "Juan Valera", "胡安·瓦莱拉", "1874"),
    BK("sombrero-de-tres-picos", "The Three-Cornered Hat", "三角帽", "El sombrero de tres picos", "Pedro Antonio de Alarcón", "佩德罗·安东尼奥·德阿拉尔孔", "1874",
       aliases=["Tío Lucas", "Frasquita"]),
    BK("trafalgar-galdos", "Trafalgar", "特拉法尔加", "Trafalgar", GALD, "贝尼托·佩雷斯·加尔多斯", "1873",
       aliases=["Episodios nacionales", "民族轶事", "Gabriel Araceli"]),
    BK("fortunata-y-jacinta", "Fortunata and Jacinta", "福尔图娜塔与哈辛塔", "Fortunata y Jacinta", GALD, "贝尼托·佩雷斯·加尔多斯", "1887",
       aliases=["Juanito Santa Cruz"]),
    BK("miau", "Miau", "喵", "Miau", GALD, "贝尼托·佩雷斯·加尔多斯", "1888", aliases=["Ramón Villaamil"]),
    BK("la-regenta", "La Regenta", "庭长夫人", "La Regenta", "Leopoldo Alas, “Clarín”", "莱奥波尔多·阿拉斯（克拉林）", "1884–1885",
       author_orig="Leopoldo Alas «Clarín»", aliases=["Clarín", "克拉林", "Ana Ozores", "Vetusta"]),
    BK("pazos-de-ulloa", "The House of Ulloa", "乌略亚府邸", "Los pazos de Ulloa", PARDO, "埃米莉亚·帕尔多·巴桑", "1886"),
    BK("insolacion", "Midsummer Madness", "中暑", "Insolación", PARDO, "埃米莉亚·帕尔多·巴桑", "1889", aliases=["Sunstroke"]),
    BK("la-barraca", "The Cabin", "茅屋", "La barraca", "Vicente Blasco Ibáñez", "比森特·布拉斯科·伊巴涅斯", "1898", aliases=["The Holding"]),
]

places = [
    ORIG("es-burgos-cathedral", "Burgos Cathedral", "布尔戈斯大教堂",
         "In the Cantar, the exiled Cid rides into Burgos to find every door shut against him on the king's orders. Since 1921 he and his wife Jimena have lain under the crossing of this Gothic cathedral, begun in 1221 and a World Heritage Site; his iron-bound chest hangs in a chapel nearby",
         "《熙德之歌》里，被放逐的熙德骑马进入布尔戈斯，全城家家闭户，因为国王下了禁令。1921 年起，他和妻子希梅娜就合葬在这座哥特大教堂的十字交叉处下方。教堂 1221 年动工，是世界遗产，附近一间礼拜堂还挂着据说属于他的铁箍木箱"),
    PIL("es-hita", "Hita, Guadalajara", "瓜达拉哈拉 · 伊塔",
        "The hill town whose archpriest, Juan Ruiz, wrote the Book of Good Love in the fourteenth century, and signed it with his title. Little is left of its castle and walls but the Arco de Santa María gate; every summer the town stages a medieval festival with scenes from the book",
        "14 世纪写下《真爱之书》的胡安·鲁伊斯就是这座山城的大司铎，他在书里以这个头衔署名。城堡和城墙只剩圣玛利亚城门，每年夏天镇上办中世纪节，上演书里的段落",
        ["libro-de-buen-amor"]),
    PIL("es-penafiel", "Peñafiel", "佩尼亚菲耶尔",
        "Don Juan Manuel, nephew of King Alfonso X and author of Count Lucanor, was Duke of Peñafiel and left his manuscripts to the town's monastery. The long, ship-shaped castle on the ridge above the Duero vineyards was largely rebuilt in the fifteenth century and now houses the province's wine museum",
        "《卢卡诺尔伯爵》的作者唐胡安·曼努埃尔是阿方索十世的侄子，也是佩尼亚菲耶尔公爵，把自己的手稿托付给镇上的修道院。山脊上那座船形的狭长城堡大多是 15 世纪重建的，下面是杜埃罗河谷的葡萄园，城堡里如今是省葡萄酒博物馆",
        ["conde-lucanor"]),
    ORIG("es-huerto-calixto", "Huerto de Calixto y Melibea, Salamanca", "萨拉曼卡 · 卡利斯托与梅利维娅花园",
         "La Celestina never names its city, but Rojas studied law at Salamanca and tradition has long set the play there. This walled garden on the old ramparts above the Tormes is held to be Melibea's, the one Calisto climbs into by a ladder; lovers now hang padlocks on its well",
         "《塞莱斯蒂娜》没有点名是哪座城，但罗哈斯在萨拉曼卡读过法律，历来都认为故事发生在这里。古城墙上这座俯瞰托尔梅斯河的围墙花园，传说就是梅利维娅家的花园，卡利斯托夜里搭梯子翻进来的地方。如今情侣们把锁挂在园中的井栏上"),
    ORIG("es-verraco-salamanca", "Verraco on the Roman Bridge, Salamanca", "萨拉曼卡罗马桥头的石兽",
         "At the head of Salamanca's Roman bridge over the Tormes stands a weathered granite beast, carved by the Iron Age Vettones. Here, in the first chapter of Lazarillo de Tormes, the blind man tells the boy to put his ear to the stone bull and hear a noise inside, then knocks his head against it",
         "萨拉曼卡罗马桥横跨托尔梅斯河，桥头立着一尊风化的花岗岩石兽，是铁器时代维通人的雕刻。《小癞子》第一章里，瞎子叫男孩把耳朵贴在这头石牛上听里面的声响，随即把他的头狠狠撞了上去"),
    ORIG("es-encarnacion-avila", "Monastery of the Incarnation, Ávila", "阿维拉 · 降生隐修院",
         "The Carmelite convent outside Ávila's walls where Teresa entered as a novice in 1535 and lived for nearly thirty years. Her Book of Her Life tells of the illness, doubts and visions of those years, and of the day in 1554 when an image of the wounded Christ turned her life around. The nuns keep her cell and a small museum",
         "阿维拉城墙外的加尔默罗会修院。特蕾莎 1535 年在这里做见习修女，此后住了近三十年。《圣女大德兰自传》写的就是这些年里的病痛、疑惑和神视，以及 1554 年她在一尊伤痕累累的基督像前彻底转变的那一天。修女们保留着她的小室和一座小博物馆"),
    PIL("es-carmelitas-segovia", "Convent of the Discalced Carmelites, Segovia", "塞哥维亚 · 赤足加尔默罗会修院",
        "John of the Cross composed most of the Spiritual Canticle in his head in 1577–78, locked in a cell in the Carmelite priory at Toledo, before escaping over the wall by night. From 1588 he was prior of this friary below Segovia's walls, and he lies in a marble tomb in its church",
        "1577 到 1578 年，十字若望被关在托莱多加尔默罗会修院的小囚室里，《灵歌》的大部分诗节就是在那里默默写成的，后来他趁夜翻墙逃出。1588 年起他在塞哥维亚城墙下的这座修院任院长，如今长眠在修院教堂的大理石墓里",
        ["cantico-espiritual"]),
    ORIG("es-criptana", "Windmills of Campo de Criptana", "坎波德克里普塔纳的风车",
         "A row of white windmills along the Sierra de los Molinos above a La Mancha town. Cervantes only says 'thirty or forty windmills on that plain', but Campo de Criptana has long been taken for the place where Don Quixote charges them as giants. Ten survive, three with machinery from the sixteenth century",
         "拉曼恰小镇上方的磨坊岭，一排白色风车沿山脊排开。塞万提斯只写了“那片原野上有三四十架风车”，但历来都认为堂吉诃德把风车当成巨人冲上去的地方就是坎波德克里普塔纳。如今还留着十架，其中三架保存着 16 世纪的机械"),
    PROTO("es-toboso", "Casa de Dulcinea, El Toboso", "托博索 · 杜尔西内娅之家",
          "The village of Dulcinea, Don Quixote's lady, whom Sancho has never seen. A sixteenth-century farmhouse of the Zarco de Morales family, said to be the home of the real woman behind her, is furnished as a manchego house of Cervantes's time; the town's Cervantes museum collects editions of the novel in many languages",
          "堂吉诃德的意中人杜尔西内娅住在这个村子，桑丘其实从没见过她。镇上一座 16 世纪的扎尔科·德莫拉莱斯家农舍，据说就是她的现实原型的家，如今按塞万提斯时代的拉曼恰民居布置；镇上的塞万提斯博物馆收藏着各种语言的《堂吉诃德》"),
    PIL("es-cervantes-valladolid", "Casa de Cervantes, Valladolid", "巴利亚多利德 · 塞万提斯故居",
        "While Valladolid was briefly Spain's capital, Cervantes lived in this house from 1604 to 1606, the years when the first part of Don Quixote came out. Next door stood the Hospital of the Resurrection, where two dogs talk through a night in his Exemplary Novels. The house is a museum furnished in the style of the time",
        "巴利亚多利德短暂做西班牙首都那几年，塞万提斯 1604 到 1606 年住在这座房子里，《堂吉诃德》第一部正是这时出版的。隔壁原来是复活医院，《惩恶扬善故事集》里两条狗就在那里聊了一整夜。故居如今是按当时风格布置的博物馆",
        ["novelas-ejemplares", "don-quixote"]),
    ORIG("es-fuente-obejuna", "Fuente Obejuna", "丰特奥韦胡纳",
         "A hill town in the north of Córdoba province. In 1476 its people rose against their overlord, the commander Fernán Gómez de Guzmán, and killed him; asked under torture who had done it, they answered only 'Fuenteovejuna'. the townspeople still stage Lope's play in the main square",
         "科尔多瓦省北部的一座山城。1476 年，镇民起来反抗领主费尔南·戈麦斯·德古斯曼骑士团长，把他杀了；受刑审问是谁干的，他们只回答“羊泉村”。镇民至今还会在主广场上演洛佩的这部戏"),
    ORIG("es-olmedo", "Olmedo", "奥尔梅多",
         "A walled town on the Castilian plain, with several Mudéjar brick churches. An old folk song mourned a knight from Olmedo killed at night on the road from Medina del Campo, and Lope built his tragedy on it. A theme park beside the walls retells the story, and a classical theatre festival is held every July",
         "卡斯蒂利亚平原上的一座围城，有多座穆德哈尔风格的砖砌教堂。一首老民谣哀悼一位从梅迪纳德尔坎波回来、夜里在路上被杀的奥尔梅多骑士，洛佩据此写成这部悲剧。城墙边的主题公园重讲这个故事，每年七月还有古典戏剧节"),
    ORIG("es-sevilla", "Seville", "塞维利亚",
         "The port of the Indies, Spain's richest city in the Golden Age, and the home of Don Juan. In Tirso's play the libertine returns here from Naples, kills the Commander of Calatrava, and mocks the dead man's statue in a church, which comes to dinner and drags him to hell. The cathedral, the Alcázar and Santa Cruz quarter are at its heart",
         "黄金世纪通往西印度群岛的港口，西班牙最富的城市，也是唐璜的故乡。蒂尔索的戏里，这个浪荡子从那不勒斯回到这里，杀了卡拉特拉瓦骑士团长，又在教堂里嘲弄死者的石像；石像赴宴，把他拖进地狱。大教堂、王宫和圣十字区就在城中心"),
    PIL("es-hosteria-laurel", "Hostería del Laurel, Seville", "塞维利亚 · 月桂客栈",
        "An inn on the Plaza de los Venerables in the Santa Cruz quarter, where José Zorrilla is said to have stayed and imagined his Don Juan Tenorio, whose first act opens in a Seville tavern during Carnival. It is still a bar and hotel, and a plaque recalls the play",
        "圣十字区尊者广场上的一家客栈。据说何塞·索里利亚曾在这里住过，构思了《唐璜·特诺里奥》，剧本第一幕就开在狂欢节期间塞维利亚的一家酒馆里。这里至今仍是酒吧和旅馆，墙上的牌匾纪念这部戏",
        ["don-juan-tenorio"]),
    ORIG("es-segovia", "Segovia", "塞哥维亚",
         "The city of the Roman aqueduct, and the home town of Quevedo's swindler Pablos, son of a thieving barber and a witch. He is sent to board with the licentiate Cabra, a schoolmaster so mean that his pupils nearly starve. The 28-metre granite arches still stride across the Plaza del Azoguejo",
         "古罗马引水渠所在的城市，也是克维多笔下骗子帕布洛斯的家乡，他父亲是爱偷东西的理发匠，母亲是女巫。他被送到卡夫拉学士家寄宿读书，这位先生吝啬得让学生差点饿死。高 28 米的花岗岩拱券至今跨过阿索盖霍广场"),
    ORIG("es-zalamea", "Zalamea de la Serena", "萨拉梅亚－德拉塞雷纳",
         "An Extremaduran farming town where, in Calderón's play, a company of soldiers is billeted on its way to Portugal in 1580. When the captain abducts and rapes the daughter of Pedro Crespo, a rich peasant, Crespo is elected mayor and has him garrotted. Every August hundreds of townspeople stage the play in the main square",
         "埃斯特雷马杜拉的一个农业小镇。卡尔德隆的戏里，1580 年一队开往葡萄牙的士兵驻扎在这里。上尉劫走并强暴了富裕农民佩德罗·克雷斯波的女儿，克雷斯波当选镇长，下令把他绞死。每年八月，几百名镇民在主广场上演这部戏"),
    ORIG("es-alcala", "Alcalá de Henares", "阿尔卡拉－德埃纳雷斯",
         "The university town east of Madrid where Cervantes was born in 1547. Moratín set his comedy in one of its inns, where sixteen-year-old Paquita, brought from her convent school to marry the 59-year-old Don Diego, meets again the young officer she loves. The university and the old town are a World Heritage Site",
         "马德里以东的大学城，塞万提斯 1547 年生在这里。莫拉廷把这部喜剧放在城里一家客栈：十六岁的帕基塔被从修道院学校接出来，要嫁给 59 岁的唐迭戈，却在这里重逢她爱着的年轻军官。大学和老城是世界遗产"),
    ORIG("es-hornachuelos", "Hornachuelos", "奥尔纳丘埃洛斯",
         "A white village in the Sierra Morena west of Córdoba. In the last act of Don Álvaro, the hero, now a friar at the convent of Los Ángeles in these hills, kills his last enemy and throws himself off a cliff in a storm. Verdi turned the play into La forza del destino; the village is now the gateway to a natural park",
         "科尔多瓦以西莫雷纳山里的一座白色村庄。《唐阿尔瓦罗》最后一幕，主人公已在这片山里的天使修道院当了修士，却在暴风雨中杀死最后一个仇人，从悬崖上纵身跳下。威尔第据此写了歌剧《命运之力》，村子如今是自然公园的入口"),
    ORIG("es-san-juan-duero", "San Juan de Duero and the Monte de las Ánimas, Soria", "索里亚 · 杜埃罗河畔圣胡安修道院与亡魂山",
         "A ruined monastery of the Knights Hospitaller on the left bank of the Duero, with a cloister of interlaced Moorish-style arches. Behind it rises the Monte de las Ánimas, where in Bécquer's legend young Alonso goes on All Souls' night to fetch his cousin's lost blue ribbon and never returns. A riverside walk follows the poet's routes",
         "杜埃罗河左岸的医院骑士团修道院遗址，回廊的拱券交错缠绕，带摩尔风格。背后的山就是亡魂山：贝克尔的传说里，年轻的阿隆索在万灵节夜里上山替表妹找回丢失的蓝丝带，再也没有回来。河边步道沿着诗人走过的路线"),
    PIL("es-cabra", "Cabra, Córdoba", "科尔多瓦 · 卡夫拉",
        "The hill town in the olive country south of Córdoba where Juan Valera was born in 1824. Its streets, fields and gossip went into the unnamed Andalusian village of Pepita Jiménez, where a young seminarian falls in love with the widow his father means to marry.",
        "科尔多瓦以南橄榄种植区的山城，胡安·瓦莱拉 1824 年生在这里。镇上的街道、田野和闲话都写进了《佩皮塔·希梅内斯》里那个没点名的安达卢西亚村子：年轻的神学生爱上了父亲打算娶的寡妇",
        ["pepita-jimenez"]),
    ORIG("es-guadix", "Guadix", "瓜迪克斯",
         "An old bishop's city below the Sierra Nevada, known for its cave houses dug into the soft hills. Alarcón, born here in 1833, set The Three-Cornered Hat in its countryside around 1805: the corregidor schemes to seduce the miller's wife and is outwitted. Falla's ballet made the story famous; the cave district is still lived in",
         "内华达山下的古老主教城，以挖进软土丘的窑洞民居闻名。阿拉尔孔 1833 年生在这里，把《三角帽》放在约 1805 年这里的乡间：地方长官想勾引磨坊主的妻子，反被捉弄。法雅的芭蕾让这个故事出了名，窑洞区至今仍有人住"),
    ORIG("es-trafalgar", "Cape Trafalgar", "特拉法尔加角",
         "A low headland with a lighthouse on the Atlantic coast of Cádiz. Off this cape on 21 October 1805 Nelson's fleet destroyed the French and Spanish fleets. Galdós's first National Episode is told by Gabriel Araceli, a fourteen-year-old ship's boy aboard the Santísima Trinidad, the largest warship of the age",
         "加的斯大西洋岸边一个带灯塔的低矮岬角。1805 年 10 月 21 日，纳尔逊的舰队在这片海面击溃了法国和西班牙联合舰队。加尔多斯《民族轶事》的第一部由十四岁的见习水手加夫列尔·阿拉塞利讲述，他就在当时最大的战舰“至圣三位一体号”上"),
    ORIG("es-cava-san-miguel", "Cava de San Miguel, Madrid", "马德里 · 圣米格尔坑道街",
         "A curving lane below the arches of the Plaza Mayor, its tall houses built against the square's back wall. At number 11, visiting the old shop assistant Estupiñá, Juanito Santa Cruz first sees Fortunata on the stairs, eating a raw egg. The street is now lined with taverns, the mesones of old Madrid",
         "马约尔广场拱廊下一条弯弯的小街，高高的房子靠着广场的后墙而建。《福尔图娜塔与哈辛塔》里，胡安尼托·圣克鲁斯到 11 号看望老伙计埃斯图皮尼亚，在楼梯上第一次见到福尔图娜塔，她正在吃一个生鸡蛋。如今这条街满是老马德里风味的酒馆"),
    ORIG("es-aduana", "Real Casa de la Aduana (Ministry of Finance), Madrid", "马德里 · 皇家海关大楼（财政部）",
         "Sabatini's customs house of 1769 on the Calle de Alcalá, home of the Ministry of Finance since the 1840s. In Miau, Ramón Villaamil, dismissed from the ministry two months short of his pension, haunts its corridors and writes letter after letter pleading to be taken back, while the neighbours call his wife and daughters 'the Miaus'",
         "阿尔卡拉街上萨巴蒂尼 1769 年设计的海关大楼，19 世纪 40 年代起是财政部所在地。《喵》里，拉蒙·比利亚米尔在离领退休金只差两个月时被财政部辞退，从此天天在这里的走廊里转，一封接一封写信求复职；邻居们管他的妻子和女儿叫“喵家”"),
    PROTO("es-oviedo-cathedral", "Oviedo Cathedral", "奥维耶多大教堂",
          "Vetusta, the sleepy provincial capital of La Regenta, is Oviedo, where Clarín lived and taught. The novel opens with the canon Fermín de Pas climbing the tower of this Gothic cathedral to spy on the city through a telescope. A statue of Ana Ozores, the Regenta, now stands in the square in front",
          "《庭长夫人》里那座昏昏欲睡的外省首府维图斯塔，就是克拉林生活和教书的奥维耶多。小说开头，教士费尔明·德帕斯登上这座哥特大教堂的塔楼，用望远镜窥看全城。大教堂前的广场上如今立着庭长夫人安娜·奥索雷斯的雕像"),
    PIL("es-pardo-bazan-house", "Casa-Museo Emilia Pardo Bazán, A Coruña", "拉科鲁尼亚 · 帕尔多·巴桑故居博物馆",
        "The townhouse on Calle Tabernas where Emilia Pardo Bazán was born in 1851, the most important Spanish woman novelist of her century and the author of The House of Ulloa, set in the wolf country of inland Galicia. It now belongs to the Royal Galician Academy and keeps her study, library and portraits",
        "埃米莉亚·帕尔多·巴桑 1851 年出生在塔韦尔纳斯街的这座宅子里。她是 19 世纪西班牙最重要的女小说家，《乌略亚府邸》写的就是加利西亚内陆那片“狼的国度”。宅子如今属于加利西亚皇家学院，保留着她的书房、藏书和肖像",
        ["pazos-de-ulloa", "insolacion"]),
    ORIG("es-san-isidro", "Pradera de San Isidro, Madrid", "马德里 · 圣伊西德罗草地",
         "The meadow across the Manzanares where Madrid has gathered for the feast of its patron saint every 15 May since the eighteenth century, as Goya painted it. In Insolación the widowed Marquesa de Andrade comes to the fair with the charming Andalusian Pacheco, drinks too much in the sun, and falls dizzily in love",
         "曼萨纳雷斯河对岸的草地，18 世纪以来每年 5 月 15 日马德里人都来这里过主保圣人节，戈雅画过当年的盛况。《中暑》里，守寡的安德拉德侯爵夫人和迷人的安达卢西亚人帕切科一起来赶集，在烈日下喝多了，晕乎乎地坠入爱河"),
    ORIG("es-tribunal-aguas", "Water Tribunal, Valencia Cathedral", "瓦伦西亚大教堂 · 水法庭",
         "Every Thursday at noon, at the Apostles' Door of the cathedral, the elected heads of the huerta's eight irrigation canals sit in black smocks to settle water disputes, as they have for a thousand years. In La barraca, the newcomer Batiste is fined here for watering out of turn, on the word of his enemy Pimentó",
         "每周四中午，在大教堂的使徒门前，菜园区八条灌溉渠选出的代表穿着黑罩衫坐成一圈，裁决用水纠纷，这个传统已有上千年。《茅屋》里，外来的巴蒂斯特被仇人皮门托告发不按轮次放水，就在这里被判罚款"),
]

lines = [
    S("cid-s1", "cantar-de-mio-cid", "es-burgos-cathedral", "Cantar I, laisses 3–4", "第一歌，第 3–4 节",
      "Banished by King Alfonso, the Cid rides into Burgos with sixty lances. The townspeople weep at their windows but dare not take him in, for the king has forbidden it on pain of losing everything. At his inn's barred door only a girl of nine comes out to tell him so, and he camps on the sandbank of the Arlanzón outside the town.",
      "被阿方索国王放逐的熙德带着六十名骑士进入布尔戈斯。市民们在窗口落泪，却不敢收留他，因为国王有令，违者家产全没。在他投宿的那家紧闭的门口，只有一个九岁的小女孩出来把话告诉他。他只好在城外阿兰松河的沙洲上扎营。",
      ["Burgos", "a girl of nine"], ["布尔戈斯", "九岁的小女孩"], W + "Cantar_de_mio_Cid"),
    S("lba-s1", "libro-de-buen-amor", "es-hita", "The battle of Don Carnal and Lady Lent", "“肉食先生大战斋期夫人”",
      "In the mock-epic battle of Don Carnal and Lady Lent, Lent sends her challenge and her army of fish against Carnal's sausages, hams and roast meats. Carnal is beaten and imprisoned for the forty days, escapes at Easter, and returns in triumph with Don Amor.",
      "在戏仿史诗的“肉食先生大战斋期夫人”一段里，斋期夫人下战书，率领鱼的大军迎战肉食先生的香肠、火腿和烤肉。肉食先生战败，被关了四十天，复活节时越狱，与爱神先生一起凯旋。",
      ["Don Carnal and Lady Lent"], ["肉食先生大战斋期夫人"], W + "Libro_de_buen_amor"),
    S("luc-s1", "conde-lucanor", "es-penafiel", "Exemplo XXXII", "第三十二则",
      "Three tricksters tell a king they can weave a cloth that cannot be seen by anyone who is not truly his father's son. Afraid of losing his kingdom, the king, then his court and his people, all praise the empty loom, until a groom who has nothing to lose says the king is naked. Andersen's 'Emperor's New Clothes' comes from this tale.",
      "三个骗子对国王说，他们能织一种布，凡不是自己父亲亲生的人都看不见。国王怕丢了王位，跟着整个朝廷和百姓一起夸那台空织机，直到一个无所顾忌的马夫说出国王光着身子。安徒生的《皇帝的新装》就来自这则故事。",
      ["the king is naked"], ["国王光着身子", "皇帝的新装"], W + "The_Emperor%27s_New_Clothes"),
    S("cel-s1", "la-celestina", "es-huerto-calixto", "Acts XIX–XX", "第十九至二十幕",
      "After a night with Melibea in her garden, Calisto hears a scuffle in the street, hurries down the ladder over the wall, slips and falls to his death. Melibea climbs her father's tower, tells him the whole story and throws herself down.",
      "卡利斯托在梅利维娅家的花园里过了一夜，听见街上有打斗声，急忙顺着翻墙的梯子下去，一脚踩空，摔死了。梅利维娅登上父亲的塔楼，把一切告诉父亲，然后纵身跳下。",
      ["ladder over the wall"], ["翻墙的梯子"], W + "La_Celestina"),
    S("laz-s1", "lazarillo-de-tormes", "es-verraco-salamanca", "Tratado I", "第一章",
      "Leaving Salamanca, the blind beggar stops at the stone bull at the end of the bridge and tells the boy to put his ear to it and hear the great noise inside. When Lázaro does, the old man slams his head against the stone and laughs: a blind man's boy must be one point sharper than the devil. Lázaro says he woke up that day.",
      "离开萨拉曼卡时，瞎眼乞丐在桥头的石牛前停下，叫男孩把耳朵贴上去，听听里面的大声响。小拉撒路照做了，老头猛地把他的头撞在石头上，笑着说：给瞎子领路的孩子，得比魔鬼还精一分。小拉撒路说，他就是从那天起醒过来的。",
      ["stone bull"], ["石牛"], W + "Lazarillo_de_Tormes"),
    S("vida-s1", "libro-de-la-vida", "es-encarnacion-avila", "Chapter 9", "第九章",
      "After nearly twenty years of half-hearted prayer at the Incarnation, Teresa walks into the oratory one day in 1554 and sees a statue of Christ covered in wounds, brought in for a feast. Overcome, she throws herself down before it in tears and asks for strength never to offend him again. From then on, she writes, her life changed.",
      "在降生隐修院不冷不热地祈祷了近二十年后，1554 年的一天，特蕾莎走进祈祷室，看见一尊为节日搬来的、满身伤痕的基督像。她心如刀绞，泪流满面地扑倒在像前，求赐力量，永不再冒犯他。她写道，从那以后她的生活变了。",
      ["covered in wounds"], ["满身伤痕"], W + "Teresa_of_%C3%81vila"),
    S("can-s1", "cantico-espiritual", "es-carmelitas-segovia", "Composition, 1577–78", "写作经过，1577–78 年",
      "Kidnapped by friars opposed to his reforms, John is shut for nine months in a tiny cell in the Toledo priory, flogged and half-starved. There, without paper, he composes the first thirty-one stanzas of the Canticle, a dialogue between the soul as bride and her hidden beloved, and memorises them. In August 1578 he escapes by a rope of knotted blankets.",
      "反对他改革的修士们把十字若望绑走，关在托莱多修院一间狭小的囚室里九个月，鞭打他、几乎不给饭吃。他没有纸，就在那里默默写出《灵歌》的前三十一节——作为新娘的灵魂与隐藏的爱人之间的对答，全凭记忆记下。1578 年 8 月，他用打结的毯子结成绳索逃了出去。",
      ["thirty-one stanzas"], ["前三十一节"], W + "Spiritual_Canticle"),
    S("dq-s1", "don-quixote", "es-criptana", "Part I, chapter 8", "上卷第八章",
      "Riding out with Sancho, Don Quixote sees thirty or forty windmills on the plain and takes them for giants. Ignoring Sancho's shouts, he charges the nearest with his lance just as the wind turns the sails, and is flung across the field with his horse. Enchanters, he says, have turned the giants into mills to rob him of his victory.",
      "堂吉诃德和桑丘骑马出行，看见原野上有三四十架风车，把它们当成了巨人。他不顾桑丘的喊叫，挺枪冲向最近的一架，正赶上一阵风转动叶片，连人带马被甩到田里。他说，是魔法师把巨人变成了风车，要夺走他的胜利。",
      ["thirty or forty windmills"], ["三四十架风车"], W + "Don_Quixote"),
    S("dq-s2", "don-quixote", "es-toboso", "Part II, chapter 9", "下卷第九章",
      "At midnight Don Quixote and Sancho ride into the sleeping village of El Toboso to find Dulcinea's palace. Sancho, who has never seen her, leads him through dark streets among barking dogs until they come up against a great building: 'It's the church we've run into, Sancho.'",
      "半夜，堂吉诃德和桑丘骑马进入沉睡的托博索村，寻找杜尔西内娅的宫殿。从没见过她的桑丘领着他在漆黑的街上、在一片狗叫声中摸来摸去，最后撞上一座大建筑——“桑丘，我们撞上的是教堂。”",
      ["It's the church we've run into"], ["我们撞上的是教堂"], WES + "Don_Quijote_de_la_Mancha"),
    S("nov-s1", "novelas-ejemplares", "es-cervantes-valladolid", "The Dialogue of the Dogs", "《双狗对话》",
      "Two guard dogs of the Hospital of the Resurrection in Valladolid, Cipión and Berganza, find one night that they can speak. Berganza tells his life with a slaughterman of Seville, shepherds, a policeman, a witch and travelling players, while Cipión keeps him from straying, in a satire of the whole of Spanish society.",
      "巴利亚多利德复活医院的两条看门狗西皮翁和贝尔甘萨，一天夜里发现自己会说话了。贝尔甘萨讲述自己跟过塞维利亚的屠夫、牧羊人、警官、女巫和流浪戏班的一生，西皮翁不时把他拉回正题，借狗的眼睛讽刺了整个西班牙社会。",
      ["Hospital of the Resurrection"], ["复活医院"], W + "The_Dialogue_of_the_Dogs"),
    S("fov-s1", "fuenteovejuna", "es-fuente-obejuna", "Act III", "第三幕",
      "After the Commander assaults Laurencia on her wedding day, the village rises and kills him. A judge sent by the Catholic Monarchs puts three hundred villagers to torture, even an old man and a boy, but to 'Who killed the Commander?' every one answers only 'Fuenteovejuna, sir.' The king, finding no single culprit, pardons the town.",
      "骑士团长在劳伦西娅的婚礼上对她施暴，全村起来把他杀了。天主教双王派来的法官对三百个村民动刑，连老人和孩子也不放过，可是问到“谁杀了骑士团长？”，每个人都只回答：“羊泉村，大人。”国王找不出哪一个凶手，便赦免了全村。",
      ["Fuenteovejuna, sir"], ["羊泉村，大人"], W + "Fuenteovejuna"),
    S("olm-s1", "caballero-de-olmedo", "es-olmedo", "Act III", "第三幕",
      "Riding home alone by night from the fair at Medina del Campo, Don Alonso hears a peasant singing the old song of the knight who was killed on that road, 'the pride of Medina, the flower of Olmedo'. He rides on, and is shot dead from ambush by his jealous rival Don Rodrigo.",
      "唐阿隆索夜里独自从梅迪纳德尔坎波的集市骑马回家，听见一个农夫唱着那首老歌，唱的是死在这条路上的骑士，“梅迪纳的骄傲，奥尔梅多之花”。他继续往前走，被嫉妒的情敌唐罗德里戈埋伏枪杀。",
      ["the flower of Olmedo"], ["奥尔梅多之花"], WES + "El_caballero_de_Olmedo"),
    S("bur-s1", "burlador-de-sevilla", "es-sevilla", "Act III", "第三幕",
      "In a Seville church Don Juan reads the epitaph on the tomb of Don Gonzalo, the Commander he killed, tugs the statue's beard and mockingly invites it to supper. The stone guest comes, and asks him in return to dine in its chapel. There it takes his hand; Don Juan, burning, begs for a priest too late.",
      "在塞维利亚的一座教堂里，唐璜读着被他杀死的骑士团长唐贡萨洛墓上的碑文，扯了扯石像的胡子，戏谑地请它来吃晚饭。石客真的来了，还回请他到自己的礼拜堂赴宴。在那里石像握住他的手，唐璜浑身着火，要求忏悔，却已太迟。",
      ["invites it to supper"], ["请它来吃晚饭"], W + "El_burlador_de_Sevilla"),
    S("ten-s1", "don-juan-tenorio", "es-hosteria-laurel", "Part I, Act I", "第一部第一幕",
      "On a Carnival night in 1545, in a Seville tavern, Don Juan Tenorio and Don Luis Mejía meet a year after their wager to see who could do more harm, and read out their lists of duels and conquests. Don Juan wins, and raises the stakes: he will seduce a novice in her convent, Doña Inés, and Don Luis's own bride.",
      "1545 年狂欢节的一个夜晚，在塞维利亚的一家酒馆里，唐璜·特诺里奥和唐路易斯·梅希亚一年前打了个赌，比谁能干更多坏事，如今如约见面，各自念出决斗和征服的名单。唐璜赢了，又把赌注加码：他要诱拐修道院里的见习修女唐娜伊内斯，还有唐路易斯自己的未婚妻。",
      ["a Seville tavern"], ["塞维利亚的一家酒馆"], W + "Don_Juan_Tenorio"),
    S("bus-s1", "el-buscon", "es-segovia", "Book I, chapter 3", "第一卷第三章",
      "In Segovia, Pablos is sent as servant to young Don Diego, who boards with the licentiate Cabra, a priest so thin and so stingy that his pupils live on a broth so clear that a chickpea lost in it is chased like treasure. After months of starving, Don Diego's father takes the boys away, and they can barely walk.",
      "在塞哥维亚，帕布洛斯给小少爷唐迭戈当仆人，跟着他寄宿在卡夫拉学士家。这位神父又瘦又吝啬，学生们喝的汤清得见底，汤里漂着一粒鹰嘴豆都要争着去捞。饿了几个月后，唐迭戈的父亲把孩子们接走，他们已经几乎走不动路了。",
      ["licentiate Cabra"], ["卡夫拉学士"], W + "El_Busc%C3%B3n"),
    S("zal-s1", "alcalde-de-zalamea", "es-zalamea", "Act III", "第三幕",
      "Newly elected mayor, Pedro Crespo kneels to beg the captain who has dishonoured his daughter to marry her, offering him all his money. Refused, he arrests him, and when King Philip II arrives to demand the officer back, shows him garrotted in his cell. The king approves the sentence and makes Crespo mayor for life.",
      "刚当选镇长的佩德罗·克雷斯波跪下来，求那个玷污了他女儿的上尉娶她，愿意把家财全给他。遭到拒绝后，他把上尉抓了起来。国王腓力二世赶到要人时，他让国王看到上尉已在牢里被绞死。国王认可了判决，并任命克雷斯波为终身镇长。",
      ["mayor for life"], ["终身镇长"], W + "The_Mayor_of_Zalamea"),
    S("sdn-s1", "si-de-las-ninas", "es-alcala", "Acts I–III", "第一至三幕",
      "At an inn in Alcalá, Don Diego, 59, waits to marry Paquita, 16, whose mother has arranged the match. In the night he overhears that she loves a young officer, who turns out to be his own nephew Carlos. Don Diego gives her up and attacks the custom of forcing girls to say 'yes' out of obedience.",
      "在阿尔卡拉的一家客栈里，59 岁的唐迭戈等着迎娶母亲替她定下亲事的十六岁姑娘帕基塔。夜里他偷听到她爱着一位年轻军官，那人竟是他自己的侄子卡洛斯。唐迭戈放弃了婚事，并痛斥逼姑娘们出于顺从说“是”的风气。",
      ["an inn in Alcalá"], ["阿尔卡拉的一家客栈"], W + "The_Maidens%27_Consent"),
    S("alv-s1", "don-alvaro", "es-hornachuelos", "Act V", "第五幕",
      "Years after accidentally killing Leonor's father, Don Álvaro has become Father Rafael at the convent of Los Ángeles near Hornachuelos. Leonor's brother tracks him down and forces a duel; dying, he stabs his sister, who has lived as a hermit nearby. In a thunderstorm Álvaro curses heaven and throws himself from the cliff.",
      "多年前，唐阿尔瓦罗误杀了莱昂诺尔的父亲，如今他已在奥尔纳丘埃洛斯附近的天使修道院当了拉斐尔神父。莱昂诺尔的哥哥找上门来逼他决斗；哥哥临死前刺死了在附近隐居的妹妹。雷雨中，阿尔瓦罗诅咒上天，从悬崖上跳了下去。",
      ["throws himself from the cliff"], ["从悬崖上跳了下去"], W + "Don_%C3%81lvaro"),
    S("ryl-s1", "rimas-y-leyendas", "es-san-juan-duero", "Leyenda: El monte de las ánimas", "传说《亡魂山》",
      "On All Souls' night, riding back to Soria from a hunt, Beatriz tells her cousin Alonso she has lost the blue ribbon he gave her on the Monte de las Ánimas, where the dead Templars ride. He goes back for it and does not return. At dawn she finds the ribbon, bloodied, on her prayer stool, and the hunters later find his body torn by wolves.",
      "万灵节夜里，打猎归来的贝亚特丽斯在回索里亚的路上对表哥阿隆索说，他送的那条蓝丝带丢在了亡魂山上，传说死去的圣殿骑士在那里出没。阿隆索回去替她找，再也没有回来。天亮时，她发现那条沾着血的丝带就放在自己的祈祷凳上；后来猎人们在山上找到了他被狼撕碎的尸体。",
      ["blue ribbon"], ["蓝丝带"], WES + "El_monte_de_las_%C3%A1nimas"),
    S("pep-s1", "pepita-jimenez", "es-cabra", "Part I, letters", "第一部，书信",
      "Luis de Vargas, a seminarian home in his Andalusian village before his ordination, writes to his uncle the dean about the young widow Pepita Jiménez, whom his father hopes to marry. Letter by letter his learned descriptions of her charity and good sense turn into a confession of love he cannot admit to himself.",
      "神学生路易斯·德巴尔加斯在受神职前回到安达卢西亚老家，写信给当主任司铎的叔叔，讲到父亲想娶的年轻寡妇佩皮塔·希梅内斯。一封接一封，他那些引经据典地称赞她善良明理的描述，渐渐变成了一份连自己都不肯承认的爱的告白。",
      ["writes to his uncle"], ["写信给当主任司铎的叔叔"], W + "Pepita_Jim%C3%A9nez"),
    S("som-s1", "sombrero-de-tres-picos", "es-guadix", "Chapters 20–36", "第二十至三十六章",
      "While the miller Tío Lucas is lured into town on a false summons, the corregidor, in his three-cornered hat, steals into the mill to court Frasquita, falls in the millrace and is left to dry in Lucas's bed. Lucas returns, thinks the worst, puts on the corregidor's clothes and sets off to pay the corregidor's wife a visit in turn.",
      "磨坊主卢卡斯大叔被一纸假传票骗进城，戴三角帽的地方长官趁机溜进磨坊去勾引弗拉斯基塔，却掉进水渠，只好脱下湿衣服躺在卢卡斯的床上。卢卡斯回来，以为最坏的事发生了，便穿上长官的衣服，出发去回访长官夫人。",
      ["three-cornered hat"], ["三角帽"], WES + "El_sombrero_de_tres_picos_(novela)"),
    S("tra-s1", "trafalgar-galdos", "es-trafalgar", "Chapters 10–14", "第十至十四章",
      "Gabriel, a fourteen-year-old orphan from Cádiz, sails as page to an old officer aboard the Santísima Trinidad. He watches the line of British ships cut through the fleet, the masts fall and the decks fill with the dead, and is taken off the sinking ship alive. Years later, as an old man, he tells what he saw.",
      "加夫列尔是加的斯的孤儿，十四岁，作为一位老军官的侍从登上“至圣三位一体号”。他眼看着英国战舰纵队冲断了联合舰队，桅杆倒下，甲板上堆满死尸，最后从正在下沉的船上活着脱身。多年以后，已经年迈的他讲述了自己的所见。",
      ["Santísima Trinidad"], ["至圣三位一体号"], W + "Trafalgar_(novel)"),
    S("fyj-s1", "fortunata-y-jacinta", "es-cava-san-miguel", "Part I, chapter 3", "第一部第三章",
      "Going to visit the sick Estupiñá at number 11 of the Cava de San Miguel, the rich young Juanito Santa Cruz finds a girl in a blue headscarf on the stairs of the poultry shop, sucking a raw egg. That meeting with Fortunata shapes the rest of both their lives and of his marriage to Jacinta.",
      "富家少爷胡安尼托·圣克鲁斯去圣米格尔坑道街 11 号看望生病的埃斯图皮尼亚，在禽蛋铺的楼梯上遇见一个戴浅蓝头巾的姑娘，正在吸一个生鸡蛋。与福尔图娜塔的这次相遇，决定了两人此后的一生，也决定了他和哈辛塔的婚姻。",
      ["raw egg"], ["生鸡蛋"], "http://michaelpeverett.blogspot.com/2021/06/benito-perez-galdos-fortunata-and.html"),
    S("miau-s1", "miau", "es-aduana", "Throughout", "全书",
      "Ramón Villaamil, a conscientious clerk of the Ministry of Finance, has been dismissed two months before he would have earned his pension. Day after day he walks to the ministry, buttonholes officials and writes petitions and reform plans, while his family keeps up appearances on credit and his grandson Luis has visions in which God tells him his grandfather will never be reinstated.",
      "拉蒙·比利亚米尔是财政部一名尽职的职员，在离领退休金只差两个月时被辞退。他天天走到部里，拦住官员，写请愿书和改革方案；家里人靠赊账撑着体面，孙子路易斯则在幻觉中听见上帝告诉他，爷爷永远也复不了职。",
      ["Ministry of Finance"], ["财政部"], WES + "Miau_(novela)"),
    S("reg-s1", "la-regenta", "es-oviedo-cathedral", "Chapter 1", "第一章",
      "'The heroic city was taking its siesta.' On an autumn afternoon in Vetusta, Fermín de Pas, the ambitious canon who rules the town through its confessionals, climbs the cathedral tower and sweeps the streets with a telescope, as if the whole city were his. Soon he will become confessor to Ana Ozores, the young wife of the old ex-judge.",
      "“英雄的城市正在午睡。”维图斯塔的一个秋日午后，靠告解室掌控全城的野心勃勃的教士费尔明·德帕斯登上大教堂的塔楼，用望远镜把街道一一扫过，仿佛整座城都归他所有。不久，他就要成为老前庭长年轻妻子安娜·奥索雷斯的告解神父。",
      ["telescope"], ["望远镜"], W + "La_Regenta"),
    S("pdu-s1", "pazos-de-ulloa", "es-pardo-bazan-house", "Chapters 1–3", "第一至三章",
      "Julián, a timid young priest, rides into the Galician hills to become chaplain at the manor of the Marquis of Ulloa. He finds a ruined house run by the steward Primitivo, whose daughter Sabel is the marquis's mistress, and at supper watches the men make Sabel's small son Perucho drunk on wine for fun.",
      "胆小的年轻神父胡利安骑马进入加利西亚山区，到乌略亚侯爵的府邸当家庭神父。他发现府邸破败不堪，由管家普里米蒂沃把持，管家的女儿萨贝尔是侯爵的情妇；晚饭时，他眼看着男人们为了取乐，把萨贝尔的小儿子佩鲁乔灌醉。",
      ["Galician hills"], ["加利西亚山区"], W + "The_House_of_Ulloa"),
    S("ins-s1", "insolacion", "es-san-isidro", "Chapters 3–6", "第三至六章",
      "On the feast of San Isidro, Asís, a widowed Galician marquise living in Madrid, goes to the fair on the meadow with Diego Pacheco, a charming idle Andalusian she has just met. Among the stalls, the crowds and the dust she drinks wine and liqueurs in the burning sun, faints, and wakes up already half in love.",
      "圣伊西德罗节那天，住在马德里的加利西亚寡妇侯爵夫人阿西丝，和刚认识的迷人的安达卢西亚闲人迭戈·帕切科一起去草地上赶集。在货摊、人群和尘土之间，她在烈日下喝了酒和甜酒，晕倒过去，醒来时已经爱上了他一半。",
      ["feast of San Isidro"], ["圣伊西德罗节"], WES + "Insolaci%C3%B3n_(historia_amorosa)"),
    S("bar-s1", "la-barraca", "es-tribunal-aguas", "Chapter 4", "第四章",
      "Batiste and his family have dared to farm the fields of old Barret, left empty for ten years as a curse on any newcomer. Pimentó, who sets the watering turns, accuses him of opening the sluice out of turn, and on a Thursday at the cathedral's Apostles' Door the Water Tribunal fines him, while the huerta looks on with satisfaction.",
      "巴蒂斯特一家竟敢耕种巴雷特老汉的那片田——它荒了十年，被整个菜园区诅咒，谁来种谁倒霉。负责分配浇水轮次的皮门托告他不按轮次开闸，一个星期四，在大教堂的使徒门前，水法庭判他罚款，围观的菜农们幸灾乐祸。",
      ["Water Tribunal"], ["水法庭"], "https://www.textos.info/vicente-blasco-ibanez/la-barraca/ebook"),
]

HEAD = {"books": "window.RA_DATA = window.RA_DATA || {};\nwindow.RA_DATA.books = [\n",
        "places": "// Each place's admin-1 region is worked out from its coordinates by app.js.\nwindow.RA_DATA = window.RA_DATA || {};\nwindow.RA_DATA.places = [\n",
        "lines": "window.RA_DATA = window.RA_DATA || {};\nwindow.RA_DATA.lines = [\n"}

def write(name, entries, marker):
    path = b.data(name + ".js")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    body = ",\n".join("  " + b.obj(e) for e in entries)
    open(path, "w", encoding="utf-8").write(f"// Spain, hand-written content (tools/content/batches/add_es1.py + add_es2.py, {marker}).\n" + HEAD[name] + body + "\n];\n")

FLAGS = {"es-trafalgar": {"rough_coast": True}}
for x in places:
    x.update(FLAGS.get(x["id"], {}))
if __name__ == "__main__":
    ids = [x["id"] for x in places]
    assert len(ids) == len(set(ids))
    bids = {x["id"] for x in books}
    for l in lines:
        for p in l["place_ids"]: assert p in ids, (l["id"], p)
        assert l["book_id"] in bids, l["id"]
    for x in places:
        for bk in x.get("book_ids", []): assert bk in bids, (x["id"], bk)
    write("books", books, "2026-11-17")
    write("places", places, "2026-11-17")
    write("lines", lines, "2026-11-17")
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
