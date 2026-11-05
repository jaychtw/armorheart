import fs from 'node:fs';import {C,simulate,stationary,interceptLeft,routeLength} from './model.mjs';
const rows=[];for(const speed of [40,56,64,72,80]){const spawn=simulate(stationary(),{speed}),active=simulate(interceptLeft,{speed});rows.push({speed,duration:routeLength/speed,spawn,active});console.log(speed,'spawn',spawn.outcome,spawn.time,spawn.bossHP,spawn.tankHP,'active',active.outcome,active.time,active.bossHP,active.tankHP);}
fs.writeFileSync(new URL('./evidence/parameter-assessment.json',import.meta.url),JSON.stringify(rows,null,2)+'\n');
const winners=[],totals={};let maxDamage=0;
for(const delay of [0,.125,.25,.375,.5,.625,.75,.875])for(const x of [272,304,352,384,416,464,496])for(const y of [288,352,432,512,592,688,720])for(const facing of ['up','right','down','left']){
 let arrived=null;
 const policy=(t,tank)=>{if(Math.abs(tank.x-x)>1)return{direction:tank.x>x?'left':'right'};if(Math.abs(tank.y-y)>1)return{direction:tank.y>y?'up':'down'};arrived??=t;return{face:facing,fire:t>=arrived+delay};};
 const r=simulate(policy);maxDamage=Math.max(maxDamage,6-r.bossHP);totals[r.outcome]=(totals[r.outcome]??0)+1;if(r.outcome==='win')winners.push({x,y,facing,delay,time:r.time,tankHP:r.tankHP,history:r.history});
}
const twoSideThenTop=(t,tank)=>t<.675?{direction:'left'}:t<1.9?{face:'left',fire:true}:t<2.575?{direction:'right'}:{face:'up',fire:true};
const witness=simulate(twoSideThenTop),convergence=[1/120,1/240,1/480].map(dt=>({dt,...simulate(twoSideThenTop,{dt})}));
const out={status:'isolated mathematical Offer model; no M3 runtime implementation or actual-input player test',proposedSpeed:C.ship.speed,routeLength,duration:routeLength/C.ship.speed,stationaryReachableCampSamples:1568,grid:{x:[272,304,352,384,416,464,496],y:[288,352,432,512,592,688,720],facings:4,delayPhases:8},totals,maxDamage,winners,witness,convergence,spawn:simulate(stationary()),noFire:simulate(()=>({})),exactVolleys:simulate(()=>({}),{enemy:false}).volleys};
fs.writeFileSync(new URL('./evidence/combat-assessment.json',import.meta.url),JSON.stringify(out,null,2)+'\n');console.log('Camp search',totals,'max hits',maxDamage,'witness',witness.outcome,witness.time,witness.tankHP,'first wins',winners.slice(0,3));
