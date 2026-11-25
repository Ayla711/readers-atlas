"""11-24: photos for the places added under selection rule v2 (dz, dk, tr, ua, fi, hu, nl, be second packs; ke, ro, ma packs 2).
One freely licensed Wikimedia Commons photo per place (CC0, public domain, CC BY, CC BY-SA; never NC or ND), chosen by eye
from contact sheets of candidates (tools/content/photos/find_photos.py); each one checked to show the place itself
(Vejlby: the church near Grenaa, not the Vejlby near Allingåbro; Ter-Muren: the chapel on the Kapellekensbaan, Commons
category "Kapel Onze-Lieve-Vrouw Termuren"). Author names are as the file pages give them; three are written out by hand
because the page uses a creator template (Voorschoten), the Fortepan credit form (Attila út) or adds a user name (Nizhyn).
Not found: no free photo of the Tazmamart site (ma-tazmamart stays without one).

Each image: the 960 px Commons thumbnail (or the original when smaller), resized to 800 px wide, JPEG q82, no metadata, saved
as images/places/<id>.jpg; the place gets photo: {file, width, height, author, license, license_url, source, alt_en, alt_zh};
docs/photo-credits.md gets one row per photo.

Usage: python3 -I tools/content/batches/add_photos_v2_1124.py <app_dir> [<cache_dir>]
<cache_dir>/<id>.jpg is used when present (the downloads made while choosing); otherwise the thumbnail is downloaded."""
import json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

