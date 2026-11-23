"""11-23: Italy, fourth pack: 20 more books and 22 more places, to bring the country in line with its weight
(more Dante, Machiavelli, Foscolo, Carducci, Pascoli, Verga, Deledda; the foreign classics of Italy; post-war novels
from the Langhe to Naples and Sicily).

Quotations (17 lines) are cut from Wikisource pages (tools/content/wikisource.py): Italian, French and English
Wikisource; translations of the Italian and French are our own drafts (translation: "own"). Books in copyright have
scene notes in our own words. What a cut changes, named in `checked`: the editor's line numbers in verse are left out;
hard-wrapped French pages have their line ends joined; one note mark in Byron is left out.

Coordinates are those of the place's Italian Wikipedia article (cache/it/coords.json).

Usage: python3 -I add_it4.py <app_dir> <coords.json> <wikisource_root>"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WSR = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-23"
b.init(APP, "", "it", DATE)
W = b.W
ITW = "https://it.wikipedia.org/wiki/"
GAP = b.GAP

def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, pd=True, **kw):
    d = dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
             orig_lang=kw.pop("lang", "it"), public_domain=pd, source_url=kw.pop("src", None), author_orig=author_orig)
    d.update(kw)
    return {k: v for k, v in d.items() if v is not None or k == "source_url"}

def C(pid):
    c = CO[pid]
    return c["lat"], c["lon"], c["st"], c["su"]

def ORIG(pid, name, zh, en_note, zh_note, **kw): return b.ORIG(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PROTO(pid, name, zh, en_note, zh_note, **kw): return b.PROTO(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PIL(pid, name, zh, en_note, zh_note, ids, **kw): return b.PIL(pid, name, zh, *C(pid), en_note, zh_note, ids, **kw)
S = b.S

def raw(title, start, end, lang="it"):
    """the page's own text between two markers; the markers are matched with no-break and thin spaces read as spaces"""
    t = ws.text(os.path.join(WSR, lang), title)
    n = re.sub("[\xa0\u202f\u2009\u2007]", " ", t)
    i = n.find(start)
    assert i >= 0, (title, start)
    j = n.find(end, i)
    assert j >= 0, (title, start, end)
    return t[i:j + len(end)]

def flow(s):
    """a hard-wrapped plain-text page: lines joined, doubled spaces written as one"""
    return re.sub(r" {2,}", " ", s.replace("\n", " "))

def Q(id, book, place, loc, loc_zh, site, title, orig, hl_orig, en, hl_en, zh, hl_zh, note=""):
    if re.search("[\xa0   ]", orig):
        orig = re.sub("[\xa0   ]+", " ", orig)
        orig = re.sub(r" {2,}", " ", orig)
        note += " (no-break and thin spaces written as plain spaces)"
    if re.search(r"(?m)^ +", orig):
        orig = re.sub(r"(?m)^ +", "", orig)
        note += " (verse indent dropped)"
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls:
            assert h in text, (id, h)
    assert "  " not in orig and "[" not in orig, (id, "spacing or page mark")
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh,
                text_orig=orig, highlight_orig=hl_orig, text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh, translation="own",
                status="draft", checked=f"{site} Wikisource, {title}{note}, {DATE}")

IT = lambda t: ws.url("it", t)
IW, EW, FW = "Italian", "English", "French"
NUM = " (the editor's line numbers left out)"
def nums(s):
    s = re.sub(r"(?m)[ \xa0]+\d+$", "", s)
    return re.sub(r"(?m)^([ \xa0]*)\d+(?=\D)", r"\1", s)
def flow(s):
    return re.sub(r" {2,}", " ", s.replace("\n", " "))
T_INF5, T_INF33, T_PUR5 = "Divina Commedia/Inferno/Canto V", "Divina Commedia/Inferno/Canto XXXIII", "Divina Commedia/Purgatorio/Canto V"
T_SG, T_SEP, T_MAC = "Rime nuove/Libro V/Davanti san Guido", "Dei sepolcri (Bettoni 1808)/Dei Sepolcri", "Lettere (Machiavelli)/Lettera XI a Francesco Vettori"
T_CAN, T_XA, T_CAV = "Canne al vento/I", "Myricae/Elegie/X Agosto", "Vita dei campi (1897)/Cavalleria rusticana"
T_DUCH, T_PIC, T_MF = "Bells and Pomegranates, First Series/Italy", "Pictures From Italy/Chapter 5", "The Marble Faun (Hawthorne)/Volume 1/Miriam, Hilda, Kenyon, Donatello"
T_CH4 = "The Works of Lord Byron (ed. Coleridge, Prothero)/Poetry/Volume 2/Childe Harold's Pilgrimage/Canto IV"
T_MC, T_CP = "Le Comte de Monte-Cristo/Chapitre 24", "La Chartreuse de Parme (édition Martineau, 1927)/Chapitre II"
BYRON = "pt-childe-harold"

