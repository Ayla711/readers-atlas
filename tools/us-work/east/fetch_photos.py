import subprocess,pathlib,urllib.parse
p=pathlib.Path(__file__).parent/'cache'
files=['Stowe Center for Literary Activism (55618577734).jpg','Whitmore House, Brunswick, ME.jpg','Providence Athenaeum 2024-07-13.jpg','Robert Frost Stone House Museum Shaftsbury 2006.jpg']
for i,f in enumerate(files):
 subprocess.run(['curl','-fL','https://commons.wikimedia.org/wiki/File:'+urllib.parse.quote(f.replace(' ','_')),'-o',str(p/f'photo{i}.html')],check=True)
