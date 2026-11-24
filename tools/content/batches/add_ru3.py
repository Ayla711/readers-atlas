"""11-22: Russia, quotations for the public-domain books that had only placeholder scene notes, taken from Russian
Wikisource (tools/content/wikisource.py: the rendered page's own text). English and Chinese are our own translations
(translation: "own"), drafts for review. Each quotation replaces the book's placeholder scene note.

What a cut changes, each named again in that line's `checked`:
- several editions set no-break spaces between words; they are written as plain spaces;
- the Bronze Horseman page numbers every fifth line: the numbers are left out;
- My Past and Thoughts keeps the printed page's line ends inside paragraphs: they are joined;
- Bely's Petersburg marks a word with an asterisk for an endnote: the asterisk is left out.

Still scene notes only:
- not on Wikisource: The Master and Margarita, Heart of a Dog;
- the place on the map is the author's house, estate or museum, which the book does not reach: Dead Souls (Gogol
  House), Fathers and Sons (Spasskoye), The Brothers Karamazov (Staraya Russa: the town is renamed, and the stone of
  the epilogue is not the house), The Golovlyov Family (Spas-Ugol), The Steppe (Taganrog), The Seagull (Melikhovo), The
  Cherry Orchard (the White Dacha), The Twelve (Blok's flat), A Cloud in Trousers (the Mayakovsky Museum; the poem is
  set in Odessa), We (Lebedyan), Dark Avenues (the Bunin Museum);
- Resurrection: the novel never names Butyrka.

Usage: python3 -I add_ru3.py <app_dir> <wikisource_dir>   (python3 -I ../wikisource.py <dir> ru <title> … downloads)"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws
from datafile import drop_entries, set_source

APP, WS = sys.argv[1], sys.argv[2]
DATE = "2026-11-22"
b.init(APP, None, "ru", DATE)
GAP = b.GAP
NBSP = "; no-break spaces written as spaces"
JOINED = "; the page's line ends inside a paragraph joined"

def take(title, start, end, after=None):
    """block() on the page's text with no-break spaces written as spaces; returns (text, whether any were there)"""
    raw = ws.text(WS, title)
    t = raw.replace("\xa0", " ")
    i = t.find(start, t.find(after) if after else 0)
    assert i >= 0, (title, start)
    j = t.find(end, i)
    assert j >= 0, (title, start, end)
    s = "\n".join(l.lstrip(" 　\t") for l in t[i:j + len(end)].split("\n"))
    return s, "\xa0" in raw[i:j + len(end)]

def Q(id, book, place, loc, loc_zh, title, cut, hl_orig, en, hl_en, zh, hl_zh, note=""):
    orig, nb = cut
    for h in hl_orig:
        assert h in orig, (id, h)
    for h in hl_en:
        assert h in en, (id, h)
    for h in hl_zh:
        assert h in zh, (id, h)
    assert "  " not in orig and "\xa0" not in orig, (id, "double or no-break space")
    note = (NBSP if nb else "") + note
    if note.startswith("; "):
        note = " (" + note[2:] + ")"
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh,
                text_orig=orig, highlight_orig=hl_orig, text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh,
                translation="own", status="draft", checked=f"Russian Wikisource, {title}{note}, {DATE}")

def plus(a, b_, sep=GAP):
    return a[0] + sep + b_[0], a[1] or b_[1]

lines, sources = [], {}

# ---- The Life of the Archpriest Avvakum ----
AVV = "Житие протопопа Аввакума, им самим написанное (Аввакум)"
sources["life-of-avvakum"] = AVV
lines.append(Q("avv-1", "life-of-avvakum", "ru-pustozersk", "The Life: exile to Pustozersk", "《行传》：流放普斯托泽尔斯克", AVV,
    take(AVV, "Таже, братию казня", "а другое больши."), ["Пустозерье", "Пустозерья"],
    "Then, punishing the brethren but not punishing me, they exiled me to Pustozersk. And from Pustozersk I sent the "
    "tsar two epistles: the first not long, the other longer.",
    ["Pustozersk"],
    "随后，他们惩处了弟兄们，却没有惩处我，把我流放到普斯托泽尔斯克。我从普斯托泽尔斯克给沙皇寄去两封书信：头一封不长，另一封长些。",
    ["普斯托泽尔斯克"]))

# ---- Poor Liza, opening ----
LIZ = "Бедная Лиза (Карамзин)"
sources["poor-liza"] = LIZ
lines.append(Q("liza-1", "poor-liza", "ru-simonov", "Opening", "开篇", LIZ,
    take(LIZ, "Но всего приятнее для меня то место", "к небу возносящихся!"), ["Си…нова монастыря"],
    "But the place I like best of all is where the gloomy Gothic towers of the Si…nov Monastery rise. Standing on this "
    "hill, you see on your right almost the whole of Moscow, that awful mass of houses and churches, which appears to "
    "the eye in the shape of a majestic amphitheatre: a magnificent picture, especially when the sun shines on it, when "
    "its evening rays blaze on countless golden domes, on countless crosses rising to the sky!",
    ["the Si…nov Monastery"],
    "但我最喜欢的，是西……诺夫修道院那些阴郁的哥特式塔楼高耸的地方。站在这座山上，右边几乎可以望见整个莫斯科，"
    "那一大片吓人的房屋和教堂，在眼前呈现为一座宏伟的圆形剧场：这是一幅壮丽的图画，尤其是在阳光照耀的时候，"
    "当夕阳的余晖在无数金色圆顶、在无数直指天空的十字架上燃烧的时候！",
    ["西……诺夫修道院"]))

