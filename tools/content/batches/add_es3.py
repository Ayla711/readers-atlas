"""11-22: Spain, quotations for the public-domain books that had only placeholder scene notes, taken from Spanish
Wikisource (tools/content/wikisource.py: the rendered page's own text). English and Chinese are our own translations
(translation: "own"), drafts for review. Homage to Catalonia is written in English: its text comes from Project
Gutenberg Australia (Project Gutenberg itself was down for maintenance) and only the Chinese is ours.
Each quotation replaces the book's placeholder scene note.

What a cut changes, each named again in that line's `checked`:
- the Poema del Cid (Sánchez, 1779) numbers every fifth line and brackets lines that were one in the manuscript; the
  numbers and the bracket are left out;
- where a play sets two or more spaces between a speaker's name and the speech, one space is kept;
- where a scanned page's line ends fall inside a prose speech (El sí de las niñas, Trafalgar), the lines are joined;
- the 1905 Quixote prints the first letter of the chapter as a picture: the E is restored;
- in El monte de las ánimas the transcription reads "ios Templarios" for "los Templarios" (a misread l): corrected.

Still scene notes only:
- Don Quixote Part II (Wikisource has Part I only, so dq-s2 stays);
- the Spiritual Canticle (the poem names no place), Romancero gitano ("Romance sonámbulo" names none, and neither
  ties to the Huerta de San Vicente), Blood Wedding (names no place; the Cortijo del Fraile is its real-life source);
- The Three-Cornered Hat (its city is never named, so no line can be set at Guadix), Miau (the ministry building is
  never described), The House of Ulloa (the place on the map is the author's house in A Coruña, which the novel does
  not reach).

Usage: python3 -I add_es3.py <app_dir> <wikisource_dir>   (python3 -I ../wikisource.py <dir> es <title> … downloads)"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws
from datafile import drop_entries, set_source

APP, WS = sys.argv[1], sys.argv[2]
DATE = "2026-11-22"
b.init(APP, None, "es", DATE)
GAP = b.GAP
cut = lambda t, a, z, **k: ws.cut(WS, t, a, z, **k)
blk = lambda t, a, z, **k: ws.block(WS, t, a, z, **k)

def spaced(s):
    """one space between a speaker's name and the speech"""
    assert re.search(r"[^\s] {2,}", s), s[:40]
    return re.sub(r"(?<=[^\s]) {2,}", " ", s)

def joined(s):
    """a prose speech whose page line ends were kept by the transcription"""
    return " ".join(s.split("\n"))

SPACED = "; spacing after the speaker's name evened"
JOINED = "; the page's line ends inside the speech joined"

def unindent(s):
    """the edition's verse indent, printed as no-break spaces, which block() does not take off"""
    assert "\n\xa0" in s, s[:40]
    return "\n".join(l.lstrip("\xa0 ") for l in s.split("\n"))

def Q(id, book, place, loc, loc_zh, title, orig, hl_orig, en, hl_en, zh, hl_zh, note=""):
    for h in hl_orig:
        assert h in orig, (id, h)
    for h in hl_en:
        assert h in en, (id, h)
    for h in hl_zh:
        assert h in zh, (id, h)
    assert "  " not in orig and "\xa0" not in orig, (id, "double or no-break space")
    return dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh,
                text_orig=orig, highlight_orig=hl_orig, text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh,
                translation="own", status="draft", checked=f"Spanish Wikisource, {title}{note}, {DATE}")

lines, sources = [], {}

# ---- Cantar de mio Cid (Tomás Antonio Sánchez, 1779) ----
CID = "Colección de poesías castellanas anteriores al siglo XV/Tomo I/Poema del Cid"
sources["cantar-de-mio-cid"] = CID
def cid(a, z):
    out = []
    for l in blk(CID, a, z).split("\n"):
        l = re.sub(r"^\d+ ", "", l)
        l = re.sub(r"^\{\s+", "", l)
        out.append(l)
    return "\n".join(out)
CIDNOTE = " (Sánchez's line numbers and bracket left out)"
lines.append(Q("cid-1", "cantar-de-mio-cid", "es-burgos-cathedral", "Cantar I, lines 15–20", "第一歌，第 15–20 行", CID,
    cid("15 Mio Cid Ruy Diaz por Burgos", "si oviese buen Señor!"), ["Burgos"],
    "My Cid Ruy Díaz rode into Burgos,\nsixty pennons in his company;\nmen and women came out to see him,\n"
    "the burghers and their wives stood at the windows,\nweeping from their eyes, so great was their grief.\n"
    "From every mouth came one saying:\n'God, what a good vassal, if only he had a good lord!'",
    ["Burgos"],
    "我的熙德鲁伊·迪亚斯进入布尔戈斯，\n随行六十面旌旗；\n男男女女出来看他，\n市民和他们的妻子都站在窗前，\n泪流满面，悲痛至极。\n"
    "人人口中说着同一句话：\n“天哪，多好的臣子，可惜没有一位好主君！”",
    ["布尔戈斯"], CIDNOTE))
lines.append(Q("cid-2", "cantar-de-mio-cid", "es-burgos-cathedral", "Cantar I, lines 50–56", "第一歌，第 50–56 行", CID,
    cid("50 Ya lo vee el Cid", "en la Glera posaba."), ["Sancta Maria"],
    "The Cid sees now that he has no favour from the king.\nHe leaves the door and spurs on through Burgos;\n"
    "he comes to Santa María, and at once dismounts,\nfalls on his knees, and prays from his heart.\n"
    "The prayer made, he mounts again,\nrides out through the gate and camps by the Arlanzón,\n"
    "beside that town, upon the sandbank.",
    ["Santa María"],
    "熙德这才明白，国王不肯开恩。\n他离开那扇门，策马穿过布尔戈斯；\n来到圣玛利亚教堂，随即下马，\n双膝跪地，诚心祈祷。\n"
    "祷告完毕，他又上马，\n出了城门，在阿兰松河边扎营，\n就在城外的沙洲上。",
    ["圣玛利亚教堂"], CIDNOTE))

