"""11-18: Greece, first pack (ancient works). Books chosen with the scoring rubric (sel/gr: Britannica's Great Books of the Western
World, the bookpress.gr / Politeia list of the 100 best books of modern Greek literature, Goodreads, the gymnasium curriculum,
Bokklubben and thegreatestbooks.org), plus the user's additions (second pack).
Gutenberg is down, so every book gets scene notes for now; the ancient texts can take quotations from public-domain translations later.
Coordinates come from Commons categories or geotagged Commons photos (coords_gr.json).
Usage: python3 -I add_gr1.py <app_dir> <coords_gr.json>"""
import json, os, sys
sys.path.insert(0, __file__.rsplit("/", 2)[0])
import batchlib as b
APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
b.init(APP, "", "gr", "2026-11-18")
W = b.W

def BK(id, title, title_zh, title_orig, author, author_zh, author_orig, year, pd=True, **kw):
    d = dict(id=id, title=title, title_zh=title_zh, author=author, author_zh=author_zh, year=year,
             orig_lang=kw.pop("lang", "grc"), public_domain=pd, source_url=None)
    if title_orig:
        d["title_orig"] = title_orig
    if author_orig:
        d["author_orig"] = author_orig
    d.update(kw)
    return d

def C(pid):
    c = CO[pid]
    return c["lat"], c["lon"], c["st"], c["su"]

