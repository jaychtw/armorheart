"""Planning-only, reproducible oriented geometry assessment; no runtime integration.
Uses exact integer route costs:16 units /48u/s =20/60s;90-degree pivot =21/60s.
"""
from pathlib import Path
import math,heapq,json,itertools,hashlib
ROOT=Path(__file__).resolve().parents[2];PATH=ROOT/'docs/geometry/r3';spec=json.loads((PATH/'map.json').read_text());cfg=spec['truck'];bounds=spec['bounds'];exit=spec['exit'];directions=[(0,-16),(16,0),(0,16),(-16,0)]
assert cfg==dict(length=128,width=56,navigationMargin=4,turnRadius=76,spacing=16,speed=48,quarterTurnSeconds=.35)
assert math.hypot(68,32)<76

def rect(s,pad=True):
 x,y,h=s;long=64+(4 if pad else 0);short=28+(4 if pad else 0);w,l=(short,long) if h%2==0 else (long,short)
 return x-w,y-l,x+w,y+l

def clear(box,walls):
 a,b,c,d=box
 return a>=bounds['left'] and c<=bounds['right'] and b>=bounds['top'] and d<=bounds['bottom'] and not any(c>w['x'] and a<w['x']+64 and d>w['y'] and b<w['y']+64 for w in walls)

def turn_clearance(x,y,walls):
 distances=[x-bounds['left'],bounds['right']-x,y-bounds['top'],bounds['bottom']-y]
 distances += [math.hypot(max(w['x']-x,0,x-w['x']-64),max(w['y']-y,0,y-w['y']-64)) for w in walls]
 return min(distances)-76

def build(mask):
 walls=spec['steel']+[w for w in spec['brick'] if not mask>>w['id']&1]
 valid={(x,y,h) for y in range(32,737,16) for x in range(224,545,16) for h in range(4) if clear(rect((x,y,h)),walls)};edges={};goals=set()
 for s in valid:
  x,y,h=s;dx,dy=directions[h];n=(x+dx,y+dy,h);choices=[]
  if n in valid:
   a,b=rect(s),rect(n);swept=(min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3]))
   if clear(swept,walls):choices.append((n,20))
  if turn_clearance(x,y,walls)>=-1e-9:choices.extend([((x,y,(h-1)%4),21),((x,y,(h+1)%4),21)])
  assert all(n in valid for n,_ in choices);edges[s]=choices
  a,b,c,d=rect(s,False)
  if h==0 and a>=exit['left'] and c<=exit['right'] and b>=exit['top'] and d<=exit['bottom']:goals.add(s)
 return {'walls':walls,'valid':valid,'edges':edges,'goals':goals}

def route(graph):
 start=tuple(spec['truckSpawn'][k] for k in ['x','y','heading']);assert start in graph['valid'];counter=itertools.count();q=[(0,next(counter),start)];dist={start:0};parent={};goal=None
 while q:
  cost,_,s=heapq.heappop(q)
  if cost!=dist[s]:continue
  if s in graph['goals']:goal=s;break
  for n,extra in graph['edges'][s]:
   nc=cost+extra
   if nc<dist.get(n,10**9):dist[n]=nc;parent[n]=s;heapq.heappush(q,(nc,next(counter),n))
 if goal is None:return dict(reachable=False,visited=len(dist))
 path=[goal]
 while path[-1]!=start:path.append(parent[path[-1]])
 path.reverse();length=0;turns=0;minimum=math.inf
 for a,b in zip(path,path[1:]):
  assert (b,20 if a[2]==b[2] else 21) in graph['edges'][a]
  assert clear(rect(a),graph['walls']) and clear(rect(b),graph['walls'])
  if a[2]!=b[2]:turns+=1;minimum=min(minimum,turn_clearance(a[0],a[1],graph['walls']))
  else:length+=abs(a[0]-b[0])+abs(a[1]-b[1])
 assert dist[goal]==length//16*20+turns*21
 a,b,c,d=rect(goal,False);assert exit['left']<=a<=c<=exit['right'] and exit['top']<=b<=d<=exit['bottom']
 return dict(reachable=True,cost_ticks_60hz=dist[goal],seconds=dist[goal]/60,distance=length,quarter_turns=turns,min_turn_disc_clearance=minimum,turn_poses=[path[0]]+[b for a,b in zip(path,path[1:]) if a[2]!=b[2]]+[path[-1]],poses=path)

graphs={mask:build(mask) for mask in range(16)};rows=[dict(mask=m,removed=[w['label'] for w in spec['brick'] if m>>w['id']&1],valid_poses=len(g['valid']),**route(g)) for m,g in graphs.items()]
assert not rows[0]['reachable'] and all(not r['reachable'] for r in rows if len(r['removed'])<2)
assert rows[12]['reachable'] and rows[14]['reachable'] and rows[14]['distance']<rows[12]['distance'] and rows[14]['seconds']<rows[12]['seconds']
assert min(r['seconds'] for r in rows if r['reachable'] and len(r['removed'])<=2)>min(r['seconds'] for r in rows if r['reachable'] and len(r['removed'])<=3)
# Wall removal never invalidates a legal moving pose/action; this also validates
# finishing a current safe action before replanning in every one-bit transition.
transitions=0;checked_edges=0
for mask,g in graphs.items():
 for bit in range(4):
  if mask>>bit&1:continue
  nxt=graphs[mask|1<<bit];assert g['valid']<=nxt['valid'];assert g['goals']<=nxt['goals']
  for s,edges in g['edges'].items():
   for edge in edges:assert edge in nxt['edges'][s];checked_edges+=1
  transitions+=1
result={'passed':True,'map_sha256':hashlib.sha256((PATH/'map.json').read_bytes()).hexdigest(),'body':[128,56],'padded':[136,64],'swept_turn_disc_radius':76,'spacing':16,'costs':'forward16=20 ticks;quarter turn=21 ticks;60 ticks per second','all_destruction_states':rows,'monotonicity':{'one_cell_removal_transitions':transitions,'preserved_edges_checked':checked_edges},'limitations':'Exhaustive16 configurations and complete finite oriented lattice; swept boxes/discs continuously certify each returned action. Not actual truck artwork, game integration, browser playthrough or independent human testing.'}
(PATH/'transport-results.json').write_text(json.dumps(result,indent=2)+'\n')
for r in rows:print(r['mask'],r['removed'],{k:r[k] for k in ['reachable','distance','quarter_turns','seconds','min_turn_disc_clearance'] if k in r})
print('Monotonic wall-removal transitions:',transitions)