# ---- The Book of Good Love ----
LBA = "Libro de Buen Amor/041C"
sources["libro-de-buen-amor"] = LBA
lines.append(Q("lba-1", "libro-de-buen-amor", "es-hita", "Stanza 575", "第 575 节", LBA,
    blk(LBA, "Yo Joan Ruis, el sobredicho", "en toda esta coyta."), ["arçipreste de Hita"],
    "I, Juan Ruiz, the aforesaid Archpriest of Hita,\nthough my heart never gives up making verses,\n"
    "never found such a lady as Love paints for you,\nnor do I think I shall find her in all this trouble.",
    ["Archpriest of Hita"],
    "我，胡安·鲁伊斯，前面说过的伊塔大司铎，\n虽然我的心从不停止作诗，\n却从没遇见过爱神为你描绘的那样一位女子，\n"
    "我想在这一切苦恼里也不会遇见。",
    ["伊塔大司铎"]))

# ---- Count Lucanor, the author's preface ----
LUC = "Conde Lucanor/Anteprólogo"
sources["conde-lucanor"] = LUC
lines.append(Q("luc-1", "conde-lucanor", "es-penafiel", "The author's preface", "作者前言", LUC,
    cut(LUC, "Et los libros que él fizo son éstos", "que él fizo en Peñafiel."), ["Peñafiel"],
    "And the books he has made so far are these: the Abridged Chronicle, the Book of the Wise, the Book of Chivalry, "
    "the Book of the Prince, the Book of the Knight and the Squire, the Book of the Count, the Book of Hunting, the Book "
    "of Engines, the Book of Songs. And these books are in the monastery of the Preaching Friars that he founded at "
    "Peñafiel.",
    ["Peñafiel"],
    "他至今写成的书有这些：《编年史略》《智者之书》《骑士之书》《王子之书》《骑士与侍从之书》《伯爵之书》《狩猎之书》"
    "《器械之书》《歌谣之书》。这些书都存放在他在佩尼亚菲尔创建的多明我会修道院里。",
    ["佩尼亚菲尔"]))

# ---- La Celestina, Act XIX (1913 edition) ----
CEL = "La Celestina (1913)/Aucto décimonono"
sources["la-celestina"] = CEL
lines.append(Q("cel-1", "la-celestina", "es-huerto-calixto", "Act XIX", "第十九幕", CEL,
    spaced(blk(CEL, "SOSIA.-  ¡O Tristán, discreto mancebo!", "buena señal de mi amor en absencia.")), ["huerto", "pared"],
    "SOSIA. O Tristán, wise lad! You have told me much more than your years call for. A shrewd suspicion you have "
    "flushed, and I believe a true one. But since we have reached the garden and our master is coming up to us, let us "
    "leave this story, which is very long, for another day.\nCALISTO. Set up the ladder, lads, and be quiet, for I "
    "think my lady is talking inside. I will climb on top of the wall and listen from there, to see whether I hear some "
    "good sign of my love while I am away.",
    ["the garden", "the wall"],
    "索西亚：啊，特里斯坦，你真是个聪明小伙子！你跟我说的远远超出了你这个年纪。你嗅出了一个精明的怀疑，我相信是真的。"
    "不过我们已经到了花园，主人也朝我们走过来了，这个故事太长，留到改天再说吧。\n卡利斯托：孩子们，把梯子架好，别出声，"
    "我好像听见我的小姐在里面说话。我爬到墙头上去，在那儿听着，看能不能听到她在我不在时说起我的什么好话。",
    ["花园", "墙头"], SPACED))
lines.append(Q("cel-2", "la-celestina", "es-huerto-calixto", "Act XIX", "第十九幕", CEL,
    spaced(blk(CEL, "TRISTÁN.-  Tente, señor, no baxes", "ni se bulle.")), ["caydo del escala"],
    "TRISTÁN. Hold on, sir, don't come down, they've gone; it was only Traso the Lame and some other rogues going by "
    "shouting. Sosia is coming back now. Hold on, hold on, sir, with your hands on the ladder.\nCALISTO. Oh, Holy Mary "
    "save me! I am dead! Confession!\nTRISTÁN. Come quick, Sosia, our poor master has fallen from the ladder and neither "
    "speaks nor moves.",
    ["fallen from the ladder"],
    "特里斯坦：等等，老爷，别下来，他们走了；不过是瘸子特拉索和别的几个无赖，一路喊着过去了。索西亚已经回来了。"
    "抓住，抓住梯子，老爷！\n卡利斯托：啊，圣母玛利亚救我！我要死了！我要忏悔！\n特里斯坦：快过来，索西亚，"
    "我们可怜的主人从梯子上摔下来了，不说话也不动了。",
    ["从梯子上摔下来了"], SPACED))

# ---- Lazarillo de Tormes, Tratado I ----
LAZ = "El Lazarillo de Tormes/Tratado primero"
sources["lazarillo-de-tormes"] = LAZ
lines.append(Q("laz-1", "lazarillo-de-tormes", "es-verraco-salamanca", "Tratado I", "第一章", LAZ,
    blk(LAZ, "Salimos de Salamanca", "Y rió mucho la burla."),
    ["Salamanca", "un animal de piedra, que casi tiene forma de toro"],
    "We left Salamanca, and coming to the bridge, there is at its entrance an animal of stone that has almost the shape "
    "of a bull, and the blind man told me to go up close to the animal, and when I was there he said:\n'Lázaro, put "
    "your ear to this bull and you will hear a great noise inside it.'\nI, simple as I was, went up, believing it to be "
    "so. And as soon as he felt my head close to the stone, he struck out hard with his hand and banged my head against "
    "that devil of a bull, so that the pain of the goring lasted me more than three days, and he said to me:\n'Fool, "
    "learn that a blind man's boy must know one point more than the devil.'\nAnd he laughed a great deal at the joke.",
    ["Salamanca", "an animal of stone that has almost the shape of a bull"],
    "我们出了萨拉曼卡，来到桥头，桥口有一头石头雕的牲口，样子差不多像一头牛。瞎子叫我走到那牲口跟前，我站好了，他就说：\n"
    "“拉撒路，把耳朵贴到这头牛上，你会听见里面有很大的声响。”\n我老老实实地凑上去，以为真是这样。他一觉出我的头挨着石头，"
    "就使劲一推，让我的脑袋在那头见鬼的牛上狠狠撞了一下，这一“牛角顶”疼了我三天还多。他对我说：\n"
    "“傻瓜，记住，给瞎子领路的孩子得比魔鬼还多懂一分。”\n他为这个恶作剧笑了好半天。",
    ["萨拉曼卡", "石头雕的牲口，样子差不多像一头牛"]))

