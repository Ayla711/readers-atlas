"""11-24: Turkey, second pack: books that selection rule v2 adds (tools/selection/tr.md), as far as their places are found.
All nine are scene notes in our own words. Madonna in a Fur Coat (Sabahattin Ali, d. 1948) is in the public domain in Turkey
(Turkish Wikisource has the text), but it was first published in 1943 and is probably still protected in the United States,
so it gets a scene note too. Where a novel spreads over a city, the pin is the place the sources tie it to most closely:
- My Name Is Red: the palace treasury, where Master Osman blinds himself (Topkapı Palace).
- The Time Regulation Institute: the novel mostly happens in Şehzadebaşı, Vezneciler and Edirnekapı (Abdullah Uçman,
  Türk Dili, May 2026); the pin is the Şehzade Mosque, which gives Şehzadebaşı its name.
- Aylak Adam: C.'s walks through Beyoğlu, Taksim, Nişantaşı, Harbiye; the pin is İstiklal Avenue in Beyoğlu.
- Puslu Kıtalar Atlası: seventeenth-century Istanbul and Galata; a literary walk on the novel starts at the Galata Tower.
- Madonna in a Fur Coat: the Ankara frame story; the narrator walks between the station and the Exhibition House (Sergievi),
  now the Ankara Opera House.
- The Black Book: Galip and Rüya's flat in Nişantaşı. A Mind at Peace: Nuran's Kandilli. Bereketli Topraklar Üzerinde: Adana.
  Çalıkuşu: Feride's first post, the village of Zeyniler near Bursa.
Not yet added: Tutunamayanlar (no place the sources fix) and Aşk-ı Memnu (its opening, at Kalender on the Bosphorus,
has no coordinates in any Wikipedia). No photos yet.

Usage: python3 -I tools/content/batches/add_tr2.py <app_dir> tools/content/batches/coords/add_tr2.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-24"
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]
def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, lang, aliases, pd=False, src=None):
    return dict(id=id, title=title, title_zh=title_zh, title_orig=title_orig, author=author, author_zh=author_zh, year=year,
                orig_lang=lang, public_domain=pd, source_url=src, author_orig=author_orig, aliases=aliases)
def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
def check(books, places, lines):
    allb = set()
    for f in glob.glob(os.path.join(APP, "data", "*", "books.js")): allb |= ids_in(f)
    assert not {x["id"] for x in books} & allb, {x["id"] for x in books} & allb
    assert not {p["id"] for p in places} & ids_in(b.data("places.js")) and {p["id"] for p in places} == set(CO)
    assert not {l["id"] for l in lines} & ids_in(b.data("lines.js"))
    for l in lines:
        assert l["book_id"] in {x["id"] for x in books} and l["place_ids"][0] in {p["id"] for p in places}, l["id"]
    assert {l["book_id"] for l in lines} == {x["id"] for x in books}
    assert {l["place_ids"][0] for l in lines} == {p["id"] for p in places}
b.init(APP, "", "tr", DATE)
books = [
    BK("my-name-is-red", "My Name Is Red", "我的名字叫红", "Benim Adım Kırmızı", "Orhan Pamuk", "奥尔罕·帕慕克", "Orhan Pamuk", "1998", "tr",
       ["Benim Adim Kirmizi", "Black", "Kara", "Shekure", "Şeküre", "Enishte", "Master Osman", "Elegant Effendi", "Pamuk"]),
    BK("time-regulation-institute", "The Time Regulation Institute", "时间调节研究所", "Saatleri Ayarlama Enstitüsü", "Ahmet Hamdi Tanpınar",
       "艾哈迈德·哈姆迪·坦珀纳尔", "Ahmet Hamdi Tanpınar", "1961", "tr", ["Saatleri Ayarlama Enstitusu", "Hayri İrdal", "Halit Ayarcı", "Tanpinar"]),
    BK("aylak-adam", "Aylak Adam (The Idler)", "闲人", "Aylak Adam", "Yusuf Atılgan", "优素福·阿特尔甘", "Yusuf Atılgan", "1959", "tr",
       ["The Loiterer", "The Idler", "C.", "Atilgan"]),
    BK("puslu-kitalar-atlasi", "Puslu Kıtalar Atlası (The Atlas of Misty Continents)", "迷雾大陆地图集", "Puslu Kıtalar Atlası", "İhsan Oktay Anar",
       "伊赫桑·奥克泰·阿纳尔", "İhsan Oktay Anar", "1995", "tr", ["Puslu Kitalar Atlasi", "Atlas of Misty Continents", "Uzun İhsan Efendi", "Bünyamin", "Ebrehe", "Anar"]),
    BK("madonna-in-a-fur-coat", "Madonna in a Fur Coat", "穿皮大衣的圣母", "Kürk Mantolu Madonna", "Sabahattin Ali", "萨巴哈丁·阿里", "Sabahattin Ali",
       "1943", "tr", ["Kurk Mantolu Madonna", "Raif Efendi", "Maria Puder", "Sabahattin Ali"], src="https://tr.wikisource.org/wiki/K%C3%BCrk_Mantolu_Madonna"),
    BK("the-black-book", "The Black Book", "黑书", "Kara Kitap", "Orhan Pamuk", "奥尔罕·帕慕克", "Orhan Pamuk", "1990", "tr",
       ["Kara Kitap", "Galip", "Rüya", "Celâl", "Pamuk"]),
    BK("huzur", "A Mind at Peace", "宁静", "Huzur", "Ahmet Hamdi Tanpınar", "艾哈迈德·哈姆迪·坦珀纳尔", "Ahmet Hamdi Tanpınar", "1949", "tr",
       ["Huzur", "Mümtaz", "Nuran", "Suad", "İhsan", "Tanpinar"]),
    BK("bereketli-topraklar", "Bereketli Topraklar Üzerinde (On Fertile Lands)", "在丰饶的土地上", "Bereketli Topraklar Üzerinde", "Orhan Kemal",
       "奥尔罕·凯末尔", "Orhan Kemal", "1954", "tr", ["Bereketli Topraklar Uzerinde", "On Fertile Lands", "İflahsızın Yusuf", "Köse Hasan", "Pehlivan Ali", "Çukurova"]),
    BK("calikusu", "Çalıkuşu (The Wren)", "鹪鹩", "Çalıkuşu", "Reşat Nuri Güntekin", "雷沙特·努里·京泰金", "Reşat Nuri Güntekin", "1922", "tr",
       ["Calikusu", "The Wren", "Feride", "Kâmran", "Munise", "Guntekin"]),
]
places = [
    b.ORIG("tr-topkapi", "Topkapı Palace, Istanbul", "托普卡珀宫，伊斯坦布尔", *C("tr-topkapi"),
           "The Ottoman sultans' palace on the point of the old city, which kept the imperial treasury. In My Name Is Red (1998) Black and Master Osman, head of the Sultan's painting workshop, are let into the palace treasury in the winter of 1591, and there, among the old illustrated books, Osman blinds himself with a needle",
           "老城岬角上的奥斯曼苏丹宫殿，帝国的宝库就在这里。《我的名字叫红》（1998）里，1591 年冬天，黑和苏丹画坊的总管奥斯曼大师获准进入宫中宝库；就在那些古老的插画书之间，奥斯曼用一根针刺瞎了自己的眼睛"),
    b.ORIG("tr-sehzadebasi", "Şehzadebaşı, Istanbul (Şehzade Mosque)", "谢赫扎德巴舍，伊斯坦布尔（王子清真寺）", *C("tr-sehzadebasi"),
           "Quarter of the walled city named after the Şehzade Mosque. Tanpınar's The Time Regulation Institute (1961) mostly happens here and in neighbouring Vezneciler and Edirnekapı, the heart of old Istanbul in the years it covers",
           "老城墙内的街区，因王子清真寺得名。坦珀纳尔的《时间调节研究所》（1961）大部分就发生在这里，以及相邻的韦兹内吉莱尔和埃迪尔内卡珀——书中那些年代伊斯坦布尔老城的中心"),
    b.ORIG("tr-istiklal", "İstiklal Avenue, Beyoğlu, Istanbul", "独立大街，贝伊奥卢，伊斯坦布尔", *C("tr-istiklal"),
           "The main street of Beyoğlu. In Yusuf Atılgan's Aylak Adam (1959) C. drifts day after day through Beyoğlu, Taksim, Nişantaşı and Harbiye, looking at the crowds and looking for a woman he could truly love",
           "贝伊奥卢的主街。尤素福·阿特尔甘的《闲人》（1959）里，C. 日复一日地在贝伊奥卢、塔克西姆、尼尚塔石和哈尔比耶游荡，看着人群，寻找一个他能真心去爱的女人"),
    b.ORIG("tr-galata", "Galata Tower, Istanbul", "加拉塔塔，伊斯坦布尔", *C("tr-galata"),
           "The medieval tower above Galata, across the Golden Horn from the old city. İhsan Oktay Anar's Puslu Kıtalar Atlası (1995) is set in seventeenth-century Istanbul and Galata; a literary walking route through the city built on the novel starts at the tower",
           "金角湾对岸、加拉塔区高处的中世纪塔楼。伊赫桑·奥克泰·阿纳尔的《迷雾大陆地图集》（1995）以十七世纪的伊斯坦布尔和加拉塔为背景；按这部小说设计的伊斯坦布尔文学步行路线，就从这座塔出发"),
    b.ORIG("tr-ankara-sergievi", "Ankara Opera House (the old Exhibition House)", "安卡拉歌剧院（原展览馆）", *C("tr-ankara-sergievi"),
           "Built in 1933 as the Exhibition House (Sergievi) and turned into the opera house in 1948. In the Ankara frame story of Sabahattin Ali's Madonna in a Fur Coat (1943) the narrator, out of work, walks on an autumn evening along the quiet road between the station and the Sergievi",
           "1933 年作为展览馆（Sergievi）建成，1948 年改为歌剧院。萨巴哈丁·阿里《穿皮大衣的圣母》（1943）在安卡拉的框架故事里，失业的叙述者在一个秋天的傍晚，走在火车站和展览馆之间那条冷清的路上"),
    b.ORIG("tr-nisantasi", "Nişantaşı, Istanbul", "尼尚塔石，伊斯坦布尔", *C("tr-nisantasi"),
           "Well-to-do quarter north of Taksim, where Pamuk has spent most of his life. In The Black Book (1990) the lawyer Galip wakes in his flat in Nişantaşı beside his wife and cousin Rüya, and comes home that evening to find that she has left him",
           "塔克西姆以北的富裕街区，帕慕克一生大半住在这一带。《黑书》（1990）里，律师加利普在尼尚塔石的公寓里醒来，身边是他的妻子、也是他的表妹如梦；当天傍晚回家时，他发现她已经离开了"),
    b.ORIG("tr-kandilli", "Kandilli, Bosphorus", "坎迪利，博斯普鲁斯海峡", *C("tr-kandilli"),
           "Village on the Asian shore of the Bosphorus. In Tanpınar's A Mind at Peace (1949), set in Istanbul on the eve of the Second World War, Nuran, whom Mümtaz loves, lives here",
           "博斯普鲁斯海峡亚洲岸边的村子。坦珀纳尔的《宁静》（1949）以二战前夕的伊斯坦布尔为背景，穆姆塔兹所爱的努兰就住在这里"),
    b.ORIG("tr-adana", "Adana", "阿达纳", *C("tr-adana"),
           "City of the Çukurova plain in the south of Turkey. In Orhan Kemal's Bereketli Topraklar Üzerinde (1954) three friends from a village near Sivas get off the train here to look for work, first in a cotton-ginning mill",
           "土耳其南部乔库罗瓦平原上的城市。奥尔罕·凯末尔的《在丰饶的土地上》（1954）里，锡瓦斯附近一个村子的三个朋友在这里下了火车找活干，先进了一家轧棉厂"),
    b.ORIG("tr-zeyniler", "Zeyniler, Bursa", "泽伊尼莱尔，布尔萨", *C("tr-zeyniler"),
           "Village, now a quarter of Yıldırım, on the slopes of Uludağ above Bursa. In Reşat Nuri Güntekin's Çalıkuşu (1922) it is Feride's first post as a teacher, the remote village nobody else wanted; a house there is now shown as the Çalıkuşu House",
           "布尔萨上方乌卢达山坡上的村子，如今是耶尔德勒姆区的一个街区。雷沙特·努里·京泰金的《鹪鹩》（1922）里，这里是费丽黛当教师的第一个地方，一个谁都不愿去的偏远村庄；如今村里有一座房子作为“鹪鹩之家”开放参观"),
]
lines = [
    b.S("tr-nr-1", "my-name-is-red", "tr-topkapi", "The palace treasury", "宫中宝库",
        "Istanbul, winter 1591. Black, back after twelve years in Persia, is drawn into the secret book his uncle Enishte Effendi is making for the Sultan in the manner of the Venetian painters, after one of its miniaturists, Elegant Effendi, is murdered; the dead man narrates the first chapter. Near the end Black and Master Osman, head of the Sultan's workshop, are let into the palace treasury at Topkapı to search the old illustrated books for the clue to the murderer, and there Osman blinds himself with a needle, as the great Bihzad was said to have done.",
        "1591 年冬天的伊斯坦布尔。在波斯待了十二年的黑回到这里，卷进了舅舅恩尼什特为苏丹秘密制作、仿威尼斯画家画法的一本书——书的一位细密画家“高雅先生”被人杀了，第一章就由这个死人自己来讲。临近结尾，黑和苏丹画坊的总管奥斯曼大师获准进入托普卡珀宫的宝库，在古老的插画书里寻找凶手的线索；奥斯曼就在那里用一根针刺瞎了自己，就像传说中伟大的毕扎德那样。",
        ["Topkapı"], ["托普卡珀宫"],
        "https://en.wikipedia.org/wiki/My_Name_Is_Red; https://www.encyclopedia.com/arts/educational-magazines/my-name-red; https://litcharts.com/lit/my-name-is-red/chapter-49-i-am-called-black; https://en.wikipedia.org/wiki/Nakka%C5%9F_Osman"),
    b.S("tr-tr-1", "time-regulation-institute", "tr-sehzadebasi", "The novel as a whole", "全书",
        "Hayri İrdal, who tells the story, has no shop of his own but understands clocks better than anyone. Back in Istanbul after four years in the army, he falls in with Halit Ayarcı, who founds the Time Regulation Institute to set the city's clocks right, a hollow institution through which the novel mocks a modernisation that copies only the surface of the West. Through Hayri's memories the novel runs from the reign of Abdülhamid II to the Republic, mostly in Şehzadebaşı, Vezneciler and Edirnekapı, and ends with Halit Ayarcı's death in a suspicious traffic accident.",
        "讲故事的海里·伊尔达尔自己没有铺子，却比谁都懂钟表。服完四年兵役回到伊斯坦布尔后，他结识了哈利特·阿亚尔哲；后者创办了“时间调节研究所”，要把全城的钟表拨准——小说借这个空洞的机构，讽刺只学到西方皮毛的现代化。借着海里的回忆，小说从阿卜杜勒哈米德二世的时代一直写到共和国，地点大多在谢赫扎德巴舍、韦兹内吉莱尔和埃迪尔内卡珀；结尾是哈利特·阿亚尔哲死于一场可疑的车祸。",
        ["Şehzadebaşı"], ["谢赫扎德巴舍"],
        "https://dergipark.org.tr/download/article-file/50509; https://tdk.gov.tr/wp-content/uploads/2025/05/Abdullah-Ucman-_-E-_-Saatleri-Ayarlama-Enstitusu-Uzerine-Notlar-_11.pdf; https://tdk.gov.tr/wp-content/uploads/2026/05/Zeynep-Karaca-_Soylesi_-ABDULLAH-UCMANLA-SAATLERI-AYARLAMA-ENSTITUSU-UZERINE-20-DERS._-5.pdf; https://dergipark.org.tr/en/download/article-file/3810275"),
    b.S("tr-aa-1", "aylak-adam", "tr-istiklal", "The novel as a whole", "全书",
        "C., who lost his mother as a small child and was brought up by his aunt, is idle and alone. He wanders the streets of Istanbul, through Beyoğlu, Taksim, Nişantaşı and Harbiye, uneasy among the crowds, looking for a woman he could truly love. At the opening the crowd in the avenue oppresses him, until he thinks that the woman he is to meet must be somewhere near. Letters and diary pages of his girlfriends Ayşe and Güler show him from outside.",
        "C. 很小就没了母亲，由姨妈带大；他无所事事，孤身一人。他在伊斯坦布尔的街上游荡，走过贝伊奥卢、塔克西姆、尼尚塔石和哈尔比耶，在人群里坐立不安，寻找一个他能真心去爱的女人。开篇时，大街上的人群叫他气闷，直到他想起要见的那个女人一定就在附近。他的女友阿伊谢和居莱尔的信和日记，让读者从外面看到他。",
        ["Beyoğlu"], ["贝伊奥卢"],
        "https://dergipark.org.tr/en/download/article-file/757853; https://boenstitu.com/blog/kitap-ozetleri/aylak-adam; https://www.haberturk.com/ozel-icerikler/muhsin-kizilkaya-2291/3882576-1-mayis-sabahi-aylak-adama-rastladim-stockholmde; https://qantara.de/node/12205"),
    b.S("tr-pk-1", "puslu-kitalar-atlasi", "tr-galata", "The novel as a whole", "全书",
        "Seventeenth-century Istanbul and Galata. Uzun İhsan Efendi spends most of his life asleep; under a sleeping draught he dreams long dreams and makes of them an atlas of the world, which he hands to his son Bünyamin when the boy comes back from the dead. Bünyamin, a sapper in the Ottoman army, lives out the adventures the atlas maps, while the janissaries are forcing Uzun İhsan's door.",
        "十七世纪的伊斯坦布尔和加拉塔。乌尊·伊赫桑大人一生大半在睡觉；喝了安眠的糖浆，他做着长长的梦，把梦里所见编成一部世界地图集。儿子比尼亚明死而复生，他便把地图集交给了儿子。比尼亚明在奥斯曼军中当坑道兵，亲身经历着地图集里画下的冒险；与此同时，禁卫军正在撞乌尊·伊赫桑家的门。",
        ["Galata"], ["加拉塔"],
        "https://www.milliyet.com.tr/egitim/puslu-kitalar-atlasi-kitap-ozeti-oku-puslu-kitalar-atlasi-kitabi-konusu-karakterleri-ve-sayfa-sayisi-7518677; https://www.goodreads.com/book/show/1546936; https://tr.euronews.com/kultur/2026/06/21/istanbulda-edebiyat-rotasi-puslu-kitalar-atlasi-ile-sehri-okumak"),
    b.S("tr-km-1", "madonna-in-a-fur-coat", "tr-ankara-sergievi", "The Ankara frame story", "安卡拉的框架故事",
        "The narrator, dismissed from a small bank job, looks for work in Ankara through the summer and autumn, and walks one evening along the quiet road between the station and the Exhibition House. He finds a clerk's place in a timber firm, where he shares an office with the quiet Raif Efendi. When Raif falls ill he gives the narrator a notebook to read and destroy: the story of his youth in Berlin, where he was captivated by a portrait of a woman in a fur coat and then met the woman herself, Maria Puder. Raif dies, and the narrator turns back to the notebook's first page.",
        "叙述者丢了银行里的小差事，整个夏天和秋天都在安卡拉找活干；一天傍晚，他走在火车站和展览馆之间那条冷清的路上。后来他在一家木材公司谋到个文书职位，同不声不响的拉伊夫先生共用一间办公室。拉伊夫病倒后，交给他一本笔记，让他读完就毁掉：那是拉伊夫年轻时在柏林的故事——一幅穿皮大衣的女人画像叫他着了迷，后来他遇见了画中人玛丽亚·普德尔。拉伊夫死了，叙述者又翻回笔记的第一页。",
        ["Ankara"], ["安卡拉"],
        "https://tr.wikisource.org/wiki/K%C3%BCrk_Mantolu_Madonna; https://en.wikipedia.org/wiki/Madonna_in_a_Fur_Coat"),
    b.S("tr-kk-1", "the-black-book", "tr-nisantasi", "The novel as a whole", "全书",
        "A snowy winter in Istanbul. The lawyer Galip wakes in his flat in Nişantaşı beside Rüya, his wife and cousin, and comes home in the evening to a short note: she has left him. He hides it from the family and searches the city for her, and for their relative Celâl, the newspaper columnist whom Galip has envied since childhood and who has vanished too. He moves into Celâl's secret flat, wears his clothes and starts writing his column. In the end Celâl is shot dead in the street, and Rüya is found shot in Aladdin's shop.",
        "伊斯坦布尔一个下雪的冬天。律师加利普在尼尚塔石的公寓里醒来，身边是他的妻子、也是表妹的如梦；傍晚回家，只看到一张短短的字条：她走了。他瞒着家里人，满城寻找她，也寻找同样失踪了的杰拉尔——报纸专栏作家，加利普从小就羡慕的人。他住进杰拉尔的秘密公寓，穿上他的衣服，替他写起专栏来。最后，杰拉尔在街上被枪杀，如梦也被发现中枪死在阿拉丁的店里。",
        ["Nişantaşı"], ["尼尚塔石"],
        "https://en.wikipedia.org/wiki/The_Black_Book_(Pamuk_novel); https://www.bookrags.com/studyguide-the-black-book-1990-novel/; https://www.goodreads.com/book/show/1269960"),
    b.S("tr-hz-1", "huzur", "tr-kandilli", "Part two, “Nuran”", "第二部“努兰”",
        "Istanbul just before the Second World War, in four parts named after İhsan, Nuran, Suad and Mümtaz. Mümtaz, a young assistant at the university, falls in love with Nuran, divorced from her husband, who grew up in an old cultured family on the Bosphorus and lives in Kandilli. For a year they wander the city's outlying quarters, its old buildings, the Islands and the Bosphorus, and go to evenings of classical music. As they prepare to marry, Suad, who has long loved Nuran, comes between them.",
        "第二次世界大战前夕的伊斯坦布尔，全书四部分别以伊赫桑、努兰、苏阿德和穆姆塔兹命名。大学里年轻的助教穆姆塔兹爱上了已经离婚的努兰——她在博斯普鲁斯海峡边一个有教养的老家族里长大，住在坎迪利。整整一年，他们一起走遍城边的老街区、古建筑、王子群岛和博斯普鲁斯海峡，去听古典音乐会。就在两人准备结婚时，早就爱着努兰的苏阿德插到了他们中间。",
        ["Kandilli"], ["坎迪利"],
        "https://islamansiklopedisi.org.tr/huzur--tanpinar; https://www.einaudi.it/content/uploads/estratti/978880622888PCA.pdf; https://dergipark.org.tr/en/download/article-file/156789"),
    b.S("tr-bt-1", "bereketli-topraklar", "tr-adana", "The novel as a whole", "全书",
        "Three friends from a village near Sivas, İflahsızın Yusuf, Köse Hasan and Pehlivan Ali, set out for the Çukurova to earn money. After a long, hard train journey they get off at Adana and find the cotton-ginning mill of a man from their parts. Köse Hasan falls ill and dies without ever really working; Pehlivan Ali, injured, bleeds to death through the boss's indifference. Only Yusuf goes home, in new clothes and with presents for his wife and children, and hears at the station of Ali's death.",
        "锡瓦斯附近一个村子的三个朋友——伊弗拉赫瑟兹的尤素福、科塞·哈桑和佩赫利万·阿里——动身去乔库罗瓦挣钱。坐了一路艰难的火车，他们在阿达纳下车，找到一个同乡开的轧棉厂。科塞·哈桑还没真正干上活就病倒死了；佩赫利万·阿里受了伤，因为东家不管不顾，流血而死。只有尤素福回了家，穿着新衣服，给妻儿带着礼物；他是在火车站听到阿里的死讯的。",
        ["Adana"], ["阿达纳"],
        "https://www.turkedebiyati.org/?p=12783; https://kureansiklopedi.com/tr/detay/bereketli-topraklar-uzerinde-kitap; https://dergipark.org.tr/en/download/article-file/1284946; https://1000kitap.com/kitap/bereketli-topraklar-uzerinde--229824"),
    b.S("tr-ck-1", "calikusu", "tr-zeyniler", "Feride's first post", "费丽黛的第一个任职地",
        "Feride, orphaned young and schooled at a French boarding school in Istanbul, where her mischief earned her the name Çalıkuşu, the wren, is engaged to her cousin Kâmran. Her pride wounded on the wedding day, she leaves Istanbul and becomes a teacher in Anatolia. Her first post is Zeyniler, a remote village near Bursa that no one wants; there she adopts her little pupil Munise and meets the army doctor Hayrullah Bey, who will look after her later in Kuşadası. She goes on to teach in Bursa, Çanakkale and other towns.",
        "费丽黛自幼父母双亡，在伊斯坦布尔一所法国寄宿学校长大，因为淘气被同学叫作“鹪鹩”。她同表哥卡姆兰订了婚，却在婚礼那天自尊受了伤，离开伊斯坦布尔，到安纳托利亚去当教师。她的第一个任职地是布尔萨附近谁都不愿去的偏远村子泽伊尼莱尔；在那里，她收养了小学生穆妮赛，也认识了军医海鲁拉赫先生——后来在库沙达瑟照顾她的就是他。之后她又在布尔萨、恰纳卡莱等地教书。",
        ["Zeyniler"], ["泽伊尼莱尔"],
        "https://www.turkedebiyati.org/?p=23574; https://www.sozcu.com.tr/calikusu-wp7319904; https://1000kitap.com/doktor-hayrullah-bey-feride--2005626; https://hurriyetdailynews.com/village-in-famous-turkish-novel-to-open-tourism-58485"),
]
check(books, places, lines)
if __name__ == "__main__":
    M = "11-24: second pack, books added under selection rule v2 (tools/content/batches/add_tr2.py)"
    b.append(b.data("books.js"), books, M); b.append(b.data("places.js"), places, M); b.append(b.data("lines.js"), lines, M)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
