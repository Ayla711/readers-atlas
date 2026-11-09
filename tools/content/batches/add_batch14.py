"""11-05: coverage check, category 2 — sixteen writers who had no book at all.
Public domain, quoted from the downloaded Project Gutenberg files: Milton, Coleridge, Tennyson, Robert Browning, Spenser,
Dryden, John Clare, Sterne, Carlyle, Cowper; Hedd Wyn (Welsh, no excerpt: his place is the farm where his Black Chair is kept).
Still in copyright, scene notes in our own words: Heaney, Dahl, Pullman, Richard Adams, James Herriot.
Facts from Wikipedia unless the coord source says otherwise; coordinates from Wikipedia, Geograph / Commons locations or an
OS grid reference converted with coordtools/osgrid.py; photos from Commons.
Usage: python3 -I add_batch14.py <app_dir> <pg_texts_dir> <photo_work_dir>"""
import importlib.util, json, re, sys
from PIL import Image
APP, TX, PW = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("b5", __file__.replace("add_batch14.py", "add_batch5.py"))
b5 = importlib.util.module_from_spec(spec)
_argv, sys.argv = sys.argv, [sys.argv[0], APP, TX]
spec.loader.exec_module(b5)
sys.argv = _argv
b5.D = ", 2026-11-05"
append, ORIG, PROTO, PIL, W, G, norm, GAP = b5.append, b5.ORIG, b5.PROTO, b5.PIL, b5.W, b5.G, b5.norm, b5.GAP
GEO = "https://www.geograph.org.uk/photo/"
COM = "https://commons.wikimedia.org/wiki/"
def GG(n, what): return (f"{what} (Geograph photo {n}, subject location)", GEO + str(n))

def V(book, start, n, cut=None, lead_numbers=False):
    """n verse lines from the line containing `start`; footnote markers and line or stanza numbers removed;
    `cut` ends the last line after that text"""
    lines = b5.verse_lines(book, start, n).split("\n")
    out = []
    for l in lines:
        l = re.sub(r"\s*\[[0-9ivxlc:]+\]", "", l)
        if lead_numbers:
            l = re.sub(r"^\d+\s+", "", l)
        out.append(l.rstrip())
    if cut:
        out[-1] = out[-1][:out[-1].index(cut) + len(cut)]
    return "\n".join(out)

def RAW(book, start, end):
    """prose that the editor printed with line numbers in the margin: lines joined, numbers and footnote markers removed"""
    raw = open(f"{TX}/{book}.txt", encoding="utf-8").read().replace("\r", "")
    flat = " ".join(re.sub(r"\s+\d+\s*$", "", l.strip()) for l in raw.split("\n"))
    flat = norm(re.sub(r"\[\d+:\d+\]", "", " ".join(flat.split())))
    i = flat.index(start); j = flat.index(end, i)
    return flat[i:j + len(end)]

def B(id, title, title_zh, author, author_zh, year, pg=None, pd=True, url=None, **kw):
    d = dict(id=id, title=title, title_zh=title_zh, author=author, author_zh=author_zh, year=year, orig_lang=kw.pop("lang", "en"),
             public_domain=pd, source_url=url or (G + str(pg) if pg else None))
    d.update(kw)
    return d
