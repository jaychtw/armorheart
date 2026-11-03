"""Continuous configuration-space bound, complementing sampled engine tests.
For each source free-space rectangle/edge/vertex, find a closed legal target
rectangle within19 units of the whole piece; subdivide conservatively if needed.
The corner-distance bound to a convex rectangle covers every point of a piece.
No runtime/accepted-engine code is changed. Floating tolerance is1e-7 units.
"""
from pathlib import Path
import subprocess,json,math,hashlib
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'docs/geometry/r3';spec=json.loads((P/'map.json').read_text());EPS=1e-8;TOL=1e-7;LIMIT=19
hulls=json.loads(subprocess.check_output(['node','--input-type=module','-e',"import {hullBounds} from './src/engine.mjs';console.log(JSON.stringify(Object.fromEntries(['up','right','down','left'].map(f=>[f,hullBounds(0,0,f)]))))"],cwd=ROOT))
def configuration(walls,f):
 h=hulls[f];b=spec['bounds'];domain=(b['left']-EPS-h['left'],b['top']-EPS-h['top'],b['right']+EPS-h['right'],b['bottom']+EPS-h['bottom'])
 obstacles=[(w['x']+EPS-h['right'],w['y']+EPS-h['bottom'],w['x']+64-EPS-h['left'],w['y']+64-EPS-h['top']) for w in walls]
 return domain,obstacles

def legal(x,y,c):
 b,o=c
 return b[0]<=x<=b[2] and b[1]<=y<=b[3] and not any(a<x<d and q<y<e for a,q,d,e in o)

def certify(source,target):
 xs=sorted({v for b,o in [source,target] for r in [b,*o] for v in [r[0],r[2]]});ys=sorted({v for b,o in [source,target] for r in [b,*o] for v in [r[1],r[3]]})
 pieces=[];targets=[]
 for y0,y1 in zip(ys,ys[1:]):
  row=None
  for x0,x1 in zip(xs,xs[1:]):
   x,y=(x0+x1)/2,(y0+y1)/2
   if legal(x,y,source):pieces.append((x0,y0,x1,y1))
   if legal(x,y,target):
    row=(row[0],y0,x1,y1) if row else (x0,y0,x1,y1)
   elif row:targets.append(row);row=None
  if row:targets.append(row)
 # Initial contact-only legal segments and vertices are included explicitly.
 for y in ys:
  pieces.extend((a,y,b,y) for a,b in zip(xs,xs[1:]) if legal((a+b)/2,y,source))
 for x in xs:
  pieces.extend((x,a,x,b) for a,b in zip(ys,ys[1:]) if legal(x,(a+b)/2,source))
 pieces.extend((x,y,x,y) for x in xs for y in ys if legal(x,y,source))
 assert targets
 def distance_bound(r,t):
  # Max distance over a Cartesian rectangle occurs at a corner. The per-axis
  # extrema give that conservative bound without sampling the interior.
  return math.hypot(max(t[0]-r[0],r[2]-t[2],0),max(t[1]-r[1],r[3]-t[3],0))
 stack=[(r,0) for r in pieces];maximum=0;accepted=0;maxdepth=0;unresolved=[]
 while stack:
  r,depth=stack.pop();v=min(distance_bound(r,t) for t in targets)
  if v<=LIMIT+TOL:accepted+=1;maximum=max(maximum,v);maxdepth=max(maxdepth,depth);continue
  if depth>=16:unresolved.append({'piece':r,'upper_bound':v});continue
  if r[2]-r[0]>=r[3]-r[1]:
   m=(r[0]+r[2])/2;children=[(r[0],r[1],m,r[3]),(m,r[1],r[2],r[3])]
  else:
   m=(r[1]+r[3])/2;children=[(r[0],r[1],r[2],m),(r[0],m,r[2],r[3])]
  stack.extend((q,depth+1) for q in children)
 return {'initial_pieces':len(pieces),'certified_pieces':accepted,'maximum_bound':maximum,'maximum_subdivision_depth':maxdepth,'unresolved':unresolved}
cases=[]
for mask in range(16):
 walls=spec['steel']+[w for w in spec['brick'] if not mask>>w['id']&1];cfg={f:configuration(walls,f) for f in hulls}
 for a in hulls:
  for b in hulls:
   if a==b:continue
   r=certify(cfg[a],cfg[b]);assert not r['unresolved'],json.dumps({'mask':mask,'from':a,'to':b,'unresolved':r['unresolved'][:2]});cases.append(dict(mask=mask,initial=a,requested=b,**r))
 print('certified mask',mask,flush=True)
report={'passed':True,'method':'Continuous free configuration-space rectangle/segment/vertex cover; max-corner distance to a closed legal target strip, with recursive conservative subdivision','map_sha256':hashlib.sha256((P/'map.json').read_bytes()).hexdigest(),'engine_sha256':hashlib.sha256((ROOT/'src/engine.mjs').read_bytes()).hexdigest(),'engine_collision_epsilon':EPS,'numeric_tolerance':TOL,'limit':LIMIT,'facing_pairs':len(cases),'certified_pieces':sum(c['certified_pieces'] for c in cases),'maximum_bound':max(c['maximum_bound'] for c in cases),'unresolved_pieces':0,'cases':cases,'reason_engine_bound_applies':'Nearest legal point of axis-aligned rectangular free space is on an obstacle/world face, its corner, or the unchanged coordinate projection. The accepted turn solver enumerates those x/y faces plus the original coordinates and picks minimum valid distance. Existence of a legal target within the bound therefore bounds its chosen correction.','limitations':'Numerical certificate with1e-7 tolerance, not a proof-assistant/interval-arithmetic verification; no artwork, game integration or human acceptance claimed.'}
(P/'continuous-certificate.json').write_text(json.dumps(report,indent=2)+'\n');print('Continuous cases',len(cases),'pieces',report['certified_pieces'],'bound',report['maximum_bound'])
