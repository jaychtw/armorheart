// Bounded conservative threat sampling, not a player test or universal fairness proof.
import fs from 'node:fs';import {C,pose,muzzles,starboard} from './model.mjs';
import {createState,step,hullBounds,intersect} from '../../src/engine.mjs';
const volleyTimes=JSON.parse(fs.readFileSync(new URL('./evidence/combat-assessment.json',import.meta.url))).exactVolleys.filter(v=>v.fired).map(v=>v.time);
const samples=[];
for(const x of[272,304,352,384,416,464,496])for(const y of[288,352,432,512,592,688,720])for(const facing of['up','right','down','left'])samples.push({x,y,facing});
for(const facing of['up','right','down','left']){const h=hullBounds(0,0,facing);for(const x of[C.land.left-h.left,C.land.right-h.right])for(const y of[C.land.top-h.top,C.land.bottom-h.bottom])samples.push({x,y,facing});}
function trial(at,initial,direction,duration=Infinity,face=null){const dt=1/240,s=createState();s.scenario='m3-escape-assessment';s.walls=[];s.bounds={...C.land};s.tank={...initial};let bullets=null;
 for(let t=at-.6;t<at+7;t+=dt){const before={...s.tank};if(t>=at-.6+duration&&face)step(s,{direction:face},0);step(s,{direction:t<at-.6+duration?direction:undefined},dt);if(t+dt<at)continue;
  if(!bullets){const p=pose(at),sb=starboard(p);bullets=muzzles(p).map(m=>({...m,dx:sb.x,dy:sb.y}));}
  const b0=hullBounds(before.x,before.y,before.facing),b1=hullBounds(s.tank.x,s.tank.y,s.tank.facing),left=Math.min(b0.left-before.x,b1.left-s.tank.x)-4,top=Math.min(b0.top-before.y,b1.top-s.tank.y)-4,right=Math.max(b0.right-before.x,b1.right-s.tank.x)+4,bottom=Math.max(b0.bottom-before.y,b1.bottom-s.tank.y)+4;
  for(const b of bullets){const h=Math.min(dt,Math.max(0,t+dt-at)),nx=b.x+b.dx*180*h,ny=b.y+b.dy*180*h;const hit=intersect(b.x-before.x,b.y-before.y,nx-b.x-(s.tank.x-before.x),ny-b.y-(s.tank.y-before.y),{x:left,y:top,width:right-left,height:bottom-top});if(hit!==null)return false;b.x=nx;b.y=ny;}
 }
 return true;
}
let scenarios=0,stationaryThreats=0,noConstantEscape=[],noEscape=[];
for(const at of volleyTimes)for(const tank of samples){scenarios++;if(trial(at,tank,undefined))continue;stationaryThreats++;if(['up','right','down','left'].some(d=>trial(at,tank,d)))continue;noConstantEscape.push({time:at,tank});let escaped=false;outer:for(const direction of ['up','right','down','left'])for(const duration of [.1,.2,.3,.4,.5,.6,.8,1,1.2,1.5,2])for(const face of ['up','right','down','left'])if(trial(at,tank,direction,duration,face)){escaped=true;break outer;}if(!escaped)noEscape.push({time:at,tank});}
const report={status:'isolated model, conservative swept axis-aligned hull envelope plus4-unit radius; no actual-input or human timing validation',prechargeSeconds:.6,volleyTimes,startingSamples:samples.length,scenarios,stationaryThreats,noConstantEscapeSamples:noConstantEscape,noEscapeSamples:noEscape,meaning:'Bounded search tries constant cardinal evasion, then move-stop-face responses. A nonempty noEscapeSamples list is an unresolved model warning, not proof of unavoidable damage. Empty list supports only sampled starts/one volley/0.6s warning and evaluated responses, not overlapping volleys, late reactions or all continuous positions'};
fs.writeFileSync(new URL('./evidence/volley-escape.json',import.meta.url),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