MILTON, COLERIDGE, TENNYSON = ("John Milton", "弥尔顿"), ("Samuel Taylor Coleridge", "柯勒律治"), ("Alfred, Lord Tennyson", "丁尼生")
DAHL, PULLMAN = ("Roald Dahl", "罗尔德·达尔"), ("Philip Pullman", "菲利普·普尔曼")
books = [
    B("paradise-lost", "Paradise Lost", "失乐园", *MILTON, "1667", 26),
    B("comus", "Comus", "科摩斯", *MILTON, "1637", 19819, aliases=["A Masque Presented at Ludlow Castle"]),
    B("kubla-khan", "Kubla Khan", "忽必烈汗", *COLERIDGE, "1816", 29090),
    B("in-memoriam", "In Memoriam A.H.H.", "悼念集", *TENNYSON, "1850", 70950, aliases=["In Memoriam"]),
    B("dramatic-romances", "Dramatic Romances and Lyrics", "戏剧传奇与抒情诗", "Robert Browning", "罗伯特·勃朗宁", "1845", 4253),
    B("prothalamion", "Prothalamion", "婚前曲", "Edmund Spenser", "斯宾塞", "1596", 10602),
    B("annus-mirabilis", "Annus Mirabilis", "奇迹之年", "John Dryden", "德莱顿", "1667", 11488),
    B("clare-poems", "Poems Chiefly from Manuscript", "手稿诗选", "John Clare", "约翰·克莱尔", "1920", 8672),
    B("tristram-shandy", "Tristram Shandy", "项狄传", "Laurence Sterne", "斯特恩", "1759–1767", 1079,
      aliases=["The Life and Opinions of Tristram Shandy, Gentleman"]),
    B("french-revolution", "The French Revolution: A History", "法国革命史", "Thomas Carlyle", "卡莱尔", "1837", 1301),
    B("the-task", "The Task", "任务", "William Cowper", "柯珀", "1785", 3698),
    B("yr-arwr", "The Hero", "英雄", "Hedd Wyn", "赫德·温", "1917", lang="cy", title_orig="Yr Arwr",
      url="https://www.library.wales/discover/digital-gallery/manuscripts/modern-period/yr-arwr-hedd-wyn/", aliases=["Black Chair", "黑椅子"]),
    B("death-of-a-naturalist", "Death of a Naturalist", "一位自然主义者之死", "Seamus Heaney", "谢默斯·希尼", "1966", pd=False),
    B("boy-dahl", "Boy: Tales of Childhood", "好小子：童年故事", *DAHL, "1984", pd=False),
    B("charlie-chocolate-factory", "Charlie and the Chocolate Factory", "查理和巧克力工厂", *DAHL, "1964", pd=False),
    B("northern-lights", "Northern Lights", "北极光", *PULLMAN, "1995", pd=False, aliases=["The Golden Compass", "His Dark Materials", "黄金罗盘", "黑暗物质"]),
    B("amber-spyglass", "The Amber Spyglass", "琥珀望远镜", *PULLMAN, "2000", pd=False, aliases=["His Dark Materials", "黑暗物质"]),
    B("watership-down", "Watership Down", "兔子共和国", "Richard Adams", "理查德·亚当斯", "1972", pd=False, aliases=["沃特希普荒原"]),
    B("if-only-they-could-talk", "If Only They Could Talk", "要是它们会说话", "James Herriot", "吉米·哈利", "1970", pd=False,
      aliases=["All Creatures Great and Small"]),
]

