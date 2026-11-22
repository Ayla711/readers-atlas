"""11-22: Portugal, first pack: 50 books, 62 places. The canon from the medieval cantigas to Saramago and Peixoto, plus
the best-known foreign books set in the country (Candide, Childe Harold, Pereira Maintains, Night Train to Lisbon…).
Fictional or unnamed settings hang on the real place the book is modelled on, or on the writer's own place, and the
note says which.

Quotations (13 books, 16 lines) are cut from Wikisource pages (tools/content/wikisource.py): Portuguese, French and
English Wikisource; English and Chinese translations are our own drafts (translation: "own"), Byron's English is the
original. Every other book has a scene note for now, in copyright or not: the public-domain ones can take quotations
later (Peregrinação and the Portuguese Letters are on Wikisource only in facsimile spelling).
What a cut changes, named again in that line's `checked`: page line ends inside a sentence are joined; the French
no-break space before ; is written as a space; the stanza number of the Lusiads is left out.

Coordinates come from Wikimedia Commons (median of the geotagged files of the place's category) or, where a category
has none, from the place's Wikidata item (cache/pt/coords.json, made by cache/pt/co.py).
Candide is the book already on the shared list (id "candide").

Usage: python3 -I add_pt1.py <app_dir> <coords.json> <wikisource_dir>"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b
import wikisource as ws

APP, CO, WS = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
DATE = "2026-11-22"
b.init(APP, "", "pt", DATE)
W, GAP = b.W, b.GAP

def BK(id, title, title_zh, author, author_zh, year, pd=True, **kw):
    d = dict(id=id, title=title, title_zh=title_zh, author=author, author_zh=author_zh, year=year,
             orig_lang=kw.pop("lang", "pt"), public_domain=pd, source_url=kw.pop("src", None))
    d.update(kw)
    return d

def C(pid):
    c = CO[pid]
    return c["lat"], c["lon"], c["st"], c["su"]

def ORIG(pid, name, zh, en_note, zh_note, **kw): return b.ORIG(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PROTO(pid, name, zh, en_note, zh_note, **kw): return b.PROTO(pid, name, zh, *C(pid), en_note, zh_note, **kw)
def PIL(pid, name, zh, en_note, zh_note, ids, **kw): return b.PIL(pid, name, zh, *C(pid), en_note, zh_note, ids, **kw)
S = b.S

def raw(title, start, end, after=None):
    t = ws.text(WS, title)
    i = t.find(start, t.find(after) if after else 0)
    assert i >= 0, (title, start)
    j = t.find(end, i)
    assert j >= 0, (title, start, end)
    return t[i:j + len(end)]

def joined(title, start, end, **k):
    s = raw(title, start, end, **k)
    assert "\n" in s, (title, start)
    return " ".join(s.split("\n"))

def Q(id, book, place, loc, loc_zh, site, title, orig, hl_orig, en, hl_en, zh, hl_zh, note="", original=False):
    for text, hls in ((orig, hl_orig), (en, hl_en), (zh, hl_zh)):
        for h in hls:
            assert h in text, (id, h)
    assert "  " not in orig and "\xa0" not in orig, (id, "spacing")
    d = dict(id=id, book_id=book, place_ids=[place], location=loc, location_zh=loc_zh)
    if original:
        d.update(text_en=orig, highlight_en=hl_orig, text_zh=zh, highlight_zh=hl_zh, translation="original")
    else:
        d.update(text_orig=orig, highlight_orig=hl_orig, text_en=en, highlight_en=hl_en, text_zh=zh, highlight_zh=hl_zh, translation="own")
    d.update(status="draft", checked=f"{site} Wikisource, {title}{note}, {DATE}")
    return d

JOINED = " (the page's line ends inside sentences joined)"
EC = ("Eça de Queirós", "埃萨·德·克罗兹")
PESSOA = ("Fernando Pessoa", "佩索阿")
SARAMAGO = ("José Saramago", "萨拉马戈")
PTS = lambda t: ws.url("pt", t)

# ============================== books ==============================
L3, L4 = "Os Lusíadas (grafia atualizada)/III", "Os Lusíadas (grafia atualizada)/IV"
VIA, AMOR, MAIAS, AMARO = "Viagens na Minha Terra (1846)/XXVII", "Amor de Perdição (1862)/Prefacio", "Os Maias/Livro I/I", "O Crime do Padre Amaro/I"
SERRAS, CES, DIN, ABO = "A Cidade e as Serras/VIII", "O Sentimento dum ocidental", "Ai flores, ai flores do verde pino", "A Abóbada/I"
FAM, PRIMO = "Uma Família Ingleza/VII", "O Primo Basílio/VI"
BYRON = "The Works of Lord Byron (ed. Coleridge, Prothero)/Poetry/Volume 2/Childe Harold's Pilgrimage/Canto I"
CAN5, CAN6 = "Candide, ou l’Optimisme/Garnier 1877/Chapitre 5", "Candide, ou l’Optimisme/Garnier 1877/Chapitre 6"

books = [
    BK("pt-cantigas-dinis", "Songs of King Dinis", "国王迪尼什的歌谣", "Dinis I of Portugal", "迪尼什一世", "c. 1300", title_orig="Cantigas de D. Dinis", src=PTS(DIN),
       aliases=["Ai flores, ai flores do verde pino", "cantigas de amigo", "Dom Dinis"]),
    BK("pt-cronica-joao-i", "Chronicle of King João I", "若昂一世编年史", "Fernão Lopes", "费尔南·洛佩斯", "c. 1443", title_orig="Crónica de D. João I",
       aliases=["Cronica de D. Joao I", "Aljubarrota", "Nuno Álvares Pereira"]),
    BK("pt-barca-do-inferno", "The Ship of Hell", "地狱之船", "Gil Vicente", "吉尔·维森特", "1517", title_orig="Auto da Barca do Inferno", aliases=["Auto da Barca do Inferno"]),
    BK("pt-lusiadas", "The Lusiads", "卢济塔尼亚人之歌", "Luís de Camões", "卡蒙斯", "1572", title_orig="Os Lusíadas", src=PTS(L3),
       aliases=["Os Lusiadas", "Camoes", "Vasco da Gama", "Inês de Castro", "Adamastor", "葡国魂"]),
    BK("pt-peregrinacao", "The Travels of Mendes Pinto", "远游记", "Fernão Mendes Pinto", "费尔南·门德斯·平托", "1614", title_orig="Peregrinação", aliases=["Peregrinacao", "Pilgrimage"]),
    BK("pt-portuguese-letters", "Letters of a Portuguese Nun", "葡萄牙修女的情书", "attributed to Mariana Alcoforado", "传为玛丽安娜·阿尔科福拉多", "1669", lang="fr",
       title_orig="Lettres portugaises", aliases=["Lettres portugaises", "Cartas Portuguesas", "Guilleragues", "Mariana Alcoforado"]),
    BK("pt-voyage-to-lisbon", "The Journal of a Voyage to Lisbon", "里斯本航行日记", "Henry Fielding", "菲尔丁", "1755", lang="en"),
    BK("pt-bocage-sonnets", "Sonnets", "博卡热十四行诗", "Manuel Maria Barbosa du Bocage", "博卡热", "1791–1804", title_orig="Sonetos", aliases=["Bocage"]),
    BK("pt-childe-harold", "Childe Harold's Pilgrimage", "恰尔德·哈洛尔德游记", "Lord Byron", "拜伦", "1812", lang="en", src=ws.url("en", BYRON), aliases=["Cintra", "glorious Eden"]),
    BK("pt-beckford-alcobaca", "Recollections of an Excursion to the Monasteries of Alcobaça and Batalha", "阿尔科巴萨与巴塔利亚修道院游记", "William Beckford", "贝克福德", "1835", lang="en",
       aliases=["Alcobaca and Batalha"]),
    BK("pt-lendas-e-narrativas", "Legends and Narratives", "传说与故事", "Alexandre Herculano", "埃尔库拉诺", "1851", title_orig="Lendas e Narrativas", src=PTS(ABO),
       aliases=["A Abóbada", "A Abobada", "The Vault", "Afonso Domingues"]),
    BK("pt-viagens", "Travels in My Homeland", "故乡之旅", "Almeida Garrett", "阿尔梅达·加勒特", "1846", title_orig="Viagens na Minha Terra", src=PTS(VIA), aliases=["Joaninha", "Carlos"]),
    BK("pt-amor-de-perdicao", "Doomed Love", "毁灭之恋", "Camilo Castelo Branco", "卡米洛·卡斯特洛·布兰科", "1862", title_orig="Amor de Perdição", src=PTS(AMOR),
       aliases=["Amor de Perdicao", "Simão Botelho", "Teresa de Albuquerque"]),
    BK("pt-pupilas", "The Pupils of the Dean", "教区长的两个养女", "Júlio Dinis", "儒利奥·迪尼斯", "1867", title_orig="As Pupilas do Senhor Reitor", aliases=["As Pupilas do Senhor Reitor"]),
    BK("pt-familia-inglesa", "An English Family", "一个英国家庭", "Júlio Dinis", "儒利奥·迪尼斯", "1868", title_orig="Uma Família Inglesa", src=PTS(FAM), aliases=["Uma Familia Inglesa", "Carlos Whitestone", "Jenny"]),
    BK("pt-misterio-sintra", "The Mystery of the Sintra Road", "辛特拉公路之谜", "Eça de Queirós and Ramalho Ortigão", "埃萨·德·克罗兹与拉马略·奥尔蒂冈", "1870",
       title_orig="O Mistério da Estrada de Sintra", aliases=["O Misterio da Estrada de Sintra"]),
    BK("pt-padre-amaro", "The Crime of Father Amaro", "阿马罗神父的罪恶", *EC, "1875", title_orig="O Crime do Padre Amaro", src=PTS(AMARO), aliases=["Amélia", "Padre Amaro"]),
    BK("pt-primo-basilio", "Cousin Bazilio", "巴济里奥表兄", *EC, "1878", title_orig="O Primo Basílio", src=PTS(PRIMO), aliases=["O Primo Basilio", "Luísa", "Juliana"]),
    BK("pt-os-maias", "The Maias", "马亚一家", *EC, "1888", title_orig="Os Maias", src=PTS(MAIAS), aliases=["Carlos da Maia", "Maria Eduarda", "Ramalhete", "João da Ega"]),
    BK("pt-antero-sonnets", "Complete Sonnets", "肯塔尔十四行诗全集", "Antero de Quental", "安特罗·德·肯塔尔", "1886", title_orig="Os Sonetos Completos"),
    BK("pt-cesario-verde", "The Book of Cesário Verde", "塞萨里奥·维尔德诗集", "Cesário Verde", "塞萨里奥·维尔德", "1887", title_orig="O Livro de Cesário Verde", src=PTS(CES),
       aliases=["O Sentimento dum Ocidental", "The Feeling of a Westerner"]),
    BK("pt-os-meus-amores", "My Loves", "我的所爱", "Trindade Coelho", "特林达德·科埃略", "1891", title_orig="Os Meus Amores"),
    BK("pt-so", "Alone", "孤独", "António Nobre", "安东尼奥·诺布雷", "1892", title_orig="Só", aliases=["So", "Antonio Nobre"]),
    BK("pt-cidade-e-serras", "The City and the Mountains", "城与山", *EC, "1901", title_orig="A Cidade e as Serras", src=PTS(SERRAS), aliases=["Jacinto", "Zé Fernandes", "Tormes"]),
    BK("pt-maranus", "Marânus", "马拉努斯", "Teixeira de Pascoaes", "特谢拉·德·帕斯科埃斯", "1911", title_orig="Marânus", aliases=["Maranus", "saudade", "Saudosismo"]),
    BK("pt-os-pescadores", "The Fishermen", "渔夫", "Raul Brandão", "劳尔·布兰当", "1923", title_orig="Os Pescadores"),
    BK("pt-ilhas-desconhecidas", "The Unknown Islands", "陌生的岛屿", "Raul Brandão", "劳尔·布兰当", "1926", title_orig="As Ilhas Desconhecidas"),
    BK("pt-charneca-em-flor", "Heath in Bloom", "繁花的荒原", "Florbela Espanca", "弗洛贝拉·埃斯潘卡", "1931", title_orig="Charneca em Flor"),
    BK("pt-mensagem", "Message", "使命", *PESSOA, "1934", title_orig="Mensagem", aliases=["Mar Português", "O Infante"]),
    BK("pt-pessoa-poems", "Poems of Fernando Pessoa", "佩索阿诗选", *PESSOA, "1914–1935", aliases=["Tabacaria", "The Tobacco Shop", "Álvaro de Campos", "Alberto Caeiro", "Ricardo Reis", "烟草店"]),
    BK("pt-disquiet", "The Book of Disquiet", "不安之书", *PESSOA, "1982", title_orig="Livro do Desassossego", aliases=["Bernardo Soares", "惶然录"]),
    BK("pt-esteiros", "Esteiros", "小港湾", "Soeiro Pereira Gomes", "索埃罗·佩雷拉·戈梅斯", "1941", title_orig="Esteiros"),
    BK("pt-contos-da-montanha", "Tales from the Mountain", "山村故事", "Miguel Torga", "米格尔·托尔加", "1941", pd=False, title_orig="Contos da Montanha", aliases=["Novos Contos da Montanha"]),
    BK("pt-mau-tempo-no-canal", "Stormy Isles: An Azorean Tale", "海峡的坏天气", "Vitorino Nemésio", "维托里诺·内梅西奥", "1944", pd=False, title_orig="Mau Tempo no Canal",
       aliases=["Mau Tempo no Canal", "Margarida Clark Dulmo"]),
    BK("pt-toada-de-portalegre", "Ballad of Portalegre", "波塔莱格雷之歌", "José Régio", "若泽·雷吉奥", "1941", pd=False, title_orig="Toada de Portalegre"),
    BK("pt-a-sibila", "The Sibyl", "女预言者", "Agustina Bessa-Luís", "阿古斯蒂娜·贝萨-路易斯", "1954", pd=False, title_orig="A Sibila", aliases=["Quina", "Casa da Vessada"]),
    BK("pt-quando-os-lobos-uivam", "When the Wolves Howl", "狼嚎之时", "Aquilino Ribeiro", "阿基利诺·里贝罗", "1958", pd=False, title_orig="Quando os Lobos Uivam"),
    BK("pt-aparicao", "Apparition", "显现", "Vergílio Ferreira", "维吉利奥·费雷拉", "1959", pd=False, title_orig="Aparição", aliases=["Aparicao"]),
    BK("pt-menina-do-mar", "The Little Girl from the Sea", "海的女儿", "Sophia de Mello Breyner Andresen", "索菲亚·德·梅洛·布雷内·安德雷森", "1958", pd=False, title_orig="A Menina do Mar"),
    BK("pt-novas-cartas", "New Portuguese Letters", "新葡萄牙书简", "Maria Isabel Barreno, Maria Teresa Horta and Maria Velho da Costa", "“三位玛丽亚”", "1972", pd=False,
       title_orig="Novas Cartas Portuguesas", aliases=["The Three Marias", "Novas Cartas Portuguesas"]),
    BK("pt-levantado-do-chao", "Raised from the Ground", "大地起义", *SARAMAGO, "1980", pd=False, title_orig="Levantado do Chão", aliases=["Mau-Tempo", "Monte Lavre"]),
    BK("pt-memorial-do-convento", "Baltasar and Blimunda", "修道院纪事", *SARAMAGO, "1982", pd=False, title_orig="Memorial do Convento", aliases=["Memorial do Convento", "Sete-Sóis", "Sete-Luas"]),
    BK("pt-ricardo-reis", "The Year of the Death of Ricardo Reis", "里卡多·雷耶斯离世那年", *SARAMAGO, "1984", pd=False, title_orig="O Ano da Morte de Ricardo Reis"),
    BK("pt-pequenas-memorias", "Small Memories", "小回忆", *SARAMAGO, "2006", pd=False, title_orig="As Pequenas Memórias"),
    BK("pt-manual-dos-inquisidores", "The Inquisitors' Manual", "审讯者手册", "António Lobo Antunes", "安东尼奥·洛博·安图内斯", "1996", pd=False, title_orig="O Manual dos Inquisidores"),
    BK("pt-galveias", "Galveias", "加尔维亚什", "José Luís Peixoto", "若泽·路易斯·佩肖托", "2014", pd=False, title_orig="Galveias"),
    BK("pt-pereira-maintains", "Pereira Maintains", "佩雷拉的证词", "Antonio Tabucchi", "安东尼奥·塔布齐", "1994", pd=False, lang="it", title_orig="Sostiene Pereira", aliases=["Sostiene Pereira", "Pereira Declares"]),
    BK("pt-night-train", "Night Train to Lisbon", "开往里斯本的夜车", "Pascal Mercier", "帕斯卡·梅西耶", "2004", pd=False, lang="de", title_orig="Nachtzug nach Lissabon",
       aliases=["Nachtzug nach Lissabon", "Raimund Gregorius", "Amadeu de Prado"]),
    BK("pt-high-mountains", "The High Mountains of Portugal", "葡萄牙的高山", "Yann Martel", "扬·马特尔", "2016", pd=False, lang="en"),
]

# ============================== places ==============================
places = [
    # ---- Lisbon ----
    ORIG("pt-jeronimos", "Jerónimos Monastery, Belém", "贝伦 · 热罗尼莫斯修道院",
         "Vasco da Gama's fleet sailed for India in 1497 from the beach at Restelo, beside a small chapel that stood here; the monastery was built afterwards with the wealth of the voyages. In Canto IV of The Lusiads the sailors leave 'the holy temple that stands on the sea shore' while the crowd weeps and an old man curses the venture. The tombs of Camões and, since 1985, of Fernando Pessoa are inside",
         "1497 年，达·伽马的船队从雷斯特洛海滩启航前往印度，海滩边原有一座小礼拜堂；修道院是后来用航海带来的财富建成的。《卢济塔尼亚人之歌》第四章里，水手们离开“坐落在海滩上的圣殿”，岸上人群哭泣，一位老人咒骂这次远航。卡蒙斯的墓在修道院里，佩索阿的墓 1985 年也迁到了这里"),
    PIL("pt-teatro-dmaria", "Teatro Nacional D. Maria II, Rossio", "罗西奥广场 · 玛丽亚二世国家剧院",
        "The national theatre, opened in 1846 at the urging of Almeida Garrett; a statue of Gil Vicente, the founder of Portuguese theatre, stands on top of its pediment. It was built on the site of the palace of the Inquisition",
        "国家剧院，1846 年在加勒特的推动下落成；山墙顶上立着葡萄牙戏剧之父吉尔·维森特的雕像。剧院所在的地方原是宗教裁判所的宫殿", ["pt-barca-do-inferno"]),
    ORIG("pt-carmo", "Carmo Convent ruins", "卡尔莫修道院遗址",
         "The Gothic church of the Carmelites lost its roof in the earthquake of 1 November 1755 and was never rebuilt; its open arches are Lisbon's memorial to the disaster. Candide and Pangloss walk into the city at the moment the earthquake strikes",
         "加尔默罗会的哥特式教堂在 1755 年 11 月 1 日的大地震中塌了屋顶，此后再没有重建，露天的拱架成了里斯本对这场灾难的纪念。老实人和邦葛罗斯走进城里的那一刻，正赶上地震"),
    ORIG("pt-rossio", "Rossio Square", "罗西奥广场",
         "Lisbon's main square. The palace of the Inquisition stood on its north side and its processions and autos-da-fé passed through here; in Candide, after the earthquake, the wise men of the country decide that a fine auto-da-fé is the way to stop the earth from shaking",
         "里斯本的中心广场。宗教裁判所的宫殿原在广场北侧，游行和火刑仪式都经过这里；《老实人》里，地震之后，当地的贤人们断定，办一场漂亮的火刑仪式就能让大地不再震动"),
    PIL("pt-english-cemetery", "English Cemetery, Lisbon", "里斯本英国人墓地",
        "Henry Fielding, gravely ill, sailed to Lisbon in the summer of 1754 hoping the climate would help, and died here two months later. His journal of the voyage was published the next year. His tomb is in this cemetery beside the Estrela gardens",
        "1754 年夏天，重病的菲尔丁乘船来到里斯本，指望这里的气候对他有好处，两个月后在此去世。他的航行日记第二年出版。他的墓就在埃什特雷拉花园旁的这座墓地里", ["pt-voyage-to-lisbon"]),
    PIL("pt-cafe-nicola", "Café Nicola, Rossio", "罗西奥广场 · 尼古拉咖啡馆",
        "The café where Bocage held court in the 1790s, improvising verses and satires; the present café keeps his statue inside",
        "18 世纪 90 年代博卡热常在这家咖啡馆即兴吟诗、讥讽时人；如今的咖啡馆里立着他的雕像", ["pt-bocage-sonnets"]),
    ORIG("pt-brasileira", "Chiado and Café A Brasileira", "希亚多区与巴西人咖啡馆",
         "The Chiado is the fashionable hill of shops, cafés and theatres where Eça de Queirós's Lisbon shows itself off; Luísa drives down it in a cab on her way to her lover in Cousin Bazilio. Outside the Café A Brasileira, opened in 1905 and a haunt of Fernando Pessoa and his friends, sits Lagoa Henriques's bronze statue of the poet",
         "希亚多是里斯本的时髦街区，满是商店、咖啡馆和剧院，埃萨笔下的里斯本人爱在这里露面；《巴济里奥表兄》里，路易莎坐着马车从这里下坡去见情人。巴西人咖啡馆 1905 年开业，佩索阿和朋友们常来，门外坐着拉戈阿·恩里克斯为诗人塑的铜像", book_ids=["pt-pessoa-poems"]),
    ORIG("pt-janelas-verdes", "Rua das Janelas Verdes", "绿窗街",
         "The Maias opens with the family's Lisbon house, the Ramalhete, in the quarter of Janelas Verdes, a gloomy mansion with a sunflower panel in place of a coat of arms. Tradition points to a house on this street as its model",
         "《马亚一家》开篇写的就是这家人在里斯本的宅子“花束楼”，在绿窗街一带，是一座阴沉的大宅，门上不挂族徽，只有一块向日葵瓷砖。相传这条街上的一座房子就是它的原型"),
    ORIG("pt-rua-augusta", "Rua Augusta and the Baixa", "奥古斯塔街与下城",
         "Cesário Verde worked in his father's hardware shop in the Baixa, the grid of streets rebuilt after the earthquake. His long poem 'The Feeling of a Westerner' follows one evening's walk through these streets as the gas lamps are lit, down to the Tagus",
         "塞萨里奥·维尔德在父亲开在下城的五金店里做事；下城是大地震后重建的棋盘式街区。他的长诗《一个西方人的感受》写的是傍晚煤气灯亮起时在这些街上的一次漫步，一直走到特茹河边"),
    ORIG("pt-douradores", "Rua dos Douradores", "金匠街",
         "The street of Bernardo Soares, the assistant bookkeeper who 'writes' The Book of Disquiet: he works in an office here and rents a room on the same street; the office, he says, stands for Life, and his room for Art",
         "《不安之书》的“作者”、助理会计贝尔纳多·索阿雷斯的街：他在这条街上的一间办公室上班，也在这条街上租了一间屋子；他说，办公室代表“生活”，他的房间代表“艺术”"),
    PIL("pt-casa-pessoa", "Casa Fernando Pessoa, Campo de Ourique", "佩索阿故居（奥里克区）",
        "Pessoa lived in a flat in this building for the last fifteen years of his life, from 1920 to 1935. It is now a museum with his library, his bedroom and the trunk-full of papers that became his posthumous works",
        "佩索阿一生最后十五年（1920–1935）住在这栋楼的一套房间里。现在这里是纪念馆，保存着他的藏书、卧室，还有那一箱后来整理成遗作的手稿的故事", ["pt-pessoa-poems", "pt-disquiet"]),
    PIL("pt-martinho", "Café Martinho da Arcada, Praça do Comércio", "商业广场 · 拱廊下的马蒂纽咖啡馆",
        "Lisbon's oldest café, under the arcade of the riverside square. Pessoa came here almost daily in his last years and wrote at a table that is still kept for him; Message, the only book in Portuguese he published in his lifetime, came out in 1934",
        "里斯本最老的咖啡馆，在河边广场的拱廊下。佩索阿晚年几乎天天来，在一张桌子上写作，那张桌子至今为他留着；《使命》是他生前出版的唯一一本葡萄牙语诗集，1934 年问世", ["pt-mensagem", "pt-pessoa-poems"]),
    ORIG("pt-santa-catarina", "Miradouro de Santa Catarina", "圣卡塔琳娜观景台",
         "The terrace above the Tagus with the stone figure of Adamastor, the giant of the Cape from The Lusiads. In Saramago's novel Ricardo Reis rents a flat overlooking it, and the old men of the neighbourhood sit here every day reading the newspaper",
         "俯瞰特茹河的平台，立着《卢济塔尼亚人之歌》里好望角巨人阿达马斯托的石像。萨拉马戈的小说里，里卡多·雷耶斯租的房子正对着这里，街坊的老人们天天坐在这儿看报"),
    ORIG("pt-prazeres", "Prazeres Cemetery", "普拉泽雷斯墓园",
         "Pessoa was buried here in 1935 (his remains were moved to the Jerónimos in 1985). In The Year of the Death of Ricardo Reis, Reis comes to the grave soon after landing in Lisbon, and the dead poet later visits him",
         "佩索阿 1935 年葬在这里（1985 年迁往热罗尼莫斯修道院）。《里卡多·雷耶斯离世那年》里，雷耶斯到里斯本后不久就来看这座墓，后来死去的诗人也来拜访他"),
    PIL("pt-casa-bicos", "Casa dos Bicos (José Saramago Foundation)", "尖石宫（萨拉马戈基金会）",
        "The sixteenth-century house faced with diamond-pointed stones is the seat of the José Saramago Foundation. Saramago's ashes lie under the olive tree in front of it, brought from his native Azinhaga",
        "这座外墙布满菱形尖石的十六世纪宅邸是萨拉马戈基金会所在地。萨拉马戈的骨灰埋在门前那棵橄榄树下，树是从他的家乡阿济尼亚加移来的", ["pt-pequenas-memorias", "pt-ricardo-reis", "pt-memorial-do-convento"]),
    PIL("pt-graca", "Miradouro da Graça (Sophia de Mello Breyner Andresen viewpoint)", "恩典观景台（索菲亚观景台）",
        "The viewpoint by the Graça church was renamed after Sophia de Mello Breyner Andresen, who lived nearby; her bust and one of her poems about Lisbon stand here",
        "恩典教堂旁的这座观景台后来以索菲亚·安德雷森的名字命名，她曾住在附近；这里立着她的半身像和她写里斯本的一首诗", ["pt-menina-do-mar"]),
    ORIG("pt-santa-apolonia", "Santa Apolónia Station", "圣阿波罗尼亚火车站",
         "Lisbon's old riverside terminus for long-distance and international trains. In Night Train to Lisbon a Bern schoolteacher walks out of his classroom and takes the night train to a city he has never seen",
         "里斯本河边的老终点站，长途和国际列车到这里。《开往里斯本的夜车》里，伯尔尼的一位中学教师走出课堂，坐上夜车，去了一座从没见过的城市"),
    ORIG("pt-rodrigo-fonseca", "Rua Rodrigo da Fonseca", "罗德里戈·达·丰塞卡街",
         "In Pereira Maintains the culture page of the evening paper Lisboa has its one-room office in this street, with a fan that does not work and a caretaker who informs for the police. Here Pereira, in the heat of August 1938, translates French stories and files obituaries he cannot print",
         "《佩雷拉的证词》里，晚报《里斯本报》文化版的编辑室就是这条街上的一间屋子，电扇是坏的，看门的女人是警察的眼线。1938 年 8 月的酷暑里，佩雷拉在这里翻译法国小说，把登不出去的悼文存进档案"),
    # ---- around Lisbon ----
    ORIG("pt-seteais", "Seteais Palace, Sintra", "辛特拉 · 塞特艾斯宫",
         "In The Maias Carlos drives out to Sintra with the musician Cruges in the hope of meeting Maria Eduarda, and they walk to Seteais and look through its arch at the Pena palace on its rock",
         "《马亚一家》里，卡洛斯带着音乐家克鲁热斯坐车去辛特拉，盼着能遇见玛丽亚·爱德华达；两人走到塞特艾斯，透过拱门望见山岩上的佩纳宫"),
    ORIG("pt-sintra", "Sintra", "辛特拉",
         "The wooded hill town west of Lisbon that Byron, arriving in 1809, called a 'glorious Eden'. The road back to Lisbon is where two friends are stopped by masked men at the opening of The Mystery of the Sintra Road",
         "里斯本以西林木葱茏的山城，拜伦 1809 年来到这里，称它是“光辉的伊甸园”。《辛特拉公路之谜》开头，两个朋友就是在从这里回里斯本的公路上被蒙面人拦下的"),
    PIL("pt-lawrence", "Lawrence's Hotel, Sintra", "辛特拉 · 劳伦斯旅馆",
        "The inn where Byron stayed in July 1809, at the start of the journey that became Childe Harold's Pilgrimage; it claims to be the oldest hotel in the Iberian peninsula",
        "1809 年 7 月拜伦在这家旅店住过，那次旅行后来写成了《恰尔德·哈洛尔德游记》；旅馆自称是伊比利亚半岛最老的旅馆", ["pt-childe-harold"]),
    ORIG("pt-cabo-roca", "Cabo da Roca", "罗卡角",
         "The westernmost point of mainland Europe. A stone at the lighthouse carries the line with which Vasco da Gama, in Canto III of The Lusiads, describes Portugal: 'where the land ends and the sea begins'",
         "欧洲大陆的最西端。灯塔旁的石碑上刻着《卢济塔尼亚人之歌》第三章里达·伽马形容葡萄牙的那一句：“陆地在这里结束，海洋从这里开始”"),
    ORIG("pt-mafra", "Mafra National Palace", "马夫拉宫",
         "The vast palace-convent King João V vowed to build if he was given an heir. Baltasar and Blimunda tells of the tens of thousands of men conscripted to raise it, among them the one-handed soldier Baltasar, hauling a single giant stone from Pêro Pinheiro",
         "国王若昂五世许愿说，只要得到子嗣就修建这座巨大的宫殿兼修道院。《修道院纪事》写的是被征来修它的几万人，其中有独手士兵巴尔塔萨，他们从佩罗皮涅鲁拖来一整块巨石"),
    ORIG("pt-alhandra", "Alhandra", "阿良德拉",
         "The Tagus-side town of brickworks and tile kilns where Soeiro Pereira Gomes lived, working at the cement plant. Esteiros, dedicated 'to the children who never were children', follows a gang of boys who work in the brickyards along the tidal creeks",
         "特茹河边的砖瓦窑小镇，索埃罗·佩雷拉·戈梅斯曾住在这里，在水泥厂做事。《小港湾》题献给“那些从没当过孩子的孩子”，写的是一群在潮沟边砖厂里干活的男孩"),
    # ---- Setúbal ----
    PIL("pt-pragal", "Pragal, Almada", "阿尔马达 · 普拉加尔",
        "After twenty-one years in Asia, Fernão Mendes Pinto settled on a small estate at Pragal, across the Tagus from Lisbon, and there wrote the Peregrinação for his children. He died here in 1583; the book was printed in 1614",
        "在亚洲漂泊二十一年后，门德斯·平托在特茹河对岸普拉加尔的一处小庄园安了家，在这里为儿女们写下《远游记》。他 1583 年在此去世，书到 1614 年才印出来", ["pt-peregrinacao"]),
    PIL("pt-bocage", "Bocage Monument, Setúbal", "塞图巴尔 · 博卡热纪念碑",
        "Bocage was born in Setúbal in 1765. The column with his statue has stood in the square that bears his name since 1871",
        "博卡热 1765 年生在塞图巴尔。这根顶着他雕像的石柱 1871 年起就立在以他命名的广场上", ["pt-bocage-sonnets"]),
    ORIG("pt-palmela", "Palmela", "帕尔梅拉",
         "The Inquisitors' Manual turns on the farm at Palmela of Senhor Francisco, a minister of Salazar, where his son, his housekeeper, his mistress and his servants each tell what they saw of the old man's power and its ruin",
         "《审讯者手册》的中心是萨拉查的部长弗朗西斯科先生在帕尔梅拉的庄园；他的儿子、女管家、情妇和仆人轮流讲述他们看到的这位老人的权势和败落"),
    # ---- Santarém ----
    ORIG("pt-portas-sol", "Portas do Sol, Santarém", "圣塔伦 · 太阳门花园",
         "The garden inside the old Moorish citadel, on the cliff above the Tagus. Garrett's journey up the river in 1843 ends in Santarém, where he climbs to the Alcáçova and mourns the ruined churches",
         "悬崖上旧摩尔城堡里的花园，下面就是特茹河。1843 年加勒特沿河而上的旅行以圣塔伦为终点，他登上城堡，为破败的教堂叹息"),
    ORIG("pt-azinhaga", "Azinhaga", "阿济尼亚加",
         "Saramago was born in this village on the Almonda in 1922 and spent his childhood holidays with his grandparents Jerónimo and Josefa, landless peasants who took the weakest piglets into their bed in winter. Small Memories is his book about them",
         "1922 年萨拉马戈生在阿尔蒙达河边的这个村子，小时候放假就回来跟外祖父母热罗尼莫和若泽法住；他们是没有土地的农民，冬天把最弱的小猪抱到床上取暖。《小回忆》写的就是他们"),
    # ---- Leiria ----
    ORIG("pt-pinhal-leiria", "Pinhal de Leiria (the King's Pine Forest)", "莱里亚松林（国王松林）",
         "The great pine forest along the coast, which tradition says King Dinis planted to hold back the dunes and give timber for ships. His best-known song begins with a girl asking the flowers of the green pine for news of her lover",
         "海岸边的大片松林，相传是国王迪尼什为固沙、造船而种的。他最有名的一首歌谣，开头就是一个姑娘向青松的花打听情人的消息"),
    ORIG("pt-aljubarrota", "Battlefield of Aljubarrota", "阿尔茹巴罗塔古战场",
         "On 14 August 1385 the outnumbered army of João I and Nuno Álvares Pereira defeated the king of Castile here and secured Portugal's independence. Fernão Lopes's chronicle of the reign builds up to this afternoon",
         "1385 年 8 月 14 日，若昂一世和努诺·阿尔瓦雷斯·佩雷拉以少胜多，在这里打败卡斯蒂利亚国王，保住了葡萄牙的独立。费尔南·洛佩斯为这位国王写的编年史，高潮就是这个下午"),
    ORIG("pt-alcobaca", "Alcobaça Monastery", "阿尔科巴萨修道院",
         "The Cistercian abbey where Pedro I and Inês de Castro lie in facing tombs. Beckford came here in 1794 and wrote of the monks' kitchen with a stream running through it and the feasts they laid on for him",
         "熙笃会修道院，佩德罗一世和伊内斯·德·卡斯特罗的石棺在这里相对而放。1794 年贝克福德来访，写下修士们那间有溪水穿过的大厨房，还有他们为他摆的盛宴", book_ids=["pt-lusiadas"]),
    ORIG("pt-batalha", "Batalha Monastery", "巴塔利亚修道院",
         "Built to give thanks for Aljubarrota. Herculano's story 'The Vault' tells how the blind old architect Afonso Domingues, set aside for a foreign master whose vault collapses, rebuilds the chapter-house vault and sits beneath it for three days without food to prove it will hold",
         "为感谢阿尔茹巴罗塔的胜利而建。埃尔库拉诺的小说《拱顶》讲的是：年老失明的建筑师阿丰索·多明格斯被外国匠师取代，那人造的拱顶塌了，他重新建起议事厅的拱顶，并在下面不吃不喝坐了三天，证明它不会倒"),
    ORIG("pt-leiria-se", "Leiria Cathedral", "莱里亚主教座堂",
         "The Crime of Father Amaro opens with the death of the cathedral's parish priest in Leiria, and with the arrival of his young successor, Amaro Vieira, who takes lodgings in the house of the devout São Joaneira and her daughter Amélia",
         "《阿马罗神父的罪恶》开头就是莱里亚主教座堂教区神父的死，接替他的年轻神父阿马罗·维埃拉来到这里，住进虔诚的若阿内拉太太和女儿阿梅莉亚的家"),
    ORIG("pt-nazare", "Nazaré", "纳扎雷",
         "Raul Brandão's The Fishermen moves down the whole coast from Caminha to the Algarve; at Nazaré he watches the oxen haul the boats up the sand and the women in black wait on the beach",
         "劳尔·布兰当的《渔夫》从北边的卡米尼亚一路写到阿尔加维；在纳扎雷，他看着牛把渔船拖上沙滩，穿黑衣的女人们在海滩上等着"),
    # ---- Coimbra ----
    ORIG("pt-lagrimas", "Quinta das Lágrimas, Coimbra", "科英布拉 · 泪泉庄园",
         "The garden by the Mondego where, by tradition, Inês de Castro was killed in 1355 on the orders of the king, her lover's father; its Fountain of Tears is said to have sprung from her weeping. Camões tells her story in Canto III of The Lusiads",
         "蒙德古河边的花园，相传 1355 年伊内斯·德·卡斯特罗就是在这里被国王（她情人的父亲）下令杀害的，“泪泉”据说是她的眼泪化成的。卡蒙斯在《卢济塔尼亚人之歌》第三章讲了她的故事"),
    PIL("pt-torre-anto", "Torre de Anto, Coimbra", "科英布拉 · 安托塔",
        "The medieval tower on the old city wall where António Nobre lodged as a law student around 1890 and wrote poems that went into Só; it has been called 'Anto's tower' after him ever since",
        "老城墙上的中世纪塔楼。1890 年前后，读法律的安东尼奥·诺布雷寄住在这里，写下后来收进《孤独》的诗；此后人们就叫它“安托塔”", ["pt-so"]),
    # ---- Aveiro ----
    PIL("pt-julio-dinis", "Júlio Dinis House Museum, Ovar", "奥瓦尔 · 儒利奥·迪尼斯故居博物馆",
        "The young doctor Júlio Dinis, ill with tuberculosis, spent some months of 1863 in this small house of his aunt's in Ovar, and here began The Pupils of the Dean, his novel of village life",
        "年轻的医生儒利奥·迪尼斯患了肺结核，1863 年在奥瓦尔姑妈家的这座小房子里住了几个月，在这里开始写他的乡村小说《教区长的两个养女》", ["pt-pupilas"]),
    # ---- Porto ----
    ORIG("pt-cadeia-relacao", "Cadeia da Relação, Porto", "波尔图 · 上诉法院监狱",
         "Camilo Castelo Branco was held in this prison in 1860–61 on a charge of adultery, and wrote Doomed Love here in two weeks. The novel begins with the entry he found in the prison's register for his own uncle, Simão Botelho, aged eighteen. The building is now the Portuguese Centre of Photography",
         "1860 至 1861 年，卡米洛·卡斯特洛·布兰科因通奸罪被关在这座监狱里，两个星期写完了《毁灭之恋》。小说一开头就是他在监狱登记簿上查到的一条记录：他的叔叔西芒·博特略，十八岁。这座建筑现在是葡萄牙摄影中心"),
    ORIG("pt-ribeira", "Ribeira and the Rua dos Ingleses, Porto", "波尔图 · 河岸区与英国人街",
         "The riverside quarter where the British port-wine merchants had their offices, in the street then called Rua dos Ingleses (now Rua do Infante D. Henrique). In An English Family the merchant Mr Whitestone goes there every day, and his son Carlos would rather not",
         "河岸区是英国波特酒商人办公的地方，那条街当时叫英国人街（今天的恩里克王子街）。《一个英国家庭》里，商人怀特斯通先生天天去那里上班，他的儿子卡洛斯却宁可不去"),
    ORIG("pt-foz", "Foz do Douro", "杜罗河口",
         "Raul Brandão was born in 1867 at Foz do Douro, where the river meets the Atlantic, into a family of seamen; The Fishermen begins with his memories of the boats and drowned men of his childhood here",
         "1867 年劳尔·布兰当生在杜罗河入海口的一个航海人家；《渔夫》就从他童年在这里见过的渔船和溺死的人写起"),
    ORIG("pt-leca", "Leça da Palmeira", "莱萨达帕尔梅拉",
         "The fishing village north of Porto where António Nobre spent the summers of his childhood; its beach, its fishermen and the chapel of Boa Nova on the rocks return again and again in Só",
         "波尔图以北的渔村，安东尼奥·诺布雷小时候在这里过夏天；这里的海滩、渔民和礁石上的博阿诺瓦小教堂一再出现在《孤独》里"),
    PROTO("pt-tormes", "Casa de Tormes (Eça de Queiroz Foundation), Santa Cruz do Douro", "托尔梅斯之家（埃萨·德·克罗兹基金会）",
          "The manor house above the Douro that Eça's wife inherited, and which he visited in 1892, is the Tormes of The City and the Mountains, where Jacinto, bored of Paris, arrives to find no luggage and no beds, and a peasant supper of chicken broth and rice with broad beans that he never forgets",
          "杜罗河上方的这座庄园是埃萨的妻子继承的，他 1892 年来过；它就是《城与山》里的托尔梅斯：厌倦了巴黎的雅辛托来到这里，行李没到，床也没有，却吃到一顿让他终生难忘的农家晚饭：鸡汤和蚕豆饭"),
    PIL("pt-pascoaes", "Casa de Pascoaes, Amarante", "阿马兰特 · 帕斯科埃斯故居",
        "The family house at Gatão, facing the Marão, where Teixeira de Pascoaes lived and wrote almost all his life; he took his pen name from it",
        "加唐村面对马朗山的家宅，特谢拉·德·帕斯科埃斯几乎一辈子住在这里写作，他的笔名就取自这座宅子", ["pt-maranus"]),
    ORIG("pt-marao", "Serra do Marão", "马朗山",
         "The granite range between the Douro coast and Trás-os-Montes. Pascoaes's long poem Marânus is named for it: its hero wanders these heights with the shepherdess Eleonor and meets Saudade, the longing the poet took to be the soul of Portugal",
         "杜罗沿海和山后省之间的花岗岩山脉。帕斯科埃斯的长诗《马拉努斯》以它得名：主人公和牧羊女埃莱奥诺尔在山上游荡，遇见了“萨乌达德”——诗人认为那种思念就是葡萄牙的灵魂"),
    PROTO("pt-granja", "Praia da Granja", "格兰雅海滩",
          "The beach south of Porto where Sophia de Mello Breyner Andresen spent her childhood summers, in a white house facing the sea. It is the beach of The Little Girl from the Sea, where a boy finds a tiny girl dancing with a crab, an octopus and a fish in a rock pool",
          "波尔图以南的海滩，索菲亚·安德雷森小时候在这里一座面海的白房子里过夏天。《海的女儿》里的海滩就是这里：一个男孩在礁石间的水洼里发现一个小小的女孩，正和螃蟹、章鱼、鱼一起跳舞"),
    PIL("pt-vila-mea", "Vila Meã, Amarante", "阿马兰特 · 梅昂镇",
        "Agustina Bessa-Luís was born here in 1922. The farms of this country between the Douro and the Minho are the world of The Sibyl, in which the unmarried Quina makes the house of Vessada rich and becomes the oracle of her neighbours",
        "1922 年阿古斯蒂娜·贝萨-路易斯生在这里。杜罗河和米尼奥之间的这片农庄就是《女预言者》的世界：终身未嫁的基娜把韦萨达家的家业撑了起来，成了四邻求教的“女预言者”", ["pt-a-sibila"]),
    # ---- Braga ----
    PIL("pt-seide", "Casa de Camilo, São Miguel de Seide", "塞德 · 卡米洛故居",
        "Camilo Castelo Branco lived in this house with Ana Plácido from 1863, wrote most of his books in its study, and, going blind, shot himself here in 1890. It is now a museum",
        "1863 年起，卡米洛·卡斯特洛·布兰科和安娜·普拉西多住在这座房子里，大部分作品都在这里的书房写成；1890 年，眼睛快要失明的他在这里开枪自尽。现在是纪念馆", ["pt-amor-de-perdicao"]),
    # ---- Vila Real / Bragança ----
    PIL("pt-torga", "São Martinho de Anta", "圣马蒂纽德安塔",
        "Miguel Torga was born in this village of Trás-os-Montes in 1907 and came back to it all his life; he is buried here. The hard, proud villagers of Tales from the Mountain are his neighbours",
        "1907 年米格尔·托尔加生在山后省的这个村子，一生不断回来，死后也葬在这里。《山村故事》里那些倔强、骄傲的山里人就是他的乡亲", ["pt-contos-da-montanha"]),
    PIL("pt-mogadouro", "Mogadouro", "莫加多鲁",
        "Trindade Coelho was born in this small town in the far north-east in 1861; the shepherds, donkeys and village feasts of My Loves are those of his childhood here",
        "1861 年特林达德·科埃略生在东北边陲的这个小镇；《我的所爱》里的牧人、驴子和村里的节日，都是他在这里的童年记忆", ["pt-os-meus-amores"]),
    ORIG("pt-tuizelo", "Tuizelo", "图伊泽洛",
         "The remote village in the hills of Trás-os-Montes that all three parts of The High Mountains of Portugal lead to: a grieving man drives there in one of the country's first cars in 1904, and decades later a Canadian senator arrives with a chimpanzee",
         "山后省群山里的偏远村庄，《葡萄牙的高山》的三个故事都通向这里：1904 年，一个丧亲的男人开着全国最早的汽车之一来到这里；几十年后，一位加拿大参议员带着一只黑猩猩来了"),
    # ---- Viseu ----
    ORIG("pt-viseu", "Viseu", "维塞乌",
         "In Doomed Love the Botelho and Albuquerque families are neighbours and enemies in Viseu, and Simão and Teresa fall in love from their windows; it is in a street here that Simão shoots his rival",
         "《毁灭之恋》里，博特略家和阿尔布克尔克家在维塞乌是邻居，也是仇家，西芒和特蕾莎隔着窗户相爱；西芒就是在这里的街上开枪打死了情敌"),
    PIL("pt-serra-lapa", "Sanctuary of Nossa Senhora da Lapa, Sernancelhe", "塞尔南塞列 · 拉帕圣母朝圣地",
        "Aquilino Ribeiro, born nearby in 1885, went to school at the Jesuit college beside this mountain sanctuary. The highlanders of these hills are the people of When the Wolves Howl, who rise when the state takes their common land to plant forest",
        "阿基利诺·里贝罗 1885 年生在附近，小时候就在这座山间朝圣地旁的耶稣会学校读书。《狼嚎之时》写的就是这一带的山民：国家要把他们的公地收去造林，他们起来反抗", ["pt-quando-os-lobos-uivam"]),
    # ---- Portalegre ----
    PIL("pt-regio", "José Régio House Museum, Portalegre", "波塔莱格雷 · 若泽·雷吉奥故居博物馆",
        "José Régio taught at the Portalegre lyceum for more than thirty years and lodged in this old inn, which he filled with the crucifixes and folk art he collected. His 'Ballad of Portalegre' is about the house and the windy city",
        "若泽·雷吉奥在波塔莱格雷中学教了三十多年书，寄住在这座旧客栈里，屋里摆满他收集的十字架和民间艺术品。他的《波塔莱格雷之歌》写的就是这座房子和这座多风的城", ["pt-toada-de-portalegre"]),
    ORIG("pt-galveias", "Galveias", "加尔维亚什",
         "José Luís Peixoto's native village in the Alentejo, and the whole world of his novel: one January night in 1984 a nameless thing falls from the sky outside it, and afterwards the bread tastes of sulphur",
         "若泽·路易斯·佩肖托在阿连特茹的家乡，也是他这部小说的全部世界：1984 年 1 月的一个夜里，一个说不出名字的东西从天上掉在村外，从此面包里有了硫磺味"),
    # ---- Évora ----
    ORIG("pt-giraldo", "Praça do Giraldo, Évora", "埃武拉 · 吉拉尔多广场",
         "The arcaded square at the centre of Évora. In Apparition a young teacher, Alberto Soares, arrives in the white city in September to take up a post at the lyceum, and his questions about death unsettle the family that takes him in",
         "埃武拉市中心带拱廊的广场。《显现》里，年轻教师阿尔贝托·索阿雷斯九月来到这座白色的城市，到中学任教；他关于死亡的追问搅乱了接纳他的那一家人"),
    PIL("pt-vila-vicosa", "Vila Viçosa", "维索萨镇",
        "Florbela Espanca was born in this marble town of the Alentejo in 1894 and is buried here. Heath in Bloom, her last book of sonnets, was published a few weeks after her death in 1930",
        "1894 年弗洛贝拉·埃斯潘卡生在阿连特茹这座大理石小城，如今也葬在这里。她最后一本十四行诗集《繁花的荒原》在她 1930 年去世几周后出版", ["pt-charneca-em-flor"]),
    ORIG("pt-lavre", "Lavre", "拉夫雷",
         "In 1976 Saramago, out of work, came to live among the farm labourers of Lavre and listened to their stories. Raised from the Ground, set in 'Monte Lavre', follows three generations of the Mau-Tempo family from hunger and beatings to the occupation of the great estates",
         "1976 年，失业的萨拉马戈来到拉夫雷，住在农业工人中间，听他们讲自己的事。《大地起义》的背景“拉夫雷山”就是这里，写的是“坏天气”一家三代人，从挨饿挨打到占领大庄园"),
    # ---- Beja ----
    ORIG("pt-beja-convento", "Convent of Nossa Senhora da Conceição, Beja", "贝雅 · 圣母无染原罪修道院",
         "The convent of the nun Mariana Alcoforado, to whom the five love letters published in Paris in 1669 were long attributed; she writes of the balcony from which Mértola can be seen. Three centuries later the 'Three Marias' answered her in New Portuguese Letters, which was banned and put on trial. The convent is now the regional museum",
         "修女玛丽安娜·阿尔科福拉多的修道院；1669 年在巴黎出版的五封情书长期被认为是她写的，信里提到那个能望见梅尔图拉的阳台。三百年后，“三位玛丽亚”用《新葡萄牙书简》回应她，书被查禁，作者受审。修道院现在是地区博物馆"),
    # ---- Azores ----
    PIL("pt-antero", "Campo de São Francisco, Ponta Delgada", "蓬塔德尔加达 · 圣方济各广场",
        "Antero de Quental was born in Ponta Delgada in 1842. On 11 September 1891 he sat down on a bench in this square, by the wall of the Esperança convent, and shot himself; an anchor and the word 'Esperança' are on the wall above the spot",
        "安特罗·德·肯塔尔 1842 年生在蓬塔德尔加达。1891 年 9 月 11 日，他在这个广场上、希望修道院墙边的一张长椅上坐下，开枪自尽；那处墙上有一只锚和“希望”一词", ["pt-antero-sonnets"]),
    ORIG("pt-corvo", "Corvo", "科尔沃岛",
         "The smallest and most remote of the Azores. Raul Brandão spent the summer of 1924 among the islands, and the chapter on Corvo, a single village of herdsmen who share everything and lock nothing, is the heart of The Unknown Islands",
         "亚速尔群岛中最小、最偏远的一座。1924 年夏天劳尔·布兰当在群岛间旅行，《陌生的岛屿》里最核心的一章写的就是科尔沃：岛上只有一个牧人的村子，什么都共有，家家不上锁"),
    ORIG("pt-horta", "Horta, Faial", "法亚尔岛 · 奥尔塔",
         "Stormy Isles is set in Horta in 1917–19, among the old families, the whalers and the staff of the transatlantic cable stations, with the cone of Pico across the channel. Margarida Clark Dulmo, torn between duty to her ruined family and her own wishes, is its heroine",
         "《海峡的坏天气》写的是 1917 至 1919 年的奥尔塔：世家、捕鲸人、越洋电缆站的职员，海峡对面是皮库岛的火山锥。女主人公玛格丽达·克拉克·杜尔莫在败落家族的责任和自己的愿望之间挣扎"),
]

# Two real points fall in water on the simplified map (the Tagus estuary, the south coast of São Miguel): the district is named.
for _pid, _reg in (("pt-alhandra", "PT-11"), ("pt-antero", "PT-20")):
    next(p for p in places if p["id"] == _pid)["region"] = _reg

# ============================== lines ==============================
lu20 = raw(L3, '"Eis aqui, quase cume da cabeça', "repousa no Oceano.")
lu120 = raw(L3, '"Estavas, linda Inês', "escrito tinhas.")
lu87 = raw(L4, '"Partimo-nos assim do santo templo', "ao mundo dado.")
STAN = " (the stanza number left out)"
can5 = raw(CAN5, "À peine ont-ils mis le pied", "écrasés sous des ruines.")
can6 = raw(CAN6, "Après le tremblement de terre", "empêcher la terre de trembler.")
assert "\xa0;" in can5 and "\xa0;" in can6
NB = " (the no-break space before ; written as a space)"

lines = [
    Q("pt-dinis-1", "pt-cantigas-dinis", "pt-pinhal-leiria", "'Ai flores, ai flores do verde pino', stanzas 1–2", "《青松的花啊》第一、二节", "Portuguese", DIN,
      "\n".join(l.strip() for l in raw(DIN, "Ai flores, ai flores do verde pino", "Ai Deus, e u é?").split("\n")) + "\n"
      + "\n".join(l.strip() for l in raw(DIN, "Ai, flores, ai flores do verde ramo", "Ai Deus, e u é?").split("\n")),
      ["verde pino"],
      "O flowers, O flowers of the green pine,\ndo you have news of my friend?\nO God, where is he?\nO flowers, O flowers of the green bough,\ndo you have news of my beloved?\nO God, where is he?",
      ["green pine"],
      "花啊，青松的花啊，\n你们可有我朋友的消息？\n天主啊，他在哪里？\n花啊，绿枝的花啊，\n你们可有我爱人的消息？\n天主啊，他在哪里？",
      ["青松"], " (the lines' indent and the dash before the first line left out)"),
    Q("pt-lus-1", "pt-lusiadas", "pt-cabo-roca", "Canto III, stanza 20", "第三章第 20 节", "Portuguese", L3, lu20, ["Onde a terra se acaba e o mar começa"],
      "'See here, almost the crown of the head\nof all Europe, the Lusitanian kingdom,\nwhere the land ends and the sea begins,\nand where Phoebus goes to rest in the Ocean.'",
      ["where the land ends and the sea begins"],
      "“看这里，几乎就在整个欧洲的头顶，\n是卢济塔尼亚王国，\n陆地在这里结束，海洋从这里开始，\n太阳神也在这片大洋里安歇。”",
      ["陆地在这里结束，海洋从这里开始"], STAN),
    Q("pt-lus-2", "pt-lusiadas", "pt-lagrimas", "Canto III, stanza 120", "第三章第 120 节", "Portuguese", L3, lu120, ["Nos saudosos campos do Mondego"],
      "'You were at peace, lovely Inês,\ngathering the sweet fruit of your years,\nin that deception of the soul, glad and blind,\nthat fortune does not let last long,\nin the wistful fields of the Mondego,\nnever dry of the tears of your beautiful eyes,\nteaching the hills and the little grasses\nthe name you bore written in your heart.'",
      ["in the wistful fields of the Mondego"],
      "“美丽的伊内斯，你曾安然度日，\n采摘着青春年华的甜美果实，\n沉浸在心灵那快乐而盲目的错觉里，\n可命运不让它长久；\n在蒙德古河畔令人思念的原野上，\n你美丽的眼睛泪水从不曾干，\n你教给山峦和小草的，\n是那个刻在你心上的名字。”",
      ["蒙德古河畔令人思念的原野"], STAN),
    Q("pt-lus-3", "pt-lusiadas", "pt-jeronimos", "Canto IV, stanza 87", "第四章第 87 节", "Portuguese", L4, lu87, ["santo templo", "nas praias do mar"],
      "'So we set out from the holy temple\nthat stands on the shore of the sea\nand bears, as a sign, the name of the land\nwhere God was given to the world in flesh.'",
      ["the holy temple", "on the shore of the sea"],
      "“我们就这样离开了那座圣殿，\n它坐落在大海的沙滩上，\n殿名取自那片土地，作为表记——\n天主正是在那里降生为人。”",
      ["圣殿", "大海的沙滩"], STAN),
    Q("pt-can-1", "candide", "pt-carmo", "Chapter 5", "第五章", "French", CAN5, can5.replace("\xa0;", " ;"), ["les maisons s’écroulent"],
      "Scarcely have they set foot in the city, weeping for the death of their benefactor, when they feel the earth tremble beneath their feet; the sea rises boiling in the harbour and breaks the ships that lie at anchor. Whirlwinds of flame and ash cover the streets and public squares; the houses collapse, the roofs are thrown down upon the foundations, and the foundations are scattered; thirty thousand inhabitants of every age and of both sexes are crushed under the ruins.",
      ["the houses collapse"],
      "他们一边哭着恩人的死，一边刚踏进城里，就觉得脚下的大地在震动；港口里海水沸腾般涌起，把停泊的船只撞得粉碎。火焰和灰烬的旋风盖住了街道和广场；房屋倒塌，屋顶砸在地基上，地基也四散崩裂；三万居民，不分男女老幼，都被压死在废墟下。",
      ["房屋倒塌"], NB),
    Q("pt-can-2", "candide", "pt-rossio", "Chapter 6", "第六章", "French", CAN6, can6.replace("\xa0;", " ;"), ["Lisbonne", "un bel auto-da-fé"],
      "After the earthquake that had destroyed three quarters of Lisbon, the wise men of the country had found no more effective way of preventing total ruin than to give the people a fine auto-da-fé; it was decided by the University of Coimbra that the spectacle of a few persons burned over a slow fire, with great ceremony, is an infallible secret for keeping the earth from quaking.",
      ["Lisbon", "a fine auto-da-fé"],
      "地震毁掉了四分之三的里斯本之后，当地的贤人们想不出更有效的办法来防止全城毁灭，只有给老百姓办一场漂亮的火刑仪式；科英布拉大学断定，隆重其事地用文火烧死几个人，是防止地震万无一失的秘方。",
      ["里斯本", "一场漂亮的火刑仪式"], NB),
    Q("pt-byron-1", "pt-childe-harold", "pt-sintra", "Canto I, stanza 18", "第一章第 18 节", "English", BYRON,
      raw(BYRON, "Lo! Cintra's glorious Eden intervenes", "unlocked Elysium's gates."), ["Cintra's glorious Eden"], "", [],
      "看！辛特拉那光辉的伊甸园出现在眼前，\n山峦与幽谷交错成斑斓的迷宫。\n唉！什么样的手能运笔挥毫，\n追得上眼前展开的景色的一半？\n这景色在凡人眼里光彩夺目，\n胜过那位诗人所讲述的一切——\n他曾向敬畏的世人打开了极乐世界的大门。",
      ["辛特拉那光辉的伊甸园"], original=True),
    Q("pt-abo-1", "pt-lendas-e-narrativas", "pt-batalha", "'The Vault', chapter 1", "《拱顶》第一章", "Portuguese", ABO,
      raw(ABO, "No adro do mosteiro de Santa Maria da Victoria", "que entoava os kyries."), ["mosteiro de Santa Maria da Victoria, vulgarmente chamado da Batalha"],
      "In the churchyard of the monastery of Santa Maria da Vitória, commonly called Batalha, the people were swarming as they went into the new church, which had only lately begun to serve for religious solemnities. The Dominican friars, to whom King João I had given this magnificent monastery, were singing the mass of the day beneath those high vaults, where the sounds of the organ echoed, and the voice of the celebrant intoning the kyries.",
      ["the monastery of Santa Maria da Vitória, commonly called Batalha"],
      "在胜利圣母修道院——人们通常叫它巴塔利亚修道院——的前庭里，百姓熙熙攘攘地涌进新教堂，这座教堂用来举行宗教典礼还没有多久。国王若昂一世把这座宏伟的修道院赐给了多明我会的修士，此刻他们正在高高的拱顶下唱当天的弥撒，管风琴声和主祭吟唱垂怜经的声音在拱顶间回荡。",
      ["胜利圣母修道院——人们通常叫它巴塔利亚修道院"]),
    Q("pt-via-1", "pt-viagens", "pt-portas-sol", "Chapter 27", "第二十七章", "Portuguese", VIA,
      joined(VIA, "Eram as últimas horas do dia", "são os seus olivaes."), ["Santarem"],
      "It was the last hours of the day when we came to the foot of the paved road that leads up to the heights of Santarém. The few people about, the ill-kept kitchen gardens and orchards, the ruined country houses, all showed that we were near a great town fallen and forsaken. Yet the finest of its ornaments and glories outside the walls the noble town still has; they have not quite destroyed it: its olive groves.",
      ["Santarém"],
      "我们来到通往圣塔伦高处的石板坡道脚下时，已是一天中最后的时光。行人稀少，菜园和果园无人打理，乡间的房舍破败不堪，一切都说明我们走近了一座衰落、被人遗弃的大城。不过，这座高贵的城在城外最美的装点和荣耀还在，没有被完全毁掉：那就是它的橄榄林。",
      ["圣塔伦"], JOINED),
    Q("pt-amor-1", "pt-amor-de-perdicao", "pt-cadeia-relacao", "Preface", "序", "Portuguese", AMOR,
      joined(AMOR, "Folheando os livros de antigos assentamentos", "o seguinte:"), ["cadêas da Relação do Porto"],
      "Leafing through the books of old entries in the registry of the prison of the Relação in Porto, I read, in the one recording prisoners admitted from 1803 to 1805, on folio 232, the following:",
      ["the prison of the Relação in Porto"],
      "我在波尔图上诉法院监狱的档案室里翻阅旧登记簿，在记载 1803 至 1805 年入狱犯人的那一本的第 232 页上，读到这样一条：",
      ["波尔图上诉法院监狱"], JOINED),
    Q("pt-fam-1", "pt-familia-inglesa", "pt-ribeira", "Chapter 7", "第七章", "Portuguese", FAM,
      raw(FAM, "—Mas é tão monotono!", "abomino-a."), ["rua dos Inglezes"],
      "'But it is so monotonous! You have no idea! I hate that Rua dos Ingleses, Jenny; I loathe it.'",
      ["Rua dos Ingleses"],
      "“可是那儿太单调了！你根本想不到！我讨厌那条英国人街，珍妮；我恨透它了。”",
      ["英国人街"]),
    Q("pt-amaro-1", "pt-padre-amaro", "pt-leiria-se", "Chapter 1, opening", "第一章开篇", "Portuguese", AMARO,
      raw(AMARO, "Foi no domingo de Páscoa", "o comilão dos comilões."), ["Leiria", "o pároco da Sé"],
      "It was on Easter Sunday that it became known in Leiria that the parish priest of the cathedral, José Miguéis, had died in the small hours of an apoplexy. The priest was a full-blooded, well-fed man, who passed among the clergy of the diocese for the glutton of gluttons.",
      ["Leiria", "the parish priest of the cathedral"],
      "复活节那个星期天，莱里亚城里传开了消息：主教座堂的教区神父若泽·米盖斯凌晨中风死了。这位神父血气旺盛，养得肥壮，在教区的神职人员中间是出了名的饕餮之王。",
      ["莱里亚", "主教座堂的教区神父"]),
    Q("pt-primo-1", "pt-primo-basilio", "pt-brasileira", "Chapter 6", "第六章", "Portuguese", PRIMO,
      joined(PRIMO, "Mas no Largo de Camões reparou", "vida amorosa!"), ["ao descer o Chiado"],
      "But in the Largo de Camões she noticed that the fellow with the long goatee, the one from the Passeio, was following her with the obstinacy of a cockerel; she took a cab at once. And as she went down the Chiado she felt a delicious sensation at being carried so swiftly to her lover, and even looked with a certain disdain at the people passing by in the bustle of trivial life, while she was on her way to so romantic an hour of the life of love!",
      ["as she went down the Chiado"],
      "可是到了卡蒙斯广场，她发觉那个留着长山羊胡的家伙——就是在散步大道上见过的那个——像公鸡一样死死跟着她；她马上叫了一辆马车。车沿着希亚多往下走时，她觉得就这样被飞快地送到情人那里，真是美妙极了，甚至带着几分轻蔑看着那些在平庸生活里来来往往的行人——而她，正要去度过爱情生活中那样浪漫的一个钟头！",
      ["沿着希亚多往下走"], JOINED),
    Q("pt-maias-1", "pt-os-maias", "pt-janelas-verdes", "Chapter 1, opening", "第一章开篇", "Portuguese", MAIAS,
      raw(MAIAS, "A casa que os Maias vieram habitar em Lisboa", "ou simplesmente o Ramalhete."), ["bairro das Janellas Verdes", "casa do Ramalhete"],
      "The house in Lisbon to which the Maias came to live in the autumn of 1875 was known in the neighbourhood of the Rua de São Francisco de Paula, and throughout the quarter of Janelas Verdes, as the house of the Ramalhete, or simply the Ramalhete.",
      ["the quarter of Janelas Verdes", "the house of the Ramalhete"],
      "1875 年秋天马亚一家搬来里斯本住的那座房子，在圣弗朗西斯科·德·保拉街一带，乃至整个绿窗街区，都被叫做“花束楼”，或者干脆就叫“花束”。",
      ["整个绿窗街区", "花束楼"]),
    Q("pt-ces-1", "pt-cesario-verde", "pt-rua-augusta", "'The Feeling of a Westerner', I, stanzas 1–2", "《一个西方人的感受》第一部分第一、二节", "Portuguese", CES,
      raw(CES, "Nas nossas ruas, ao anoitecer,", "monótona e londrina."), ["Nas nossas ruas", "o Tejo"],
      "In our streets, as night falls,\nthere is such gloom, such melancholy,\nthat the shadows, the bustle, the Tagus, the sea air\nwake in me an absurd desire to suffer.\nThe sky seems low and made of mist,\nthe escaping gas sickens me, disturbs me;\nand the buildings, with their chimneys, and the crowd\nare veiled in a monotonous, London colour.",
      ["In our streets", "the Tagus"],
      "在我们的街道上，夜幕降临时，\n是那样阴沉，那样忧郁，\n暗影、喧嚷、特茹河、海的气息\n在我心里唤起一种荒唐的受苦的渴望。\n天空显得低矮，像一片薄雾，\n漏出的煤气叫我恶心，叫我不安；\n那些带烟囱的楼房，还有人群，\n都蒙上一层单调的、伦敦般的颜色。",
      ["在我们的街道上", "特茹河"]),
    Q("pt-serras-1", "pt-cidade-e-serras", "pt-tormes", "Chapter 8", "第八章", "Portuguese", SERRAS,
      raw(SERRAS, "Parou lentamente á beira dos colxões", "quem assassinaste?..."), ["Tormes"],
      "He stopped slowly at the edge of the mattresses and, gravely, as if he were announcing his marriage or his death, let fall upon me this formidable declaration:\n'Zé Fernandes, I am leaving for Tormes.'\nThe jump with which I sat up shook old Dom Galião's stout blackwood bed:\n'For Tormes? Oh Jacinto, whom have you murdered?...'",
      ["Tormes"],
      "他慢慢走到床垫边停下，神情庄重，仿佛要宣布自己的婚事或者死讯，向我抛下这句惊人的话：\n“泽·费尔南德斯，我要动身去托尔梅斯。”\n我猛地坐起来，把老堂加利昂那张结实的黑木床都震动了：\n“去托尔梅斯？哎呀，雅辛托，你杀了谁啦？……”",
      ["托尔梅斯"]),

    # ---------- scene notes ----------
    S("pt-cronica-s1", "pt-cronica-joao-i", "pt-aljubarrota", "Part 2, the battle of Aljubarrota", "第二部，阿尔茹巴罗塔之战",
      "Fernão Lopes, keeper of the royal archives, tells how the bastard Master of Avis was raised to the throne by the people of Lisbon in 1383–85, and how on a hot August afternoon his small army, drawn up on foot behind ditches and pits on a ridge chosen by the Constable Nuno Álvares Pereira, broke the charge of the Castilian cavalry at Aljubarrota.",
      "王室档案保管人费尔南·洛佩斯讲述了 1383 至 1385 年里斯本百姓怎样把私生子阿维什骑士团团长拥上王位，又讲到八月一个炎热的下午，他那支人数不多的军队在统帅努诺·阿尔瓦雷斯·佩雷拉选定的山脊上，下马列阵于壕沟和陷坑之后，在阿尔茹巴罗塔挡住了卡斯蒂利亚骑兵的冲锋。",
      ["Aljubarrota"], ["阿尔茹巴罗塔"], W + "Fern%C3%A3o_Lopes"),
    S("pt-barca-s1", "pt-barca-do-inferno", "pt-teatro-dmaria", "Throughout", "全剧",
      "On a river bank two boats are waiting, one for Hell with the Devil as ferryman, one for Paradise with an Angel. The newly dead arrive one by one, a nobleman with his page and chair, a moneylender, a cobbler, a friar with his mistress, a bawd, a corrupt judge, and each argues that he belongs in the Angel's boat. Only a simpleton and four knights who died fighting for the faith are let aboard it.",
      "河岸边等着两条船，一条开往地狱，魔鬼撑船；一条开往天堂，天使掌舵。刚死的人一个个到来：带着侍从和椅子的贵族、放高利贷的、鞋匠、带着情妇的修士、老鸨、贪赃的法官，个个都争辩说自己该上天使的船。最后只有一个傻子和四个为信仰战死的骑士上了那条船。",
      ["two boats"], ["两条船"], W + "Auto_da_Barca_do_Inferno"),
    S("pt-peregrinacao-s1", "pt-peregrinacao", "pt-pragal", "Throughout", "全书",
      "Mendes Pinto tells how in twenty-one years in the East he was 'thirteen times a captive and seventeen times sold': shipwrecked, enslaved, a pirate with António de Faria on the China coast, among the first Europeans to reach Japan, and a companion of Francis Xavier. Back in Portugal with nothing, he wrote it all down at Pragal for his children.",
      "门德斯·平托讲述他在东方的二十一年里“十三次被俘，十七次被卖”：遇过海难，当过奴隶，跟着安东尼奥·德·法里亚在中国沿海做过海盗，是最早到达日本的欧洲人之一，还做过沙勿略的同伴。他两手空空回到葡萄牙，在普拉加尔把这一切写下来留给儿女。",
      ["Pragal"], ["普拉加尔"], W + "Fern%C3%A3o_Mendes_Pinto"),
    S("pt-letters-s1", "pt-portuguese-letters", "pt-beja-convento", "The five letters", "五封信",
      "In five letters a Portuguese nun writes to the French officer who seduced her and has gone home. She reproaches him, forgives him, begs for a longer letter, and in one of them tells how a sister led her out onto the balcony from which Mértola can be seen, where she first saw him ride past, and how the memory made her weep for the rest of the day.",
      "一位葡萄牙修女给引诱了她又回国去的法国军官写了五封信。她责备他，原谅他，求他写一封长一点的信；在其中一封信里，她说一位修女姐妹带她到那个能望见梅尔图拉的阳台上去散心，她当初就是在那里第一次看见他骑马经过，这回忆让她哭了一整天。",
      ["the balcony from which Mértola can be seen"], ["能望见梅尔图拉的阳台"], W + "Letters_of_a_Portuguese_Nun"),
    S("pt-fielding-s1", "pt-voyage-to-lisbon", "pt-english-cemetery", "Throughout", "全书",
      "Dropsical and unable to walk, Fielding is hoisted aboard the Queen of Portugal at Rotherhithe in June 1754 with his wife and daughter. Contrary winds keep the ship for weeks on the English coast, and he fills the journal with the captain, the landladies who overcharge him and the price of fish, before the ship at last runs up the Tagus to Lisbon.",
      "1754 年 6 月，患水肿、无法行走的菲尔丁在罗瑟海斯被人吊上“葡萄牙王后号”，同行的有妻子和女儿。逆风把船在英国海岸边困了好几个星期，他就在日记里写船长，写乱收费的女房东，写鱼价，直到船终于驶进特茹河，到了里斯本。",
      ["Lisbon"], ["里斯本"], W + "The_Journal_of_a_Voyage_to_Lisbon"),
    S("pt-bocage-s1", "pt-bocage-sonnets", "pt-bocage", "The self-portrait sonnet and others", "自画像十四行诗及其他",
      "In his best-known sonnet Bocage draws himself: thin, blue-eyed, dark-faced, with large feet, a tall nose, quick to anger and to love, and unable to stay in one place. Other sonnets look back to the banks of the Sado at Setúbal where he was born, mourn his wasted years, and, at the end, take back his blasphemies.",
      "在最有名的那首十四行诗里，博卡热给自己画了一幅像：瘦削，蓝眼睛，脸色黝黑，大脚，高鼻子，易怒也易动情，在哪儿都待不住。别的十四行诗里，他回望故乡塞图巴尔的萨杜河岸，痛惜虚度的年华，临终时又收回了自己渎神的话。",
      ["Setúbal"], ["塞图巴尔"], W + "Manuel_Maria_Barbosa_du_Bocage"),
    S("pt-bocage-s2", "pt-bocage-sonnets", "pt-cafe-nicola", "Lisbon years", "里斯本岁月",
      "Back from India and Macau in 1790, Bocage became the wit of Lisbon's cafés, above all the Nicola on the Rossio, improvising verses on any subject thrown at him and satires on his rivals; his freethinking poems put him in the prisons of the police and the Inquisition in 1797.",
      "1790 年从印度和澳门回来后，博卡热成了里斯本咖啡馆里的才子，尤其是罗西奥广场上的尼古拉咖啡馆：别人随口出个题目，他就即兴成诗，还写诗挖苦对手；1797 年，他那些自由思想的诗把他送进了警察和宗教裁判所的监狱。",
      ["the Nicola"], ["尼古拉咖啡馆"], W + "Manuel_Maria_Barbosa_du_Bocage"),
    S("pt-beckford-s1", "pt-beckford-alcobaca", "pt-alcobaca", "Days 4–6", "第四至第六天",
      "In June 1794 the rich English exile William Beckford rides out from Lisbon with two worldly priors on a twelve-day excursion. At Alcobaça the monks lead him into the most distinguished temple of gluttony in Europe, a kitchen with a brook running through it full of live fish, and feast him for days; he also stands before the tombs of Pedro and Inês.",
      "1794 年 6 月，流亡在外的英国富豪威廉·贝克福德带着两位通晓世故的修道院长从里斯本出发，作了一次十二天的旅行。在阿尔科巴萨，修士们把他领进全欧洲最气派的“饕餮殿堂”——一间有小溪穿过、溪里养着活鱼的厨房，一连款待他好几天；他还在佩德罗和伊内斯的墓前驻足。",
      ["Alcobaça"], ["阿尔科巴萨"], W + "William_Beckford_(novelist)"),
    S("pt-amor-s2", "pt-amor-de-perdicao", "pt-viseu", "Chapters 1–10", "第一至十章",
      "Simão Botelho, the wild son of a magistrate, and Teresa de Albuquerque, daughter of the family his own is at law with, grow up in neighbouring houses in Viseu and fall in love. Her father shuts her in a convent to make her marry her cousin Baltasar; Simão shoots Baltasar dead in the street and gives himself up.",
      "法官的儿子西芒·博特略生性狂放，特蕾莎·德·阿尔布克尔克则是跟他家打官司的那家人的女儿；两人在维塞乌相邻的房子里长大，相爱了。她父亲把她关进修道院，逼她嫁给表兄巴尔塔萨；西芒在街上开枪打死了巴尔塔萨，然后自首。",
      ["Viseu"], ["维塞乌"], W + "Amor_de_Perdi%C3%A7%C3%A3o"),
    S("pt-pupilas-s1", "pt-pupilas", "pt-julio-dinis", "Throughout", "全书",
      "In a village of the north, the old priest has brought up two orphan half-sisters, grave Margarida and lively Clara. Daniel, a farmer's son, comes home from Porto a doctor, forgets his childhood promise to Margarida and flirts with Clara, who is engaged to his brother; Margarida takes the blame for a night meeting to save her sister's name.",
      "北方的一个村子里，老神父把两个同父异母的孤女抚养成人：稳重的玛格丽达和活泼的克拉拉。农家子弟达尼埃尔从波尔图学医归来，忘了小时候对玛格丽达的承诺，去招惹已同他哥哥订婚的克拉拉；为了保住妹妹的名声，玛格丽达把一次夜间幽会的过错揽到了自己身上。",
      ["Margarida"], ["玛格丽达"], W + "J%C3%BAlio_Dinis"),
    S("pt-misterio-s1", "pt-misterio-sintra", "pt-sintra", "The doctor's first letter", "医生的第一封信",
      "A doctor writes to a Lisbon newspaper: riding back from Sintra with a friend at dusk, he was stopped on the road by masked men, blindfolded, and driven to a house where a man lay dead on a sofa. The letters that followed in the Diário de Notícias in 1870 were taken for fact by many readers.",
      "一位医生给里斯本的报纸写信说：黄昏时他和朋友从辛特拉骑马回来，在公路上被几个蒙面人拦住，蒙上眼睛，用马车带到一座房子里，那里的沙发上躺着一个死人。1870 年《新闻日报》上接连刊出的这些信，被不少读者当成了真事。",
      ["Sintra"], ["辛特拉"], W + "The_Mystery_of_the_Sintra_Road"),
    S("pt-maias-s2", "pt-os-maias", "pt-seteais", "Chapter 8", "第八章",
      "Having glimpsed Maria Eduarda in Lisbon, Carlos da Maia hears that she has gone to Sintra and drives out with the absent-minded composer Cruges. They walk under the trees to Seteais and look through its arch; she has already left, and Cruges forgets the cheese tarts he promised his mother.",
      "卡洛斯·达·马亚在里斯本瞥见过玛丽亚·爱德华达，听说她去了辛特拉，就带着心不在焉的作曲家克鲁热斯坐车赶去。两人在树荫下走到塞特艾斯，透过拱门眺望；她已经走了，克鲁热斯也忘了答应给母亲带的奶酪小饼。",
      ["Seteais"], ["塞特艾斯"], W + "Os_Maias"),
    S("pt-antero-s1", "pt-antero-sonnets", "pt-antero", "Throughout", "全书",
      "The sonnets follow a mind through thirty years: the student rebel of Coimbra who believed in reason and revolution, the pessimist who found the universe empty, and the sick man who at last writes of resting 'in the hand of God, in his right hand'. Antero arranged them himself as the autobiography of his thought.",
      "这些十四行诗记录了一个头脑三十年的历程：科英布拉那个相信理性和革命的学生领袖，后来发觉宇宙空无一物的悲观者，最后是那个写下“在上帝的手里，在他的右手里”安息的病人。安特罗亲自把它们编排成自己思想的自传。",
      ["in the hand of God"], ["在上帝的手里"], W + "Antero_de_Quental"),
    S("pt-meus-amores-s1", "pt-os-meus-amores", "pt-mogadouro", "Throughout", "全书",
      "Short tales of the villages of Trás-os-Montes, told with tenderness: an old donkey sold at the fair who finds his way home, a mother's lullaby, a shepherd boy, the prayers and games of the author's own childhood.",
      "讲山后省乡村的短篇故事，笔调温柔：集市上被卖掉又自己找路回家的老驴，母亲的摇篮曲，放羊的男孩，还有作者自己童年的祷告和游戏。",
      ["Trás-os-Montes"], ["山后省"], "https://pt.wikipedia.org/wiki/Jos%C3%A9_Francisco_Trindade_Coelho"),
    S("pt-so-s1", "pt-so", "pt-leca", "Throughout", "全书",
      "Written largely in Paris, where Nobre was a homesick student, Só calls up the Portugal of his childhood: the fishermen and processions of Leça, his nurse, the saints' days, the names of the boats. He called it 'the saddest book there is in Portugal'.",
      "《孤独》大部分写于巴黎，当时诺布雷是个想家的留学生；书里召唤的是他童年的葡萄牙：莱萨的渔民和宗教游行，他的奶妈，圣徒的节日，渔船的名字。他说这是“葡萄牙最悲伤的一本书”。",
      ["Leça"], ["莱萨"], W + "Ant%C3%B3nio_Nobre"),
    S("pt-maranus-s1", "pt-maranus", "pt-marao", "Throughout", "全诗",
      "Marânus, a man of the Marão, loves the shepherdess Eleonor and wanders the mountain in search of something beyond her. On the heights he meets Saudade, a veiled woman who is at once memory and desire, and their union gives birth to a new god for Portugal.",
      "马拉努斯是马朗山的人，爱着牧羊女埃莱奥诺尔，却又在山上游荡，寻找比她更远的东西。在高处他遇见了“萨乌达德”——一个蒙着面纱的女人，既是回忆又是渴望；两人的结合为葡萄牙生下了一位新的神。",
      ["Marão"], ["马朗山"], W + "Teixeira_de_Pascoaes"),
    S("pt-pescadores-s1", "pt-os-pescadores", "pt-foz", "Opening chapters", "开头几章",
      "Brandão begins with Foz do Douro as it was in his childhood: the pilots and fishermen who were his grandfather's people, the bar of the river where boats were lost in sight of the houses, the women waiting on the rocks.",
      "布兰当从他童年时的杜罗河口写起：引水员和渔民，那是他外祖父那一辈的人；河口的沙洲，船就在家家户户的眼前沉没；还有站在礁石上等待的女人。",
      ["Foz do Douro"], ["杜罗河口"], W + "Raul_Brand%C3%A3o"),
    S("pt-pescadores-s2", "pt-os-pescadores", "pt-nazare", "Nazaré", "纳扎雷一章",
      "At Nazaré he finds the most beautiful beach and the hardest life: the high-prowed boats launched through the surf and hauled back by oxen, the men in checked shirts, the women in seven skirts who carry the fish and do the mourning.",
      "在纳扎雷，他看到了最美的海滩和最苦的日子：船头高翘的渔船冲过碎浪出海，回来时由牛拖上岸；男人穿着格子衬衫，女人穿着七层裙子，扛鱼的是她们，守丧的也是她们。",
      ["Nazaré"], ["纳扎雷"], W + "Raul_Brand%C3%A3o"),
    S("pt-ilhas-s1", "pt-ilhas-desconhecidas", "pt-corvo", "Corvo", "科尔沃岛一章",
      "In the summer of 1924 Brandão sails through the Azores and Madeira. On Corvo he finds a few hundred people in one village under a crater, who own their pastures in common, have no prison and no lock on any door, and take him in as a guest of the whole island.",
      "1924 年夏天，布兰当乘船游历亚速尔群岛和马德拉岛。在科尔沃岛，他见到火山口下只有一个村子，几百口人，牧场是公有的，没有监狱，哪家的门都不上锁，全岛的人把他当作共同的客人来接待。",
      ["Corvo"], ["科尔沃岛"], W + "Raul_Brand%C3%A3o"),
    S("pt-charneca-s1", "pt-charneca-em-flor", "pt-vila-vicosa", "Throughout", "全书",
      "Florbela's last sonnets speak in a woman's voice no Portuguese poet had used before: of desire without shame, of wanting to be everything at once, of the burnt plains of her Alentejo in flower. The book appeared in January 1931, a month after she died on her thirty-sixth birthday.",
      "弗洛贝拉最后的十四行诗用的是此前葡萄牙诗人从没用过的女性声音：毫不羞愧的欲望，想要同时成为一切的渴求，还有她的阿连特茹那片烧焦的原野开花的样子。诗集 1931 年 1 月出版，一个月前，她在自己三十六岁生日那天去世。",
      ["Alentejo"], ["阿连特茹"], W + "Florbela_Espanca"),
    S("pt-mensagem-s1", "pt-mensagem", "pt-martinho", "Throughout", "全书",
      "Forty-four short poems arranged like a coat of arms: the founders and kings of Portugal, the navigators, and the hidden king Sebastian who will return in the fog. 'O salt sea, how much of your salt is tears of Portugal!' is here, and the line that everything is worth it if the soul is not small.",
      "四十四首短诗，像一枚纹章那样排列：葡萄牙的开国者和国王，航海家，还有将在雾中归来的隐没之王塞巴斯蒂昂。“咸涩的大海啊，你的盐里有多少是葡萄牙的眼泪！”就出自这里，还有那一句：只要灵魂不渺小，一切都值得。",
      ["tears of Portugal"], ["葡萄牙的眼泪"], W + "Mensagem"),
    S("pt-pessoa-s1", "pt-pessoa-poems", "pt-brasileira", "The heteronyms", "异名者的诗",
      "Pessoa wrote as several poets with their own lives and styles: Alberto Caeiro, the keeper of sheep who says things are just what they are; Ricardo Reis, a doctor writing stoic odes; Álvaro de Campos, a naval engineer who shouts odes to machines and then, in 'The Tobacco Shop', looks from his window at the shop across the street and says he is nothing. Most of it was found after his death.",
      "佩索阿以好几位诗人的身份写作，各有各的生平和文风：牧羊人阿尔贝托·卡埃罗，说事物就是事物本身；医生里卡多·雷耶斯，写斯多葛式的颂歌；海军工程师阿尔瓦罗·德·坎波斯，先是对着机器高声放歌，后来在《烟草店》里从窗口望着街对面的铺子，说自己什么都不是。这些诗大部分是他死后才发现的。",
      ["The Tobacco Shop"], ["《烟草店》"], W + "Fernando_Pessoa"),
    S("pt-disquiet-s1", "pt-disquiet", "pt-douradores", "Throughout", "全书",
      "Bernardo Soares, assistant bookkeeper in a fabric warehouse in the Rua dos Douradores, keeps a 'factless autobiography': the view from his fourth-floor window, his boss Vasques, the rain on the Baixa, his certainty that he will never leave this street and that the dreams he has in it are larger than any journey.",
      "贝尔纳多·索阿雷斯在金匠街一家布料行当助理会计，写着一部“没有事实的自传”：四楼窗口望出去的景色，老板瓦斯克斯，落在下城的雨；他确信自己永远不会离开这条街，也确信在这条街上做的梦比任何旅行都大。",
      ["Rua dos Douradores"], ["金匠街"], W + "The_Book_of_Disquiet"),
    S("pt-esteiros-s1", "pt-esteiros", "pt-alhandra", "Throughout", "全书",
      "Through the four seasons a gang of boys, Gineto, Gaitinhas, Maquineta and the rest, work at the brickyards by the creeks of the Tagus when there is work and steal fruit when there is none. One wants to go to school; one ends in prison; the river floods the kilns.",
      "一年四季里，吉内托、盖蒂尼亚斯、马基内塔这一帮男孩，有活干的时候在特茹河潮沟边的砖厂做工，没活干的时候就去偷水果。有一个想上学，有一个进了监狱；河水漫过了砖窑。",
      ["Tagus"], ["特茹河"], W + "Soeiro_Pereira_Gomes"),
    S("pt-torga-s1", "pt-contos-da-montanha", "pt-torga", "Throughout", "全书",
      "Stories of the villages of Trás-os-Montes: smugglers, shepherds, a woman who gives birth alone on a mountain path, feuds over water and boundary stones, honour paid for with a knife. Torga published them himself; under the dictatorship the book was banned and had to be reprinted in Brazil.",
      "山后省村庄的故事：走私的，放羊的，独自在山路上生下孩子的女人，为水和界石结下的世仇，用刀子讨回的名誉。托尔加自费出版了这些故事；独裁时期这本书遭禁，只能拿到巴西重印。",
      ["Trás-os-Montes"], ["山后省"], W + "Miguel_Torga"),
    S("pt-nemesio-s1", "pt-mau-tempo-no-canal", "pt-horta", "Throughout", "全书",
      "In Horta, as the Great War ends, Margarida Clark Dulmo loves João Garcia, the son of a family hers has quarrelled with for a generation. Plague breaks out on Faial; she nurses an old servant who has caught it, is carried off to another island on a whaling boat, and in the end marries the rich man who can save her father's house.",
      "第一次世界大战将尽时的奥尔塔，玛格丽达·克拉克·杜尔莫爱上了若昂·加西亚，而两家已经结怨一代人。法亚尔岛上闹起鼠疫；她照顾染病的老仆人，被一条捕鲸船带到了另一座岛上，最后嫁给了那个能保住她父亲家业的有钱人。",
      ["Horta"], ["奥尔塔"], W + "Vitorino_Nem%C3%A9sio"),
    S("pt-regio-s1", "pt-toada-de-portalegre", "pt-regio", "Throughout", "全诗",
      "In Portalegre, a city of the Upper Alentejo ringed by hills and wind, the poet lives alone in an old house full of bad furniture, and tells how the wind at his window and an acacia in the yard kept him company until he could no longer tell his loneliness from the town.",
      "在波塔莱格雷这座群山环抱、多风的上阿连特茹小城，诗人独自住在一座摆满破家具的老房子里，讲述窗前的风和院子里的一棵金合欢怎样陪伴他，直到他再也分不清自己的孤独和这座城。",
      ["Portalegre"], ["波塔莱格雷"], W + "Jos%C3%A9_R%C3%A9gio"),
    S("pt-sibila-s1", "pt-a-sibila", "pt-vila-mea", "Throughout", "全书",
      "Germa remembers her aunt Quina, who as a sickly girl took over the half-ruined farm of Vessada from her spendthrift father, made it prosper by shrewdness and work, and came to be consulted by the whole district as a kind of seer, vain, generous and unknowable to the end.",
      "热尔玛回忆她的姑姑基娜：她年轻时体弱多病，却从挥霍的父亲手里接过半败落的韦萨达庄园，靠精明和劳作把它经营得兴旺起来，后来四乡八里的人都把她当成先知来请教；她虚荣，慷慨，到死都叫人看不透。",
      ["Vessada"], ["韦萨达"], W + "Agustina_Bessa-Lu%C3%ADs"),
    S("pt-lobos-s1", "pt-quando-os-lobos-uivam", "pt-serra-lapa", "Throughout", "全书",
      "The state decides to plant pine forest on the common upland where the villages of the serra have always grazed their flocks and cut their firewood. The highlanders resist the foresters, the Republican Guard opens fire, and the survivors are tried in Porto. The regime banned the book and prosecuted its author.",
      "政府决定在山上的公地造松林，而山里各村世世代代都在那里放牧、砍柴。山民抵抗林务人员，共和国卫队开了枪，活下来的人在波尔图受审。当局查禁了这本书，还起诉了作者。",
      ["common upland"], ["公地"], W + "Aquilino_Ribeiro"),
    S("pt-aparicao-s1", "pt-aparicao", "pt-giraldo", "Throughout", "全书",
      "Alberto Soares, newly bereaved of his father, comes to teach in Évora and is taken up by Dr Moura's family. His insistence that each person must face the 'apparition' of his own existence and his own death fascinates the daughters Sofia and Ana and a troubled pupil, Carolino, and ends in a killing.",
      "刚刚丧父的阿尔贝托·索阿雷斯来埃武拉教书，受到莫拉医生一家的接待。他坚持认为每个人都必须直面自身存在和自身死亡的“显现”，这让医生的女儿索菲亚和安娜、还有一个心事重重的学生卡罗利诺着了迷，最后酿成了一桩命案。",
      ["Évora"], ["埃武拉"], W + "Verg%C3%ADlio_Ferreira"),
    S("pt-menina-s1", "pt-menina-do-mar", "pt-granja", "Throughout", "全书",
      "A boy who lives in a white house on the dunes hears laughter among the rocks at low tide and finds a girl a hand's span tall, who lives in the sea with a crab, an octopus and a fish. He shows her the things of the land, a rose, fire, wine; she wants to see it and cannot leave the water.",
      "住在沙丘上白房子里的男孩，退潮时听见礁石间有笑声，发现了一个只有一拃高的小女孩，她和螃蟹、章鱼、鱼一起住在海里。男孩给她看陆地上的东西：一朵玫瑰，火，葡萄酒；她想去看看陆地，却离不开水。",
      ["a white house on the dunes"], ["沙丘上白房子"], W + "Sophia_de_Mello_Breyner_Andresen"),
    S("pt-novas-cartas-s1", "pt-novas-cartas", "pt-beja-convento", "Throughout", "全书",
      "Three women writers meet every week in 1971 and write, without signing which of them wrote what, letters, poems and stories that start from Mariana of Beja shut in her convent and go on to the wives of emigrants and conscripts, to abortion, desire and the colonial war. The book was seized within days and its authors tried for offending public morals; they were acquitted after the 1974 revolution.",
      "1971 年，三位女作家每周见面，一起写信、写诗、写故事，不标明哪一篇出自谁手；从关在修道院里的贝雅修女玛丽安娜写起，一直写到移民和征兵者的妻子，写到堕胎、欲望和殖民战争。书出版没几天就被没收，三位作者以有伤风化的罪名受审；1974 年革命之后，她们被宣告无罪。",
      ["Mariana of Beja"], ["贝雅修女玛丽安娜"], W + "New_Portuguese_Letters"),
    S("pt-levantado-s1", "pt-levantado-do-chao", "pt-lavre", "Throughout", "全书",
      "From the monarchy to the Carnation Revolution, the Mau-Tempos of Monte Lavre work other men's land for a wage that does not feed them: Domingos the drunken shoemaker, his son João, arrested and tortured for a strike, and João's daughter and granddaughter, who with the others walk onto the estates after the revolution and take them. It is the book in which Saramago found his run-on, spoken style.",
      "从王朝时代到康乃馨革命，拉夫雷山的“坏天气”一家一直在别人的土地上干活，挣的工钱不够吃饭：酗酒的鞋匠多明戈斯，他的儿子若昂因为罢工被捕受刑，革命之后，若昂的女儿和外孙女同大家一起走进庄园，把土地占了下来。萨拉马戈那种连绵不断、像说话一样的文体，就是在这本书里找到的。",
      ["Monte Lavre"], ["拉夫雷山"], "https://pt.wikipedia.org/wiki/Levantado_do_Ch%C3%A3o"),
    S("pt-memorial-s1", "pt-memorial-do-convento", "pt-mafra", "Throughout", "全书",
      "While João V drains the gold of Brazil into his convent at Mafra, Baltasar Sete-Sóis, who lost a hand in the war, and Blimunda, who can see inside people when she is fasting, help the priest Bartolomeu Lourenço build a flying machine lifted by human wills. They fly once; years later Blimunda finds Baltasar at an auto-da-fé.",
      "若昂五世把巴西的黄金源源不断地投进马夫拉的修道院；与此同时，在战争中失去一只手的巴尔塔萨“七个太阳”，和空腹时能看见人体内部的布里蒙达，帮着神父巴尔托洛梅乌·洛伦索造一架靠人的意志升空的飞行器。他们飞了一次；多年以后，布里蒙达在一场火刑仪式上找到了巴尔塔萨。",
      ["Mafra"], ["马夫拉"], W + "Baltasar_and_Blimunda"),
    S("pt-reis-s1", "pt-ricardo-reis", "pt-santa-catarina", "Throughout", "全书",
      "Ricardo Reis, one of Pessoa's invented poets, sails home from Brazil at the end of 1935 on hearing that Pessoa is dead. He moves from the Hotel Bragança to a flat at the Alto de Santa Catarina, in front of the statue of Adamastor, and through the first year of the Spanish war reads the newspapers, loves a chambermaid called Lídia and receives visits from Pessoa's ghost.",
      "里卡多·雷耶斯是佩索阿虚构的诗人之一。1935 年底，他听说佩索阿去世，从巴西乘船回国。他先住布拉干萨旅馆，后来搬到圣卡塔琳娜高地、正对阿达马斯托石像的一套房子里；在西班牙内战的头一年里，他读报纸，爱上了名叫莉迪亚的客房女佣，还接待佩索阿鬼魂的来访。",
      ["Alto de Santa Catarina", "Adamastor"], ["圣卡塔琳娜高地", "阿达马斯托"], W + "The_Year_of_the_Death_of_Ricardo_Reis"),
    S("pt-reis-s2", "pt-ricardo-reis", "pt-prazeres", "Early chapters", "开头几章",
      "A few days after landing, Reis takes the tram to the Prazeres cemetery and finds the grave where Pessoa was buried a month before, in his grandmother's tomb. Soon afterwards the dead man walks into his hotel room and explains that the dead are given nine months, as long as they spent in the womb, before they are forgotten.",
      "上岸没几天，雷耶斯坐电车去普拉泽雷斯墓园，找到了佩索阿一个月前下葬的地方——他祖母的墓。不久，死者走进他的旅馆房间，解释说人死后还有九个月的时间，和在娘胎里待的一样长，然后才会被遗忘。",
      ["Prazeres cemetery"], ["普拉泽雷斯墓园"], W + "The_Year_of_the_Death_of_Ricardo_Reis"),
    S("pt-memorias-s1", "pt-pequenas-memorias", "pt-azinhaga", "Throughout", "全书",
      "Saramago remembers his first fifteen years: the poor streets of Lisbon where his father was a policeman, and above all the summers at Azinhaga with his grandfather Jerónimo, a swineherd who could not read and who, sensing he would die, went round his yard embracing the trees one by one.",
      "萨拉马戈回忆自己人生的头十五年：里斯本的穷街，父亲在那里当警察；更多的是在阿济尼亚加跟外祖父热罗尼莫一起度过的夏天。外祖父是个不识字的猪倌，预感到自己要死的时候，在院子里一棵一棵地拥抱了那些树。",
      ["Azinhaga"], ["阿济尼亚加"], W + "Jos%C3%A9_Saramago"),
    S("pt-inquisidores-s1", "pt-manual-dos-inquisidores", "pt-palmela", "Throughout", "全书",
      "Senhor Francisco, a minister and friend of Salazar, rules his farm at Palmela and everyone on it, wearing his hat even to take the cook in the barn. After the 1974 revolution he is a paralysed old man in a Lisbon nursing home, and a chorus of voices, his feckless son João, the housekeeper Titina, his mistress, the vet, the chauffeur, give their depositions about him.",
      "弗朗西斯科先生是部长，也是萨拉查的朋友；他统治着帕尔梅拉的庄园和庄园里的每一个人，连在谷仓里占有厨娘的时候都戴着帽子。1974 年革命之后，他成了里斯本一家养老院里瘫痪的老人；许多个声音——他没出息的儿子若昂、女管家蒂蒂娜、情妇、兽医、司机——轮流为他作证。",
      ["Palmela"], ["帕尔梅拉"], W + "Ant%C3%B3nio_Lobo_Antunes"),
    S("pt-galveias-s1", "pt-galveias", "pt-galveias", "Throughout", "全书",
      "After the thing falls from the sky it rains for days, then not at all, and a smell of sulphur settles on Galveias. Chapter by chapter the village shows itself: two brothers who have not spoken for fifty years, the baker who is also a prostitute, the postman with a second family in Guinea, the dogs. A child born at the end does not smell of sulphur.",
      "那个东西从天上掉下来之后，雨下了好些天，然后一滴也不下了，加尔维亚什笼罩在硫磺味里。村子一章一章地显出面目：五十年没说过话的两兄弟，兼做妓女的面包师，在几内亚另有一个家的邮差，还有那些狗。结尾出生的一个孩子，身上没有硫磺味。",
      ["Galveias"], ["加尔维亚什"], W + "Jos%C3%A9_Lu%C3%ADs_Peixoto"),
    S("pt-pereira-s1", "pt-pereira-maintains", "pt-rodrigo-fonseca", "Throughout", "全书",
      "Pereira, a fat, widowed journalist who talks to his wife's photograph, edits the culture page of the Lisboa from a room in the Rua Rodrigo da Fonseca. He hires a young man, Monteiro Rossi, to write obituaries in advance, and finds himself paying for articles he cannot print and hiding Rossi from the political police; when they beat Rossi to death in Pereira's own flat, Pereira gets the truth into the paper and leaves the country.",
      "佩雷拉是个肥胖的鳏夫记者，常对着亡妻的照片说话；他在罗德里戈·达·丰塞卡街的一间屋子里编《里斯本报》的文化版。他雇了年轻人蒙泰罗·罗西预先写悼文，结果发现自己在为登不出去的文章付稿费，还得把罗西藏起来躲避政治警察；警察在佩雷拉自己家里把罗西活活打死之后，佩雷拉设法把真相登上了报纸，然后离开了这个国家。",
      ["Rua Rodrigo da Fonseca"], ["罗德里戈·达·丰塞卡街"], W + "Pereira_Maintains"),
    S("pt-night-train-s1", "pt-night-train", "pt-santa-apolonia", "Throughout", "全书",
      "Raimund Gregorius, a teacher of classical languages in Bern, stops a Portuguese woman from jumping off a bridge, finds in a bookshop the reflections of a Lisbon doctor, Amadeu de Prado, and that night boards the train. In Lisbon he seeks out those who knew Prado, his sisters, his teacher, his comrades in the resistance to Salazar, and pieces together a life unlike his own.",
      "赖蒙德·戈列格里尤斯在伯尔尼教古典语言。他拦下了一个要从桥上跳下去的葡萄牙女人，又在书店里发现了里斯本医生阿马德乌·德·普拉多的随想录，当晚就上了火车。在里斯本，他寻访认识普拉多的人——他的姐妹、老师、反抗萨拉查时的同志——一点点拼出一个和自己截然不同的人生。",
      ["Lisbon"], ["里斯本"], W + "Night_Train_to_Lisbon"),
    S("pt-martel-s1", "pt-high-mountains", "pt-tuizelo", "Parts 1–3", "第一至三部",
      "In 1904 Tomás, who has lost his lover, his son and his father in one week and now walks backwards, drives from Lisbon to Tuizelo in search of a strange crucifix. On the last night of 1938 a pathologist in Bragança opens the body of an old man from the same village. In 1981 a Canadian senator buys a chimpanzee and goes to live with him in the village his parents came from.",
      "1904 年，托马斯在一个星期里失去了情人、儿子和父亲，从此倒着走路；他开车从里斯本去图伊泽洛，寻找一个奇特的十字架。1938 年的最后一夜，布拉干萨的一位病理学家解剖了同一个村子里一位老人的遗体。1981 年，一位加拿大参议员买下一只黑猩猩，带着它搬到了父母的老家——这个村子。",
      ["Tuizelo"], ["图伊泽洛"], W + "The_High_Mountains_of_Portugal"),
]

# ============================== write ==============================
used = {p for l in lines for p in l["place_ids"]}
for p in places:
    assert p["id"] in used or p.get("book_ids"), ("place without a line or a book", p["id"])
bids = {x["id"] for x in books} | {"candide"}
for l in lines:
    assert l["book_id"] in bids, l["id"]
lined = {l["book_id"] for l in lines}
pilgrim = {i for p in places for i in p.get("book_ids", [])}
assert not ({x["id"] for x in books} - lined - pilgrim), {x["id"] for x in books} - lined - pilgrim
assert len({x["id"] for x in places}) == len(places) and len({x["id"] for x in lines}) == len(lines)

HEAD = "// Portugal, hand-written content (tools/content/batches/add_pt1.py, 2026-11-22).\n"
def write(name, key, entries, extra=""):
    os.makedirs(os.path.dirname(b.data(name)), exist_ok=True)
    with open(b.data(name), "w", encoding="utf-8") as fh:
        fh.write(HEAD + extra + "window.RA_DATA = window.RA_DATA || {};\nwindow.RA_DATA." + key + " = [\n"
                 + ",\n".join("  " + b.obj(e) for e in entries) + "\n];\n")
if __name__ == "__main__":
    write("books.js", "books", books)
    write("places.js", "places", places, "// Each place's admin-1 region is worked out from its coordinates by app.js.\n")
    write("lines.js", "lines", lines)
    print(len(books), "books,", len(places), "places,", len(lines), "lines (", sum(1 for l in lines if l.get("kind") != "scene"), "quotations )")
