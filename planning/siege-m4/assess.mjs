// Isolated, predetermined motion/ray timelines. NOT an M4 runtime or actual-input test.
import fs from 'node:fs';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import {createState,step,canMove,hullBounds,intersect} from '../../src/engine.mjs';
import {tankShellEntry} from '../../src/interception.mjs';
const C=JSON.parse(fs.readFileSync(new URL('./map.json',import.meta.url))),F=C.fortress,V=C.volley,EPS=1e-8;
const BODY={id:99,kind:'steel',x:F.x,y:F.y,width:F.width,height:F.height};
const allWalls=mask=>C.walls.filter(w=>w.kind!=='brick'||!(mask>>w.id&1));
const facings=['up','right','down','left'];
function path(points,mask=0){const s=createState();s.scenario='study';s.walls=[...allWalls(mask),BODY];s.tank={...C.tank};let time=0,segments=[],correction=0;
 const wait=(until,fire=false)=>{if(until>time+EPS){segments.push({a:time,b:until,p:{...s.tank},q:{...s.tank},fire});time=until;}};
 const face=f=>{const p={...s.tank};step(s,{direction:f},0);correction=Math.max(correction,Math.hypot(s.tank.x-p.x,s.tank.y-p.y));};
 const move=(x,y)=>{for(const [axis,to]of [['x',x],['y',y]]){const delta=to-s.tank[axis];if(Math.abs(delta)<EPS)continue;const dir=axis==='x'?(delta>0?'right':'left'):(delta>0?'down':'up');face(dir);const p={...s.tank},duration=Math.abs(delta)/156;let remain=duration;while(remain>EPS){const dt=Math.min(1/120,remain);step(s,{direction:dir},dt);assert(canMove(s,s.tank.x,s.tank.y));remain-=dt;}assert(Math.abs(s.tank[axis]-to)<1e-6,'Blocked route '+axis);segments.push({a:time,b:time+duration,p,q:{...s.tank},fire:false});time+=duration;}};
 for(const p of points.slice(1))move(...p);
 return {s,segments,get time(){return time;},wait,face,move,get correction(){return correction;}};
}
function finish(p,until=33){p.wait(until,true);const segments=p.segments;const at=t=>{const e=segments.find(e=>t<e.b-EPS)??segments.at(-1);const k=Math.max(0,Math.min(1,(t-e.a)/(e.b-e.a)));return{x:e.p.x+(e.q.x-e.p.x)*k,y:e.p.y+(e.q.y-e.p.y)*k,facing:e.p.facing};};return{segments,at,correction:p.correction};}
function heldAt(x,y,delay=0){const edge=x>384?576:192;const p=path(y<608?[[384,688],[edge,688],[edge,y],[x,y]]:[[384,688],[x,688],[x,y]]);p.face('up');p.wait(p.time+delay);return finish(p);}
function dodge(side){const x=side==='left'?288:480,edge=side==='left'?192:576;const p=path([[384,688],[edge,688],[edge,480],[x,480]]);p.face('up');p.wait(6,true);
 for(let launch=6;launch<=30;launch+=3){p.move(384,480);p.wait(launch+1.8);p.move(x,480);p.face('up');p.wait(launch+3,true);}return finish(p,33);}
