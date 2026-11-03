"""Offline geometry assessment only. Not an application/preview module."""
from pathlib import Path
import heapq,itertools,json,math,hashlib
HERE=Path(__file__).resolve().parent
M=json.loads((HERE/'map.json').read_text());B=M['bounds'];E=M['exit'];BRICKS=[w['id'] for w in M['walls'] if w['kind']=='brick']
SPEED=48;TURN=.35;RADIUS=76;DXDY=[(0,-16),(16,0),(0,16),(-16,0)]
def assess(mask):
 removed={n for i,n in enumerate(BRICKS) if mask>>i&1};walls=[(w['x'],w['y'],w['x']+64,w['y']+64) for w in M['walls'] if w['id'] not in removed]
 def clear(r):
  x0,y0,x1,y1=r
  return x0>=B['left'] and x1<=B['right'] and y0>=B['top'] and y1<=B['bottom'] and not any(x1>a and x0<c and y1>b and y0<d for a,b,c,d in walls)
 def rect(s,pad=4):
  x,y,h=s;w,l=(28+pad,64+pad) if h%2==0 else (64+pad,28+pad);return x-w,y-l,x+w,y+l
 def turning(s):
  x,y,_=s
  return x-RADIUS>=B['left'] and x+RADIUS<=B['right'] and y-RADIUS>=B['top'] and y+RADIUS<=B['bottom'] and all(math.hypot(max(a-x,0,x-c),max(b-y,0,y-d))>=RADIUS for a,b,c,d in walls)
 def neighbors(s):
  x,y,h=s;dx,dy=DXDY[h];n=(x+dx,y+dy,h);a=rect(s);b=rect(n)
  if clear((min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3]))):yield n,16/SPEED,'forward'
  if turning(s):
   yield (x,y,(h-1)%4),TURN,'left'
   yield (x,y,(h+1)%4),TURN,'right'
 def goal(s):
  a=rect(s,0);return s[2]==0 and a[0]>=E['left'] and a[2]<=E['right'] and a[1]>=E['top'] and a[3]<=E['bottom']
 start=(M['truck']['x'],M['truck']['y'],M['truck']['heading']);assert clear(rect(start))
 serial=itertools.count();q=[(0,next(serial),start)];distance={start:0};parents={};end=None
 while q:
  cost,_,s=heapq.heappop(q)
  if cost>distance[s]+1e-10:continue
  if goal(s):end=s;break
  for n,dt,action in neighbors(s):
   nc=cost+dt
   if nc<distance.get(n,math.inf)-1e-10:distance[n]=nc;parents[n]=(s,action);heapq.heappush(q,(nc,next(serial),n))
 result={'mask':mask,'removed':sorted(removed),'reachable':end is not None,'visited':len(distance)}
 if end is None:return result
 states=[end];actions=[]
 while states[-1]!=start:
  p,a=parents[states[-1]];actions.append(a);states.append(p)
 states.reverse();actions.reverse()
 # Independently revalidate every recorded action and its full swept volume.
 min_wall_turn_gap=math.inf;min_world_turn_gap=math.inf;max_pose_angle=0
 for a,b,action in zip(states,states[1:],actions):
  assert clear(rect(a)) and clear(rect(b))
  if action=='forward':
   aa=rect(a);bb=rect(b);assert clear((min(aa[0],bb[0]),min(aa[1],bb[1]),max(aa[2],bb[2]),max(aa[3],bb[3])))
  else:
   assert turning(a);x,y,h=a
   min_world_turn_gap=min(min_world_turn_gap,x-B['left']-RADIUS,B['right']-x-RADIUS,y-B['top']-RADIUS,B['bottom']-y-RADIUS)
   min_wall_turn_gap=min(min_wall_turn_gap,*(math.hypot(max(l-x,0,x-r),max(t-y,0,y-bot))-RADIUS for l,t,r,bot in walls))
   # Sample actual padded rectangle corners throughout the certified disc.
   for k in range(91):
    theta=(h*math.pi/2)+(-1 if action=='left' else 1)*k*math.pi/180
    for px,py in [(-32,-68),(32,-68),(32,68),(-32,68)]:
     # Local source rectangle initially points north.
     xx=x+px*math.cos(theta)-py*math.sin(theta);yy=y+px*math.sin(theta)+py*math.cos(theta)
     assert B['left']<=xx<=B['right'] and B['top']<=yy<=B['bottom']
     assert not any(l<xx<r and t<yy<bot for l,t,r,bot in walls)
    max_pose_angle+=1
 turns=sum(a!='forward' for a in actions);movement=16*sum(a=='forward' for a in actions)
 bends=[states[0]]+[b for a,b,act in zip(states,states[1:],actions) if act!='forward']+[states[-1]]
 result.update(travel_units=movement,quarter_turns=turns,predicted_seconds=round(distance[end],9),turn_poses_and_goal=bends,
  turn_disc_min_wall_gap=min_wall_turn_gap,turn_disc_min_world_gap=min_world_turn_gap,angle_samples_checked=max_pose_angle,
  route_states=states,actions=actions,goal_full_body=rect(end,0))
 return result
rows=[assess(mask) for mask in range(16)]
# Stronger than selected-state claims: complete truth table and dominance checks.
for r in rows:assert r['reachable']==({'U0','U1'}<=set(r['removed']))
low=next(r for r in rows if set(r['removed'])=={'U0','U1'})
high=next(r for r in rows if len(r['removed'])==4)
assert high['travel_units']<low['travel_units'] and high['predicted_seconds']<low['predicted_seconds']
assert all(abs(r['predicted_seconds']-low['predicted_seconds'])<1e-8 for r in rows if r['reachable'] and len(r['removed'])==3)
report={'method':'Deterministic orientation-state Dijkstra; forward16 at48 units/s; quarter pivots0.35s; exact swept padded AABBs and conservative76-unit rotation disc',
 'map_sha256':hashlib.sha256((HERE/'map.json').read_bytes()).hexdigest(),'body':[128,56],'padding_per_side':4,'padded_circumradius':math.hypot(68,32),'turn_radius':76,'states':rows}
(HERE/'transport-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps([{k:r[k] for k in ['mask','removed','reachable','travel_units','quarter_turns','predicted_seconds'] if k in r} for r in rows],indent=2))
