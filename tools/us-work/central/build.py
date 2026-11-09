"""Rebuild central shard from downloaded source caches; no quotation transcription."""
import json,re,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
C=ROOT/'cache'
def dump(name,obj): (ROOT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
books=[]
def book(id,title,zh,author,azh,year,death,pg=None):
 url=f'https://www.gutenberg.org/ebooks/{pg}' if pg else 'https://en.wikipedia.org/wiki/'+title.replace(' ','_')
 books.append(dict(id=id,title=title,title_zh=zh,author=author,author_zh=azh,year=str(year),orig_lang='en',public_domain=death is not None and death<=1955,source_url=url,aliases=[]))
 return id
lm=book('life-on-mississippi','Life on the Mississippi','密西西比河上的生活','Mark Twain','马克·吐温',1883,1910,245)
ut=book('uncle-toms-cabin',"Uncle Tom’s Cabin",'汤姆叔叔的小屋','Harriet Beecher Stowe','哈丽特·比彻·斯托',1852,1896,203)
sc=book('sister-carrie','Sister Carrie','嘉莉妹妹','Theodore Dreiser','西奥多·德莱塞',1900,1945,233)
lh=book('little-house-in-big-woods','Little House in the Big Woods','大森林里的小木屋','Laura Ingalls Wilder','劳拉·英格尔斯·怀尔德',1932,1957)
mk=book('to-kill-a-mockingbird','To Kill a Mockingbird','杀死一只知更鸟','Harper Lee','哈珀·李',1960,2016)
cp=book('color-purple','The Color Purple','紫色','Alice Walker','艾丽斯·沃克',1982,None)
sf=book('sound-and-fury','The Sound and the Fury','喧哗与骚动','William Faulkner','威廉·福克纳',1929,1962)
te=book('their-eyes-were-watching-god','Their Eyes Were Watching God','他们眼望上苍','Zora Neale Hurston','佐拉·尼尔·赫斯顿',1937,1960)
na=book('nick-adams-stories','The Nick Adams Stories','尼克·亚当斯故事集','Ernest Hemingway','欧内斯特·海明威',1972,1961)
ld=book('lonesome-dove','Lonesome Dove','孤鸽镇','Larry McMurtry','拉里·麦克默特里',1985,2021)
places=[]; evidence={'places':{},'quotations':{},'books':{}}
rows=[
('hannibal','Hannibal','汉尼拔','MO','Hannibal,_Missouri'),('memphis','Memphis','孟菲斯','TN','Memphis,_Tennessee'),('helena','Helena','海伦娜','AR','Helena,_Arkansas'),('dubuque','Dubuque','迪比克','IA','Dubuque,_Iowa'),('burlington','Burlington','伯灵顿','IA','Burlington,_Iowa'),('davenport','Davenport','达文波特','IA','Davenport,_Iowa'),('minneapolis','Minneapolis','明尼阿波利斯','MN','Minneapolis'),('saint-paul','Saint Paul','圣保罗','MN','Saint_Paul,_Minnesota'),('new-orleans','New Orleans','新奥尔良','LA','New_Orleans'),('cairo','Cairo','开罗','IL','Cairo,_Illinois'),('louisville','Louisville','路易斯维尔','KY','Louisville,_Kentucky'),('chicago','Chicago','芝加哥','IL','Chicago'),('indianapolis','Indianapolis','印第安纳波利斯','IN','Indianapolis'),('pepin','Pepin','佩平','WI','Pepin,_Wisconsin'),('monroeville','Monroeville','门罗维尔','AL','Monroeville,_Alabama'),('eatonton','Eatonton','伊顿顿','GA','Eatonton,_Georgia'),('oxford','Oxford','牛津','MS','Oxford,_Mississippi'),('eatonville','Eatonville','伊顿维尔','FL','Eatonville,_Florida'),('jacksonville','Jacksonville','杰克逊维尔','FL','Jacksonville,_Florida'),('seney','Seney','塞尼','MI','Seney,_Michigan'),('fox-river','Fox River, Michigan','密歇根州福克斯河','MI','Fox_River_(Michigan)'),('fort-smith','Fort Smith','史密斯堡','AR','Fort_Smith,_Arkansas'),('san-antonio','San Antonio','圣安东尼奥','TX','San_Antonio')]
notes={
'hannibal':('Twain returns to the town where he grew up.','吐温重返自己长大的城镇。',245),
'memphis':('After the Pennsylvania steamboat disaster, Henry and other injured passengers receive care in Memphis.','宾夕法尼亚号汽船失事后，亨利和其他伤员在孟菲斯接受照料。',245),
'helena':('Twain reproduces a historical steamboat record describing a run to Helena.','吐温转录的汽船航行记录提到前往海伦娜的一次航程。',245),
'dubuque':('Twain describes Dubuque during his journey up the Mississippi.','吐温在溯游密西西比河时描写了迪比克。',245),
'burlington':('Twain includes Burlington in his inventory of rapidly growing river cities.','吐温将伯灵顿列入发展迅速的沿河城市名单。',245),
'davenport':('Twain includes Davenport in his inventory of rapidly growing river cities.','吐温将达文波特列入发展迅速的沿河城市名单。',245),
'minneapolis':('Twain lists Minneapolis among the growing cities of the upper river region.','吐温将明尼阿波利斯列入上游地区发展中的城市。',245),
'saint-paul':('The northbound journey ends at Saint Paul.','北上旅程在圣保罗结束。',245),
'new-orleans':('New Orleans is the southern starting point recalled at the end of Twain’s upriver voyage.','吐温在上游旅程的终点回顾了南方出发地新奥尔良。',245),
'cairo':('Twain uses Cairo and New Orleans as endpoints when discussing changes in the river’s length.','吐温讨论河道长度的变化时，以开罗和新奥尔良作为两端。',245),
'louisville':('Aunt Chloe works for a confectioner in Louisville to help raise money to redeem Tom.','克洛伊大娘在路易斯维尔为糖果糕点商工作，筹钱赎回汤姆。',203),
'chicago':('Carrie travels to Chicago to join her sister.','嘉莉前往芝加哥投奔姐姐。',233),
'indianapolis':('Ames identifies Indianapolis as the city he has come from; this is a reference to his home, not a scene taking place there.','艾姆斯说自己来自印第安纳波利斯；这里是人物提到的家乡，并非这段对话的发生地。',233),
'pepin':('Laura and her family visit Pepin in the chapter Going to Town.','在《进城》一章中，劳拉与家人到佩平游览购物。','https://www.storychasers.com/big-woods'),
'monroeville':('Monroeville inspired the fictional town of Maycomb.','门罗维尔是虚构城镇梅科姆的原型。','https://alabama.travel/plan-your-trip/road-trips/monroeville-the-to-kill-a-mockingbird-experience/'),
'eatonton':('Walker’s childhood landscape around Eatonton informs the novel’s rural Georgia setting.','沃克在伊顿顿周边度过童年的乡村环境，为小说中的佐治亚乡村提供了背景。','https://catalog.afi.com/Film/67174-THE-COLOR-PURPLE?cxt=ymal'),
'oxford':('Oxford inspired Faulkner’s fictional Jefferson.','牛津是福克纳笔下虚构城镇杰斐逊的原型。','https://en.wikipedia.org/wiki/Oxford,_Mississippi'),
'eatonville':('Janie lives in Eatonville with Joe Starks, whose store becomes a focus of town life.','珍妮与乔·斯塔克斯住在伊顿维尔；乔的商店是镇上生活的中心之一。','https://en.wikipedia.org/wiki/Their_Eyes_Were_Watching_God'),
'jacksonville':('Janie leaves Eatonville to marry Tea Cake in Jacksonville.','珍妮离开伊顿维尔，前往杰克逊维尔与茶点结婚。','https://en.wikipedia.org/wiki/Their_Eyes_Were_Watching_God'),
'seney':('Nick arrives at the fire-damaged town in Big Two-Hearted River.','在《大双心河》中，尼克来到遭大火毁坏的塞尼。','https://en.wikipedia.org/wiki/Big_Two-Hearted_River'),
'fox-river':('Hemingway’s fishing experience on the Fox River informed Big Two-Hearted River. The map uses the public page’s river marker, not a claimed campsite.','海明威在福克斯河的垂钓经历为《大双心河》提供了素材。地图采用公开页面的河流标记，不指认小说营地。','https://www.michiganhemingwaysociety.org/publications/hemingway-in-seney/'),
'fort-smith':('Sheriff July Johnson leaves Fort Smith in pursuit of Jake Spoon.','警长朱莱·约翰逊离开史密斯堡追捕杰克·斯普恩。','https://en.wikipedia.org/wiki/Lonesome_Dove'),
'san-antonio':('Call returns Gus’s body to the orchard near San Antonio. The city marker represents the surrounding area, not the fictional burial spot.','考尔将格斯的遗体送回圣安东尼奥附近的果园。城市标记代表周边地区，不指认虚构的埋葬地点。','https://en.wikipedia.org/wiki/Lonesome_Dove')}
for id,name,zh,state,page in rows:
 f=C/(id+'.html')
 if id=='hannibal' and not f.exists():f=C/'Hannibal.html'
 html=f.read_text();m=re.search(r'class="geo"[^>]*>(.*?)</span>',html)
 if id=='fox-river':
  m=re.search(r'"coordinates":\[(-?[\d.]+),(-?[\d.]+)\]',html);lon,lat=map(float,m.groups()); raw=m.group()
 else:raw=m.group(1);lat,lon=map(float,raw.split(';'))
 url='https://en.wikipedia.org/wiki/'+page
 en,cn,src=notes[id];src=f'https://www.gutenberg.org/ebooks/{src}' if isinstance(src,int) else src
 p=dict(id=id,name=name,name_zh=zh,lat=round(lat,4),lon=round(lon,4),place_type='original',note_en=en+' The point represents the place as a whole.',note=cn+'坐标代表该地点整体。',coord_checked=f'Wikipedia: {name} — {url}',fact_source=src)
 proto={'monroeville':('Maycomb','梅科姆'),'eatonton':('Celie’s rural Georgia community','西莉生活的佐治亚乡村'),'oxford':('Jefferson','杰斐逊'),'fox-river':('The river in Big Two-Hearted River','《大双心河》中的河流')}
 if id in proto:p.update(place_type='prototype',prototype_of_en=proto[id][0],prototype_of=proto[id][1])
 places.append(p);evidence['places'][id]={'state':state,'coord_source':url,'raw_coordinates':raw,'cache':str(f.relative_to(ROOT)),'fact_source':src}
lines=[];spec=[]
def quote(id,b,pg,ps,chapter,start,end,zh,high):
 raw=(C/f'pg{pg}.txt').read_bytes().decode('utf-8');a=start.replace('\n','\r\n');z=end.replace('\n','\r\n');i=raw.index(a);j=raw.index(z,i)+len(z);q=raw[i:j]
 line=dict(id=id,book_id=b,place_ids=ps,location=f'Chapter {chapter}',location_zh=f'第 {chapter} 章',text_en=q,text_zh=zh,highlight_en=high,translation='original',source={'kind':'gutenberg','id':pg},status='draft')
 lines.append(line);spec.append({'line_id':id,'gutenberg_id':pg,'start':start,'end':end,'start_char':i,'end_char':j});evidence['quotations'][id]={'cache':f'cache/pg{pg}.txt','sha256':hashlib.sha256(raw.encode()).hexdigest(),'exact_substring':True}
quote('lom-1',lm,245,['hannibal'],53,'At seven in the morning we reached Hannibal','was spent.','早上七点，我们抵达密苏里州汉尼拔，我的童年就是在那里度过的。',['Hannibal'])
quote('lom-2',lm,245,['memphis'],20,'Forty of the wounded','nursed the wounded.','四十名伤员被安置在一座大礼堂地板上的铺位上，亨利也在其中。孟菲斯的女士们每天带来鲜花、水果和各种佳肴，留在这里护理伤员。',['Memphis'])
quote('lom-3',lm,245,['helena'],50,'In 1832 steamer','in twelve hours.','1832年，哈德逊号汽船从白河航行至海伦娜，七十五英里的航程用了十二小时。',['Helena'])
quote('lom-4',lm,245,['saint-paul','new-orleans'],60,'WE reached St. Paul','from New Orleans ended.','我们到达密西西比河航运的终点圣保罗，从新奥尔良出发的两千英里航程至此结束。',['St. Paul','New Orleans'])
quote('lom-5',lm,245,['burlington','davenport','minneapolis'],58,'Then we have Muscatine','Minneapolis, sixty thousand and upward.','接下来，马斯卡廷有一万人，威诺纳一万人；莫林一万人，罗克艾兰一万二千人，拉克罗斯一万二千人；伯灵顿两万五千人，迪比克两万五千人；达文波特三万人，圣保罗五万八千人，明尼阿波利斯六万人以上。',['Burlington','Davenport','Minneapolis'])
quote('lom-6',lm,245,['dubuque'],58,'We move up the river--always through enchanting scenery','The lead mines are very productive, and of wide extent.','我们溯河而上，沿途始终是迷人的风景——密西西比河上游处处如此——经过工业重镇莫林，又经过木材业重镇克林顿与莱昂斯，不久便到达坐落在富矿地区的迪比克。这里的铅矿产量很高，分布也很广。',['Dubuque'])
quote('lom-7',lm,245,['cairo'],17,'Therefore, the Mississippi between Cairo','seventy-six years ago.','因此，一百七十六年前，开罗与新奥尔良之间的密西西比河长一千二百一十五英里。',['Cairo'])
quote('utc-1',ut,203,['louisville'],22,'It contained various','the family generally.','信中有许多令人欣慰的家乡消息，这些读者已经知道：克洛伊大娘受雇于路易斯维尔的一位糖果糕点商，她的糕点手艺赚来了可观的收入，汤姆得知这些钱都将存起来为他赎身；摩西与皮特长得很好，小宝宝也已能在屋里走动，由萨莉和家里人照料。',['Louisville'])
quote('sc-1',sc,233,['chicago'],1,'When Caroline Meeber boarded','It was in August, 1889.','卡罗琳·米伯登上开往芝加哥的午后火车时，全部行李只有一只小箱子、一个便宜的仿鳄鱼皮手提包、一份纸盒装午餐，以及一个黄色皮革搭扣钱包。钱包里装着车票、一张写有姐姐在范布伦街住址的纸条和四美元。那是1889年八月。',['Chicago'])
quote('sc-2',sc,233,['indianapolis'],32,'“Yes; I am just on here','completed the last touches of her toilet.','“是的，我从印第安纳波利斯来这里待一周左右，”年轻的艾姆斯说。他坐在椅子边上，等万斯太太完成最后的梳妆。',['Indianapolis'])
def scene(id,b,ps,loc,lzh,en,zh,src,high=[]):lines.append(dict(id=id,kind='scene',book_id=b,place_ids=ps,location=loc,location_zh=lzh,text_en=en,text_zh=zh,highlight_en=high,status='draft',fact_source=src))
scene('lhbw-s1',lh,['pepin'],'Chapter 9, Going to Town','第 9 章《进城》','Laura visits Pepin with her family, sees the lake and explores the unfamiliar sights of the town.','劳拉与家人来到佩平，看见湖泊，探索镇上陌生的新鲜景象。','https://www.storychasers.com/big-woods',['Pepin'])
scene('tkam-s1',mk,['monroeville'],'Trial sequence','审判段落','In Maycomb, Scout and Jem watch Atticus defend Tom Robinson and confront the town’s racial prejudice.','在梅科姆，斯库特和杰姆旁听阿蒂克斯为汤姆·鲁滨逊辩护，面对镇上的种族偏见。','https://en.wikipedia.org/wiki/To_Kill_a_Mockingbird',['Maycomb'])
scene('tcp-s1',cp,['eatonton'],'Opening letters','开篇书信','In rural Georgia, Celie writes to God about the abuse and isolation she experiences within her family.','在佐治亚乡村，西莉写信向上帝诉说自己在家庭中遭受的虐待与孤独。','https://en.wikipedia.org/wiki/The_Color_Purple',['Georgia'])
scene('saf-s1',sf,['oxford'],'Part 4, April 8, 1928','第四部分，1928年4月8日','In Jefferson, Dilsey takes Benjy to an Easter church service as the Compson family continues to unravel.','在杰斐逊，迪尔西带班吉参加复活节礼拜，而康普生一家仍在走向瓦解。','https://en.wikipedia.org/wiki/The_Sound_and_the_Fury',['Jefferson'])
scene('tewwg-s1',te,['eatonville'],'Janie’s marriage to Joe Starks','珍妮与乔·斯塔克斯的婚姻','In Eatonville, Joe Starks builds his standing through his store and public role, while Janie finds her freedom increasingly restricted.','在伊顿维尔，乔·斯塔克斯通过商店和公共职务建立威望，珍妮却感到自己的自由日益受限。','https://en.wikipedia.org/wiki/Their_Eyes_Were_Watching_God',['Eatonville'])
scene('tewwg-s2',te,['jacksonville'],'Janie and Tea Cake’s marriage','珍妮与茶点成婚','Janie leaves Eatonville and travels to Jacksonville to marry Tea Cake, beginning a different life after Joe’s death.','乔去世后，珍妮离开伊顿维尔，前往杰克逊维尔与茶点结婚，开始另一种生活。','https://en.wikipedia.org/wiki/Their_Eyes_Were_Watching_God',['Jacksonville'])
scene('nas-s1',na,['seney'],'Big Two-Hearted River, Part 1','《大双心河》第一部','Nick steps off the train at Seney and finds that fire has destroyed the town before he heads into the countryside.','尼克在塞尼下火车，发现城镇已被大火毁坏，随后走向郊野。','https://en.wikipedia.org/wiki/Big_Two-Hearted_River',['Seney'])
scene('nas-s2',na,['fox-river'],'Big Two-Hearted River, Part 2','《大双心河》第二部','Nick fishes alone and concentrates on the practical details of the river and his tackle; the Fox River supplied the story’s real-world fishing landscape.','尼克独自垂钓，专注于河流与钓具的具体细节；福克斯河为这个故事提供了现实中的垂钓环境。','https://www.michiganhemingwaysociety.org/publications/hemingway-in-seney/',['Fox River'])
scene('ld-s1',ld,['fort-smith'],'July Johnson’s pursuit','朱莱·约翰逊的追捕','After Jake Spoon kills a man in Fort Smith and flees, Sheriff July Johnson sets out to find him.','杰克·斯普恩在史密斯堡杀人后逃走，警长朱莱·约翰逊出发追捕他。','https://en.wikipedia.org/wiki/Lonesome_Dove',['Fort Smith'])
scene('ld-s2',ld,['san-antonio'],'Return to Texas','返回得克萨斯','Call brings Gus’s body back to Texas and buries him near San Antonio, fulfilling his friend’s final request.','考尔将格斯的遗体带回得克萨斯，安葬在圣安东尼奥附近，完成朋友最后的嘱托。','https://en.wikipedia.org/wiki/Lonesome_Dove',['San Antonio'])
canon=json.loads((ROOT.parents[2]/'tools/canon-us.json').read_text())
deaths=[1910,1896,1945,1957,2016,None,1962,1960,1961,2021]
for b,d in zip(books,deaths):
 name=b['author'];evidence['books'][b['id']]={'death_year':d,'living_if_null':True,'copyright_rule':'UK life + 70, cutoff 1955 for 2026','author_source':'https://en.wikipedia.org/wiki/'+name.replace(' ','_'),'author_cache':'cache/author-'+name.replace(' ','_')+'.html','canon_author':next(x for x in canon['authors'] if x['name']==name),'canon_books':[x for x in canon['big_read'] if x['author']==name]}
assert len(books)==10 and len(lines)==20 and 20<=len(places)<=26
assert all(1<=sum(x['book_id']==b['id'] for x in lines)<=10 for b in books)
assert all(h in l['text_en'] for l in lines for h in l.get('highlight_en',[]))
for b in books:
 if not b['public_domain']:assert all(l.get('kind')=='scene' for l in lines if l['book_id']==b['id'])
for name,obj in [('books.json',books),('places.json',places),('lines.json',lines),('photos.json',{}),('evidence.json',evidence),('extractions.json',spec)]:dump(name,obj)
print(f'Built {len(books)} books, {len(places)} places, {len(lines)} lines; {len(spec)} byte-faithful quotations.')
# Human-auditable evidence from the retrieved author infoboxes.
for b in books:
 e=evidence['books'][b['id']];s=(ROOT/e['author_cache']).read_text()
 m=re.search(r'Died.{0,1800}',s)
 if m:
  clean=re.sub('<[^>]+>',' ',m.group());e['death_evidence']=clean.split('(aged')[0].strip()
  assert str(e['death_year']) in e['death_evidence']
 else:
  assert e['death_year'] is None;e['death_evidence']='Fetched biography has no death field; treated as living and copyrighted.'
for x in spec:evidence['quotations'][x['line_id']].update(start_char=x['start_char'],end_char=x['end_char'],source_url=f"https://www.gutenberg.org/cache/epub/{x['gutenberg_id']}/pg{x['gutenberg_id']}.txt")
extras={
'cache/little-house.html':'https://en.wikipedia.org/wiki/Little_House_in_the_Big_Woods',
'cache/mockingbird.html':'https://en.wikipedia.org/wiki/To_Kill_a_Mockingbird',
'cache/color-purple.html':'https://en.wikipedia.org/wiki/The_Color_Purple',
'cache/sound-fury.html':'https://en.wikipedia.org/wiki/The_Sound_and_the_Fury',
'cache/their-eyes.html':'https://en.wikipedia.org/wiki/Their_Eyes_Were_Watching_God',
'cache/lonesome-dove.html':'https://en.wikipedia.org/wiki/Lonesome_Dove',
'cache/nick-adams.html':'https://www.michiganhemingwaysociety.org/publications/hemingway-in-seney/',
'cache/nick-scene.html':'https://en.wikipedia.org/wiki/Big_Two-Hearted_River',
'cache/pepin-scene.html':'https://www.storychasers.com/big-woods',
'cache/maycomb-prototype.html':'https://alabama.travel/plan-your-trip/road-trips/monroeville-the-to-kill-a-mockingbird-experience/',
'cache/eatonton-prototype.html':'https://catalog.afi.com/Film/67174-THE-COLOR-PURPLE?cxt=ymal'}
urls={**{x['cache']:x['coord_source'] for x in evidence['places'].values()},**{x['author_cache']:x['author_source'] for x in evidence['books'].values()},**{x['cache']:x['source_url'] for x in evidence['quotations'].values()},**extras}
evidence['source_caches']=[{'file':f,'url':u,'sha256':hashlib.sha256((ROOT/f).read_bytes()).hexdigest(),'fetched_date':'2026-11-09'} for f,u in urls.items()]
evidence['scene_sources']={l['id']:{'url':l['fact_source'],'cache':next((f for f,u in urls.items() if u==l['fact_source']),None)} for l in lines if l.get('kind')=='scene'}
dump('evidence.json',evidence)
import shlex
(ROOT/'fetch.sh').write_text('#!/bin/sh\nset -eu\ncd "$(dirname "$0")"\nmkdir -p cache\n'+''.join('curl -fL '+shlex.quote(u)+' -o '+shlex.quote(f)+'\nsleep 1\n' for f,u in urls.items()))
counts={s:sum(x['state']==s for x in evidence['places'].values()) for s in sorted({x['state'] for x in evidence['places'].values()})}
(ROOT/'notes.md').write_text('''# Central and Southern US — first-batch shard

10 books, 23 places, exactly 20 draft lines: 10 public-domain extracts and 10 original scene descriptions. No pilgrimage or film-location entries; photos.json is intentionally empty. All mapped cities represent the named settlement as a whole. Fox River uses the coordinate explicitly embedded in the fetched Wikipedia mapframe and is an inspiration/prototype, not an asserted exact fictional fishing spot.

## Reproduction

Run `sh fetch.sh` to refresh the recorded public sources, then `python3 build.py`. The build reads Gutenberg bytes as UTF-8 without newline normalization, finds specified start/end strings, and copies the complete substring including CRLF. `extractions.json` records boundaries and character offsets; `evidence.json` records original file hashes and sources. A refreshed edition can shift offsets or fail an anchor; do not silently adjust quotes. The sources were fetched over the network with curl -fL. An unrelated exploratory Gutenberg download (64310) was not used in any content.

## Selection and copyright

Selection follows tools/canon-us.json. Twain, Stowe, Dreiser, Wilder, Lee, Faulkner, Hurston and Hemingway are tier 1 authors. Walker and McMurtry are tier 2, with The Color Purple and Lonesome Dove explicitly listed by Great American Read. Sister Carrie and The Sound and the Fury are Modern Library selections; Mockingbird and Their Eyes are Great American Read selections. Life on the Mississippi, Uncle Tom’s Cabin, Little House in the Big Woods and The Nick Adams Stories are author-based selections for reliable regional coverage. The Michigan Hemingway Society supplies the Nick Adams geographical rationale. Each book has one to seven lines.

Copyright follows the specified UK death-year cutoff, not US publication dates. Death dates were read from fetched biography infoboxes; see evidence.json. No Hemingway, Wilder, Faulkner, Hurston, Lee, Walker or McMurtry wording is quoted.

'''+ '\n'.join(f"- {b['author']}: {evidence['books'][b['id']]['death_evidence']} — {evidence['books'][b['id']]['author_source']}" for b in books)+ '\n\n## State coverage\n\n'+str(counts)+'''\n
Oklahoma is delegated to the west shard's Sallisaw / The Grapes of Wrath entry and is not falsely assigned to a Lonesome Dove river scene. The Canadian River sequence in that novel was not used to claim an Oklahoma coordinate.

## Scope and editorial limits

Indianapolis is a place explicitly mentioned by Ames in dialogue, not the location of that dialogue; the place note says so. Eatonton is marked as a prototype, supported by AFI’s production history linking the novel to Walker’s childhood landscape. Oxford and Monroeville are prototypes for Jefferson and Maycomb. San Antonio is a regional marker for the nearby fictional burial site and does not claim an identifiable orchard. The population inventory in Life on the Mississippi is historical narration, not present-day demographic information. Draft status is retained throughout.

Reserved proposals Huckleberry Finn, Tom Sawyer, The Awakening and Gone with the Wind were replaced in this shard to cover more states within ten books. No second batch has been started.
''')

# Final identifiers and chapter titles, kept reproducible.
for p in places:
 if p['id']=='oxford':p['id']='oxford-mississippi'
for l in lines:l['place_ids']=['oxford-mississippi' if x=='oxford' else x for x in l['place_ids']]
evidence['places']['oxford-mississippi']=evidence['places'].pop('oxford')
titles={
 'lom-1':("My Boyhood's Home",'童年的故乡'),
 'lom-2':('A Catastrophe','一场灾难'),
 'lom-3':("The 'Original Jacobs'",'最初的雅各布斯'),
 'lom-4':('Speculations and Conclusions','推测与结论'),
 'lom-5':('On the Upper River','在河流上游'),
 'lom-6':('On the Upper River','在河流上游'),
 'lom-7':('Cut-offs and Stephen','河道裁弯与斯蒂芬'),
 'utc-1':('The Grass Withereth—the Flower Fadeth','草必枯干，花必凋残'),
 'sc-1':('The Magnet Attracting: A Waif Amid Forces','磁石的吸引：漂泊的孤女'),
 'sc-2':('The Feast of Belshazzar: A Seer to Translate','伯沙撒的盛宴：解读的先知')}
for l in lines:
 if l['id'] in titles:
  en,zh=titles[l['id']];l['location']+=', '+en;l['location_zh']+='《'+zh+'》'
for name,obj in [('places.json',places),('lines.json',lines),('evidence.json',evidence)]:dump(name,obj)
