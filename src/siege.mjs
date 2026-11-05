import {createState,step,intersect,hullBounds} from './engine.mjs';
import {tankShellEntry,worldClip,movingTankShellEntry} from './interception.mjs';
import {SIEGE as C} from './maps/siege.mjs';
const EPS=1e-9,F=C.fortress,V=C.volley;
export function createSiege(){const s=createState();s.scenario='siege';s.walls=structuredClone(C.walls);s.solids=[{...F,id:99,kind:'fortress'}];s.tank={x:C.tank.x,y:C.tank.y,facing:C.tank.facing};s.siege={elapsed:0,fortressHP:8,tankHP:3,immuneUntil:0,damageAt:-100,fortressHitAt:-100,nextCharge:2.4,nextVolley:3,chargedGun:null,gunAngles:[Math.PI/2,Math.PI/2,Math.PI/2],enemyShells:[],lastVolley:null,volleys:[],shotHits:[],tankHits:[],coverHits:[],finishedAt:null,outcome:null,serial:0};return s;}
export function fortressStage(hp){return hp>=6?'intact':hp>=3?'broken':hp>0?'half':'defeated';}
export function fortressGun(s,i){const m=s.siege,[x,y]=F.gunPivots[i],angle=m.chargedGun===i?Math.atan2(s.tank.y-y,s.tank.x-x):m.gunAngles[i];return {i,x,y,angle,muzzle:{x:x+24*Math.cos(angle),y:y+24*Math.sin(angle)}};}
export function fortressStatus(s){return s.siege.outcome??(s.siege.chargedGun===null?'watch':'charging');}
export function fortressCharge(s){const m=s.siege;return m.chargedGun===null?0:Math.max(0,Math.min(1,1-(m.nextVolley-m.elapsed)/.6));}
function finish(s,outcome,at){const m=s.siege;m.outcome=outcome;m.finishedAt=at;m.chargedGun=null;m.enemyShells=[];s.shells=[];s.complete=true;s.events.push({type:'siegeComplete',outcome});}
function charge(s){const m=s.siege;let i=0;for(let j=1;j<3;j++)if(Math.abs(F.gunPivots[j][0]-s.tank.x)<Math.abs(F.gunPivots[i][0]-s.tank.x)-EPS)i=j;m.chargedGun=i;m.nextCharge+=3;}
function volley(s){const m=s.siege;if(m.chargedGun===null)charge(s);const g=fortressGun(s,m.chargedGun);m.gunAngles[g.i]=g.angle;const rounds=V.offsetDegrees.map(offset=>{const a=g.angle+offset*Math.PI/180;return {id:m.serial++,...g.muzzle,dx:Math.cos(a),dy:Math.sin(a),born:m.nextVolley};});m.enemyShells.push(...rounds);m.lastVolley={time:m.nextVolley,gun:g.i,muzzle:{...g.muzzle},angle:g.angle};if(m.volleys.length<128)m.volleys.push({...m.lastVolley,target:{x:s.tank.x,y:s.tank.y},directions:rounds.map(b=>[b.dx,b.dy])});m.nextVolley+=3;m.chargedGun=null;s.events.push({type:'fortressVolley',...m.lastVolley});}
// Resolve both sides together. Every exact-time batch sees one pre-impact cover snapshot.
// Caller retains accepted engine firing/cooldown/muzzle semantics; only this adapter delegates rays.
function resolve(s,before,after,dt,start,pending){const m=s.siege;let clock=0,alive=[...s.shells.map(b=>({...b,enemy:false})),...m.enemyShells.map(b=>({...b,enemy:true})),...pending.map(b=>({...b,id:m.serial++,enemy:false,instant:true}))];
 const distance=Math.hypot(after.x-before.x,after.y-before.y),stop=dt>0&&distance>EPS?Math.min(1,distance/(156*dt)):0;
 const position=at=>{const f=stop>EPS?Math.min(1,at/(dt*stop)):0;return{x:before.x+(after.x-before.x)*f,y:before.y+(after.y-before.y)*f,facing:after.facing};};
 const candidate=b=>{const remaining=Math.max(0,dt-clock),speed=b.enemy?180:480,dx=b.dx*(b.instant?68:speed*remaining),dy=b.dy*(b.instant?68:speed*remaining);let best=null;const rank={wall:0,boss:1,tank:2,exit:3,unfold:4};
  const take=(f,kind,item=null)=>{if(f===null)return;const at=b.instant?0:f*remaining;if(!best||at<best.at-EPS||(Math.abs(at-best.at)<EPS&&(rank[kind]<rank[best.kind]||(rank[kind]===rank[best.kind]&&(item?.id??0)<(best.item?.id??0)))))best={at,kind,item,b,point:{x:b.x+dx*f,y:b.y+dy*f}};};
  const clip=b.instant?1:worldClip(b.x,b.y,dx,dy);if(clip===null)return{at:0,kind:'exit',b};
  for(const w of s.walls){const f=b.enemy?tankShellEntry(b.x,b.y,dx,dy,{left:w.x,top:w.y,right:w.x+w.width,bottom:w.y+w.height},4):intersect(b.x,b.y,dx,dy,w);if(f!==null&&f<=clip+EPS)take(f,'wall',w);}
  if(!b.enemy&&m.fortressHP>0){const f=intersect(b.x,b.y,dx,dy,F);if(f!==null&&f<=clip+EPS)take(f,'boss');}
  if(b.enemy){const f=movingTankShellEntry(b,dx,dy,position(clock),after,remaining,clip);if(f!==null)take(f,'tank');}
  if(b.instant)take(1,'unfold');else if(clip<1-EPS||b.x<0||b.x>768||b.y<0||b.y>768)take(clip,'exit');
  return best;
 };
 for(let n=0;n<256&&!s.complete;n++){
  const candidates=alive.map(candidate).filter(Boolean);if(!candidates.length){for(const b of alive){const v=b.enemy?180:480;b.x+=b.dx*v*(dt-clock);b.y+=b.dy*v*(dt-clock);}clock=dt;break;}
  const next=Math.min(...candidates.map(e=>e.at));if(next>dt-clock+EPS)throw Error('Siege event outside interval');
  for(const b of alive)if(!b.instant){const v=b.enemy?180:480;b.x+=b.dx*v*next;b.y+=b.dy*v*next;}clock+=next;
  const batch=candidates.filter(e=>Math.abs(e.at-next)<EPS),removed=new Set(),consumed=new Set();
  for(const e of batch){if(e.kind==='unfold'){e.b.x+=e.b.dx*68;e.b.y+=e.b.dy*68;delete e.b.instant;delete e.b.muzzle;continue;}consumed.add(e.b);if(e.kind==='wall'){const w=e.item;const brick=w.kind==='brick';s.hits++;s.events.push({type:'impact',x:e.point.x,y:e.point.y,brick});if(brick)removed.add(w.id);if(brick&&!m.coverHits.some(h=>h.id===w.id))m.coverHits.push({time:start+clock,id:w.id,side:e.b.enemy?'enemy':'player'});}}
  if(removed.size){s.walls=s.walls.filter(w=>!removed.has(w.id));s.destroyed+=removed.size;}
  // Exact simultaneous final boss/tank hits are player-safe; earlier lethal contact wins.
  for(const e of batch.filter(e=>e.kind==='boss')){if(s.complete)break;m.fortressHP--;m.fortressHitAt=start+clock;s.hits++;m.shotHits.push({time:start+clock,hp:m.fortressHP});s.events.push({type:'impact',x:e.point.x,y:e.point.y,brick:false},{type:'fortressHit',hp:m.fortressHP});if(m.fortressHP===0)finish(s,'success',start+clock);}
  for(const e of batch.filter(e=>e.kind==='tank')){if(s.complete)break;if(start+clock+EPS>=m.immuneUntil){m.tankHP--;m.damageAt=start+clock;m.immuneUntil=start+clock+3;m.tankHits.push({time:start+clock,hp:m.tankHP});s.events.push({type:'impact',x:e.point.x,y:e.point.y,brick:false},{type:'tankHit',hp:m.tankHP});if(!m.tankHP)finish(s,'defeat',start+clock);}}
  alive=alive.filter(b=>!consumed.has(b));if(clock>=dt-EPS&&!alive.some(b=>b.instant))break;
  if(n===255)throw Error('Siege event iteration bound');
 }
 if(!s.complete){s.shells=alive.filter(b=>!b.enemy).map(({enemy,instant,muzzle,...b})=>b);m.enemyShells=alive.filter(b=>b.enemy).map(({enemy,...b})=>b);}
}
export function stepSiege(s,input,dt){if(s.complete)return s;if(!Number.isFinite(dt)||dt<0)throw Error('Invalid Siege interval');dt=Math.min(.05,dt);let remaining=dt,first=true,all=[];
 while((first||remaining>1e-12)&&!s.complete){first=false;const m=s.siege,start=m.elapsed;s.events=[];if(m.nextCharge<=start+EPS)charge(s);if(m.nextVolley<=start+EPS)volley(s);all.push(...s.events);
  const delta=Math.min(remaining,Math.max(0,m.nextCharge-start),Math.max(0,m.nextVolley-start)),pending=[],delegate={projectiles:b=>pending.push(b)};
  if(input.direction)step(s,{direction:input.direction},0,delegate);const before={...s.tank};step(s,input,delta,delegate);resolve(s,before,{...s.tank},delta,start,pending);m.elapsed=start+delta;all.push(...s.events);remaining-=delta;
  s.events=[];if(!s.complete&&m.nextCharge<=m.elapsed+EPS)charge(s);if(!s.complete&&m.nextVolley<=m.elapsed+EPS)volley(s);all.push(...s.events);
  if(delta===0)break;
 }
 s.events=all;return s;
}
