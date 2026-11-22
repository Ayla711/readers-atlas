"""11-22 fact check of the Portugal and Austria notes against Wikipedia (cache/facts): the corrections.
Each text is replaced once in the batch script and once in the data, so the two stay the same.
Usage: python3 -I fix_ptat_facts.py <app_dir>"""
import os, sys
APP = sys.argv[1]
T = {
"at": [
 ("They spend the night awake in a cave of blue ice under the stars, hearing the ice crack,", "They look into a cave of blue ice, are frightened by it, and spend the night awake under a roof of boulders, hearing the ice crack,"),
 ("两人在蓝色冰洞里一夜没睡，头上是星空，耳边是冰层开裂的声音；", "他们见到一个蓝色的冰洞，吓得退了出来，在乱石搭成的石棚下熬了一夜没睡，耳边是冰层开裂的声音；"),
 ("A military court, moved by their story, lets him off lightly,", "The court, moved by their story, lets him off lightly,"),
 ("军事法庭被两人的遭遇打动", "法庭被两人的遭遇打动"),
 ("the play caused riots and a trial when it was staged in 1921.", "the play caused riots and a trial when it was staged in Berlin and Vienna in 1920–21."),
 ("1921 年公演时引发了骚乱和一场官司。", "1920 至 1921 年在柏林和维也纳公演时引发了骚乱和一场官司。"),
 ("works at the polyclinic and ends his night's wanderings in the hospital mortuary", "works at the polyclinic, and his search ends the next night in the mortuary of the pathological institute"),
 ("在门诊部上班，一夜游荡的终点是医院的停尸间", "在门诊部上班，第二天夜里，他的追寻在病理研究所的停尸间结束"),
 ("Robert Musil lived at Rasumofskygasse 20 from 1921 until he left Austria in 1938, and wrote most of The Man Without Qualities there; a plaque marks the house", "Robert Musil's Vienna flat was at Rasumofskygasse 20, and most of The Man Without Qualities was written there; the plaque on the house gives the years 1921 to 1938, part of which he spent in Berlin"),
 ("罗伯特·穆齐尔从 1921 年起住在拉祖莫夫斯基巷 20 号，直到 1938 年离开奥地利；《没有个性的人》大部分是在这里写的，楼上有纪念牌", "罗伯特·穆齐尔在维也纳的住所是拉祖莫夫斯基巷 20 号，《没有个性的人》大部分是在这里写的；楼上纪念牌写的年份是 1921 至 1938 年，其间他也在柏林住过一段"),
 ("he comes upon the coffin of the wife he wronged", "he stands at the deathbed of the wife he wronged"),
 ("他撞见被自己亏待的前妻的灵柩", "他站在被自己亏待的前妻的灵床前"),
 ("Vienna's state pawnshop and auction house is the 'Theresianum' of Auto-da-Fé", "Vienna's state pawnshop and auction house is, thinly disguised, the 'Theresianum' of Auto-da-Fé"),
 ("维也纳这家国营当铺兼拍卖行就是《迷惘》里的", "维也纳这家国营当铺兼拍卖行略加改头换面，就是《迷惘》里的"),
 ("the tunnels in the Mönchsberg where the town sheltered from the bombs, and the hill as the place from which the desperate threw themselves", "the tunnels in the rock where the town sheltered from the bombs, and the Mönchsberg as the place from which the desperate threw themselves"),
 ("全城人躲避轰炸的僧侣山隧洞，还有，这座山是绝望的人往下跳的地方", "全城人躲避轰炸的山岩隧洞，还有，僧侣山是绝望的人往下跳的地方"),
 ("came back on foot from the war at eighteen and never wanted to leave again", "was sent to the front at eighteen, came back from Soviet captivity and never wanted to leave again"),
 ("十八岁从战场上步行回来，从此再也不想离开", "十八岁被送上前线，从苏军战俘营回来以后再也不想离开"),
 ("the prisoner of war who weighed forty kilos, the municipal clerk", "the prisoner of war who nearly died of dysentery, the municipal clerk"),
 ("一个体重只剩四十公斤的战俘", "一个差点死于痢疾的战俘"),
 ("is buried by the door", "is buried in the left aisle"),
 ("葬在门边", "葬在左侧廊"),
 ("where the children and Maria fall out of the boat. The rococo palace", "where the children and Maria fall out of the boat; the scenes were shot on the lake here, in the grounds of the palace and of the property next to it. The rococo palace"),
 ("孩子们和玛丽亚从船上掉进水里的那场戏就在这里。", "孩子们和玛丽亚从船上掉进水里的那场戏，就是在这片湖上、在宫苑和相邻的庄园里拍的。"),
 ("Twelve poems for the rooms of the house, each dedicated to a friend:", "A sequence of poems for the rooms of the house, most of them dedicated to friends:"),
 ("十二首诗，写房子里的各个房间，每一首题献给一位朋友：", "一组诗，写房子里的各个房间，大多各题献给一位朋友："),
 ("built himself a villa nearby in 1834", "bought a country house nearby, at Pernitz, in 1834"),
 ("1834 年在附近给自己盖了别墅", "1834 年在附近的佩尼茨买下一处乡间住宅"),
 ("founding a cheese cooperative and a library", "founding a cheese-trading cooperative and a cattle insurance society"),
 ("还办了奶酪合作社和图书馆", "还办了奶酪销售合作社和牲畜保险社"),
 ("comes to the four-power Vienna of 1947 at the invitation", "comes to four-power Vienna just after the war at the invitation"),
 ("来到 1947 年四国共管的维也纳", "来到战后四国共管的维也纳"),
 ("and still lives here. It is the model", "and has gone on living in Götzis. It is the model"),
 ("长大，至今住在这里。它是", "长大，后来也一直住在格齐斯。它是"),
 ("together with the geographer Simony's account of the Dachstein ice, gave him", "together with the geographer Simony's picture of a glacier cave, gave him"),
 ("又听地理学家西莫尼讲达赫施泰因的冰川，由此有了", "又看到地理学家西莫尼画的冰川洞穴，由此有了"),
 ],
"pt": [
 ("he was stopped on the road by four masked gentlemen, blindfolded,", "he was stopped on the road by masked men, blindfolded,"),
 ("在公路上被四个蒙面的绅士拦住", "在公路上被几个蒙面人拦住"),
 ("In 1939 a pathologist in Bragança", "On the last night of 1938 a pathologist in Bragança"),
 ("1939 年，布拉干萨的一位病理学家", "1938 年的最后一夜，布拉干萨的一位病理学家"),
 ("where Soeiro Pereira Gomes worked. Esteiros", "where Soeiro Pereira Gomes lived, working at the cement plant. Esteiros"),
 ("索埃罗·佩雷拉·戈梅斯曾在这里工作。", "索埃罗·佩雷拉·戈梅斯曾住在这里，在水泥厂做事。"),
 ("and in the fourth tells how", "and in one of them tells how"),
 ("在第四封信里，她说", "在其中一封信里，她说"),
 ("Letter 4", "The five letters"),
 ("第四封信", "五封信"),
 ("and nineteen voices, his feckless son João", "and a chorus of voices, his feckless son João"),
 ("十九个声音——", "许多个声音——"),
 ("it rains for seven days, then not at all,", "it rains for days, then not at all,"),
 ("雨下了七天，然后", "雨下了好些天，然后"),
 ("The riverside terminus where the international trains from Paris by way of Irún used to arrive. In Night Train to Lisbon a Bern schoolteacher walks out of his classroom, takes the night train and gets off in a city he has never seen", "Lisbon's old riverside terminus for long-distance and international trains. In Night Train to Lisbon a Bern schoolteacher walks out of his classroom and takes the night train to a city he has never seen"),
 ("河边的终点站，从巴黎经伊伦来的国际列车过去都到这里。《开往里斯本的夜车》里，伯尔尼的一位中学教师走出课堂，坐上夜车，在一座从没见过的城市下了车", "里斯本河边的老终点站，长途和国际列车到这里。《开往里斯本的夜车》里，伯尔尼的一位中学教师走出课堂，坐上夜车，去了一座从没见过的城市"),
 ],
}
SRC = {  # (in the script, in the data) -> new address
"at": [("W + \"The_Poor_Fiddler\"", "https://en.wikipedia.org/wiki/The_Poor_Fiddler", "https://de.wikipedia.org/wiki/Der_arme_Spielmann"),
       ("W + \"Gathering_Evidence\"", "https://en.wikipedia.org/wiki/Gathering_Evidence", "https://de.wikipedia.org/wiki/Die_Ursache._Eine_Andeutung"),
       ("W + \"Reisebilder\"", "https://en.wikipedia.org/wiki/Reisebilder", "https://de.wikipedia.org/wiki/Hofkirche_(Innsbruck)"),
       ("W + \"The_Third_Man_(novella)\"", "https://en.wikipedia.org/wiki/The_Third_Man_(novella)", "https://de.wikipedia.org/wiki/Der_dritte_Mann_(Roman)")],
"pt": [("W + \"Raised_from_the_Ground\"", "https://en.wikipedia.org/wiki/Raised_from_the_Ground", "https://pt.wikipedia.org/wiki/Levantado_do_Ch%C3%A3o"),
       ("W + \"Trindade_Coelho\"", "https://en.wikipedia.org/wiki/Trindade_Coelho", "https://pt.wikipedia.org/wiki/Jos%C3%A9_Francisco_Trindade_Coelho")],
}
for cc in ("pt", "at"):
    sp = f"{APP}/tools/content/batches/add_{cc}1.py"
    dp = [f"{APP}/data/{cc}/places.js", f"{APP}/data/{cc}/lines.js"]
    s = open(sp, encoding="utf-8").read()
    d = [open(p, encoding="utf-8").read() for p in dp]
    for a, b in T[cc]:
        assert s.count(a) == 1, (cc, "script", a[:40], s.count(a))
        n = [x.count(a) for x in d]
        assert sum(n) == 1, (cc, "data", a[:40], n)
        s = s.replace(a, b); d = [x.replace(a, b) for x in d]
    for a_s, a_d, new in SRC[cc]:
        n = s.count(a_s); assert n >= 1, (cc, a_s)
        assert d[1].count(a_d + '"') == n, (cc, a_d, d[1].count(a_d + '"'), n)
        s = s.replace(a_s, '"' + new + '"'); d[1] = d[1].replace(a_d + '"', new + '"')
    for p, x in zip([sp] + dp, [s] + d):
        open(p + ".new", "w", encoding="utf-8").write(x); os.replace(p + ".new", p)
    print(cc, len(T[cc]) // 2, "notes corrected,", len(SRC[cc]), "source addresses replaced")