def ORIG(pid, name, zh, en_note, zh_note, **kw): return b.ORIG(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PROTO(pid, name, zh, en_note, zh_note, **kw): return b.PROTO(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PIL(pid, name, zh, en_note, zh_note, ids, **kw): return b.PIL(pid, name, zh, *C(pid), en_note, zh_note, ids, **kw)
def FILM(pid, name, zh, adaptation, scene_en, scene_zh, ids, **kw):
    return b.P(pid, name, zh, *C(pid), "film_location", adaptation=adaptation, scene=scene_zh, scene_en=scene_en, book_ids=ids, **kw)
S = b.S

AESCH = ("Aeschylus", "埃斯库罗斯", "Αἰσχύλος")
SOPH = ("Sophocles", "索福克勒斯", "Σοφοκλῆς")
EUR = ("Euripides", "欧里庇得斯", "Εὐριπίδης")
ARIST = ("Aristophanes", "阿里斯托芬", "Ἀριστοφάνης")
PLATO = ("Plato", "柏拉图", "Πλάτων")

books = [
    BK("odyssey", "The Odyssey", "奥德赛", "Ὀδύσσεια", "Homer", "荷马", "Ὅμηρος", "c. 8th c. BC",
       aliases=["Odysseus", "Ulysses", "Penelope", "Telemachus", "Ithaca", "奥德修斯", "珀涅罗珀", "伊萨卡"]),
    BK("oresteia", "The Oresteia", "俄瑞斯忒亚", "Ὀρέστεια", *AESCH, "458 BC",
       aliases=["Agamemnon", "The Libation Bearers", "The Eumenides", "Clytemnestra", "Orestes", "阿伽门农", "复仇女神"]),
    BK("seven-thebes", "Seven Against Thebes", "七将攻忒拜", "Ἑπτὰ ἐπὶ Θήβας", *AESCH, "467 BC", aliases=["Eteocles", "Polynices", "厄忒俄克勒斯"]),
    BK("oedipus-rex", "Oedipus Rex", "俄狄浦斯王", "Οἰδίπους Τύραννος", *SOPH, "c. 429 BC",
       aliases=["Oedipus the King", "Oedipus Tyrannus", "Jocasta", "Tiresias", "伊俄卡斯忒"]),
    BK("antigone", "Antigone", "安提戈涅", "Ἀντιγόνη", *SOPH, "c. 441 BC", aliases=["Creon", "Ismene", "Polynices", "克瑞翁"]),
    BK("oedipus-colonus", "Oedipus at Colonus", "俄狄浦斯在科罗诺斯", "Οἰδίπους ἐπὶ Κολωνῷ", *SOPH, "401 BC", aliases=["Theseus", "忒修斯"]),
    BK("medea", "Medea", "美狄亚", "Μήδεια", *EUR, "431 BC", aliases=["Jason", "伊阿宋"]),
    BK("bacchae", "The Bacchae", "酒神的伴侣", "Βάκχαι", *EUR, "405 BC", aliases=["Dionysus", "Pentheus", "Agave", "狄俄尼索斯", "彭透斯"]),
    BK("iphigenia-aulis", "Iphigenia in Aulis", "伊菲革涅亚在奥利斯", "Ἰφιγένεια ἐν Αὐλίδι", *EUR, "405 BC", aliases=["Iphigenia", "Agamemnon", "Aulis"]),
    BK("lysistrata", "Lysistrata", "吕西斯特拉忒", "Λυσιστράτη", *ARIST, "411 BC", aliases=["Lampito", "Acropolis"]),
    BK("clouds", "The Clouds", "云", "Νεφέλαι", *ARIST, "423 BC", aliases=["Strepsiades", "Socrates", "Thinkery", "思想所"]),
    BK("histories", "The Histories", "历史", "Ἱστορίαι", "Herodotus", "希罗多德", "Ἡρόδοτος", "c. 430 BC",
       aliases=["Leonidas", "Thermopylae", "Marathon", "Salamis", "Xerxes", "列奥尼达", "温泉关", "薛西斯"]),
    BK("thucydides", "History of the Peloponnesian War", "伯罗奔尼撒战争史", "Ἱστορίαι", "Thucydides", "修昔底德", "Θουκυδίδης", "c. 400 BC",
       aliases=["Pericles' Funeral Oration", "Melian Dialogue", "伯里克利葬礼演说", "米洛斯对话"]),
    BK("socrates", "The Trial and Death of Socrates", "苏格拉底的审判与死亡", "Ἀπολογία Σωκράτους · Κρίτων · Φαίδων", *PLATO, "c. 399–360 BC",
       aliases=["Apology", "Crito", "Phaedo", "Socrates", "苏格拉底的申辩", "克里托", "斐多"]),
    BK("symposium", "The Symposium", "会饮篇", "Συμπόσιον", *PLATO, "c. 385 BC", aliases=["Agathon", "Alcibiades", "Diotima", "Eros", "阿伽松", "阿尔基比亚德"]),
    BK("republic", "The Republic", "理想国", "Πολιτεία", *PLATO, "c. 375 BC", aliases=["Allegory of the Cave", "Cephalus", "洞穴寓言"]),
    BK("ethics", "The Nicomachean Ethics", "尼各马可伦理学", "Ἠθικὰ Νικομάχεια", "Aristotle", "亚里士多德", "Ἀριστοτέλης", "c. 340 BC",
       aliases=["Lyceum", "Peripatetic", "eudaimonia", "吕克昂"]),
    BK("plutarch", "Parallel Lives", "希腊罗马名人传", "Βίοι Παράλληλοι", "Plutarch", "普鲁塔克", "Πλούταρχος", "c. 100",
       aliases=["Plutarch's Lives", "Lives of the Noble Greeks and Romans", "希腊罗马名人传"]),
    BK("sappho", "Poems and Fragments", "萨福诗集", None, "Sappho", "萨福", "Σαπφώ", "c. 600 BC",
       aliases=["If Not, Winter", "Ode to Aphrodite", "Lesbos", "莱斯博斯"]),
]

places = [
    ORIG("gr-ithaca", "Vathy, Ithaca", "伊萨卡岛 · 瓦西", "The small Ionian island that Homer made Odysseus's home and the goal of his ten-year voyage. Scholars still argue whether Homer's Ithaca is the island that bears the name today, but its harbour town of Vathy, the Cave of the Nymphs and the hill-top ruins are visited as his. Cavafy's poem Ithaka tells the traveller to hope the road is long. Ferries run from Kefalonia",
         "伊奥尼亚海上的小岛，荷马让奥德修斯以这里为家，他十年漂泊的终点就是这里。学者至今争论荷马的伊萨卡是不是今天这座同名的岛，但港镇瓦西、宁芙洞和山顶遗址都被当作他的故地来参观。卡瓦菲斯的诗《伊萨卡》劝旅人盼望路途漫长。从凯法利尼亚岛有渡船过来"),
    ORIG("gr-areopagus", "Areopagus, Athens", "雅典 · 战神山", "A bare limestone outcrop below the west end of the Acropolis, where Athens' oldest court tried cases of murder. In The Eumenides, the last play of the Oresteia, Athena founds the court here to try Orestes for killing his mother; the jury's votes are tied and she casts hers to acquit him. Steps cut in the rock lead to the top, with a wide view of the Agora",
         "卫城西端下面一块光秃秃的石灰岩，雅典最古老的法庭在这里审理杀人案。《俄瑞斯忒亚》最后一部《复仇女神》里，雅典娜在这里设立法庭审判弑母的俄瑞斯忒斯；陪审团票数相等，她投下决定性的一票判他无罪。岩石上凿有台阶通到顶上，可以俯瞰古市集"),
    ORIG("gr-thebes", "Thebes (Thiva)", "底比斯（锡瓦）", "The modern town of Thiva stands on the Cadmea, the hill of ancient Thebes, the most tragic city on the Greek stage: here Oedipus solved the Sphinx's riddle and married his mother, his sons killed each other at the seven gates, Antigone buried her brother against the law, and Pentheus was torn apart by Bacchants. Little stands above ground, but the archaeological museum is rich",
         "今天的锡瓦城就建在古底比斯的卡德摩斯山上。这是希腊悲剧舞台上最悲惨的城：俄狄浦斯在这里解开斯芬克斯之谜、娶了自己的母亲，他的两个儿子在七座城门前同归于尽，安提戈涅违法埋葬哥哥，彭透斯被酒神女信徒撕碎。地面遗迹很少，考古博物馆藏品丰富"),
    ORIG("gr-colonus", "Hill of Colonus, Athens", "雅典 · 科罗诺斯山", "A low hill in north-west Athens, once the village where Sophocles was born. In his last play, the blind old Oedipus, led by Antigone, reaches the sacred grove of the Eumenides here and is taken under the protection of Theseus before he passes mysteriously from the earth. Today it is a small park among apartment blocks, with the graves of two classical scholars",
         "雅典西北的一座矮山，古时是索福克勒斯出生的村子。在他最后一部剧里，失明的老俄狄浦斯由安提戈涅搀扶，来到这里的复仇女神圣林，受到忒修斯庇护，随后神秘地离开人世。如今这里是公寓楼之间的一个小公园，园里葬着两位古典学者"),
    ORIG("gr-corinth", "Ancient Corinth", "古科林斯", "The rich trading city on the isthmus, guarded by the rock of Acrocorinth. Medea is set here: Jason, whom she helped win the Golden Fleece, leaves her to marry the king's daughter, and she kills the bride with a poisoned robe and then her own children. Seven columns of the Temple of Apollo still stand in the ruins, below the castle on the rock",
         "地峡上富庶的商城，由科林斯卫城那块巨岩守护。《美狄亚》就发生在这里：她曾帮伊阿宋夺得金羊毛，伊阿宋却抛弃她，要娶国王的女儿；她用毒袍害死新娘，又杀了自己的孩子。废墟里阿波罗神庙还立着七根石柱，上方岩顶是城堡"),
    ORIG("gr-aulis", "Temple of Artemis, Aulis", "奥利斯 · 阿耳忒弥斯神庙", "The sheltered bay on the strait of Euboea where, in myth, the Greek fleet gathered to sail for Troy and lay becalmed. In Iphigenia in Aulis, Agamemnon lures his daughter here with a promise of marriage to Achilles, to sacrifice her to Artemis for a wind; she ends by offering herself. The foundations of a temple of Artemis survive by the shore",
         "埃维亚海峡边一个避风的海湾。神话里，希腊舰队在这里集结准备远征特洛伊，却因无风困在港中。《伊菲革涅亚在奥利斯》里，阿伽门农以嫁给阿喀琉斯为名把女儿骗来，要把她献祭给阿耳忒弥斯换取顺风；最后她自愿献身。海边还留着一座阿耳忒弥斯神庙的地基"),
    ORIG("gr-acropolis", "Acropolis of Athens", "雅典卫城", "The rock above Athens crowned by the Parthenon, built in the 440s BC, which held the city's treasury. In Lysistrata, written in the twentieth year of the war with Sparta, the women of Athens seize the Acropolis to keep the men from the war funds, and with the women of Sparta go on a sex strike until the men make peace",
         "雅典城上方的巨岩，顶上是公元前 440 年代建成的帕特农神庙，城邦的金库就放在这里。在与斯巴达交战的第二十年写成的《吕西斯特拉忒》里，雅典妇女占领卫城，不让男人动用军费，又联合斯巴达妇女一起拒绝同房，直到男人们讲和"),
    ORIG("gr-agora", "Ancient Agora of Athens", "雅典古市集", "The marketplace and civic heart of classical Athens, where Socrates spent his days questioning anyone who would talk. The state prison where he drank the hemlock is thought to stand at its south-west corner. The restored Stoa of Attalos now houses the Agora Museum, and the Temple of Hephaestus above it is one of the best-preserved Greek temples",
         "古典时代雅典的市场和公共生活中心，苏格拉底每天在这里拦住愿意交谈的人发问。人们认为他饮下毒芹汁的国家监狱就在市集西南角。重建的阿塔罗斯柱廊如今是市集博物馆，上方的赫菲斯托斯神庙是保存最完好的希腊神庙之一"),
    ORIG("gr-thermopylae", "Thermopylae", "温泉关", "The narrow pass between the mountains and the sea where in 480 BC Leonidas and his three hundred Spartans held off the army of Xerxes for three days, until a local man showed the Persians a mountain path. Herodotus tells the story; the sea has since retreated, leaving a plain. A bronze statue of Leonidas stands by the road, opposite the hill of the last stand",
         "群山和大海之间的狭窄关口。公元前 480 年，列奥尼达率三百斯巴达人在这里挡住薛西斯大军三天，直到一个本地人给波斯人指出一条山路。希罗多德记下了这个故事。如今海岸线已经后退，留下一片平原。路边立着列奥尼达的铜像，对面就是最后死守的小山"),
    ORIG("gr-kerameikos", "Kerameikos, Athens", "雅典 · 凯拉米克斯", "The potters' quarter and great cemetery of ancient Athens, outside the Dipylon Gate, where the city buried its war dead at public expense. In the winter of 431 BC Pericles gave the funeral oration for the first dead of the Peloponnesian War here, as Thucydides records, praising Athens as 'the school of Hellas'. Grave monuments line the ancient road",
         "古雅典的陶匠区和大墓地，在双门外，城邦在这里公葬阵亡将士。据修昔底德记载，公元前 431 年冬天，伯里克利在这里为伯罗奔尼撒战争第一批阵亡者发表葬礼演说，称雅典是“全希腊的学校”。古道两旁排列着墓碑"),
    ORIG("gr-piraeus", "Piraeus", "比雷埃夫斯", "The port of Athens since Themistocles fortified it in the 5th century BC, and still Greece's busiest, with ferries to every island. The Republic begins here: 'I went down yesterday to the Piraeus with Glaucon', says Socrates, to see a festival of the goddess Bendis, and at the house of old Cephalus the long conversation about justice begins",
         "公元前 5 世纪地米斯托克利修筑城防以来就是雅典的港口，至今仍是希腊最繁忙的港口，渡轮开往各个岛屿。《理想国》从这里开始：苏格拉底说，“昨天我和格劳孔一起下到比雷埃夫斯”，去看女神本狄斯的节庆，在老人克法洛斯家里，那场关于正义的长谈开始了"),
    PIL("gr-lyceum", "Lyceum of Aristotle, Athens", "雅典 · 亚里士多德吕克昂", "The site of the school Aristotle founded in 335 BC in a grove sacred to Apollo Lykeios, where he taught while walking up and down the colonnades, which is why his followers were called Peripatetics. Its remains were found in 1996 while digging for a new museum and opened to visitors in 2014, beside the Athens Conservatory",
        "亚里士多德公元前 335 年在阿波罗·吕克奥斯圣林里创办学园的地方，他边在柱廊下来回走动边讲课，所以他的学生被称为“逍遥学派”。遗址是 1996 年为新博物馆挖地基时发现的，2014 年对公众开放，就在雅典音乐学院旁边",
        ["ethics"]),
    PIL("gr-chaeronea", "Chaeronea", "喀罗尼亚", "A Boeotian village where Plutarch was born around AD 46 and spent most of his life, writing the Parallel Lives and serving as a priest at nearby Delphi. A huge marble lion by the road marks the grave of the Theban Sacred Band, killed here in 338 BC when Philip of Macedon defeated Athens and Thebes, a battle Plutarch describes",
        "维奥蒂亚的一个村子，普鲁塔克约公元 46 年生在这里，一生大半住在这里，写《希腊罗马名人传》，还在附近的德尔斐任祭司。路边一头巨大的大理石狮子，是公元前 338 年在此战死的底比斯圣队之墓——那一年马其顿的腓力在这里打败雅典和底比斯，普鲁塔克写过这场战役",
        ["plutarch"]),
    PIL("gr-eresos", "Eresos, Lesbos", "莱斯博斯岛 · 埃雷索斯", "A village in western Lesbos, named by ancient writers as Sappho's birthplace. Around 600 BC she wrote love poems to women on this island that made her name, and the word for women who love women, from Lesbos. Most of her nine books are lost; the long beach of Skala Eresou below the village draws many women travellers",
        "莱斯博斯岛西部的村子，古代作家记载这里是萨福的出生地。约公元前 600 年，她在这座岛上写下献给女子的情诗，她的名字和“莱斯博斯”这个词都由此成了爱女子的女子的代称。她的九卷诗大多已经失传；村下斯卡拉埃雷索斯的长海滩吸引了许多女性旅人",
        ["sappho"]),
]

lines = [
    S("odyssey-s1", "odyssey", "gr-ithaca", "Books 13–23", "第十三至二十三卷",
      "After twenty years away, Odysseus is set ashore asleep on Ithaca by the Phaeacians. Disguised by Athena as an old beggar, he lodges with his loyal swineherd Eumaeus, is recognised by his dying dog Argos, and reveals himself to his son Telemachus. In his own hall he strings the great bow that none of Penelope's suitors can bend, kills them all, and is finally known to Penelope by the secret of their bed.",
      "离家二十年后，奥德修斯在睡梦中被费埃克斯人送上伊萨卡的海岸。雅典娜把他变成年老的乞丐，他住进忠实的猪倌欧迈俄斯的小屋，被奄奄一息的老狗阿尔戈斯认了出来，又向儿子忒勒马科斯表明了身份。在自己的大厅里，他拉开了珀涅罗珀的求婚者谁也拉不开的大弓，把他们全部杀死，最后凭着婚床的秘密与珀涅罗珀相认。",
      ["his dying dog Argos"], ["老狗阿尔戈斯"], W + "Odyssey"),
    S("oresteia-s1", "oresteia", "gr-areopagus", "Agamemnon; The Eumenides", "《阿伽门农》《复仇女神》",
      "Agamemnon comes home from Troy and is killed in his bath by his wife Clytemnestra, in revenge for the daughter he sacrificed. Years later their son Orestes kills his mother and is hunted by the Furies to Athens. There, on the Areopagus, Athena sets up the first court of law; the jury's votes are equal, she acquits Orestes, and the Furies are persuaded to become the Kindly Ones.",
      "阿伽门农从特洛伊回到家，被妻子克吕泰涅斯特拉杀死在浴池里——她要为他献祭的女儿报仇。多年后，他们的儿子俄瑞斯忒斯杀死了母亲，被复仇女神一路追到雅典。在战神山上，雅典娜设立了第一个法庭；陪审团票数相等，她判俄瑞斯忒斯无罪，复仇女神也被说服，成了“慈悲女神”。",
      ["first court of law"], ["第一个法庭"], W + "Oresteia"),
    S("seven-s1", "seven-thebes", "gr-thebes", "Throughout", "全剧",
      "Polynices, exiled son of Oedipus, marches on Thebes with six champions to take the throne from his brother Eteocles. A scout describes each attacker and the device on his shield, and Eteocles names a defender for each of the seven gates, taking the seventh himself against his own brother. The city is saved, and the two brothers kill each other.",
      "俄狄浦斯被放逐的儿子波吕尼刻斯带着六员猛将进攻底比斯，要从兄弟厄忒俄克勒斯手中夺回王位。探子逐一描述每个攻城者和他盾牌上的图案，厄忒俄克勒斯为七座城门各派一名守将，第七门由他亲自迎战自己的兄弟。城保住了，兄弟俩却同归于尽。",
      ["seven gates"], ["七座城门"], W + "Seven_Against_Thebes"),
    S("oedipus-s1", "oedipus-rex", "gr-thebes", "Throughout", "全剧",
      "Thebes is dying of plague, and the oracle at Delphi says the murderer of the old king Laius must be driven out. King Oedipus, who once saved the city by answering the Sphinx's riddle, swears to find him, and step by step learns from the blind prophet Tiresias and an old shepherd that he himself killed Laius, his father, and married Jocasta, his mother. Jocasta hangs herself and Oedipus blinds himself.",
      "底比斯正遭瘟疫，德尔斐的神谕说必须驱逐杀害老国王拉伊俄斯的凶手。曾经解开斯芬克斯之谜、拯救过城邦的俄狄浦斯王发誓要找出凶手，从盲先知忒瑞西阿斯和一个老牧人那里一步步得知：杀死拉伊俄斯的正是他自己，那是他的父亲，而他娶的伊俄卡斯忒是他的母亲。伊俄卡斯忒自缢，俄狄浦斯刺瞎了双眼。",
      ["Sphinx's riddle"], ["斯芬克斯之谜"], W + "Oedipus_Rex"),
    S("antigone-s1", "antigone", "gr-thebes", "Throughout", "全剧",
      "After Oedipus's sons have killed each other, the new king Creon orders that the traitor Polynices be left unburied for the dogs and birds. His sister Antigone, obeying the unwritten laws of the gods, scatters earth over the body and is sentenced to be walled up alive. Creon gives way too late: Antigone has hanged herself, and his son and his wife kill themselves.",
      "俄狄浦斯的两个儿子同归于尽后，新王克瑞翁下令让叛徒波吕尼刻斯暴尸荒野，任狗和鸟啄食。他的妹妹安提戈涅遵从众神不成文的律法，往尸体上撒了土，被判活活关进石墓。克瑞翁让步时已经太迟：安提戈涅已经自缢，他的儿子和妻子也相继自杀。",
      ["unwritten laws"], ["不成文的律法"], W + "Antigone_(Sophocles_play)"),
    S("bacchae-s1", "bacchae", "gr-thebes", "Throughout", "全剧",
      "The god Dionysus comes to Thebes, the city of his mother, in the shape of a young stranger, and drives its women mad so that they run to Mount Cithaeron to dance in his honour. Young King Pentheus tries to suppress the new god, is persuaded to spy on the women in women's clothes, and is torn apart by them; his own mother Agave carries his head back to the city, believing it a lion's.",
      "酒神狄俄尼索斯化身为一个年轻的外乡人来到他母亲的城市底比斯，让城里的妇女发狂，跑到基泰隆山上为他跳舞。年轻的国王彭透斯想镇压这位新神，却被诱骗穿上女装去偷看她们，结果被她们撕成碎片；他的亲生母亲阿高厄捧着他的头回城，还以为那是一头狮子的头。",
      ["Mount Cithaeron"], ["基泰隆山"], W + "The_Bacchae"),
    S("colonus-s1", "oedipus-colonus", "gr-colonus", "Throughout", "全剧",
      "Old, blind and banished, Oedipus wanders with his daughter Antigone to the sacred grove of the Eumenides at Colonus, where an oracle has said he will die. Creon and his son Polynices try to take him back to serve their own ends; Theseus of Athens protects him. At a clap of thunder Oedipus leads the way, without help, to a place no one may know, and vanishes.",
      "年老、失明、被放逐的俄狄浦斯由女儿安提戈涅陪着，流浪到科罗诺斯的复仇女神圣林，神谕说他将死在这里。克瑞翁和他的儿子波吕尼刻斯都想把他带回去，为自己所用；雅典的忒修斯保护了他。一声雷鸣之后，俄狄浦斯不用人扶，自己领路走向一个无人可以知道的地方，就此消失了。",
      ["sacred grove"], ["圣林"], W + "Oedipus_at_Colonus"),
    S("medea-s1", "medea", "gr-corinth", "Throughout", "全剧",
      "In Corinth, Jason abandons Medea, the foreign princess who betrayed her own family to help him win the Golden Fleece, in order to marry the daughter of King Creon. Ordered into exile, Medea begs for one day; she sends the bride a poisoned robe and crown that burn her and her father to death, kills her two sons, and escapes in the chariot of the Sun.",
      "在科林斯，伊阿宋为了娶国王克瑞翁的女儿，抛弃了美狄亚——这位异邦公主当年背叛家族，帮他夺得了金羊毛。被勒令流放的美狄亚请求宽限一天；她给新娘送去浸了毒的袍子和金冠，把新娘和她父亲活活烧死，又杀了自己的两个儿子，乘着太阳神的车逃走了。",
      ["Golden Fleece"], ["金羊毛"], W + "Medea_(play)"),
    S("iphigenia-s1", "iphigenia-aulis", "gr-aulis", "Throughout", "全剧",
      "The Greek fleet is stuck at Aulis without a wind, and the prophet says Artemis demands the sacrifice of Agamemnon's daughter. He sends for Iphigenia on the pretence that she is to marry Achilles, then tries to change his mind. When Achilles offers to fight the whole army for her, Iphigenia chooses to go willingly to the altar for Greece.",
      "希腊舰队因为无风被困在奥利斯，先知说阿耳忒弥斯要求献祭阿伽门农的女儿。他谎称要把伊菲革涅亚嫁给阿喀琉斯，派人接她来，随后又反悔。阿喀琉斯愿意为她与全军为敌，伊菲革涅亚却决定为了希腊自愿走上祭坛。",
      ["marry Achilles"], ["嫁给阿喀琉斯"], W + "Iphigenia_in_Aulis"),
    S("lysistrata-s1", "lysistrata", "gr-acropolis", "Throughout", "全剧",
      "Tired of the endless war, Lysistrata persuades the women of Athens and Sparta to refuse their husbands until they make peace, while the older women seize the Acropolis and the treasury. The old men try to smoke them out and are drenched with water; the young husbands grow desperate, and at last the ambassadors of both sides, in obvious discomfort, sign the peace.",
      "厌倦了没完没了的战争，吕西斯特拉忒说服雅典和斯巴达的妇女拒绝与丈夫同房，直到他们讲和；年长的妇女则占领了卫城和金库。老头子们想用烟把她们熏出来，结果被浇成了落汤鸡；年轻的丈夫们越来越绝望，最后双方使节明显狼狈不堪地签下了和约。",
      ["seize the Acropolis"], ["占领了卫城"], W + "Lysistrata"),
    S("clouds-s1", "clouds", "gr-agora", "Throughout", "全剧",
      "Strepsiades, ruined by his son's love of horses, enrols at the Thinkery of Socrates, who hangs in a basket to study the heavens and worships the Clouds, to learn the argument that can win any case and cheat his creditors. Too stupid to learn, he sends his son instead, who comes back able to prove that a son may beat his father; Strepsiades burns the Thinkery down.",
      "斯特瑞普西阿得斯被儿子爱马的嗜好弄得倾家荡产，便进了苏格拉底的“思想所”——苏格拉底吊在篮子里研究天象，崇拜云神——想学会能打赢任何官司的诡辩，好赖掉债主的钱。他太笨学不会，就让儿子去学，儿子回来后能论证儿子打老子天经地义；斯特瑞普西阿得斯一把火烧了思想所。",
      ["Thinkery"], ["思想所"], W + "The_Clouds"),
    S("histories-s1", "histories", "gr-thermopylae", "Book 7", "第七卷",
      "As Xerxes' vast army marches into Greece, Leonidas of Sparta holds the pass at Thermopylae. Told that the Persian arrows would hide the sun, a Spartan answers that they will fight in the shade. For two days the Persians cannot break through; when the traitor Ephialtes leads them over the mountain path, Leonidas sends most of the Greeks away and dies with his three hundred.",
      "薛西斯大军开进希腊，斯巴达王列奥尼达扼守温泉关。有人说波斯人的箭多得能遮住太阳，一个斯巴达人回答：那我们就在阴凉里作战。波斯人两天攻不破关口；叛徒厄菲阿尔特斯带他们翻过山路后，列奥尼达遣走了大部分希腊人，和他的三百勇士一起战死。",
      ["fight in the shade"], ["在阴凉里作战"], W + "Battle_of_Thermopylae"),
    S("thucydides-s1", "thucydides", "gr-kerameikos", "Book 2, Pericles' Funeral Oration", "第二卷，伯里克利葬礼演说",
      "At the public funeral for the Athenians killed in the first year of the war, Pericles speaks not of the dead but of the city they died for: a democracy open to the world, where men love beauty without extravagance and wisdom without weakness. Soon afterwards plague strikes the crowded city, and Thucydides, who caught it himself, describes its symptoms and the breakdown of all law.",
      "在为战争第一年阵亡的雅典人举行的公葬上，伯里克利讲的不是死者，而是他们为之而死的城邦：一个向世界敞开的民主城邦，人们爱美而不奢侈，爱智慧而不柔弱。不久瘟疫袭击了拥挤的雅典，自己也染过病的修昔底德记下了它的症状，以及一切法律秩序的崩溃。",
      ["public funeral"], ["公葬"], W + "Pericles%27_Funeral_Oration"),
    S("socrates-s1", "socrates", "gr-agora", "Apology; Phaedo", "《申辩》《斐多》",
      "Accused of corrupting the young and not believing in the city's gods, the seventy-year-old Socrates tells the jury that the unexamined life is not worth living, and when found guilty proposes, as his penalty, free meals for life. In prison he refuses his friends' plan of escape, spends his last day arguing that the soul is immortal, and drinks the hemlock calmly.",
      "七十岁的苏格拉底被控败坏青年、不信城邦的神，他对陪审团说，未经省察的人生不值得过；被判有罪后，他提出的“刑罚”是由城邦终身供他吃饭。在狱中，他拒绝了朋友们的越狱计划，最后一天都在论证灵魂不朽，然后平静地喝下了毒芹汁。",
      ["unexamined life"], ["未经省察的人生"], W + "Apology_(Plato)"),
    S("symposium-s1", "symposium", "gr-agora", "Throughout", "全篇",
      "At a dinner party in Athens to celebrate the playwright Agathon's victory, the guests agree to make speeches in praise of Love. Aristophanes tells how humans were once double creatures split in two, forever seeking their other half; Socrates repeats what the priestess Diotima taught him of the ladder from the love of one body to the love of beauty itself; then the drunken Alcibiades bursts in.",
      "在雅典，为庆祝剧作家阿伽松获奖而办的一场宴会上，客人们约定轮流发表赞美爱神的演说。阿里斯托芬讲人原本是双体的，被劈成两半，从此永远寻找另一半；苏格拉底转述女祭司狄奥提玛教给他的道理：从爱一个身体，一级级上升到爱美本身；接着，喝醉的阿尔基比亚德闯了进来。",
      ["other half"], ["另一半"], W + "Symposium_(Plato)"),
    S("republic-s1", "republic", "gr-piraeus", "Book 1 and Book 7", "第一卷与第七卷",
      "Coming back from a festival at the Piraeus, Socrates is pressed into a conversation at the house of old Cephalus about what justice is. To answer, he builds an ideal city ruled by philosophers, and in its most famous image compares people to prisoners chained in a cave, who take the shadows on the wall for reality until one of them is dragged up into the sunlight.",
      "苏格拉底在比雷埃夫斯看完节庆，被拉进老人克法洛斯家里，讨论什么是正义。为了回答这个问题，他构建了一个由哲学家统治的理想城邦；书中最有名的比喻把人比作被锁在洞穴里的囚徒，把墙上的影子当成真实，直到其中一个人被拖上地面，看见阳光。",
      ["prisoners chained in a cave"], ["被锁在洞穴里的囚徒"], W + "Republic_(Plato)"),
    S("ethics-s1", "ethics", "gr-lyceum", "Books 1, 2 and 10", "第一、二、十卷",
      "In lectures given at the Lyceum, Aristotle asks what the highest good of human life is and answers eudaimonia, flourishing, which comes from living according to virtue. Virtue is a habit, learned by practice, and lies in a mean between two extremes, as courage lies between cowardice and rashness; the happiest life of all is one spent in contemplation.",
      "在吕克昂的讲课里，亚里士多德追问人生最高的善是什么，回答是“幸福”，即依照德性生活而得的繁荣兴旺。德性是一种习惯，靠实践养成，处于两个极端之间的中道，就像勇敢处在怯懦和鲁莽之间；最幸福的生活是沉思的生活。",
      ["a mean between two extremes"], ["中道"], W + "Nicomachean_Ethics"),
    S("plutarch-s1", "plutarch", "gr-chaeronea", "Throughout", "全书",
      "Plutarch pairs the lives of famous Greeks and Romans, Theseus with Romulus, Alexander with Caesar, Demosthenes with Cicero, to show character in action. He says he writes lives, not histories, and that a small thing, a phrase or a jest, often reveals a man better than battles. Shakespeare took Julius Caesar and Antony and Cleopatra from North's translation.",
      "普鲁塔克把著名的希腊人和罗马人两两配对立传：忒修斯和罗慕路斯，亚历山大和恺撒，德摩斯梯尼和西塞罗，用行动展现人物的品格。他说自己写的是传记而不是历史，一句话或一个玩笑这样的小事，常常比战役更能看出一个人。莎士比亚的《裘力斯·恺撒》和《安东尼与克莉奥佩特拉》就取材于诺斯的译本。",
      ["lives, not histories"], ["传记而不是历史"], W + "Parallel_Lives"),
    S("sappho-s1", "sappho", "gr-eresos", "Fragments 1 and 31", "残篇第一首与第三十一首",
      "Sappho calls on Aphrodite to come down again from heaven, as she has before, and help her win a girl who flees her. In another fragment she watches the girl she loves laughing with a man and feels her tongue break, a thin fire run under her skin, her eyes go blind and her ears roar, 'greener than grass', close to death.",
      "萨福呼唤阿佛洛狄忒像从前那样再次从天上降临，帮她赢得一个躲着她的女孩。在另一首残篇里，她看着心爱的女孩和一个男人说笑，觉得舌头僵住，一股细火在皮肤下流窜，眼睛看不见，耳朵轰鸣，脸色“比青草还绿”，仿佛就要死去。",
      ["greener than grass"], ["比青草还绿"], W + "Sappho_31"),
]

if __name__ == "__main__":
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