# ---- The Book of Her Life, chapter 9 ----
VID = "Su vida (Santa Teresa de Jesús)/Capítulo IX"
sources["libro-de-la-vida"] = VID
lines.append(Q("vida-1", "libro-de-la-vida", "es-encarnacion-avila", "Chapter 9", "第九章", VID,
    cut(VID, "Pues ya andaba mi alma cansada", "para no ofenderle."), ["el oratorio", "en casa"],
    "My soul was now weary, and, though it wished to, the bad habits I had would not let it rest. It happened that, "
    "going one day into the oratory, I saw an image that had been brought there to be kept, which had been got for a "
    "certain feast held in the house. It was of Christ sorely wounded, and so devout that, as I looked at it, I was "
    "utterly shaken to see him so, for it showed well what he went through for us. So great was what I felt at how "
    "badly I had thanked him for those wounds that my heart seemed to break; and I threw myself down beside him with a "
    "great flood of tears, begging him to strengthen me once and for all, so that I would not offend him.",
    ["the oratory", "the house"],
    "那时我的灵魂已经疲惫不堪，虽然它想安歇，我那些恶习却不让它安歇。有一天我走进祈祷室，看见一尊像，是为院里要办的"
    "某个节日找来、暂时放在那里的。那是一尊遍体伤痕的基督像，那样虔敬动人，我一看见他这副模样，整个人都震动了，"
    "因为它真切地表现出他为我们受的苦。想到自己对这些伤痕是多么不知感恩，我的心仿佛要碎了；我扑倒在他身旁，泪如泉涌，"
    "求他一劳永逸地坚固我，使我不再冒犯他。",
    ["祈祷室", "院里"]))

# ---- Don Quixote, Part I, chapter 8 (1905 edition) ----
DQ = "El ingenioso hidalgo Don Quijote de la Mancha (1905)/Tomo I/Capítulo VIII"
sources["don-quixote"] = DQ
dq = blk(DQ, "n esto descubrieron treinta", "la piedra del molino.")
assert dq.startswith("n esto")
lines.append(Q("dq-1", "don-quixote", "es-criptana", "Part I, chapter 8", "上卷第八章", DQ,
    "E" + dq, ["treinta ó cuarenta molinos de viento"],
    "Just then they came in sight of thirty or forty windmills that there are on that plain, and as soon as Don Quixote "
    "saw them he said to his squire:\n'Fortune is guiding our affairs better than we could have wished; for look there, "
    "friend Sancho Panza, where thirty or more monstrous giants appear, with whom I mean to do battle and take all their "
    "lives, and with their spoils we shall begin to grow rich; for this is fair war, and it is a great service to God "
    "to sweep so evil a breed from the face of the earth.'\n'What giants?' said Sancho Panza.\n'Those you see there,' "
    "answered his master, 'with the long arms, for some of them are wont to have them almost two leagues long.'\n"
    "'Look, your worship,' answered Sancho, 'those that appear there are not giants but windmills, and what seem to be "
    "arms in them are the sails, which, turned by the wind, make the millstone go.'",
    ["thirty or forty windmills"],
    "这时，他们看见野地里有三四十架风车。堂吉诃德一看见，就对侍从说：\n“命运把我们的事安排得比我们希望的还好。你瞧，"
    "桑丘·潘沙朋友，那边出现了三十多个奇大无比的巨人，我要同他们交战，把他们统统杀死，用他们的战利品开始发家致富。"
    "这是正义的战争，把这些坏种从地面上扫除干净，也是为上帝立了大功。”\n“什么巨人？”桑丘·潘沙说。\n"
    "“就是你看见的那些，”他的主人回答，“胳膊长长的，有的胳膊差不多有两里瓦长。”\n“您瞧，”桑丘回答，"
    "“那边的不是巨人，是风车；那些像胳膊的东西是风车的翼子，被风一吹转起来，就带动磨石。”",
    ["三四十架风车"], " (the chapter's first letter, printed as a picture, restored)"))

# ---- Exemplary Novels: The Dialogue of the Dogs, opening (1825 edition) ----
COL = "El coloquio de los perros (1825)"
sources["novelas-ejemplares"] = COL
lines.append(Q("nov-1", "novelas-ejemplares", "es-cervantes-valladolid", "The Dialogue of the Dogs, opening",
    "《双狗对话》开篇", COL,
    blk(COL, "Novela y coloquio que pasó", "pasa de los términos de naturaleza."),
    ["Hospital de la Resurrección", "Valladolid"],
    "Novel and dialogue that passed between Cipión and Berganza, dogs of the Hospital of the Resurrection, which is in "
    "the City of Valladolid, outside the Puerta del Campo, and who are commonly called 'the dogs of Mahude'.\n"
    "CIPIÓN. Berganza, my friend, let us leave the Hospital tonight in the keeping of trust and withdraw to this quiet "
    "place, among these mats, where we can enjoy unnoticed this unheard-of favour that heaven has done the two of us at "
    "one and the same moment.\nBERGANZA. Brother Cipión, I hear you speak and I know that I am speaking to you, and I "
    "cannot believe it, for it seems to me that our speaking goes beyond the bounds of nature.",
    ["Hospital of the Resurrection", "Valladolid"],
    "西皮翁与贝尔甘萨之间的小说兼对话。这两条狗属于巴利亚多利德城坎波门外的复活医院，人们通常管它们叫“马乌德的狗”。\n"
    "西皮翁：贝尔甘萨朋友，今晚我们就把医院交给信任去看守，躲到这僻静地方、这些草席中间来吧，在这里我们可以不被人察觉，"
    "享受上天同时赐给我们俩的这份闻所未闻的恩典。\n贝尔甘萨：西皮翁兄弟，我听见你说话，也知道我在跟你说话，可我不敢相信，"
    "因为我觉得我们会说话，已经超出了自然的界限。",
    ["复活医院", "巴利亚多利德"]))

# ---- Fuenteovejuna, Act III ----
FOV = "Fuenteovejuna/Acto III"
sources["fuenteovejuna"] = FOV
lines.append(Q("fov-1", "fuenteovejuna", "es-fuente-obejuna", "Act III", "第三幕", FOV,
    spaced(blk(FOV, "ESTEBAN:       Déjenme un poco.", "Fuenteovejuna lo hizo.") + GAP
           + blk(FOV, "JUEZ:          Que os he de matar", "PASCUALA:      Fuenteovejuna, señor.")),
    ["Fuenteovejuna"],
    "ESTEBAN: Let me be a moment.\nJUDGE: I will.\nNow tell me: who killed Fernando?\nESTEBAN: Fuenteovejuna did it.\n"
    "…\nJUDGE: I'll kill you, believe me,\non this rack, you peasants.\nWho killed the Commander?\n"
    "PASCUALA: Fuenteovejuna, sir.",
    ["Fuenteovejuna"],
    "埃斯特万：让我歇一会儿。\n法官：好，让你歇。\n说吧：谁杀了费尔南多？\n埃斯特万：是羊泉村干的。\n…\n"
    "法官：相信我，我要让你们这些乡巴佬\n死在这刑架上。\n谁杀了骑士团长？\n帕斯夸拉：羊泉村，大人。",
    ["羊泉村"], SPACED))