APP = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 else None
UA = {"User-Agent": "ReadersAtlas/1.0 (https://github.com/Ayla711/readers-atlas; student project)"}
# id, Commons file page, original file URL, author, license, license URL, alt (en), alt (zh)
PHOTOS = [
    ["be-waasland", "https://commons.wikimedia.org/wiki/File%3ASint-Niklaas_April_2012-1.jpg", "https://upload.wikimedia.org/wikipedia/commons/5/52/Sint-Niklaas_April_2012-1.jpg", "Alvesgaspar", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The Grote Markt of Sint-Niklaas, the chief town of the Waasland", "瓦斯兰首府圣尼古拉斯的大集市广场"],
    ["be-antwerp", "https://commons.wikimedia.org/wiki/File%3AAntwerpen_Grote_Markt_11a.jpg", "https://upload.wikimedia.org/wikipedia/commons/7/7f/Antwerpen_Grote_Markt_11a.jpg", "Zairon", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Guild houses on the Grote Markt, Antwerp", "安特卫普大集市广场上的行会大楼"],
    ["be-ter-muren", "https://commons.wikimedia.org/wiki/File%3AKapel_kapellekensbaan_Aalst.jpg", "https://upload.wikimedia.org/wikipedia/commons/c/ce/Kapel_kapellekensbaan_Aalst.jpg", "Jaronax", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The chapel on the Kapellekensbaan, Erembodegem", "埃伦博德海姆小教堂路边的小教堂"],
    ["be-weert", "https://commons.wikimedia.org/wiki/File%3AWeert_Scheldestraat.JPG", "https://upload.wikimedia.org/wikipedia/commons/a/af/Weert_Scheldestraat.JPG", "Torsade de Pointes", "Public domain", "https://en.wikipedia.org/wiki/Public_domain", "Scheldestraat in Weert", "韦尔特的斯海尔德街"],
    ["be-vaalserberg", "https://commons.wikimedia.org/wiki/File%3ADrie_symbolische_grenspalen_op_drielandenpunt_%28Vaals%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/3/31/Drie_symbolische_grenspalen_op_drielandenpunt_%28Vaals%29.jpg", "Dominicus Johannes Bergsma", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Three boundary posts at the Drielandenpunt on the Vaalserberg", "瓦尔瑟山三国交界点的三根界碑"],
    ["be-antwerpen-centraal", "https://commons.wikimedia.org/wiki/File%3AHal_Centraal_station_Antwerpen_van_boven_I.jpg", "https://upload.wikimedia.org/wikipedia/commons/a/a9/Hal_Centraal_station_Antwerpen_van_boven_I.jpg", "Smiley.toerist", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The great hall of Antwerpen-Centraal station", "安特卫普中央车站大厅"],
    ["dk-vejlby", "https://commons.wikimedia.org/wiki/File%3AVejlby_kirke%2C_Gren%C3%A5_%28Norddjurs%29.JPG", "https://upload.wikimedia.org/wikipedia/commons/2/23/Vejlby_kirke%2C_Gren%C3%A5_%28Norddjurs%29.JPG", "Bococo", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "Vejlby Church, near Grenaa", "格雷诺附近的韦尔比教堂"],
    ["dk-skorping", "https://commons.wikimedia.org/wiki/File%3ASk%C3%B8rping_KulturStation.JPG", "https://upload.wikimedia.org/wikipedia/commons/e/ec/Sk%C3%B8rping_KulturStation.JPG", "Søren1997", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The old station building at Skørping", "斯科尔平的老车站楼"],
    ["dk-blataarn", "https://commons.wikimedia.org/wiki/File%3AChristiansborg_Palace_2017-08-16.jpg", "https://upload.wikimedia.org/wikipedia/commons/8/83/Christiansborg_Palace_2017-08-16.jpg", "Colin", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Christiansborg Palace on Slotsholmen, Copenhagen", "哥本哈根斯洛茨岛上的克里斯蒂安堡宫"],
    ["dz-thagaste", "https://commons.wikimedia.org/wiki/File%3ASouk-ahras_barage.jpg", "https://upload.wikimedia.org/wikipedia/commons/d/dc/Souk-ahras_barage.jpg", "Abdallahdjabi", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The dam lake near Souk Ahras", "苏格阿赫拉斯附近的水库"],
    ["dz-constantine", "https://commons.wikimedia.org/wiki/File%3APont_El_Kantara_%28Constantine%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/5/51/Pont_El_Kantara_%28Constantine%29.jpg", "Bernard Gagnon", "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0", "El Kantara Bridge over the gorge, Constantine", "君士坦丁峡谷上的坎塔拉桥"],
    ["fi-urjala", "https://commons.wikimedia.org/wiki/File%3AUrjalan_kirkko.jpg", "https://upload.wikimedia.org/wikipedia/commons/3/36/Urjalan_kirkko.jpg", "JKorpimies", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Urjala church", "乌尔亚拉教堂"],
    ["fi-vuosaari", "https://commons.wikimedia.org/wiki/File%3AValkopaadentie_Vuosaari_2.jpg", "https://upload.wikimedia.org/wikipedia/commons/d/d7/Valkopaadentie_Vuosaari_2.jpg", "kallerna", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Buses on Valkopaadentie, Vuosaari", "沃萨里瓦尔科帕登路上的公交车"],
    ["fi-pellinki", "https://commons.wikimedia.org/wiki/File%3APellinki_ferry_sea.jpg", "https://upload.wikimedia.org/wikipedia/commons/2/2a/Pellinki_ferry_sea.jpg", "Tappinen", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The ferry to Pellinki", "开往佩林基的渡轮"],
    ["fi-suomussalmi", "https://commons.wikimedia.org/wiki/File%3ASuomussalmen_kirkko.jpg", "https://upload.wikimedia.org/wikipedia/commons/5/57/Suomussalmen_kirkko.jpg", "Mikkoau", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Suomussalmi church", "苏奥穆斯萨尔米教堂"],
    ["hu-doczy", "https://commons.wikimedia.org/wiki/File%3AKossuth_Stra%C3%9Fe_35-37%2C_Links%2C_2022_Debrecen.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/90/Kossuth_Stra%C3%9Fe_35-37%2C_Links%2C_2022_Debrecen.jpg", "Globetrotter19", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The Dóczy Gimnázium building, Debrecen", "德布勒森多齐中学大楼"],
    ["hu-pasaret", "https://commons.wikimedia.org/wiki/File%3ABus_terminus_and_Pasar%C3%A9t_Franciscan_Church%27s_tower._Monument_ID_314_-_Budapest_District_II.%2C_Pasar%C3%A9ti_St.%2C_137_and_Pasar%C3%A9ti_Sq.JPG", "https://upload.wikimedia.org/wikipedia/commons/d/dc/Bus_terminus_and_Pasar%C3%A9t_Franciscan_Church%27s_tower._Monument_ID_314_-_Budapest_District_II.%2C_Pasar%C3%A9ti_St.%2C_137_and_Pasar%C3%A9ti_Sq.JPG", "Globetrotter19", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "Pasaréti tér: the bus terminus and the tower of the Franciscan church", "帕沙雷特广场：公交总站和方济各会教堂的钟楼"],
    ["hu-budapest", "https://commons.wikimedia.org/wiki/File%3AHUN-2015-Budapest-Hungarian_Parliament_%28Budapest%29_2015-02.jpg", "https://upload.wikimedia.org/wikipedia/commons/b/ba/HUN-2015-Budapest-Hungarian_Parliament_%28Budapest%29_2015-02.jpg", "Godot13", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The Hungarian Parliament on the Danube, Budapest", "多瑙河畔的匈牙利国会大厦，布达佩斯"],
    ["hu-attila-ut", "https://commons.wikimedia.org/wiki/File%3AForgalomir%C3%A1ny%C3%ADt%C3%B3_rend%C5%91r%2C_Attila_%C3%BAt%2C_1959_Budapest_-_Fortepan_104163.jpg", "https://upload.wikimedia.org/wikipedia/commons/8/88/Forgalomir%C3%A1ny%C3%ADt%C3%B3_rend%C5%91r%2C_Attila_%C3%BAt%2C_1959_Budapest_-_Fortepan_104163.jpg", "Fortepan / BRFK Hivatala Bűnügyi Technikai Osztály", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "A traffic policeman on Attila út, 1959", "1959 年阿提拉大街上的交通警察"],
    ["hu-eszterhaza", "https://commons.wikimedia.org/wiki/File%3AEsterh%C3%A1zy_Palace%2C_Fert%C5%91d%2C_20220426_1102_5450.jpg", "https://upload.wikimedia.org/wikipedia/commons/f/fc/Esterh%C3%A1zy_Palace%2C_Fert%C5%91d%2C_20220426_1102_5450.jpg", "Jakub Hałun", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Esterházy Palace, Fertőd", "费尔特德的埃斯特哈泽宫"],
    ["ke-bondo", "https://commons.wikimedia.org/wiki/File%3ABondo_Town%2C_Siaya_County%2C_Kenya.jpg", "https://upload.wikimedia.org/wikipedia/commons/1/12/Bondo_Town%2C_Siaya_County%2C_Kenya.jpg", "Mark Souther", "CC BY-SA 2.0", "https://creativecommons.org/licenses/by-sa/2.0", "A street in Bondo town", "邦多镇的街道"],
    ["ke-nairobi", "https://commons.wikimedia.org/wiki/File%3ASkyline_of_Nairobi_06.jpg", "https://upload.wikimedia.org/wikipedia/commons/d/db/Skyline_of_Nairobi_06.jpg", "Cynthia Omondi", "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0", "The skyline of Nairobi", "内罗毕的城市天际线"],
    ["ma-agadir", "https://commons.wikimedia.org/wiki/File%3APlage_d%27Agadir_-_from_Dunes_d%27Or_Hotel_2.jpg", "https://upload.wikimedia.org/wikipedia/commons/8/8e/Plage_d%27Agadir_-_from_Dunes_d%27Or_Hotel_2.jpg", "Ideophagous", "CC0", "http://creativecommons.org/publicdomain/zero/1.0/deed.en", "The beach at Agadir", "阿加迪尔海滩"],
    ["nl-amsterdam", "https://commons.wikimedia.org/wiki/File%3AColorful_canal_houses_at_golden_hour_in_Damrak_avenue_Amsterdam_the_Netherlands.jpg", "https://upload.wikimedia.org/wikipedia/commons/e/ef/Colorful_canal_houses_at_golden_hour_in_Damrak_avenue_Amsterdam_the_Netherlands.jpg", "Basile Morin", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Canal houses on the Damrak, Amsterdam", "阿姆斯特丹达姆拉克的运河房屋"],
    ["nl-voorschoten", "https://commons.wikimedia.org/wiki/File%3AOverzicht_Schoolstraat_naar_het_zuiden_-_Voorschoten_-_20245828_-_RCE.jpg", "https://upload.wikimedia.org/wikipedia/commons/a/ae/Overzicht_Schoolstraat_naar_het_zuiden_-_Voorschoten_-_20245828_-_RCE.jpg", "Gerard Dukker (Rijksdienst voor het Cultureel Erfgoed)", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Schoolstraat in Voorschoten, with the Dorpskerk, 1966", "1966 年福尔斯霍滕的学校街和村教堂"],
    ["nl-westerbork-telescope", "https://commons.wikimedia.org/wiki/File%3AWesterbork_Synthese_Radio_Telescoop.JPG", "https://upload.wikimedia.org/wikipedia/commons/5/5f/Westerbork_Synthese_Radio_Telescoop.JPG", "Onderwijsgek", "CC BY-SA 2.5 nl", "https://creativecommons.org/licenses/by-sa/2.5/nl/deed.en", "The dishes of the Westerbork Synthesis Radio Telescope", "韦斯特博克综合孔径射电望远镜的天线"],
    ["ro-ineu", "https://commons.wikimedia.org/wiki/File%3ABorosjen%C5%91_-_V%C3%A1r_-_panoramio_%286%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/8/85/Borosjen%C5%91_-_V%C3%A1r_-_panoramio_%286%29.jpg", "h_laca", "CC BY 3.0", "https://creativecommons.org/licenses/by/3.0", "Ineu Castle", "伊内乌城堡"],
    ["ro-antim", "https://commons.wikimedia.org/wiki/File%3AAntim_Monastery_Bucharest_%28March_2023%29_-_img_01.jpg", "https://upload.wikimedia.org/wikipedia/commons/b/b4/Antim_Monastery_Bucharest_%28March_2023%29_-_img_01.jpg", "Chainwit.", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The bell-tower gate of Antim Monastery, Bucharest", "布加勒斯特安蒂姆修道院的钟楼门"],
    ["ro-sabasa", "https://commons.wikimedia.org/wiki/File%3AValea_Sabasa_sat_Sabasa_Comuna_Borca.JPG", "https://upload.wikimedia.org/wikipedia/commons/f/f7/Valea_Sabasa_sat_Sabasa_Comuna_Borca.JPG", "Qvadratvs", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The Sabasa valley", "萨巴萨河谷"],
    ["ro-campulung", "https://commons.wikimedia.org/wiki/File%3AM%C4%83n%C4%83stirea_Negru_Vod%C4%83_02.jpg", "https://upload.wikimedia.org/wikipedia/commons/8/88/M%C4%83n%C4%83stirea_Negru_Vod%C4%83_02.jpg", "Nicubunu", "CC BY-SA 3.0 ro", "https://creativecommons.org/licenses/by-sa/3.0/ro/deed.en", "Negru Vodă Monastery, Câmpulung", "肯普隆格的内格鲁沃达修道院"],
    ["ro-silistea", "https://commons.wikimedia.org/wiki/File%3ASili%C8%99tea_Gume%C8%99ti.jpg", "https://upload.wikimedia.org/wikipedia/commons/e/e2/Sili%C8%99tea_Gume%C8%99ti.jpg", "Smugfrog", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Siliștea-Gumești at dusk", "黄昏时的西利什泰亚-古梅什蒂"],
    ["tr-topkapi", "https://commons.wikimedia.org/wiki/File%3ATopkap%C4%B1_-_01.jpg", "https://upload.wikimedia.org/wikipedia/commons/0/06/Topkap%C4%B1_-_01.jpg", "Carlos Delgado", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "Topkapı Palace on Seraglio Point, seen from the water", "从水上望萨拉基里奥角上的托普卡帕宫"],
    ["tr-sehzadebasi", "https://commons.wikimedia.org/wiki/File%3A%C5%9Eehzade_cami_%281%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/b/b5/%C5%9Eehzade_cami_%281%29.jpg", "Yahia.Mokhtar", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The Şehzade Mosque, Istanbul", "伊斯坦布尔的王子清真寺"],
    ["tr-istiklal", "https://commons.wikimedia.org/wiki/File%3AHistoric_tram_on_%C4%B0stiklal_Avenue_-_panoramio.jpg", "https://upload.wikimedia.org/wikipedia/commons/0/09/Historic_tram_on_%C4%B0stiklal_Avenue_-_panoramio.jpg", "Alexey Komarov", "CC BY 3.0", "https://creativecommons.org/licenses/by/3.0", "The historic tram on İstiklal Avenue", "独立大街上的老式有轨电车"],
    ["tr-galata", "https://commons.wikimedia.org/wiki/File%3AIstanbul_Galata_Tower_IMG_8211_1920.jpg", "https://upload.wikimedia.org/wikipedia/commons/1/1f/Istanbul_Galata_Tower_IMG_8211_1920.jpg", "Alexxx1979", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Galata Tower above the rooftops", "屋顶之上的加拉塔塔"],
    ["tr-ankara-sergievi", "https://commons.wikimedia.org/wiki/File%3AAnkara_Opera_House.jpg", "https://upload.wikimedia.org/wikipedia/commons/a/ae/Ankara_Opera_House.jpg", "LoudHmen", "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0", "The Ankara Opera House, the former Exhibition House", "安卡拉歌剧院，原展览馆"],
    ["tr-nisantasi", "https://commons.wikimedia.org/wiki/File%3ANi%C5%9Fanta%C5%9F%C4%B1_Abdi_%C4%B0pek%C3%A7i_Avenue.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/96/Ni%C5%9Fanta%C5%9F%C4%B1_Abdi_%C4%B0pek%C3%A7i_Avenue.jpg", "Metuboy", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Abdi İpekçi Avenue, Nişantaşı", "尼尚塔什的阿布迪·伊佩克奇大街"],
    ["tr-kandilli", "https://commons.wikimedia.org/wiki/File%3A20180114_Bosphorus_7208_%2825277583587%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/6/64/20180114_Bosphorus_7208_%2825277583587%29.jpg", "Ray Swi-hymn from Sijhih-Taipei, Taiwan", "CC BY-SA 2.0", "https://creativecommons.org/licenses/by-sa/2.0", "Kandilli from the Bosphorus", "从博斯普鲁斯海峡上望坎迪利"],
    ["tr-adana", "https://commons.wikimedia.org/wiki/File%3ASheraton_Hotel_Adana_and_Seyhan_River.jpg", "https://upload.wikimedia.org/wikipedia/commons/8/84/Sheraton_Hotel_Adana_and_Seyhan_River.jpg", "ThibautRe", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The Seyhan River at Adana", "阿达纳的塞伊汉河"],
    ["tr-zeyniler", "https://commons.wikimedia.org/wiki/File%3AZeyniler_K%C3%B6y%C3%BC%2C_%C3%87al%C4%B1ku%C5%9Fu_Evi%2C_Bursa.jpg", "https://upload.wikimedia.org/wikipedia/commons/3/32/Zeyniler_K%C3%B6y%C3%BC%2C_%C3%87al%C4%B1ku%C5%9Fu_Evi%2C_Bursa.jpg", "Basak", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The Çalıkuşu House in Zeyniler", "泽伊尼莱尔村的“鹪鹩之家”"],
    ["ua-kyiv-river-port", "https://commons.wikimedia.org/wiki/File%3AKyiv_-_River_Port_and_Podil_buildings.jpg", "https://upload.wikimedia.org/wikipedia/commons/a/ad/Kyiv_-_River_Port_and_Podil_buildings.jpg", "Віктор Полянко", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "The Kyiv river port and the buildings of Podil", "基辅河港与波季尔的建筑"],
    ["ua-kryvorivnia", "https://commons.wikimedia.org/wiki/File%3AKryvorivnia_view_2023.jpg", "https://upload.wikimedia.org/wikipedia/commons/b/b3/Kryvorivnia_view_2023.jpg", "MonX94", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Kryvorivnia in the Carpathians", "喀尔巴阡山中的克里沃里夫尼亚"],
    ["ua-tukhlia", "https://commons.wikimedia.org/wiki/File%3ASaint_Nicholas_church%2C_Tukhlia.jpg", "https://upload.wikimedia.org/wikipedia/commons/f/fb/Saint_Nicholas_church%2C_Tukhlia.jpg", "Dmytro Petishkin", "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0", "St Nicholas Church, Tukhlia", "图赫利亚的圣尼古拉教堂"],
    ["ua-nizhyn", "https://commons.wikimedia.org/wiki/File%3A2005-08-16_Nizhyn_383.JPG", "https://upload.wikimedia.org/wikipedia/commons/7/7d/2005-08-16_Nizhyn_383.JPG", "Norbert Aepli (User:Noebu)", "CC BY 3.0", "https://creativecommons.org/licenses/by/3.0", "Nizhyn railway station", "尼任火车站"],
    ["ua-sosnytsia", "https://commons.wikimedia.org/wiki/File%3AZemstvo_building%2C_Sosnytsia_04.jpg", "https://upload.wikimedia.org/wikipedia/commons/7/7e/Zemstvo_building%2C_Sosnytsia_04.jpg", "Dmytro Petishkin", "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0", "The old zemstvo building, Sosnytsia", "索斯尼齐亚的旧地方自治局大楼"],
    ["ua-odesa-film-studio", "https://commons.wikimedia.org/wiki/File%3AOdessa_Film_Studio.jpg", "https://upload.wikimedia.org/wikipedia/commons/0/00/Odessa_Film_Studio.jpg", "Сіліч Марія", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Odesa Film Studio", "敖德萨电影制片厂"],
]

def thumb(u):
    m = re.match(r"https://upload\.wikimedia\.org/wikipedia/commons/(\w)/(\w\w)/(.+)$", u)
    return f"https://upload.wikimedia.org/wikipedia/commons/thumb/{m.group(1)}/{m.group(2)}/{m.group(3)}/960px-{m.group(3)}" if m else u

def image(pid, url):
    if CACHE and os.path.exists(os.path.join(CACHE, pid + ".jpg")):
        return Image.open(os.path.join(CACHE, pid + ".jpg"))
    f = os.path.join(APP, "images", "places", pid + ".download")
    for u in (thumb(url), url):
        try:
            open(f, "wb").write(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()); break
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(60)
    time.sleep(4)
    im = Image.open(f); im.load(); os.replace(f, f + ".done"); return im

def write(path, s):
    open(path + ".new", "w", encoding="utf-8").write(s); os.replace(path + ".new", path)

assert len({p[0] for p in PHOTOS}) == len(PHOTOS)
files = {}
for pid, page, url, author, lic, lic_url, alt_en, alt_zh in PHOTOS:
    pp = os.path.join(APP, "data", pid.split("-")[0], "places.js")
    s = files.get(pp) or open(pp, encoding="utf-8").read()
    m = re.search(r'(\{ id: "' + re.escape(pid) + r'".*?)( \},?\n)', s)
    assert m, pid
    assert "photo:" not in m.group(1), pid + ": already has a photo"
    im = image(pid, url).convert("RGB")
    if im.width > 800:
        im = im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS)
    assert im.width >= im.height, pid
    rel = f"images/places/{pid}.jpg"
    im.save(os.path.join(APP, rel), "JPEG", quality=82, optimize=True, progressive=True)  # no EXIF carried over
    photo = {"file": rel, "width": im.width, "height": im.height, "author": author, "license": lic, "license_url": lic_url,
             "source": page, "alt_en": alt_en, "alt_zh": alt_zh}
    files[pp] = s[:m.end(1)] + ", photo: " + json.dumps(photo, ensure_ascii=False) + s[m.end(1):]
    name = re.search(r'name: "([^"]*)"', m.group(1)).group(1)
    files.setdefault("credits", []).append(f"| {name} | {author} | [{lic}]({lic_url}) | [Commons]({page}) |")
for pp, s in files.items():
    if pp != "credits": write(pp, s)
cred = os.path.join(APP, "docs", "photo-credits.md")
write(cred, open(cred, encoding="utf-8").read().rstrip("\n") + "\n" + "\n".join(files["credits"]) + "\n")
print(len(files["credits"]), "photos attached")
