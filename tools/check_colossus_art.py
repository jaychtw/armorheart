"""Validate registered original frames, actual opaque target cores and paint bounds."""
from pathlib import Path
from PIL import Image
import json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];manifest=json.load(open(ROOT/'assets/colossus/manifest.json'));text=(ROOT/'src/colossus-art.mjs').read_text();art=json.loads(text.split('=',1)[1].rstrip(';\n'));rows=[]
ratio=art['worldPerPixel'];ax,ay=art['anchor'];stops=[(208,288),(560,288),(560,544),(208,544),(384,416)];margin=10000;poses=0
for key,entry in art['images'].items():
 file=ROOT/'assets/colossus/frames'/f'{key}.png';im=Image.open(file);a=im.getchannel('A');assert im.size==(448,448);assert hashlib.sha256(file.read_bytes()).hexdigest()==manifest['frames'][key]['sha256'];bounds=a.getbbox();solid=sum(a.histogram()[200:]);covered=0
 for x,y,w,h in entry['rects']:
  left,top,width,height=round(x/ratio+ax),round(y/ratio+ay),round(w/ratio),round(h/ratio);piece=a.crop((left,top,left+width,top+height));assert piece.getextrema()[0]>=200,(key,x,y,w,h);covered+=width*height
 assert covered/solid>.75,(key,covered/solid)
 if not key.endswith('airborne'):assert abs(entry['bounds'][3]-42)<2
 for x,y in stops:
  l,t,r,b=entry['bounds'];assert x+l>=0 and x+r<=768 and y+t>=0 and y+b<=768
 if key.endswith('airborne'):
  l,t,r,b=entry['bounds']
  for i,(x,y)in enumerate(stops):
   xx,yy=stops[(i+1)%5]
   for n in range(121):
    p=n/120;cx=x+(xx-x)*p;cy=y+(yy-y)*p-64*math.sin(math.pi*p);gap=min(cx+l,768-cx-r,cy+t,768-cy-b);assert gap>0;margin=min(margin,gap);poses+=1
 rows.append(dict(key=key,painted_world_bounds=entry['bounds'],opaque_body_pixels=solid,conservative_core_coverage=covered/solid,target_rects=len(entry['rects'])))
assert manifest['decoded_frame_bytes']<=24*1024*1024
sw=art['images']['south_idle']['bounds'];assert abs((sw[2]-sw[0])-236)<8
report=dict(passed=True,frames=len(rows),source_hashes=manifest['source_sha256'],decoded_bytes=manifest['decoded_frame_bytes'],airborne_bound_samples=poses,minimum_painted_world_margin=margin,south_idle_width=sw[2]-sw[0],geometry_method='opaque4px blocks merged to core rectangles; every represented pixel independently checked alpha>=200; soft fur/gaps excluded',frames_inspected=rows,creative_acceptance='Pending final human review of directional extension and in-game transitions')
(ROOT/'evidence/m2/art-check.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(rows),'frames,',poses,'hop paint-bound samples; min margin',margin)
