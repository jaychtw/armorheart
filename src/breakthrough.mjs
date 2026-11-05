import {createState} from './engine.mjs';
import {BREAKTHROUGH,missionWalls} from './maps/breakthrough.mjs';
import {planTransport,transportInsideExit} from './transport.mjs';
function replan(s){
 const m=s.mission,t=m.truck,result=planTransport(s.walls,{x:t.x,y:t.y,heading:t.heading});m.replans++;m.pendingReplan=false;
 m.plan=result.actions;m.predictedRouteSeconds=result.seconds;m.routeDistance=result.distance;m.routeTurns=result.turns;
 if(result.reachable&&m.phase==='waiting'){m.phase='evacuating';m.evacuatingAt=m.elapsed;return true;}return false;
}
export function createMission(){
 const s=createState();s.scenario='breakthrough';s.bounds={...BREAKTHROUGH.bounds};s.tank={...BREAKTHROUGH.tank};s.walls=missionWalls();
 s.mission={elapsed:0,phase:'waiting',revision:0,replans:0,pendingReplan:false,plan:[],evacuatingAt:null,
  truck:{...BREAKTHROUGH.truck,action:null},predictedRouteSeconds:null,routeDistance:0,routeTurns:0};replan(s);return s;
}
export function refreshRoute(s){
 const m=s.mission;if(s.complete||m.revision===s.destroyed)return false;
 m.revision=s.destroyed;
 if(m.truck.action){m.pendingReplan=true;return false;}return replan(s);
}
function finish(s,phase,elapsed){s.mission.elapsed=elapsed;s.mission.phase=phase;s.complete=true;}
// First full-body northward entry, not cab/center-only contact.
function exitFraction(a,b){
 if(a.heading!==0)return null;
 const e=BREAKTHROUGH.exit;let near=0,far=1;
 for(const [p,d,lo,hi] of [[a.x,b.x-a.x,e.left+28,e.right-28],[a.y,b.y-a.y,e.top+64,e.bottom-64]]){
  if(Math.abs(d)<1e-10){if(p<lo||p>hi)return null;}
  else{let u=(lo-p)/d,v=(hi-p)/d;if(u>v)[u,v]=[v,u];near=Math.max(near,u);far=Math.min(far,v);if(near>far)return null;}
 }
 return near>=0&&near<=1?near:null;
}
export function advanceMission(s,dt){
 if(s.complete)return;if(!Number.isFinite(dt)||dt<0)throw new Error('Invalid mission time interval');
 const m=s.mission,t=m.truck,deadline=BREAKTHROUGH.deadline,start=m.elapsed,window=Math.min(dt,Math.max(0,deadline-start));let available=window,used=0;
 if(transportInsideExit(t)&&start<deadline){finish(s,'success',start);return;}
 while(available>1e-12){
  if(!t.action){if(m.pendingReplan)replan(s);const action=m.plan.shift();if(!action)break;t.action={...action,progress:0};}
  const a=t.action,remaining=a.duration-a.progress,portion=Math.min(available,remaining),nextProgress=a.progress+portion;
  const ratio=Math.min(1,nextProgress/a.duration),next=a.kind==='forward'?{x:a.from.x+(a.to.x-a.from.x)*ratio,y:a.from.y+(a.to.y-a.from.y)*ratio,heading:t.heading}:{x:t.x,y:t.y,heading:t.heading};
  if(a.kind==='forward'){
   const entry=exitFraction(t,next),arrival=entry===null?Infinity:portion*entry;
   if(arrival<=portion&&start+used+arrival<deadline){
    const f=portion?arrival/portion:0;t.x+=(next.x-t.x)*f;t.y+=(next.y-t.y)*f;a.progress+=arrival;finish(s,'success',start+used+arrival);return;
   }
  }
  t.x=next.x;t.y=next.y;a.progress=nextProgress;used+=portion;available-=portion;
  if(a.progress>=a.duration-1e-12){
   t.x=a.to.x;t.y=a.to.y;t.heading=a.to.heading;t.action=null;
   if(transportInsideExit(t)&&start+used<deadline){finish(s,'success',start+used);return;}
  }
 }
 m.elapsed=start+window;if(m.elapsed>=deadline)finish(s,'timeout',deadline);
}
export function truckRenderHeading(t){return t.action&&t.action.kind!=='forward'?t.action.from.heading+(t.action.kind==='left'?-1:1)*(t.action.progress/t.action.duration):t.heading;}
export function missionSnapshot(s){return structuredClone(s.mission);}