books = [
    BK("canne-al-vento", "Reeds in the Wind", "风中芦苇", "Canne al vento", "Grazia Deledda", "格拉齐娅·黛莱达", "Grazia Deledda", "1913", src=IT("Canne al vento"),
       aliases=["Canne al vento", "Deledda", "Efix", "Galte", "邪恶之路"]),
    BK("davanti-san-guido", "Before San Guido", "在圣圭多前", "Davanti San Guido", "Giosuè Carducci", "卡尔杜齐", "Giosuè Carducci", "1874", src=IT(T_SG),
       aliases=["Davanti san Guido", "Carducci", "Bolgheri", "i cipressi"]),
    BK("dei-sepolcri", "Of Tombs", "墓地哀思", "Dei sepolcri", "Ugo Foscolo", "乌戈·福斯科洛", "Ugo Foscolo", "1807", src=IT("Dei sepolcri (Bettoni 1808)"),
       aliases=["Dei Sepolcri", "On Sepulchres", "Foscolo", "Santa Croce"]),
    BK("letter-to-vettori", "Letter to Francesco Vettori (10 December 1513)", "致弗朗切斯科·韦托里的信", "Lettera a Francesco Vettori", "Niccolò Machiavelli", "马基雅维利", "Niccolò Machiavelli", "1513",
       src=IT(T_MAC), aliases=["Machiavelli", "The Prince", "Il Principe", "君主论", "Albergaccio"]),
    BK("cavalleria-rusticana", "Cavalleria rusticana", "乡村骑士", "Cavalleria rusticana", "Giovanni Verga", "乔万尼·维尔加", "Giovanni Verga", "1880", src=IT(T_CAV),
       aliases=["Rustic Chivalry", "Turiddu", "Vita dei campi", "Mascagni"]),
    BK("my-last-duchess", "My Last Duchess", "我已故的公爵夫人", None, "Robert Browning", "罗伯特·勃朗宁", "Robert Browning", "1842", lang="en", src=ws.url("en", T_DUCH),
       aliases=["Ferrara", "Browning", "Dramatic Lyrics", "我的前公爵夫人"]),
    BK("pictures-from-italy", "Pictures from Italy", "意大利风光", None, "Charles Dickens", "查尔斯·狄更斯", "Charles Dickens", "1846", lang="en", src=ws.url("en", "Pictures From Italy"),
       aliases=["Dickens in Italy", "Genoa", "Palazzo Peschiere"]),
    BK("count-of-monte-cristo", "The Count of Monte Cristo", "基督山伯爵", "Le Comte de Monte-Cristo", "Alexandre Dumas", "大仲马", "Alexandre Dumas", "1844–1846", lang="fr",
       src=ws.url("fr", "Le Comte de Monte-Cristo"), aliases=["Monte Cristo", "Edmond Dantès", "Dantès", "唐泰斯", "基度山恩仇记"]),
    BK("marble-faun", "The Marble Faun", "玉石雕像", None, "Nathaniel Hawthorne", "纳撒尼尔·霍桑", "Nathaniel Hawthorne", "1860", lang="en", src=ws.url("en", "The Marble Faun (Hawthorne)"),
       aliases=["Transformation", "Donatello", "Miriam", "Hilda", "Faun of Praxiteles"]),
    BK("charterhouse-of-parma", "The Charterhouse of Parma", "帕尔马修道院", "La Chartreuse de Parme", "Stendhal", "司汤达", "Stendhal", "1839", lang="fr",
       src=ws.url("fr", "La Chartreuse de Parme"), aliases=["La Chartreuse de Parme", "Fabrice del Dongo", "Fabrizio", "Grianta", "Lake Como"]),
    BK("fontamara", "Fontamara", "丰塔马拉", "Fontamara", "Ignazio Silone", "伊尼亚齐奥·西洛内", "Ignazio Silone", "1933", pd=False, aliases=["Silone", "Marsica", "Fucino", "cafoni"]),
    BK("day-of-the-owl", "The Day of the Owl", "猫头鹰之日", "Il giorno della civetta", "Leonardo Sciascia", "莱昂纳多·夏侠", "Leonardo Sciascia", "1961", pd=False,
       aliases=["Il giorno della civetta", "Mafia Vendetta", "Sciascia", "Captain Bellodi", "Regalpetra"]),
    BK("moon-and-the-bonfires", "The Moon and the Bonfires", "月亮与篝火", "La luna e i falò", "Cesare Pavese", "切萨雷·帕韦塞", "Cesare Pavese", "1950", pd=False,
       aliases=["La luna e i falò", "Pavese", "Anguilla", "Nuto", "Langhe"]),
    BK("twenty-three-days-of-alba", "The Twenty-Three Days of the City of Alba", "阿尔巴城的二十三天", "I ventitré giorni della città di Alba", "Beppe Fenoglio", "贝佩·费诺利奥", "Beppe Fenoglio", "1952", pd=False,
       aliases=["Fenoglio", "Il partigiano Johnny", "Una questione privata", "partisans", "Langhe"]),
    BK("gomorrah", "Gomorrah", "格莫拉", "Gomorra", "Roberto Saviano", "罗伯托·萨维亚诺", "Roberto Saviano", "2006", pd=False, aliases=["Gomorra", "Camorra", "Saviano", "Scampia", "蛾摩拉"]),
    BK("farewell-to-arms", "A Farewell to Arms", "永别了，武器", None, "Ernest Hemingway", "欧内斯特·海明威", "Ernest Hemingway", "1929", pd=False, lang="en",
       aliases=["Frederic Henry", "Catherine Barkley", "Stresa", "Caporetto", "战地春梦"]),
    BK("that-awful-mess", "That Awful Mess on the Via Merulana", "梅鲁拉纳街上的可怕混乱", "Quer pasticciaccio brutto de via Merulana", "Carlo Emilio Gadda", "卡洛·埃米利奥·加达", "Carlo Emilio Gadda", "1957", pd=False,
       aliases=["Quer pasticciaccio", "Ingravallo", "Gadda", "Via Merulana"]),
    BK("enchanted-april", "The Enchanted April", "迷人的四月", None, "Elizabeth von Arnim", "伊丽莎白·冯·阿尼姆", "Elizabeth von Arnim", "1922", lang="en",
       aliases=["San Salvatore", "Portofino", "Mrs Wilkins", "Lotty"]),
    BK("talented-mr-ripley", "The Talented Mr. Ripley", "天才雷普利", None, "Patricia Highsmith", "帕特里夏·海史密斯", "Patricia Highsmith", "1955", pd=False, lang="en",
       aliases=["Tom Ripley", "Dickie Greenleaf", "Mongibello", "天才里普利先生"]),
    BK("where-angels-fear-to-tread", "Where Angels Fear to Tread", "天使不敢涉足的地方", None, "E. M. Forster", "E. M. 福斯特", "E. M. Forster", "1905", pd=False, lang="en",
       aliases=["Monteriano", "Lilia Herriton", "Gino Carella", "天使不敢踏足"]),
]

