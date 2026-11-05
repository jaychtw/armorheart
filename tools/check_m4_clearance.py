"""Planning-only continuous certificate, adapted from the accepted R3 proof; no runtime edits."""
import json,subprocess,math,time,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];M=json.load(open(ROOT/'planning/siege-m4/map.json'))
hulls=json.loads(subprocess.check_output(['node','--input-type=module','-e',"import {hullBounds} from './src/engine.mjs';console.log(JSON.stringify(Object.fromEntries(['up','right','down','left'].map(f=>[f,hullBounds(0,0,f)]))))"],cwd=ROOT))
EPS=1e-8
M['walls'].append(dict(id=99,kind='steel',**{k:M['fortress'][k] for k in ['x','y','width','height']}))
B=M['bounds'];bricks=[w['id'] for w in M['walls'] if w['kind']=='brick']
def cfg(walls,f):
 h=hulls[f];bounds=(B['left']-EPS-h['left'],B['top']-EPS-h['top'],B['right']+EPS-h['right'],B['bottom']+EPS-h['bottom'])
 obs=[(w['x']+EPS-h['right'],w['y']+EPS-h['bottom'],w['x']+w['width']-EPS-h['left'],w['y']+w['height']-EPS-h['top']) for w in walls]
 return bounds,obs
def legal(p,c):
 x,y=p;b,obs=c
 return b[0]<=x<=b[2] and b[1]<=y<=b[3] and not any(a<x<c and b<y<d for a,b,c,d in obs)
def certify(walls,f,g):
 a,c=cfg(walls,f),cfg(walls,g)
 xx=sorted({z for b,o in [a,c] for r in [b,*o] for z in [r[0],r[2]]})
 yy=sorted({z for b,o in [a,c] for r in [b,*o] for z in [r[1],r[3]]})
 old=[];target=[]
 for j in range(len(yy)-1):
  run=None
  for i in range(len(xx)-1):
   r=(xx[i],yy[j],xx[i+1],yy[j+1]);p=((r[0]+r[2])/2,(r[1]+r[3])/2)
   if legal(p,a):old.append(r)
   if legal(p,c):
    if run is None:run=r
    else:run=(run[0],run[1],r[2],r[3])
   elif run is not None:target.append(run);run=None
  if run is not None:target.append(run)
 # Include every legal partition edge and vertex, not only open-area cells.
 for y in yy:
  for i in range(len(xx)-1):
   if legal(((xx[i]+xx[i+1])/2,y),a):old.append((xx[i],y,xx[i+1],y))
 for x in xx:
  for j in range(len(yy)-1):
   if legal((x,(yy[j]+yy[j+1])/2),a):old.append((x,yy[j],x,yy[j+1]))
 for x in xx:
  for y in yy:
   if legal((x,y),a):old.append((x,y,x,y))
 # Closed valid target strips are sufficient; no approximation or buffers.
 def bound(r,t):
  dx=max(t[0]-r[0],r[2]-t[2],0);dy=max(t[1]-r[1],r[3]-t[3],0);return math.hypot(dx,dy)
 checked=0;maxbound=0;bad=[]
 def cover(r,depth=0):
  nonlocal checked,maxbound
  checked+=1;v=min(bound(r,t) for t in target)
  if v<=19+1e-7:maxbound=max(maxbound,v);return
  if depth>=12:bad.append((r,v));return
  if r[2]-r[0]>=r[3]-r[1]:
   m=(r[0]+r[2])/2;cover((r[0],r[1],m,r[3]),depth+1);cover((m,r[1],r[2],r[3]),depth+1)
  else:
   m=(r[1]+r[3])/2;cover((r[0],r[1],r[2],m),depth+1);cover((r[0],m,r[2],r[3]),depth+1)
 for r in old:cover(r)
 return {'checked':checked,'bound':maxbound,'bad':bad[:2]}
t=time.time();out=[]
for mask in range(16):
 walls=[w for w in M['walls'] if w['id'] not in {n for i,n in enumerate(bricks) if mask>>i&1}]
 for f in hulls:
  for g in hulls:
   if f==g:continue
   r=certify(walls,f,g);r.update(mask=mask,initial=f,requested=g);out.append(r)
   if r['bad']:print('FAIL',mask,f,g,r);raise SystemExit(1)
print('PASS',len(out),'pairs',sum(r['checked'] for r in out),'rectangles bound',max(r['bound'] for r in out),'secs',time.time()-t)

report={'map_sha256':hashlib.sha256((ROOT/'planning/siege-m4/map.json').read_bytes()).hexdigest(),'engine_sha256':hashlib.sha256((ROOT/'src/engine.mjs').read_bytes()).hexdigest(),'method':'Continuous configuration-space rectangle cover, including legal partition segments/vertices; corner-distance convexity certificates to closed legal target strips; actual engine hulls and EPS=1e-8',
 'numeric_tolerance':1e-7,'destruction_states':16,'facing_pairs':len(out),'covered_pieces':sum(r['checked'] for r in out),'max_certified_distance':max(r['bound'] for r in out),'failures':sum(bool(r['bad']) for r in out),'cases':out}
(ROOT/'evidence/m4/clearance-certificate.json').write_text(json.dumps(report,indent=2)+'\n')
