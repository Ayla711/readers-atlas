"""Build west fragment from cached exact Gutenberg bytes and reviewed source data.
Run: python3 tools/us-work/west/build.py
Gutenberg refresh: curl -fL https://www.gutenberg.org/cache/epub/ID/pgID.txt -o cache/pgID.txt
CRLFs are preserved in extracted JSON strings; no whitespace normalization.
"""
import json,re,hashlib
from pathlib import Path
D=Path(__file__).parent
books=[]; places=[]; lines=[]; evidence={'checked':'2026-11-09','coordinates':{},'quotes':{},'scenes':{},'copyright':{},'canon':{}}
def write(n,v): (D/(n+'.json')).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def book(id,title,zh,author,azh,year,death,src,deathsrc):
 books.append(dict(id=id,title=title,title_zh=zh,author=author,author_zh=azh,year=str(year),orig_lang='en',public_domain=death<=1955,source_url=src))
 evidence['copyright'][id]={'author_death_year':death,'source':deathsrc,'rule':'UK life plus 70; project cutoff death <=1955'}
book('roughing-it','Roughing It','苦行记','Mark Twain','马克·吐温',1872,1910,'https://www.gutenberg.org/ebooks/3177','https://marktwainmuseum.org/learn-with-us/twain-faqs/')
book('travels-in-alaska','Travels in Alaska','阿拉斯加游记','John Muir','约翰·缪尔',1915,1914,'https://www.gutenberg.org/ebooks/7345','https://www.nps.gov/jomu/learn/news/100th-anniversary-of-john-muirs-death.htm')
book('virginian','The Virginian: A Horseman of the Plains','弗吉尼亚人','Owen Wister','欧文·威斯特',1902,1938,'https://www.gutenberg.org/ebooks/1298','https://www.penguinrandomhouse.com/authors/2049062/owen-wister/')
book('my-antonia','My Ántonia','我的安东妮亚','Willa Cather','薇拉·凯瑟',1918,1947,'https://www.gutenberg.org/ebooks/242','https://www.nps.gov/people/willa-cather.htm')
books[-1]['aliases']=['My Antonia']
book('o-pioneers','O Pioneers!','啊，拓荒者！','Willa Cather','薇拉·凯瑟',1913,1947,'https://www.gutenberg.org/ebooks/24','https://www.nps.gov/people/willa-cather.htm')
book('main-travelled-roads','Main-Travelled Roads','大路','Hamlin Garland','哈姆林·加兰',1891,1940,'https://www.gutenberg.org/ebooks/2809','https://poets.org/poet/hamlin-garland')
book('grapes-of-wrath','The Grapes of Wrath','愤怒的葡萄','John Steinbeck','约翰·斯坦贝克',1939,1968,'https://en.wikipedia.org/wiki/The_Grapes_of_Wrath','https://sjsu.edu/steinbeck/resources/biography/index.php')
book('on-the-road','On the Road','在路上','Jack Kerouac','杰克·凯鲁亚克',1957,1969,'https://en.wikipedia.org/wiki/On_the_Road','https://en.wikipedia.org/wiki/Jack_Kerouac')
book('travels-with-charley','Travels with Charley: In Search of America','与查理同行','John Steinbeck','约翰·斯坦贝克',1962,1968,'https://en.wikipedia.org/wiki/Travels_with_Charley','https://sjsu.edu/steinbeck/resources/biography/index.php')
book('angle-of-repose','Angle of Repose','安息角','Wallace Stegner','华莱士·斯特格纳',1971,1993,'https://en.wikipedia.org/wiki/Angle_of_Repose','https://en.wikipedia.org/wiki/Wallace_Stegner')
# Coordinates transcribed from fetched Wikipedia coordinate fields, not geocoded/estimated.
rows=[
('marysville','Marysville, Kansas','马里斯维尔',39.84306,-96.63861,'KS'),
('salt-lake-city','Salt Lake City','盐湖城',40.76083,-111.89111,'UT'),
('virginia-city','Virginia City, Nevada','弗吉尼亚城',39.30750,-119.64833,'NV'),
('honolulu','Honolulu','檀香山',21.304650,-157.857217,'HI'),
('mount-hood','Mount Hood','胡德山',45.37361,-121.69583,'OR'),
('seattle','Seattle','西雅图',47.60389,-122.33000,'WA'),
('tacoma','Tacoma, Washington','塔科马',47.24583,-122.45944,'WA'),
('wrangell','Wrangell, Alaska','兰格尔',56.38500,-132.08639,'AK'),
('medicine-bow','Medicine Bow, Wyoming','梅迪辛博',41.89944,-106.20194,'WY'),
('lincoln-nebraska','Lincoln, Nebraska','林肯',40.81028,-96.67472,'NE'),
('omaha','Omaha, Nebraska','奥马哈',41.25861,-95.93750,'NE'),
('ordway','Ordway, South Dakota','奥德韦',45+34/60+43/3600,-(98+24/60+43/3600),'SD'),
('gallup','Gallup, New Mexico','盖洛普',35.51389,-108.74306,'NM'),
('flagstaff','Flagstaff, Arizona','弗拉格斯塔夫',35.18056,-111.62000,'AZ'),
('sallisaw','Sallisaw, Oklahoma','萨利索',35.46056,-94.80722,'OK'),
('weedpatch-camp','Weedpatch Camp','威德帕奇营地',35.22306,-118.90528,'CA'),
('denver','Denver','丹佛',39.74000,-104.99000,'CO'),
('san-francisco','San Francisco','旧金山',37.77750,-122.41639,'CA'),
('fargo','Fargo, North Dakota','法戈',46.87333,-96.82722,'ND'),
('billings','Billings, Montana','比灵斯',45.78361,-108.50611,'MT'),
('kuna','Kuna, Idaho','库纳',43.49028,-116.37167,'ID'),
('leadville','Leadville, Colorado','莱德维尔',39.25056,-106.29111,'CO')]
notes={
'marysville':('Twain passes through Marysville on the overland stage journey. The marker represents the town as a whole.','吐温乘长途驿车经过马里斯维尔；标记代表整个城镇。'),
'salt-lake-city':('Twain describes the city seen against its surrounding mountains. The marker represents the city as a whole.','吐温描写群山映衬下的盐湖城；标记代表整座城市。'),
'virginia-city':('Twain turns a single hay wagon into a newspaper story in this Nevada mining town. The marker represents the town, not a verified newspaper-office address.','吐温在这座内华达矿业城镇把一辆运草车编成多条新闻；标记代表城镇，并非已核实的报社地址。'),
'honolulu':('Twain recalls the fruit available during his visit. The marker represents the city as a whole at its present-day civic center, Honolulu Hale; it does not locate the fruit passage at that building.','吐温回忆在此游览时吃到的水果；以今日市政厅的位置代表整个檀香山，供地图定位；并非指水果片段发生在这座建筑里。'),
'mount-hood':('Muir names Mount Hood in his comparison of Cascade volcanoes. The summit marks the mountain as a whole, not his vantage point.','缪尔比较喀斯喀特火山群时提到胡德山；以山顶代表整座山，并非作者观景的位置。'),
'seattle':('Muir describes Seattle and Tacoma as rival growing towns. The marker represents Seattle as a whole.','缪尔描写西雅图与塔科马这两座互相竞争的新兴城镇；标记代表整个西雅图。'),
'tacoma':('Muir describes Tacoma as Seattle’s rival and a railway terminus. The marker represents the town as a whole.','缪尔将塔科马描写为西雅图的竞争对手及铁路终点；标记代表整个城镇。'),
'wrangell':('Muir arrives here by canoe before planning a journey farther north. The marker represents the settlement, not an identified landing.','缪尔乘独木舟抵达此地，继而筹划继续北行；标记代表聚落，并非已确定的登岸地点。'),
'medicine-bow':('The narrator’s train stops here at the beginning of The Virginian. The marker represents the town rather than an identified historic water tank.','《弗吉尼亚人》开篇，叙述者乘坐的列车在这里停靠；标记代表城镇，并非已确定的历史水塔。'),
'lincoln-nebraska':('Jim stays in Lincoln during his first university summer vacation. The marker represents the city, not a lodging address.','吉姆在大学的第一个暑假留在林肯；标记代表城市，并非他的住址。'),
'omaha':('Marie’s father settles in Omaha and becomes an adviser in its Bohemian community. The marker represents the city as a whole.','玛丽的父亲定居奥马哈，成为当地波希米亚移民的顾问；标记代表整座城市。'),
'ordway':('In the author’s preface, Garland recalls travelling to Ordway, where his parents lived. This is a nonfiction preface location, represented by the settlement point.','加兰在作者序言中回忆前往父母居住的奥德韦；这是非虚构序言中的地点，以聚落坐标代表。'),
'gallup':('Gallup is a named waypoint in the novel’s Route 66 panorama. The marker represents the town, not a particular migrant stop.','盖洛普是小说描写六十六号公路时点名的沿途城镇；标记代表城镇，并非特定移民停靠点。'),
'flagstaff':('Flagstaff is a named waypoint in the novel’s Route 66 panorama. The marker represents the city as a whole.','弗拉格斯塔夫是小说描写六十六号公路时点名的沿途城镇；标记代表整座城市。'),
'sallisaw':('Tom Joad returns to his family’s home near Sallisaw. The town point represents the surrounding setting; it does not locate the fictional farm.','汤姆·乔德回到萨利索附近的家；以城镇坐标代表周边故事区域，并非虚构农场的精确位置。'),
'weedpatch-camp':('The real migrant camp informed the government camp depicted in The Grapes of Wrath. The marker identifies the historic camp.','这座真实的移民劳工营地为《愤怒的葡萄》中的政府营地提供了素材；标记指向历史营地。'),
'denver':('Sal meets Dean, Carlo and their circle in Denver on his first westward trip. The marker represents the city as a whole.','萨尔初次西行时在丹佛与迪安、卡洛及他们的朋友会合；标记代表整座城市。'),
'san-francisco':('Sal’s first westward journey takes him to Remi and a night-watchman job in San Francisco. The marker represents the city, not the camp’s precise site.','萨尔初次西行来到旧金山，投奔雷米并当上守夜人；标记代表城市，并非营地的精确位置。'),
'fargo':('Steinbeck compares the Fargo he visits with the place he has imagined. The marker represents the city as a whole.','斯坦贝克将亲见的法戈与心中的想象比较；标记代表整座城市。'),
'billings':('Steinbeck buys a hat in Billings as he lingers in Montana. The marker represents the city, not an identified shop.','斯坦贝克流连蒙大拿时在比灵斯买了一顶帽子；标记代表城市，并非已确定的店铺。'),
'kuna':('Kuna is one of the Idaho settings in the Wards’ western story. The marker represents the settlement as a whole.','库纳是沃德一家西部经历中的爱达荷地点之一；标记代表整个聚落。'),
'leadville':('Leadville belongs to the Wards’ mining-world itinerary in Angle of Repose. The marker represents the town as a whole.','莱德维尔是《安息角》中沃德一家在矿业世界辗转的地点之一；标记代表整个城镇。')}
for id,name,zh,lat,lon,state in rows:
 url='https://en.wikipedia.org/wiki/'+name.replace(' ','_')
 en,cn=notes[id]
 if id=='honolulu': url='https://en.wikipedia.org/wiki/Honolulu_Hale'
 places.append(dict(id=id,name=name,name_zh=zh,lat=round(lat,4),lon=round(lon,4),place_type='original',note_en=en,note=cn,coord_checked=('Honolulu Hale (representative city point)' if id=='honolulu' else name)+' — '+url,fact_source=url))
 evidence['coordinates'][id]={'state':state,'url':url,'source_lat':lat,'source_lon':lon,'method':'public Wikipedia coordinate field; rounded to four decimals','cache':'cache/Ordway.html' if id=='ordway' else 'cache/coordinate-web-evidence*.json'}
