"""11-22: Japan, the classics Aozora Bunko has no original of, quoted from Japanese Wikisource
(tools/content/wikisource.py: the rendered page's own text; ruby readings and page numbers dropped). English and Chinese
are our own translations (translation: "own"), drafts for review. Each quotation replaces the book's placeholder scene
note at the same place.
Where an edition prints its own glosses in the running text (〔…〕 in the Yuhodo Sarashina, （＊ママ） in the Kokumin
Bunko Bamboo Cutter) or numbers its poems (the Man'yoshu), the cut drops them and says so in `checked`.
Still scene notes only: the Tale of the Heike (Wikisource has only a list of editions), Sonezaki and Chushingura (not on
Wikisource), and The Setting Sun (names no place on the map; see add_jp3.py).
Usage: python3 -I add_jp4.py <app_dir> <wikisource_dir>   (python3 -I ../wikisource.py <dir> ja <title> … downloads)"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws
from datafile import drop_entries, set_source

APP, WS = sys.argv[1], sys.argv[2]
DATE = "2026-11-22"
b.init(APP, None, "jp", DATE)
GAP = b.GAP
cut = lambda t, a, z, **k: ws.cut(WS, t, a, z, **k)
blk = lambda t, a, z, **k: ws.block(WS, t, a, z, **k)

def Q(id, book, place, loc, loc_zh, title, orig, hl_orig, en, hl_en, zh, hl_zh, note=""):
    for h in hl_orig:
        assert h in orig, (id, h)
    for h in hl_en:
        assert h in en, (id, h)
    for h in hl_zh:
        assert h in zh, (id, h)
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh,
                text_orig=orig, highlight_orig=hl_orig, text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh,
                translation="own", status="draft", checked=f"Japanese Wikisource, {title}{note}, {DATE}")

lines, sources = [], {}

# ---- Man'yoshu, book 1 (Kamochi Masazumi's reading) ----
MY = "万葉集 (鹿持雅澄訓訂)/巻第一"
sources["manyoshu"] = MY
lines.append(Q("manyo-1", "manyoshu", "jp-amanokagu", "Book 1, poem 13", "卷一第 13 首", MY,
    blk(MY, "0013　香具山は", "争ふらしき", number="0013　"), ["香具山"],
    "Mount Kagu, finding Unebi fair,\nquarrelled with Miminashi over her.\nSince the age of the gods, it seems, it has been "
    "so;\nand since it was so in ancient days,\nwe in this mortal world too,\nit seems, must quarrel over a wife.",
    ["Mount Kagu"],
    "香具山看中了亩傍山，\n同耳成山相争。\n自神代以来，似乎就是这样；\n古时既然如此，\n如今世上的人\n也要为妻子相争吧。",
    ["香具山"], " (the editor's poem number left out)"))
lines.append(Q("manyo-2", "manyoshu", "jp-amanokagu", "Book 1, poem 28", "卷一第 28 首", MY,
    cut(MY, "春過ぎて夏来るらし", "天の香具山"), ["天の香具山"],
    "Spring has passed, and summer, it seems, has come:\nwhite robes are spread to dry\non heavenly Mount Kagu.",
    ["heavenly Mount Kagu"],
    "春天过去，夏天似乎来了：\n天之香具山上，\n晾着雪白的衣裳。",
    ["天之香具山"]))

# ---- The Tale of the Bamboo Cutter, ending (Kokumin Bunko) ----
TK = "竹取物語 (國民文庫)"
sources["taketori"] = TK
lines.append(Q("taketori-1", "taketori", "jp-fuji-summit", "Ending", "结尾", TK,
    cut(TK, "勅使には調岩笠", "いひ傳へたる。", drop=("（＊ママ）",)), ["ふしの山"],
    "As his envoy he summoned a man named Tsuki no Iwakasa, and ordered him to take them to the summit of the mountain in "
    "the land of Suruga. He had him taught what was to be done on the peak: to set the letter and the jar of the elixir "
    "of immortality side by side, put fire to them and burn them. The envoy took the order and climbed the mountain with "
    "a great many soldiers, and from that time, it is said, the mountain has been called Fuji, rich in soldiers. Its "
    "smoke, the story goes, still rises into the clouds.",
    ["Fuji"],
    "他召来一个名叫调岩笠的人做敕使，命他把这些带到骏河国那座山的山顶上去，又叫人教他在峰顶该怎样做：把书信和不死药的药壶并排放好，点火烧掉。"
    "敕使领了旨，带着许多兵士登上山去；从那以后，这座山就叫做富士山。据说那烟至今还升入云中。",
    ["富士山"], " (the editor's sic mark left out)"))

# ---- The Tales of Ise, episode 9 (Gunsho ruiju) ----
IS = "伊勢物語"
sources["tales-of-ise"] = IS
lines.append(Q("ise-1", "tales-of-ise", "jp-yatsuhashi", "Episode 9", "第九段", "伊勢物語 (群書類從)",
    blk(IS, "もとよりともする人。", "ほとびにけり。"), ["やつはし", "八橋"],
    "One or two who had always been his companions went along with him. With no one who knew the way, they went on, "
    "losing it, and came to a place called Yatsuhashi in the land of Mikawa. It is called Yatsuhashi, Eight Bridges, "
    "because the water there branches out like a spider's legs and eight planks are laid across it. They got down in "
    "the shade of the trees by that marsh and ate their dried rice. In the marsh the irises were blooming beautifully. "
    "Seeing them, he longed for the capital. So one of them said, 'Make a poem on the feelings of the journey, with the "
    "five syllables ka-ki-tsu-ba-ta at the heads of its lines,' and he made this:\n"
    "I have a wife, familiar as the robe from Kara I have worn so long,\nand so I think how far I have come on this "
    "journey.\nWhen he had said it, everyone wept onto their dried rice until it swelled.",
    ["Yatsuhashi"],
    "一向同行的朋友有一两个，便一起去了。没有认得路的人，一路走一路迷路，来到三河国一个叫八桥的地方。所以叫八桥，是因为那里的水像蜘蛛的脚一样分流开去，"
    "上面架了八座木桥。他们在那片沼泽边的树荫下下马坐着，吃干饭。沼泽里燕子花开得正好。看见了，他非常想念京城。于是有人说："
    "“把‘燕子花’（かきつばた）这五个音放在每句的开头，咏一首旅途的心情吧。”他便咏道：\n"
    "唐衣穿久了贴身，妻子也这样与我亲近；\n远远地来到这里，不禁想起这趟旅途。\n他一吟完，大家的眼泪都落在干饭上，把饭泡软了。",
    ["八桥"]))

# ---- The Pillow Book, the snow of Xianglu Peak (Kokubun taikan) ----
MK = "枕草紙 (國文大觀)"
sources["pillow-book"] = MK
lines.append(Q("pillow-1", "pillow-book", "jp-kyoto-gosho", "'The snow of Xianglu Peak'", "《香炉峰之雪》", MK,
    cut(MK, "雪いと高く降りたるを例ならず", "さるべきなめり」といふ。"), ["この宮"],
    "The snow had fallen very deep, and, which was unusual, the lattice shutters had been let down; we had made up a fire "
    "in the brazier and were gathered round it talking, when Her Majesty said, 'Shonagon, how is the snow on Xianglu "
    "Peak?' I had the shutters raised and rolled the blind up high, and she laughed. The others all knew the lines and "
    "had even put them into songs, but it had not occurred to them. 'Someone in this palace,' they said, 'ought to be "
    "just like that.'",
    ["this palace"],
    "雪下得很深，难得地放下了格子窗，在火盆里生了火，大家聚在一起说话。这时中宫说：“少纳言，香炉峰的雪怎么样了？”我叫人把格子窗打开，把帘子高高卷起，"
    "中宫便笑了。别的人也都知道这句诗，甚至还唱进歌里，却没有想到这一层。她们说：“这宫里的人，就该是这样吧。”",
    ["这宫里"]))

# ---- The Tale of Genji, 'The Drifting Boat' (Shibuya Eiichi's text) ----
GJ = "源氏物語/浮舟"
sources["tale-of-genji"] = GJ
lines.append(Q("genji-1", "tale-of-genji", "jp-uji-bridge", "'The Drifting Boat'", "《浮舟》", "源氏物語 (渋谷栄一校訂)/浮舟",
    cut(GJ, "山の方は霞隔てて", "多かるべきほどなり。") + GAP + blk(GJ, "「宇治橋の長き契りは", "なほ頼めとや」"), ["宇治橋"],
    "Toward the hills the haze hung between, and even a magpie standing on the cold sandspit looked lovely, as things do "
    "in such a place; Uji Bridge could be seen stretching far into the distance, and boats loaded with brushwood passed "
    "one another here and there. It was a place that gathered together nothing but sights unlike any one grew used to "
    "elsewhere, so that each time he looked at it the past came back as if it were now; even with a woman who had no such "
    "ties to it, such a meeting would have been full of rare feeling." + GAP +
    "'Long as Uji Bridge,\nour pledge will never rot away:\ndo not let your heart race in fear that it will fall.\n"
    "You will see soon enough,'\nhe said.\n'Uji Bridge, so full of gaps,\nalways so unsafe in this world,\nand you still "
    "ask me to trust it will not rot?'",
    ["Uji Bridge"],
    "山那边隔着一层霞，寒冷的沙洲上立着的喜鹊，因了这个地方，也显得格外有趣；宇治桥远远地望得见，运柴的船这里那里往来交错——这里聚集的尽是别处看不惯的景致，"
    "所以他每次看见，往事都像眼前的事一样；即使对面是与这里毫无因缘的人，这样难得的相会也该有许多感慨。" + GAP +
    "“宇治桥长，我们的盟约，\n永远不会朽坏：\n莫要担心它断，心慌意乱。\n不久你就会明白。”\n他这样说。\n"
    "“宇治桥上处处断缺，\n世上最是危险，\n你还要我相信它不会朽坏吗？”",
    ["宇治桥"]))

# ---- As I Crossed a Bridge of Dreams, opening (Yuhodo Bunko) ----
SR = "更級日記 (有朋堂文庫)"
sources["sarashina-diary"] = SR
lines.append(Q("sarashina-1", "sarashina-diary", "jp-kazusa-kokubunji", "Opening", "开篇", SR,
    cut(SR, "東路の道のはてよりも、なほ", "覺え語らむ。", drop=("〔源氏物語〕",)), ["東路の道のはて"],
    "Brought up somewhere even further off than the far end of the road to the east, how countrified I must have been! "
    "Yet somehow, I cannot think how it began, I came to hear that there were such things in the world as tales, and "
    "longed to read them; in idle daytimes and evenings my sister, my stepmother and the others would tell bits of this "
    "tale and that, and of how the Shining Genji lived, and hearing them only made me long for more. But how could they "
    "tell them from memory just as I wished?",
    ["the far end of the road to the east"],
    "我生长在比东路的尽头还要更远的地方，那时该是多么土气啊。可不知怎么起了念头，听说世上有“物语”这种东西，就一心想看看。闲来无事的白天和夜晚，"
    "姐姐、继母她们讲这个物语、那个物语，讲光源氏怎样怎样，零零碎碎的，我听了更想看了；可她们凭记忆，又怎能照我的心意讲给我听呢。",
    ["东路的尽头"], " (the editor's gloss 〔源氏物語〕 left out)"))

# ---- Essays in Idleness, section 52 (Kokubun taikan) ----
TZ = "徒然草 (國文大觀)"
sources["tsurezuregusa"] = TZ
lines.append(Q("tsure-1", "tsurezuregusa", "jp-ninnaji", "Section 52", "第五十二段", TZ,
    cut(TZ, "仁和寺にある法師、年よるまで", "あらまほしきことなり。"), ["仁和寺"],
    "A monk of Ninna-ji, ashamed that he had grown old without ever worshipping at Iwashimizu, made up his mind one day "
    "and went there alone, on foot. He worshipped at Gokuraku-ji, the Kora shrine and the rest, decided that was all, and "
    "came home. Then, meeting one of his fellows, he said: 'I have done at last what I had meant to do for years. It was "
    "even holier than I had heard. Though I did wonder what was up there, since everyone who went was climbing the hill; "
    "I wanted to see, but I thought, it is the god I came to worship, and did not go up the hill.' Even in small things, "
    "a guide is to be wished for.",
    ["Ninna-ji"],
    "仁和寺有个法师，到老还没拜过石清水，心里觉得惭愧，有一天下了决心，独自一人步行前去。拜了极乐寺、高良社这些地方，以为就是这些了，便回来了。"
    "后来他见了同伴，说：“多年的心愿总算了了。比听说的还要庄严。只是去参拜的人个个都往山上爬，不知上面有什么，我很想看看，可又想，来拜神才是本意，"
    "就没上山去看。”哪怕是小事，也最好有个引路的人。",
    ["仁和寺"]))

# ---------- write ----------
replaced = {"manyoshu": "manyo-s1", "taketori": "taketori-s1", "tales-of-ise": "ise-s1", "pillow-book": "pillow-s1",
            "tale-of-genji": "genji-s1", "sarashina-diary": "sarashina-s1", "tsurezuregusa": "tsure-s1"}
assert set(replaced) == {l["book_id"] for l in lines} == set(sources)
lp = b.data("lines.js")
existing = set(re.findall(r'  \{ id: "([^"]+)"', open(lp, encoding="utf-8").read()))
assert not ({l["id"] for l in lines} & existing), "ids already in use"
drop_entries(lp, set(replaced.values()))
b.append(lp, lines, "11-22 quotations from Japanese Wikisource, replacing the placeholder scene notes (add_jp4.py)")
for bid, title in sources.items():
    set_source(b.data("books.js"), bid, ws.url("ja", title))
print(len(lines), "quotations;", len(replaced), "scene notes replaced")