places = [
    PIL("milton-cottage", "Milton's Cottage, Chalfont St Giles", "查尔芬特圣贾尔斯 · 弥尔顿小屋", 51.6305, -0.5728,
        *GG(8063115, "Milton's Cottage, Chalfont St. Giles"),
        "Milton and his wife moved into this cottage in 1665 to escape the plague in London, and he finished Paradise Lost here. It was bought by public subscription in 1887; the ground floor is a museum and the garden is open",
        "1665 年弥尔顿和妻子为躲避伦敦的瘟疫搬进这座小屋，他在这里写完了《失乐园》。1887 年靠公众募捐买下，底层是博物馆，花园对外开放",
        ["paradise-lost", "comus"]),
    PIL("coleridge-cottage", "Coleridge Cottage, Nether Stowey", "下斯托伊 · 柯勒律治小屋", 51.1522, -3.1579, "Coleridge Cottage (Wikipedia)", W + "Coleridge_Cottage",
        "Coleridge rented the cottage from 1797 to 1799 and wrote This Lime-Tree Bower My Prison, The Rime of the Ancient Mariner, Frost at Midnight and part of Christabel here. It has been run by the National Trust since 1909",
        "柯勒律治 1797 至 1799 年租住在这里，写了《这菩提树荫是我的牢房》《古舟子咏》《午夜寒霜》和《克丽斯塔贝尔》的一部分。1909 年起由国民信托管理",
        ["kubla-khan", "wordsworth-poems"]),
    ORIG("porlock", "Porlock", "波洛克", 51.2086, -3.5961, "Porlock (Wikipedia), grid ref SS886467", W + "Porlock",
         "A village on the Exmoor coast. In his preface to Kubla Khan Coleridge says he dreamt the poem in 1797 at a lonely farmhouse between Porlock and Linton, usually placed near Culbone Church, and lost the rest of it when 'a person on business from Porlock' called",
         "埃克斯穆尔海岸边的村庄。柯勒律治在《忽必烈汗》的序言里说，1797 年他在波洛克和林顿之间一座僻静的农舍里梦到这首诗，一般认为那座农舍在卡尔伯恩教堂附近；醒来写到一半，“一位从波洛克来办事的人”上门，其余的诗句就都忘了",
         ),
    PIL("farringford", "Farringford, Isle of Wight", "怀特岛 · 法林福德", 50.6742, -1.5242, *GG(6241203, "Farringford House, once the home of Tennyson"),
        "Tennyson rented Farringford in 1853, bought it in 1856 and kept it as his home until his death in 1892, spending the winters here after he built Aldworth in Sussex. It reopened as a historic house in 2017, with guided tours from April to October",
        "丁尼生 1853 年租下法林福德，1856 年买下，此后一直以这里为家，直到 1892 年去世；他在苏塞克斯盖了奥尔德沃斯之后，冬天仍回这里住。2017 年修复后作为历史名宅开放，4 月到 10 月有导览",
        ["in-memoriam"]),
    ORIG("clevedon-st-andrews", "St Andrew's Church, Clevedon", "克利夫登 · 圣安德鲁教堂", 51.4332, -2.8737,
         "St Andrew's Church, Clevedon (Wikipedia)", W + "St_Andrew%27s_Church,_Clevedon",
         "The old church on a hill above the Bristol Channel, where the Severn estuary meets the sea. Arthur Hallam, Tennyson's closest friend and the A.H.H. of In Memoriam, is buried here",
         "布里斯托尔海峡边小山上的老教堂，塞文河口就在这里入海。丁尼生最好的朋友阿瑟·哈勒姆，也就是《悼念集》标题里的 A.H.H.，葬在这里",
         rough_coast=True),
    PIL("st-marylebone-church", "St Marylebone Parish Church", "圣马里波恩教区教堂", 51.5227, -0.1523,
        "St Marylebone Parish Church (Wikipedia), grid ref TQ 28285 82034", W + "St_Marylebone_Parish_Church",
        "Robert Browning and Elizabeth Barrett were married here in 1846. When the church reopened after war damage in 1949 it made a Browning Chapel to mark the wedding, and the parish still keeps their marriage certificate",
        "罗伯特·勃朗宁和伊丽莎白·巴雷特 1846 年在这里结婚。教堂在战争中受损，1949 年重新开放时设了一间勃朗宁礼拜堂纪念这场婚礼，教区至今保存着他们的结婚证书",
        ["dramatic-romances"]),
    ORIG("temple-church", "Temple Church and the Temple", "圣殿教堂与圣殿区", 51.5132, -0.1106,
         "Temple Church (Commons photo 'Temple Church 5, London, UK - Diliff', camera location)", COM + "File:Temple_Church_5,_London,_UK_-_Diliff.jpg",
         "The round church the Knights Templar built as their English headquarters, consecrated in 1185. The Temple around it, between Fleet Street and the Thames, now belongs to two Inns of Court, Inner Temple and Middle Temple: the lawyers who, as Spenser says, took the Templars' place",
         "圣殿骑士团在英格兰的总部教堂，圆形，1185 年祝圣。周围舰队街和泰晤士河之间的圣殿区，现在属于内殿和中殿两所律师学院——正是斯宾塞诗里取代了圣殿骑士的“好学的律师”"),
    PIL("clare-cottage", "John Clare Cottage, Helpston", "赫尔普斯顿 · 约翰·克莱尔小屋", 52.6339, -0.3447, *GG(3945475, "John Clare Cottage, Helpston"),
        "Clare was born in 1793 in this thatched cottage at 12 Woodgate. The fields and commons around Helpston, and their enclosure, run all through his poems; he is buried in St Botolph's churchyard in the village. The John Clare Trust bought the cottage in 2005 and has restored it",
        "克莱尔 1793 年生在林门街 12 号这座茅草屋里。赫尔普斯顿周围的田野、公地，以及公地被圈占的经过，贯穿他的诗；他葬在村里的圣博托尔夫教堂墓园。约翰·克莱尔基金会 2005 年买下小屋并加以修复，现在对外开放",
        ["clare-poems"]),
    # coordinates of the next seven are set below from their photo sources
    PIL("shandy-hall", "Shandy Hall, Coxwold", "考克斯沃尔德 · 项狄府", 54.1887, -1.1875, "Shandy Hall (Wikipedia)", W + "Shandy_Hall",
        "Sterne lived here from 1760 to 1768 as curate of Coxwold and wrote the later volumes of Tristram Shandy and A Sentimental Journey here; the first two volumes were already out. Run by the Laurence Sterne Trust and open to visitors",
        "斯特恩 1760 至 1768 年在考克斯沃尔德当牧师，住在这里，写了《项狄传》后面几卷和《感伤的旅行》；《项狄传》头两卷在他搬来以前已经出版。现由劳伦斯·斯特恩基金会管理，对外开放",
        ["tristram-shandy"]),
    PIL("carlyles-house", "Carlyle's House, Chelsea", "切尔西 · 卡莱尔故居", 0, 0, "", "",
        "Thomas and Jane Carlyle lived at 24 Cheyne Row from 1834 until his death in 1881. He wrote The French Revolution and most of his later work here. Owned by the National Trust",
        "托马斯和简·卡莱尔 1834 年搬进切恩街 24 号，一直住到他 1881 年去世。他在这里写了《法国革命史》和此后的大部分作品。现归国民信托所有",
        ["french-revolution"]),
    PIL("cowper-museum", "Cowper and Newton Museum, Olney", "奥尔尼 · 柯珀与牛顿博物馆", 0, 0, "", "",
        "Cowper lived at Orchard Side, on the Market Place, from 1768 to 1786. With the curate John Newton, who wrote Amazing Grace, he wrote the Olney Hymns, and in 1783 he began The Task, which looks out over the Ouse valley around the town. The house is now the Cowper and Newton Museum",
        "柯珀 1768 至 1786 年住在集市广场边的果园居。他和写《奇异恩典》的牧师约翰·牛顿合写了《奥尔尼圣诗》，1783 年又开始写长诗《任务》，诗里的风景就是小镇周围的乌斯河谷。房子现在是柯珀与牛顿博物馆",
        ["the-task"]),
    PIL("yr-ysgwrn", "Yr Ysgwrn, Trawsfynydd", "特劳斯维尼兹 · 伊斯古恩农场", 0, 0, "", "",
        "The hill farm in Cwm Prysor where Hedd Wyn (Ellis Humphrey Evans) grew up. He was killed at Passchendaele on 31 July 1917; later that year his awdl Yr Arwr won the chair at the National Eisteddfod, and the empty chair was draped in black. The Black Chair is kept here, and the Snowdonia National Park bought the farm for the nation in 2012",
        "普里索谷里的山间农场，赫德·温（本名埃利斯·汉弗莱·埃文斯）在这里长大。他 1917 年 7 月 31 日战死在帕斯尚尔；同年晚些时候，他的长诗《英雄》在全国诗歌节上获得诗人椅，空着的椅子盖上了黑布。这把“黑椅子”就保存在农场里；2012 年斯诺登尼亚国家公园代表国家买下了这里",
        ["yr-arwr"]),
    PIL("heaney-homeplace", "Seamus Heaney HomePlace, Bellaghy", "贝拉希 · 谢默斯·希尼故里中心", 54.8078, -6.5211, "Seamus Heaney HomePlace (Wikipedia)", W + "Seamus_Heaney_HomePlace",
        "An arts centre about Heaney's life and work, opened in 2016 in Bellaghy, where his family moved in 1953. He was born in 1939 at Mossbawn, the family farm near Castledawson, and is buried in St Mary's churchyard in the village, under the words 'Walk on air against your better judgement'",
        "介绍希尼生平和作品的艺术中心，2016 年在贝拉希开幕；他家 1953 年搬到这个村子。他 1939 年生在卡斯尔道森附近的家族农场莫斯鲍恩，葬在村里的圣玛利亚教堂墓园，墓碑上写着“不顾理智，在空中行走”",
        ["death-of-a-naturalist"]),
    PIL("dahl-museum", "Roald Dahl Museum and Story Centre, Great Missenden", "大米森登 · 罗尔德·达尔博物馆", 0, 0, "", "",
        "Dahl lived at Gipsy House in Great Missenden for 36 years, until his death in 1990. The museum, in an old coaching inn on the High Street, opened in 2005 and holds his papers",
        "达尔在大米森登的吉普赛屋住了 36 年，直到 1990 年去世。博物馆设在高街上一座旧驿站客栈里，2005 年开幕，收藏着他的手稿和文件",
        ["boy-dahl", "charlie-chocolate-factory"]),
    ORIG("llandaff-sweetshop", "The sweet shop, 11 High Street, Llandaff", "兰达夫 · 高街 11 号糖果店", 51.4940, -3.2187, "11 High Street, Llandaff (Wikipedia)", W + "11_High_Street,_Llandaff",
         "The sweet shop of the Great Mouse Plot in Boy. In 1924 seven-year-old Dahl and four friends put a dead mouse in a jar of gobstoppers here; the shopkeeper became Mrs Pratchett in the book. A blue plaque went up in 2009",
         "《好小子》里“老鼠大阴谋”发生的糖果店。1924 年，七岁的达尔和四个伙伴把一只死老鼠放进了这里的硬糖罐；店主后来成了书里的普拉切特太太。2009 年挂上了蓝色纪念牌"),
    PROTO("repton-school", "Repton School", "雷普顿公学", 52.8409, -1.5510, "Repton School (Wikipedia)", W + "Repton_School",
          "Not the factory itself: at Repton in the 1930s Dahl and the other boys tested new Cadbury chocolate bars, and he dreamed of working as an inventor for Cadbury. He said this was where Charlie and the Chocolate Factory came from",
          "不是工厂本身：1930 年代达尔在雷普顿上学时，和同学们一起替吉百利试吃新出的巧克力，他梦想将来给吉百利发明巧克力。他说《查理和巧克力工厂》就是从这里来的"),
    PROTO("exeter-college-jordan", "Exeter College, Oxford", "牛津 · 埃克塞特学院", 51.7539, -1.2560, "Exeter College, Oxford (Wikipedia)", W + "Exeter_College,_Oxford",
          "Pullman's own college and the model for Jordan College, which stands where Exeter does and is laid out like it, only bigger, richer and older",
          "普尔曼自己读书的学院，也是乔丹学院的原型：乔丹学院的位置和布局都照着它，只是更大、更富、更古老"),
    ORIG("botanic-garden-bench", "The bench in the Oxford Botanic Garden", "牛津植物园 · 长椅", 51.7506, -1.2483,
         "University of Oxford Botanic Garden (Wikipedia)", W + "University_of_Oxford_Botanic_Garden",
         "Britain's oldest botanic garden, founded in 1621. The bench at the back of the garden, where Will and Lyra promise to sit every Midsummer's Day, has become a place of pilgrimage for readers; a sculpture by Julian Warren has stood behind it since 2019",
         "英国最古老的植物园，建于 1621 年。园子后面那张长椅——威尔和莱拉约定每年仲夏日去坐的地方——成了读者的朝圣地；2019 年起，长椅后面立着朱利安·沃伦的雕塑"),
    ORIG("watership-down-hill", "Watership Down", "沃特希普高地", 0, 0, "", "",
         "A chalk down in north Hampshire, near Kingsclere, that gives the novel its name. The rabbits' journey starts at Sandleford, south of Newbury",
         "汉普郡北部金斯克莱尔附近的白垩丘陵，小说就以它命名。兔子们的旅程从纽伯里南边的桑德福德出发"),
    PIL("herriot-thirsk", "The World of James Herriot, Thirsk", "瑟斯克 · 吉米·哈利的世界", 0, 0, "", "",
        "Alf Wight, who wrote as James Herriot, lived and practised as a vet at 23 Kirkgate; in the books it is Skeldale House, and Darrowby is a mix of Thirsk, Richmond, Leyburn and Middleham. The house opened as a museum in 1999",
        "以吉米·哈利（James Herriot）为笔名写作的阿尔夫·怀特，住在柯克盖特 23 号并在这里行医；书里它是斯凯尔代尔宅，达罗比镇则是瑟斯克、里士满、莱伯恩和米德尔赫姆几个小镇的合体。1999 年改为博物馆开放",
        ["if-only-they-could-talk"]),
]