# ---- Woe from Wit, Act IV, scene 14 (1911 edition, modern spelling) ----
WFW = "Горе от ума (Грибоедов)/ПСС 1911 (ВТ)/Действие IV"
sources["woe-from-wit"] = WFW
lines.append(Q("wfw-1", "woe-from-wit", "ru-griboyedov-moscow", "Act IV, scene 14", "第四幕第十四场", WFW,
    take(WFW, "Вон из Москвы!", "Карету мне, карету!"), ["Москвы"],
    "Out of Moscow! I'll come here no more.\nI'm running, I won't look back, I'll go and search the world\nfor a corner "
    "where wounded feeling has a place!..\nMy carriage, my carriage!",
    ["Moscow"],
    "离开莫斯科！我再也不来这里了。\n我要跑，头也不回，到世界上去寻找\n一个能容下受伤感情的角落！……\n备车，给我备车！",
    ["莫斯科"]))

# ---- Eugene Onegin, chapter 2, stanza I ----
ONE = "Евгений Онегин (Пушкин)/ПСС 1977 (СО)/Глава 2"
sources["eugene-onegin"] = ONE
lines.append(Q("one-1", "eugene-onegin", "ru-mikhailovskoye", "Chapter 2, stanza I", "第二章第一节", ONE,
    take(ONE, "Деревня, где скучал Евгений", "Приют задумчивых Дриад."), ["Деревня, где скучал Евгений"],
    "The village where Evgeny was bored\nwas a charming little corner;\na friend of innocent delights\nmight there have "
    "blessed the heavens.\nThe manor house, secluded,\nscreened from the winds by a hill,\nstood above a stream; far "
    "off\nbefore it meadows and golden cornfields\nlay bright with colour and in bloom.\nVillages glimpsed here and "
    "there,\nherds wandered over the meadows,\nand a huge neglected garden,\nthe haunt of pensive Dryads,\nspread wide "
    "its dense shade.",
    ["The village where Evgeny was bored"],
    "叶甫盖尼在那儿苦闷的乡村\n原是个迷人的小角落；\n一个爱好纯真乐趣的人\n在那里会为上天祝福。\n地主的宅子孤零零的，\n"
    "有山岗替它挡住风，\n立在小河上方；远处，\n草地和金黄的田野\n在它前面斑斓开放。\n村落在这里那里闪现，\n"
    "牛羊在草地上漫游，\n一座荒芜的大花园\n铺开浓密的绿荫，\n是沉思的林中仙女的栖所。",
    ["叶甫盖尼在那儿苦闷的乡村"]))

# ---- The Tales of Belkin: 'The Stationmaster' ----
BEL = "Станционный смотритель (Пушкин)"
sources["tales-of-belkin"] = BEL
lines.append(Q("bel-1", "tales-of-belkin", "ru-vyra", "'The Stationmaster'", "《驿站长》", BEL,
    take(BEL, "В трех верстах от станции ***", "но опрятную обитель."), ["станции ***", "смиренную, но опрятную обитель"],
    "Three versts from the *** station it began to spit with rain, and a minute later a downpour soaked me to the skin. "
    "On arriving at the station my first concern was to change as quickly as I could, my second to ask for tea. 'Hey, "
    "Dunya!' the stationmaster shouted, 'put the samovar on, and go and fetch some cream.' At these words a girl of "
    "about fourteen came out from behind the partition and ran into the passage. Her beauty struck me. 'Is that your "
    "daughter?' I asked the stationmaster. 'My daughter, sir,' he answered with an air of satisfied pride; 'and so "
    "sensible, so quick, the image of her late mother.' Then he set about copying out my travel order, and I busied "
    "myself looking at the pictures that adorned his humble but tidy dwelling.",
    ["the *** station", "his humble but tidy dwelling"],
    "离***驿站还有三俄里时，开始落雨点，不一会儿一场倾盆大雨把我浇得透湿。到了驿站，我头一件事是赶紧换衣服，"
    "第二件是要茶。“喂，杜尼娅！”驿站长喊道，“把茶炊烧上，再去拿点奶油来。”话音刚落，隔板后面走出一个十四岁上下的小姑娘，"
    "跑进了门廊。她的美貌叫我吃了一惊。“这是你女儿？”我问驿站长。“是我女儿，先生，”他带着心满意足的得意神情回答，"
    "“又懂事，又麻利，跟她过世的娘一模一样。”接着他动手誊写我的驿马使用证，我便观赏起那些装点着他这间简陋却整洁的小屋的图画来。",
    ["***驿站", "简陋却整洁的小屋"]))

