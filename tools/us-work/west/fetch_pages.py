from pathlib import Path
import subprocess,concurrent.futures,re,json,html
from urllib.parse import quote
D=Path(__file__).parent
pages=['Marysville, Kansas','Salt Lake City','Virginia City, Nevada','Honolulu','Mount Hood','Seattle','Tacoma, Washington','Wrangell, Alaska','Medicine Bow, Wyoming','Lincoln, Nebraska','Omaha, Nebraska','Ordway, South Dakota','Gallup, New Mexico','Flagstaff, Arizona','Sallisaw, Oklahoma','Weedpatch Camp','Denver','San Francisco','Fargo, North Dakota','Billings, Montana','Kuna, Idaho','Leadville, Colorado']
def f(p):
 url='https://en.wikipedia.org/wiki/'+quote(p.replace(' ','_'))
 path=D/'cache'/(p.replace(' ','_')+'.html')
 if not path.exists(): subprocess.run(['curl','-fsSL',url,'-o',str(path)],check=True)
 s=path.read_text();lat=re.search(r'class="latitude"[^>]*>([^<]+)',s);lon=re.search(r'class="longitude"[^>]*>([^<]+)',s)
 def n(t):
  nums=list(map(float,re.findall(r'[0-9.]+',t)));return round(sum(x/60**i for i,x in enumerate(nums))*(-1 if 'W' in t or 'S' in t else 1),4)
 if not lat or not lon: return p,{'url':url,'error':'no geo'}
 return p,{'url':url,'lat':n(lat[1]),'lon':n(lon[1]),'source_lat':lat[1],'source_lon':lon[1]}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as e: data=dict(e.map(f,pages))
(D/'coordinates.json').write_text(json.dumps(data,indent=2,ensure_ascii=False));print(json.dumps(data,ensure_ascii=False,indent=2))