places = [
    ORIG("it-galtelli", "Galtellì", "加尔泰利",
         "The village under Monte Tuttavista in the Baronia of eastern Sardinia, with the ruins of a medieval castle above it. Deledda's novel of the decayed Pintor family and their servant Efix is set here under the name Galte, and the village has a literary park named after her",
         "撒丁岛东部巴罗尼亚地区图塔维斯塔山下的村子，上方有中世纪城堡的废墟。黛莱达这部写没落的平托尔家族和仆人埃菲克斯的小说，就以“加尔泰”之名发生在这里；村里有一座以黛莱达命名的文学公园"),
    ORIG("it-bolgheri", "Viale dei Cipressi, Bolgheri", "柏树大道，博尔盖里",
         "The avenue of cypresses, about five kilometres long, that runs from the oratory of San Guido on the Via Aurelia up to the village of Bolgheri. Carducci spent part of his boyhood at Bolgheri; passing the avenue by train years later, he imagined the trees calling him to stay",
         "从奥雷利亚大道旁的圣圭多小礼拜堂一直通到博尔盖里村、长约五公里的柏树大道。卡尔杜齐少年时在博尔盖里住过几年；多年后坐火车经过这里，他想象这些树在呼唤他留下"),
    ORIG("it-albergaccio", "Machiavelli's House (the Albergaccio), Sant'Andrea in Percussina", "马基雅维利故居（“破客栈”），圣安德烈亚因佩尔库西纳",
         "Dismissed from office and exiled from Florence after the return of the Medici in 1512, Machiavelli lived on his small farm here, south of the city. In a letter of 10 December 1513 he described his days in the woods and the tavern and his evenings in the study, where he had just written The Prince",
         "1512 年美第奇家族重返佛罗伦萨后，马基雅维利被免职并逐出城，便住在城南这里的小农庄上。1513 年 12 月 10 日他写信描述了自己白天在树林和小酒馆里的日子，以及夜里在书房里的时光——他刚在那里写完了《君主论》"),
    PIL("it-san-mauro", "San Mauro Pascoli", "圣毛罗帕斯科利",
        "Giovanni Pascoli was born here in 1855; the town took his name in 1932. His father was shot dead on the road home on 10 August 1867, the night of San Lorenzo, and the killing was never solved. The poem 'X Agosto' is about that night",
        "乔万尼·帕斯科利 1855 年生于此地，1932 年小镇改用他的名字。1867 年 8 月 10 日，也就是圣洛伦佐之夜，他的父亲在回家路上被人开枪打死，凶手始终没有查明。《八月十日》写的就是那一夜",
        ["myricae"]),
    PROTO("it-san-gimignano", "San Gimignano ('Monteriano')", "圣吉米尼亚诺（“蒙特里亚诺”）",
          "The Tuscan hill town of medieval towers that Forster saw in 1901; it is taken as the model for 'Monteriano', where the widowed Lilia Herriton marries a young Italian, although the novel also mentions San Gimignano by name",
          "托斯卡纳山城，以中世纪塔楼闻名，福斯特 1901 年来过。它被认为是小说里“蒙特里亚诺”的原型——寡居的莉莉娅·赫里顿就在那里嫁给了一个年轻的意大利人；不过小说里也另外提到了圣吉米尼亚诺这个名字"),
    ORIG("it-castello-estense", "Castello Estense, Ferrara", "埃斯特城堡，费拉拉",
         "The moated castle of the Este dukes. Browning's duke is taken to be Alfonso II d'Este, whose young first wife Lucrezia de' Medici died in 1561 after three years of marriage, and later editions head the poem 'Ferrara'",
         "埃斯特公爵家族的护城河城堡。勃朗宁诗中的公爵一般认为是阿方索二世·德·埃斯特，他的年轻妻子卢克雷齐娅·德·美第奇婚后三年于 1561 年去世；后来的版本给这首诗加了标题“费拉拉”"),
    ORIG("it-peschiere", "Villa delle Peschiere, Genoa", "佩斯基耶雷别墅，热那亚",
         "The sixteenth-century villa on the hill above Genoa's centre, with its terraced gardens and fishponds. Dickens rented it for his family from the autumn of 1844 to the spring of 1845",
         "热那亚市中心上方山坡上的十六世纪别墅，有梯台花园和鱼池。狄更斯 1844 年秋天到 1845 年春天为全家租下了这里"),
    ORIG("it-ponte-sospiri", "Bridge of Sighs, Venice", "叹息桥，威尼斯",
         "The covered bridge of 1600 that carried prisoners from the Doge's Palace to the new prisons across the canal. Byron's opening line made the name famous",
         "1600 年建成的封闭式石桥，把犯人从总督府押送到运河对岸的新监狱。拜伦的诗句让这个名字天下闻名"),
    ORIG("it-montecristo", "Island of Montecristo", "基督山岛",
         "The granite island south of Elba in the Tuscan archipelago, uninhabited apart from wardens and a nature reserve that few may visit. Dumas sailed round it in 1842 and made it the hiding place of the cardinal's treasure that Edmond Dantès finds",
         "托斯卡纳群岛中厄尔巴岛以南的花岗岩小岛，除了管护人员无人居住，是一处很少对外开放的自然保护区。大仲马 1842 年乘船绕岛航行过，把它写成了埃德蒙·唐泰斯找到红衣主教宝藏的地方"),
    ORIG("it-musei-capitolini", "Capitoline Museums, Rome", "卡比托利欧博物馆，罗马",
         "The sculpture galleries on the Capitol, where the Faun of Praxiteles still stands near the Dying Gladiator. Hawthorne saw it in 1858, and his novel begins in front of it",
         "卡比托利欧山上的雕塑陈列馆，普拉克西特列斯的《农牧神》至今还在《垂死的高卢人》附近。霍桑 1858 年在这里见到它，他的小说就从这尊雕像前开始"),
    ORIG("it-pisa-muda", "Torre della Muda (Ugolino's tower), Pisa", "穆达塔（乌哥利诺之塔），比萨",
         "In 1289 Count Ugolino della Gherardesca, accused of betraying Pisa, was walled up in this tower with his sons and grandsons and starved to death. Its remains are built into the Palazzo dell'Orologio on Piazza dei Cavalieri",
         "1289 年，被控背叛比萨的乌哥利诺·德拉·盖拉尔代斯卡伯爵和他的儿孙一起被关进这座塔，活活饿死。塔的残迹今砌在骑士广场的钟楼宫里"),
    ORIG("it-castel-di-pietra", "Castel di Pietra, Maremma", "石堡，马雷玛",
         "A ruined castle on a crag near Gavorrano in the Maremma. Local tradition holds that Pia de' Tolomei, the Sienese lady Dante meets in Purgatory, was killed here by her husband, who threw her from a window",
         "马雷玛地区加沃拉诺附近峭壁上的城堡废墟。当地传说，但丁在炼狱中遇到的锡耶纳贵妇皮娅·德·托洛梅伊就是在这里被丈夫从窗口推下摔死的"),
    PROTO("it-pescina", "Pescina", "佩斯奇纳",
          "Ignazio Silone's native town on the edge of the drained Fucino basin in the Abruzzo; his mother died in the earthquake of 1915. Fontamara, the poor village of the novel, is modelled on the villages of this part of the Marsica",
          "伊尼亚齐奥·西洛内的故乡，在阿布鲁佐已排干的富齐诺盆地边上；他的母亲死于 1915 年的地震。小说里那个穷村子丰塔马拉，就以马尔西卡这一带的村庄为原型",
          book_ids=["fontamara"]),
    PIL("it-racalmuto", "Racalmuto", "拉卡尔穆托",
        "Leonardo Sciascia was born in this Sicilian sulphur town in 1921, wrote about it as 'Regalpetra' and is buried here; a foundation in his name stands in the town. The Day of the Owl, his novel of a Mafia killing and a northern carabinieri captain, is set in an unnamed town of the same Sicily",
        "莱昂纳多·夏侠 1921 年生于这个西西里硫磺矿小镇，以“雷加尔佩特拉”之名写过它，死后也葬在这里；镇上有以他命名的基金会。《猫头鹰之日》写一桩黑手党谋杀案和一位来自北方的宪兵上尉，背景是同一片西西里的一个无名小镇",
        ["day-of-the-owl"]),
    ORIG("it-santo-stefano-belbo", "Santo Stefano Belbo", "圣斯特凡诺贝尔博",
         "Pavese was born here in 1908, in the hills of the Langhe where his family spent their summers. The narrator of his last novel comes back from America to the Belbo valley where he was a foundling and a farmhand",
         "帕韦塞 1908 年生于此地，在朗格丘陵之间，家里每年夏天都来这里。他最后一部小说的叙述者从美国回到贝尔博河谷——他从前当弃儿和雇工的地方"),
    ORIG("it-alba", "Alba", "阿尔巴",
         "The market town of the Langhe. In October 1944 the partisans took it from the Fascist garrison and held it for twenty-three days. Beppe Fenoglio, born here in 1922, fought in those hills and told the story with dry irony",
         "朗格地区的集镇。1944 年 10 月，游击队从法西斯驻军手里夺下这座城，守了二十三天。生于此地（1922 年）的贝佩·费诺利奥就在这一带的山里打过仗，他用冷峻的反讽讲述了这段往事"),
    ORIG("it-scampia", "Vele di Scampia, Naples", "斯坎皮亚“风帆楼”，那不勒斯",
         "The huge sail-shaped housing blocks of the 1960s and 1970s on the northern edge of Naples, which became one of Europe's largest drug markets during the Camorra feud of 2004 and 2005. Most have since been demolished",
         "那不勒斯北郊 1960—1970 年代建造的巨大帆形住宅楼，在 2004—2005 年克莫拉内斗期间成了欧洲最大的毒品市场之一。如今大部分已被拆除"),
    ORIG("it-stresa", "Grand Hotel des Iles Borromées, Stresa", "博罗梅奥群岛大酒店，斯特雷萨",
         "The grand hotel on Lake Maggiore where Hemingway, wounded in 1918, stayed while convalescing. In the novel Frederic Henry, a deserter after the retreat from Caporetto, finds Catherine here, and the two row across the lake to Switzerland by night",
         "马焦雷湖畔的豪华酒店，1918 年受伤的海明威疗养期间在这里住过。小说里，卡波雷托大撤退后开了小差的弗雷德里克·亨利在这里找到了凯瑟琳，两人连夜划船渡湖逃往瑞士"),
    ORIG("it-merulana", "Via Merulana, Rome", "梅鲁拉纳街，罗马",
         "The long straight street between Santa Maria Maggiore and San Giovanni in Laterano. Gadda's detective novel turns on a theft and a murder in the same building, at number 219, in March 1927",
         "从圣母大殿通往拉特朗圣若望大殿的一条笔直长街。加达的侦探小说围绕 1927 年 3 月发生在同一幢楼——219 号——里的一起盗窃案和一起凶杀案展开"),
    PROTO("it-portofino", "Castello Brown, Portofino", "布朗城堡，波托菲诺",
          "Elizabeth von Arnim stayed in this castle above Portofino in 1921, and it is taken for the model of San Salvatore, the medieval castle on the Italian Riviera that four unhappy Englishwomen rent for a month",
          "伊丽莎白·冯·阿尼姆 1921 年住在波托菲诺上方的这座城堡里；它被认为是小说里“圣萨尔瓦多”的原型——四个不快乐的英国女人合租了意大利里维埃拉海岸上的这座中世纪城堡，住了一个月",
          book_ids=["enchanted-april"]),
    PROTO("it-positano", "Positano ('Mongibello')", "波西塔诺（“蒙吉贝洛”）",
          "Highsmith visited Positano in 1951 and later said the novel began there, with the sight of a young man alone on the beach early one morning. It is taken for the model of Mongibello, the village south of Naples where Dickie Greenleaf lives",
          "海史密斯 1951 年到过波西塔诺，后来她说，这部小说的念头就始于某天清晨在这里的海滩上看到一个独自一人的年轻人。它被认为是迪基·格林里夫居住的那个那不勒斯以南小村“蒙吉贝洛”的原型"),
    ORIG("it-griante", "Griante (Grianta), Lake Como", "格里安泰（“格里安塔”），科莫湖",
         "The village above Cadenabbia on Lake Como, which Stendhal calls Grianta; the del Dongo family castle of the novel stands above it, and the young Fabrice spends his boyhood on the lake",
         "科莫湖畔卡德纳比亚上方的村子，司汤达称之为“格里安塔”；小说里德尔·唐戈家族的城堡就在村子上方，少年法布里斯在湖上度过了童年"),
]