# ---- The Bronze Horseman, Part 2 ----
BH = "Медный всадник (Пушкин)"
sources["bronze-horseman"] = BH
bh, bh_nb = take(BH, "И он по площади пустой", "С тяжёлым топотом скакал.")
assert re.search(r"^\d+ ", bh, re.M)
lines.append(Q("bh-1", "bronze-horseman", "ru-bronze-horseman", "Part 2, lines 448–460", "第二部第 448–460 行", BH,
    (re.sub(r"^\d+ ", "", bh, flags=re.M), bh_nb), ["Всадник Медный"],
    "And over the empty square he runs\nand hears behind him,\nlike the rumbling of thunder,\na heavy, ringing "
    "gallop\nover the shaken roadway.\nAnd, lit by the pale moon,\nhis hand stretched out on high,\nthe Bronze Horseman "
    "races after him\non his ringing, galloping steed;\nand all night long, wherever\nthe poor madman turned his "
    "steps,\neverywhere the Bronze Horseman\ngalloped after him with heavy tread.",
    ["the Bronze Horseman"],
    "他在空荡荡的广场上\n奔跑，听见身后——\n仿佛雷声隆隆——\n沉重而响亮的马蹄声\n踏过震颤的路面。\n惨白的月光照着，\n"
    "他高高伸出手臂，\n青铜骑士在后面追赶，\n骑着嘚嘚飞奔的骏马；\n这可怜的疯子整整一夜\n无论把脚步转向哪里，\n"
    "青铜骑士都在后面\n沉重地蹄声嗒嗒追来。",
    ["青铜骑士"], "; the page's line numbers left out"))

# ---- A Hero of Our Time: 'Princess Mary', 11 May ----
HER = "Герой нашего времени (Лермонтов)/СО/Княжна Мери"
sources["hero-of-our-time"] = HER
lines.append(Q("hero-1", "hero-of-our-time", "ru-lermontov-duel", "'Princess Mary', 11 May", "《梅丽公爵小姐》，5 月 11 日", HER,
    take(HER, "Вчера я приехал в Пятигорск", "Весело жить в такой земле!"), ["Пятигорск", "у подошвы Машука"],
    "Yesterday I arrived in Pyatigorsk and took lodgings at the edge of the town, on the highest spot, at the foot of "
    "Mashuk: in a storm the clouds will come down to my roof. This morning at five, when I opened the window, my room "
    "filled with the scent of the flowers growing in the modest front garden. Branches of flowering cherry look in at "
    "my windows, and the wind sometimes strews my writing desk with their white petals. The view on three sides is "
    "wonderful. To the west five-peaked Beshtu shows blue, like 'the last cloud of a scattered storm'; to the north "
    "rises Mashuk, like a shaggy Persian hat, and hides all that part of the sky; to the east the view is merrier: below "
    "me spreads a clean, brand-new little town, the healing springs murmur, a crowd of many tongues murmurs, and there, "
    "further off, the mountains pile up like an amphitheatre, ever bluer and mistier, and on the edge of the horizon "
    "stretches a silver chain of snowy peaks, beginning with Kazbek and ending with two-headed Elbrus... It is a joy to "
    "live in such a land!",
    ["Pyatigorsk", "at the foot of Mashuk"],
    "昨天我到了五山城，在城边最高的地方、马舒克山脚下租了一处住所：下雷雨时，云会一直降到我的屋顶上。今天早上五点钟，"
    "我打开窗户，屋里立刻充满了小前院里花朵的香气。开花的樱桃树枝探进我的窗口，风有时把白色的花瓣撒满我的书桌。"
    "三面的景色都美极了。西边，五峰的别什图山泛着蓝色，像“消散的暴风雨的最后一片云”；北边，马舒克山像一顶毛茸茸的波斯帽子耸立着，"
    "遮住了这一片天空；往东看更叫人愉快：脚下是一座干干净净、崭新的小城，疗养的泉水哗哗作响，操着各种语言的人群喧闹着，"
    "再远处，群山层层叠叠像一座圆形剧场，越远越蓝，越远越朦胧，地平线边上绵延着一道银色的雪峰链，从卡兹别克峰开始，"
    "到双峰的厄尔布鲁士峰为止……生活在这样的地方多么快活！",
    ["五山城", "马舒克山脚下"]))

# ---- The Overcoat, ending (1967 edition) ----
OVC = "Шинель (Гоголь)/СС 1967 (СО)"
sources["the-overcoat"] = OVC
lines.append(Q("ovc-1", "the-overcoat", "ru-kalinkin-bridge", "Ending", "结尾", OVC,
    take(OVC, "Но кто бы мог вообразить", "для прикрытия собственной."), ["Калинкина моста"],
    "But who could have imagined that this was not yet all about Akaky Akakievich, that he was destined to live on "
    "noisily for a few days after his death, as if in reward for a life that no one had noticed? But so it happened, "
    "and our poor story unexpectedly takes a fantastic ending. Rumours suddenly spread through Petersburg that at the "
    "Kalinkin Bridge, and far beyond it, a dead man in the shape of a clerk had begun to appear at night, looking for "
    "some overcoat that had been stolen, and under the pretext of the stolen overcoat pulling from everyone's shoulders, "
    "regardless of rank and title, every kind of overcoat: catskin, beaver, wadded, raccoon, fox, bearskin coats; in a "
    "word, every kind of fur and skin that people have ever devised to cover their own.",
    ["the Kalinkin Bridge"],
    "可是谁能想到，关于阿卡基·阿卡基耶维奇的事到这里还没有完，他命中注定要在死后热热闹闹地再活几天，"
    "仿佛是对他那无人注意的一生的补偿。然而事情就是这样，我们这个可怜的故事竟出人意料地有了一个离奇的结尾。"
    "彼得堡忽然传开了谣言，说在卡林金桥一带，以及更远的地方，夜里出现了一个官员模样的死人，在寻找一件被抢走的外套，"
    "并且借口找那件被抢的外套，不分官阶职衔，从所有人肩上扒下各种各样的外套：猫皮的、海狸皮的、棉絮的、浣熊皮的、"
    "狐皮的、熊皮的大衣——总之，凡是人们为了遮盖自己的皮而想出来的各种毛皮和皮革。",
    ["卡林金桥"]))

