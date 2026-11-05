// Isolated Offer calculations only. Not imported by src/, preview or game UI.
import fs from 'node:fs';
import {createGeometry} from './geometry.mjs';
import {createState,step,hullBounds,intersect,VECTORS} from '../../src/engine.mjs';
export const C=JSON.parse(fs.readFileSync(new URL('./map.json',import.meta.url)));
export const {lengths,routeLength,poseAtDistance,pose,world,local,hull,muzzles,starboard,fireWindow}=createGeometry(C);
function inPoly(x,y){let sign=0;const v=C.ship.hullPolygon;for(let i=0;i<v.length;i++){const a=v[i],b=v[(i+1)%v.length],c=(b[0]-a[0])*(y-a[1])-(b[1]-a[1])*(x-a[0]);if(Math.abs(c)<1e-8)continue;const ss=Math.sign(c);if(sign&&sign!==ss)return false;sign=ss;}return true;}
export function hitHull(p0,p1,x,y,nx,ny){
 // Player shell collision is restricted to visible world space, including clipped turns.
 if(x<0||x>768||y<0||y>768)return null;
 let clip=1;const dxWorld=nx-x,dyWorld=ny-y;
 if(nx<0)clip=Math.min(clip,-x/dxWorld);if(nx>768)clip=Math.min(clip,(768-x)/dxWorld);
 if(ny<0)clip=Math.min(clip,-y/dyWorld);if(ny>768)clip=Math.min(clip,(768-y)/dyWorld);
 nx=x+dxWorld*clip;ny=y+dyWorld*clip;
 p1={...p1,x:p0.x+(p1.x-p0.x)*clip,y:p0.y+(p1.y-p0.y)*clip,heading:p0.heading+(p1.heading-p0.heading)*clip};
 const a=local(p0,x,y),b=local(p1,nx,ny);if(inPoly(...a))return 0;
 if(Math.min(a[0],b[0])>160||Math.max(a[0],b[0])< -160||Math.min(a[1],b[1])>44||Math.max(a[1],b[1])< -44)return null;
 const dx=b[0]-a[0],dy=b[1]-a[1],v=C.ship.hullPolygon;let best=null;
 for(let i=0;i<v.length;i++){const c=v[i],d=v[(i+1)%v.length],ex=d[0]-c[0],ey=d[1]-c[1],den=dx*ey-dy*ex;if(Math.abs(den)<1e-10)continue;const cx=c[0]-a[0],cy=c[1]-a[1],t=(cx*ey-cy*ex)/den,u=(cx*dy-cy*dx)/den;if(t>=0&&t<=1&&u>=0&&u<=1&&(best===null||t<best))best=t;}return best===null?null:best*clip;
}
export function simulate(policy,{speed=C.ship.speed,dt=1/240,station=null,enemy=true}={}){
 const s=createState();s.walls=[];s.bounds={...C.land};s.scenario='m3-offer-model';s.tank={...C.tank};delete s.tank.hp;delete s.tank.speed;delete s.tank.invulnerabilitySeconds;if(station)s.tank={...station};
 let hp=6,tankHP=3,immune=-1,nextShot=0,nextVolley=3,player=[],hostile=[],history=[],volleys=[],shots=0,turnCorrection=0;const duration=routeLength/speed;
 for(let t=0;t<duration-1e-9;t+=dt){
  const h=Math.min(dt,duration-t),p0=pose(t,speed),p1=pose(t+h,speed),input=policy(t,s.tank),before={...s.tank};
  if(input.face){step(s,{direction:input.face},0);turnCorrection=Math.max(turnCorrection,Math.hypot(s.tank.x-before.x,s.tank.y-before.y));}
  step(s,{direction:input.direction},h);
  if(input.fire&&t>=nextShot-1e-8){const [dx,dy]=VECTORS[s.tank.facing];nextShot=t+1;shots++;const x=s.tank.x,y=s.tank.y,mx=x+dx*68,my=y+dy*68;const hit=hitHull(p0,p0,x,y,mx,my);if(hit!==null){hp--;history.push({type:'shipHit',time:t,hp});}else player.push({x:mx,y:my,dx,dy});}
  if(t+h>=nextVolley-1e-9){const tick=nextVolley,pp=pose(tick,speed),open=fireWindow(pp);volleys.push({time:tick,leg:pp.leg,fired:open});nextVolley+=3;if(open&&enemy){const sb=starboard(pp);for(const m of muzzles(pp))hostile.push({...m,dx:sb.x,dy:sb.y,born:tick});}}
  let hits=[];
  player=player.filter(b=>{const nx=b.x+b.dx*480*h,ny=b.y+b.dy*480*h,at=hitHull(p0,p1,b.x,b.y,nx,ny);if(at!==null){hits.push(t+h*at);return false;}b.x=nx;b.y=ny;return nx>=0&&nx<=768&&ny>=0&&ny<=768;});
  for(const at of hits){if(hp>0){hp--;history.push({type:'shipHit',time:at,hp});}}
  const b0=hullBounds(before.x,before.y,before.facing),b1=hullBounds(s.tank.x,s.tank.y,s.tank.facing),r=C.volley.shellRadius;
  hostile=hostile.filter(b=>{const move=Math.max(0,t+h-Math.max(t,b.born)),nx=b.x+b.dx*180*move,ny=b.y+b.dy*180*move;const rx=b.x-before.x,ry=b.y-before.y,rdx=nx-b.x-(s.tank.x-before.x),rdy=ny-b.y-(s.tank.y-before.y);const at=intersect(rx,ry,rdx,rdy,{x:Math.min(b0.left-before.x,b1.left-s.tank.x)-r,y:Math.min(b0.top-before.y,b1.top-s.tank.y)-r,width:Math.max(b0.right-before.x,b1.right-s.tank.x)-Math.min(b0.left-before.x,b1.left-s.tank.x)+2*r,height:Math.max(b0.bottom-before.y,b1.bottom-s.tank.y)-Math.min(b0.top-before.y,b1.top-s.tank.y)+2*r});if(at!==null){const when=t+h*at;if(when>=immune-1e-8&&hp>0){tankHP--;immune=when+3;history.push({type:'tankHit',time:when,hp:tankHP});}return false;}b.x=nx;b.y=ny;return nx>=0&&nx<=768&&ny>=0&&ny<=768;});
  if(hp<=0||tankHP<=0)return{outcome:hp<=0?'win':'tankDefeat',time:t+h,bossHP:hp,tankHP,shots,history,volleys,turnCorrection,tank:s.tank};
 }
 return{outcome:'shipEscaped',time:duration,bossHP:hp,tankHP,shots,history,volleys,turnCorrection,tank:s.tank};
}
export const stationary=()=>()=>({fire:true});
export function interceptLeft(t,tank){
 if(tank.x>280.1)return{direction:'left'};
 if(tank.y>352.1)return{direction:'up'};
 return{face:'left',fire:true};
}