# ---- The Knight of Olmedo, Act III ----
OLM = "El caballero de Olmedo/Acto III"
sources["caballero-de-olmedo"] = OLM
lines.append(Q("olm-1", "caballero-de-olmedo", "es-olmedo", "Act III", "第三幕", OLM,
    blk(OLM, "Que de noche le mataron", "la flor de Olmedo."), ["la flor de Olmedo"],
    "For by night they killed him,\nthe knight,\nthe pride of Medina,\nthe flower of Olmedo.",
    ["the flower of Olmedo"],
    "夜里他们杀了他，\n那位骑士，\n梅迪纳的骄傲，\n奥尔梅多之花。",
    ["奥尔梅多之花"]))

# ---- The Trickster of Seville, Act II ----
BUR = "El burlador de Sevilla/Acto II"
sources["burlador-de-sevilla"] = BUR
lines.append(Q("bur-1", "burlador-de-sevilla", "es-sevilla", "Act II", "第二幕", BUR,
    unindent(blk(BUR, "Sevilla a voces me llama", "y dejarla sin honor.")), ["Sevilla"],
    "Seville cries me out by name\nthe Trickster, and the greatest\npleasure there can be for me\nis to trick a woman\n"
    "and leave her without honour.",
    ["Seville"],
    "整个塞维利亚都大声叫我\n“骗子”，而我最大的\n乐趣，就是\n骗一个女人，\n让她名誉扫地。",
    ["塞维利亚"], " (the edition's verse indent left out)"))

# ---- The Swindler, Book I, chapter 1 ----
BUS = "Historia de la vida del Buscón/Libro Primero: Capítulo I"
sources["el-buscon"] = BUS
lines.append(Q("bus-1", "el-buscon", "es-segovia", "Book I, chapter 1", "第一卷第一章", BUS,
    cut(BUS, "Yo, señora, soy de Segovia.", "sastre de barbas."), ["Segovia"],
    "I, madam, am from Segovia. My father was called Clemente Pablo, a native of the same town; God keep him in heaven. "
    "He was, as everyone says, a barber by trade, though his thoughts ran so high that he was ashamed to be called that, "
    "saying he was a shearer of cheeks and a tailor of beards.",
    ["Segovia"],
    "夫人，我是塞哥维亚人。我父亲叫克莱门特·巴勃罗，也是本地人，愿上帝让他在天堂安息。正如大家所说，他的营生是剃头匠，"
    "不过他心气极高，被人这么叫就觉得丢脸，说自己是“脸颊的剪毛匠、胡子的裁缝”。",
    ["塞哥维亚"]))

# ---- The Mayor of Zalamea, Act III ----
ZAL = "El alcalde de Zalamea/Jornada Tercera"
sources["alcalde-de-zalamea"] = ZAL
lines.append(Q("zal-1", "alcalde-de-zalamea", "es-zalamea", "Act III", "第三幕", ZAL,
    blk(ZAL, "CRESPO: Mirad que echado en el suelo", "de guerra enviará por mí."), ["Zalamea"],
    "CRESPO: See, flung on the ground,\nI beg you aloud for my honour.\nÁLVARO: What a nuisance!\nCRESPO: See, I am\n"
    "mayor in Zalamea today.\nÁLVARO: Over me you have never had\njurisdiction. The council\nof war will send for me.",
    ["Zalamea"],
    "克雷斯波：您看，我跪倒在地，\n高声求您还我名誉。\n阿尔瓦罗：真烦人！\n克雷斯波：您看，我今天\n是萨拉梅亚的镇长。\n"
    "阿尔瓦罗：你对我从来没有\n管辖权。军事法庭\n会派人来提我的。",
    ["萨拉梅亚"], " ('Es consejo' as printed, for 'El consejo')"))

# ---- The Maidens' Consent, Act I, scene 1 (1830 edition) ----
SDN = "El sí de las niñas (1830)/Acto primero"
sources["si-de-las-ninas"] = SDN
lines.append(Q("sdn-1", "si-de-las-ninas", "es-alcala", "Act I, scene 1 (the inn at Alcalá)", "第一幕第一场（阿尔卡拉的客栈）",
    SDN, joined(blk(SDN, "SIMÓN.\nEllo también ha sido", "un instante de quietud.")), ["la posada"],
    "SIMÓN. It was a strange decision, too, for you to stay two whole days without leaving the inn. One gets tired of "
    "reading, tired of sleeping... And above all, tired of the grime of the room, the rickety chairs, the prints of the "
    "Prodigal Son, the noise of handbells and harness bells, and the hoarse talk of carters and yokels, which never "
    "allows a moment's peace.",
    ["the inn"],
    "西蒙：您这一回也真是古怪，整整两天待在客栈里不出门。读书读累了，睡觉睡累了……最累人的是房间里的油垢、"
    "东倒西歪的椅子、画着浪子回头的版画，还有铃铛和马铃的叮当声，车夫和乡巴佬粗哑的说话声，叫人片刻不得安宁。",
    ["客栈"], JOINED))

# ---- Don Álvaro, or the Force of Fate, Act V, last scene ----
ALV = "Don Álvaro o La fuerza del sino/Jornada quinta"
sources["don-alvaro"] = ALV
lines.append(Q("alv-1", "don-alvaro", "es-hornachuelos", "Act V, last scene", "第五幕末场", ALV,
    blk(ALV, "DON ÁLVARO\n(Desde un risco", "y se precipita.)"), ["Desde un risco", "lo más alto del monte"],
    "DON ÁLVARO\n(From a crag, with a diabolical smile, convulsed all over, he says:)\nLook for Father Rafael, you "
    "fool...\nI am an envoy from hell,\nI am the destroying demon...\nFlee, you wretches.\nALL\nJesus, Jesus!\n"
    "DON ÁLVARO\nHell, open your mouth and swallow me.\nLet heaven fall, let the human race perish;\nextermination, "
    "destruction...\n(He climbs to the highest point of the mountain and throws himself off.)",
    ["From a crag", "the highest point of the mountain"],
    "唐阿尔瓦罗\n（站在一块岩石上，脸上带着魔鬼般的笑，浑身抽搐，说：）\n去找拉斐尔神父吧，蠢货……\n我是地狱派来的使者，\n"
    "我是灭绝一切的魔鬼……\n逃命吧，可怜虫们。\n众人\n耶稣啊，耶稣！\n唐阿尔瓦罗\n地狱啊，张开你的嘴，把我吞下去。\n"
    "让天塌下来，让人类灭亡；\n毁灭，摧毁……\n（他爬上山的最高处，纵身跳下。）",
    ["站在一块岩石上", "山的最高处"]))