def L(id, book, place, loc, loc_zh, text, hl, pg):
    for h in hl:
        assert h in text, (id, h)
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh, text_en=text, highlight_en=hl,
                translation="original", status="draft", checked=f"Project Gutenberg #{pg}{b5.D}")
lines = [
    L("comus-1", "comus", "ludlow", "The Attendant Spirit's opening speech (performed at Ludlow Castle, 1634)", "开场守护精灵的独白（1634 年在拉德洛城堡演出）",
      V(19819, "And all this tract that fronts the falling sun", 4), ["this tract that fronts the falling sun"], 19819),
    L("kk-1", "kubla-khan", "porlock", "Preface", "序言",
      RAW(29090, "In the summer of the year 1797, the Author", "Somerset and Devonshire.") + GAP +
      RAW(29090, "At this moment he was unfortunately called out", "without the after restoration of the latter!"), ["Porlock"], 29090),
    L("imm-1", "in-memoriam", "clevedon-st-andrews", "Section 19", "第 19 首",
      V(70950, "The Danube to the Severn gave", 8), ["Severn", "Wye"], 70950),
    L("pro-1", "prothalamion", "temple-church", "Stanza 8", "第 8 节",
      V(10602, "At length they all to mery London came", 10), ["Templer Knights", "Themmes", "mery London"], 10602),
    L("am-1", "annus-mirabilis", "pudding-lane", "Stanzas 212 and 216–217", "第 212 节、第 216—217 节",
      V(11488, "212 Yet London, empress of the northern clime", 4, lead_numbers=True) + GAP +
      V(11488, "216 The diligence of trades and noiseful gain", 8, lead_numbers=True), ["London", "seeds of fire"], 11488),
    L("rem-1", "clare-poems", "clare-cottage", "Remembrances, stanza 7", "《回忆》第 7 节",
      V(8672, "By Langley Bush I roam, but the bush hath left its hill", 10), ["Langley Bush", "Enclosure"], 8672),
    L("task-1", "the-task", "cowper-museum", "Book 1, The Sofa", "第一卷《沙发》",
      V(3698, "Here Ouse, slow winding through a level plain", 4, cut="Delighted."), ["Ouse"], 3698),
]
def S(id, book, place, loc, loc_zh, en, zh, hl_en, hl_zh):
    for h in hl_en: assert h in en, (id, h)
    for h in hl_zh: assert h in zh, (id, h)
    return dict(id=id, kind="scene", book_id=book, place_ids=[place], location=loc, location_zh=loc_zh, text_en=en, text_zh=zh,
                highlight_en=hl_en, highlight_zh=hl_zh, status="draft")