lines = [
    Q("it-dc-inf5", "divine-comedy", "it-dante-tomb", "Inferno, canto 5", "《地狱篇》第五歌", IW, T_INF5,
      nums(raw(T_INF5, "Siede la terra dove nata fui", "per aver pace co’ seguaci sui.")), ["la terra dove nata fui"],
      "The town where I was born sits on the shore\nwhere the Po comes down\nto be at peace with all the streams that follow it.",
      ["The town where I was born"],
      "我出生的那座城坐落在海边，\n波河在那里流下，\n同它所有的支流一起归于安宁。",
      ["我出生的那座城"], note=NUM),
    Q("it-dc-inf33", "divine-comedy", "it-pisa-muda", "Inferno, canto 33", "《地狱篇》第三十三歌", IW, T_INF33,
      nums(raw(T_INF33, "Ahi Pisa, vituperio de le genti", "sì ch’elli annieghi in te ogne persona!")), ["Pisa"],
      "Ah Pisa, shame of the peoples\nof the fair land where 'sì' is spoken,\nsince your neighbours are slow to punish you,\nlet Capraia and Gorgona move\nand make a hedge across the mouth of the Arno,\nso that it drowns every soul in you!",
      ["Pisa"],
      "啊，比萨，你是说“是”的美丽国度里\n各族人民的耻辱，\n既然你的邻居们迟迟不惩罚你，\n就让卡普拉亚岛和戈尔戈纳岛移过来，\n在阿诺河口筑起一道堤，\n好让河水淹死你城中的每一个人！",
      ["比萨"], note=NUM),
    Q("it-dc-pur5", "divine-comedy", "it-castel-di-pietra", "Purgatorio, canto 5", "《炼狱篇》第五歌", IW, T_PUR5,
      nums(raw(T_PUR5, "\"ricorditi di me, che son la Pia;", "disposando m’avea con la sua gemma\".")), ["Maremma"],
      "'remember me, who am La Pia;\nSiena made me, Maremma unmade me:\nhe knows it who, having first given me his ring,\nhad wedded me with his gem.'",
      ["Maremma"],
      "“请记住我，我是皮娅；\n锡耶纳生了我，马雷玛毁了我：\n那个先给我戴上戒指、\n用他的宝石娶了我的人知道这件事。”",
      ["马雷玛"], note=NUM),
    Q("it-sg-1", "davanti-san-guido", "it-bolgheri", "Stanzas 1–2", "第一、二节", IW, T_SG,
      nums(raw(T_SG, "I cipressi che a Bólgheri alti e schietti", "Fresca è la sera e a te noto il cammino.")), ["Bólgheri", "San Guido"],
      "The cypresses that at Bolgheri, tall and straight,\nrun from San Guido in a double row,\nlike young giants racing,\nleapt out to meet me and looked at me.\nThey knew me, and, 'Welcome back at last,'\nthey whispered to me with bowed heads,\n'why don't you get down? why don't you stay?\nThe evening is cool and you know the way.'",
      ["Bolgheri", "San Guido"],
      "博尔盖里那些高大挺拔的柏树，\n从圣圭多排成两行，\n像奔跑着的年轻巨人，\n向我扑来，望着我。\n它们认出了我，低着头\n向我轻声说：“你终于回来了——\n为什么不下车？为什么不留下？\n傍晚凉爽，路你也认得。”",
      ["博尔盖里", "圣圭多"], note=NUM),
    Q("it-sep-1", "dei-sepolcri", "it-santa-croce", "Lines 151–158", "第 151—158 行", IW, T_SEP,
      nums(raw(T_SEP, "A egregie cose il forte animo accendono", "Di che lagrime grondi e di che sangue;")), ["L’urne de’ forti"],
      "The tombs of the strong, Pindemonte, kindle\nthe strong mind to noble deeds; and they make\nbeautiful and holy to the pilgrim the earth\nthat holds them. When I saw the monument\nwhere lies the body of that great man\nwho, tempering the sceptre for rulers,\nstrips its laurels and shows the peoples\nwhat tears and what blood it drips with;",
      ["The tombs of the strong"],
      "强者的墓地，品德蒙特啊，\n激励坚强的心灵去成就伟业；\n它们使收容它们的土地\n在朝圣者眼中美丽而神圣。当我看见\n那位伟人安息的墓碑——\n他为君主们锤炼权杖，\n却剥去它的桂冠，向人民揭示\n它滴淌着怎样的泪和血；",
      ["强者的墓地"], note=NUM),
    Q("it-mac-1", "letter-to-vettori", "it-albergaccio", "The letter of 10 December 1513", "1513 年 12 月 10 日信", IW, T_MAC,
      raw(T_MAC, "Venuta la sera, mi ritorno a casa ed entro nel mio scrittoio", "tutto mi transferisco in loro."), ["mio scrittoio"],
      "When evening comes, I return home and go into my study; and at the door I take off my everyday clothes, covered in mud and dirt, and put on the robes of court and palace; and, decently dressed again, I enter the ancient courts of the men of old, where, lovingly received by them, I feed on that food which alone is mine and for which I was born; where I am not ashamed to speak with them and to ask them the reasons for their actions; and they in their kindness answer me; and for four hours I feel no weariness, I forget every trouble, I do not fear poverty, death does not dismay me: I give myself over entirely to them.",
      ["my study"],
      "傍晚时分，我回到家，走进书房；在门口脱下沾满泥污的日常衣服，换上朝廷和宫中的礼服；衣冠整齐之后，我走进古人的庭院，受到他们亲切的款待，享用那唯一属于我、我生来就是为了它的食粮；在那里，我毫不羞愧地同他们交谈，问他们行事的缘由，而他们出于仁慈回答我；四个钟头里，我感觉不到一丝疲倦，忘掉一切烦恼，不怕贫穷，也不畏惧死亡：我把自己整个儿交给了他们。",
      ["书房"]),
    Q("it-can-1", "canne-al-vento", "it-galtelli", "Chapter 1", "第一章", IW, T_CAN,
      raw(T_CAN, "I fantasmi degli antichi Baroni scendevano dalle rovine del castello sopra il paese di Galte", "indicava il loro passaggio."), ["paese di Galte"],
      "The ghosts of the old Barons came down from the ruins of the castle above the village of Galte, on the horizon to Efix's left, and ranged along the banks of the river hunting boar and fox: their weapons glittered among the low alders of the shore, and the faint barking of dogs in the distance marked their passing.",
      ["the village of Galte"],
      "古代男爵们的幽灵从加尔泰村上方的城堡废墟上下来——那废墟就在埃菲克斯左手边的天边——沿着河岸追猎野猪和狐狸：他们的兵器在岸边低矮的桤木丛中闪光，远处隐约的犬吠声标出了他们经过的地方。",
      ["加尔泰村"]),
    Q("it-xa-1", "myricae", "it-san-mauro", "'X Agosto', stanzas 1–2", "《八月十日》第一、二节", IW, T_XA,
      nums(raw(T_XA, "San Lorenzo, io lo so perchè tanto", "la cena de’ suoi rondinini.")), ["San Lorenzo"],
      "Saint Lawrence, I know why so many\nstars burn and fall through the still air,\nwhy so great a weeping\nsparkles in the hollow sky.\nA swallow was flying back to its roof:\nthey killed it: it fell among the thorns:\nit had an insect in its beak:\nthe supper of its little ones.",
      ["Saint Lawrence"],
      "圣洛伦佐啊，我知道为什么\n有那么多星星在宁静的空中燃烧、坠落，\n为什么这样大的哭泣\n在凹形的天空中闪烁。\n一只燕子正飞回屋檐下：\n人们杀了它；它落进荆棘丛里；\n它嘴里衔着一只虫子：\n那是它的雏燕们的晚饭。",
      ["圣洛伦佐"], note=NUM),
    Q("it-cav-1", "cavalleria-rusticana", "it-vizzini", "Opening", "开头", IW, T_CAV,
      raw(T_CAV, "Turiddu Macca, il figlio della gnà Nunzia", "il berretto rosso,"), ["in piazza"],
      "Turiddu Macca, the son of old Nunzia, when he came back from soldiering, strutted about the square every Sunday in his bersagliere uniform and red cap,",
      ["the square"],
      "图里杜·马卡是努恩齐娅大婶的儿子，当兵回来以后，每个星期天都穿着狙击兵的军服、戴着红帽子在广场上神气活现地走来走去，",
      ["广场"]),
    Q("it-mc-1", "count-of-monte-cristo", "it-montecristo", "Chapter 24, 'Dazzlement'", "第二十四章《眼花缭乱》", FW, "Le Comte de Monte-Cristo/Chapitre 24",
      flow(raw("Le Comte de Monte-Cristo/Chapitre 24", "Le soleil était arrivé au tiers de sa course", "Edmond s’y sentait seul sous la main de Dieu.", "fr")), ["l’île était habitée"],
      "The sun had travelled about a third of its course, and its May rays fell warm and life-giving on the rocks, which themselves seemed to feel its heat; thousands of cicadas, invisible in the heather, kept up their monotonous, unbroken murmur; the leaves of the myrtles and olives stirred and shivered with an almost metallic sound; at every step Edmond took on the sun-warmed granite he startled lizards that looked like emeralds; in the distance, on the sloping banks, the wild goats that sometimes draw hunters there could be seen leaping: in a word, the island was inhabited, alive, astir, and yet Edmond felt himself alone under the hand of God.",
      ["the island was inhabited"],
      "太阳大约走完了三分之一的路程，五月的阳光温暖而充满生机地照在岩石上，岩石仿佛也感到了它的热度；成千上万只蝉藏在石楠丛中看不见，不停地发出单调的鸣声；桃金娘和橄榄树的叶子瑟瑟抖动，发出几乎像金属一样的声响；埃德蒙每在晒热的花岗岩上走一步，都会惊起一些像绿宝石般的蜥蜴；远处倾斜的坡上，可以看见野山羊在跳跃，有时猎人们就是为它们而来的：总之，这座岛有生命，有活力，热闹得很，然而埃德蒙觉得自己孤零零地处在上帝的手掌之下。",
      ["这座岛有生命"], note=" (the page's line ends joined)"),
    Q("it-cp-1", "charterhouse-of-parma", "it-griante", "Chapter 2", "第二章", FW, T_CP,
      flow(raw(T_CP, "Il était\nle chef de toutes les grandes expéditions", "quelque arbre voisin du rivage.", "fr")), ["Grianta"],
      "He was the leader of all the great expeditions of the little peasant boys of Grianta and Cadenabbia. These children had got hold of some small keys, and when the night was really dark they would try to open the padlocks of the chains that tie the boats to some big stone or to a tree near the shore.",
      ["Grianta"],
      "他是格里安塔和卡德纳比亚那帮农家孩子一切大行动的头领。这些孩子弄到了几把小钥匙，一到夜色漆黑的时候，就去试着打开挂锁——那些锁把小船的铁链拴在岸边的大石头或树上。",
      ["格里安塔"], note=" (the page's line ends joined)"),
]
# English originals
_d = raw(T_DUCH, "That's my last Duchess painted on the wall,", "and there she stands.", "en")
_p = raw(T_PIC, "There is not in Italy, they say (and I believe them) a lovelier residence than the Palazzo Peschiere", "had ceased and determined.", "en") + "\n" + raw(T_PIC, "It stands on a height within the walls of Genoa", "groves of roses and camelias.", "en")
_m = raw(T_MF, "Four individuals, in whose fortunes we should be glad to interest the reader", "the sculpture-gallery in the Capitol at Rome.", "en")
_b = raw(T_CH4, "I stood in Venice, on the \"Bridge of Sighs;N1\nA Palace", "throned on her hundred isles!", "en")
assert _b.count("N1") == 1; _b = _b.replace("Sighs;N1", "Sighs;")
for t in (_d, _p, _m, _b):
    assert "[" not in t and "\xa0" not in t, t[:40]