# ---- Don Juan Tenorio, Part I, Act I, scene 8 (1844 edition) ----
TEN = "Don Juan Tenorio (1844)/1"
sources["don-juan-tenorio"] = TEN
lines.append(Q("ten-1", "don-juan-tenorio", "es-hosteria-laurel", "Part I, Act I, scene 8", "第一部第一幕第八场", TEN,
    blk(TEN, "DIEGO.\n¿La hostería del Laurel?", "BUTT.\nYo."), ["La hostería del Laurel"],
    "DIEGO.\nThe Laurel inn?\nBUTT.\nYou are in it, sir.\nDIEGO.\nIs the innkeeper at home?\nBUTT.\nYou are speaking to "
    "him.\nDIEGO.\nAre you Buttarelli?\nBUTT.\nI am.",
    ["The Laurel inn"],
    "迭戈\n是月桂客栈吗？\n布塔雷利\n您正在里头，先生。\n迭戈\n店主在家吗？\n布塔雷利\n您正在跟他说话。\n迭戈\n"
    "您就是布塔雷利？\n布塔雷利\n正是。",
    ["月桂客栈"]))

# ---- Rhymes and Legends: The Mount of Souls ----
MON = "El monte de las ánimas"
sources["rimas-y-leyendas"] = MON
mon = cut(MON, "—Ese monte que hoy llaman", "religiosos á la vez.")
assert "á ios Templarios" in mon
lines.append(Q("ryl-1", "rimas-y-leyendas", "es-san-juan-duero", "Legend: The Mount of Souls", "传说《亡魂山》", MON,
    mon.replace("á ios Templarios", "á los Templarios"), ["monte que hoy llaman de las Ánimas"],
    "'That mountain they now call the Mount of Souls belonged to the Templars, whose monastery you see there on the bank "
    "of the river. The Templars were warriors and monks at once.'",
    ["the Mount of Souls"],
    "“那座如今叫做亡魂山的山，从前属于圣殿骑士团，他们的修道院你看就在那边河岸上。圣殿骑士既是武士，又是修士。”",
    ["亡魂山"], " ('ios', a misread 'los', corrected)"))

# ---- Pepita Jiménez, the first letter ----
PEP = "Pepita Jiménez/Capítulo I"
sources["pepita-jimenez"] = PEP
lines.append(Q("pep-1", "pepita-jimenez", "es-cabra", "Part I, letter of 22 March", "第一部，3 月 22 日的信", PEP,
    cut(PEP, "Querido tío y venerado maestro:", "amigos y parientes.") + GAP
    + cut(PEP, "Como salí de aquí tan niño", "sobre todo, son deliciosas."), ["este lugar de mi nacimiento"],
    "Dear uncle and revered master: Four days ago I arrived safe and well in this place where I was born, and found my "
    "father, the vicar, and my friends and relations in good health.\n…\nAs I left here so young and have come back a "
    "man, all these things I kept in my memory make a strange impression on me. Everything seems smaller to me, much "
    "smaller, but also prettier than I remembered it. My father's house, which in my imagination was immense, is no "
    "doubt a large house for a rich farmer, but smaller than the Seminary. What I now understand and value more is the "
    "countryside round here. The orchards above all are delightful.",
    ["this place where I was born"],
    "亲爱的叔叔、可敬的老师：四天前我平安回到了我出生的这个地方，父亲、副本堂神父和亲友们都身体安好。\n…\n"
    "我离开这里时还那么小，如今长大成人回来，记忆中保存的这一切东西给我一种奇特的感觉。一切都显得小了，小了许多，"
    "却也比记忆中更美。父亲的房子在我想象里大得无边，其实不过是个富裕农户的大宅，比神学院小。我现在更懂得、"
    "也更珍惜的是这一带的田野。尤其是那些果园，真是可爱极了。",
    ["我出生的这个地方"]))

# ---- Trafalgar, chapter 1 ----
TRA = "Trafalgar/1"
sources["trafalgar-galdos"] = TRA
lines.append(Q("tra-1", "trafalgar-galdos", "es-trafalgar", "Chapter 1", "第一章", TRA,
    joined(blk(TRA, "A este sentimiento consagré", "para que sea verdadero.")), ["Trafalgar"],
    "To this feeling I devoted my manhood, and to it I devote this labour of my last years, setting it as the guardian "
    "spirit or angel of my written life, since it was that of my real one. I have many things to tell. Trafalgar, "
    "Bailén, Madrid, Zaragoza, Gerona, Arapiles!... Of all this I shall say something, if your patience does not fail. "
    "My story will not be as fine as it should be, but I shall do all I can to make it true.",
    ["Trafalgar"],
    "我把壮年献给了这种感情，如今又把晚年的这份工作献给它，让它做我这部笔下人生的守护神或护卫天使，"
    "因为它也曾是我真实人生的守护者。我要讲的事情很多。特拉法尔加、拜伦、马德里、萨拉戈萨、赫罗纳、阿拉皮莱斯！……"
    "这一切我都要讲一些，只要你们有耐心。我的叙述不会像应有的那样美，但我会尽力让它真实。",
    ["特拉法尔加"], JOINED.replace("speech", "paragraph")))

