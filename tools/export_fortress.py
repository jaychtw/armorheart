"""Refine the approved original editable vector; export registered body states and gun layers."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import xml.etree.ElementTree as E
import hashlib,json,random,base64,copy
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/fortress';OUT.mkdir(exist_ok=True)
source=ROOT/'planning/siege-m4/art/fortress-study.svg';original=source.read_bytes();NS='http://www.w3.org/2000/svg';E.register_namespace('',NS)
def tag(n):return '{'+NS+'}'+n
root=E.fromstring(original);root.set('width','256');root.set('height','160');root.set('viewBox','0 0 256 160');root.set('aria-label','Original Armorheart Fortress: refined stone, roof wear and three stable damage foundations')
# Readable material wear and light/shadow at two pixels per world unit, no changed geometry.
defs=root.find(tag('defs'))
texture=E.SubElement(defs,tag('pattern'),{'id':'wear','width':'64','height':'64','patternUnits':'userSpaceOnUse'})
rng=random.Random(441)
for i in range(180):
 x,y=rng.randrange(64),rng.randrange(64);E.SubElement(texture,tag('path'),{'d':f'M{x} {y}h{rng.choice([.7,1,1.5,2.5])}','stroke':rng.choice(['#f3dfb0','#463c2d','#d3ba83']),'stroke-width':str(rng.choice([.5,.8,1])),'opacity':str(rng.choice([.16,.22,.32]))})
grad=E.SubElement(defs,tag('linearGradient'),{'id':'sunlight','x1':'0','y1':'0','x2':'1','y2':'1'})
for at,color,alpha in [('0','#ffe1a5','.16'),('.5','#f4dfa4','0'),('1','#1d2d23','.25')]:E.SubElement(grad,tag('stop'),{'offset':at,'stop-color':color,'stop-opacity':alpha})
removed=0
for group in [g for g in root if g.tag==tag('g')]:
 for elem in list(group):
  if elem.tag==tag('path') and elem.get('fill') in ['url(#metal)','#222e25']:
   group.remove(elem);removed+=1
 E.SubElement(group,tag('rect'),{'width':'256','height':'160','fill':'url(#wear)','pointer-events':'none'})
 E.SubElement(group,tag('rect'),{'width':'256','height':'160','fill':'url(#sunlight)','pointer-events':'none'})
 # Broad side bevels and stepped roof highlights remain inside physical foundation.
 for d in ['M2 15V145L12 155H244','M13 5H242L251 14','M70 49V124H184']:
  E.SubElement(group,tag('path'),{'d':d,'fill':'none','stroke':'#d5bc85','stroke-width':'1.5','opacity':'.55'})
assert removed==18,removed
master=E.tostring(root,encoding='utf-8',xml_declaration=True);(OUT/'fortress-source.svg').write_bytes(master)
barrel='''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="40" viewBox="-8 -8 16 40"><defs><linearGradient id="m"><stop stop-color="#24372c"/><stop offset=".45" stop-color="#a0a88a"/><stop offset=".7" stop-color="#607059"/><stop offset="1" stop-color="#263a2e"/></linearGradient></defs><path d="M-4 -5H4V24H-4Z" fill="url(#m)" stroke="#263a2c" stroke-width="1.5"/><path d="M-5 20H5V24H-5Z" fill="#283329"/><path d="M-3.5 23.5H3.5" stroke="#141f18"/></svg>'''
cap='''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="-12 -12 24 24"><defs><linearGradient id="c" x2=".5" y2="1"><stop stop-color="#9a9e79"/><stop offset="1" stop-color="#3c503d"/></linearGradient></defs><circle r="10" fill="url(#c)" stroke="#263b2d" stroke-width="2"/><path d="M-7 0A7 7 0 0 1 6 -4" stroke="#bec49b" fill="none"/><path d="M-4 -2H4V3H-4Z" fill="#59684d" stroke="#344b37"/><circle cx="-6" cy="5" r="1" fill="#d7cc9c"/><circle cx="6" cy="5" r="1" fill="#d7cc9c"/></svg>'''
(OUT/'barrel.svg').write_text(barrel);(OUT/'gun-cap.svg').write_text(cap)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);pg=b.new_page();pg.route('**/*',lambda r:r.abort());pg.set_content('<canvas width="512" height="320"></canvas>')
 for stage in ['intact','broken','half']:
  r=copy.deepcopy(root)
  for g in r.findall(tag('g')):g.set('style','display:'+('inline' if g.get('id')==stage else 'none'))
  data=base64.b64encode(E.tostring(r)).decode();encoded=pg.evaluate('''async(data)=>{const im=new Image();im.src='data:image/svg+xml;base64,'+data;await im.decode();const c=document.querySelector('canvas'),x=c.getContext('2d');x.clearRect(0,0,512,320);x.drawImage(im,0,0,512,320);return c.toDataURL('image/png').split(',')[1]}''',data)
  (OUT/(stage+'.png')).write_bytes(base64.b64decode(encoded))
 b.close()
info={'accepted_offer':'a44485475d573d65228d70e377e2561fed9f0e47','authorization':'ce298580273e34da872f1d99e5150edbcc109c12','approved_study_sha256':hashlib.sha256(original).hexdigest(),'source_sha256':hashlib.sha256(master).hexdigest(),'body_world':[256,64,256,160],'body_pixels':[512,320],'gun_pivots':[[288,216],[384,216],[480,216]],'barrel_frame':[-8,-8,16,40],'barrel_axis':'local+Y','muzzle_from_pivot':24,'cap_frame':[-12,-12,24,24],'method':'Original editable approved study with deterministic vector stone wear/light refinement; separate rotating barrel and overlying gun cap; Chromium154 raster export','sha256':{n:hashlib.sha256((OUT/n).read_bytes()).hexdigest() for n in ['intact.png','broken.png','half.png','barrel.svg','gun-cap.svg']}}
(OUT/'anchors.json').write_text(json.dumps(info,indent=2)+'\n');print('Refined Fortress: three512x320 states; all physical corners opaque; registered original gun layers')