def EN(id, book, place, loc, loc_zh, title, text, hl, zh, hl_zh, note=""):
    for h in hl: assert h in text, (id, h)
    for h in hl_zh: assert h in zh, (id, h)
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh, text_en=text, highlight_en=hl, translation="original",
                text_zh=zh, highlight_zh=hl_zh, status="draft", checked=f"English Wikisource, {title}{note}, {DATE}")
lines += [
    EN("it-duch-1", "my-last-duchess", "it-castello-estense", "Lines 1–4", "第 1—4 行", T_DUCH, _d, ["my last Duchess"],
       "那墙上画着的是我已故的公爵夫人，\n看上去她好像还活着。我说，\n这幅画真是个奇迹：潘道夫修士的手\n忙了整整一天，她就站在那里了。",
       ["我已故的公爵夫人"]),
    EN("it-pic-1", "pictures-from-italy", "it-peschiere", "'Genoa and its Neighbourhood'", "《热那亚及其近郊》", T_PIC, _p, ["Palazzo Peschiere", "Genoa"],
       "他们说（我也相信）全意大利再没有比佩斯基耶雷宫——或者说“鱼池宫”——更可爱的住所了。我们在阿尔巴罗那座“粉红监狱”的三个月租期届满之后，就搬到了这里。\n它坐落在热那亚城墙之内的一处高地上，却远离市区；四周是它自己的美丽花园，点缀着雕像、花瓶、喷泉、大理石水池、梯台、橘树和柠檬树夹道的小径，还有成丛的玫瑰和山茶。",
       ["佩斯基耶雷宫", "热那亚"]),
    EN("it-mf-1", "marble-faun", "it-musei-capitolini", "Chapter 1", "第一章", T_MF, _m, ["the Capitol at Rome"],
       "有四个人——我们很愿意让读者关心他们的命运——碰巧站在罗马卡比托利欧山雕塑陈列馆的一间展厅里。",
       ["罗马卡比托利欧山"]),
    EN("it-byron-1", BYRON, "it-ponte-sospiri", "Canto IV, stanza 1", "第四章第一节", T_CH4, _b, ["Bridge of Sighs"],
       "我站在威尼斯的“叹息桥”上，\n一边是宫殿，一边是监狱：\n我看见她的建筑从波涛中升起，\n仿佛魔法师的魔杖一挥而成：\n一千年的岁月展开它们朦胧的翅膀\n环绕着我，一片垂死的荣光\n照着遥远的往昔——那时许多臣属之地\n都仰望着那带翼雄狮的大理石殿堂，\n威尼斯就在那里，端坐在她的百座岛屿之上！",
       ["叹息桥"], note=" (the editor's note mark left out)"),
]
lines += [
    S("it-fon-s1", "fontamara", "it-pescina", "Chapters 1–2", "第一、二章",
      "Fontamara is the poorest village of the Marsica, below the mountain on the edge of the drained Fucino lake. One June evening the electric light is cut off for unpaid bills; the next morning men from the town come to divert the stream that waters the peasants' fields to the land of a new landowner, the 'Impresario', and the cafoni slowly understand that the new government is not on their side.",
      "丰塔马拉是马尔西卡最穷的村子，在已排干的富齐诺湖边的山脚下。六月的一个傍晚，村里的电灯因欠费被掐断；第二天早上，城里来人把浇灌农民田地的那条小溪改道，引到一个新地主——“承包商”——的地里去。这些穷苦农民慢慢明白，新政府并不站在他们这一边。",
      ["Fontamara"], ["丰塔马拉"], W + "Fontamara"),
    S("it-moon-s1", "moon-and-the-bonfires", "it-santo-stefano-belbo", "Chapters 1–3", "第一至三章",
      "Back from America after the war with some money, a man called Anguilla, who was a foundling raised by a poor family on the hill of Gaminella, comes to the village fair in the Belbo valley. With his old friend Nuto, the carpenter and band musician, he walks over the farms where he once worked, and finds the past both unchanged and gone.",
      "战后，一个外号叫“鳗鱼”的人带着一点钱从美国回来，来到贝尔博河谷的村子里赶节。他原是个弃儿，在加米内拉山上一户穷人家里长大。他和老朋友、木匠兼乐队乐手努托一起，走遍了自己当年干过活的那些农庄，发现过去的一切既没有变，又已经消失了。",
      ["the Belbo valley"], ["贝尔博河谷"], W + "The_Moon_and_the_Bonfires"),
    S("it-alba-s1", "twenty-three-days-of-alba", "it-alba", "The title story", "同名短篇",
      "In October 1944 some two thousand partisans take Alba, and a few weeks later a far smaller number lose it again. They march into the town to the bells, hang out flags and make speeches, quarrel over uniforms and requisitioned cars, and then, when the Fascists come back across the river, slip away into the hills.",
      "1944 年 10 月，大约两千名游击队员攻下阿尔巴，几个星期后，又由少得多的人把它丢掉了。他们在钟声中开进城里，挂旗、演讲，为制服和征用来的汽车吵来吵去；等法西斯军队渡河回来，他们又悄悄溜回了山里。",
      ["Alba"], ["阿尔巴"], ITW + "I_ventitré_giorni_della_città_di_Alba"),
    S("it-gom-s1", "gomorrah", "it-scampia", "'The Secessionist War'", "《分离者战争》",
      "Saviano follows the feud of 2004 and 2005 between the Di Lauro clan and the breakaway 'Secessionists' through the housing blocks of Scampia and Secondigliano, where the drug trade has its open-air supermarkets: lookouts on scooters, children as couriers, and a killing almost every day.",
      "萨维亚诺追踪了 2004—2005 年迪劳罗家族同另立门户的“分离派”之间的血战，现场就在斯坎皮亚和塞孔迪利亚诺的住宅楼群里——那里的毒品交易有露天的“超市”：骑摩托的望风者，当信差的孩子，几乎每天都有一桩命案。",
      ["Scampia"], ["斯坎皮亚"], W + "Gomorrah_(book)"),
    S("it-fta-s1", "farewell-to-arms", "it-stresa", "Book 4", "第四部",
      "After the retreat from Caporetto, Frederic Henry jumps into a river to escape being shot by the battle police and makes his way to Stresa, where he finds Catherine Barkley at the hotel. Warned by the barman that he will be arrested in the morning, he rows her the whole night up Lake Maggiore through the rain to Switzerland.",
      "卡波雷托大撤退之后，弗雷德里克·亨利为了躲避战地宪兵的枪决跳进河里逃走，辗转来到斯特雷萨，在酒店里找到了凯瑟琳·巴克利。酒吧侍者警告他第二天早上就会被捕，他便冒雨划了一整夜的船，带着她沿马焦雷湖北上逃往瑞士。",
      ["Stresa"], ["斯特雷萨"], W + "A_Farewell_to_Arms"),
    S("it-merul-s1", "that-awful-mess", "it-merulana", "Chapters 1–3", "第一至三章",
      "In March 1927 the police officer Francesco Ingravallo, a Molisan philosopher of crime, is called to number 219 Via Merulana twice in three days: first to the flat of a countess robbed of her jewels, then to the flat across the landing, where his friend Liliana Balducci lies with her throat cut.",
      "1927 年 3 月，警官弗朗切斯科·因格拉瓦洛——一个来自莫利塞、对犯罪颇有一套哲学的人——三天之内两次被叫到梅鲁拉纳街 219 号：先是一位伯爵夫人的公寓里珠宝被盗，接着是楼道对面的公寓里，他的朋友莉莉亚娜·巴尔杜奇被人割断了喉咙。",
      ["Via Merulana"], ["梅鲁拉纳街"], W + "That_Awful_Mess_on_the_Via_Merulana"),
    S("it-rip-s1", "talented-mr-ripley", "it-positano", "Chapters 6–12", "第六至十二章",
      "Sent from New York by a shipbuilder to bring his son home, Tom Ripley finds Dickie Greenleaf living idly in Mongibello, a fishing village of white houses climbing the hill south of Naples. He makes himself Dickie's friend, then his shadow, and on a boat off San Remo kills him and takes his place.",
      "一位造船商派汤姆·雷普利从纽约去意大利把儿子带回家。汤姆在蒙吉贝洛找到了迪基·格林里夫——那是那不勒斯以南一个白房子沿山坡往上爬的渔村，迪基在那里无所事事地过日子。汤姆先成了迪基的朋友，又成了他的影子，后来在圣雷莫外海的一条小船上杀了他，冒名顶替了他。",
      ["Mongibello"], ["蒙吉贝洛"], W + "The_Talented_Mr._Ripley"),
    S("it-wa-s1", "where-angels-fear-to-tread", "it-san-gimignano", "Chapters 1–2", "第一、二章",
      "Lilia Herriton, a young widow sent to Italy by her in-laws to improve herself, writes home from the little hill town of Monteriano that she is engaged to Gino Carella, the son of a dentist. Her brother-in-law Philip is dispatched from Sawston to stop the marriage and arrives too late.",
      "年轻的寡妇莉莉娅·赫里顿被婆家送到意大利去长长见识，她从小山城蒙特里亚诺写信回家，说自己已经同一个牙医的儿子吉诺·卡雷拉订了婚。她的小叔子菲利普被从索斯顿派去阻止这门婚事，却赶到得太晚了。",
      ["Monteriano"], ["蒙特里亚诺"], W + "Where_Angels_Fear_to_Tread"),
]