places[15].update(place_type='prototype',prototype_of='《愤怒的葡萄》中的政府移民营地',prototype_of_en='The government migrant camp in The Grapes of Wrath')
def q(id,bid,pg,pids,loc,lzh,start,end,zh,hi,hzh):
 raw=(D/f'cache/pg{pg}.txt').read_bytes();t=raw.decode('utf-8-sig');a=t.index(start);z=t.index(end,a)+len(end);txt=t[a:z]
 lines.append(dict(id=id,book_id=bid,place_ids=pids,location=loc,location_zh=lzh,text_en=txt,text_zh=zh,highlight_en=hi,highlight_zh=hzh,translation='original',source={'kind':'gutenberg','id':pg},status='draft'))
 evidence['quotes'][id]={'url':f'https://www.gutenberg.org/cache/epub/{pg}/pg{pg}.txt','sha256':hashlib.sha256(raw).hexdigest(),'start':start,'end':end,'location':loc,'location_zh':lzh,'character_start':a,'character_end':z,'exact_substring':True,'preserved_crlf':'\r\n' in txt}
q('ri-1','roughing-it',3177,['marysville'],'Chapter 3','第3章','By and by we passed','entered Nebraska.','不久我们经过马里斯维尔，越过大蓝河和小桑迪河；再走大约一英里，就进入了内布拉斯加。',['Marysville'],['马里斯维尔'])
q('ri-2','roughing-it',3177,['salt-lake-city'],'Chapter 13','第13章','Seen from one of these dizzy heights','Chinese wall.','从十二或十五英里外的一处眩目高地望去，大盐湖城的色彩变得柔和，身形也缩小了，仿佛一座玩具村庄，安卧在中国长城般雄伟的屏障之下。',['Salt Lake City'],['盐湖城'])
q('ri-3','roughing-it',3177,['virginia-city'],'Chapter 42','第42章','I canvassed the city again','world before.','我又在城里四处搜寻，只见一辆破旧的运草车从乡下驶来。我却把它利用得十足：将它变成十六辆，从十六个方向进城，编出十六条新闻，让弗吉尼亚城为干草忙得热火朝天，这可是从未有过的事。',['Virginia City'],['弗吉尼亚城'])
q('ri-4','roughing-it',3177,['honolulu'],'Chapter 63','第63章','We had an abundance of fruit','deliciousness itself.','当然，我们在檀香山有许多水果：橙子、菠萝、香蕉、草莓、柠檬、酸橙、芒果、番石榴、甜瓜，还有一种罕见而奇特的美味，叫作秘鲁番荔枝，简直就是美味本身。',['Honolulu'],['檀香山'])
q('tia-1','travels-in-alaska',7345,['mount-hood'],'Chapter 1, Puget Sound and British Columbia','第1章，普吉特海湾与不列颠哥伦比亚','Mt. Baker, to the northward','perhaps the best\r\nknown.','北面的贝克山高约一万零七百英尺，是一座雄伟的山。亚当斯山、圣海伦斯山和胡德山也同样雄伟。其中俯瞰波特兰的胡德山，也许最为人熟知。',['Hood'],['胡德山'])
q('tia-2','travels-in-alaska',7345,['seattle','tacoma'],'Chapter 1, Puget Sound and British Columbia','第1章，普吉特海湾与不列颠哥伦比亚','Seattle was famed','Northern Pacific Railway.','西雅图以煤矿闻名，自称将成为北太平洋海岸的新兴重镇。它的对手塔科马也这样宣称；人们议论纷纷的北太平洋铁路已选定那里作为终点。',['Seattle','Tacoma'],['西雅图','塔科马'])
q('tia-3','travels-in-alaska',7345,['wrangell'],'Chapter 9, A Canoe Voyage to Northward','第9章，乘独木舟北行','I arrived at Wrangell','burned in my mind.','十月，我与一队卡西亚矿工乘独木舟抵达兰格尔，心中仍热切惦念着北方的冰雪世界。',['Wrangell'],['兰格尔'])
q('vir-1','virginian',1298,['medicine-bow'],'Chapter 1, Enter the Man','第1章，人物登场','We had plenty of time','platform of Medicine Bow.','我们有充足的时间观看这番较量，因为列车停了下来，让机车先在水塔旁加水，然后才把我们拉到梅迪辛博的站台边。',['Medicine Bow'],['梅迪辛博'])
q('myan-1','my-antonia',242,['lincoln-nebraska'],'Book 3, Lena Lingard, Chapter 1','第三卷《莉娜·林加德》，第1章','I did not go home for my first summer vacation','entering the freshman class.','第一个暑假我没有回家，而是留在林肯，补修一整年的希腊语；这是我进入一年级时唯一需要补足的条件。',['Lincoln'],['林肯'])
q('opion-1','o-pioneers',24,['omaha'],'Part 2, Neighboring Fields, Chapter 7','第二部《毗邻的田野》，第7章','Marie’s father, Albert Tovesky','adviser among his people there.','玛丽的父亲阿尔伯特·托韦斯基，是十九世纪七十年代初来到西部的波希米亚人中较有见识的一位。他在奥马哈定居，成为当地同乡的领袖和顾问。',['Omaha'],['奥马哈'])
q('mtr-1','main-travelled-roads',2809,['ordway'],'Foreword','前言','In the summer of 1887','farm we had opened on Dry Run prairie in 1871.','一八八七年夏天，我在波士顿住了三年，离开爱荷华北部的旧家也已有六年，终于有钱买车票去南达科他的奥德韦看望父母。绕道迪比克和查尔斯城所费无几，我便打算顺路看看爱荷华的奥塞奇，以及我们一八七一年在德赖兰草原开辟的农场。',['Ordway'],['奥德韦'])
def scene(id,bid,pids,loc,lzh,en,zh,hi,hzh,src):
 lines.append(dict(id=id,kind='scene',book_id=bid,place_ids=pids,location=loc,location_zh=lzh,text_en=en,text_zh=zh,highlight_en=hi,highlight_zh=hzh,status='draft',fact_source=src));evidence['scenes'][id]={'url':src,'method':'Original bilingual synopsis; no book quotation'}
