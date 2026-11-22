"""11-22: the English-language public-domain books that had only placeholder scene notes (UK, Ireland, Canada, US),
quoted from English Wikisource (tools/content/wikisource.py: the rendered page's own text) while Project Gutenberg was
down for maintenance. The English is the original (translation: "original"); the Chinese is our own draft for review.
Each quotation replaces the book's placeholder scene note; a book's existing Gutenberg source_url is kept.

What a cut changes, each named again in that line's `checked`:
- where a transcription keeps the printed page's line ends inside a sentence, the lines are joined;
- the 1859 Vanity Fair prints the chapter's first letter as a picture: the W is restored;
- in The Importance of Being Earnest the double space after a speaker's name is evened, and where a transcription
  keeps a double space between sentences (Jude the Obscure), it is evened too.

Still scene notes only:
- not on Wikisource: The Way We Live Now, Melmoth the Wanderer, The Real Charlotte, Some Experiences of an Irish R.M.,
  Yeats's 'Meditations in Time of Civil War' and 'Under Ben Bulben', Klee Wyck, Gone with the Wind (Project Gutenberg
  Australia, its source, cannot be reached from here);
- in Irish, with no Irish text to hand: The Táin, The Islandman;
- no line sets the book at the place on the map: On the Origin of Species (Down House), A Modest Proposal (St Patrick's),
  Castle Rackrent (Edgeworthstown), The Playboy of the Western World (Synge's cottage; the play is set in Mayo), the
  Dollymount scene of A Portrait (the strand is not named), Emily of New Moon, Roughing It in the Bush (Douro is not
  named in the bush chapters).

Usage: python3 -I add_en3.py <app_dir> <wikisource_dir>   (python3 -I ../wikisource.py <dir> en <title> … downloads)"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws
from datafile import drop_entries

APP, WS = sys.argv[1], sys.argv[2]
DATE = "2026-11-22"
GAP = b.GAP
JOINED = " (the page's line ends inside sentences joined)"

def raw(title, start, end, after=None):
    t = ws.text(WS, title)
    i = t.find(start, t.find(after) if after else 0)
    assert i >= 0, (title, start)
    j = t.find(end, i)
    assert j >= 0, (title, start, end)
    return t[i:j + len(end)]

def one(title, start, end, **k):
    s = raw(title, start, end, **k)
    assert "\n" not in s, (title, start, "crosses a line")
    return s

def joined(title, start, end, **k):
    s = raw(title, start, end, **k)
    assert "\n" in s, (title, start, "nothing to join")
    return " ".join(s.split("\n"))

def Q(id, book, place, loc, loc_zh, title, en, hl_en, zh, hl_zh, note=""):
    if "  " in en:                                    # Victorian double spaces after a full stop
        en = re.sub(r"(?<=\S) {2,}", " ", en)
        note = (note[:-1] + "; " if note else " (") + "double spaces between sentences evened)"
    for h in hl_en:
        assert h in en, (id, h)
    for h in hl_zh:
        assert h in zh, (id, h)
    assert "  " not in en and "\xa0" not in en, (id, "spacing")
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh,
                text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh,
                translation="original", status="draft", checked=f"English Wikisource, {title}{note}, {DATE}")

batches = {"uk": [], "ie": [], "ca": [], "us": []}
sources = {}
replaced = {}

def add(cc, scene_ids, title, q):
    batches[cc].append(q)
    sources.setdefault(cc, {}).setdefault(q["book_id"], title)
    replaced.setdefault(cc, []).extend(scene_ids)

# ================= UK =================
TJ = "The History of Tom Jones, a Foundling/Book IX"
add("uk", ["tj-s1"], TJ, Q("tj-1", "tom-jones", "white-lion-upton", "Book IX, chapters 2–3", "第九卷第二至三章", TJ,
    one(TJ, "However, he had better fortune than what attended poor Orpheus", "the famous town of Upton.") + "\n"
    + one(TJ, "Chapter iii. — The arrival of Mr Jones", "the battle of Upton."),
    ["the famous town of Upton", "the inn"],
    "不过，他的运气比可怜的俄耳甫斯好，他把他的同伴，或者不如说他的追随者，平平安安地带进了有名的厄普顿镇。\n"
    "第三章 琼斯先生携女士抵达客栈；附厄普顿之战的详尽描述。",
    ["有名的厄普顿镇", "客栈"]))

NHS = "The Natural History of Selborne, 1879/Letter 1"
add("uk", ["nhs-s1"], NHS, Q("nhs-1", "natural-history-of-selborne", "gilbert-whites-house", "Letter I to Thomas Pennant",
    "致托马斯·彭南特的第一封信", NHS,
    one(NHS, "THE parish of Selborne", "Alton and Petersfield.") + GAP + one(NHS, "The high part of the south-west", "called The Hanger."),
    ["THE parish of Selborne", "The Hanger"],
    "塞尔伯恩教区位于汉普郡的最东角，与萨塞克斯郡接壤，离萨里郡也不远；它在伦敦西南约五十英里，北纬五十一度，"
    "差不多在奥尔顿和彼得斯菲尔德两镇的正中间。\n…\n西南面的高处是一座巨大的白垩山，高出村子三百英尺，分为一片羊群牧场、"
    "高林和一片长长的悬林，叫做“垂林”。",
    ["塞尔伯恩教区", "垂林"]))

JSN = "The Private Memoirs and Confessions of a Justified Sinner/The Editor's Narrative"
add("uk", ["jsn-s1"], JSN, Q("jsn-1", "justified-sinner", "arthurs-seat", "The Editor's Narrative", "编者的叙述", JSN,
    one(JSN, "George was, from infancy", "out of the eastern ocean.") + GAP
    + one(JSN, "George did admire this halo of glory", "beneath his feet."),
    ["Arthur's Seat"],
    "乔治从小就生性好动，受不了拘束；近来这个古怪的纠缠者让他少年人的游戏大受限制，他对这种约束越来越不耐烦。一天早上，"
    "他碰巧醒得很早，便起身到亚瑟王座山顶去走走，呼吸黎明的清风，看太阳从东边的大海里升起来。\n…\n"
    "乔治确实赞叹这圈光环，它越来越宽，也越来越模糊，因为他正接近云层的表面。可是，令他大为惊奇、也大为欣喜的是，"
    "到了亚瑟王座山顶，他发现这道月下的彩虹、这圈人间的光环，正以最鲜艳的色彩铺展在他脚下。",
    ["亚瑟王座"]))

OE = "Confessions of an English Opium-Eater/Part II Introduction"
add("uk", ["oe-s1"], OE, Q("oe-1", "opium-eater", "pantheon-oxford-street", "Part II, opening", "第二部开篇", OE,
    one(OE, "So then, Oxford-street", "groans of innumerable hearts."), ["Oxford-street"],
    "就这样，牛津街，铁石心肠的后母啊！你倾听孤儿的叹息，啜饮孩子的眼泪，我终于离开了你：时候终于到了，"
    "我不必再痛苦地在你那望不到头的街廊上踱步，不必再做梦，醒来又陷入饥饿的痛苦。后来，太多继我之后的人，"
    "想必又踏上了我和安的足迹，继承了我们的苦难：除了安，还有别的孤儿叹过气；别的孩子也流过泪；而你，牛津街，"
    "此后想必也回荡过无数颗心的呻吟。",
    ["牛津街"]))

VF = "Vanity Fair (Thackeray)/Chapter 1"
vf = one(VF, "HILE the present century", "four miles an hour.")
add("uk", ["vf-s1"], VF, Q("vf-1", "vanity-fair", "walpole-house", "Chapter 1, 'Chiswick Mall'", "第一章《奇西克林荫道》", VF,
    "W" + vf, ["Chiswick Mall"],
    "当本世纪还在十几岁的时候，六月里一个阳光明媚的早晨，一辆大大的家用马车驶到了奇西克林荫道上平克顿小姐女子学校的大铁门前，"
    "马车由两匹肥马拉着，马具闪闪发亮，赶车的是个戴三角帽和假发的胖车夫，车速每小时四英里。",
    ["奇西克林荫道"], " (the chapter's first letter, printed as a picture, restored)"))

VIL = "Villette (1st edition)/Chapter 6"
add("uk", ["vil-s1"], VIL, Q("vil-1", "villette", "st-pauls", "Chapter 6, 'London'", "第六章《伦敦》", VIL,
    one(VIL, "The next day was the first of March", "Jonah's gourd."), ["the dome"],
    "第二天是三月一日。我醒来，起床，拉开窗帘，看见初升的太阳正在雾中挣扎。在我头顶上方，在屋顶之上，几乎与云齐高，"
    "我看见一团庄严的、圆圆的、暗蓝而朦胧的东西——那穹顶。我望着它，内心为之一动；我那一向被束缚的灵魂把翅膀半松开来抖了抖；"
    "我突然觉得，从未真正活过的我，终于要尝到生活的滋味了：那天早上，我的灵魂长得像约拿的蓖麻一样快。",
    ["那穹顶"]))

DD = "Daniel Deronda (First Edition)/Volume 3/Chapter 40"
add("uk", ["dd-s1"], DD, Q("dd-1", "daniel-deronda", "blackfriars-bridge", "Chapter 40", "第四十章", DD,
    one(DD, "When the wherry was approaching Blackfriars Bridge", "that brooding glory."), ["Blackfriars Bridge"],
    "小船驶近黑衣修士桥时——德龙达打算在那里上岸——已是四点半，灰色的白昼正壮丽地死去，西天的云朵碎成一道道渐窄的紫色云层，"
    "衬着一片铺展开来的橘黄色的明净；这片明净在天上显出一种纪念碑般的宁静，映在河面上却成了流动的光：涟漪和水流交替闪烁，"
    "褐色的帆骤然发亮，满载的驳船从漆黑驶入色彩之中，活跃地回应着那片沉思的光辉。",
    ["黑衣修士桥"]))

BT = "Barchester Towers/Chapter 1"
add("uk", ["bt-s1"], BT, Q("bt-1", "barchester-towers", "salisbury", "Chapter 1, opening", "第一章开篇", BT,
    one(BT, "IN the latter days of July", "Who was to be the new Bishop?"), ["the cathedral city of Barchester"],
    "185—年七月下旬，在巴彻斯特这座大教堂城里，有一个极其重要的问题，十天来每个小时都有人问起，每个小时又有各种各样的回答——"
    "谁会是新主教？",
    ["巴彻斯特这座大教堂城"]))

JUDE = "Jude the Obscure/Part 1/Chapter 3"
add("uk", ["jto-s1"], JUDE, Q("jude-1", "jude-the-obscure", "oxford", "Part 1, chapter 3", "第一部第三章", JUDE,
    raw(JUDE, '"I wanted to know where the city of Christminster is', "I don't know what.\""),
    ["the city of Christminster", "Christminster is out across there"],
    "“我想知道基督寺城在哪儿，劳驾。”\n“基督寺在那边，那片树丛过去。你能看见它——至少天气晴朗的时候能看见。啊，不行，现在看不见。”\n"
    "另一个瓦匠也乐得从单调的活计里分分心，跟着朝那个方向望去。“这种天气很少能看见，”他说，“我看见它的时候，"
    "是太阳落山、一片火光的时候，那时候它看上去就像——我也说不上像什么。”",
    ["基督寺城", "基督寺在那边"]))

MC1, MC4 = "The Mayor of Casterbridge (Hardy, 1886)/Volume 1/Chapter 1", "The Mayor of Casterbridge (Hardy, 1886)/Volume 1/Chapter 4"
add("uk", ["moc-s1"], MC1, Q("moc-1", "mayor-of-casterbridge", "weyhill", "Chapter 1, opening", "第一章开篇", MC1,
    one(MC1, "One evening of late summer", "on foot."), ["Weydon-Priors"],
    "夏末的一个傍晚，本世纪还不到三十年的时候，一对年轻男女正步行走近韦敦-普赖尔斯这个大村子，女的抱着一个孩子。",
    ["韦敦-普赖尔斯"]))
add("uk", ["moc-s2"], MC1, Q("moc-2", "mayor-of-casterbridge", "dorchester-casterbridge", "Chapter 4", "第四章", MC4,
    one(MC4, "Sometimes they might have been seen on foot", "drew near to Casterbridge.") + GAP
    + one(MC4, "It was on a Friday evening", "the town and its environs."), ["Casterbridge", "the town"],
    "她们有时步行，有时搭农夫的大车，有时搭运货马车；就这样，她们走近了卡斯特桥。\n…\n那是九月中旬的一个星期五傍晚，天刚要黑，"
    "她们来到离目的地一英里的一座小山顶上。这里的大路两旁没有树篱，她们走上绿草地坐了下来。从这里可以把那座城镇及其四周一览无余。",
    ["卡斯特桥", "那座城镇"]))

ASH = "The Adventures of Sherlock Holmes (1892, US)/A Scandal in Bohemia"
add("uk", ["ash-s1"], ASH, Q("ash-1", "adventures-of-sherlock-holmes", "baker-street", "'A Scandal in Bohemia'",
    "《波希米亚丑闻》", ASH,
    joined(ASH, "One night—it was on the 20th of March, 1888", "his extraordinary powers."), ["Baker Street"],
    "一天夜里——那是1888年3月20日——我出诊回来（我那时已重新开业行医），路过贝克街。经过那扇记忆犹新的门时——在我心里，"
    "它总是同我的求婚、同《血字的研究》里那些阴暗的事件连在一起——我忽然非常想再见见福尔摩斯，想知道他正在怎样运用他那非凡的才能。",
    ["贝克街"], JOINED))

DP = "De Profundis (Wilde, 1915)/De Profundis"
add("uk", ["dp-s1"], DP, Q("dp-1", "de-profundis", "reading-gaol", "The letter from Reading Gaol", "雷丁狱中书", DP,
    one(DP, "People point to Reading Gaol", "lead to worse places."), ["Reading Gaol"],
    "人们指着雷丁监狱说：“那就是艺术生活把人引向的地方。”嗯，它还可能把人引到更糟的地方去。",
    ["雷丁监狱"]))

IBE = "The Importance of Being Earnest/Act I"
ibe = raw(IBE, "Jack.\xa0 In the cloak-room at Victoria Station.", "The line is immaterial.")
assert "\xa0 " in ibe
add("uk", ["ibe-s1"], IBE, Q("ibe-1", "importance-of-being-earnest", "victoria-station", "Act I", "第一幕", IBE,
    ibe.replace("\xa0 ", " "), ["Victoria Station", "The Brighton line"],
    "杰克：在维多利亚车站的衣帽寄存处。是别人错当成自己的包拿给他的。\n布拉克内尔夫人：维多利亚车站的衣帽寄存处？\n"
    "杰克：是的。布莱顿线。\n布拉克内尔夫人：哪条线无关紧要。",
    ["维多利亚车站", "布莱顿线"], " (the no-break space and space after a speaker's name or a full stop written as one space)"))

NGS = "New Grub Street/Chapter VIII"
add("uk", ["ngs-s1"], NGS, Q("ngs-1", "new-grub-street", "bm-reading-room", "Chapter 8", "第八章", NGS,
    joined(NGS, "The days darkened.", "was not there."), ["the Museum", "the Reading-room"],
    "日子越来越暗。玛丽安冒着十一月的雨和雾，照常去博物馆，在那里同别的辛苦人一起辛苦。也许一个星期有一次，"
    "她允许自己在阅览室的走道间徘徊，偷偷打量坐在书桌前的人，可是她也许能找到的那张脸并不在那里。",
    ["博物馆", "阅览室"], JOINED))

HOD = "Youth: a Narrative, and Two Other Stories/Heart of Darkness/Section 1"
add("uk", ["hod-s1"], HOD, Q("hod-1", "heart-of-darkness", "gravesend", "Part 1, opening", "第一部开篇", HOD,
    raw(HOD, "The Nellie, a cruising yawl", "town on earth."), ["the Thames", "Gravesend"],
    "“奈莉号”是一艘巡游用的双桅帆船，它在锚上转了个身，帆一动不动，停了下来。潮水已经涨满，风几乎静了，"
    "既然要顺流而下，就只好停船，等着退潮。\n泰晤士河的入海河段在我们面前伸展开去，像一条无尽水道的开端。远处海天相接，浑然一体，"
    "没有一丝接缝；在那片明亮的空间里，驳船那晒成褐色的帆随着潮水向上游漂来，仿佛静止不动，成了一簇簇尖尖的红帆，"
    "上过漆的斜杠闪着光。一层薄雾笼罩着低平的河岸，河岸平平地伸进大海，渐渐消失。格雷夫森德上空的天色是暗的，"
    "再往后，天色仿佛凝成一片凄凉的阴郁，一动不动地笼罩在那座地球上最大、最伟大的城市上空。",
    ["泰晤士河", "格雷夫森德"]))

WIL = "Women in Love/Chapter XIV"
add("uk", ["wil-s1"], WIL, Q("wil-1", "women-in-love", "moorgreen-reservoir", "Chapter 14, 'Water-Party'", "第十四章《水上聚会》", WIL,
    joined(WIL, "Every year Mr Crich gave", "the boat-house by the lake."), ["Willey Water"],
    "克里奇先生每年都要在湖上举办一场多少带点公开性质的水上聚会。威利湖上有一艘小游艇和几条划艇，客人们可以在宅子院里搭起的大帐篷里喝茶，"
    "也可以在湖边船屋旁那棵大胡桃树的树荫下野餐。",
    ["威利湖"], JOINED))

ROO = "A Room of One's Own (Hogarth 1929)/Chapter 1"
add("uk", ["roo-s1"], ROO, Q("roo-1", "room-of-ones-own", "newnham-college", "Chapter 1 (dinner at Fernham)",
    "第一章（在芬汉姆用餐）", ROO,
    one(ROO, "Here was my soup.", "The plate was plain."), ["the great dining-hall"],
    "我的汤来了。晚饭在大餐厅里供应。根本不是春天，实际上是十月的一个傍晚。大家都聚在大餐厅里。晚饭准备好了。汤来了。"
    "那是一道清淡的肉汁汤，没有什么能激起想象的。透过那透明的汤水，盘子上要是有什么花纹，都能看得一清二楚。可是盘子上没有花纹。"
    "那是一只素净的盘子。",
    ["大餐厅"]))

WOTW = "The War of the Worlds (1898)/Book 1/Chapter 2"
add("uk", ["wotw-s1"], WOTW, Q("wotw-1", "war-of-the-worlds", "horsell-common", "Book 1, chapter 2", "第一部第二章", WOTW,
    raw(WOTW, "\"It's out on Horsell Common now.\"", "something inside.\""), ["Horsell Common"],
    "“它现在就在霍塞尔公地上。”\n“天哪！”亨德森说，“陨石掉下来了！太好了。”\n"
    "“可它不只是陨石。它是个圆筒——人造的圆筒，老兄！里面还有东西。”",
    ["霍塞尔公地"]))

# ================= Ireland =================
INN = "The Lake Isle of Innisfree"
add("ie", ["yeats-s1"], INN, Q("yeats-1", "yeats-poems", "ie-innisfree", "'The Lake Isle of Innisfree'", "《茵纳斯弗利岛》", INN,
    raw(INN, "I will arise and go now, and go to Innisfree", "in the deep heart's core."), ["Innisfree", "lake water"],
    "我要起身走了，去茵纳斯弗利岛，\n在那里用黏土和枝条搭一间小屋：\n种九垄豆子，养一箱蜜蜂，\n独自住在蜂声嗡嗡的林间空地。\n"
    "我会在那里得到些许安宁，因为安宁慢慢滴落，\n从清晨的面纱滴落到蟋蟀歌唱的地方；\n那里半夜一片微光，正午一片紫光，\n"
    "傍晚满是红雀的翅膀。\n我要起身走了，因为无论白天黑夜\n我总听见湖水轻轻拍岸的低声；\n当我站在马路上，或在灰色的人行道上，\n"
    "我在心灵深处听见它。",
    ["茵纳斯弗利岛", "湖水"]))

SW = "The Wild Swans at Coole (Collection)/The Wild Swans at Coole"
add("ie", ["yeats-s2"], SW, Q("yeats-2", "yeats-poems", "ie-coole-park", "'The Wild Swans at Coole', stanzas 1–2",
    "《柯尔庄园的野天鹅》第一、二节", SW,
    raw(SW, "The trees are in their autumn beauty", "Upon their clamorous wings."), ["nine and fifty swans"],
    "树木披着秋天的美，\n林中小径干燥，\n十月的暮色里，湖水\n映着静止的天空；\n石头间漫溢的水面上\n浮着五十九只天鹅。\n"
    "自从我第一次数它们，\n第十九个秋天已经来临；\n我还没数完，就看见\n它们一下子全飞了起来，\n盘旋着散成一个个巨大的断环，\n"
    "拍着喧闹的翅膀。",
    ["五十九只天鹅"]))

ARAN = "The Aran Islands/Parts 1 & 2/Part I"
add("ie", ["aran-s1"], ARAN, Q("aran-1", "aran-islands", "ie-synges-chair", "Part I", "第一部", ARAN,
    one(ARAN, "They walked on with me to the sound", "two walls of cliff."), ["Inishmaan"],
    "他们陪我一直走到把这个岛和伊尼什曼——群岛中间那个岛——隔开的海峡边，指给我看大西洋的浪涌从两道悬崖之间涌进来。",
    ["伊尼什曼"]))

DEAD = "Dubliners/The Dead"
add("ie", ["dubliners-s1"], DEAD, Q("dubliners-1", "dubliners", "ie-usher-island", "'The Dead'", "《死者》", DEAD,
    one(DEAD, "For years and years it had gone off in splendid style", "the corn-factor on the ground floor."),
    ["Usher's Island"],
    "多少年来，它一直办得风风光光，人们记得的年头里都是如此；自从凯特和朱莉娅在她们的哥哥帕特死后离开了斯托尼巴特的房子，"
    "带着她们唯一的侄女玛丽·简搬到厄舍岛上那座阴暗、空落的房子里住，就一直这样。那座房子的楼上是她们从一楼的谷物商富勒姆先生那里租来的。",
    ["厄舍岛"]))

POR = "A Portrait of the Artist as a Young Man/Chapter 1"
add("ie", ["portrait-s1"], POR, Q("portrait-1", "portrait", "ie-clongowes", "Chapter 1", "第一章", POR,
    raw(POR, "He turned to the flyleaf of the geography", "The Universe"), ["Clongowes Wood College"],
    "他翻到地理课本的扉页，读他在那里写下的东西：他自己，他的名字，还有他在哪里。\n斯蒂芬·迪达勒斯\n基础班\n克朗格斯伍德公学\n"
    "萨林斯\n基尔代尔郡\n爱尔兰\n欧洲\n世界\n宇宙",
    ["克朗格斯伍德公学"]))

U1, U3, U18 = "Ulysses (1922)/Chapter 1", "Ulysses (1922)/Chapter 3", "Ulysses (1922)/Chapter 18"
add("ie", ["ulysses-s1"], U1, Q("ulysses-1", "ulysses", "ie-joyce-tower", "Episode 1, opening", "第一章开篇", U1,
    raw(U1, "Stately, plump Buck Mulligan", "Come up, you fearful Jesuit."), ["the stairhead", "the dark winding stairs"],
    "庄重而丰腴的勃克·穆利根从楼梯口走上来，手里端着一碗肥皂沫，碗上交叉放着一面镜子和一把剃刀。他没系腰带的黄色晨衣被清晨温和的风"
    "轻轻托在身后。他把碗高高举起，吟诵道：\n——我要走向天主的祭台。\n他停下来，朝幽暗的盘旋楼梯下面张望，粗声大气地喊道：\n"
    "——上来，金赤。上来，你这吓人的耶稣会士。",
    ["楼梯口", "幽暗的盘旋楼梯"]))
add("ie", ["ulysses-s2"], U1, Q("ulysses-2", "ulysses", "ie-sandymount", "Episode 3, 'Proteus'", "第三章《普洛透斯》", U3,
    one(U3, "Sounds solid:", "Wild sea money."), ["Sandymount strand"],
    "听上去很结实：是造物主那把木槌造出来的。我是在沿着沙丘湾海滩走进永恒吗？嘎吱，咔嚓，嘎嘎，嘎嘎。野海的钱币。",
    ["沙丘湾海滩"]))
add("ie", ["ulysses-s3"], U1, Q("ulysses-3", "ulysses", "ie-howth-head", "Episode 18, 'Penelope'", "第十八章《珀涅罗珀》", U18,
    joined(U18, "the sun shines for you he said the day we were lying", "out of my mouth",
           after="they might as well try to stop the sun"), ["Howth head"],
    "太阳是为你照耀的他说那天我们躺在豪斯岬的杜鹃花丛里他穿着灰色花呢衣服戴着草帽那天我让他向我求婚是的我先把嘴里那块香籽饼喂给了他",
    ["豪斯岬"], JOINED))

# ================= Canada =================
AOGG = "Anne of Green Gables (1908)/Chapter I"
add("ca", ["aogg-s1"], AOGG, Q("aogg-1", "anne-of-green-gables", "ca-green-gables", "Chapter 1", "第一章", AOGG,
    one(AOGG, "Accordingly after tea Mrs. Rachel set out", "did not call living in such a place living at all."),
    ["Green Gables"],
    "于是喝过茶后，雷切尔太太就出发了；她要去的地方不远，卡斯伯特家住的那座大而散漫、掩映在果园里的房子，离林德谷沿路往上只有四分之一英里不到。"
    "不过那条长长的小路倒让路程远了不少。马修·卡斯伯特的父亲和后来的儿子一样腼腆寡言，当初建宅时，他在不至于退进树林的前提下，"
    "尽可能远离了他的同类。绿山墙就建在他开垦出来的土地的最远处，至今仍在那里，从大路上几乎看不见，而埃文利的其他人家都亲亲热热地沿着大路排开。"
    "雷切尔·林德太太认为住在那样的地方根本算不上过日子。",
    ["绿山墙"]))

WF = "White Fang/4.4"
add("ca", ["wf-s1"], WF, Q("wf-1", "white-fang", "ca-dawson", "Part 4, chapter 4", "第四部第四章", WF,
    raw(WF, "\"Wait till I get back to Dawson,\"", "\"Yes,\" Beauty Smith grunted, shrinking away."), ["Dawson"],
    "“等我回到道森再说，”美人史密斯威胁道，“我要告你。”\n“你回到道森要是敢开口，我就把你赶出城去。明白吗？”\n"
    "美人史密斯哼了一声。\n“明白吗？”对方突然厉声大喝。\n“明白，”美人史密斯哼哼着，缩着身子退开了。",
    ["道森"]))

# ================= US =================
EDL = "The Life and Letters of Emily Dickinson/Letters of Emily Dickinson"
add("us", ["usedl-s1"], EDL, Q("usedl-1", "letters-emily-dickinson", "us-amherst-dickinson-museum",
    "Letter to Louisa Norcross, December 1861", "致路易莎·诺克罗斯的信，1861 年 12 月", EDL,
    joined(EDL, "My garden is all covered up by snow", "long white nightgowns."), ["My garden"],
    "我的花园全被雪盖住了；星期二还摘过紫罗兰，现在紫罗兰都睡了。山丘脱下紫色的外衣，换上长长的白睡袍。",
    ["我的花园"], JOINED))

# ---------- write ----------
for cc in ["uk", "ie", "ca", "us"]:
    b.init(APP, None, cc, DATE)
    lp, bp = b.data("lines.js"), b.data("books.js")
    existing = set(re.findall(r'  \{ id: "([^"]+)"', open(lp, encoding="utf-8").read()))
    assert not ({l["id"] for l in batches[cc]} & existing), (cc, "ids already in use")
    drop_entries(lp, set(replaced[cc]))
    b.append(lp, batches[cc], "11-22 quotations from English Wikisource, replacing the placeholder scene notes (add_en3.py)")
    bs = open(bp, encoding="utf-8").read()
    for bid, title in sources[cc].items():
        pat = re.compile(r'(  \{ id: "' + re.escape(bid) + r'",[^\n]*?source_url: )null')
        bs, k = pat.subn(lambda m: m.group(1) + json.dumps(ws.url("en", title), ensure_ascii=False), bs)
        assert k <= 1, bid
    open(bp, "w", encoding="utf-8").write(bs)
    print(cc, len(batches[cc]), "quotations for", len({l["book_id"] for l in batches[cc]}), "books;",
          len(replaced[cc]), "scene notes replaced")