# ---- The Nose, chapter II ----
NOS = "Нос (Гоголь)/Глава II"
sources["the-nose"] = NOS
lines.append(Q("nose-1", "the-nose", "ru-kazan-cathedral", "Chapter II", "第二章", NOS,
    take(NOS, "Он побежал за каретою", "величайшей набожности молился."), ["Казанским собором"],
    "He ran after the carriage, which, luckily, did not go far and stopped in front of the Kazan Cathedral.\nHe hurried "
    "into the cathedral, made his way through the row of beggar women with their faces bound up and two holes for the "
    "eyes, whom he used to laugh at so much, and went into the church. There were few worshippers inside; they all "
    "stood just by the doors. Kovalyov felt so upset that he was quite unable to pray, and searched every corner with "
    "his eyes for that gentleman. At last he saw him standing to one side. The Nose had hidden his face completely in "
    "his big stand-up collar and was praying with an expression of the greatest piety.",
    ["the Kazan Cathedral"],
    "他追着马车跑，幸好马车没走多远，就在喀山大教堂前停下了。\n他赶紧走进大教堂，穿过一排包着脸、只露出两个眼洞的乞讨老婆子——"
    "他从前总拿她们取笑——进了教堂。里面做祈祷的人不多，都只站在门口。科瓦廖夫心里乱成一团，根本没法祈祷，"
    "只顾用眼睛在各个角落里搜寻那位先生。最后他看见那人站在一旁。鼻子把脸整个藏在宽大的立领里，带着无比虔诚的神情在祈祷。",
    ["喀山大教堂"]))

# ---- A Sportsman's Sketches: 'Bezhin Meadow' ----
BEZ = "Бежин луг (Тургенев)"
sources["sportsmans-sketches"] = BEZ
lines.append(Q("hun-1", "sportsmans-sketches", "ru-bezhin-meadow", "'Bezhin Meadow'", "《别任草地》", BEZ,
    take(BEZ, "Я узнал наконец, куда я зашел.", "дождаться зари."), ["Бежина луга"],
    "At last I realised where I had got to. This meadow is famous in our parts under the name of Bezhin Meadow... But "
    "there was no way of getting home, especially at night; my legs were giving way under me from tiredness. I decided "
    "to go down to the fires and wait for the dawn in the company of the men I took for drovers.",
    ["Bezhin Meadow"],
    "我终于明白自己走到哪儿来了。这片草地在我们这一带很有名，叫做别任草地……可是要回家已经不可能了，尤其是在夜里；"
    "我累得两腿发软。我决定走到火堆那边去，和那些我当成是赶牲口的人一起等天亮。",
    ["别任草地"]))

# ---- Home of the Gentry, chapter 1 ----
GEN = "Дворянское гнездо (Тургенев)/Глава 1"
sources["home-of-the-gentry"] = GEN
lines.append(Q("gen-1", "home-of-the-gentry", "ru-noble-nest-oryol", "Chapter 1, opening", "第一章开篇", GEN,
    take(GEN, "Весенний, светлый день", "семидесяти лет."), ["губернского города О…"],
    "A bright spring day was drawing towards evening; small pink clouds stood high in the clear sky and seemed not to "
    "float past but to go away into the very depths of the azure.\nBefore the open window of a handsome house, in one of "
    "the outlying streets of the provincial town of O… (this was in 1842), sat two women, one about fifty, the other "
    "already an old woman of seventy.",
    ["the provincial town of O…"],
    "一个明媚的春日渐近黄昏；几朵粉红的小云高高停在晴朗的天空里，仿佛不是飘过去，而是退进了蔚蓝的深处。\n"
    "在省城O……的一条边远街道上，一座漂亮房子敞开的窗前（事情发生在1842年），坐着两个女人，一个五十岁上下，另一个已是七十岁的老太太。",
    ["省城O……"]))

# ---- Oblomov, opening ----
OBL = "Обломов (Гончаров)/Часть 1/Глава 1"
sources["oblomov"] = OBL
lines.append(Q("obl-1", "oblomov", "ru-gorokhovaya", "Part 1, chapter 1, opening", "第一部第一章开篇", OBL,
    take(OBL, "В Гороховой улице", "Илья Ильич Обломов."), ["В Гороховой улице"],
    "In Gorokhovaya Street, in one of those big houses whose population would have made up a whole district town, Ilya "
    "Ilyich Oblomov lay in bed in his flat one morning.",
    ["Gorokhovaya Street"],
    "在豌豆街一幢大楼里——楼里的住户多得足够组成一座县城——伊利亚·伊里奇·奥勃洛莫夫一天早上躺在他寓所的床上。",
    ["豌豆街"]))

