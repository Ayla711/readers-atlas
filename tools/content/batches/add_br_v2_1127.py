"""11-27: Brazil, the new books of the selection re-check (tools/selection/br.md, rule v2; the user took all seven on 11-27).
The book records go to the shared South American list (data/sa/books.js). Places, with the reason for each:
- Rio de Janeiro for The Passion According to G.H.: G.H. lives in a Rio de Janeiro penthouse, where the whole book happens.
- Pindorama for Lavoura arcaica: the farm of the Lebanese family is unnamed, somewhere in the rural interior of São Paulo
  state; Nassar was born in Pindorama, SP, where his family farmed (A-24, said in the note).
- Itabira for A rosa do povo: a book of 55 poems with no single setting, written 1943-45; hung on Itabira, Drummond's
  birthplace (A-24, said in the note).
- Espaço Pasárgada, Recife, for Libertinagem: "Evocação do Recife" calls up "a casa de meu avô", this house in Rua da União
  where Bandeira lived from six to ten. Libertinagem (1930) is in the US public domain since 2026, but no free text of it was
  found (not on Wikisource or Gutenberg): a scene note, no quotation.
- Itaparica (existing br-itaparica) for Um defeito de cor: Kehinde is enslaved on the island of Itaparica, Bahia.
- Belo Horizonte for Canção para ninar menino grande: the towns along Fio Jasmim's railway are not named; Conceição Evaristo
  was born in Belo Horizonte (A-24, said in the note).
- Rio Japurá for O som do rugido da onça: Iñe-e is a Miranha girl from the Japurá country, taken by Spix and Martius to
  Munich (the Munich chapters could later get a place in the German files).
Usage: python3 -I tools/content/batches/add_br_v2_1127.py <app_dir> tools/content/batches/coords/add_br_v2_1127.json"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batchlib as b

APP, CO = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
DATE = "2026-11-27"
b.init(APP, "", "br", DATE)
SA_BOOKS = os.path.join(APP, "data", "sa", "books.js")
def C(pid):
    c = CO[pid]; return c["lat"], c["lon"], c["st"], c["su"]

books = [
    dict(id="passion-according-to-gh", title="The Passion According to G.H.", title_zh="G.H.受难记", title_orig="A paixão segundo G.H.",
         author="Clarice Lispector", author_zh="克拉丽丝·李斯佩克朵", year="1964", orig_lang="pt", public_domain=False, source_url=None,
         aliases=["A paixão segundo G.H."]),
    dict(id="lavoura-arcaica", title="Ancient Tillage", title_zh="古老的耕作", title_orig="Lavoura arcaica", author="Raduan Nassar",
         author_zh="拉杜安·纳萨尔", year="1975", orig_lang="pt", public_domain=False, source_url=None, aliases=["Lavoura arcaica", "To the Left of the Father"]),
    dict(id="a-rosa-do-povo", title="The People's Rose", title_zh="人民的玫瑰", title_orig="A rosa do povo", author="Carlos Drummond de Andrade",
         author_zh="卡洛斯·德鲁蒙德·德安德拉德", year="1945", orig_lang="pt", public_domain=False, source_url=None, aliases=["A rosa do povo"]),
    dict(id="libertinagem", title="Libertinagem", title_zh="放纵", title_orig="Libertinagem", author="Manuel Bandeira", author_zh="曼努埃尔·班德拉",
         year="1930", orig_lang="pt", public_domain=False, source_url=None, aliases=["Evocação do Recife", "Vou-me embora pra Pasárgada", "Pasárgada"]),
    dict(id="um-defeito-de-cor", title="A Defect of Colour", title_zh="肤色的缺陷", title_orig="Um defeito de cor", author="Ana Maria Gonçalves",
         author_zh="安娜·玛丽亚·贡萨尔维斯", year="2006", orig_lang="pt", public_domain=False, source_url=None, aliases=["Um defeito de cor", "Kehinde", "Luísa Mahin"]),
    dict(id="cancao-para-ninar-menino-grande", title="Lullaby for a Big Boy", title_zh="大男孩摇篮曲", title_orig="Canção para ninar menino grande",
         author="Conceição Evaristo", author_zh="孔塞桑·埃瓦里斯托", year="2018", orig_lang="pt", public_domain=False, source_url=None,
         aliases=["Canção para ninar menino grande", "Fio Jasmim"]),
    dict(id="o-som-do-rugido-da-onca", title="The Sound of the Jaguar's Roar", title_zh="美洲豹吼声", title_orig="O som do rugido da onça",
         author="Micheliny Verunschk", author_zh="米切利尼·韦伦施克", year="2021", orig_lang="pt", public_domain=False, source_url=None,
         aliases=["O som do rugido da onça", "Iñe-e", "Spix and Martius"]),
]

places = [
    b.ORIG("br-rio-de-janeiro", "Rio de Janeiro", "里约热内卢", *C("br-rio-de-janeiro"),
        "Brazil's capital until 1960 and still its literary capital for much of the century. Clarice Lispector, who lived here, set The Passion According to G.H. (1964) in the penthouse of a well-to-do Rio woman: the whole book is one day's crisis in her flat and the maid's room behind it",
        "1960 年以前的巴西首都，大半个世纪里也是巴西文学的中心。住在这里的克拉丽丝·李斯佩克朵把《G.H.受难记》（1964）放在一位富裕的里约女人的顶层公寓里：整本书就是她在自家公寓和后面女佣房里经历的一天的危机"),
    b.ORIG("br-pindorama", "Pindorama, São Paulo", "圣保罗州 · 平多拉马", *C("br-pindorama"),
        "A small farming town in the north-west of São Paulo state, where Raduan Nassar was born in 1935 into a Lebanese family who had landed at Santos in 1920; they later moved to Catanduva and then to São Paulo. His Lavoura arcaica is set on the farm of a Lebanese immigrant family in the rural interior of the state, never named in the book; Pindorama, the farming country of his own childhood, is its nearest real place",
        "圣保罗州西北部的一个农业小镇。拉杜安·纳萨尔 1935 年生在这里的一个黎巴嫩家庭，他家 1920 年在桑托斯上岸，后来搬到卡坦杜瓦，再到圣保罗。他的《古老的耕作》写圣保罗州内地一个黎巴嫩移民家庭的农庄，书里没有写地名；作者童年所在的农业小镇平多拉马，是离它最近的真实地点"),
    b.ORIG("br-itabira", "Itabira, Minas Gerais", "米纳斯吉拉斯 · 伊塔比拉", *C("br-itabira"),
        "An old iron-mining town in Minas Gerais, the birthplace of Carlos Drummond de Andrade (1902). His A rosa do povo, 55 poems written between 1943 and 1945, under the Second World War and the Estado Novo, has no single setting; it is hung here, on the town where he was born",
        "米纳斯吉拉斯州的一座老铁矿城，卡洛斯·德鲁蒙德·德安德拉德 1902 年生在这里。他的《人民的玫瑰》收 55 首诗，写于 1943 至 1945 年，正值二战和“新国家”独裁时期，没有一个固定的地点；这里把它放在诗人出生的小城"),
    b.PIL("br-espaco-pasargada", "Espaço Pasárgada, Recife", "累西腓 · 帕萨尔加达之家", *C("br-espaco-pasargada"),
        "The house in Rua da União, Recife, of Manuel Bandeira's maternal grandfather, where the poet lived from six to ten; he said the mythology of his childhood, more real to him than the Greek one, was formed here. His poem \"Evocação do Recife\" calls it \"a casa de meu avô\". Since 1986, the poet's centenary, it has been a cultural centre",
        "曼努埃尔·班德拉的外祖父在累西腓联合街的老宅，诗人六到十岁住在这里，他说自己童年的神话就是在这里形成的，对他来说比希腊神话还真实。他的诗《累西腓回忆》称它为“我外祖父的家”。1986 年诗人百年诞辰时，这里改成了文化中心",
        ["libertinagem"]),
    b.ORIG("br-belo-horizonte", "Belo Horizonte", "贝洛奥里藏特", *C("br-belo-horizonte"),
        "The capital of Minas Gerais, where Conceição Evaristo was born in 1946. Her novel Canção para ninar menino grande follows Fio Jasmim, a Black railwayman, through the towns along his line, which the book does not name; it is hung here, on the writer's own city",
        "米纳斯吉拉斯州首府，孔塞桑·埃瓦里斯托 1946 年生在这里。她的小说《大男孩摇篮曲》跟着黑人铁路工人菲奥·雅斯明走过他沿线的一座座小城，书里没有写地名；这里把它放在作家自己的城市"),
    b.ORIG("br-rio-japura", "Japurá River", "雅普拉河", *C("br-rio-japura"),
        "A great Amazon tributary that rises in Colombia, where it is called the Caquetá, and flows east through Brazil to join the Amazon; the point here is near its mouth. Around 1820 the Bavarian naturalists Spix and Martius took two Indigenous children from its country, Iñe-e of the Miranha people and a boy of the Juri people, called Caracara-í in the novel, to Munich, where both soon died; Micheliny Verunschk's novel O som do rugido da onça tells their story",
        "亚马孙河的一条大支流，发源于哥伦比亚（那里叫卡克塔河），向东流经巴西汇入亚马孙河；地图上的点在它的河口附近。1820 年前后，巴伐利亚博物学家施皮克斯和马齐乌斯从这一带带走了两个原住民孩子——米兰尼亚族女孩伊涅-埃和一个尤里族男孩（小说里叫卡拉卡拉-伊）——带到慕尼黑，两人不久都死在那里；米切利尼·韦伦施克的小说《美洲豹吼声》讲的就是他们的故事"),
]

lines = [
    b.S("br-gh-s1", "passion-according-to-gh", "br-rio-de-janeiro", "The novel as a whole", "全书",
        "In one long monologue G.H., a well-to-do woman living in a Rio de Janeiro penthouse, goes back over the day before. The Black maid has just left, and G.H. goes to clean out her room, expecting a mess; instead it is bare and clean, with charcoal outlines of a man, a woman and a dog on the wall, and she realises the maid hated her. A cockroach crawls out of the wardrobe; she slams the door on it, and watching it ooze while still alive pulls her into a crisis of identity. Written in a rush at the end of 1963, the novel is on the Fuvest reading list for 2027 and 2028.",
        "在一段长长的独白里，住在里约热内卢顶层公寓的富裕女人 G.H. 回想前一天的事。黑人女佣刚辞工，G.H. 去收拾她的房间，以为会一团乱，没想到房里空荡干净，墙上用炭笔画着一个男人、一个女人和一条狗，她明白女佣恨她。一只蟑螂从衣柜里爬出来，她用柜门夹住它，看着它还活着、身体里的东西慢慢渗出来，由此陷入一场关于自我的危机。小说是 1963 年底一口气写成的，列在圣保罗大学 2027、2028 年入学考试的必读书里。",
        ["Rio de Janeiro"], ["里约热内卢"],
        "https://en.wikipedia.org/wiki/The_Passion_According_to_G.H.; https://www.fuvest.br/fuvest-renova-sua-lista-de-leituras-obrigatorias-para-o-vestibular-2026-2029/"),
    b.S("br-lav-s1", "lavoura-arcaica", "br-pindorama", "The novel as a whole", "全书",
        "André, a son of a Lebanese immigrant family farming in the interior of São Paulo, has fled the farm and his father's sermons on patience and work; his elder brother Pedro finds him in a boarding house and asks him to come home. In André's feverish first-person telling we learn of his love for his sister Ana in the old house; the family holds a feast for the prodigal's return, and it ends with the father, Iohána, killing Ana. Nassar published it in 1975; Luiz Fernando Carvalho filmed it in 2001.",
        "安德烈出身一个在圣保罗州内地务农的黎巴嫩移民家庭，他逃离了农庄和父亲关于忍耐与劳作的训诫；哥哥佩德罗在一家寄宿公寓里找到他，劝他回家。在安德烈热病般的第一人称讲述里，我们得知他在老屋里对妹妹安娜的爱；全家为浪子归来举办宴会，结局却是父亲伊奥哈纳杀死了安娜。纳萨尔 1975 年出版此书，路易斯·费尔南多·卡瓦略 2001 年把它拍成电影。",
        ["São Paulo"], ["圣保罗"],
        "https://revistas.usp.br/eav/article/download/146448/140124/293935; https://lebanesestudies.ojs.chass.ncsu.edu/index.php/mashriq/article/download/38/522/1911; https://www.goodreads.com/book/show/28464285; https://core.ac.uk/download/268339408.pdf; https://revistas.usp.br/opiniaes/article/download/154890/154786/360776; https://periodicos.fclar.unesp.br/casa/article/download/17828/16067/67325; https://www.eca.usp.br/acervo/producao-academica/002860481.pdf; https://seer.ucp.br/seer/index.php/vernaculum/article/view/924/413"),
    b.S("br-rosa-s1", "a-rosa-do-povo", "br-itabira", "The book as a whole", "全书",
        "Drummond's longest book, 55 poems written between 1943 and 1945, while the Second World War was turning against the Nazis in the east and Getúlio Vargas's Estado Novo was losing the middle class. The rose of the title stands for poetry, the expression of the people of the time; the poems swing between political commitment, in hope of a left-wing utopia, and a sceptical, disenchanted view, in free and often surreal images. It is counted his first mature book and the high point of his social lyricism. Drummond was born in Itabira in 1902.",
        "这是德鲁蒙德篇幅最长的诗集，收 55 首诗，写于 1943 至 1945 年：二战的东线战局正在逆转，热图利奥·瓦加斯的“新国家”独裁正在失去中产阶级的支持。书名里的玫瑰代表诗歌，也就是那个时代的人民的表达；诗在政治参与（对左翼理想的期望）和怀疑、幻灭之间摇摆，意象自由，常带超现实色彩。它被看作诗人第一部成熟之作，也是他社会抒情诗的高峰。德鲁蒙德 1902 年生在伊塔比拉。",
        ["Itabira"], ["伊塔比拉"],
        "https://pt.wikipedia.org/wiki/A_Rosa_do_Povo; https://en.wikipedia.org/wiki/Carlos_Drummond_de_Andrade"),
    b.S("br-lib-s1", "libertinagem", "br-espaco-pasargada", "“Evocação do Recife” and the book", "《累西腓回忆》及全书",
        "Bandeira's fourth book of poems, published in 1930, the same year as Drummond's first, is counted a landmark of Brazilian Modernism: free verse, plain everyday speech, humour and irony set against death and illness (he had tuberculosis), and a frank eroticism. Among its poems are \"Vou-me embora pra Pasárgada\", the dream of an elsewhere where everything is allowed, and \"Evocação do Recife\", which calls up the Recife of his childhood: Rua da União and his grandfather's house, now the Espaço Pasárgada.",
        "这是班德拉的第四部诗集，1930 年出版，和德鲁蒙德的第一部诗集同年，被看作巴西现代主义成熟的标志：自由体，平常口语，用幽默和反讽对抗死亡与疾病（他患有肺结核），情欲写得直白。集子里有《我要去帕萨尔加达》，写一个什么都被允许的远方；还有《累西腓回忆》，追忆童年的累西腓：联合街和外祖父的房子，也就是今天的帕萨尔加达之家。",
        ["Recife", "Rua da União"], ["累西腓", "联合街"],
        "https://pt.wikipedia.org/wiki/Libertinagem_(livro); https://pt.wikipedia.org/wiki/Espaço_Pasárgada"),
    b.S("br-ddc-s1", "um-defeito-de-cor", "br-itaparica", "The novel as a whole", "全书",
        "An old African woman, Kehinde, sails back to Africa in search of a son lost decades before, and on the way she tells her life: a childhood in the kingdom of Dahomey, capture at eight, the slave ship, and slavery on the island of Itaparica in Bahia; then adult life in Bahia, her letter of freedom, and a return to Africa as a successful businesswoman among the freed Brazilians of Benin and Nigeria. The novel dramatises the life of Luísa Mahin, mother of the abolitionist Luís Gama, and passes through the Malê revolt of 1835 and the Sabinada. It won the Casa de las Américas Prize in 2007, and in 2024 it inspired the Portela samba school's carnival parade.",
        "年迈的非洲女人凯因德乘船回非洲，寻找几十年前失散的儿子，一路讲述自己的一生：在达荷美王国的童年，八岁被捕，运奴船，在巴伊亚的伊塔帕里卡岛上为奴；后来在巴伊亚的成年生活，拿到自由证书，回到非洲，在贝宁和尼日利亚那些获释的巴西人中间成了成功的女商人。小说取材于废奴主义者路易斯·加马的母亲路易莎·马因的一生，写到了 1835 年的马莱起义和萨比纳达起义。2007 年获美洲之家奖，2024 年成为波特拉桑巴学校狂欢节游行的主题。",
        ["Itaparica"], ["伊塔帕里卡"],
        "https://pt.wikipedia.org/wiki/Um_Defeito_de_Cor"),
    b.S("br-cancao-s1", "cancao-para-ninar-menino-grande", "br-belo-horizonte", "The novel as a whole", "全书",
        "Fio Jasmim, a handsome young Black railwayman, an engine driver's assistant, travels the region for work; married to Pérola, with whom he has eight children, he takes up with women in the towns along the line. In sixteen chapters his story is told by the women themselves, among them Juventina Marina Perpétua, his lover for years, who wrote him the song of the title. It is on the Fuvest reading list for 2026 to 2029. The book does not name its towns; Evaristo was born in Belo Horizonte.",
        "菲奥·雅斯明是个英俊的年轻黑人铁路工人，火车司机的助手，为工作在这一带来回奔走；他娶了佩罗拉，生了八个孩子，却在沿线的小城里和一个又一个女人往来。小说分十六章，由这些女人亲口讲他的故事，其中有做了他多年情人的尤文蒂娜·玛丽娜·佩尔佩图阿，书名那首歌就是她为他写的。小说列在圣保罗大学 2026 至 2029 年入学考试的必读书里。书里没有写地名；埃瓦里斯托生在贝洛奥里藏特。",
        ["Belo Horizonte"], ["贝洛奥里藏特"],
        "https://www.adorocinema.com/noticias/filmes/noticia-1000210538/; https://www.goodreads.com/book/show/222552005; https://periodicos.ufsc.br/index.php/literatura/article/download/105989/60941/434360; https://sistemas.uft.edu.br/periodicos/index.php/portodasletras/article/download/17405/21999/81365; https://en.wikipedia.org/wiki/Concei%C3%A7%C3%A3o_Evaristo; https://www.fuvest.br/fuvest-renova-sua-lista-de-leituras-obrigatorias-para-o-vestibular-2026-2029/"),
    b.S("br-onca-s1", "o-som-do-rugido-da-onca", "br-rio-japura", "The novel as a whole", "全书",
        "The Bavarian naturalists Spix and Martius came to Brazil with the scientists sent for the marriage of Dom Pedro I and Leopoldina of Austria, and took two Indigenous children back to Munich: Iñe-e, a ten-year-old Miranha girl, and Caracara-í, a twelve-year-old boy of the Juri people. Verunschk tells their story from Iñe-e's side, with the voices of the forest, of the jaguar and of Munich's river Isar, and sets beside it Josefa, a present-day translator in São Paulo of Indigenous descent, who comes upon a lithograph of the children at an exhibition and travels to Munich in Iñe-e's tracks. It won the Jabuti Prize for the novel in 2022.",
        "巴伐利亚博物学家施皮克斯和马齐乌斯随为佩德罗一世与奥地利的莱奥波尔迪娜联姻而派来的科学家来到巴西，把两个原住民孩子带回了慕尼黑：十岁的米兰尼亚族女孩伊涅-埃和十二岁的尤里族男孩卡拉卡拉-伊。韦伦施克从伊涅-埃这一边讲他们的故事，交织着森林、美洲豹和慕尼黑伊萨尔河的声音，并在旁边写了约瑟法：一个住在圣保罗、有原住民血统的当代译者，她在一次展览上偶然看到这两个孩子的石版画像，于是循着伊涅-埃的路去了慕尼黑。2022 年获雅布蒂奖长篇小说奖。",
        ["Miranha"], ["米兰尼亚"],
        "https://rd.uffs.edu.br/bitstream/prefix/9228/1/HANAUER.pdf; https://www.goethe.de/prj/hum/pt/col/25533337.html; https://outraspalavras.net/poeticas/o-som-do-rugido-da-onca-a-contra-historia-de-um-sequestro-2/; https://periodicos.unb.br/index.php/estudos/article/download/58477/42705/212124; https://seer.ufrgs.br/index.php/cadernosdoil/article/download/153732/99651/711127; https://www.goodreads.com/book/show/57090882; https://revistas.ufrj.br/index.php/alea/article/view/72886/46894; https://periodicos.ufmg.br/index.php/aletria/article/download/33566/28572/110038; https://meriva.pucrs.br/dspace/bitstream/10923/26035/1/000508026-Texto%2bcompleto-0.pdf; https://www.companhiadasletras.com.br/livro/9786559210213/o-som-do-rugido-da-onca-vencedor-jabuti-2022"),
]

def ids_in(path): return set(re.findall(r'\{ id: "([^"]+)"', open(path, encoding="utf-8").read()))
all_books = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "books.js"))))
all_places = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "places.js"))))
all_lines = set().union(*(ids_in(f) for f in glob.glob(os.path.join(APP, "data", "*", "lines.js"))))
assert not {x["id"] for x in books} & all_books
assert {p["id"] for p in places} == set(CO) and not set(CO) & all_places
assert not {l["id"] for l in lines} & all_lines
assert "br-itaparica" in all_places
if __name__ == "__main__":
    note = "11-27 selection re-check, rule v2 (add_br_v2_1127.py)"
    b.append(SA_BOOKS, books, note)
    b.append(b.data("places.js"), places, note)
    b.append(b.data("lines.js"), lines, note)
    print(len(books), "books,", len(places), "places,", len(lines), "lines")
