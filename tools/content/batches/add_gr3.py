"""11-22: Greece, quotations for the public-domain books that had only placeholder scene notes, taken from Greek
Wikisource (tools/content/wikisource.py: the rendered page's own text). English and Chinese are our own translations
(translation: "own"), drafts for review. Each quotation replaces the book's placeholder scene note.

What a cut changes, each named again in that line's `checked`:
- the editions number the lines of verse (at the head or the end of a line): the numbers are left out, and so is the
  indent the Erotokritos page sets before the second line of each couplet;
- Herodotus, Thucydides and Plato carry section and Stephanus markers ([226.2], [327b], 'd') inside the prose: the
  markers inside a cut are left out.

Still scene notes only (no line sets the book at the place on the map): The Clouds and The Symposium (the Agora is not
their scene), the Nicomachean Ethics (the Lyceum is never named), Sappho (her fragments do not name Eresos), The Beggar
(Kravara is named only in passing), The Murderess (the novel never names Skiathos), Makriyannis's Memoirs (the
Makrygianni quarter is named after him, not by him), Honour and Money (Mantouki is not the Old Town of Corfu).

Usage: python3 -I add_gr3.py <app_dir> <wikisource_dir>   (python3 -I ../wikisource.py <dir> el <title> … downloads)"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws
from datafile import drop_entries, set_source

APP, WS = sys.argv[1], sys.argv[2]
DATE = "2026-11-22"
b.init(APP, None, "gr", DATE)
GAP = b.GAP
NUMS = " (the edition's line numbers left out)"

def raw(title, start, end, after=None):
    t = ws.text(WS, title)
    i = t.find(start, t.find(after) if after else 0)
    assert i >= 0, (title, start)
    j = t.find(end, i)
    assert j >= 0, (title, start, end)
    return t[i:j + len(end)]

def verse(title, start, end, numbered=True):
    """lines of verse, each line's indent and the edition's line number (at its head or end) taken off"""
    s = raw(title, start, end)
    out = []
    for l in s.split("\n"):
        l = l.strip(" \t\xa0")
        l = re.sub(r"^\d+\s+", "", l)
        l = re.sub(r"[\s\xa0]+\d+$", "", l)
        out.append(l)
    v = "\n".join(out)
    assert (v != s) == numbered, (title, start, "numbered?")
    return v

def prose(title, start, end, markers=()):
    """one passage of prose; each marker named in `markers` must be inside it, and is taken out"""
    s = raw(title, start, end)
    for m in markers:
        assert s.count(m) == 1, (title, m)
        s = s.replace(m, " " if m.startswith(" ") and m.endswith(" ") else "")
    assert "\n" not in s, (title, start)
    return s

def Q(id, book, place, loc, loc_zh, title, orig, hl_orig, en, hl_en, zh, hl_zh, note=""):
    for h in hl_orig:
        assert h in orig, (id, h)
    for h in hl_en:
        assert h in en, (id, h)
    for h in hl_zh:
        assert h in zh, (id, h)
    assert "  " not in orig and "\xa0" not in orig and "\t" not in orig, (id, "spacing")
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh,
                text_orig=orig, highlight_orig=hl_orig, text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh,
                translation="own", status="draft", checked=f"Greek Wikisource, {title}{note}, {DATE}")

lines, sources = [], {}

# ---- The Odyssey, Book 9 ----
OD = "Ὀδύσσεια ι"
sources["odyssey"] = OD
lines.append(Q("odyssey-1", "odyssey", "gr-ithaca", "Book 9, lines 21–28", "第九卷第 21–28 行", OD,
    verse(OD, "ναιετάω δ' Ἰθάκην", "ἄλλο ἰδέσθαι."), ["Ἰθάκην"],
    "I dwell in clear-seen Ithaca; on it is a mountain,\nNeriton, its leaves shaking, standing out from afar; and round "
    "it lie islands,\nmany, very close to one another,\nDoulichion and Same and wooded Zakynthos.\nIthaca itself lies "
    "low, furthest of all in the sea\ntowards the dusk, while the others lie apart towards the dawn and the sun;\na rugged "
    "land, but a good nurse of young men; for my part\nI can see nothing sweeter than one's own land.",
    ["Ithaca"],
    "我住在阳光明媚的伊萨卡，岛上有座山，\n涅里托斯山，林木摇曳，远远望去十分醒目；四周有许多岛屿，\n彼此紧紧相邻，\n"
    "杜利基昂、萨墨，还有林木茂密的扎昆托斯。\n伊萨卡地势低平，在大海中最远，\n朝着昏暗的西方，其他的岛屿则远远朝着黎明和太阳；\n"
    "这地方崎岖，却是养育少年的好地方；在我看来，\n再没有什么比自己的故土更甜美可看的了。",
    ["伊萨卡"], NUMS))

# ---- The Oresteia: The Eumenides ----
EUM = "Ευμενίδες"
sources["oresteia"] = EUM
lines.append(Q("oresteia-1", "oresteia", "gr-areopagus", "The Eumenides, lines 681–695", "《报仇神》第 681–695 行", EUM,
    verse(EUM, "κλύοιτ᾽ ἂν ἤδη θεσμόν", "εὑρήσεις ποτόν."), ["πάγον δ᾽ Ἄρειον", "πάγος τ᾽ Ἄρειος"],
    "Hear now my ordinance, people of Attica,\nyou who judge the first trial for blood shed.\nFor the future too, for "
    "the people of Aegeus,\nthis council of judges shall always remain.\nThis Hill of Ares, the seat of the Amazons\nand "
    "their tents, when they came in hatred of Theseus\nleading an army, and built up towers against the city,\nthis new "
    "city with its high towers,\nand sacrificed to Ares, whence the rock\nis named the Hill of Ares: on it the citizens' "
    "awe\nand its kinsman, fear, shall keep them from wrongdoing\nby day and by night alike,\nso long as the citizens "
    "themselves do not alter the laws\nwith evil inflows; if you foul clear water\nwith mud you will never find a drink.",
    ["This Hill of Ares", "the Hill of Ares"],
    "阿提卡的人民啊，现在听我立下的规矩，\n你们是审判第一桩流血案件的人。\n今后，为埃勾斯的子民，\n这个法官的议事会将永远存在。\n"
    "这座战神山，从前阿马宗女战士\n怀着对忒修斯的仇恨率军前来时，\n在这里扎营安帐，筑起塔楼对抗这座城，\n这座新建的、塔楼高耸的城，\n"
    "她们在这里向战神阿瑞斯献祭，这块岩石由此得名，\n叫做战神山：在这里，市民的敬畏\n和与它同源的恐惧，将使他们不敢作恶，\n"
    "无论白天还是黑夜，\n只要市民自己不用恶劣的混流\n去败坏法律；用污泥弄脏清水，\n你就再也找不到可喝的水了。",
    ["这座战神山", "叫做战神山"], NUMS))

# ---- Seven Against Thebes, opening ----
SEV = "Επτά επί Θήβας"
sources["seven-thebes"] = SEV
lines.append(Q("seven-1", "seven-thebes", "gr-thebes", "Lines 1–9", "第 1–9 行", SEV,
    verse(SEV, "Κάδμου πολῖται", "Καδμείων πόλει."), ["Κάδμου πολῖται", "Καδμείων πόλει"],
    "Citizens of Cadmus, he must speak what the moment needs\nwho guards the city's affairs at the stern,\nturning the "
    "tiller, not letting his eyes close in sleep.\nFor if we fare well, the cause is a god's;\nbut if, which may it not "
    "happen, disaster strikes,\nEteocles alone would be the name, many times over, through the city,\nchanted by the "
    "citizens in loud preludes\nand laments; from which may Zeus the Defender,\ntrue to his name, defend the city of the "
    "Cadmeans.",
    ["Citizens of Cadmus", "the city of the Cadmeans"],
    "卡德摩斯的公民们，谁在城邦的船尾\n守护着国事、掌着舵，\n不让眼睛合上入睡，谁就应当说合时宜的话。\n如果我们一切顺利，那是神的功劳；\n"
    "可要是——但愿不会——遭了灾祸，\n全城上下，人们就只会一遍遍喊着埃特奥克勒斯一个人的名字，\n用嘈杂的序曲\n和哀号来唱他；"
    "愿守护者宙斯\n不负其名，保护卡德摩斯人的城邦免遭此祸。",
    ["卡德摩斯的公民们", "卡德摩斯人的城邦"], NUMS))

# ---- Oedipus Rex, opening ----
OT = "Οιδίπους Τύραννος"
sources["oedipus-rex"] = OT
lines.append(Q("oedipus-1", "oedipus-rex", "gr-thebes", "Lines 1–8", "第 1–8 行", OT,
    verse(OT, "ὦ τέκνα, Κάδμου", "Οἰδίπους καλούμενος."), ["Κάδμου τοῦ πάλαι", "πόλις"],
    "My children, newest brood of ancient Cadmus,\nwhy do you sit here before me like this,\ncrowned with the "
    "suppliant's branches?\nThe city is full of incense at once,\nand full of hymns of healing and of groans;\nand I, "
    "thinking it not right to hear of this from messengers,\nfrom others, my children, have come here myself,\nI, Oedipus, "
    "whom all men call renowned.",
    ["ancient Cadmus", "The city"],
    "孩子们，古老的卡德摩斯的新一代，\n你们为什么这样坐在我面前，\n手持缠着羊毛的求援树枝？\n全城一时间弥漫着香烟，\n"
    "又响彻着求医的颂歌和呻吟；\n孩子们，我认为不该从别人、从信使那里听说这些，\n所以亲自来了，\n我，人人都称为声名远扬的俄狄浦斯。",
    ["古老的卡德摩斯", "全城"], NUMS))

# ---- Antigone, parodos ----
ANT = "Αντιγόνη"
sources["antigone"] = ANT
lines.append(Q("antigone-1", "antigone", "gr-thebes", "Parodos, lines 100–109", "进场歌第 100–109 行", ANT,
    verse(ANT, "ἀκτὶς ἀελίου", "ὀξυτέρῳ κινήσασα χαλινῷ·"), ["ἑπταπύλῳ", "Θήβᾳ"],
    "Beam of the sun, fairest light that ever shone\non seven-gated Thebes of all before,\nyou have shone at last, eye of "
    "golden day,\ncoming over the streams of Dirce,\nyou who drove headlong in flight, with a sharper bridle,\nthe man of "
    "the white shield who came from Argos in full armour.",
    ["seven-gated Thebes"],
    "太阳的光芒，照耀七门的底比斯的\n最美的光，胜过从前的一切，\n金色白昼的眼睛啊，你终于照临了，\n越过狄尔刻的溪流而来，\n"
    "你用更锐利的嚼铁驱赶那个\n从阿尔戈斯全副武装而来的白盾之人，叫他仓皇奔逃。",
    ["七门的底比斯"], NUMS))

# ---- Oedipus at Colonus, first stasimon ----
OC = "Οιδίπους επί Κολωνώ"
sources["oedipus-colonus"] = OC
lines.append(Q("colonus-1", "oedipus-colonus", "gr-colonus", "First stasimon, lines 668–680", "第一合唱歌第 668–680 行", OC,
    verse(OC, "εὐίππου, ξένε", "ἀμφιπολῶν τιθήναις."), ["τὸν ἀργῆτα Κολωνόν"],
    "Stranger, you have come to the finest dwelling on earth\nin this land of fine horses,\nto shining Colonus, where\nthe "
    "clear-voiced nightingale\nmost often sings her lament\nin the green glades,\nkeeping to the wine-dark ivy\nand the "
    "god's untrodden\nfoliage, rich in fruit, sunless\nand sheltered from the wind\nof every storm; where the "
    "reveller\nDionysus ever walks,\nattending the nymphs who nursed him.",
    ["shining Colonus"],
    "客人哪，你来到了这片良马之乡\n大地上最好的住处，\n来到了白亮的科罗诺斯，在这里\n声音清亮的夜莺\n最常在绿色的林谷里\n低声悲啼，\n"
    "栖息在酒色的常春藤间，\n栖息在神的那片不可践踏的\n果实累累的树丛里，那里不见阳光，\n任何风暴的风\n也吹不进去；在这里，狂欢的\n"
    "狄俄尼索斯永远漫步，\n陪伴着哺育他的女神们。",
    ["白亮的科罗诺斯"], NUMS))

# ---- Medea, opening ----
MED = "Μήδεια"
sources["medea"] = MED
lines.append(Q("medea-1", "medea", "gr-corinth", "Lines 1–15", "第 1–15 行", MED,
    verse(MED, "Εἴθ’ ὤφελ’", "μὴ διχοστατῇ."), ["τήνδε γῆν Κορινθίαν"],
    "If only the hull of the Argo had never flown\nthrough the dark Clashing Rocks to the land of the Colchians,\nnor the "
    "pine had ever fallen, cut in the glens of Pelion,\nnor put oars into the hands\nof the best of men, who went to "
    "fetch the all-golden fleece\nfor Pelias! For then my mistress\nMedea would not have sailed to the towers of the land "
    "of Iolcus,\nher heart struck with love for Jason;\nnor, having persuaded the daughters of Pelias to kill\ntheir "
    "father, would she be living in this land of Corinth\nwith her husband and children, pleasing\nthe citizens of the "
    "land she came to in her exile,\nand herself in all things at one with Jason;\nwhich is the greatest safety there "
    "is,\nwhen a wife does not stand apart from her husband.",
    ["this land of Corinth"],
    "但愿阿尔戈号的船身从没有飞越\n那暗蓝的撞岩，驶向科尔基斯人的土地，\n但愿那松树从没有在珀利翁山谷里\n被砍倒，也从没有给那些英雄好汉\n"
    "装上船桨，让他们去为珀利阿斯\n取那金羊毛！那样的话，我的女主人\n美狄亚就不会航行到伊俄尔科斯的城楼下，\n"
    "她的心也不会被对伊阿宋的爱情击中；\n她也不会劝说珀利阿斯的女儿们杀死父亲，\n如今住在这科林斯的土地上，\n和丈夫孩子在一起，讨得\n"
    "她流亡来到的这片土地上的市民的欢心，\n自己也事事顺着伊阿宋；\n这是最大的保障，\n当妻子不与丈夫离心的时候。",
    ["这科林斯的土地"], NUMS))

# ---- The Bacchae, opening ----
BAC = "Βάκχαι"
sources["bacchae"] = BAC
lines.append(Q("bacchae-1", "bacchae", "gr-thebes", "Lines 1–5", "第 1–5 行", BAC,
    verse(BAC, "ἥκω Διὸς παῖς", "Ἰσμηνοῦ θ᾽ ὕδωρ.", numbered=False), ["τήνδε Θηβαίων χθόνα"],
    "I have come, the son of Zeus, to this land of the Thebans,\nDionysus, whom once the daughter of Cadmus bore,\nSemele, "
    "delivered by the lightning-bearing fire;\nand having changed my form from god to mortal\nI am here by the streams of "
    "Dirce and the water of Ismenus.",
    ["this land of the Thebans"],
    "我来了，宙斯的儿子，来到这底比斯人的土地，\n我是狄俄尼索斯，卡德摩斯的女儿塞墨勒\n当年在闪电的火焰中生下了我；\n"
    "我把神的模样换成凡人的形貌，\n来到狄尔刻的溪流和伊斯墨诺斯河边。",
    ["这底比斯人的土地"]))

# ---- Iphigenia in Aulis, prologue ----
IA = "Ιφιγένεια εν Αυλίδι"
sources["iphigenia-aulis"] = IA
lines.append(Q("iphigenia-1", "iphigenia-aulis", "gr-aulis", "Prologue, lines 87–93", "开场第 87–93 行", IA,
    verse(IA, "ἠθροισμένου δὲ καὶ", "οὐκ εἶναι τάδε."), ["κατ᾽ Αὐλίδα", "Ἀρτέμιδι θῦσαι τῇ τόδ᾽ οἰκούσῃ πέδον"],
    "When the army had gathered and assembled,\nwe sat at Aulis, unable to sail.\nCalchas the prophet, as we were at a "
    "loss,\ndeclared that Iphigenia, whom I fathered,\nmust be sacrificed to Artemis, who dwells on this ground,\nand "
    "that we would have our voyage and the overthrow of the Phrygians\nif we sacrificed her, and if we did not, none of "
    "this.",
    ["Aulis", "Artemis, who dwells on this ground"],
    "大军集结完毕，\n我们却在奥利斯困住了，无法起航。\n我们走投无路时，先知卡尔卡斯\n宣布说，必须把我生的伊菲革涅亚\n"
    "献祭给住在这片土地上的阿耳忒弥斯，\n献祭了，就能起航，就能摧毁弗里基亚人；\n不献祭，这一切就都不会有。",
    ["奥利斯", "住在这片土地上的阿耳忒弥斯"], NUMS))

# ---- Lysistrata ----
LYS = "Λυσιστράτη"
sources["lysistrata"] = LYS
lines.append(Q("lysistrata-1", "lysistrata", "gr-acropolis", "Lines 175–179", "第 175–179 行", LYS,
    verse(LYS, "ἀλλ᾽ ἔστι καὶ τοῦτ᾽", "καταλαβεῖν τὴν ἀκρόπολιν."), ["τὴν ἀκρόπολιν"],
    "But that too has been well prepared:\nwe'll seize the Acropolis today.\nThe oldest women have been given the job of "
    "doing it:\nwhile we are coming to terms here,\nthey are to seize the Acropolis, pretending to sacrifice.",
    ["the Acropolis"],
    "这一点也早已安排好了：\n我们今天就占领卫城。\n最年长的妇女们已经接到命令去办这件事：\n趁我们在这里商量的时候，\n"
    "她们假装去献祭，把卫城占领下来。",
    ["卫城"], NUMS))

# ---- Herodotus, Book 7 ----
HDT = "Ιστορίαι (Ηροδότου)/Πολύμνια"
sources["histories"] = HDT
lines.append(Q("histories-1", "histories", "gr-thermopylae", "Book 7, 225–226", "第七卷第 225–226 节", HDT,
    prose(HDT, "ὁ δὲ κολωνὸς ἐστὶ ἐν τῇ ἐσόδῳ", "ἐπὶ Λεωνίδῃ.") + GAP
    + prose(HDT, "Λακεδαιμονίων δὲ καὶ Θεσπιέων τοιούτων", "καὶ οὐκ ἐν ἡλίῳ.", markers=("[226.2]\xa0",)),
    ["ὁ δὲ κολωνὸς ἐστὶ ἐν τῇ ἐσόδῳ"],
    "The hillock is at the entrance of the pass, where the stone lion now stands in honour of Leonidas.\n…\nThough the "
    "Lacedaemonians and Thespians proved themselves such men, the bravest of all, it is said, was the Spartan Dieneces. "
    "They say he spoke this word before they closed with the Medes, when he learned from one of the Trachinians that "
    "when the barbarians let fly their arrows they hid the sun by the multitude of their shafts, so great was their "
    "number. He was not dismayed by this, but, making light of the multitude of the Medes, said that their Trachinian "
    "friend brought them nothing but good news, for if the Medes hid the sun they would fight them in the shade and not "
    "in the sun.",
    ["The hillock is at the entrance of the pass"],
    "那座小山丘就在关口的入口处，如今那里立着一尊为列奥尼达而立的石狮子。\n…\n拉刻代蒙人和忒斯皮埃人虽然都表现得如此英勇，"
    "据说其中最勇敢的是斯巴达人狄耶涅凯斯。据说在同米底人交锋之前，他从一个特拉基斯人那里听说，蛮族人一放箭，箭多得能把太阳遮住，"
    "他们的人数就是这么多。他并没有被吓住，反而毫不把米底人的人多放在眼里，说这位特拉基斯朋友给他们带来的全是好消息："
    "既然米底人能遮住太阳，那他们就可以在阴凉里而不是在太阳底下作战了。",
    ["那座小山丘就在关口的入口处"], " (the section marker [226.2] left out)"))

# ---- Thucydides, Book 2 ----
THU = "Ιστορία του Πελοποννησιακού Πολέμου/Β"
sources["thucydides"] = THU
lines.append(Q("thucydides-1", "thucydides", "gr-kerameikos", "Book 2, 34", "第二卷第 34 节", THU,
    prose(THU, "τιθέασιν οὖν ἐς τὸ δημόσιον σῆμα", "τὸν τάφον ἐποίησαν.") + GAP
    + prose(THU, "ἐπὶ δ’ οὖν τοῖς πρώτοις τοῖσδε", "ἔλεγε τοιάδε."), ["τὸ δημόσιον σῆμα"],
    "So they lay them in the public burial ground, which is in the most beautiful suburb of the city, and there they "
    "always bury those who fall in war, except those at Marathon; for them, judging their valour outstanding, they made "
    "the tomb on the spot.\n…\nOver these first dead, then, Pericles son of Xanthippus was chosen to speak. And when the "
    "moment came, he went forward from the tomb onto a high platform that had been built so that he could be heard by as "
    "much of the crowd as possible, and spoke as follows.",
    ["the public burial ground"],
    "于是他们把遗骨安葬在公墓里，公墓位于城郊最美的地方；战死的人一向都葬在这里，只有马拉松的阵亡者例外：人们认为那些人的英勇格外出众，"
    "就在当地为他们修了坟墓。\n…\n为这第一批阵亡者致辞的，被选中的是克珊西波斯之子伯里克利。时候一到，他从墓地走上一座高台——"
    "高台是特意搭起来的，好让尽可能多的人听见——发表了如下的演说。",
    ["公墓"]))

# ---- Plato, Apology ----
APO = "Απολογία Σωκράτους (Πλάτων)"
sources["socrates"] = APO
lines.append(Q("socrates-1", "socrates", "gr-agora", "Apology 17c–d", "《申辩篇》17c–d", APO,
    prose(APO, "καὶ μέντοι καὶ πάνυ, ὦ ἄνδρες Ἀθηναῖοι", "ἔτη γεγονὼς ἑβδομήκοντα·", markers=(" d\xa0 ",)),
    ["ἐν ἀγορᾷ ἐπὶ τῶν τραπεζῶν"],
    "And indeed, men of Athens, I very much ask and beg this of you: if you hear me making my defence with the same "
    "words I am used to speaking in the agora, at the bankers' tables, where many of you have heard me, and elsewhere, "
    "do not be surprised or make a disturbance on that account. For this is how it is: now for the first time I have "
    "come up before a court, at the age of seventy.",
    ["in the agora, at the bankers' tables"],
    "而且，雅典人啊，我非常恳切地请求你们这一点：如果你们听见我为自己辩护时，用的还是我平常在市集上、在钱庄的桌子旁——"
    "你们许多人都在那里听过我说话——以及在别处惯用的那些话，请不要为此感到惊讶，也不要喧哗。因为情形是这样的："
    "我活到七十岁，这是头一回上法庭。",
    ["在市集上、在钱庄的桌子旁"], " (the Stephanus letter 'd' left out)"))

# ---- Plato, Republic, opening ----
REP = "Πολιτεία/Α"
sources["republic"] = REP
lines.append(Q("republic-1", "republic", "gr-piraeus", "Book 1, 327a–b", "第一卷 327a–b", REP,
    prose(REP, "κατέβην χθὲς εἰς Πειραιᾶ", "πρὸς τὸ ἄστυ.", markers=("[327b] ",)), ["εἰς Πειραιᾶ"],
    "I went down yesterday to the Piraeus with Glaucon, son of Ariston, to pray to the goddess and also because I wanted "
    "to see how they would hold the festival, since they were holding it for the first time. I thought the procession "
    "of the local people was fine, but the one the Thracians sent seemed no less fitting. When we had prayed and "
    "watched, we set off back to the city.",
    ["the Piraeus"],
    "昨天我和阿里斯通的儿子格劳孔一起下到比雷埃夫斯港，去向女神祈祷，同时也想看看他们怎样举办这个节日，因为这是他们第一次举办。"
    "我觉得本地人的游行队伍很好看，色雷斯人派出的队伍也同样出色。我们祈祷完、看完之后，就动身回城里去。",
    ["比雷埃夫斯港"], " (the Stephanus marker [327b] left out)"))

# ---- Plutarch, Life of Demosthenes ----
PLU = "Βίοι Παράλληλοι/Δημοσθένης"
sources["plutarch"] = PLU
lines.append(Q("plutarch-1", "plutarch", "gr-chaeronea", "Life of Demosthenes, chapter 2", "《德摩斯梯尼传》第二章", PLU,
    prose(PLU, "ἡμεῖς δὲ μικρὰν μὲν οἰκοῦντες πόλιν", "ἀλλ' ἀληθὲς ἐπάσχομεν."), ["μικρὰν μὲν οἰκοῦντες πόλιν"],
    "But as for me, I live in a small city, and I stay in it gladly so that it may not become smaller; and in Rome and "
    "my stays in Italy I had no leisure to practise the Roman language because of public business and the people who "
    "came to me for philosophy, so that it was late, and well on in years, that I began to read Roman writings; and "
    "something remarkable, but true, happened to me.",
    ["I live in a small city"],
    "至于我，我住在一座小城里，并且乐意住在那里，免得它变得更小；在罗马和意大利逗留期间，我忙于公务，又要应付那些来向我求教哲学的人，"
    "没有闲暇练习罗马人的语言，所以直到很晚、年纪已大，我才开始读罗马人的著作；于是我有了一种奇妙但真实的体验。",
    ["我住在一座小城里"]))

# ---- Erotokritos, the poet's signature ----
ERO = "Ερωτόκριτος/Ε"
sources["erotokritos"] = ERO
lines.append(Q("eroto-1", "erotokritos", "gr-sitia", "Part V, lines 1535–1540", "第五部第 1535–1540 行", ERO,
    verse(ERO, "ΒΙΤΣΕΝΤΖΟΣ", "όπου ο Θεός ορίσει."), ["Στη Στείαν εγεννήθηκε, στη Στείαν ενεθράφη"],
    "Vitsentzos is the poet, and of the family Kornaros,\nmay he be found without sin when Charon takes him.\nIn Sitia he "
    "was born, in Sitia he was raised,\nthere he made and laboured over what he writes to you.\nIn Kastro he married, as "
    "nature counsels;\nhis end will come wherever God decrees.",
    ["In Sitia he was born, in Sitia he was raised"],
    "诗人名叫维岑佐斯，家族姓科尔纳罗斯，\n愿卡戎来带走他时，他清白无罪。\n他生在锡蒂亚，长在锡蒂亚，\n在那里写成、辛苦经营了这些献给你们的诗句。\n"
    "他在卡斯特罗成了家，正如天性的指引；\n他的结局将在上帝安排的地方。",
    ["他生在锡蒂亚，长在锡蒂亚"], " (the edition's line number and couplet indent left out)"))

# ---- The Free Besieged, second draft ----
FB = "Οι Ελεύθεροι Πολιορκημένοι/σχεδίασμα Β"
sources["free-besieged"] = FB
lines.append(Q("besieged-1", "free-besieged", "gr-missolonghi", "Second draft, fragments 1–2", "第二稿，片段 1–2", FB,
    verse(FB, "Άκρα του τάφου σιωπή", "κι’ ο Αγαρηνός το ξέρει.»", numbered=False) + GAP
    + prose(FB, "Το Μεσολόγγι έπεσε την άνοιξη·", "να δειλιάση τους πολιορκημένους·"), ["Το Μεσολόγγι"],
    "The silence of the grave reigns over the plain.\nA bird sings, takes a seed, and the mother envies it.\nHunger has "
    "blackened their eyes; in the eyes the mother swears;\nthe good Souliot stands aside and weeps:\n'Wretched dark gun, "
    "why do I hold you in my hand?\nYou have become heavy to me, and the Hagarene knows it.'\n…\nMissolonghi fell in "
    "spring; the poet shows Nature, at the moment when she is loveliest, as a power which, with everything else, "
    "material and moral, against them, tries to break the courage of the besieged;",
    ["Missolonghi"],
    "坟墓般的死寂笼罩着原野。\n鸟儿啼叫着啄起一粒种子，母亲都羡慕它。\n饥饿使人的眼睛发黑；母亲凭眼睛起誓；\n善良的苏利人站在一旁哭泣：\n"
    "“可怜的黑沉沉的枪啊，我把你握在手里做什么？\n你在我手里变得这么沉重，阿加尔的子孙都知道。”\n…\n"
    "迈索隆吉翁是在春天陷落的；诗人把大自然表现为一种力量：在她最美的时刻，当一切物质的和精神的东西都与被围者作对时，"
    "她也设法动摇他们的勇气；",
    ["迈索隆吉翁"]))

# ---- Cavafy, 'Ithaka' ----
ITH = "Ιθάκη"
sources["cavafy"] = ITH
lines.append(Q("cavafy-1", "cavafy", "gr-ithaca", "'Ithaka'", "《伊萨卡》", ITH,
    verse(ITH, "Σα βγεις στον πηγαιμό", "γεμάτος γνώσεις.", numbered=False) + GAP
    + verse(ITH, "Πάντα στον νου σου νάχεις", "οι Ιθάκες τι σημαίνουν.", numbered=False), ["Ιθάκη"],
    "As you set out on the journey to Ithaka,\npray that the road is long,\nfull of adventures, full of knowledge.\n…\n"
    "Always keep Ithaka in your mind.\nTo arrive there is your destination.\nBut do not hurry the journey at "
    "all.\nBetter that it last many years;\nand that you anchor at the island old at last,\nrich with all you have gained "
    "on the road,\nnot expecting Ithaka to give you riches.\nIthaka gave you the lovely journey.\nWithout her you would "
    "not have set out on the road.\nShe has nothing more to give you.\nAnd if you find her poor, Ithaka has not deceived "
    "you.\nWise as you have become, with so much experience,\nyou will have understood by now what Ithakas mean.",
    ["Ithaka"],
    "当你启程前往伊萨卡，\n但愿你的道路漫长，\n充满冒险，充满见识。\n…\n心里要时时想着伊萨卡。\n抵达那里，是你的目的地。\n"
    "可是千万不要催促旅程。\n最好让它延续许多年；\n等你老了，才在那岛上泊岸，\n带着一路上得来的一切财富，\n不必指望伊萨卡给你什么财富。\n"
    "伊萨卡给了你这趟美好的旅程。\n没有她，你就不会上路。\n她再没有什么可以给你了。\n如果你发现她贫瘠，伊萨卡并没有欺骗你。\n"
    "你已经变得这样智慧，有了这么多阅历，\n此刻你一定已经懂得，一个个伊萨卡意味着什么。",
    ["伊萨卡"]))

# ---- Karyotakis, 'Preveza' ----
PRE = "Πρέβεζα"
sources["karyotakis"] = PRE
lines.append(Q("karyotakis-1", "karyotakis", "gr-preveza", "'Preveza', stanzas 1 and 4", "《普雷韦扎》第一、四节", PRE,
    verse(PRE, "Θάνατος είναι οι κάργες", "καθαρίζουνε κρεμμύδια.", numbered=False) + GAP
    + verse(PRE, "Βάσις, Φρουρά", "δραχμαί τριάντα.", numbered=False), ["Πρεβέζης"],
    "Death is the jackdaws beating themselves\nagainst the black walls and the roof tiles,\ndeath the women who are "
    "loved\nas if they were peeling onions.\n…\nBase, Garrison, Gendarmerie Company of Preveza.\nOn Sunday we shall hear "
    "the band.\nI took out a bank book,\nfirst deposit thirty drachmas.",
    ["Preveza"],
    "死亡是那些寒鸦，撞在\n黑色的墙壁和屋瓦上，\n死亡是那些女人，她们被爱着，\n就像在剥洋葱。\n…\n普雷韦扎基地、卫戍部队、宪兵连。\n"
    "星期天我们将去听乐队演奏。\n我办了一本银行存折，\n第一笔存款三十德拉克马。",
    ["普雷韦扎"]))

# ---------- write ----------
replaced = {"odyssey": ["odyssey-s1"], "oresteia": ["oresteia-s1"], "seven-thebes": ["seven-s1"],
            "oedipus-rex": ["oedipus-s1"], "antigone": ["antigone-s1"], "oedipus-colonus": ["colonus-s1"],
            "medea": ["medea-s1"], "bacchae": ["bacchae-s1"], "iphigenia-aulis": ["iphigenia-s1"],
            "lysistrata": ["lysistrata-s1"], "histories": ["histories-s1"], "thucydides": ["thucydides-s1"],
            "socrates": ["socrates-s1"], "republic": ["republic-s1"], "plutarch": ["plutarch-s1"],
            "erotokritos": ["eroto-s1"], "free-besieged": ["besieged-s1"], "cavafy": ["cavafy-s1"],
            "karyotakis": ["karyotakis-s1"]}
assert set(replaced) == {l["book_id"] for l in lines} == set(sources)
lp = b.data("lines.js")
existing = set(re.findall(r'  \{ id: "([^"]+)"', open(lp, encoding="utf-8").read()))
assert not ({l["id"] for l in lines} & existing), "ids already in use"
drop_entries(lp, {i for v in replaced.values() for i in v})
b.append(lp, lines, "11-22 quotations from Greek Wikisource, replacing the placeholder scene notes (add_gr3.py)")
for bid, title in sources.items():
    set_source(b.data("books.js"), bid, ws.url("el", title))
print(len(lines), "quotations for", len(replaced), "books;", sum(map(len, replaced.values())), "scene notes replaced")
