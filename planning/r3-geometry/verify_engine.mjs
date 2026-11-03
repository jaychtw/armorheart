// Assessment only: exercise the frozen Guardian engine against proposed data.
// Never imported by the game or its preview builder.
import fs from 'node:fs';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {createState,canMove,step,hullBounds} from '../../src/engine.mjs';
assert.equal(fs.readFileSync(new URL('../../src/engine.mjs',import.meta.url),'utf8'),execFileSync('git',['show','bfd228359fbf56f03f921cb3d3439c7c26ed5c79:src/engine.mjs'],{cwd:new URL('../../',import.meta.url),encoding:'utf8'}));
const map=JSON.parse(fs.readFileSync(new URL('./map.json',import.meta.url)));
const walls=map.walls.map(w=>({...w,width:64,height:64})),bricks=walls.filter(w=>w.kind==='brick');
function state(mask=0){const removed=new Set(bricks.filter((w,i)=>mask>>i&1).map(w=>w.id));return {...createState(),scenario:'breakthrough',bounds:map.bounds,walls:walls.filter(w=>!removed.has(w.id)),tank:{...map.tank}};}
const facings=['up','right','down','left'];let checked=0,worst={distance:0};
for(let mask=0;mask<16;mask++){
 const base=state(mask);
 for(let x=224;x<=544;x+=8)for(let y=48;y<=720;y+=8)for(const facing of facings){
  const s={...base,tank:{x,y,facing}};if(!canMove(s,x,y))continue;
  for(const direction of facings){
   const t=structuredClone(s);step(t,{direction},0);const distance=Math.hypot(t.tank.x-x,t.tank.y-y);checked++;
   assert.equal(t.tank.facing,direction);assert.ok(canMove(t,t.tank.x,t.tank.y));assert.ok(distance<=19+1e-7);
   if(distance>worst.distance)worst={distance,mask,before:s.tank,requested:direction,after:t.tank};
  }
 }
}
function solution(shortcut){
 const s=state();let updates=0,maxCorrection=0;const damage=[],trace=[structuredClone(s.tank)];
 function face(direction){const before={...s.tank};step(s,{direction},0);maxCorrection=Math.max(maxCorrection,Math.hypot(s.tank.x-before.x,s.tank.y-before.y));assert.ok(canMove(s,s.tank.x,s.tank.y));trace.push({...s.tank});}
 function drive(direction,target){
  face(direction);const axis=['left','right'].includes(direction)?'x':'y',sign=['up','left'].includes(direction)?-1:1;
  for(let i=0;Math.abs(s.tank[axis]-target)>1e-6;i++){
   assert.ok(i<10000,'route must not stick');const distance=(target-s.tank[axis])*sign;assert.ok(distance>0);
   step(s,{direction},Math.min(.05,distance/156));updates++;assert.ok(canMove(s,s.tank.x,s.tank.y));
  }
  trace.push({...s.tank});
 }
 function fire(id){
  const before=s.walls.map(w=>w.id);for(let i=0;s.walls.some(w=>w.id===id);i++){assert.ok(i<180,'shot reaches its selected cell');step(s,{fire:true},1/60);updates++;assert.ok(canMove(s,s.tank.x,s.tank.y));}
  const removed=before.filter(n=>!s.walls.some(w=>w.id===n));assert.deepEqual(removed,[id]);damage.push({removed:id,remaining:s.walls.map(w=>w.id)});
 }
 if(shortcut){drive('left',320);face('up');fire('L1');fire('L0');drive('up',400);}
 else drive('up',400);
 drive('left',288);drive('up',160);face('right');fire('U0');fire('U1');
 assert.equal(s.walls.filter(w=>w.kind==='steel').length,5);
 return {updates,maxCorrection,trace,damage,shots:s.shots,removed:damage.map(d=>d.removed),stateDestroyed:s.destroyed};
}
const negative=state();for(let i=0;i<600;i++)step(negative,{fire:true},1/60);assert.equal(negative.destroyed,0);
const regression=state();regression.tank={x:224,y:304,facing:'up'};assert.ok(canMove(regression,224,304));step(regression,{direction:'right'},0);const oldWitnessNow={before:{x:224,y:304,facing:'up'},after:regression.tank,distance:Math.hypot(regression.tank.x-224,regression.tank.y-304)};assert.ok(oldWitnessNow.distance<=19);
const report={oldWitnessNow,map_sha256:crypto.createHash('sha256').update(fs.readFileSync(new URL('./map.json',import.meta.url))).digest('hex'),engine_sha256:crypto.createHash('sha256').update(fs.readFileSync(new URL('../../src/engine.mjs',import.meta.url))).digest('hex'),
 method:'Actual unchanged engine: every 8-unit sampled legal pose, all 16 cell states, all requested facings; deterministic physics/firing route replays',
 checked,worst,hulls:Object.fromEntries(facings.map(f=>[f,hullBounds(0,0,f)])),solutions:{long:solution(false),shortcut:solution(true)},stationarySpawnFire:{seconds:10,destroyed:negative.destroyed,shots:negative.shots,hits:negative.hits}};
fs.writeFileSync(new URL('./engine-results.json',import.meta.url),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({checked,worst,solutions:report.solutions},null,2));
