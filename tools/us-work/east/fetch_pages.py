import subprocess, pathlib, urllib.parse
p=pathlib.Path(__file__).parent/'cache'
titles=['New_Bedford,_Massachusetts','Nantucket','Walden_Pond','Washington,_D.C.','Falmouth,_Virginia','Camden,_New_Jersey','Pittsburgh','Weirton,_West_Virginia','Orchard_House','Great_Neck,_New_York','Plaza_Hotel',"Sullivan%27s_Island,_South_Carolina",'Charleston,_South_Carolina','Wilmington,_North_Carolina','Clyde,_Ohio','Franconia,_New_Hampshire','Georgetown,_Delaware','Laurel,_Delaware','Princess_Anne,_Maryland','Dover,_Delaware','Harriet_Beecher_Stowe_House_(Hartford,_Connecticut)','Harriet_Beecher_Stowe_House_(Brunswick,_Maine)','Providence_Athenaeum','Robert_Frost_Stone_House_Museum','The_Marrow_of_Tradition','Winesburg,_Ohio','Herman_Melville','Henry_David_Thoreau','Walt_Whitman','Louisa_May_Alcott','F._Scott_Fitzgerald','Edgar_Allan_Poe','Charles_W._Chesnutt','Sherwood_Anderson','Robert_Frost','George_Alfred_Townsend']
for t in titles:
 path=p/(urllib.parse.unquote(t)+'.html')
 if not path.exists():
  subprocess.run(['curl','-fL','--retry','3','--retry-delay','2','https://en.wikipedia.org/wiki/'+urllib.parse.unquote(t)+'?oldformat=true','-o',str(path)],check=True)
