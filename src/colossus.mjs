import {createState,step,hullBounds,intersect} from './engine.mjs';
import {COLOSSUS as C} from './maps/colossus.mjs';
import {COLOSSUS_ART as ART} from './colossus-art.mjs';
const EPS=1e-9;
export function createColossus(){const s=createState();s.scenario='colossus';s.bounds={...C.bounds};s.walls=[];s.tank={...C.tank};s.colossus={elapsed:0,phase:'grounded',phaseTime:0,stop:0,arrivalView:'east',landings:0,bossHP:C.bossHP,tankHP:C.tankHP,immuneUntil:0,damageAt:-100,bossHitAt:-100,outcome:null,finishedAt:null,history:[],shotHits:[],tankHits:[]};return s;}
export function bossStage(hp){return hp===4?'intact':hp>=2?'fatigued':hp===1?'wounded':'defeated';}
function routeView(stop){const a=C.stops[stop],b=C.stops[(stop+1)%5];return b.y<a.y?'north':b.x>a.x?'east':b.x<a.x?'west':'south';}
export function bossView(s){const m=s.colossus;return m.phase==='grounded'&&m.phaseTime<.4?m.arrivalView:routeView(m.stop);}
export function bossPose(s){const m=s.colossus;if(m.bossHP===0)return 'wounded';if(m.phase==='airborne')return 'airborne';if(m.elapsed-m.bossHitAt<.14-EPS)return 'hit';if(m.phaseTime<.18&&m.landings>0)return 'landing';if(m.bossHP===1)return 'wounded';if(m.bossHP<4)return 'fatigued';return m.phaseTime>=.55&&m.phaseTime<1.15?'look':'idle';}
export function bossPosition(s){const m=s.colossus,a=C.stops[m.stop],b=C.stops[(m.stop+1)%5],p=m.phase==='airborne'?m.phaseTime/C.jumpSeconds:0;return {x:a.x+(b.x-a.x)*p,y:a.y+(b.y-a.y)*p,z:m.phase==='airborne'?C.height*Math.sin(Math.PI*p):0};}
export function bossRender(s){return {...bossPosition(s),view:bossView(s),pose:bossPose(s),next:{...C.stops[(s.colossus.stop+1)%5]}};}
export function bossTarget(s,x,y,dx,dy){if(s.colossus.phase!=='grounded'||s.colossus.bossHP<=0)return null;const p=bossPosition(s),art=ART.images[bossView(s)+'_'+bossPose(s)];let nearest=null;
 for(const [l,t,w,h] of art.rects){const time=intersect(x,y,dx,dy,{x:p.x+l,y:p.y+t,width:w,height:h});if(time!==null&&(nearest===null||time<nearest))nearest=time;}
 return nearest===null?null:{t:nearest,entity:'colossus'};
}
export function contactInterval(a,b,p){
 const h=hullBounds(0,0,b.facing),rx=C.contact[0],ry=C.contact[1];
 const distance=t=>{const x=a.x+(b.x-a.x)*t,y=a.y+(b.y-a.y)*t;return (Math.max(x+h.left-p.x,0,p.x-x-h.right)/rx)**2+(Math.max(y+h.top-p.y,0,p.y-y-h.bottom)/ry)**2;};
 if(Math.max(a.x,b.x)+h.right<p.x-rx||Math.min(a.x,b.x)+h.left>p.x+rx||Math.max(a.y,b.y)+h.bottom<p.y-ry||Math.min(a.y,b.y)+h.top>p.y+ry)return null;
 let l=0,r=1;for(let i=0;i<45;i++){const x=l+(r-l)/3,y=r-(r-l)/3;if(distance(x)<distance(y))r=y;else l=x;}const center=(l+r)/2;
 if(distance(center)>1+EPS&&distance(0)>1+EPS&&distance(1)>1+EPS)return null;
 let lo=0,hi=center;if(distance(0)<=1+EPS)hi=0;else for(let i=0;i<40;i++){const t=(lo+hi)/2;if(distance(t)<=1+EPS)hi=t;else lo=t;}const enter=hi;
 lo=center;hi=1;if(distance(1)<=1+EPS)lo=1;else for(let i=0;i<40;i++){const t=(lo+hi)/2;if(distance(t)<=1+EPS)lo=t;else hi=t;}return [enter,lo];
}
function finish(s,outcome,at){const m=s.colossus;m.outcome=outcome;m.finishedAt=at;s.complete=true;s.events.push({type:'colossusComplete',outcome});}
function transition(s){const m=s.colossus;m.phaseTime=0;if(m.phase==='grounded'){m.phase='airborne';m.history.push({event:'takeoff',time:m.elapsed,stop:C.stops[m.stop].id});}else{m.arrivalView=routeView(m.stop);m.stop=(m.stop+1)%5;m.phase='grounded';m.landings++;m.history.push({event:'landing',time:m.elapsed,stop:C.stops[m.stop].id});s.events.push({type:'bossLanding',stop:C.stops[m.stop].id});}if(m.history.length>128)m.history.splice(0,m.history.length-128);}
export function stepColossus(s,input,dt){if(s.complete)return s;if(!Number.isFinite(dt)||dt<0)throw Error('Invalid M2 interval');dt=Math.min(dt,.05);let remaining=dt,allEvents=[],first=true;
 while((remaining>1e-12||first)&&!s.complete){first=false;const m=s.colossus,period=m.phase==='grounded'?C.groundSeconds:C.jumpSeconds;
  if(period-m.phaseTime<EPS){s.events=[];transition(s);allEvents.push(...s.events);continue;}
  const delta=Math.min(remaining,period-m.phaseTime),start=m.elapsed,phase=m.phase,boundary=Math.abs(delta-(period-m.phaseTime))<EPS,events=[],before={...s.tank},position=bossPosition(s);
  const combat={sweep:(x,y,dx,dy,instant)=>{const hit=bossTarget(s,x,y,dx,dy);return hit&&!(!instant&&phase==='grounded'&&boundary&&hit.t>=1-EPS)?hit:null;},impact:(hit,x,y,instant)=>events.push({kind:'boss',at:start+(instant?0:hit.t*delta),x,y})};
  step(s,input,delta,combat);m.elapsed=start+delta;m.phaseTime+=delta;
  if(phase==='grounded'){
   const interval=contactInterval(before,s.tank,position);
   if(interval){const eligible=Math.max(start+interval[0]*delta,m.immuneUntil);if(eligible<=start+interval[1]*delta+EPS&&eligible<m.elapsed+(boundary?-EPS:EPS))events.push({kind:'tank',at:eligible});}
  }
  events.sort((a,b)=>Math.abs(a.at-b.at)<EPS?((a.kind==='boss'?0:1)-(b.kind==='boss'?0:1)):a.at-b.at);
  for(const event of events){if(s.complete)break;
   if(event.kind==='boss'&&m.bossHP>0){m.bossHP--;m.bossHitAt=event.at;s.hits++;s.events.push({type:'impact',x:event.x,y:event.y,brick:false});m.shotHits.push({time:event.at,hp:m.bossHP,stop:C.stops[m.stop].id,view:bossView(s)});s.events.push({type:'bossHit',hp:m.bossHP});if(!m.bossHP)finish(s,'success',event.at);}
   else if(event.kind==='tank'&&event.at+EPS>=m.immuneUntil){m.tankHP--;m.damageAt=event.at;m.immuneUntil=event.at+C.immunity;m.tankHits.push({time:event.at,hp:m.tankHP,stop:C.stops[m.stop].id});s.events.push({type:'tankHit',hp:m.tankHP});if(!m.tankHP)finish(s,'defeat',event.at);}
  }
  allEvents.push(...s.events);remaining-=delta;
  if(!s.complete&&boundary){s.events=[];transition(s);allEvents.push(...s.events);}
 }
 s.events=allEvents;return s;
}
export const COLOSSUS_SPRITES={keys:Object.keys(ART.images),size:ART.frame*ART.worldPerPixel,anchor:ART.anchor.map(x=>x*ART.worldPerPixel)};
