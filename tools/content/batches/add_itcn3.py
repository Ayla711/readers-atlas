"""11-22: Italy and China, the last public-domain books with placeholder scene notes only. Each quotation replaces
the book's scene note; English and Chinese translations are our own drafts for review (translation: "own").

Sources:
- I Fioretti (Italian Wikisource) and Tales of Hulan River (Chinese Wikisource): the rendered page's own text, read
  with tools/content/wikisource.py;
- Der Jäger Gracchus (German Wikisource) and Le Lépreux de la cité d'Aoste (French Wikisource): those two sites
  cannot be reached from the scripts here, so the text was read from the page in a browser on 11-22 and is written
  out below; `checked` says so.

What a cut changes, named again in that line's `checked`: in the Fioretti the transcription breaks a line inside the
last sentence; the lines are joined.

Still scene notes only: From Emperor to Citizen (not on Wikisource; Puyi's memoir is still in copyright in the US).

Usage: python3 -I add_itcn3.py <app_dir> <it_wikisource_dir> <zh_wikisource_dir>"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws
from datafile import drop_entries, set_source

APP, WS_IT, WS_ZH = sys.argv[1], sys.argv[2], sys.argv[3]
DATE = "2026-11-22"
GAP = b.GAP

def raw(d, title, start, end):
    t = ws.text(d, title)
    i = t.find(start)
    assert i >= 0, (title, start)
    j = t.find(end, i)
    assert j >= 0, (title, start, end)
    return t[i:j + len(end)]

def check(id, pairs):
    for text, hls in pairs:
        for h in hls:
            assert h in text, (id, h)

def Q(id, book, place, loc, loc_zh, orig, hl_orig, en, hl_en, zh, hl_zh, checked):
    check(id, [(orig, hl_orig), (en, hl_en), (zh, hl_zh)])
    assert "  " not in orig and "\xa0" not in orig, (id, "spacing")
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh,
                text_orig=orig, highlight_orig=hl_orig, text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh,
                translation="own", status="draft", checked=f"{checked}, {DATE}")

# ================= Italy =================
it = []
FIO = "Fioretti di San Francesco/Capitolo ottavo"
fio_b = raw(WS_IT, FIO, "E san Francesco si gli rispose:", "che qui è\nperfetta letizia.")
it.append(Q("it-lf-1", "little-flowers-of-st-francis", "it-assisi", "Chapter 8", "第 8 章",
    raw(WS_IT, FIO, "Venendo una volta san Francesco da Perugia", "che non è quivi perfetta letizia.") + GAP
    + " ".join(fio_b.split("\n")),
    ["Santa Maria degli Agnoli", "Santa Maria degli Angeli"],
    "Once, when St Francis was coming from Perugia to Santa Maria degli Angeli with Brother Leo in winter, and the very "
    "great cold pained him sorely, he called Brother Leo, who was walking ahead, and said this: Brother Leo, although "
    "the Friars Minor in every land give a great example of holiness and good edification, nevertheless write, and note "
    "carefully, that perfect joy is not in that.\n…\nAnd St Francis answered him: When we come to Santa Maria degli "
    "Angeli, soaked with rain and frozen with cold and splashed with mud and afflicted with hunger, and knock at the "
    "door of the house, and the porter comes angrily and says, 'Who are you?' and we say, 'We are two of your "
    "brothers,' and he says, 'You are not telling the truth; you are two rogues who go about deceiving the world and "
    "stealing the alms of the poor; go away'; and he does not open to us, but makes us stand outside in the snow and "
    "the rain, with cold and hunger, until nightfall: then, if we bear such insult and such cruelty and such dismissals "
    "patiently, without being troubled and without murmuring against him, and think humbly and charitably that the "
    "porter truly knows us and that God makes him speak against us: O Brother Leo, write that here is perfect joy.",
    ["Santa Maria degli Angeli"],
    "有一次，圣方济各和利奥弟兄在冬天从佩鲁贾往天使圣母堂去，严寒狠狠折磨着他。他叫住走在前面的利奥弟兄，这样说道：利奥弟兄，"
    "虽然小兄弟会的弟兄们在各地都树立了圣德和善表的伟大榜样，你还是要写下来，仔细记住：完美的喜乐不在这里。\n…\n"
    "圣方济各回答他说：当我们到了天使圣母堂，被雨淋透，被冻僵，满身泥浆，又饥肠辘辘，去敲会院的门；看门人气冲冲地出来，说："
    "“你们是谁？”我们说：“我们是你们的两个弟兄。”他却说：“你们说谎；你们是两个无赖，到处骗人，偷穷人的施舍；走开！”"
    "他不给我们开门，让我们在雪里雨里挨冻挨饿，一直站到天黑；这时，如果我们能耐心忍受这样的侮辱、这样的冷酷、这样的驱赶，"
    "不烦乱，也不抱怨他，还谦卑地、怀着爱心想：这看门人真的认识我们，是天主让他这样说我们：啊，利奥弟兄，你写下来，"
    "这里才是完美的喜乐。",
    ["天使圣母堂"],
    f"Italian Wikisource, {FIO} (a line break inside the last sentence joined)"))

it.append(Q("it-hg-1", "the-hunter-gracchus", "it-riva-del-garda", "Opening; the mayor", "开篇；市长",
    "Zwei Knaben saßen auf der Quaimauer und spielten Würfel. Ein Mann las eine Zeitung auf den Stufen eines Denkmals "
    "im Schatten des säbelschwingenden Helden. Ein Mädchen am Brunnen füllte Wasser in ihre Bütte. Ein Obstverkäufer "
    "lag neben seiner Wage und blickte auf den See hinaus. In der Tiefe einer Kneipe sah man durch die leeren Tür- und "
    "Fensterlöcher zwei Männer beim Wein. Der Wirt saß vorn an einem Tisch und schlummerte. Eine Barke schwebte leise, "
    "als werde sie über dem Wasser getragen, in den kleinen Hafen. Ein Mann in blauem Kittel stieg ans Land und zog die "
    "Seile durch die Ringe. Zwei andere Männer in dunklen Röcken mit Silberknöpfen trugen hinter dem Bootsmann eine "
    "Bahre, auf der unter einem großen blumengemusterten gefransten Seidentuch offenbar ein Mensch lag." + GAP
    + "Sofort schlug der Mann auf der Bahre die Augen auf, wandte schmerzlich lächelnd das Gesicht dem Herrn zu und "
    "sagte: „Wer bist du?“ – Der Herr erhob sich ohne weiteres Staunen aus seiner knieenden Stellung und antwortete: "
    "„Der Bürgermeister von Riva.“",
    ["in den kleinen Hafen", "Riva"],
    "Two boys were sitting on the harbour wall playing dice. A man was reading a newspaper on the steps of a monument, "
    "in the shadow of the sabre-swinging hero. A girl at the fountain was filling her tub with water. A fruit-seller lay "
    "beside his scales, looking out at the lake. In the depths of a tavern two men could be seen at their wine through "
    "the empty holes of door and windows. The landlord sat at a table in front, dozing. A barque floated softly into the "
    "little harbour, as if it were being carried over the water. A man in a blue smock stepped ashore and drew the "
    "ropes through the rings. Two other men in dark coats with silver buttons carried a bier behind the boatman, on "
    "which, under a large flower-patterned fringed silk cloth, a person evidently lay.\n…\nAt once the man on the bier "
    "opened his eyes, turned his face, smiling painfully, towards the gentleman and said: 'Who are you?' Without "
    "further astonishment the gentleman rose from his kneeling position and answered: 'The Mayor of Riva.'",
    ["the little harbour", "Riva"],
    "两个男孩坐在码头的堤墙上掷骰子。一个男人坐在纪念碑的台阶上，在那位挥舞军刀的英雄的阴影里读报。一个姑娘在泉边往木桶里装水。"
    "一个卖水果的躺在他的秤旁边，望着湖面。透过一家小酒馆空荡荡的门洞和窗洞，能看见里面深处有两个男人在喝酒。店主坐在前面一张桌旁打盹。"
    "一条小船悄无声息地漂进小港，仿佛是被托着从水面上送过来的。一个穿蓝罩衫的男人上了岸，把缆绳穿过铁环。另外两个穿深色外衣、"
    "钉着银扣子的男人跟在船夫后面，抬着一副担架，担架上盖着一块印花带流苏的大丝绸，下面显然躺着一个人。\n…\n"
    "担架上的人立刻睁开眼睛，带着痛苦的微笑把脸转向那位先生，说：“你是谁？”那位先生并不再惊讶，从跪着的姿势站起来，"
    "回答说：“里瓦的市长。”",
    ["小港", "里瓦"],
    "German Wikisource, Der Jäger Gracchus (from Beim Bau der Chinesischen Mauer, 1931; read in a browser)"))

it.append(Q("it-lep-1", "leper-of-aosta", "it-aosta-leper-tower", "Opening", "开篇",
    "Plus loin, à quelques centaines de pas, est une tour carrée, adossée au mur antique et construite avec le marbre "
    "dont il était jadis revêtu : on l’appelle la Tour de la frayeur, parce que le peuple l’a crue longtemps habitée par "
    "des revenants. Les vieilles femmes de la cité d’Aoste se ressouviennent fort bien d’en avoir vu sortir, pendant les "
    "nuits sombres, une grande femme blanche, tenant une lampe à la main.\nIl y a environ quinze ans que cette tour fut "
    "réparée par ordre du gouvernement et entourée d’une enceinte, pour y loger un lépreux et le séparer ainsi de la "
    "société, en lui procurant tous les agréments dont sa triste situation était susceptible.",
    ["une tour carrée", "la Tour de la frayeur"],
    "Further on, a few hundred paces away, is a square tower, backing onto the ancient wall and built with the marble "
    "that once faced it: it is called the Tower of Fright, because the people long believed it haunted by ghosts. The "
    "old women of the city of Aosta remember very well having seen come out of it, on dark nights, a tall white woman "
    "holding a lamp in her hand.\nSome fifteen years ago this tower was repaired by order of the government and "
    "surrounded by an enclosure, to house a leper and so separate him from society, while giving him all the comforts "
    "his sad situation allowed.",
    ["a square tower", "the Tower of Fright"],
    "再往前几百步，有一座方塔，背靠古城墙，是用从前贴在墙上的大理石砌成的：人们管它叫“惊恐塔”，因为老百姓很久以来都相信里面闹鬼。"
    "奥斯塔城的老妇人们清楚地记得，在漆黑的夜里，曾看见一个高大的白衣女人手里提着一盏灯从塔里走出来。\n大约十五年前，"
    "政府下令修缮了这座塔，在四周围上一道围墙，用来安置一个麻风病人，把他同社会隔开，同时尽他那悲惨处境所能允许的，为他提供一切便利。",
    ["一座方塔", "惊恐塔"],
    "French Wikisource, Le Lépreux de la cité d’Aoste (Œuvres complètes, Firmin-Didot, 1880; read in a browser)"))

# ================= China =================
cn = []
HLH = "呼蘭河傳/第三章"
cn.append(Q("cn-hlh-1", "tales-of-hulan-river", "cn-xiao-hong-residence", "Chapter 3", "第三章",
    raw(WS_ZH, HLH, "呼蘭河這小城裡邊住著我的祖父。", "樣樣都有。") + GAP
    + raw(WS_ZH, HLH, "花開了，就像花睡醒了似的。", "都是自由的。"),
    ["呼蘭河這小城", "大花園"],
    "In the little town of Hulan River lived my grandfather.\nWhen I was born, Grandfather was already over sixty; by "
    "the time I was four or five, he was nearly seventy.\nOur family had a big garden, and in this garden there were "
    "bees, butterflies, dragonflies and grasshoppers, every kind of thing.\n…\nWhen the flowers opened, it was as if "
    "the flowers had woken from sleep. When the birds flew, it was as if the birds had gone up to heaven. When the "
    "insects chirped, it was as if the insects were talking. Everything was alive. Everything had boundless powers: "
    "whatever it wanted to do, it did; however it wanted to be, so it was. Everything was free.",
    ["the little town of Hulan River", "a big garden"],
    "呼兰河这小城里边住着我的祖父。\n我生的时候，祖父已经六十多岁了，我长到四五岁，祖父就快七十了。\n"
    "我家有一个大花园，这花园里蜂子、蝴蝶、蜻蜓、蚂蚱，样样都有。\n…\n花开了，就像花睡醒了似的。鸟飞了，就像鸟上天了似的。"
    "虫子叫了，就像虫子在说话似的。一切都活了。都有无限的本领，要做什么，就做什么。要怎么样，就怎么样。都是自由的。",
    ["呼兰河这小城", "大花园"],
    f"Chinese Wikisource, {HLH}"))

# ---------- write ----------
plan = [("it", it, {"it-lf-s1", "it-hg-s1", "it-lep-s1"},
         {"little-flowers-of-st-francis": ws.url("it", FIO),
          "the-hunter-gracchus": "https://de.wikisource.org/wiki/Der_J%C3%A4ger_Gracchus",
          "leper-of-aosta": "https://fr.wikisource.org/wiki/Le_L%C3%A9preux_de_la_cit%C3%A9_d%E2%80%99Aoste"}),
        ("cn", cn, {"cn-hlh-s1"}, {"tales-of-hulan-river": ws.url("zh", HLH)})]
for cc, qs, scenes, srcs in plan:
    b.init(APP, None, cc, DATE)
    lp = b.data("lines.js")
    existing = set(re.findall(r'  \{ id: "([^"]+)"', open(lp, encoding="utf-8").read()))
    assert scenes <= existing and not ({q["id"] for q in qs} & existing), cc
    drop_entries(lp, scenes)
    b.append(lp, qs, "11-22 quotations from Wikisource, replacing the placeholder scene notes (add_itcn3.py)")
    for bid, url in srcs.items():
        set_source(b.data("books.js"), bid, url)
    print(cc, len(qs), "quotations;", len(scenes), "scene notes replaced")
