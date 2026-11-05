import test from 'node:test';
import assert from 'node:assert/strict';
import {createState,step,intersect,recoil,normalizeSettings,hullBounds} from '../src/engine.mjs';
import {messages} from '../src/i18n.mjs';
function advance(s,seconds,input={}){for(let i=0;i<Math.round(seconds*60);i++)step(s,input,1/60);}
test('facing changes while an adjacent solid wall prevents movement',()=>{const s=createState();s.walls=[{id:0,x:320,y:320,kind:'steel'}];s.tank={x:352,y:384-hullBounds(0,0,'up').top,facing:'up'};step(s,{direction:'up'},1/60);assert.equal(s.tank.facing,'up');assert.equal(s.tank.y,429.5);});
test('cardinal movement has fixed speed, no diagonal and remains in bounds',()=>{const s=createState();advance(s,1,{direction:'right'});assert.ok(Math.abs(s.tank.x-508)<1e-7);assert.equal(s.tank.y,608);advance(s,10,{direction:'down'});assert.ok(s.tank.y<=745);});
test('first held shot is immediate, repeat interval is one second, ammunition is unlimited',()=>{const s=createState();s.walls=[];step(s,{fire:true},1/60);assert.equal(s.shots,1);advance(s,59/60,{fire:true});assert.equal(s.shots,1);step(s,{fire:true},1/60);assert.equal(s.shots,2);advance(s,10,{fire:true});assert.equal(s.shots,12);});
test('tapping fire cannot bypass cooldown',()=>{const s=createState();step(s,{fire:true},1/60);advance(s,.2);step(s,{fire:true},1/60);assert.equal(s.shots,1);});
test('one shell hits nearest wall, consumes itself and does not pierce',()=>{const s=createState();advance(s,.6,{fire:true});assert.equal(s.destroyed,1);assert.equal(s.shells.length,0);assert.ok(s.walls.some(w=>w.id===1));});
test('muzzle overlap cannot shoot through an adjacent wall',()=>{const s=createState();s.walls=[{id:0,x:320,y:320,kind:'brick'}];s.tank.y=429.5;step(s,{fire:true},1/60);assert.equal(s.destroyed,1);assert.equal(s.shells.length,0);});
test('steel consumes shell and remains unchanged',()=>{const s=createState();s.tank={x:160,y:608,facing:'up'};advance(s,.5,{fire:true});assert.equal(s.hits,1);assert.equal(s.destroyed,0);assert.equal(s.walls.length,12);assert.equal(s.shells.length,0);});
test('swept collision finds thin crossing even when endpoint is beyond wall',()=>{assert.equal(intersect(0,32,200,0,{x:64,y:0}),.32);assert.equal(intersect(0,100,200,0,{x:64,y:0}),null);});
test('completion occurs on sixth removed brick and reset restores scene',()=>{const s=createState();s.destroyed=5;s.walls=[{id:0,x:320,y:416,kind:'brick'}];s.tank.y=475;step(s,{fire:true},1/60);assert.equal(s.complete,true);assert.equal(s.destroyed,6);const next=createState();assert.equal(next.destroyed,0);assert.equal(next.walls.length,12);assert.equal(next.shots,0);});
test('independent recoil peaks then recovers; reduced motion preserves smaller cue',()=>{assert.equal(recoil(0),0);assert.equal(recoil(.045),12);assert.ok(recoil(.12)>0&&recoil(.12)<12);assert.equal(recoil(.3),0);assert.equal(recoil(.045,true),4);});
test('settings reject corrupt fields and localization key coverage matches',()=>{assert.deepEqual(normalizeSettings({language:'bad',muted:'no',reduced:'yes'}),{language:'en',muted:true,reduced:null});assert.deepEqual(Object.keys(messages.en).sort(),Object.keys(messages['zh-TW']).sort());});