# ---- Notes from Underground, Part 2, chapter 1 ----
UND = "Записки из подполья (Достоевский)/Часть 2/Глава 1"
sources["notes-from-underground"] = UND
lines.append(Q("und-1", "notes-from-underground", "ru-anichkov-bridge", "Part 2, chapter 1", "第二部第一章", UND,
    take(UND, "Иногда по праздникам", "шмыгающей фигурки."), ["на Невский"],
    "Sometimes on holidays I used to go to the Nevsky at about four o'clock and stroll along the sunny side. That is, I "
    "didn't stroll there at all, but went through countless torments, humiliations and overflowings of bile; but that, "
    "no doubt, was just what I needed. I darted like an eel, in the most unsightly way, among the passers-by, "
    "constantly giving way now to generals, now to officers of the Horse Guards and the hussars, now to ladies; at those "
    "moments I felt convulsive pains in my heart and a hot flush down my back at the mere thought of the wretchedness of "
    "my clothes, of the wretchedness and vulgarity of my darting little figure.",
    ["the Nevsky"],
    "有时逢到节假日，我下午四点来钟到涅瓦大街去，在向阳的那一边散步。其实我根本不是在散步，而是在经受数不清的折磨、屈辱和怒火中烧；"
    "不过，这大概正是我所需要的。我像泥鳅一样，以最难看的样子在行人中间钻来钻去，不停地给人让路，一会儿让将军，"
    "一会儿让近卫骑兵和骠骑兵军官，一会儿让太太们；这种时候，我一想到自己衣着的寒酸、想到我这钻来钻去的小身影的寒酸和猥琐，"
    "心里就一阵阵抽痛，脊背发烫。",
    ["涅瓦大街"]))

# ---- Crime and Punishment, opening ----
CP = "Преступление и наказание (Достоевский)/Часть I/Глава I"
sources["crime-and-punishment"] = CP
lines.append(Q("cp-1", "crime-and-punishment", "ru-raskolnikov-house", "Part I, chapter I, opening", "第一部第一章开篇", CP,
    take(CP, "В начале июля", "чем на квартиру."), ["С\u202f—\u2009м переулке", "высокого пятиэтажного дома"],
    "At the beginning of July, in an extremely hot spell, towards evening, a young man came out of the little room he "
    "rented from tenants in S— Lane into the street and slowly, as if undecided, set off towards K— Bridge.\nHe had "
    "safely avoided meeting his landlady on the stairs. His little room was right under the roof of a tall five-storey "
    "house and was more like a cupboard than a flat.",
    ["S— Lane", "a tall five-storey house"],
    "七月初，天气异常炎热，傍晚时分，一个年轻人从他在С胡同向二房东租住的小屋里走到街上，慢慢地、仿佛犹豫不决地朝К桥走去。\n"
    "他顺利地避开了在楼梯上碰见女房东。他的小屋就在一座高高的五层楼房的屋顶底下，与其说是住房，不如说像个柜子。",
    ["С胡同", "五层楼房"]))

# ---- The Idiot, Part III, chapter V (Ippolit's 'Necessary Explanation') ----
IDI = "Идиот (Достоевский)/Часть III/Глава V"
sources["the-idiot"] = IDI
lines.append(Q("idi-1", "the-idiot", "ru-pavlovsk", "Part III, chapter V (Ippolit's 'Necessary Explanation')",
    "第三部第五章（伊波利特的《必要的说明》）", IDI,
    take(IDI, "Я спросил его, что он подразумевает", "посмотреть на деревья."), ["Павловск"],
    "I asked him what he meant by his incessant 'trees' and why he kept pressing these 'trees' on me, and learned from "
    "him with surprise that I myself had supposedly said, that evening, that I had come to Pavlovsk to look at the "
    "trees for the last time.",
    ["Pavlovsk"],
    "我问他，他那没完没了的“树”是什么意思，为什么老把这些“树”硬塞给我，结果我惊讶地从他那里得知，"
    "好像是我自己在那天晚上说过，我到巴甫洛夫斯克来，是为了最后看一看那些树。",
    ["巴甫洛夫斯克"]))

# ---- War and Peace, Volume 3, Part 2, chapter XXX ----
WP = "Война и мир (Толстой)/Том 3"
sources["war-and-peace"] = WP
lines.append(Q("wp-1", "war-and-peace", "ru-borodino", "Volume 3, Part 2, chapter XXX", "第三卷第二部第三十章", WP,
    plus(take(WP, "Войдя по ступенькам входа на курган", "длинные тени."),
         take(WP, "Всё это было оживленно", "по обеим сторонам ее.", after="Войдя по ступенькам входа на курган")),
    ["Бородина"],
    "Going up the steps onto the mound, Pierre looked ahead of him and froze in delight at the beauty of the spectacle. "
    "It was the same panorama he had admired from this mound the day before; but now the whole of this ground was "
    "covered with troops and the smoke of gunfire, and the slanting rays of the bright sun, rising behind and to the "
    "left of Pierre, cast on it, in the clear morning air, a piercing light with a gold and pink tinge, and dark, long "
    "shadows.\n…\nAll this was lively, majestic and unexpected; but what struck Pierre most of all was the sight of the "
    "battlefield itself, of Borodino and the hollow over the Kolocha on both sides of it.",
    ["Borodino"],
    "皮埃尔踏着台阶走上土丘，向前一望，被眼前壮美的景象惊呆了。这还是昨天他在这座土丘上欣赏过的那片全景；"
    "可是现在，整个这片地方布满了军队和炮火的硝烟，明亮的太阳从皮埃尔身后偏左的地方升起，斜射的光线在清澈的晨空里给它洒上一层"
    "带着金色和玫瑰色的、穿透一切的光，投下长长的暗影。\n…\n这一切生气勃勃、雄伟壮观，出人意料；但最使皮埃尔震动的，"
    "是战场本身的景象：博罗季诺，以及科洛恰河两岸的洼地。",
    ["博罗季诺"]))

