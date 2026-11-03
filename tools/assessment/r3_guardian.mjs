// Planning-only verification; imports the accepted engine, does not alter it.
import {createState,canMove,hullBounds,step,VECTORS} from '../../src/engine.mjs';
import fs from 'node:fs';import crypto from 'node:crypto';import assert from 'node:assert/strict';
const root=new URL('../../',import.meta.url),spec=JSON.parse(fs.readFileSync(new URL('docs/geometry/r3/map.json',root)));
const out=new URL('docs/geometry/r3/guardian-results.json',root);
const facings=Object.keys(VECTORS),report={map_sha256:crypto.createHash('sha256').update(fs.readFileSync(new URL('docs/geometry/r3/map.json',root))).digest('hex'),model:'Actual accepted M1 engine; unchanged source. Mask bit=removed brick.',engine_sha256:crypto.createHash('sha256').update(fs.readFileSync(new URL('src/engine.mjs',root))).digest('hex'),states:[],witnesses:{}};
function state(mask=0){const s=createState();Object.assign(s,{scenario:'breakthrough',bounds:spec.bounds,tank:{...spec.tankSpawn},walls:[...spec.steel,...spec.brick.filter(w=>!(mask>>w.id&1))]});return s;}
function shallow(s){return {...s,tank:{...s.tank},events:[],shells:[]};}
for(let mask=0;mask<16;mask++){
 const base=state(mask);let worst={distance:0},turns=0,positions=0;
 function inspect(x,y){for(const facing of facings){const s={...base,tank:{x,y,facing}};if(!canMove(s,x,y))continue;positions++;
  for(const direction of facings){const t=shallow(s);step(t,{direction},0);const d=Math.hypot(t.tank.x-x,t.tank.y-y);assert.equal(t.tank.facing,direction);assert.ok(canMove(t,t.tank.x,t.tank.y));assert.ok(d<=19+1e-6,JSON.stringify({mask,x,y,facing,direction,d}));if(d>worst.distance)worst={distance:d,before:s.tank,direction,after:t.tank};turns++;}}}
 // Uniform8-unit interior grid, including states unreachable by either witness.
 for(let x=216;x<=552;x+=8)for(let y=40;y<=728;y+=8)inspect(x,y);
 // Critical hull/wall/world contact coordinates in every orientation, their
 // interval midpoints and tiny offsets either side. Finite spatial checks, not
 // a claim to have enumerated every real-valued pose.
 function axis(which){const v=new Set();for(const f of facings){const b=hullBounds(0,0,f),lo=which==='x'?b.left:b.top,hi=which==='x'?b.right:b.bottom;
  v.add((which==='x'?spec.bounds.left:spec.bounds.top)-lo);v.add((which==='x'?spec.bounds.right:spec.bounds.bottom)-hi);
  for(const w of base.walls){const p=which==='x'?w.x:w.y;v.add(p-hi);v.add(p+64-lo);}}
 const a=[...v].sort((x,y)=>x-y),all=new Set();for(let i=0;i<a.length;i++){for(const d of [-1e-6,0,1e-6])all.add(a[i]+d);if(i)all.add((a[i-1]+a[i])/2);}return [...all].filter(x=>x>=0&&x<=768);}
 const xs=axis('x'),ys=axis('y');for(const x of xs)for(const y of ys)inspect(x,y);
 report.states.push({mask,positions,turns,criticalAxes:[xs.length,ys.length],worst});console.log('mask',mask,'turns',turns,'max',worst.distance);
}
function move(s,dir,axis,target){let corrections=0;for(let i=0;i<2000;i++){const sign=VECTORS[dir][axis==='x'?0:1],remaining=(target-s.tank[axis])*sign;if(remaining<=1e-7)return corrections;const before={...s.tank};step(s,{direction:dir},Math.min(.05,remaining/156));assert.ok(canMove(s,s.tank.x,s.tank.y));if(Math.hypot(s.tank.x-before.x,s.tank.y-before.y)<1e-9)throw Error('Witness blocked '+JSON.stringify({dir,target,tank:s.tank}));}throw Error('Witness exceeded bound');}
for(const [name,solution] of Object.entries(spec.solutions)){
 const s=state();const trace=[];
 for(const a of solution.guardian){
  if(a.action==='move')move(s,a.direction,a.axis,a.target);
  if(a.action==='face'){step(s,{direction:a.direction},0);assert.ok(canMove(s,s.tank.x,s.tank.y));}
  if(a.action==='fire'){
   if(a.direction)step(s,{direction:a.direction},0);
   const wanted=spec.brick.find(w=>w.label===a.remove).id,old=s.destroyed;
   for(let i=0;i<180&&s.walls.some(w=>w.id===wanted);i++)step(s,{fire:true},1/60);
   assert.equal(s.destroyed,old+1);assert.ok(!s.walls.some(w=>w.id===wanted));assert.ok(canMove(s,s.tank.x,s.tank.y));
  }
  trace.push({action:a,tank:{...s.tank},destroyed:s.destroyed,time:s.time});
 }
 const mask=spec.brick.reduce((m,w)=>m|(!s.walls.some(q=>q.id===w.id)?1<<w.id:0),0);assert.equal(mask,solution.mask);report.witnesses[name]={mask,shots:s.shots,seconds:s.time,trace};
}
// Drive the unchanged Guardian along each independently verified truck route.
// The tank starts at its own spawn and executes the actual demolition witness
// first; then rejoins the truck start through the already clear central lane.
const truckReport=JSON.parse(fs.readFileSync(new URL('docs/geometry/r3/transport-results.json',root)));
for(const [name,solution] of Object.entries(spec.solutions)){
 const s=state(solution.mask);s.tank={x:352,y:500,facing:'up'};move(s,'down','y',688);step(s,{direction:'up'},0);
 const route=truckReport.all_destruction_states[solution.mask].poses;assert.ok(route.length);let actions=0;
 for(let i=1;i<route.length;i++){
  const [x,y,h]=route[i],direction=['up','right','down','left'][h];
  if(x===s.tank.x&&y===s.tank.y){const before={...s.tank};step(s,{direction},0);assert.equal(s.tank.x,before.x);assert.equal(s.tank.y,before.y);}
  else move(s,direction,x!==s.tank.x?'x':'y',x!==s.tank.x?x:y);
  assert.ok(canMove(s,s.tank.x,s.tank.y));assert.ok(Math.hypot(s.tank.x-x,s.tank.y-y)<1e-7);actions++;
 }
 report.witnesses[name].guardianFollowsTruckRoute={passed:true,actions,end:s.tank,extraDemolition:0};
}
// Negative control: the assay must still catch the rejected R3 notch.
const oldRows=['......','......','......','SSSS..','BBBB..','......','......','..SSBB','..SSBB','....BB','......','......'];
const old=state();old.walls=[];let oldId=0;oldRows.forEach((row,r)=>[...row].forEach((c,col)=>{if(c!=='.'&&!(col===0&&r===4))old.walls.push({id:oldId++,x:192+64*col,y:64*r,width:64,height:64,kind:c==='B'?'brick':'steel'});}));
old.tank={x:224,y:304,facing:'up'};assert.ok(canMove(old,224,304));step(old,{direction:'right'},0);const badDistance=Math.hypot(old.tank.x-224,old.tank.y-304);assert.ok(badDistance>19);
report.negativeControl={expectedViolationDetected:true,oldBefore:{x:224,y:304,facing:'up'},oldAfter:old.tank,oldCorrection:badDistance};
const corrected=state();corrected.tank={x:224,y:304,facing:'up'};step(corrected,{direction:'right'},0);report.rejectedPoseOnNewMap={after:corrected.tank,correction:Math.hypot(corrected.tank.x-224,corrected.tank.y-304)};
report.totalTurns=report.states.reduce((n,s)=>n+s.turns,0);report.maximumCorrection=Math.max(...report.states.map(s=>s.worst.distance));report.passed=true;report.limitations='Exhaustive16 destruction masks; finite uniform and critical-boundary spatial tests. Not a proof over continuous positions, rendered artwork or a human playtest.';
fs.writeFileSync(out,JSON.stringify(report,null,2)+'\n');
