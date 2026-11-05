import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createMission,refreshRoute,advanceMission,truckRenderHeading} from '../src/breakthrough.mjs';
import {BREAKTHROUGH,missionWalls} from '../src/maps/breakthrough.mjs';
import {planTransport,transportBounds,transportPoseClear,transportSegmentClear,transportTurnClear,transportInsideExit} from '../src/transport.mjs';
import {step,canMove} from '../src/engine.mjs';
const approved=JSON.parse(fs.readFileSync(new URL('../planning/r3-geometry/map.json',import.meta.url)));
const oracle=JSON.parse(fs.readFileSync(new URL('../planning/r3-geometry/transport-results.json',import.meta.url))).states;
const ids=['U0','U1','L0','L1'];
function remove(s,...names){s.walls=s.walls.filter(w=>!names.includes(w.id));s.destroyed=4-s.walls.filter(w=>w.kind==='brick').length;return refreshRoute(s);}
test('R3 runtime geometry is exactly the approved map, spawns and clearance',()=>{
 assert.deepEqual(missionWalls(),approved.walls.map(w=>({...w,width:64,height:64})));assert.deepEqual(BREAKTHROUGH.bounds,approved.bounds);assert.deepEqual(BREAKTHROUGH.exit,approved.exit);assert.deepEqual(BREAKTHROUGH.tank,approved.tank);assert.deepEqual(BREAKTHROUGH.truck,approved.truck);assert.deepEqual(BREAKTHROUGH.body,[128,56]);assert.equal(BREAKTHROUGH.margin,4);assert.equal(BREAKTHROUGH.turnRadius,76);
});
for(let mask=0;mask<16;mask++)test(`R3 state ${mask}: runtime matches independent geometry oracle and swept actions`,()=>{
 const s=createMission();remove(s,...ids.filter((_,i)=>mask>>i&1));const r=planTransport(s.walls,BREAKTHROUGH.truck),expected=oracle[mask];
 assert.equal(r.reachable,expected.reachable);
 if(r.reachable){assert.ok(Math.abs(r.seconds-expected.predicted_seconds)<1e-8);assert.equal(r.distance,expected.travel_units);assert.equal(r.turns,expected.quarter_turns);
  let previous={...BREAKTHROUGH.truck};for(const a of r.actions){assert.deepEqual(a.from,previous);assert.ok(transportPoseClear(a.from,s.walls));assert.ok(transportPoseClear(a.to,s.walls));assert.ok(a.kind==='forward'?transportSegmentClear(a.from,a.to,s.walls):transportTurnClear(a.from,s.walls));previous=a.to;}
  assert.ok(transportInsideExit(previous));advanceMission(s,60);assert.equal(s.mission.phase,'success');assert.ok(Math.abs(s.mission.elapsed-r.seconds)<1e-8);
 }else{advanceMission(s,10);assert.equal(s.mission.phase,'waiting');assert.equal(s.mission.truck.x,272);assert.equal(s.mission.truck.y,688);}
});
test('deterministic routes survive reversed wall iteration order',()=>{const s=createMission();remove(s,'U0','U1');assert.deepEqual(planTransport(s.walls,BREAKTHROUGH.truck).actions,planTransport([...s.walls].reverse(),BREAKTHROUGH.truck).actions);});
test('one effective projectile removes one cell, not the mixed 2x2 island',()=>{
 const s=createMission();s.tank={x:274.5,y:160,facing:'right'};step(s,{fire:true},1/60);assert.equal(s.destroyed,1);assert.ok(!s.walls.some(w=>w.id==='U0'));assert.ok(['U1','US0','US1'].every(id=>s.walls.some(w=>w.id===id)));assert.equal(s.shells.length,0);
});
test('waiting steel impacts never trigger replanning or solve the maze',()=>{
 const s=createMission();for(let i=0;i<600;i++){step(s,{fire:true},1/60);refreshRoute(s);}assert.equal(s.destroyed,0);assert.ok(s.hits>0);assert.equal(s.mission.replans,1);assert.equal(s.mission.phase,'waiting');
});
test('route-open cue occurs only once after both upper cells are gone',()=>{
 const s=createMission();assert.equal(remove(s,'U0'),false);assert.equal(remove(s,'U1'),true);assert.equal(s.mission.phase,'evacuating');assert.equal(refreshRoute(s),false);assert.equal(remove(s,'L1'),false);
});
test('one lower cell does not create the shortcut',()=>{
 const a=createMission(),b=createMission();remove(a,'U0','U1');remove(b,'U0','U1','L0');assert.equal(a.mission.routeDistance,976);assert.equal(b.mission.routeDistance,976);remove(b,'L1');assert.equal(b.mission.routeDistance,656);assert.ok(b.mission.predictedRouteSeconds<a.mission.predictedRouteSeconds);
});
test('newly available shortcut replans at a legal action endpoint without a jump',()=>{
 const s=createMission();remove(s,'U0','U1');advanceMission(s,.1);const t=s.mission.truck,at={x:t.x,y:t.y,heading:t.heading},n=s.mission.replans;
 remove(s,'L0','L1');assert.deepEqual({x:t.x,y:t.y,heading:t.heading},at);assert.equal(s.mission.pendingReplan,true);assert.equal(s.mission.replans,n);
 advanceMission(s,.25);assert.equal(t.x,288);assert.equal(t.y,688);assert.equal(s.mission.pendingReplan,false);assert.equal(s.mission.replans,n+1);assert.equal(t.action.kind,'left');assert.ok(transportTurnClear(t,s.walls));
});
test('partial pivots are timed in place and their interpolation is preserved',()=>{
 const s=createMission();remove(s,'U0','U1','L0','L1');advanceMission(s,16/48+.175);const t=s.mission.truck;assert.equal(t.x,288);assert.equal(t.y,688);assert.ok(Math.abs(truckRenderHeading(t)-.5)<1e-9);const saved=structuredClone(t);advanceMission(s,0);assert.deepEqual(t,saved);advanceMission(s,.175);assert.equal(t.heading,0);assert.equal(t.action,null);
});
test('entire truck and north-facing orientation required at exit',()=>{
 assert.equal(transportInsideExit({x:352,y:160,heading:0}),false);assert.equal(transportInsideExit({x:352,y:128,heading:0}),true);assert.equal(transportInsideExit({x:352,y:112,heading:1}),false);assert.equal(transportInsideExit({x:332,y:112,heading:0}),false);
});
for(const [elapsed,expected] of [[89.649,'success'],[89.65,'timeout'],[89.651,'timeout']])test(`pivot arrival at elapsed ${elapsed} honors strict90-second boundary`,()=>{
 const s=createMission();remove(s,'U0','U1');s.mission.elapsed=elapsed;s.mission.phase='evacuating';s.mission.plan=[];s.mission.truck={x:352,y:112,heading:1,action:{kind:'left',from:{x:352,y:112,heading:1},to:{x:352,y:112,heading:0},duration:.35,progress:0}};advanceMission(s,2);assert.equal(s.mission.phase,expected);
});
test('late rendered frame retains earlier valid arrival and freezes terminal state',()=>{
 const s=createMission();remove(s,'U0','U1');s.mission.elapsed=60;advanceMission(s,50);assert.equal(s.mission.phase,'success');assert.ok(s.mission.elapsed<90);const snapshot=structuredClone(s);advanceMission(s,10);step(s,{fire:true,direction:'left'},.05);assert.deepEqual(s,snapshot);
});
test('no route times out on real active interval and late demolition cannot win',()=>{
 const s=createMission();advanceMission(s,91);assert.equal(s.mission.phase,'timeout');assert.equal(s.mission.elapsed,90);const before=s.destroyed;step(s,{fire:true},.05);assert.equal(s.destroyed,before);assert.equal(refreshRoute(s),false);
});
test('tank and shots do not block or damage the transport',()=>{
 const s=createMission();s.tank={x:272,y:688,facing:'right'};assert.ok(canMove(s,272,688));step(s,{fire:true,direction:'right'},1/60);assert.ok(s.tank.x>272);assert.equal(s.hits,0);assert.equal(s.mission.truck.x,272);assert.equal(s.mission.truck.y,688);
});
test('Retry creates fresh transport/map/time without stale actions',()=>{
 const s=createMission();remove(s,'U0','U1');advanceMission(s,100);const fresh=createMission();assert.equal(fresh.complete,false);assert.equal(fresh.mission.elapsed,0);assert.equal(fresh.mission.phase,'waiting');assert.equal(fresh.mission.truck.action,null);assert.deepEqual(fresh.mission.plan,[]);assert.equal(fresh.walls.length,9);assert.equal(fresh.shots,0);
});
test('all bricks removed or Guardian reaching refuge is not mission success',()=>{
 const s=createMission();remove(s,...ids);s.tank={x:352,y:112,facing:'up'};step(s,{},.05);assert.equal(s.complete,false);assert.equal(s.mission.phase,'evacuating');
});
test('navigation rejects a point-only passage and radius76 protects full pivot',()=>{
 const s=createMission();assert.equal(transportTurnClear({x:224,y:400,heading:0},s.walls),false);assert.equal(transportPoseClear({x:560,y:400,heading:1},s.walls),false);assert.deepEqual(transportBounds({x:272,y:688,heading:1},0),{left:208,right:336,top:660,bottom:716});
});
for(let mask=0;mask<16;mask++)test(`R3 state ${mask}: each remaining brick takes exactly one shot from a legal pose`,()=>{
 const poses={U0:{x:274.5,y:160,facing:'right'},U1:{x:500,y:160,facing:'left'},L0:{x:240,y:512,facing:'right'},L1:{x:240,y:576,facing:'right'}};
 for(const id of ids.filter((_,i)=>!(mask>>i&1))){
  const s=createMission();remove(s,...ids.filter((_,i)=>mask>>i&1));s.tank={...poses[id]};assert.ok(canMove(s,s.tank.x,s.tank.y));
  const before=s.walls.map(w=>w.id),damage=s.destroyed;step(s,{fire:true},1/60);
  assert.deepEqual(before.filter(n=>!s.walls.some(w=>w.id===n)),[id]);assert.equal(s.destroyed,damage+1);assert.equal(s.shots,1);assert.equal(s.walls.filter(w=>w.kind==='steel').length,5);
 }
});