# ---- Fortunata and Jacinta, Part I, chapter 3 ----
FY3, FY4 = "Fortunata y Jacinta: 1.03.03", "Fortunata y Jacinta: 1.03.04"
sources["fortunata-y-jacinta"] = FY3
lines.append(Q("fyj-1", "fortunata-y-jacinta", "es-cava-san-miguel", "Part I, chapter 3, section 3", "第一部第三章第三节",
    FY3, cut(FY3, "Vivía Plácido en la Cava de San Miguel.", "otra cosa de su domicilio."), ["Cava de San Miguel"],
    "Plácido lived in the Cava de San Miguel. His house was one of those that form the western side of the Plaza Mayor, "
    "and as their foundations lie much lower than the level of the square, they are of imposing height, with formidable "
    "buttresses, like a fortress. The flat he lived in was the fourth floor on the Plaza side and the seventh on the "
    "Cava side. There are no greater heights in Madrid, and to overcome them one had to tackle a hundred and twenty "
    "steps, all of stone, as Plácido said with pride, having nothing else to boast of in his home.",
    ["Cava de San Miguel"],
    "普拉西多住在圣米格尔坑道街。他的房子是构成马约尔广场西侧的那排房子之一；这些房子的地基比广场地面低得多，"
    "所以高得吓人，墙基又粗又厚，像座堡垒。他住的那一层，从广场这边算是四楼，从坑道街那边算是七楼。马德里再没有比这更高的楼了；"
    "要爬上去，得硬着头皮走一百二十级台阶，“全是石头的”，普拉西多骄傲地说，因为他的住处再没有别的可夸了。",
    ["圣米格尔坑道街"]))
lines.append(Q("fyj-2", "fortunata-y-jacinta", "es-cava-san-miguel", "Part I, chapter 3, section 4", "第一部第三章第四节",
    FY4, blk(FY4, "-¿Vive aquí -le preguntó- el Sr. de Estupiñá?", "-¡Un huevo crudo!"), ["en lo más último de arriba"],
    "'Does Señor Estupiñá live here?' he asked her.\n'Don Plácido?... right at the very top,' the girl answered, taking "
    "a few steps out.\nAnd Juanito thought: 'You're coming out so I'll see your foot. A fine boot'... Thinking this, he "
    "noticed that the girl drew from her shawl a hand in a red mitten and raised it to her mouth. The young Santa Cruz's "
    "familiarity overflowed his chest, and he could not help saying:\n'What are you eating, child?'\n'Can't you see?' "
    "she retorted, showing it to him. 'An egg.'\n'A raw egg!'",
    ["right at the very top"],
    "“埃斯图皮尼亚先生住在这儿吗？”他问她。\n“唐普拉西多？……在最顶上那层，”姑娘答道，一边往外走了几步。\n"
    "胡安尼托心想：“你走出来，是要让我看你的脚。好一双靴子。”……这么想着，他发觉姑娘从披肩里伸出一只戴红色露指手套的手，"
    "送到嘴边。年轻的圣克鲁斯心里的随便劲儿再也按捺不住，忍不住说：\n“你在吃什么呀，小家伙？”\n"
    "“您没看见吗？”她把东西亮给他看，“一个鸡蛋。”\n“一个生鸡蛋！”",
    ["最顶上那层"]))

# ---- La Regenta, chapter 1 ----
REG = "La Regenta/Capítulo I"
sources["la-regenta"] = REG
lines.append(Q("reg-1", "la-regenta", "es-oviedo-cathedral", "Chapter 1", "第一章", REG,
    cut(REG, "La heroica ciudad dormía la siesta.", "al correr hacia el Norte.") + GAP
    + cut(REG, "Vetusta, la muy noble y leal ciudad", "en la Santa Basílica."),
    ["la esbelta torre en la Santa Basílica"],
    "The heroic city was taking its siesta. The south wind, hot and lazy, pushed along the whitish clouds, which tore "
    "apart as they ran north.\n…\nVetusta, the most noble and loyal city, a royal court in a distant century, was "
    "digesting its stew and its olla podrida, and resting as it listened, half asleep, to the monotonous and familiar "
    "hum of the choir bell, which boomed high up in the slender tower of the Holy Basilica.",
    ["the slender tower of the Holy Basilica"],
    "英雄的城市正在午睡。南风又热又懒，推着灰白的云朵，云朵往北跑着跑着就撕裂了。\n…\n维图斯塔，这座极高贵、"
    "极忠诚的城市，遥远的某个世纪里曾是宫廷所在，此刻正在消化炖菜和杂烩锅，半睡半醒地听着唱诗钟那单调而熟悉的嗡嗡声，"
    "那钟声在圣殿主教座堂细长的塔楼高处回荡。",
    ["圣殿主教座堂细长的塔楼"]))

# ---- Midsummer Madness (Insolación), chapter 4 ----
INS = "Insolación/04"
sources["insolacion"] = INS
lines.append(Q("ins-1", "insolacion", "es-san-isidro", "Chapter 4", "第四章", INS,
    blk(INS, "Don Diego, que en el coche", "hasta que me cuadré."), ["San Isidro"],
    "Don Diego, who in the carriage had seemed to me reserved and rather glum, became very talkative once we were "
    "walking about San Isidro, living up to his name for charm. Holding my arm firmly so that the tides of people would "
    "not separate us, he missed nothing, and every detail of the famous stalls gave him an excuse for a joke, which "
    "often was one only by virtue of the tone and accent he said it in; for it is certain that if the sayings of "
    "Andalusians were written down they would not be half as funny as they sound on their lips: to the lilt, the little "
    "lisp and the quickness of reply is owed most of their wit.\nThe worst of it was that, as there were no respectable "
    "people there but ourselves, and Pacheco took on everyone and gave everyone rope, we were surrounded by a rabble of "
    "beggars, freaks, ragged children, gypsy women, fritter-sellers and hawkers. My companion's impulse was to buy "
    "everything he saw, from scapulars to water jugs, until I put my foot down.",
    ["San Isidro"],
    "唐迭戈在马车里显得拘谨、有点闷闷不乐，可我们一走进圣伊西德罗，他就变得妙语连珠，不愧是出了名的有趣人。"
    "他紧紧挽着我的胳膊，免得人潮把我们冲散，什么也不放过，那些出名的货棚每一处细节都能让他找到由头说个笑话。"
    "其实很多笑话之所以好笑，全凭他说话的腔调和口音；因为可以肯定，安达卢西亚人的妙语要是写下来，连说出口时一半的趣味都没有："
    "他们的风趣，大半来自那抑扬的语调、那一点点咬舌音和应答的敏捷。\n最糟的是，那里除了我们俩再没有体面人，"
    "而帕切科又跟谁都搭话、跟谁都逗乐，于是一群乞丐、畸形人、衣衫褴褛的孩子、吉卜赛女人、卖油炸饼的和小贩把我们团团围住。"
    "我的同伴见什么就想买什么，从护身圣牌到水罐，直到我坚决拦住了他。",
    ["圣伊西德罗"]))

