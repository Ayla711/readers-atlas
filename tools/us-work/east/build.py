"""Rebuild eastern shard from fetched public pages and byte-preserving text slices."""
import json,re,pathlib,hashlib,urllib.parse
from bs4 import BeautifulSoup
D=pathlib.Path(__file__).parent; C=D/'cache'
def dump(n,x): (D/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def read(n): return (C/n).read_bytes().decode('utf-8-sig')
books=[];ev={'books':{},'coordinates':{},'quotes':{},'photos':{},'state_by_place':{}}
B=[('moby-dick','Moby-Dick','白鲸','Herman Melville','赫尔曼·梅尔维尔','1851',2701,1891),('walden','Walden','瓦尔登湖','Henry David Thoreau','亨利·戴维·梭罗','1854',205,1862),('specimen-days','Specimen Days','草叶集外集·典型的日子','Walt Whitman','沃尔特·惠特曼','1882',8813,1892),('little-women','Little Women','小妇人','Louisa May Alcott','路易莎·梅·奥尔科特','1868–1869',514,1888),('great-gatsby','The Great Gatsby','了不起的盖茨比','F. Scott Fitzgerald','F. 斯科特·菲茨杰拉德','1925',64317,1940),('gold-bug','The Gold-Bug','金甲虫','Edgar Allan Poe','埃德加·爱伦·坡','1843',2147,1849),('marrow-of-tradition','The Marrow of Tradition','传统的精髓','Charles W. Chesnutt','查尔斯·W. 切斯纳特','1901',11228,1932),('winesburg-ohio','Winesburg, Ohio','小城畸人','Sherwood Anderson','舍伍德·安德森','1919',416,1941),('new-hampshire','New Hampshire','新罕布什尔','Robert Frost','罗伯特·弗罗斯特','1923',58611,1963),('entailed-hat','The Entailed Hat; Or, Patty Cannon’s Times','世袭的帽子：帕蒂·坎农的时代','George Alfred Townsend','乔治·阿尔弗雷德·汤森','1884',19146,1914)]
for bid,title,zh,a,az,y,pg,death in B:
 books.append(dict(id=bid,title=title,title_zh=zh,author=a,author_zh=az,year=y,orig_lang='en',public_domain=death<=1955,source_url=f'https://www.gutenberg.org/ebooks/{pg}',aliases=[]))
 page=a.replace(' ','_');text=BeautifulSoup(read(page+'.html'),'html.parser').get_text(' ',strip=True);i=text.index('Died')
 assert str(death) in text[i:i+90]
 ev['books'][bid]={'death_year':death,'author_source':'https://en.wikipedia.org/wiki/'+page,'death_evidence':text[i:i+110],'cache':str(C/page)+'.html'}
# id, wiki source, state, bilingual name, type, bilingual note, extras
P=[
('new-bedford','New_Bedford,_Massachusetts','MA','New Bedford','新贝德福德','original','Ishmael visits the city before taking ship for Nantucket; the marker represents the city as a whole.','以实玛利去楠塔基特搭船之前来到这座城市；标记代表整座城市。',{}),
('nantucket-island','Nantucket','MA','Nantucket','楠塔基特岛','original','Melville describes the island as a remote sandy outpost; the marker represents the island as a whole.','梅尔维尔将这座岛描写为偏远的沙地前哨；标记代表全岛。',{}),
('walden-pond','Walden_Pond','MA','Walden Pond','瓦尔登湖','original','Thoreau describes the pond and his life beside it; the marker represents the pond, not an exact cabin location.','梭罗描写这座湖泊以及湖畔生活；标记代表湖泊，并非木屋的精确位置。',{}),
('washington-whitman','Washington,_D.C.','DC','Washington, D.C.','华盛顿特区','original','Whitman records visiting wartime hospitals across the city; this is a city-wide marker.','惠特曼记录了在全城探望战时医院的经历；此标记代表整座城市。',{}),
('falmouth-whitman','Falmouth,_Virginia','VA','Falmouth','法尔茅斯','original','Whitman departs from the military camp at Falmouth with wounded soldiers; the marker represents the town.','惠特曼与伤兵一起离开法尔茅斯的军营；标记代表城镇。',{}),
('camden-whitman','Camden,_New_Jersey','NJ','Camden','卡姆登','original','Whitman returns to Camden and describes a night crossing of the Delaware; the city marker is not a ferry position.','惠特曼返回卡姆登，描写夜渡特拉华河的景象；城市标记并非渡轮所在位置。',{}),
('pittsburgh-whitman','Pittsburgh','PA','Pittsburgh','匹兹堡','original','Whitman describes the industrial city during his 1879 railway journey; the marker represents the city.','惠特曼在一八七九年的铁路旅途中描写这座工业城市；标记代表全城。',{}),
('weirton-panhandle','Weirton,_West_Virginia','WV','Northern Panhandle, represented at Weirton','西弗吉尼亚北部狭长地带 · 魏尔顿代表点','original','The passage concerns the Northern Panhandle as a region. Weirton supplies a representative inland point, not a claimed stop or exact railway alignment.','摘句描写北部狭长地带这一地区。魏尔顿提供内陆代表点，不表示作者在此停留或铁路的精确位置。',{}),
('concord-orchard-house','Orchard_House','MA','Orchard House','康科德 · 果园居','prototype','Alcott wrote and set Little Women at Orchard House; the fictional March family room is not a measured description of the surviving interior.','奥尔科特在果园居写作《小妇人》，并以此为故事背景；马奇家的虚构房间并非现存室内的实测描写。',{'prototype_of':'马奇家的住宅','prototype_of_en':'The March family home'}),
('great-neck-west-egg','Great_Neck,_New_York','NY','Great Neck','大颈镇','prototype','Great Neck is associated with the novel’s West Egg; this marker represents the community, not Gatsby’s fictional mansion.','大颈镇与小说中的西卵相对应；此标记代表社区，而非盖茨比虚构的豪宅。',{'prototype_of':'西卵','prototype_of_en':'West Egg'}),
('manhattan-plaza-hotel','Plaza_Hotel','NY','The Plaza Hotel','曼哈顿 · 广场饭店','original','Jordan tells Nick about Daisy and Gatsby while they sit in the hotel’s tea garden.','乔丹在饭店茶园里向尼克讲述黛西与盖茨比的往事。',{}),
('sullivans-island',"Sullivan's_Island,_South_Carolina",'SC',"Sullivan’s Island",'沙利文岛','original','Poe places Legrand’s retreat on this island; the marker represents the island, not the fictional hut.','坡将勒格朗的隐居处设在这座岛上；标记代表岛屿，而非虚构的小屋。',{}),
('charleston-gold-bug','Charleston,_South_Carolina','SC','Charleston','查尔斯顿','original','The narrator lives in Charleston and travels to visit Legrand; this is a city-wide marker.','叙述者住在查尔斯顿，并从那里前往勒格朗的住处；此标记代表全城。',{}),
('wilmington-wellington','Wilmington,_North_Carolina','NC','Wilmington','威尔明顿','prototype','The fictional Wellington reworks Wilmington and the white-supremacist violence of 1898; the marker represents the city.','虚构的威灵顿以威尔明顿及一八九八年的白人至上主义暴力事件为基础；标记代表全城。',{'prototype_of':'威灵顿','prototype_of_en':'Wellington'}),
('clyde-winesburg','Clyde,_Ohio','OH','Clyde','克莱德','prototype','Anderson’s childhood town helped shape fictional Winesburg; the marker is not the separate real town named Winesburg.','安德森童年居住的城镇启发了虚构的温斯堡；此标记并非另一座真实存在的同名城镇。',{'prototype_of':'温斯堡','prototype_of_en':'Winesburg'}),
('franconia-frost','Franconia,_New_Hampshire','NH','Franconia','弗兰科尼亚','original','The title poem remembers election results displayed at a film screening in Franconia; the marker represents the town.','标题诗回忆弗兰科尼亚一次电影放映中公布选举结果的情景；标记代表城镇。',{}),
('georgetown-entailed-hat','Georgetown,_Delaware','DE','Georgetown','乔治敦','original','Townsend’s fictionalized account sends Patty Cannon to jail here; the marker represents the town, not a surviving jail.','汤森的小说化叙述写到帕蒂·坎农被押往这里的监狱；标记代表城镇，并非现存监狱。',{}),
('laurel-entailed-hat','Laurel,_Delaware','DE','Laurel','劳雷尔','original','Laurel on Broad Creek is named in directions given to Mary; the marker represents the town.','人物为玛丽指路时提到布罗德溪畔的劳雷尔；标记代表城镇。',{}),
('princess-anne-entailed-hat','Princess_Anne,_Maryland','MD','Princess Anne','安妮公主镇','original','The novel opens with the town’s courts, churches and social hierarchy; the marker represents the town.','小说开篇描写城镇的法院、教堂及社会等级；标记代表城镇。',{}),
('dover-entailed-hat','Dover,_Delaware','DE','Dover','多佛','original','Dover is the destination Vesta gives Samson; the marker represents the town as a whole.','维斯塔指定多佛为萨姆森的目的地；标记代表整座城镇。',{}),
('hartford-stowe-house','Harriet_Beecher_Stowe_House_(Hartford,_Connecticut)','CT','Harriet Beecher Stowe House, Hartford','哈特福德 · 哈丽雅特·比彻·斯托故居','pilgrimage','Stowe’s later Hartford home commemorates the author; it is not a setting of Uncle Tom’s Cabin.','斯托晚年在哈特福德的故居用于纪念作者，并非《汤姆叔叔的小屋》的故事地点。',{'book_ids':['uncle-toms-cabin']}),
('brunswick-stowe-house','Harriet_Beecher_Stowe_House_(Brunswick,_Maine)','ME','Harriet Beecher Stowe House, Brunswick','布伦斯威克 · 哈丽雅特·比彻·斯托故居','pilgrimage','Stowe wrote Uncle Tom’s Cabin while living here; the novel’s action is not placed in this house.','斯托在此居住期间写作《汤姆叔叔的小屋》；小说故事并不发生在这座房子里。',{'book_ids':['uncle-toms-cabin']}),
('providence-athenaeum-poe','Providence_Athenaeum','RI','Providence Athenaeum','普罗维登斯雅典娜图书馆','pilgrimage','The library preserves its association with Poe and Sarah Helen Whitman; it is an author pilgrimage stop, not a Gold-Bug setting.','这座图书馆保留了与坡及莎拉·海伦·惠特曼有关的记忆，是作家朝圣地，并非《金甲虫》的故事地点。',{'book_ids':['gold-bug']}),
('shaftsbury-frost-stone-house','Robert_Frost_Stone_House_Museum','VT','Robert Frost Stone House Museum','沙夫茨伯里 · 罗伯特·弗罗斯特石屋博物馆','pilgrimage','Frost wrote the New Hampshire collection at this house; its location does not identify the unnamed woods in individual poems.','弗罗斯特在这座房子写作《新罕布什尔》诗集；故居位置不能用于确定各首诗里未具名的树林。',{'book_ids':['new-hampshire']})]
places=[]
for pid,page,state,n,nz,kind,note,nztext,extra in P:
 url='https://en.wikipedia.org/wiki/'+page
 if pid=='shaftsbury-frost-stone-house':
  raw='42.9345; -73.21016';url='https://mapcarta.com/W1128346439'
 else: raw=re.findall(r'<span class="geo">(.*?)</span>',read(page+'.html'))[0]
 lat,lon=map(float,raw.split(';'))
 place=dict(id=pid,name=n,name_zh=nz,lat=round(lat,4),lon=round(lon,4),place_type=kind,note_en=note,note=nztext,coord_checked=f'{page.replace("_"," ")} — {url}',fact_source='https://en.wikipedia.org/wiki/'+page,**extra)
 if pid=='wilmington-wellington':place['fact_source']='https://en.wikipedia.org/wiki/The_Marrow_of_Tradition'
 if pid=='clyde-winesburg':place['fact_source']='https://en.wikipedia.org/wiki/Winesburg,_Ohio'
 if pid=='shaftsbury-frost-stone-house':place['fact_source']='https://www.bennington.edu/robert-frost-stone-house-museum'
 places.append(place);ev['coordinates'][pid]={'raw':raw,'source':url,'cache':page+'.html'};ev['state_by_place'][pid]=state
lines=[];spec=[]
def q(id,bid,pids,start,end,loc,lzh,zh,hi):
 pg=next(b[6] for b in B if b[0]==bid);t=read(f'pg{pg}.txt');a=t.index(start);z=t.index(end,a)+len(end);text=t[a:z]
 assert len(text)<1800
 line=dict(id=id,book_id=bid,place_ids=pids.split('|'),location=loc,location_zh=lzh,text_en=text,text_zh=zh,highlight_en=hi,translation='original',source={'kind':'gutenberg','id':pg},status='draft')
 lines.append(line);spec.append({'id':id,'pg':pg,'start':start,'end':end});ev['quotes'][id]={'start_offset':a,'end_offset':z,'sha256':hashlib.sha256(text.encode()).hexdigest(),'source_url':f'https://www.gutenberg.org/cache/epub/{pg}/pg{pg}.txt','cache':f'pg{pg}.txt'}
q('usmd-1','moby-dick','new-bedford','In this same New Bedford','I am sure that I did not.','Chapter 7, The Chapel','第7章：礼拜堂','在这同一座新贝德福德城里，有一座捕鲸人的礼拜堂；那些即将驶往印度洋或太平洋、心事重重的渔人，很少有谁不在星期天来此一访。我知道自己也没有错过。',['New Bedford'])
q('usmd-2','moby-dick','nantucket-island','Nantucket! Take out your map','all beach, without a background.','Chapter 14, Nantucket','第14章：楠塔基特','楠塔基特！拿出地图看看吧。看它占据了世界怎样偏僻的一角；它远离海岸，比埃迪斯通灯塔还孤独。瞧，它不过是一个小沙丘、一块弯曲的沙地，尽是海滩，后面再无陆地。',['Nantucket'])
q('uswal-1','walden','walden-pond','When I wrote the following pages','years and two months.','Economy','经济篇','我写下后面这些文字，或者说其中的大部分时，独自住在树林里，离最近的邻居一英里，住的是自己搭建的房屋，坐落在马萨诸塞州康科德的瓦尔登湖畔，完全靠双手劳动谋生。我在那里住了两年两个月。',['Walden Pond'])
q('ussd-1','specimen-days','washington-whitman','I am now remaining in and around Washington','and getting experience.','Back to Washington','重返华盛顿','我现在留在华盛顿及周边，每天探望医院。我常去专利局、第八街、H街、军械库广场及其他医院。如今手头有些钱，替家乡的朋友施助，也渐有经验，能够做一点好事了。',['Washington'])
q('ussd-2','specimen-days','falmouth-whitman',"_January, '63_.--Left camp at Falmouth",'Many wounded were with us on the cars and boat.','Back to Washington','重返华盛顿','一八六三年一月。几天前，我与一些伤兵离开法尔茅斯军营，乘阿奎亚溪铁路，再转乘政府轮船沿波托马克河来到这里。火车和船上都有许多伤兵与我们同行。',['Falmouth'])
q('ussd-3','specimen-days','camden-whitman',"_Nov., '81_.--Again back in Camden.",'inky pall on everything.','An Ossianic Night—Dearest Friends','奥西安式的夜晚——最亲爱的朋友','一八八一年十一月。又回到了卡姆登。今晚九点至十一点，我长时间横渡特拉华河，头顶的景象十分奇特：薄纱似的雾气飞快掠过，后面跟着浓云，给一切罩上漆黑的帷幕。',['Camden'])
q('ussd-4','specimen-days','pittsburgh-whitman','at Pittsburgh in the morning to breakfast.','vast collections of coal-barges.','Begin a Long Jaunt West','开始向西的长途旅行','早晨抵达匹兹堡吃早餐。城市与伯明翰区尽收眼底：雾气与湿气、烟雾、炼焦炉、火焰、变色的木屋，还有大批运煤驳船。',['Pittsburgh'])
q('ussd-5','specimen-days','weirton-panhandle','Presently a bit of fine region, West Virginia, the Panhandle,','crossing the river, the Ohio.','Begin a Long Jaunt West','开始向西的长途旅行','接着是一片美好的地区，西弗吉尼亚的狭长地带，然后渡过俄亥俄河。',['West Virginia'])
q('uslw-1','little-women','concord-orchard-house','It was a comfortable\r\nroom,','pleasant atmosphere of home peace pervaded it.','Chapter 1, Playing Pilgrims','第1章：扮演朝圣者','这是一间舒适的屋子，虽然地毯已经褪色，家具也很简朴，墙上却挂着一两幅好画，壁龛里放满书，窗边盛开着菊花和圣诞玫瑰，满屋洋溢着家庭安宁的愉悦气息。',['comfortable'])
q('usgg-1','great-gatsby','great-neck-west-egg','I lived at West Egg,','places that rented for twelve or fifteen thousand a season.','Chapter 1','第1章','我住在西卵，就是两地中不那么时髦的一处——不过，这个说法太肤浅，无法表达两者间古怪而颇为阴森的差别。我家位于卵形半岛最尖的一端，距海湾只有五十码，夹在两座每季租金高达一万二到一万五千的巨宅之间。',['West Egg'])
q('usgg-2','great-gatsby','manhattan-plaza-hotel','(said Jordan Baker that afternoon,','straight chair in the tea-garden at the Plaza Hotel)','Chapter 4','第4章','那天下午，乔丹·贝克挺直身子坐在广场饭店茶园的一把直背椅上，这样说道。',['Plaza Hotel'])
q('usgb-1','gold-bug','sullivans-island','To\r\n      avoid the mortification','residence at Sullivan’s Island, near Charleston, South Carolina.','Opening, Legrand’s retreat','开篇：勒格朗的隐居处','为了避免遭受厄运后的羞辱，他离开了祖先居住的新奥尔良，搬到南卡罗来纳州查尔斯顿附近的沙利文岛居住。',['Sullivan’s Island'])
q('usgb-2','gold-bug','charleston-gold-bug','my\r\n      residence being, at that time, in Charleston,','re-passage were very far behind those of the present day.','Opening, the October visit','开篇：十月的拜访','我当时住在查尔斯顿，离岛九英里，而往返交通的便利程度远远不及今天。',['Charleston'])
q('usmt-1','marrow-of-tradition','wilmington-wellington',"Twenty years before, Wellington had been the world's greatest",'almost entirely upon cotton for its export business.','Chapter 15, Mrs. Carteret Seeks an Explanation','第15章：卡特雷特夫人寻求解释','二十年前，威灵顿曾是世界上最大的船用物资出口港。可是松节油产业一路南移，身后留下遭毁坏的森林，城市在这项贸易中已跌至第五或第六位，如今出口几乎完全依靠棉花。',['Wellington'])
q('uswo-1','winesburg-ohio','clyde-winesburg','Upon the half decayed veranda','man walked nervously up and down.','Hands','手','在俄亥俄州温斯堡镇附近的一道沟壑边，有一座小木屋；一个矮胖的老人正在它半朽的门廊上，紧张地来回踱步。',['Winesburg, Ohio'])
lines.append(dict(id='usnh-s1',kind='scene',book_id='new-hampshire',place_ids=['franconia-frost'],location='New Hampshire, title poem',location_zh='标题诗《新罕布什尔》',text_en='At a film screening in Franconia, the speaker recalls the audience laughing at a tiny nearby town’s election tally. The moment becomes a meditation on how larger communities look down on smaller ones.',text_zh='叙述者回忆在弗兰科尼亚看电影时，观众看到邻近小镇的选举票数而发笑。这一幕引出他对大社区如何轻视小社区的思考。',highlight_en=['Franconia'],highlight_zh=['弗兰科尼亚'],status='draft',fact_source='https://www.gutenberg.org/ebooks/58611'))
q('useh-1','entailed-hat','princess-anne-entailed-hat','Princess Anne, as its royal name implies,','gentle-minded town on the Eastern Shore.','Chapter 1, Two Hat Wearers','第1章：两个戴帽子的人','安妮公主镇，正如它带有王室意味的名字所示，是东岸一座古老的司法中心，也是一座气质温和的城镇。',['Princess Anne'])
q('useh-2','entailed-hat','georgetown-entailed-hat','The evidence of Cy James and other cowardly companions','closed her in.','Chapter 44, The Death of Patty Cannon','第44章：帕蒂·坎农之死','赛·詹姆斯和其他胆怯的同伙很快作了证，队伍穿过树林和沙地，向东面十二英里外的乔治敦进发。全镇人熬夜等候帕蒂·坎农的到来，她一到便被关进监狱。',['Georgetown'])
q('useh-3','entailed-hat','laurel-entailed-hat',"Take this old woods road", "the creek.",'Chapter 25, The Broad Creek','第25章：布罗德溪','沿着这条旧林间小路，顺布罗德溪走五英里，就到劳雷尔了；那是溪边的一座小镇。',['Laurel'])
q('useh-4','entailed-hat','dover-entailed-hat','"To Dover, in Delaware," Vesta answered.','dark, Samson, and get to Dover to-morrow afternoon."','Chapter 23, A Terrible Crime','第23章：可怕的罪行','“到特拉华州的多佛去，”维斯塔回答，“萨姆森，你天黑前可以骑到劳雷尔，明天下午就能到多佛。”',['Dover'])
files=['Stowe Center for Literary Activism (55618577734).jpg','Whitmore House, Brunswick, ME.jpg','Providence Athenaeum 2024-07-13.jpg','Robert Frost Stone House Museum Shaftsbury 2006.jpg'];licenses=['CC BY 4.0','Public domain','CC BY 4.0','CC BY-SA 3.0'];photos={}
for i,pid in enumerate(['hartford-stowe-house','brunswick-stowe-house','providence-athenaeum-poe','shaftsbury-frost-stone-house']):
 p=next(x for x in places if x['id']==pid);photos[pid]={'commons_file':'File:'+files[i],'alt_en':p['name']+' exterior','alt_zh':p['name_zh']+'外观','crop':None}
 ev['photos'][pid]={'file_page':'https://commons.wikimedia.org/wiki/File:'+urllib.parse.quote(files[i].replace(' ','_')),'license':licenses[i],'cache':f'photo{i}.html'}
# Final independent editorial review: complete sentences, accurate source headings,
# and dated pilgrimage facts. Keep all extraction changes reproducible.
def revise_quote(lid, start, end, zh):
 l=next(x for x in lines if x['id']==lid);pg=l['source']['id'];t=read(f'pg{pg}.txt')
 a=t.index(start);z=t.index(end,a)+len(end);l['text_en']=t[a:z];l['text_zh']=zh
 next(x for x in spec if x['id']==lid).update(start=start,end=end)
 ev['quotes'][lid].update(start_offset=a,end_offset=z,sha256=hashlib.sha256(l['text_en'].encode()).hexdigest())
revise_quote('ussd-4','Oblivious of the two or three hundred miles across','vast collections of coal-barges.','横穿宾夕法尼亚两三百英里的路程，不知不觉便过去了；早晨抵达匹兹堡吃早餐。城市与伯明翰区尽收眼底：雾气与湿气、烟雾、炼焦炉、火焰、变色的木屋，还有大批运煤驳船。')
revise_quote('usgg-2','One October day in nineteen-seventeen—','and half on the lawns.','一九一七年十月的一天——那天下午，乔丹·贝克挺直身子坐在广场饭店茶园的一把直背椅上，这样说道——我正从一个地方走向另一个地方，一会儿走在人行道上，一会儿走在草坪上。')
revise_quote('usgb-2','Just before sunset I scrambled my way through the evergreens to','re-passage were very far behind those of the present day.','日落前，我穿过常青树丛，费力地来到朋友的小屋；我已有几个星期没去看他了。我当时住在查尔斯顿，离岛九英里，而往返交通的便利程度远远不及今天。')
for lid,en,zh in [('usmt-1','Chapter 16, Ellis Takes a Trick','第16章：埃利斯赢得一局'),('useh-3','Chapter 24, Old Chimneys','第24章：旧烟囱'),('useh-4','Chapter 21, Long Separations','第21章：漫长的分别')]:
 next(x for x in lines if x['id']==lid).update(location=en,location_zh=zh)
pilgrimage_notes={
 'hartford-stowe-house':('Harriet Beecher Stowe lived here from 1873 until her death in 1896. Her later home is now a public house museum at the Stowe Center for Literary Activism; Uncle Tom’s Cabin had been published in 1852, before she lived here.','哈丽特·比彻·斯托从一八七三年起住在这里，直至一八九六年去世。这座晚年故居如今是斯托文学行动中心对公众开放的故居博物馆；《汤姆叔叔的小屋》早在一八五二年便已出版，并非在此写成。'),
 'brunswick-stowe-house':('Harriet Beecher Stowe and her family rented this house from 1850 to 1852, when she wrote Uncle Tom’s Cabin. It now belongs to Bowdoin College and contains faculty offices; scheduled public access is limited to Harriet’s Writing Room. The house is not a setting of the novel.','哈丽特·比彻·斯托与家人于一八五〇至一八五二年租住此屋，其间写作《汤姆叔叔的小屋》。房屋现属鲍登学院，内设教师办公室；公众只能按开放安排参观哈丽特写作室。这里并非小说的故事地点。'),
 'providence-athenaeum-poe':('Edgar Allan Poe and Sarah Helen Whitman visited this library during their 1848 courtship; she ended their relationship here on December 23. It remains a member-supported library open to visitors. Poe did not live here, and The Gold-Bug is not set here.','埃德加·爱伦·坡与莎拉·海伦·惠特曼在一八四八年交往期间到访这座图书馆；十二月二十三日，她在这里结束了两人的关系。这里如今仍是向访客开放的会员制图书馆。坡并未居住于此，《金甲虫》的故事也不发生在这里。'),
 'shaftsbury-frost-stone-house':('Robert Frost lived here from 1920 to 1929 and wrote poems collected in New Hampshire, including Stopping by Woods on a Snowy Evening. The house is now a public museum owned by Bennington College; its position does not identify the poem’s unnamed woods.','罗伯特·弗罗斯特于一九二〇至一九二九年居住在此，写下后来收入《新罕布什尔》的诗篇，其中包括《雪夜林边小驻》。这里如今是本宁顿学院所属、对公众开放的博物馆；故居位置不能用于确定诗中未具名的树林。')
}
for p in places:
 p['name_zh']=p['name_zh'].replace('哈丽雅特','哈丽特')
 if p['id'] in pilgrimage_notes:p['note_en'],p['note']=pilgrimage_notes[p['id']]
 if p['id']=='brunswick-stowe-house':p['fact_source']='https://www.bowdoin.edu/english/stowe-house/index.html'
for ph in photos.values():ph['alt_zh']=ph['alt_zh'].replace('哈丽雅特','哈丽特')
photos['brunswick-stowe-house'].update(alt_en='Historical postcard, circa 1905, showing the Harriet Beecher Stowe House in Brunswick',alt_zh='约一九〇五年的历史明信片，展示布伦斯威克的哈丽特·比彻·斯托故居')
for p in places:
 if p['place_type']=='original':
  line=next(l for l in lines if p['id'] in l['place_ids'])
  p['fact_source']=next(b['source_url'] for b in books if b['id']==line['book_id'])
assert len(books)==10 and len(lines)==20 and len(places)==24
for l in lines:
 assert all(h in l['text_en'] for h in l['highlight_en'])
for n,x in [('books.json',books),('places.json',places),('lines.json',lines),('photos.json',photos),('evidence.json',ev),('extraction-specs.json',spec)]:dump(n,x)
print('Built',len(books),len(places),len(lines),len(photos))
