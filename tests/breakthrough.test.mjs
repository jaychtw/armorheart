// Historical M1 rules retained against its frozen scenario fixture; R3 has separate current-runtime tests.
import test from 'node:test';
import assert from 'node:assert/strict';
import {createMission,refreshRoute,advanceMission} from './fixtures/m1/breakthrough.mjs';
import {buildNavigation,planRoute,crowdSegmentClear,groupInsideExit} from './fixtures/m1/navigation.mjs';
import {BREAKTHROUGH,CROWD_DOTS,missionWalls} from './fixtures/m1/map.mjs';
import {step,canMove,VECTORS,hullBounds} from '../src/engine.mjs';
const remove=(s,...ids)=>{s.walls=s.walls.filter(w=>!ids.includes(w.id));s.destroyed=3-s.walls.filter(w=>w.kind==='brick').length;return refreshRoute(s);};
const pathLength=(p,path)=>path.reduce((sum,n)=>{const d=Math.hypot(n.x-p.x,n.y-p.y);p=n;return sum+d;},0);
for(let mask=0;mask<8;mask++)test(`M1 subset ${mask}: independent oracle connectivity and shortest route`,()=>{
 const s=createMission(),ids=[1,0,2].filter((_,i)=>mask>>i&1);remove(s,...ids);
 const expected=ids.includes(0)&&(ids.includes(1)||ids.includes(2));
 assert.equal(s.mission.crowd.path.length>0,expected);
 // Independent forward BFS: raw rectangle overlap and cardinal edges, no production nav helpers.
 const valid=([x,y])=>x>=208&&x<=560&&y>=16&&y<=752&&!s.walls.some(w=>x+16>w.x&&x-16<w.x+128&&y+16>w.y&&y-16<w.y+128);
 const q=[[384,704,0]],seen=new Set(['384,704']);let oracle=null;
 for(let i=0;i<q.length;i++){
  const [x,y,d]=q[i];if(x>=336&&x<=432&&y<=80){oracle=d;break;}
  for(const [dx,dy] of [[0,-32],[-32,0],[32,0],[0,32]]){const n=[x+dx,y+dy],key=n.join(',');if(!seen.has(key)&&valid(n)){seen.add(key);q.push([...n,d+32]);}}
 }
 assert.equal(oracle!==null,expected);
 if(expected){assert.equal(pathLength(s.mission.crowd,s.mission.crowd.path),oracle);assert.equal(oracle,800);}
});
test('tied lower routes prefer left, deterministic across wall array order',()=>{
 const a=createMission(),b=createMission();remove(a,0,1,2);b.walls.reverse();remove(b,0,1,2);
 assert.deepEqual(a.mission.crowd.path,b.mission.crowd.path);assert.ok(a.mission.crowd.path.some(p=>p.x===288&&p.y===448));
});
test('mid-edge route compares both endpoints and preserves continuation on ties',()=>{
 const nodes=new Map([['384,672',{x:384,y:672}],['384,704',{x:384,y:704}]]),p={x:384,y:688};
 const nav={nodes,distances:new Map([['384,672',10],['384,704',0]]),walls:[]};
 assert.deepEqual(planRoute(nav,p,[nodes.get('384,672'),nodes.get('384,704')])[0],{x:384,y:704});
 nav.distances.set('384,672',0);assert.deepEqual(planRoute(nav,p,[nodes.get('384,672'),nodes.get('384,704')])[0],{x:384,y:672});
});
test('swept group edges reject corner cuts even with clear endpoints',()=>{
 const wall={x:320,y:320,width:128,height:128};assert.equal(crowdSegmentClear({x:288,y:352},{x:480,y:352},[wall]),false);
 assert.equal(crowdSegmentClear({x:288,y:288},{x:480,y:480},[wall]),false);
 assert.equal(crowdSegmentClear({x:288,y:288},{x:480,y:288},[wall]),true);
});
test('group pixels fit the envelope and full exit containment, not center alone, wins',()=>{
 assert.equal(CROWD_DOTS.length,12);assert.ok(CROWD_DOTS.every(([x,y])=>Math.hypot(x,y)+3<=16));
 assert.equal(groupInsideExit({x:384,y:90}),false);assert.equal(groupInsideExit({x:384,y:80}),true);
});
test('route only replans after effective destruction; first full route announces once',()=>{
 const s=createMission();assert.equal(refreshRoute(s),false);assert.equal(s.mission.replans,1);
 assert.equal(remove(s,1),false);assert.equal(s.mission.phase,'waiting');assert.equal(remove(s,0),true);
 assert.equal(s.mission.phase,'evacuating');const n=s.mission.replans;assert.equal(refreshRoute(s),false);assert.equal(s.mission.replans,n);
 assert.equal(remove(s,2),false);assert.equal(s.mission.replans,n+1);
});
test('crowd remains inside walls and corridor at every intermediate movement sample',()=>{
 const s=createMission();remove(s,0,1);
 for(let i=0;i<2000&&!s.complete;i++){const before={x:s.mission.crowd.x,y:s.mission.crowd.y};advanceMission(s,1/120);assert.ok(crowdSegmentClear(before,s.mission.crowd,s.walls));}
 assert.equal(s.mission.phase,'success');assert.ok(groupInsideExit(s.mission.crowd));
});
test('long frame processes the full route, reports earlier success before late render',()=>{
 const s=createMission();remove(s,0,1);s.mission.elapsed=70;advanceMission(s,30);assert.equal(s.mission.phase,'success');assert.ok(s.mission.elapsed<90);assert.ok(groupInsideExit(s.mission.crowd));
});
for(const [elapsed,expected] of [[88.999,'success'],[89,'timeout'],[89.001,'timeout']])test(`arrival with elapsed ${elapsed} respects strict deadline`,()=>{
 const s=createMission();s.mission.elapsed=elapsed;s.mission.phase='evacuating';s.mission.crowd={x:384,y:128,path:[{x:384,y:64}],edgeFrom:{x:384,y:128}};
 advanceMission(s,2);assert.equal(s.mission.phase,expected);
});
test('visible time cannot be extended by physics clamp and terminal state is immutable',()=>{
 const s=createMission();advanceMission(s,90);assert.equal(s.mission.phase,'timeout');assert.equal(s.mission.elapsed,90);
 const before=structuredClone(s);step(s,{fire:true,direction:'left'},.05);advanceMission(s,10);assert.deepEqual(s,before);
});
test('tank at exit and every brick removed do not trigger six-block/range completion',()=>{
 const s=createMission();remove(s,0,1,2);s.tank={x:384,y:64,facing:'up'};step(s,{},.05);assert.equal(s.complete,false);assert.equal(s.mission.phase,'evacuating');
});
test('stationary spawn firing cannot open route; shells do not interact with crowd',()=>{
 const s=createMission();for(let i=0;i<600;i++){step(s,{fire:true},1/60);advanceMission(s,1/60);refreshRoute(s);}
 assert.equal(s.destroyed,0);assert.ok(s.hits>0);assert.equal(s.mission.phase,'waiting');assert.equal(s.mission.crowd.x,384);assert.equal(s.mission.crowd.y,704);
});
test('large blocks consume one shell/one hit and corridor side boundary consumes fire',()=>{
 const s=createMission();s.tank={x:256,y:560,facing:'up'};step(s,{fire:true},1/60);assert.equal(s.destroyed,1);assert.equal(s.shells.length,0);
 s.tank={x:240,y:672,facing:'left'};s.nextShot=0;step(s,{fire:true},1/60);assert.equal(s.shells.length,0);assert.equal(s.destroyed,1);
});
test('fresh Retry state resets map, time, route, shots and completion',()=>{
 const s=createMission();remove(s,0,1,2);advanceMission(s,100);const fresh=createMission();assert.equal(fresh.mission.elapsed,0);assert.equal(fresh.mission.phase,'waiting');assert.equal(fresh.walls.length,6);assert.equal(fresh.shots,0);assert.equal(fresh.complete,false);assert.deepEqual(fresh.mission.crowd.path,[]);
});
test('all map subsets/orientations stay clear with local R2 turn correction',()=>{
 for(let mask=0;mask<8;mask++){
  const base=createMission();remove(base,...[1,0,2].filter((_,i)=>mask>>i&1));
  for(let x=224;x<=544;x+=16)for(let y=48;y<=720;y+=16)for(const facing of Object.keys(VECTORS)){
   const s=structuredClone(base);s.tank={x,y,facing};if(!canMove(s,x,y))continue;
   for(const direction of Object.keys(VECTORS)){const t=structuredClone(s);step(t,{direction},0);assert.ok(canMove(t,t.tank.x,t.tank.y));assert.ok(Math.hypot(t.tank.x-x,t.tank.y-y)<=19+1e-8);}
  }
 }
});
test('crowd overlap never blocks tank motion or consumes a shot',()=>{
 const s=createMission();s.tank={x:384,y:720,facing:'up'};const c=structuredClone(s.mission.crowd);
 assert.ok(canMove(s,384,720));step(s,{fire:true},1/60);assert.equal(s.hits,0);assert.equal(s.shots,1);assert.deepEqual(s.mission.crowd,c);
 s.tank={x:348,y:704,facing:'right'};step(s,{direction:'right'},1/60);assert.ok(s.tank.x>348);assert.deepEqual(s.mission.crowd,c);
});
test('topology change after a deadline cannot create a late win',()=>{
 const s=createMission();remove(s,1);s.tank={x:384,y:301.5,facing:'up'};s.mission.elapsed=89.99;
 advanceMission(s,.02);step(s,{fire:true},.05);assert.equal(refreshRoute(s),false);assert.equal(s.mission.phase,'timeout');assert.equal(s.destroyed,1);assert.ok(s.walls.some(w=>w.id===0));
});
test('replan while moving keeps the continuous crowd center and valid edge',()=>{
 const s=createMission();remove(s,0,1);advanceMission(s,.1);const p={x:s.mission.crowd.x,y:s.mission.crowd.y};
 remove(s,2);assert.equal(s.mission.crowd.x,p.x);assert.equal(s.mission.crowd.y,p.y);advanceMission(s,.1);assert.ok(crowdSegmentClear(p,s.mission.crowd,s.walls));
});