# ---- The Cabin (La barraca), chapter 4 ----
BAR = "La barraca/IV"
sources["la-barraca"] = BAR
lines.append(Q("bar-1", "la-barraca", "es-tribunal-aguas", "Chapter 4", "第四章", BAR,
    blk(BAR, "Era jueves, y, según una costumbre", "faldas de indiana de colores oscuros."),
    ["el Tribunal de las Aguas", "la puerta de los Apóstoles"],
    "It was Thursday, and, by a custom that went back centuries, the Water Tribunal was about to sit at the Apostles' "
    "Door of Valencia Cathedral.\nThe clock on the tower called the Miguelete showed a little after ten, and the farmers "
    "of the huerta gathered in knots or sat on the rim of the basin of the fountain that adorns the square, forming "
    "round the bowl a lively garland of blue and white blankets, red and yellow kerchiefs, and dark-coloured print "
    "skirts.",
    ["the Water Tribunal", "the Apostles' Door"],
    "那天是星期四，按照沿袭了几百年的老规矩，水法庭要在瓦伦西亚大教堂的使徒门前开庭。\n那座叫做米格莱特的钟楼上，"
    "时钟刚过十点，菜农们三五成群地聚着，或者坐在装点广场的那座喷泉的池沿上，在水池四周围成一圈热闹的花环："
    "蓝白两色的毯子，红黄两色的头巾，深色的印花布裙子。",
    ["水法庭", "使徒门"]))

# ---- Reeds and Mud, chapter 1 ----
CYB = "Cañas y barro/I"
sources["canas-y-barro"] = CYB
lines.append(Q("cyb-1", "canas-y-barro", "es-el-palmar", "Chapter 1, opening", "第一章开篇", CYB,
    blk(CYB, "Como todas las tardes, la barca-correo", "una isla de cañas y barro."),
    ["al Palmar", "una isla de cañas y barro"],
    "As every afternoon, the mail boat announced its arrival at El Palmar with several blasts of its horn.\nThe "
    "boatman, a scrawny little man with one ear cut off, went from door to door taking orders for Valencia, and on "
    "reaching the open spaces in the village's only street he blew his horn again to let the cabins scattered along "
    "the edge of the canal know he was there. A swarm of almost naked urchins followed the boatman with a certain "
    "admiration. They were awed by the man who crossed the Albufera four times a day, taking the best fish of the lake "
    "to Valencia and bringing back from there the thousand things of a city that was mysterious and fantastic to those "
    "little ones raised on an island of reeds and mud.",
    ["El Palmar", "an island of reeds and mud"],
    "像每天下午一样，邮船吹响几声号角，宣告它到了帕尔马尔。\n船夫是个干瘦的小个子，缺了一只耳朵。他挨家挨户地收捎往瓦伦西亚的东西，"
    "走到村里唯一那条街的空地上，又吹起号角，告诉散落在水渠边上的茅屋他来了。一群几乎光着身子的孩子带着几分崇拜跟在船夫后面。"
    "他们敬畏这个一天四趟渡过阿尔武费拉湖的人：他把湖里最好的鱼送到瓦伦西亚，又从那里带回千百样东西；"
    "对这些在芦苇与泥沼之岛上长大的小家伙来说，那是一座神秘而奇幻的城市。",
    ["帕尔马尔", "芦苇与泥沼之岛"]))

# ---- Fields of Castile: 'To a Dry Elm' ----
OLMO = "A un olmo seco"
sources["campos-de-castilla"] = OLMO
lines.append(Q("cdc-1", "campos-de-castilla", "es-espino-soria", "'To a Dry Elm', lines 1–8", "《致一棵枯榆》第 1–8 行",
    OLMO, blk(OLMO, "Al olmo viejo, hendido por el rayo", "carcomido y polvoriento."),
    ["El olmo centenario en la colina", "que lame el Duero"],
    "On the old elm, split by lightning\nand half rotten,\nwith the April rains and the May sun\na few green leaves have "
    "come out.\nThe hundred-year-old elm on the hill\nthat the Duero laps! A yellowish moss\nstains its whitish bark,\n"
    "the trunk worm-eaten and dusty.",
    ["The hundred-year-old elm on the hill", "that the Duero laps"],
    "这棵老榆树，被雷电劈开，\n一半已经朽烂，\n四月的雨，五月的阳光，\n竟让它长出了几片绿叶。\n这棵百年老榆，长在\n"
    "杜埃罗河轻舔的山冈上！一层黄苔\n沾污了它灰白的树皮，\n那树干已被虫蛀，蒙满尘土。",
    ["百年老榆", "杜埃罗河轻舔的山冈"]))

# ---- Mist (Niebla), chapter 31 ----
NIE = "Niebla/XXXI"
sources["niebla"] = NIE
lines.append(Q("nie-1", "niebla", "es-unamuno-house", "Chapter 31", "第三十一章", NIE,
    blk(NIE, "Emprendió, pues, un viaje acá", "se sentó, frente a mí."), ["Salamanca", "mi despacho-librería"],
    "So he set out on a journey here, to Salamanca, where I have lived for more than twenty years, to visit me.\nWhen "
    "his visit was announced I smiled enigmatically and had him shown into my study-library. He came in like a ghost, "
    "looked at an oil portrait of me that presides there over the books of my library, and at a sign from me sat down, "
    "facing me.",
    ["Salamanca", "my study-library"],
    "于是他启程来到这里，来到萨拉曼卡——我在这里已经住了二十多年——来拜访我。\n听说他来访，我神秘地一笑，"
    "叫人领他到我的书房兼藏书室。他像个幽灵似的走进来，看了一眼那幅挂在那里、俯视着我满屋藏书的我的油画肖像，"
    "然后在我示意下，在我对面坐下。",
    ["萨拉曼卡", "书房兼藏书室"]))

# ---- Saint Manuel Bueno, Martyr ----
SMB = "San Manuel Bueno, mártir"
sources["san-manuel-bueno"] = SMB
lines.append(Q("smb-1", "san-manuel-bueno", "es-sanabria", "Ángela comes home", "安赫拉回到村里", SMB,
    cut(SMB, "Pasé en el colegio unos cinco años", "el sendero de mi vida."),
    ["Valverde de Lucerna", "con el lago y con la montaña"],
    "I spent some five years at the school, which now fade from me like a dream at dawn in the distance of memory, and "
    "at fifteen I came back to my Valverde de Lucerna. By then it was all Don Manuel; Don Manuel with the lake and with "
    "the mountain. I arrived eager to know him, to put myself under his protection, for him to mark out the path of my "
    "life.",
    ["Valverde de Lucerna", "with the lake and with the mountain"],
    "我在寄宿学校待了大约五年，如今那几年在记忆的远处，像黎明时的一个梦一样渐渐模糊。十五岁那年，我回到了我的巴尔韦德-德卢塞尔纳。"
    "那时，整个村子已经全是堂曼努埃尔了；堂曼努埃尔和湖，和山。我满心渴望认识他，投到他的庇护之下，请他为我指出人生的道路。",
    ["巴尔韦德-德卢塞尔纳", "和湖，和山"]))