# ---- Anna Karenina, Part VII, chapters XXX and XXXI ----
AK30, AK31 = "Анна Каренина (Толстой)/Часть VII/Глава XXX", "Анна Каренина (Толстой)/Часть VII/Глава XXXI"
sources["anna-karenina"] = AK31
lines.append(Q("ak-1", "anna-karenina", "ru-obiralovka", "Part VII, chapter XXX", "第七部第三十章", AK30,
    take(AK30, "— Прикажете до Обираловки?", "вышла из коляски."), ["Обираловки"],
    "'To Obiralovka, madam?' said Pyotr.\nShe had quite forgotten where and why she was going, and only with a great "
    "effort could she understand the question.\n'Yes,' she said to him, handing him her purse, and, taking her little "
    "red bag on her arm, she got out of the carriage.",
    ["Obiralovka"],
    "“您是要去奥比拉洛夫卡吧？”彼得说。\n她完全忘了自己要去哪里、为什么去，费了好大劲才听懂这个问题。\n"
    "“是的，”她对他说，把钱包递给他，挎起那个红色小手提包，下了马车。",
    ["奥比拉洛夫卡"]))
lines.append(Q("ak-2", "anna-karenina", "ru-obiralovka", "Part VII, chapter XXXI", "第七部第三十一章", AK31,
    take(AK31, "И вдруг, вспомнив о раздавленном", "проходящего поезда."),
    ["по ступенькам, которые шли от водокачки к рельсам"],
    "And suddenly, remembering the man who had been crushed on the day she first met Vronsky, she understood what she "
    "had to do. With a quick, light step she went down the steps that led from the water tower to the rails, and "
    "stopped right beside the train that was passing her.",
    ["the steps that led from the water tower to the rails"],
    "她忽然想起她和弗龙斯基初次相遇那天被轧死的那个人，于是明白了自己该怎么做。她迈着轻快的步子，走下从水塔通向铁轨的台阶，"
    "紧挨着从她身旁驶过的列车站住。",
    ["从水塔通向铁轨的台阶"]))

# ---- Lady Macbeth of the Mtsensk District, opening ----
LM = "Леди Макбет Мценского уезда (Лесков)"
sources["lady-macbeth-mtsensk"] = LM
lines.append(Q("lm-1", "lady-macbeth-mtsensk", "ru-mtsensk", "Chapter 1, opening", "第一章开篇", LM,
    take(LM, "Иной раз в наших местах", "леди Макбет Мценского уезда."), ["Мценского уезда"],
    "Now and then characters turn up in our parts of such a kind that, however many years have passed since you met "
    "them, you can never recall some of them without a tremor of the soul. Among such characters is the merchant's wife "
    "Katerina Lvovna Izmailova, who once played out a terrible drama, after which our gentry, from someone's light "
    "remark, took to calling her the Lady Macbeth of the Mtsensk District.",
    ["the Mtsensk District"],
    "我们这一带有时会出这样的人物，不管同他们相遇已过去多少年，想起其中有些人来，心里总不免发颤。商人的妻子卡捷琳娜·利沃夫娜·"
    "伊兹梅洛娃就是这样一个人物，她曾经演出过一场可怕的悲剧，此后我们这里的贵族们，不知是谁随口一说，便叫她姆岑斯克县的麦克白夫人。",
    ["姆岑斯克县"]))

# ---- The Enchanted Wanderer, opening ----
EW = "Очарованный странник (Лесков)/Глава первая"
sources["enchanted-wanderer"] = EW
lines.append(Q("ew-1", "enchanted-wanderer", "ru-konevets", "Chapter 1, opening", "第一章开篇", EW,
    take(EW, "Мы плыли по Ладожскому озеру", "и мы снова отплыли."), ["от острова Коневца к Валааму"],
    "We were sailing across Lake Ladoga from Konevets Island to Valaam, and on the way put in at the landing stage at "
    "Korela on ship's business. Here many of us were curious enough to go ashore, and drove on lively Finnish ponies "
    "into the desolate little town. Then the captain made ready to continue the voyage, and we sailed again.",
    ["from Konevets Island to Valaam"],
    "我们乘船在拉多加湖上从科涅韦茨岛驶往瓦拉姆，途中因船上的事务在科列拉的码头靠了岸。我们当中许多人出于好奇上了岸，"
    "坐着芬兰人的矫健小马到那荒凉的小城里去了一趟。随后船长准备继续航行，我们又开船了。",
    ["从科涅韦茨岛驶往瓦拉姆"]))

# ---- My Past and Thoughts, Part 1, chapter 4 ----
PT = "Былое и думы (Герцен)/Часть 1"
sources["my-past-and-thoughts"] = PT
pt, pt_nb = take(PT, "Мы ушли от них вперед", "избранную нами борьбу.")
pa, pb = pt.split("\nЗапыхавшись")
lines.append(Q("pt-1", "my-past-and-thoughts", "ru-sparrow-hills", "Part 1, chapter 4", "第一部第四章", PT,
    (" ".join(pa.split("\n")) + "\n" + " ".join(("Запыхавшись" + pb).split("\n")), pt_nb),
    ["на Воробьевых горах", "в виду всей Москвы"],
    "We went on ahead of them and, far in front, ran up to the site where Vitberg's church had been founded on the "
    "Sparrow Hills.\nOut of breath and flushed, we stood there wiping off the sweat. The sun was setting, the domes "
    "glittered, the city spread over an immeasurable space below the hill, a fresh breeze blew on us; we stood a while, "
    "stood, leaned on each other and, suddenly embracing, swore, in sight of all Moscow, to sacrifice our lives to the "
    "struggle we had chosen.",
    ["Sparrow Hills", "in sight of all Moscow"],
    "我们走在他们前面，远远地把他们甩在后头，跑上了麻雀山上维特贝格大教堂的奠基处。\n我们气喘吁吁、满脸通红地站在那里擦汗。"
    "太阳正在落下，圆顶闪闪发光，城市在山下铺展成一望无际的一片，清新的微风吹拂着我们。我们站了一会儿，又站了一会儿，"
    "彼此倚靠着，忽然拥抱在一起，当着整个莫斯科宣誓：把我们的生命献给我们选定的斗争。",
    ["麻雀山", "当着整个莫斯科"], JOINED))

