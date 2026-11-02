import {createState} from './engine.mjs';
import {BREAKTHROUGH,missionWalls} from './maps/breakthrough.mjs';
import {buildNavigation,planRoute,groupInsideExit} from './navigation.mjs';
export function createMission(){
  const s=createState();s.scenario='breakthrough';s.bounds={...BREAKTHROUGH.bounds};s.tank={...BREAKTHROUGH.tank};s.walls=missionWalls();
  s.mission={elapsed:0,phase:'waiting',revision:0,replans:1,nav:buildNavigation(s.walls),
    crowd:{...BREAKTHROUGH.crowd,path:[],edgeFrom:{...BREAKTHROUGH.crowd}},evacuatingAt:null};return s;
}
export function refreshRoute(s){
  const m=s.mission;if(s.complete||m.revision===s.destroyed)return false;
  m.revision=s.destroyed;m.replans++;m.nav=buildNavigation(s.walls);
  const c=m.crowd,continuation=c.path[0];
  const route=planRoute(m.nav,c,continuation?[continuation,c.edgeFrom]:[]);
  if(route.length){
    if(continuation&&route[0].x===c.edgeFrom.x&&route[0].y===c.edgeFrom.y)c.edgeFrom={...continuation};
    c.path=route;
    if(m.phase==='waiting'){m.phase='evacuating';m.evacuatingAt=m.elapsed;return true;}
  }else c.path=[];
  return false;
}
// Entry fraction of a cardinal segment into the exit shrunk by group radius.
function exitEntry(a,b){
  const r=BREAKTHROUGH.radius,e=BREAKTHROUGH.exit;let near=0,far=1;
  for(const [p,d,lo,hi] of [[a.x,b.x-a.x,e.left+r,e.right-r],[a.y,b.y-a.y,e.top+r,e.bottom-r]]){
    if(Math.abs(d)<1e-10){if(p<lo||p>hi)return null;}
    else{let u=(lo-p)/d,v=(hi-p)/d;if(u>v)[u,v]=[v,u];near=Math.max(near,u);far=Math.min(far,v);if(near>far)return null;}
  }
  return near>=0&&near<=1?near:null;
}
export function advanceMission(s,dt){
  const m=s.mission;if(s.complete)return;
  if(!Number.isFinite(dt)||dt<0)throw new Error('Invalid mission time interval');
  const window=Math.min(dt,Math.max(0,BREAKTHROUGH.deadline-m.elapsed));
  const c=m.crowd;let available=window,used=0;
  while(c.path.length&&available>0){
    const to=c.path[0],distance=Math.hypot(to.x-c.x,to.y-c.y),duration=distance/BREAKTHROUGH.speed;
    const entry=exitEntry(c,to),arrival=entry===null?Infinity:duration*entry;
    if(arrival<=available&&m.elapsed+used+arrival<BREAKTHROUGH.deadline){
      const ratio=duration?arrival/duration:0;c.x+=(to.x-c.x)*ratio;c.y+=(to.y-c.y)*ratio;
      m.elapsed+=used+arrival;m.phase='success';s.complete=true;return;
    }
    const travel=Math.min(available,duration),ratio=duration?travel/duration:1;
    c.x+=(to.x-c.x)*ratio;c.y+=(to.y-c.y)*ratio;available-=travel;used+=travel;
    if(travel===duration){c.x=to.x;c.y=to.y;c.edgeFrom={...to};c.path.shift();}
    else break;
  }
  m.elapsed+=window;
  // Includes exactly-at-deadline arrivals; no rounding the displayed clock.
  if(m.elapsed>=BREAKTHROUGH.deadline){m.elapsed=BREAKTHROUGH.deadline;m.phase='timeout';s.complete=true;}
}
export function missionSnapshot(s){const {nav,...m}=s.mission;return structuredClone(m);}