lines += [
    S("dn-s1", "death-of-a-naturalist", "heaney-homeplace", "Digging", "《挖掘》",
      "In the book's first poem, the poet sits at his desk and hears his father digging in the flowerbeds below the window. He remembers his father lifting potatoes and his grandfather cutting turf on the bog; he has no spade to follow them with, so he will dig with his pen.",
      "诗集的第一首。诗人坐在书桌前，听见窗下父亲在花圃里挖土，想起父亲当年挖土豆、祖父在泥炭沼里切泥炭。他没有铁锹可以接着干，就决定用笔来挖。",
      ["dig with his pen"], ["用笔来挖"]),
    S("boy-s1", "boy-dahl", "llandaff-sweetshop", "The Great Mouse Plot", "《老鼠大阴谋》",
      "To get even with Mrs Pratchett, the bad-tempered woman who keeps the sweet shop in Llandaff, seven-year-old Roald and his friends slip a dead mouse into her jar of gobstoppers. She finds out who did it, and the boys are caned at school.",
      "兰达夫糖果店的普拉切特太太脾气很坏，七岁的罗尔德和伙伴们为了报复她，把一只死老鼠塞进了她的硬糖罐。她查出是谁干的，几个孩子在学校挨了鞭子。",
      ["Llandaff"], ["兰达夫"]),
    S("cf-s1", "charlie-chocolate-factory", "repton-school", "Chapters 1–12", "第 1—12 章",
      "Charlie Bucket, who lives in poverty within sight of Willy Wonka's chocolate factory, finds the last of the five Golden Tickets and wins a tour of the factory.",
      "家境贫寒的查理·巴克特就住在望得见威利·旺卡巧克力工厂的地方。他找到了五张金奖券里的最后一张，赢得参观工厂的机会。",
      ["chocolate factory"], ["巧克力工厂"]),
    S("nl-s1", "northern-lights", "exeter-college-jordan", "Chapter 1", "第 1 章",
      "Lyra Belacqua, who has grown up running wild about Jordan College, sneaks into a room no girl is allowed in and watches the Master put poison in the wine meant for her uncle, Lord Asriel.",
      "在乔丹学院里野惯了的莱拉·贝拉克瓦溜进一间女孩不许进的房间，看见院长往给她叔叔阿斯里尔勋爵准备的酒里下毒。",
      ["Jordan College"], ["乔丹学院"]),
    S("as-s1", "amber-spyglass", "botanic-garden-bench", "Chapter 38", "第 38 章",
      "Will and Lyra learn that each must live in their own world and that they can never meet again. Before they part they promise that every Midsummer's Day, at noon, each will sit for an hour on the same bench in the Botanic Garden of their own Oxford.",
      "威尔和莱拉得知两人只能各自回到自己的世界，再也不能相见。分别前他们约定：每年仲夏日中午，各自到自己那个牛津的植物园，在同一张长椅上坐一个小时。",
      ["Botanic Garden"], ["植物园"]),
    S("wd-s1", "watership-down", "watership-down-hill", "Part 1", "第一部",
      "Warned by Fiver's vision of disaster, a small band of rabbits leaves the Sandleford warren and crosses the Hampshire countryside to Watership Down, a high, lonely hill where they mean to make a new home.",
      "小五预感到大祸临头，一小群兔子离开桑德福德的养兔场，穿过汉普郡的乡野，来到又高又僻静的沃特希普高地，打算在那里安家。",
      ["Watership Down"], ["沃特希普高地"]),
    S("ioc-s1", "if-only-they-could-talk", "herriot-thirsk", "Chapters 1–2", "第 1—2 章",
      "Newly qualified, James Herriot arrives in the Yorkshire Dales town of Darrowby to be assistant to the vet Siegfried Farnon, and is soon up to his shoulder in difficult calvings on hill farms.",
      "刚拿到执照的吉米·哈利来到约克郡谷地的达罗比镇，给兽医西格弗里德·法农当助手，很快就在山间农场里给难产的母牛接生，胳膊伸进去一直到肩膀。",
      ["Darrowby"], ["达罗比"]),
]