ids = lambda name: set(re.findall(r'\{ id: "([^"]+)"', open(b.data(name), encoding="utf-8").read()))
old_books, old_places, old_lines = ids("books.js"), ids("places.js"), ids("lines.js")
new_b, new_p, new_l = {x["id"] for x in books}, {x["id"] for x in places}, {x["id"] for x in lines}
assert len(new_b) == len(books) and len(new_p) == len(places) and len(new_l) == len(lines)
assert not new_b & old_books and not new_p & old_places and not new_l & old_lines, (new_b & old_books, new_p & old_places, new_l & old_lines)
assert new_p == set(CO), new_p ^ set(CO)
bids, pids = new_b | old_books | {BYRON}, new_p | old_places
for l in lines:
    assert l["book_id"] in bids and all(p in pids for p in l["place_ids"]), l["id"]
used = {p for l in lines for p in l["place_ids"]}
for p in places:
    assert p["id"] in used or p.get("book_ids"), p["id"]
    assert all(i in bids for i in p.get("book_ids", [])), p["id"]
covered = {l["book_id"] for l in lines} | {i for p in places for i in p.get("book_ids", [])}
assert not new_b - covered, new_b - covered

if __name__ == "__main__":
    M = "11-23: fourth pack (tools/content/batches/add_it4.py)"
    b.append(b.data("books.js"), books, M)
    b.append(b.data("places.js"), places, M)
    b.append(b.data("lines.js"), lines, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines (", sum(1 for l in lines if l.get("kind") != "scene"), "quotations )")
