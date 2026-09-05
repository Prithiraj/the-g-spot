"""Collect public venue reference images for visual inspection, not publication.
No image in this output has verified commercial reuse rights.
"""
import io, json, re
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageOps, ImageDraw
OUT = Path('research-output'); OUT.mkdir(exist_ok=True)
s = requests.Session(); s.headers['User-Agent'] = 'Mozilla/5.0'
pages = [
 'https://wanderlog.com/place/details/3176375/the-g-spot',
 'https://restaurantguru.com/The-Good-Spot-Lake-Wales',
 'https://maps.roadtrippers.com/us/lake-wales-fl/food-drink/the-g-spot-lake-wales',
 'https://www.facebook.com/Gspotlakewales/',
]
urls = {'https://itin-dev.wanderlogstatic.com/freeImage/ZLuwBthB4kflj2by1LGh3MUggYfsHEMz': pages[0]}
for index, url in enumerate(pages):
 try:
  r = s.get(url, timeout=25); print('PAGE', r.status_code, url)
  if not r.ok: continue
  text=r.text; (OUT/f'page-{index}.html').write_text(text)
  soup=BeautifulSoup(text,'html.parser')
  candidates=[]
  for im in soup.select('img, meta[property="og:image"]'):
   for attr in ['src','data-src','data-original','content']:
    v=im.get(attr,'')
    if v.startswith('http'): candidates.append(v)
  candidates += re.findall(r'https?[^\s"<>\\]+(?:\.jpg|\.jpeg|\.webp)[^\s"<>\\]*',text)
  for v in candidates:
   if any(x in v for x in ['itin-dev.wanderlogstatic','fastly.4sqi','media-cdn.tripadvisor','img.restaurantguru','img02.restaurantguru','img03.restaurantguru','s3-media','scontent','sa0-sp.roadtrippers']):
    if not any(x in v.lower() for x in ['avatar','default','logo','user_','photo-s']): urls.setdefault(v,url)
 except Exception as e: print(type(e).__name__,str(e)[:120])
entries=[]; thumbs=[]
for url,source in list(urls.items())[:35]:
 try:
  r=s.get(url,timeout=20); r.raise_for_status()
  im=Image.open(io.BytesIO(r.content)); im=ImageOps.exif_transpose(im).convert('RGB')
  if min(im.size)<200: continue
  num=len(entries); file=f'{num:02d}.jpg'; im.save(OUT/file,quality=90)
  e={'file':file,'url':url,'source':source,'size':im.size,'rights':'unverified; research only'}; entries.append(e)
  t=Image.new('RGB',(300,250),'white'); t.paste(ImageOps.contain(im,(300,218)),(0,0)); ImageDraw.Draw(t).text((8,225),f'{num:02d} | {im.width} x {im.height}',fill='black'); thumbs.append(t)
  print('IMAGE',num,url)
 except Exception as e: print('SKIP',url[:90],type(e).__name__)
(OUT/'manifest.json').write_text(json.dumps(entries,indent=2))
if thumbs:
 sheet=Image.new('RGB',(900,250*((len(thumbs)+2)//3)),'#cccccc')
 for n,im in enumerate(thumbs): sheet.paste(im,((n%3)*300,(n//3)*250))
 sheet.save(OUT/'contact-sheet.jpg',quality=85)
print('ACQUIRED',len(entries),'reference images. None is cleared for commercial use.')