COORDS = json.load(open(f"{PW}/coords.json", encoding="utf-8"))   # {place_id: [lat, lon, source_text, source_url]} for the seven set from photo sources
for p in places:
    if p["id"] in COORDS:
        la, lo, st, su = COORDS[p["id"]]
        p["lat"], p["lon"] = la, lo
        p["coord_checked"] = f"{st} — {su}{b5.D}"
    assert p["lat"] and p["coord_checked"].split(" — ")[1].startswith("http"), p["id"]

PHOTOS = json.load(open(f"{PW}/choice.json", encoding="utf-8"))   # {place_id: [candidate_no, alt_en, alt_zh, crop or null]}
cands = json.load(open(f"{PW}/candidates.json"))
for p in places:
    if p["id"] not in PHOTOS:
        continue
    n, en, zh, crop = PHOTOS[p["id"]]
    c = cands[p["id"]]["candidates"][n]
    im = Image.open(f"{PW}/dl/{p['id']}__{n}.jpg").convert("RGB")
    if crop:
        x0, y0, x1, y1 = crop
        im = im.crop((round(x0 * im.width), round(y0 * im.height), round(x1 * im.width), round(y1 * im.height)))
    if im.width > 800:
        im = im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS)
    assert im.width >= im.height, p["id"]
    rel = f"images/places/{p['id']}.jpg"
    im.save(f"{APP}/{rel}", "JPEG", quality=82, optimize=True, progressive=True)
    p["photo"] = {"file": rel, "width": im.width, "height": im.height, "author": c["author"].strip() or "Unknown author", "license": c["license"].strip(),
                  "license_url": c["license_url"].strip(), "source": c["page"], "alt_en": en, "alt_zh": zh}
    if crop:
        p["photo"]["cropped"] = True