# ---- Bohemian Lights, scene 12 ----
LUB = "Luces de bohemia/Escena duodécima"
sources["luces-de-bohemia"] = LUB
lines.append(Q("lub-1", "luces-de-bohemia", "es-callejon-gato", "Scene 12", "第十二场", LUB,
    blk(LUB, "MAX: Los ultraístas son unos farsantes.", "sistemáticamente deformada."), ["el callejón del Gato"],
    "MAX: The ultraists are a bunch of frauds. Esperpentism was invented by Goya. The classical heroes have gone for a "
    "stroll in the Callejón del Gato.\nDON LATINO: You're completely sozzled!\nMAX: The classical heroes reflected in "
    "concave mirrors give the Esperpento. The tragic sense of Spanish life can only be rendered through a "
    "systematically deformed aesthetic.",
    ["the Callejón del Gato"],
    "马克斯：极端主义者都是些骗子。荒诞剧是戈雅发明的。古典英雄们都跑到猫巷去散步了。\n唐拉蒂诺：你完全喝醉了！\n"
    "马克斯：古典英雄映在凹面镜里，就成了荒诞剧。西班牙生活的悲剧意味，只有用一种系统地变形的美学才能表现出来。",
    ["猫巷"]))

# ---- The House of Bernarda Alba, Act I ----
CBA = "La casa de Bernarda Alba/Acto I"
sources["casa-de-bernarda-alba"] = CBA
lines.append(Q("cba-1", "casa-de-bernarda-alba", "es-valderrubio", "Act I", "第一幕", CBA,
    cut(CBA, "Bernarda: Pues busca otro", "en casa de mi abuelo."), ["esta casa"],
    "Bernarda: Then find another, for you'll need it. In the eight years the mourning lasts, no wind from the street is "
    "to come into this house. Think of it as if we had bricked up the doors and windows. That is how it was in my "
    "father's house and in my grandfather's.",
    ["this house"],
    "贝尔纳达：那就去另找一把，你会用得着的。守丧的这八年里，街上的风不许吹进这个家。你们就当我们已经用砖把门窗都砌死了。"
    "我父亲家是这样，我祖父家也是这样。",
    ["这个家"]))

# ---- Homage to Catalonia, chapter 10 (English original; Project Gutenberg Australia) ----
HTC_URL = "https://gutenberg.net.au/ebooks02/0201111h.html"
htc_en = ("Immediately opposite there was a cinematograph, called the Poliorama, with a museum above it, and at the top, "
          "high above the general level of the roofs, a small observatory with twin domes. The domes commanded the "
          "street, and a few men posted up there with rifles could prevent any attack on the P.O.U.M. buildings.")
htc_zh = ("正对面是一家电影院，叫波利奥拉玛，楼上是一座博物馆，顶上高出周围一片屋顶的地方，有一座带两个圆顶的小天文台。"
          "这两个圆顶俯瞰着整条街，派几个人带着步枪守在上面，就能挡住对马统工党大楼的任何进攻。")
assert "Poliorama" in htc_en and "波利奥拉玛" in htc_zh
lines.append(dict(id="htc-1", book_id="homage-to-catalonia", place_ids=["es-poliorama"], location="Chapter 10",
    location_zh="第十章", text_en=htc_en, highlight_en=["Poliorama"], text_zh=htc_zh, highlight_zh=["波利奥拉玛"],
    translation="original", status="draft",
    checked=f"Project Gutenberg Australia eBook 0201111h, chapter 10, {DATE}"))

# ---------- write ----------
replaced = {"cantar-de-mio-cid": ["cid-s1"], "libro-de-buen-amor": ["lba-s1"], "conde-lucanor": ["luc-s1"],
            "la-celestina": ["cel-s1"], "lazarillo-de-tormes": ["laz-s1"], "libro-de-la-vida": ["vida-s1"],
            "don-quixote": ["dq-s1"], "novelas-ejemplares": ["nov-s1"], "fuenteovejuna": ["fov-s1"],
            "caballero-de-olmedo": ["olm-s1"], "burlador-de-sevilla": ["bur-s1"], "el-buscon": ["bus-s1"],
            "alcalde-de-zalamea": ["zal-s1"], "si-de-las-ninas": ["sdn-s1"], "don-alvaro": ["alv-s1"],
            "don-juan-tenorio": ["ten-s1"], "rimas-y-leyendas": ["ryl-s1"], "pepita-jimenez": ["pep-s1"],
            "trafalgar-galdos": ["tra-s1"], "fortunata-y-jacinta": ["fyj-s1"], "la-regenta": ["reg-s1"],
            "insolacion": ["ins-s1"], "la-barraca": ["bar-s1"], "canas-y-barro": ["cyb-s1"],
            "campos-de-castilla": ["cdc-s1"], "niebla": ["nie-s1"], "san-manuel-bueno": ["smb-s1"],
            "luces-de-bohemia": ["lub-s1"], "casa-de-bernarda-alba": ["cba-s1"], "homage-to-catalonia": ["htc-s1"]}
assert set(replaced) == {l["book_id"] for l in lines} == set(sources) | {"homage-to-catalonia"}
lp = b.data("lines.js")
existing = set(re.findall(r'  \{ id: "([^"]+)"', open(lp, encoding="utf-8").read()))
assert not ({l["id"] for l in lines} & existing), "ids already in use"
drop_entries(lp, {i for v in replaced.values() for i in v})
b.append(lp, lines, "11-22 quotations from Spanish Wikisource (and Homage to Catalonia from Project Gutenberg Australia), "
                    "replacing the placeholder scene notes (add_es3.py)")
for bid, title in sources.items():
    set_source(b.data("books.js"), bid, ws.url("es", title))
set_source(b.data("books.js"), "homage-to-catalonia", HTC_URL)
print(len(lines), "quotations for", len(replaced), "books;", sum(map(len, replaced.values())), "scene notes replaced")