function port(tank,chosen=null){let i=chosen??0;for(let j=1;chosen===null&&j<3;j++)if(Math.abs(F.gunPivots[j][0]-tank.x)<Math.abs(F.gunPivots[i][0]-tank.x)-EPS)i=j;const [x,y]=F.gunPivots[i],angle=Math.atan2(tank.y-y,tank.x-x);return{i,x:x+24*Math.cos(angle),y:y+24*Math.sin(angle),angle};}
function timeline(T,mask=0,until=30){let walls=allWalls(mask),t=0,active=[],launches=[],wallHits=[],bossHits=[],tankContacts=[],serial=0,peak=0;
 const events=[];let next=0;
 for(const e of T.segments)if(e.fire){let at=Math.max(e.a,next);while(at<Math.min(e.b,until)-EPS){events.push({at,kind:'player'});next=at+1;at=next;}}
 for(let at=3;at<=until;at+=3)events.push({at,kind:'enemy'});
 events.sort((a,b)=>a.at-b.at||a.kind.localeCompare(b.kind));
 const collision=b=>{let best=null;const take=(at,kind,item)=>{if(at<t-EPS)return;if(!best||at<best.at-EPS||(Math.abs(at-best.at)<EPS&&(kind==='wall'||item?.id<best.item?.id)))best={at,kind,item,b};};
  const vx=b.dx*b.speed,vy=b.dy*b.speed;
  let life=until-b.born;
  if(vx>EPS)life=Math.min(life,(768-b.x)/vx);if(vx< -EPS)life=Math.min(life,-b.x/vx);if(vy>EPS)life=Math.min(life,(768-b.y)/vy);if(vy< -EPS)life=Math.min(life,-b.y/vy);
  for(const w of walls){const f=b.enemy?tankShellEntry(b.x,b.y,vx*life,vy*life,{left:w.x,top:w.y,right:w.x+w.width,bottom:w.y+w.height},4):intersect(b.x,b.y,vx*life,vy*life,w);if(f!==null)take(b.born+life*f,'wall',w);}
  if(!b.enemy){const f=intersect(b.x,b.y,vx*life,vy*life,F);if(f!==null)take(b.born+life*f,'boss',F);}
  else for(const e of T.segments){const a=Math.max(b.born,e.a,t),z=Math.min(b.born+life,e.b,until);if(z<a+EPS)continue;const p=T.at(a+1e-9),q={x:e.p.x+(e.q.x-e.p.x)*(z-e.a)/(e.b-e.a),y:e.p.y+(e.q.y-e.p.y)*(z-e.a)/(e.b-e.a)};const f=tankShellEntry(b.x+vx*(a-b.born)-p.x,b.y+vy*(a-b.born)-p.y,vx*(z-a)-(q.x-p.x),vy*(z-a)-(q.y-p.y),hullBounds(0,0,p.facing),4);if(f!==null)take(a+(z-a)*f,'tank',null);}
  take(b.born+life,'exit',null);return best;
 };
 while(t<until-EPS){const hits=active.map(collision).filter(Boolean),at=Math.min(events[0]?.at??Infinity,...hits.map(h=>h.at),until);t=at;
  // All coincident impacts see the same cover. Remove bricks only after consuming rays.
  const batch=hits.filter(h=>Math.abs(h.at-at)<EPS),gone=new Set();
  for(const h of batch){active=active.filter(b=>b!==h.b);if(h.kind==='wall'){wallHits.push({at,id:h.item.id,kind:h.item.kind,side:h.b.enemy?'enemy':'player'});if(h.item.kind==='brick')gone.add(h.item.id);}if(h.kind==='boss')bossHits.push(at);if(h.kind==='tank')tankContacts.push(at);}
  walls=walls.filter(w=>!gone.has(w.id));
  while(events.length&&events[0].at<=at+EPS){const e=events.shift(),p=T.at(e.at);
   if(e.kind==='enemy'){const o=port(p,port(T.at(e.at-.6)).i);const rounds=V.offsetDegrees.map(deg=>{const a=o.angle+deg*Math.PI/180;return{id:serial++,enemy:true,born:e.at,x:o.x,y:o.y,dx:Math.cos(a),dy:Math.sin(a),speed:180};});active.push(...rounds);launches.push({at:e.at,port:o.i,origin:[o.x,o.y],target:[p.x,p.y],anglesDegrees:rounds.map(b=>Math.atan2(b.dy,b.dx)*180/Math.PI)});}
   else{const dirs={up:[0,-1],right:[1,0],down:[0,1],left:[-1,0]},[dx,dy]=dirs[p.facing];let hit=null;for(const w of walls){const f=intersect(p.x,p.y,dx*68,dy*68,w);if(f!==null&&(!hit||f<hit.f-EPS||(Math.abs(f-hit.f)<EPS&&w.id<hit.w.id)))hit={w,f};}const target=intersect(p.x,p.y,dx*68,dy*68,F);if(target!==null&&(!hit||target<hit.f-EPS))bossHits.push(e.at);else if(hit){wallHits.push({at:e.at,id:hit.w.id,kind:hit.w.kind,side:'player'});if(hit.w.kind==='brick')walls=walls.filter(w=>w.id!==hit.w.id);}else active.push({id:serial++,enemy:false,born:e.at,x:p.x+dx*68,y:p.y+dy*68,dx,dy,speed:480});}
  }
  peak=Math.max(peak,active.filter(b=>b.enemy).length);
 }
 const effective=[];for(const at of tankContacts.sort((a,b)=>a-b))if(!effective.length||at>=effective.at(-1)+3-EPS)effective.push(at);
 const eighth=bossHits[7]??null,third=effective[2]??null;
 return {eighthTargetHit:eighth,thirdEffectiveContact:third,clearBeforeThirdContact:eighth!==null&&(third===null||eighth<third-EPS),effectiveContactsBeforeEighth:effective.filter(t=>eighth===null||t<=eighth).length,potentialEffectiveContacts:effective,bossHitTimes:bossHits.slice(0,8),coverHits:wallHits.filter(h=>h.kind==='brick'),remainingBricks:walls.filter(w=>w.kind==='brick').map(w=>w.id),peakEnemyRounds:peak,launches,method:'predetermined motion + analytical rays/event ordering; contact opportunities with3s filtering, not a playable mission or actual-input test'};
}
const routes=[];
for(let mask=0;mask<16;mask++)for(const[name,points]of Object.entries(C.routes)){const p=path(points,mask);routes.push({mask,name,travelSeconds:p.time,correction:p.correction,endpoint:{x:p.s.tank.x,y:p.s.tank.y}});assert(p.correction<=19+EPS);}
const cases={spawnHeld:timeline(heldAt(384,688)),leftDodge:timeline(dodge('left')),rightDodge:timeline(dodge('right'))};
const destructionExamples=[];for(let mask=0;mask<16;mask++)for(const side of ['left','right']){const r=timeline(dodge(side),mask);destructionExamples.push({mask,side,eighthTargetHit:r.eighthTargetHit,thirdEffectiveContact:r.thirdEffectiveContact,contacts:r.effectiveContactsBeforeEighth,clear:r.clearBeforeThirdContact,peak:r.peakEnemyRounds});assert(r.clearBeforeThirdContact,'Missing partial-destruction motion solution');}
const stations=[];for(const x of[288,384,480])for(const y of[688,480])for(const delay of[0,.75,1.5,2.25]){const r=timeline(heldAt(x,y,delay));stations.push({x,y,delay,...r});}
assert.equal(cases.spawnHeld.eighthTargetHit,null,'Spawn should not shoot through steel');
assert(cases.leftDodge.clearBeforeThirdContact&&cases.rightDodge.clearBeforeThirdContact,'Need both deterministic cover solutions');
const digest=n=>createHash('sha256').update(fs.readFileSync(new URL(n,import.meta.url))).digest('hex');
const report={input_sha256:{map:digest('./map.json'),engine:digest('../../src/engine.mjs'),contactMath:digest('../../src/interception.mjs')},date:'2026-11-04 Asia/Taipei',planningOnly:true,defaults:C.volley,routeChecks:routes,destructionExamples,isolatedExamples:cases,stationarySamples:stations.map(({launches,method,...r})=>r),stationaryWins:stations.filter(r=>r.clearBeforeThirdContact).map(({x,y,delay,eighthTargetHit,effectiveContactsBeforeEighth})=>({x,y,delay,eighthTargetHit,effectiveContactsBeforeEighth})),limitations:['No Stage4 runtime, HP/outcome system, browser input, human playtest or difficulty acceptance','Finite stationary sample, not exhaustive timing/position search','Predetermined paths; loss-of-control and unmodeled input latency require future actual-input tests','Production collision scheduler must preserve full chronological ordering including newly fired overlapping volleys']};
fs.writeFileSync(new URL('./evidence/feasibility.json',import.meta.url),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({routes:routes.length,maxCorrection:Math.max(...routes.map(r=>r.correction)),examples:Object.fromEntries(Object.entries(cases).map(([n,r])=>[n,{eighth:r.eighthTargetHit,third:r.thirdEffectiveContact,contacts:r.effectiveContactsBeforeEighth,peak:r.peakEnemyRounds}])),stationarySamples:stations.length,stationaryWins:report.stationaryWins.length},null,2));
