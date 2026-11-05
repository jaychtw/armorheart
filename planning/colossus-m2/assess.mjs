// Planning-only calculations. Uses accepted hull/movement, not a Colossus simulator.
import fs from 'node:fs';import assert from 'node:assert/strict';
import {createState,step,canMove,hullBounds} from '../../src/engine.mjs';
const dir=new URL('./',import.meta.url),data=JSON.parse(fs.readFileSync(new URL('arena.json',dir))),art=JSON.parse(fs.readFileSync(new URL('art/metadata.json',dir)));
const scale=256/art.source[0],anchor=art.ground_anchor_source.map(x=>x*scale),frame={left:-anchor[0],right:256-anchor[0],top:-anchor[1],bottom:256-anchor[1]};
let checked=0,minimumSpriteMargin=Infinity;
for(let i=0;i<5;i++){
 const a=data.jump_order[i],b=data.jump_order[(i+1)%5];
 for(let k=0;k<=120;k++){const t=k/120,x=a.x+(b.x-a.x)*t,y=a.y+(b.y-a.y)*t,z=64*Math.sin(Math.PI*t);
  const gap=Math.min(x+frame.left,768-x-frame.right,y+frame.top-z,768-y-frame.bottom+z);assert.ok(gap>=0);minimumSpriteMargin=Math.min(minimumSpriteMargin,gap);checked++;}
}
const spawn=createState();spawn.walls=[];spawn.tank={...data.tank};delete spawn.tank.hp;assert.ok(canMove(spawn,64,704));
const fullFrameMinimumX=Math.min(...data.jump_order.map(p=>p.x+frame.left));assert.ok(fullFrameMinimumX>64,'stationary spawn-up ray misses every grounded sprite frame');
function move(s,direction,axis,target){const sign=['left','up'].includes(direction)?-1:1;let n=0;while((target-s.tank[axis])*sign>1e-7){step(s,{direction},Math.min(.05,Math.abs(target-s.tank[axis])/156));assert.ok(canMove(s,s.tank.x,s.tank.y));assert.ok(++n<1000);}return s.time;}
const witness=createState();witness.walls=[];witness.tank={x:64,y:704,facing:'up'};const arrivalFirst=move(witness,'right','x',560);const prior={...witness.tank};step(witness,{direction:'up'},0);assert.deepEqual(witness.tank,{...prior,facing:'up'});
const transfer=352/156,secondReady=7.5+transfer+1/60;assert.ok(secondReady<9.85);
const coreY=(data.attack_example.core_source_pixel[1]-art.ground_anchor_source[1])*scale;
const shellTravel=(160-68-coreY)/480;const windows=[[6.4,8.4],[9.6,11.6]];
const impacts=data.attack_example.emission_times.map((t,i)=>{const time=t+shellTravel,[a,b]=windows[i>>1];assert.ok(time>=a&&time<b);return {emission:t,arrivalUpperBound:time,groundWindow:[a,b]};});
for(let i=1;i<impacts.length;i++)assert.ok(impacts[i].emission-impacts[i-1].emission>=1-1e-9);
const southHull=hullBounds(0,160,'up'),contactGap=southHull.top-data.contact_ellipse_radii[1];assert.ok(contactGap>0);
const stationHull=hullBounds(560,704,'up');
const safeAtAllStops=data.jump_order.every(p=>{const x=Math.max(stationHull.left,Math.min(p.x,stationHull.right)),y=Math.max(stationHull.top,Math.min(p.y,stationHull.bottom));return ((x-p.x)/112)**2+((y-p.y)/64)**2>1;});assert.ok(safeAtAllStops);
const upperTravel=(704-68-(288+coreY))/480;
const campShots=[{emission:3.25,arrivalUpperBound:3.25+upperTravel,stop:'UR'},{emission:4.25,arrivalUpperBound:4.25+upperTravel,stop:'UR'},{emission:6.45,arrivalUpperBound:6.45+shellTravel,stop:'LR'},{emission:7.45,arrivalUpperBound:7.45+shellTravel,stop:'LR'}];
assert.ok(campShots[1].arrivalUpperBound<5.2&&campShots[3].arrivalUpperBound<8.4);
const report={status:'analytical feasibility and actual accepted-engine empty-arena movement only; not Level2 playthrough or combat implementation',full_cycle_seconds:5*(2+1.2),sampled_sprite_poses:checked,minimum_full_frame_world_margin:minimumSpriteMargin,analytic_frame_margin_lower_bound:Math.min(...data.jump_order.map(p=>p.y))+frame.top-64,
 spawn:spawn.tank,stationary_spawn_ray_minimum_frame_gap:fullFrameMinimumX-64,first_attack_station_arrival:arrivalFirst,second_attack_station_ready:secondReady,physical_contact_vertical_gap:contactGap,conservative_shell_seconds:shellTravel,impacts,core_source_pixel:data.attack_example.core_source_pixel,safe_stationary_lane:{station:[560,704],safe_at_all_grounded_stops:safeAtAllStops,shots:campShots,status:'balance characteristic needing owner review; do not silently add attacks or shorten pause'},default_hp_stage_mapping:{4:'Intact',3:'Fatigued',2:'Fatigued',1:'Wounded',0:'Defeated'},not_verified:['production hurtbox alignment','airborne/landing damage code','pose registration/four-facing consistency','M2 browser playthrough','human balance/creative acceptance']};
fs.writeFileSync(new URL('evidence/assessment.json',dir),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
