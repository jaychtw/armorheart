import {createState,step,hullBounds,intersect} from './engine.mjs';
import {INTERCEPTION as C} from './maps/interception.mjs';
import {createGeometry} from './ship-route.mjs';
export const SHIP_ROUTE=createGeometry(C),SHIP_DURATION=SHIP_ROUTE.routeLength/C.ship.speed;
export const SHIP_SWEEP_SLICE=1/480;
const EPS=1e-9;
export function createInterception(){const s=createState();s.scenario='interception';s.walls=[];s.movementBounds={...C.land};s.tank={x:C.tank.x,y:C.tank.y,facing:C.tank.facing};s.interception={elapsed:0,shipHP:C.ship.hp,tankHP:C.tank.hp,immuneUntil:0,damageAt:-100,shipHitAt:-100,finishedAt:null,outcome:null,nextOpportunity:C.volley.firstTickSeconds,enemyShells:[],opportunities:[],shotHits:[],tankHits:[],lastVolleyAt:-100};return s;}
export function shipStage(hp){return hp>=5?'intact':hp>=3?'smoking':hp>0?'onFire':'defeated';}
export function shipRender(s){return SHIP_ROUTE.pose(s.interception.finishedAt??s.interception.elapsed);}
export function shipStatus(s){const m=s.interception;if(m.outcome)return m.outcome;const next=m.nextOpportunity;if(next<=SHIP_DURATION&&next-m.elapsed<=C.volley.prechargeSeconds+EPS&&SHIP_ROUTE.fireWindow(SHIP_ROUTE.pose(next)))return 'charging';const p=shipRender(s);return p.leg.endsWith('Turn')?'turning':SHIP_ROUTE.fireWindow(p)?'cruising':'aligning';}
export function shipCharge(s){const m=s.interception;return shipStatus(s)==='charging'?Math.max(0,Math.min(1,1-(m.nextOpportunity-m.elapsed)/C.volley.prechargeSeconds)):0;}
// First entry to the exact convex hull in local coordinates (not its full rectangle).
export function polygonEntry(a,b){let near=0,far=1;const P=C.ship.hullPolygon;
 for(let i=0;i<P.length;i++){const p=P[i],q=P[(i+1)%P.length],ex=q[0]-p[0],ey=q[1]-p[1],g0=ex*(a[1]-p[1])-ey*(a[0]-p[0]),gd=ex*(b[1]-a[1])-ey*(b[0]-a[0]);if(Math.abs(gd)<1e-12){if(g0< -EPS)return null;}else if(gd>0)near=Math.max(near,-g0/gd);else far=Math.min(far,-g0/gd);if(near>far+EPS)return null;}
 return near>=-EPS&&near<=1+EPS?Math.max(0,Math.min(1,near)):null;
}
export function worldClip(x,y,dx,dy){if(x<0||x>768||y<0||y>768)return null;let end=1;if(x+dx<0)end=Math.min(end,-x/dx);if(x+dx>768)end=Math.min(end,(768-x)/dx);if(y+dy<0)end=Math.min(end,-y/dy);if(y+dy>768)end=Math.min(end,(768-y)/dy);return Math.max(0,end);}
// Exact route sampling in <=1/480s local chords; no endpoint-only moving-target test.
// At approved speed/radius, local chord error is <0.001 world unit per slice.
export function shipSweep(start,dt,x,y,dx,dy,slice=SHIP_SWEEP_SLICE){const clip=worldClip(x,y,dx,dy);if(clip===null)return null;const count=Math.max(1,Math.ceil(dt*clip/slice));for(let i=0;i<count;i++){const a=clip*i/count,b=clip*(i+1)/count,p0=SHIP_ROUTE.pose(start+dt*a),p1=SHIP_ROUTE.pose(start+dt*b),hit=polygonEntry(SHIP_ROUTE.local(p0,x+dx*a,y+dy*a),SHIP_ROUTE.local(p1,x+dx*b,y+dy*b));if(hit!==null)return {t:a+(b-a)*hit,entity:'battleship'};}return null;}
function circleEntry(x,y,dx,dy,cx,cy,r){const a=dx*dx+dy*dy,px=x-cx,py=y-cy,c=px*px+py*py-r*r;if(c<=EPS)return 0;if(a<EPS)return null;const b=2*(px*dx+py*dy),disc=b*b-4*a*c;if(disc< -EPS)return null;const t=(-b-Math.sqrt(Math.max(0,disc)))/(2*a);return t>=-EPS&&t<=1+EPS?Math.max(0,Math.min(1,t)):null;}
// Exact circle-radius vs swept axis-aligned accepted tank hull, with rounded corners.
export function tankShellEntry(x,y,dx,dy,b,r=C.volley.shellRadius){let best=null;const take=t=>{if(t!==null&&(best===null||t<best))best=t;};take(intersect(x,y,dx,dy,{x:b.left-r,y:b.top,width:b.right-b.left+2*r,height:b.bottom-b.top}));take(intersect(x,y,dx,dy,{x:b.left,y:b.top-r,width:b.right-b.left,height:b.bottom-b.top+2*r}));for(const cx of[b.left,b.right])for(const cy of[b.top,b.bottom])take(circleEntry(x,y,dx,dy,cx,cy,r));return best;}
// Trace real movement at156/s until the shoreline clamp, then the stationary remainder.
export function movingTankShellEntry(b,dx,dy,before,after,dt,clip=1){const h=hullBounds(0,0,after.facing),distance=Math.hypot(after.x-before.x,after.y-before.y),stop=dt>0&&distance>EPS?Math.min(1,distance/(C.tank.speed*dt)):0;const tankAt=t=>{const f=stop>EPS?Math.min(1,t/stop):0;return{x:before.x+(after.x-before.x)*f,y:before.y+(after.y-before.y)*f};};const spans=stop>EPS&&stop<clip-EPS?[[0,stop],[stop,clip]]:[[0,clip]];for(const [a,z]of spans){const p=tankAt(a),q=tankAt(z),hit=tankShellEntry(b.x+dx*a-p.x,b.y+dy*a-p.y,dx*(z-a)-(q.x-p.x),dy*(z-a)-(q.y-p.y),h);if(hit!==null)return a+(z-a)*hit;}return null;}
function finish(s,outcome,at){const m=s.interception;m.outcome=outcome;m.finishedAt=at;m.enemyShells=[];s.shells=[];s.complete=true;s.events.push({type:'interceptionComplete',outcome});}
function opportunity(s){const m=s.interception,at=m.nextOpportunity,p=SHIP_ROUTE.pose(at),fired=SHIP_ROUTE.fireWindow(p),direction=SHIP_ROUTE.starboard(p),mouths=SHIP_ROUTE.muzzles(p);m.opportunities.push({time:at,leg:p.leg,fired,direction,muzzles:mouths});m.nextOpportunity+=C.volley.periodSeconds;if(!fired)return;m.lastVolleyAt=at;m.enemyShells.push(...mouths.map((q,i)=>({...q,dx:direction.x,dy:direction.y,born:at,battery:i})));s.events.push({type:'shipVolley',time:at,muzzles:mouths,direction});}
export function stepInterception(s,input,dt){if(s.complete)return s;if(!Number.isFinite(dt)||dt<0)throw Error('Invalid M3 interval');dt=Math.min(dt,.05);let remaining=dt,first=true,allEvents=[];
 while((first||remaining>1e-12)&&!s.complete){first=false;const m=s.interception,start=m.elapsed;if(m.nextOpportunity<=start+EPS&&m.nextOpportunity<=SHIP_DURATION){s.events=[];opportunity(s);allEvents.push(...s.events);}
  const delta=Math.min(remaining,Math.max(0,m.nextOpportunity-start),Math.max(0,SHIP_DURATION-start)),events=[];
  // Apply the existing immediate turn/correction before tracing actual movement.
  if(input.direction)step(s,{direction:input.direction},0);
  const before={...s.tank};
  const combat={sweep:(x,y,dx,dy,instant)=>m.shipHP>0?shipSweep(start,instant?0:delta,x,y,dx,dy):null,impact:(hit,x,y,instant)=>events.push({kind:'ship',at:start+(instant?0:hit.t*delta),x,y})};
  step(s,input,delta,combat);m.elapsed=start+delta;
  m.enemyShells=m.enemyShells.filter(b=>{const dx=b.dx*C.volley.shellSpeed*delta,dy=b.dy*C.volley.shellSpeed*delta,clip=worldClip(b.x,b.y,dx,dy);if(clip===null)return false;const fraction=movingTankShellEntry(b,dx,dy,before,s.tank,delta,clip);if(fraction!==null){events.push({kind:'tank',at:start+delta*fraction,x:b.x+dx*fraction,y:b.y+dy*fraction});return false;}b.x+=dx;b.y+=dy;return clip>=1-EPS;});
  if(m.elapsed>=SHIP_DURATION-EPS)events.push({kind:'exit',at:SHIP_DURATION});
  const priority={ship:0,tank:1,exit:2};events.sort((a,b)=>Math.abs(a.at-b.at)<EPS?priority[a.kind]-priority[b.kind]:a.at-b.at);
  for(const e of events){if(s.complete)break;if(e.kind==='ship'&&m.shipHP>0){m.shipHP--;m.shipHitAt=e.at;s.hits++;m.shotHits.push({time:e.at,hp:m.shipHP,position:SHIP_ROUTE.pose(e.at),x:e.x,y:e.y});s.events.push({type:'impact',x:e.x,y:e.y,brick:false},{type:'shipHit',hp:m.shipHP});if(!m.shipHP)finish(s,'success',e.at);}else if(e.kind==='tank'&&e.at+EPS>=m.immuneUntil){m.tankHP--;m.damageAt=e.at;m.immuneUntil=e.at+C.tank.invulnerabilitySeconds;m.tankHits.push({time:e.at,hp:m.tankHP,x:e.x,y:e.y});s.events.push({type:'impact',x:e.x,y:e.y,brick:false},{type:'tankHit',hp:m.tankHP});if(!m.tankHP)finish(s,'defeat',e.at);}else if(e.kind==='exit')finish(s,'escaped',e.at);}
  allEvents.push(...s.events);remaining-=delta;
  if(!s.complete&&m.nextOpportunity<=m.elapsed+EPS&&m.nextOpportunity<=SHIP_DURATION){s.events=[];opportunity(s);allEvents.push(...s.events);}
  if(delta===0)break;
 }
 s.events=allEvents;return s;
}
