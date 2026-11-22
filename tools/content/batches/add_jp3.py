"""11-22: Japan, quotations for the public-domain books that had scene notes only. The originals are cut from Aozora Bunko
(tools/content/aozora.py: ruby, editor's note numbers and layout notes dropped, outside characters resolved; nothing
else changed). English and Chinese are our own translations (translation: "own"), drafts for review.
Each new quotation replaces the book's placeholder scene note at the same place. The Setting Sun keeps its scene note:
the novel never names Kanagi or Tsugaru. Eight classics wait for Japanese Wikisource (Aozora has no original text of
them): the Man'yoshu, the Bamboo Cutter, Ise, the Pillow Book, Genji, the Sarashina diary, the Heike, Tsurezuregusa,
Sonezaki and Chushingura.
Usage: python3 -I add_jp3.py <app_dir> <aozora_dir>   (python3 -I ../aozora.py <aozora_dir> <n> … downloads the texts)"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import aozora as az
from datafile import drop_entries, set_source

APP, AZ = sys.argv[1], sys.argv[2]
DATE = "2026-11-22"
b.init(APP, None, "jp", DATE)
GAP = b.GAP
cut = lambda n, a, z, after=None: az.cut(AZ, n, a, z, after)

def Q(id, book, place, loc, loc_zh, n, orig, hl_orig, en, hl_en, zh, hl_zh, removed=""):
    for h in hl_orig:
        assert h in orig, (id, h)
    for h in hl_en:
        assert h in en, (id, h)
    for h in hl_zh:
        assert h in zh, (id, h)
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh,
                text_orig=orig, highlight_orig=hl_orig, text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh,
                translation="own", status="draft", checked=f"Aozora Bunko #{n}{removed}, {DATE}")

NOTES = " (ruby and the editor's note numbers left out)"
lines, sources = [], {}

# ---- Kojiki (Takeda Yukichi's annotated reading, Aozora #51731) ----
sources["kojiki"] = 51731
lines.append(Q("kojiki-1", "kojiki", "jp-izumo-taisha", "Book 1, 'The Ceding of the Land'", "上卷《让国》", 51731,
    cut(51731, "ここに答へ白さく、「僕が子ども二神", "天の御舍を造りて") + "…", ["出雲の國の多藝志の小濱"],
    "Then he answered: 'As my two sons have said, so I too will not go against it. This Central Land of the Reed Plains "
    "I have already yielded at your command. Only let my dwelling be like the rich heavenly abode from which the august "
    "child of the heavenly gods will rule the heavenly succession, its pillars planted firm on the bedrock below and its "
    "roof-beams raised high to the Plain of High Heaven; then I will withdraw and wait in the eighty winding corners of "
    "the land. And if my hundred and eighty children serve with Yae-kotoshironushi going before them and behind, not one "
    "god will disobey.' So he said, and on the little beach of Tagishi in the land of Izumo a heavenly hall was built…",
    ["the little beach of Tagishi in the land of Izumo"],
    "于是大国主神答道：“我的两个儿子怎么说，我也不违背。这苇原中国，已经遵命献上了。只求我的住处，能像天神之子继承天位时所居的丰足天宫那样，"
    "宫柱稳稳扎在地底的磐石上，屋脊的木梁高高伸到高天原；这样，我便退到弯弯曲曲的八十个角落里侍候。我那一百八十个儿子，"
    "若由八重事代主神在前后带领着侍奉，就不会有违抗的神。”说完，便在出云国多艺志的小滨，造起了天上的宫殿……",
    ["出云国多艺志的小滨"], NOTES))

# ---- The Tosa Diary (Aozora #832) ----
sources["tosa-diary"] = 832
lines.append(Q("tosa-1", "tosa-diary", "jp-tosa-kokubunji", "Opening, the 21st day of the 12th month", "开篇，十二月二十一日", 832,
    cut(832, "男もすなる日記", "船に乘るべき所へわたる。"), ["住むたち"],
    "Diaries are things that men keep, I hear; I, a woman, will try my hand at one too. In a certain year (the fourth of "
    "Shohei), on the twenty-first day of the twelfth month, at the hour of the Dog, we set out. I note down a little of how "
    "it went. A certain person, his four or five years in the province over, the customary business all done and his "
    "release papers in hand, left the residence where he had lived and crossed to the place where he was to board the boat.",
    ["the residence where he had lived"],
    "听说日记这东西是男人写的，我这个女人也想写写看。某年（承平四年）十二月二十一日戌时，动身出发。把经过略略记在这里。"
    "有一个人，在这个国任满了四五年，照例的事务都办完了，拿到了解由状，从住了多年的官舍出来，到要上船的地方去。",
    ["住了多年的官舍"]))

# ---- Hojoki (Aozora #975) ----
sources["hojoki"] = 975
lines.append(Q("hojoki-1", "hojoki", "jp-shimogamo", "Opening", "开篇", 975,
    cut(975, "行く川のながれは", "またかくの如し。"), ["行く川"],
    "The flowing river never ceases, and yet its water is never the same water. The foam that floats on its still pools now "
    "vanishes, now forms again, and never stays for long. So it is with the people of this world and their dwellings.",
    ["The flowing river"],
    "流去的河水从不断绝，却已不是原来的水。浮在河湾里的泡沫，时而消散，时而凝聚，从不久留。世上的人和他们的住处，也是这样。",
    ["流去的河水"]))

# ---- The Narrow Road to the Deep North (Sugiura Shoichiro's text, Aozora #61619) ----
sources["oku-no-hosomichi"] = 61619
lines.append(Q("oku-1", "oku-no-hosomichi", "jp-takadachi", "Hiraizumi", "《平泉》", 61619,
    cut(61619, "三代の榮耀", "泪を落し侍りぬ。") + "\n" + cut(61619, "夏草や", "夢の跡"), ["高舘"],
    "The glory of three generations passed in a single sleep; the site of the great gate lies a league this side of here. "
    "Where Hidehira's palace stood are fields now, and only Mount Kinkei keeps its shape. First we climbed to Takadachi: "
    "below it runs the Kitakami, a great river flowing down from Nanbu. The Koromo river circles Izumi's castle and falls "
    "into the great river beneath Takadachi. The old stronghold of Yasuhira and his men lay beyond the Koromo barrier, "
    "guarding the way in from Nanbu, it seems, and holding off the northern tribes. And so the chosen loyal men shut "
    "themselves in this castle, and their glory became, in a moment, a stretch of grass. 'The state is broken, the "
    "mountains and rivers remain; the castle in spring is green with grass,' I recited, and sat on my hat and wept until "
    "the time had passed.\nThe summer grass: all that is left of warriors' dreams.",
    ["Takadachi"],
    "三代的荣华，一梦之间便成空；大门的遗迹在一里之外。秀衡的旧居已成田野，只有金鸡山还留着原样。先登上高馆，只见北上川是从南部流来的大河。"
    "衣川绕过和泉的城，在高馆下面汇入大河。泰衡等人的旧迹，隔着衣关，扼守南部的入口，看来是为了防御夷人。想当年，精选的忠臣据守这座城，"
    "一时的功名，化作了一片草丛。“国破山河在，城春草青青”，我铺下斗笠坐着，流泪直到时光推移。\n夏草啊，武士们的梦的遗迹。",
    ["高馆"], NOTES))

# ---- Tales of Moonlight and Rain, 'The Kibitsu Cauldron' (Uzuki Hiroshi's text, Aozora #60608) ----
sources["ugetsu-monogatari"] = 60608
lines.append(Q("ugetsu-1", "ugetsu-monogatari", "jp-kibitsu", "'The Kibitsu Cauldron'", "《吉备津之釜》", 60608,
    cut(60608, "猶幸を神に祈るとて", "声もなし。"), ["吉備津の御釜祓"],
    "To pray to the god for still more good fortune, they gathered the shrine maidens and priests and offered the sacred "
    "hot water. Whoever makes a vow at this shrine offers many purification gifts and the sacred hot water, and so divines "
    "good fortune or ill. When the maidens have finished the prayers and the water comes to the boil, for good fortune the "
    "cauldron roars like a lowing ox; for ill, the cauldron makes no sound. This is called the Cauldron Purification of "
    "Kibitsu. But for Kasada's house, as if the god would not hear the prayer, there was not even as much sound as autumn "
    "insects make chirping in the grass.",
    ["the Cauldron Purification of Kibitsu"],
    "为了再向神祈福，他们召来巫女和神官，献上御汤。凡是到这座神社许愿的人，都要供上许多祓物，献上御汤，占卜吉凶。巫女念完祝词，等到汤沸起来，"
    "若是吉兆，釜就发出像牛吼一样的声音；若是凶兆，釜便没有声音。这叫做吉备津的御釜祓。可是轮到香央家的事，神像是不肯听这祈愿，"
    "连秋虫在草丛里鸣叫那么一点声音都没有。",
    ["吉备津的御釜祓"], NOTES))

# ---- Child's Play (Aozora #56041) ----
sources["takekurabe"] = 56041
lines.append(Q("takekurabe-1", "takekurabe", "jp-ichiyo-museum", "Chapter 1, opening", "第一章开篇", 56041,
    cut(56041, "廻れば大門", "住みたる人の申き") + "…", ["大音寺前"],
    "Go round, and the long Mikaeri willow at the great gate is still far off, yet the revelry of the three-storey houses, "
    "their lamps reflected in the black-tooth ditch, seems close enough to touch, and from the rickshaws coming and going "
    "day and night you can guess at a prosperity beyond counting. Daionji-mae, they call it, a name that smells of the "
    "temple, but it is a lively quarter all the same, said someone who lived there…",
    ["Daionji-mae"],
    "绕过去，大门口的回首柳还远，可是映在黑齿沟里的灯火、三层楼上的喧闹，却近得仿佛伸手可及；从昼夜不停来来往往的车子，就能想见那数不清的繁华。"
    "“大音寺前”，名字带着佛气，住在这里的人却说，这其实是个热闹的地方……",
    ["大音寺前"]))

# ---- Kokoro (Aozora #773) ----
sources["kokoro"] = 773
lines.append(Q("kokoro-1", "kokoro", "jp-yuigahama", "Part 1, 'Sensei and I', Chapter 1", "上篇《先生与我》第一节", 773,
    cut(773, "私が先生と知り合いになったのは", "書生であった。") + GAP + cut(773, "私は毎日海へはいりに", "事もあった。"), ["鎌倉"],
    "It was at Kamakura that I came to know Sensei. I was still a young student then." + GAP +
    "Every day I went down to swim in the sea. When I had passed between the old, smoke-blackened thatched roofs and come "
    "down to the shore, the sand was alive with men and women here to escape the heat, so many that you wondered whether "
    "so many city people really lived in these parts. Some days the sea itself was as crowded with black heads as a "
    "public bath.",
    ["Kamakura"],
    "我和先生相识，是在镰仓。那时我还是个年轻的学生。" + GAP +
    "我每天都去海里游泳。穿过那些熏得发黑的旧茅草屋顶走到海边，只见沙滩上挤满了来避暑的男男女女，多得让人怀疑这一带竟住着这么多城里人。"
    "有时候，海里黑压压的人头挤成一片，像澡堂一样。",
    ["镰仓"]))

# ---- The Broken Commandment (Aozora #1502) ----
sources["broken-commandment"] = 1502
lines.append(Q("hakai-1", "broken-commandment", "jp-iiyama", "Chapter 1, section 1", "第一章第一节", 1502,
    cut(1502, "蓮華寺では下宿を兼ねた", "白く塗つた建築物であつた。"), ["飯山町", "飯山の町"],
    "The Rengeji temple took in lodgers. The room Segawa Ushimatsu had suddenly decided to move into, and had taken, was "
    "at the corner of the upper floor, next to the storehouse. The temple, one of the twenty-odd temples of the town of "
    "Iiyama in the Shimominochi district of Shinshu, was an old foundation of the Shin sect; leaning on the sill of that "
    "upstairs window you could see, past a great ginkgo, a part of the town of Iiyama. It was, after all, the chief seat "
    "of Buddhism in Shinshu, a little town where the past seemed to stand before your eyes: the strange northern houses, "
    "the shingled roofs, the deep eaves built to keep off the winter snow, and here and there, rising high, the temples "
    "and the tops of trees, the whole old-fashioned town seemed wrapped in incense smoke. The one thing that stood out "
    "from this window was the white-painted building of the primary school where Ushimatsu now taught.",
    ["Iiyama"],
    "莲华寺兼营寄宿。濑川丑松突然想搬家，租下的那间屋子，在紧挨着库房的二楼拐角。这座寺是信州下水内郡饭山町二十几座寺院中的一座，"
    "是属于真宗的古刹；倚在那二楼的窗口眺望，隔着一棵大银杏树，还能看见饭山町的一角。不愧是信州第一的佛教之地，一座仿佛让人亲眼看见古代的小城："
    "奇特的北国式房屋、木板铺的屋顶、冬天挡雪用的特制深檐，还有处处高高露出的寺院和树梢——整个古旧的街景都像笼罩在香烟里。"
    "从这扇窗望出去，唯一特别显眼的，就是丑松现在任教的那所小学刷成白色的校舍。",
    ["饭山町"]))

# ---- The Holy Man of Mount Koya (Aozora #521) ----
sources["koya-hijiri"] = 521
lines.append(Q("koya-1", "koya-hijiri", "jp-amo-pass", "Section 1", "第一节", 521,
    "\n".join([cut(521, "「参謀本部編纂の地図を", "引張り出した。"), cut(521, "飛騨から信州へ越える", "雲の形も見えぬ。"),
               cut(521, "道と空との間に", "こう図面を見た。」")]),
    ["飛騨から信州へ越える深山の間道"],
    "'I thought there was no point in opening the General Staff's map again, but the road was so bad that, though it was "
    "stifling even to touch it, I lifted the sleeve of my travelling robe and pulled out the folding map in its covers.\n"
    "It was a byway through the deep mountains, crossing from Hida into Shinshu. There was not a single tree to stop and "
    "rest under; to right and left there was nothing but mountains. Where a peak stood so near it seemed you could reach "
    "out and touch it, peak rode upon peak and summit lay over summit; not a bird could be seen flying, not even the "
    "shape of a cloud.\nBetween the road and the sky there was only I, alone. Shielding myself under my deep, single-layer "
    "cypress hat from the glare of a sun that must have been near noon, so fierce that its very colour had gone white, I "
    "looked at the map like this.'",
    ["a byway through the deep mountains, crossing from Hida into Shinshu"],
    "“我本想，那参谋本部编的地图也不必再翻开看了，可路实在太难走，连手碰一碰都觉得闷热，我还是撩起旅途法衣的袖子，把那本带封皮的折页地图抽了出来。\n"
    "那是从飞驒翻往信州的深山小道，连一棵可以站下歇歇的树都没有，左右全是山；眼看伸手就够得着的山峰上面，又压着一座座山峰，山顶叠着山顶，"
    "看不见飞鸟，也看不见云的影子。\n路和天之间，只有我一个人。大约正午时分，酷热的太阳亮得发白，我把单层的桧木斗笠压得深深的，挡着那光，"
    "就这样看着地图。”",
    ["从飞驒翻往信州的深山小道"]))

# ---- The Crab Cannery Ship (Aozora #1465) ----
sources["crab-cannery-ship"] = 1465
lines.append(Q("kani-1", "crab-cannery-ship", "jp-hakodate-port", "Chapter 1, opening", "第一章开篇", 1465,
    cut(1465, "「おい地獄さ", "んだで！」") + "\n" + cut(1465, "二人はデッキの手すりに", "函館の街を見ていた。"), ["函館の街"],
    "'Hey, we're off to hell!'\nThe two of them leaned on the deck rail, looking at the town of Hakodate, stretched out "
    "like a snail craning its neck, its arms around the sea.",
    ["the town of Hakodate"],
    "“喂，咱们这是下地狱去啦！”\n两个人靠在甲板的栏杆上，望着函馆的街市——它像蜗牛伸长了身子那样延展开去，把海抱在怀里。",
    ["函馆的街市"]))

# ---- Rashomon (Aozora #127) ----
sources["rashomon"] = 127
lines.append(Q("rashomon-1", "rashomon", "jp-rajomon", "Opening", "开篇", 127,
    cut(127, "ある日の暮方の事である。", "雨やみを待っていた。") + "\n" + cut(127, "広い門の下には", "それが、この男のほかには誰もいない。"),
    ["羅生門"],
    "It was one evening, towards dusk. A servant was waiting under the Rashomon for the rain to stop.\nUnder the wide gate "
    "there was no one but this man. Only, on a great round pillar whose red lacquer had peeled away here and there, a "
    "single cricket was clinging. Since the Rashomon stands on Suzaku Avenue, you would think that besides this man there "
    "would be two or three others sheltering from the rain, women in broad sedge hats, men in soft lacquered caps. Yet "
    "there was no one but this man.",
    ["Rashomon"],
    "那是一天傍晚的事。一个家仆在罗生门下等雨停。\n宽阔的门下，除了这个人，再没有别人。只有一根朱漆斑驳的大圆柱上，停着一只蟋蟀。"
    "罗生门既然在朱雀大路上，除了这个人，总该还有两三个戴市女笠、戴揉乌帽子的人在这里避雨才是。可是，除了这个人，一个人也没有。",
    ["罗生门"]))

# ---- One Hundred Views of Mount Fuji (Aozora #270) ----
sources["fugaku-hyakkei"] = 270
lines.append(Q("fugaku-1", "fugaku-hyakkei", "jp-misaka-pass", "The stay at Misaka Pass", "御坂峠一段", 270,
    cut(270, "御坂峠、海抜千三百米。", "それを知つてここへ来た。") + GAP + cut(270, "この峠は、甲府から", "恥づかしくてならなかつた。"),
    ["御坂峠", "天下茶屋"],
    "Misaka Pass, thirteen hundred metres above the sea. At the top of the pass there is a little teahouse called the "
    "Tenka Chaya, and since early summer Mr Ibuse Masuji had shut himself away upstairs there to work. I knew this, and "
    "that is why I came." + GAP +
    "This pass sits at a crossing of the Kamakura road that runs from Kofu out to the Tokaido, and is said to be the finest "
    "place to view Fuji from the north; Fuji seen from here has long been counted one of the three great views of the "
    "mountain. I did not much like it. Worse than not liking it, I despised it. It was a Fuji made to order: Fuji in the "
    "middle, Lake Kawaguchi spread white and cold beneath it, and the near hills crouching quietly at either side as if "
    "holding the lake in their arms. At one look I was flustered and blushed. It was just like a painting on a bathhouse "
    "wall. A stage backdrop. A view so exactly as ordered that I could not bear the shame of it.",
    ["Misaka Pass", "Tenka Chaya"],
    "御坂峠，海拔一千三百米。峠顶上有一家叫天下茶屋的小茶店，井伏鳟二先生从初夏起就闷在这里的二楼写作。我知道这件事，才来到这里。" + GAP +
    "这座山口正当从甲府通往东海道的镰仓往还要冲，据说是从北面观赏富士最好的地方，从这里看见的富士，自古就被算作富士三景之一。可我不怎么喜欢。"
    "不只是不喜欢，甚至瞧不起。这富士也太像定做的了：富士在正中，下面河口湖白茫茫、冷清清地铺开，近处的山静静地蹲在两侧，像是把湖抱在怀里。"
    "我一看，就慌了，脸都红了。这简直是澡堂墙上的油漆画，是戏台上的布景。完全照着订单做出来的风景，我羞得受不了。",
    ["御坂峠", "天下茶屋"]))

# ---- No Longer Human (Aozora #301) ----
sources["no-longer-human"] = 301
lines.append(Q("nlh-1", "no-longer-human", "jp-shayokan", "The First Notebook", "第一手记", 301,
    cut(301, "恥の多い生涯を", "送って来ました。") + "\n" + cut(301, "自分には、人間の生活というものが", "よほど大きくなってからでした。"),
    ["東北の田舎"],
    "Mine has been a life of much shame.\nI have never been able to make out what human life is. I was born in the "
    "countryside of the northeast, and it was not until I was quite big that I saw a train for the first time.",
    ["the countryside of the northeast"],
    "我这一生，尽是可耻的事。\n我对人的生活，一点也摸不着头脑。我生在东北的乡下，第一次看见火车，已经是长得很大以后的事了。",
    ["东北的乡下"]))

# ---------- write ----------
replaced = {"kojiki": "kojiki-s1", "tosa-diary": "tosa-s1", "hojoki": "hojoki-s1", "oku-no-hosomichi": "oku-s1",
            "ugetsu-monogatari": "ugetsu-s1", "takekurabe": "takekurabe-s1", "kokoro": "kokoro-s1",
            "broken-commandment": "hakai-s1", "koya-hijiri": "koya-s1", "crab-cannery-ship": "kani-s1",
            "rashomon": "rashomon-s1", "fugaku-hyakkei": "fugaku-s1", "no-longer-human": "nlh-s1"}
assert set(replaced) == {l["book_id"] for l in lines} == set(sources)

lp = b.data("lines.js")
existing = set(re.findall(r'  \{ id: "([^"]+)"', open(lp, encoding="utf-8").read()))
assert not ({l["id"] for l in lines} & existing), "ids already in use"
for l in lines:
    assert any(f'"{l["place_ids"][0]}"' in r for r in open(b.data("places.js"), encoding="utf-8").read().split("\n") if r.startswith(f'  {{ id: "{l["place_ids"][0]}"')), l["place_ids"]
drop_entries(lp, set(replaced.values()))
b.append(lp, lines, "11-22 quotations from Aozora Bunko, replacing the placeholder scene notes (add_jp3.py)")
for bid, n in sources.items():
    set_source(b.data("books.js"), bid, az.card(AZ, n))
print(len(lines), "quotations;", len(replaced), "scene notes replaced")