// R2: actual source-space envelope, not the rejected 46x46 abstract square.
import {canMove,HULL_MASTER,VECTORS} from '../src/engine.mjs';
test('hull envelope uses artwork pivot/scale and excludes the protruding barrel',()=>{
 assert.deepEqual(HULL_MASTER,{left:12,top:70,right:198,bottom:185});
 const b=hullBounds(0,0,'right');assert.equal(b.right-b.left,93);assert.equal(b.bottom-b.top,57.5);assert.ok(b.right<68);
});
for(const kind of ['brick','steel'])for(const facing of ['up','right','down','left']){
 test(`${kind} contact clamps visible hull in ${facing} across frame deltas`,()=>{
  for(const dt of [1/240,1/60,.05,2]){
   const s=createState(),[dx,dy]=VECTORS[facing];s.walls=[{id:0,x:320,y:320,kind}];s.tank={x:352-dx*160,y:352-dy*160,facing};
   for(let i=0;i<1200;i++){step(s,{direction:facing},dt);assert.ok(canMove(s,s.tank.x,s.tank.y));}
   const b=hullBounds(s.tank.x,s.tank.y,facing);
   assert.ok(Math.abs((dx>0?b.right:dx<0?b.left:dy>0?b.bottom:b.top)-(dx>0||dy>0?320:384))<1e-7);
   assert.equal(s.destroyed,0);
  }
 });
}
test('adjacent walls, corner and parallel sliding do not clip or stick',()=>{
 const s=createState();s.walls=[{id:1,x:320,y:320,kind:'brick'},{id:2,x:384,y:320,kind:'steel'}];s.tank={x:270,y:291.5,facing:'right'};
 advance(s,1,{direction:'right'});assert.ok(Math.abs(s.tank.x-426)<1e-7);assert.ok(canMove(s,s.tank.x,s.tank.y));
 for(const direction of ['down','left','up','right']){step(s,{direction},0);assert.equal(s.tank.facing,direction);assert.ok(canMove(s,s.tank.x,s.tank.y));}
});
test('blocked cardinal turn resolves hull clearance and never moves through a wall',()=>{
 const s=createState();s.walls=[{id:0,x:320,y:320,kind:'steel'}];s.tank={x:291.5,y:352,facing:'up'};
 step(s,{direction:'right'},0);assert.equal(s.tank.facing,'right');assert.ok(canMove(s,s.tank.x,s.tank.y));assert.equal(s.tank.x,274.5);
 const before=structuredClone(s.tank);advance(s,2,{direction:'right'});assert.deepEqual(s.tank,before);
});
test('barrel overlap still consumes one projectile at the first wall',()=>{
 const s=createState();s.walls=[{id:0,x:320,y:320,kind:'brick'},{id:1,x:384,y:320,kind:'steel'}];s.tank={x:274.5,y:352,facing:'right'};
 assert.ok(s.tank.x+68>320);step(s,{fire:true},1/60);assert.equal(s.destroyed,1);assert.equal(s.hits,1);assert.equal(s.shells.length,0);assert.equal(s.walls[0].id,1);
});
test('revised proving ground keeps wall counts and avoids corridor-sized turn relocations',()=>{
 const base=createState();assert.equal(base.walls.filter(w=>w.kind==='brick').length,6);assert.equal(base.walls.filter(w=>w.kind==='steel').length,6);
 // Dense deterministic samples include edges/corners; <=19 units is the maximum
 // expansion of the rotated artwork bounds, rather than relocation out of a gap.
 let samples=0;
 for(let x=30;x<740;x+=8)for(let y=30;y<740;y+=8)for(const facing of Object.keys(VECTORS)){
  const s=structuredClone(base);s.tank={x,y,facing};if(!canMove(s,x,y))continue;
  for(const direction of Object.keys(VECTORS)){const t=structuredClone(s);step(t,{direction},0);
   assert.equal(t.tank.facing,direction);assert.ok(canMove(t,t.tank.x,t.tank.y));assert.ok(Math.hypot(t.tank.x-x,t.tank.y-y)<=19+1e-7);samples++;}
 }
 assert.ok(samples>50000);
});