# ---- The Lady with the Dog: its quotation (lwd-1, on the Yalta Embankment) is written by add_ua1.py, since the atlas
# draws Crimea in Ukraine (decision A-22); the book stays in data/ru and still gets its source here ----
LWD = "Дама с собачкой (Чехов)"
sources["lady-with-the-dog"] = LWD

# ---- The Lower Depths, Act 1 (1986 edition) ----
LD = "На дне (Горький)/ИС 1986"
sources["lower-depths"] = LD
lines.append(Q("ld-1", "lower-depths", "ru-bugrov-dosshouse", "Act 1, opening stage direction", "第一幕开场舞台说明", LD,
    take(LD, "Подвал, похожий на пещеру.", "Везде по стенам — нары."), ["Подвал, похожий на пещеру"],
    "A cellar like a cave. The ceiling: heavy stone vaults, sooty, with the plaster fallen off. The light comes from the "
    "audience and, from above downwards, through a square window on the right. The right-hand corner is taken up by "
    "Pepel's room, fenced off with thin partitions; by the door of this room are Bubnov's plank beds. In the left corner "
    "a big Russian stove; in the left-hand stone wall a door into the kitchen, where Kvashnya, the Baron and Nastya "
    "live. Between the stove and the door, against the wall, a wide bed hidden by a dirty cotton curtain. Plank beds "
    "everywhere along the walls.",
    ["A cellar like a cave"],
    "一个像山洞的地下室。天花板是沉重的石头拱顶，熏得乌黑，灰泥已经剥落。光线从观众这边来，还从右边一扇方窗由上往下照进来。"
    "右边角落是用薄板隔出来的佩佩尔的小屋，小屋门边是布勃诺夫的板铺。左边角落里有一座大俄式炉子；左边石墙上有一扇门通厨房，"
    "克瓦什尼娅、男爵和娜斯佳住在那里。炉子和门之间靠墙放着一张宽床，挂着一块肮脏的印花布帐子。四面墙边全是板铺。",
    ["像山洞的地下室"]))

# ---- Mother, Part 1, chapter I ----
MOT = "Мать (Горький)"
sources["mother-gorky"] = MOT
lines.append(Q("mot-1", "mother-gorky", "ru-sormovo", "Part 1, chapter I, opening", "第一部第一章开篇", MOT,
    take(MOT, "Каждый день над рабочей слободкой", "как толстые палки."), ["рабочей слободкой", "фабрики"],
    "Every day over the workers' settlement, in the smoky, oily air, the factory hooter shook and roared, and, obeying "
    "its call, sullen people who had not had time to refresh their muscles with sleep ran out of the small grey houses "
    "into the street like frightened cockroaches. In the cold half-light they walked along the unpaved street to the "
    "tall stone cages of the factory, which waited for them with indifferent assurance, lighting the muddy road with "
    "dozens of greasy square eyes. The mud squelched underfoot. Hoarse exclamations of sleepy voices rang out, coarse "
    "curses angrily tore the air, and towards the people floated other sounds: the heavy bustle of machines, the "
    "grumbling of steam. Gloomy and stern, the tall black chimneys loomed, rising over the settlement like thick sticks.",
    ["the workers' settlement", "the factory"],
    "每天，在工人村的上空，在烟雾弥漫、油腻腻的空气里，工厂的汽笛颤抖着、吼叫着。听到它的召唤，还没来得及用睡眠恢复筋骨的"
    "阴郁的人们，像受惊的蟑螂一样，从一座座灰色的小房子里跑到街上。在寒冷的晨昏中，他们沿着没有铺石的街道走向工厂那一座座"
    "高大的石头笼子，工厂带着冷漠的自信等着他们，用几十只油腻的方眼睛照亮泥泞的道路。烂泥在脚下咕唧作响。睡意朦胧的嗓音"
    "发出沙哑的叫喊，粗野的咒骂恶狠狠地撕破空气，迎着人们飘来的是另一些声音：机器沉重的忙乱声，蒸汽的嘟囔声。"
    "高高的黑烟囱阴沉而严峻地耸立着，像一根根粗棍子竖在工人村上空。",
    ["工人村", "工厂"]))