def edit_places():
    """Ludlow's note gains Comus; Poets' Corner's writer list gains the new writers buried or commemorated there"""
    path = f"{APP}/data/places.js"
    s = open(path, encoding="utf-8").read()
    old_en = 'note_en: "A market town in south Shropshire; Housman\'s ashes are buried at its church, St Laurence\'s"'
    old_zh = 'note: "什罗普郡南部的集镇；豪斯曼的骨灰葬在镇上的圣劳伦斯教堂"'
    assert s.count(old_en) == 1 and s.count(old_zh) == 1
    s = s.replace(old_en, 'note_en: "A market town in south Shropshire. Milton\'s masque Comus was first performed at Ludlow Castle in 1634, and Housman\'s ashes are buried at the town\'s church, St Laurence\'s"')
    s = s.replace(old_zh, 'note: "什罗普郡南部的集镇。弥尔顿的假面剧《科摩斯》1634 年在拉德洛城堡首演；豪斯曼的骨灰葬在镇上的圣劳伦斯教堂"')
    canon = json.load(open(f"{APP}/tools/canon.json", encoding="utf-8"))
    pc = next(x for x in canon["sites"] if x["ids"] == ["poets-corner"])
    authors = {b["author"] for b in books}
    m = re.search(r'(\{ id: "poets-corner".*?authors: )(\[[^\]]*\])', s)
    have = json.loads(m.group(2))
    new = [a for a in pc["authors"] if a in have or a in authors]
    s = s[:m.start(2)] + json.dumps(new, ensure_ascii=False) + s[m.end(2):]
    open(path, "w", encoding="utf-8").write(s)
    return [a for a in new if a not in have]

