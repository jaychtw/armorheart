"""Inspect/export the original alternate SVG bytes; no gameplay or physics substitution."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,base64,hashlib,itertools
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence/v1/assets';OUT.mkdir(parents=True,exist_ok=True)
names=['guardian','bulwark','vanguard','sentinel'];paths={n:ROOT/('assets/guardian' if n=='guardian' else 'assets/tanks/'+n) for n in names};results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);pg=b.new_page();pg.set_content('<canvas width="256" height="256"></canvas>')
 for n in names:
  layers={k:'data:image/svg+xml;base64,'+base64.b64encode((paths[n]/(k+'.svg')).read_bytes()).decode() for k in ['hull','barrel']}
  for age in ['rest','retracted']:
   raw=pg.evaluate('''async ({layers,retracted})=>{const load=async src=>{const i=new Image();i.src=src;await i.decode();return i};const [h,b]=await Promise.all([load(layers.hull),load(layers.barrel)]);const c=document.querySelector('canvas'),x=c.getContext('2d');x.clearRect(0,0,256,256);x.drawImage(b,retracted?-12:0,0);x.drawImage(h,0,0);return c.toDataURL('image/png').split(',')[1]}''',dict(layers=layers,retracted=age=='retracted'))
   (OUT/(n+'-'+age+'.png')).write_bytes(base64.b64decode(raw))
  raw=pg.evaluate('''async src=>{const i=new Image();i.src=src;await i.decode();const c=document.querySelector('canvas'),x=c.getContext('2d');x.clearRect(0,0,256,256);x.drawImage(i,0,0);return c.toDataURL('image/png').split(',')[1]}''',layers['hull']);(OUT/(n+'-hull.png')).write_bytes(base64.b64decode(raw));im=Image.open(OUT/(n+'-hull.png')).convert('RGBA');box=im.getchannel('A').getbbox()
  if n!='guardian':assert box== (12,70,198,185),(n,box)
  assert all(im.getpixel(q)[3]==0 for q in [(0,0),(255,0),(0,255),(255,255)])
  results.append({'tank':n,'hull_alpha_bounds':list(box),'transparent_frame_corners':True,'source_sha256':{k:hashlib.sha256((paths[n]/(k+'.svg')).read_bytes()).hexdigest() for k in ['hull','barrel']}})
 # Original master chart at labeled inspection scale, not claimed as gameplay evidence.
 data={n:'data:image/png;base64,'+base64.b64encode((OUT/(n+'-rest.png')).read_bytes()).decode() for n in names}
 pg.set_viewport_size({'width':1000,'height':420});pg.set_content('<style>body{background:#53604a;color:#f4ecd5;font:16px system-ui}main{display:flex;gap:12px}figure{margin:0}img{width:220px}h1{font-size:20px}</style><h1>Original cosmetic collection / enlarged inspection</h1><main>'+''.join(f'<figure><img src="{data[n]}"><figcaption>{n.title()}</figcaption></figure>' for n in names)+'</main>');pg.screenshot(path=str(OUT/'enlarged-collection.png'));b.close()
masks={n:[p>127 for p in Image.open(OUT/(n+'-hull.png')).getchannel('A').get_flattened_data()] for n in names};pairs=[]
for a,b in itertools.combinations(names,2):
 intersection=sum(x and y for x,y in zip(masks[a],masks[b]));union=sum(x or y for x,y in zip(masks[a],masks[b]));assert intersection<union,(a,b);pairs.append({'a':a,'b':b,'silhouette_iou':intersection/union})
(OUT/'asset-check.json').write_text(json.dumps({'passed':True,'method':'Mixed SVG/paint raster export, actual alpha envelope/corner checks; distinct silhouette masks and independent source geometry. Enlarged chart is inspection only; gameplay-scale evidence supplied separately.','layers':results,'silhouette_pairs':pairs,'game_dev_cli':'not installed; no paid jobs, GLB/package or provider receipts claimed'},indent=2)+'\n');print('PASS four constructions;3new hulls match accepted186x115 master envelope; transparent frames; all pair silhouettes differ')