scene('gow-s1','grapes-of-wrath',['gallup','flagstaff'],'Chapter 12','第12章','The account of westward migration follows Route 66 through Gallup and Flagstaff. Families face breakdowns and desert travel while learning to help one another.','描写西迁的章节沿着六十六号公路经过盖洛普和弗拉格斯塔夫。各家面对车辆故障和沙漠旅途，也逐渐学会相互扶持。',['Gallup','Flagstaff'],['盖洛普','弗拉格斯塔夫'],'https://americanliterature.com/author/john-steinbeck/book/the-grapes-of-wrath/chapter-12')
scene('gow-s2','grapes-of-wrath',['sallisaw'],'Opening chapters','开篇数章','Returning from prison to the countryside near Sallisaw, Tom meets Jim Casy. At home they discover that the family has been forced off its land.','汤姆出狱后回到萨利索附近的乡间，遇见吉姆·凯西。他们回家后发现，家人已被迫离开土地。',['Sallisaw'],['萨利索'],'https://en.wikipedia.org/wiki/The_Grapes_of_Wrath')
scene('gow-s3','grapes-of-wrath',['weedpatch-camp'],'Government camp episode','政府营地片段','At the government camp associated with Weedpatch, the Joads find washing facilities and a community governed by its residents. The improvement in daily life cannot solve their shortage of paid work.','在以威德帕奇为背景的政府营地，乔德一家找到了洗浴设施，也见到由居民自治的社区。生活条件改善了，却仍解决不了缺少有酬工作的困境。',['Weedpatch'],['威德帕奇'],'https://www.steinbeckintheschools.com/the-grapes-of-wrath-reading-guides/setting')
scene('otr-s1','on-the-road',['denver'],'Part 1','第一部','On his first trip west, Sal reaches Denver and joins Dean, Carlo and their friends. Their parties and restless plans draw him further into Dean’s circle.','第一次西行时，萨尔抵达丹佛，与迪安、卡洛及朋友们会合。聚会和不断变动的计划让他更深地融入迪安的圈子。',['Denver'],['丹佛'],'https://en.wikipedia.org/wiki/On_the_Road')
scene('otr-s2','on-the-road',['san-francisco'],'Part 1','第一部','In San Francisco, Sal stays with Remi and Lee Ann. Remi finds him work guarding a camp for merchant sailors, but Sal soon moves on.','在旧金山，萨尔与雷米和莉安住在一起。雷米替他找到看守商船海员营地的工作，但萨尔很快又上路了。',['San Francisco'],['旧金山'],'https://en.wikipedia.org/wiki/On_the_Road')
scene('twc-s1','travels-with-charley',['fargo'],'Part 3, North Dakota','第三部，北达科他','Steinbeck arrives in Fargo with a vivid imagined city already in mind. Its everyday bustle differs from that private picture, which he chooses to keep.','斯坦贝克抵达法戈时，心中早已有了一座鲜明的想象之城。眼前日常的繁忙景象与之不同，但他仍愿意保留那个私人想象。',['Fargo'],['法戈'],'https://en.wikipedia.org/wiki/Travels_with_Charley')
scene('twc-s2','travels-with-charley',['billings'],'Part 3, Montana','第三部，蒙大拿','In Billings, Steinbeck buys a hat. Shopping gives him another reason to linger in a state whose towns and people have won his affection.','在比灵斯，斯坦贝克买了一顶帽子。这个州的城镇和居民令他喜爱，购物又给了他一个多逗留片刻的理由。',['Billings'],['比灵斯'],'https://gutenbergcanada.ca/ebooks/steinbeckj-travelswithcharley/steinbeckj-travelswithcharley-00-h.html')
scene('aor-s1','angle-of-repose',['kuna'],'Idaho section, Kuna','爱达荷部分，库纳','The account of the Wards’ Idaho years turns to Kuna. The small settlement becomes a way of conveying the isolation of their western life.','叙述沃德一家在爱达荷的岁月时，故事转向库纳。这个小聚落让人感受到他们西部生活中的孤寂。',['Kuna'],['库纳'],'https://en.wikipedia.org/wiki/Kuna,_Idaho')
scene('aor-s2','angle-of-repose',['leadville'],'Colorado section, Leadville','科罗拉多部分，莱德维尔','The family’s western history includes Leadville, where mining work shapes their circumstances. Lyman reconstructs this world while trying to understand his grandparents’ marriage.','家族的西部经历包括莱德维尔，矿业工作塑造了他们的生活处境。莱曼重建这个世界，试图理解祖父母的婚姻。',['Leadville'],['莱德维尔'],'https://en.wikipedia.org/wiki/Angle_of_Repose')
photos={'weedpatch-camp':{'commons_file':'File:2009-0820-WeedpatchCamp-CommunityHall.jpg','alt_en':'Community hall at Weedpatch Camp','alt_zh':'威德帕奇营地的社区礼堂','crop':None}}
evidence['photos']={'weedpatch-camp':{'file_page':'https://commons.wikimedia.org/wiki/File:2009-0820-WeedpatchCamp-CommunityHall.jpg','license':'CC BY 3.0','author':'Bobak Ha’Eri','verified':'2026-11-09'}}
evidence['canon']={'tier1_authors':['Mark Twain','John Steinbeck','Jack Kerouac','Willa Cather'],'tier2_authors':['Wallace Stegner'],'outside_canon':{'John Muir':'https://www.nps.gov/jomu/index.htm','Owen Wister':'https://travelwyoming.com/listing/medicine-bow-museum/735/','Hamlin Garland':'https://poets.org/poet/hamlin-garland'}}
# Use literary evidence, rather than a geography page, for each place note.
for p in places:
 if p['id']=='weedpatch-camp': continue
 line=next(x for x in lines if p['id'] in x['place_ids'])
 p['fact_source']=line.get('fact_source') or f"https://www.gutenberg.org/ebooks/{line['source']['id']}"
assert len(books)==10 and len(lines)==20 and 20<=len(places)<=26
assert all(x['status']=='draft' for x in lines)
for l in lines:
 assert all(h in l['text_en'] for h in l['highlight_en'])
 assert all(h in l['text_zh'] for h in l['highlight_zh'])
for name,data in [('books',books),('places',places),('lines',lines),('photos',photos),('evidence',evidence)]:write(name,data)
print('Built',len(books),'books',len(places),'places',len(lines),'lines;',len(evidence['quotes']),'byte-preserving source excerpts')