def record_decisions():
    D = f"{APP}/tools/coverage-decisions.json"
    dec = json.load(open(D, encoding="utf-8"))
    new = [
        ("author", "Richard Brinsley Sheridan", "skip", "buried in Poets' Corner, but his plays give the map little to point at; user decided 11-05"),
        ("author", "John Gay", "skip", "buried in Poets' Corner, but little tie to a UK place worth a marker; user decided 11-05"),
        ("author", "John Masefield", "skip", "buried in Poets' Corner, but little tie to a UK place worth a marker; user decided 11-05"),
        ("site", "Roald Dahl Plass and the Norwegian Church, Cardiff Bay", "covered elsewhere",
         "Dahl's Cardiff childhood is on the map through the Llandaff sweet shop from Boy; the museum in Great Missenden is his main site"),
    ]
    known = {(d["kind"], d["name"]) for d in dec["decisions"]}
    for kind, name, what, why in new:
        if (kind, name) not in known:
            dec["decisions"].append({"kind": kind, "name": name, "decision": what, "reason": why, "date": "2026-11-05"})
    json.dump(dec, open(D, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    record_decisions()
    append(f"{APP}/data/books.js", books, "11-05 覆盖面复核第二批：16 位作家（11 位公有领域引古登堡原文，5 位有版权只写场景说明）")
    append(f"{APP}/data/places.js", places, "11-05 覆盖面复核第二批（坐标和照片均有出处）")
    append(f"{APP}/data/lines.js", lines, "11-05 覆盖面复核第二批：古登堡原文摘句和场景说明（草稿，待审核）")
    added = edit_places()
    rows = [f"| {p['name']} | {p['photo']['author']} | [{p['photo']['license']}]({p['photo']['license_url']}) | [Commons]({p['photo']['source']}) |" for p in places if "photo" in p]
    cr = open(f"{APP}/docs/photo-credits.md", encoding="utf-8").read().rstrip("\n") + "\n" + "\n".join(rows) + "\n"
    open(f"{APP}/docs/photo-credits.md", "w", encoding="utf-8").write(cr)
    print("poets' corner +", ", ".join(added))
    for l in lines:
        print(f"{l['id']:7}", l["text_en"].replace("\n", " / ")[:300])