# ---- Petersburg, chapter 6 ----
PET = "Петербург (Белый)/Версия 2"
sources["petersburg-bely"] = PET
pet, pet_nb = take(PET, "Пустовала вся площадь.", "закрывали глаза.", after="Верно в час полуночи")
assert pet.count("тяжелозвонкое*") == 1
lines.append(Q("pet-1", "petersburg-bely", "ru-bronze-horseman", "Chapter 6", "第六章", PET,
    (pet.replace("тяжелозвонкое*", "тяжелозвонкое"), pet_nb), ["на скалу", "Медный Всадник"],
    "The whole square was empty.\nAt that midnight hour metal hooves fell clanging onto the rock; the horse snorted "
    "into the incandescent mist; the bronze outline of the Horseman now separated from the horse's crupper, and the "
    "ringing spur scratched the horse's flank impatiently, so that the horse would leap down from the rock.\nAnd the "
    "horse leapt down from the rock.\nA heavy, ringing clatter rushed over the stones, across the bridge, to the "
    "islands. The Bronze Horseman flew past into the mist; in his eyes was a greenish depth; the muscles of his metal "
    "arms straightened, tensed; and the bronze crown of his head jerked forward; the horse's hooves came down on the "
    "cobbles in swift, dazzling arcs; the horse's mouth tore open in a deafening neigh like the whistle of a locomotive; "
    "thick steam from its nostrils scalded the street with luminous boiling water; horses coming the other way shied in "
    "terror, snorting; and passers-by shut their eyes in terror.",
    ["the rock", "The Bronze Horseman"],
    "整个广场空无一人。\n在这午夜时分，金属的马蹄落在岩石上，铿然作响；马打着响鼻，喷进灼热的雾里；骑士的青铜轮廓此刻从马背上分离出来，"
    "叮当作响的马刺不耐烦地划了一下马肚，要马从岩石上跃下。\n马从岩石上跃了下来。\n沉重而响亮的嗒嗒声越过石头路，过了桥，奔向群岛。"
    "青铜骑士飞进雾里；他眼中是一片泛绿的深渊；金属手臂的肌肉伸直了，绷紧了；青铜的头顶猛地向前一冲；马蹄落在圆石路上，"
    "划出一道道迅疾而耀眼的弧线；马嘴张开，发出震耳欲聋的嘶鸣，像火车头的汽笛；鼻孔里喷出的浓浓蒸汽像发光的滚水浇在街上；"
    "迎面而来的马惊恐地打着响鼻往旁边躲；行人吓得闭上了眼睛。",
    ["岩石", "青铜骑士"], "; the endnote asterisk after 'тяжелозвонкое' left out"))

# ---- The Twelve Chairs, chapter XXXVI ----
TC = "Двенадцать стульев (Ильф и Петров)/Глава XXXVI"
sources["twelve-chairs"] = TC
lines.append(Q("tc-1", "twelve-chairs", "ru-proval", "Chapter XXXVI", "第三十六章", TC,
    take(TC, "Великий комбинатор двинулся", "туристов-одиночек."), ["к Провалу"],
    "The great schemer set off at a rifleman's pace along the mountain road that leads round Mashuk to the spot where "
    "Lermontov fought his duel with Martynov, past sanatoriums and rest homes.\nOvertaken by buses and two-horse "
    "carriages, Ostap came out at the Proval.\nA small gallery cut into the rock led to a cone-shaped pit. The gallery "
    "ended in a little balcony, standing on which you could see at the bottom of the Proval a puddle of malachite-green, "
    "foul-smelling liquid. This Proval is considered one of the sights of Pyatigorsk, and so a good number of "
    "excursions and lone tourists visit it every day.",
    ["the Proval"],
    "伟大的谋略家迈着步兵的步伐，沿着那条绕马舒克山通往莱蒙托夫与马丁诺夫决斗之地的山路走去，路过一座座疗养院和休养所。\n"
    "公共汽车和双马马车一辆辆超过他，奥斯塔普来到了普罗瓦尔。\n一条凿在岩石里的小坑道通向一个锥形的深坑。坑道尽头是个小阳台，"
    "站在上面能看见普罗瓦尔坑底一小汪孔雀石般碧绿、臭烘烘的水。这个普罗瓦尔被看作五山城的名胜，所以每天来参观的旅游团和散客为数不少。",
    ["普罗瓦尔"]))

# ---------- write ----------
replaced = {"life-of-avvakum": ["avv-s1"], "poor-liza": ["liza-s1"], "woe-from-wit": ["wfw-s1"],
            "eugene-onegin": ["one-s1"], "tales-of-belkin": ["bel-s1"], "bronze-horseman": ["bh-s1"],
            "hero-of-our-time": ["hero-s1"], "the-overcoat": ["ovc-s1"], "the-nose": ["nose-s1"],
            "sportsmans-sketches": ["hun-s1"], "home-of-the-gentry": ["gen-s1"], "oblomov": ["obl-s1"],
            "notes-from-underground": ["und-s1"], "crime-and-punishment": ["cp-s1"], "the-idiot": ["idi-s1"],
            "war-and-peace": ["wp-s1"], "anna-karenina": ["ak-s1"], "lady-macbeth-mtsensk": ["lm-s1"],
            "enchanted-wanderer": ["ew-s1"], "my-past-and-thoughts": ["pt-s1"],
            "lower-depths": ["ld-s1"], "mother-gorky": ["mot-s1"], "petersburg-bely": ["pet-s1"],
            "twelve-chairs": ["tc-s1"]}
assert set(replaced) == {l["book_id"] for l in lines} == set(sources) - {"lady-with-the-dog"}
lp = b.data("lines.js")
existing = set(re.findall(r'  \{ id: "([^"]+)"', open(lp, encoding="utf-8").read()))
assert not ({l["id"] for l in lines} & existing), "ids already in use"
drop_entries(lp, {i for v in replaced.values() for i in v})
b.append(lp, lines, "11-22 quotations from Russian Wikisource, replacing the placeholder scene notes (add_ru3.py)")
for bid, title in sources.items():
    set_source(b.data("books.js"), bid, ws.url("ru", title))
print(len(lines), "quotations for", len(replaced), "books;", sum(map(len, replaced.values())), "scene notes replaced")
