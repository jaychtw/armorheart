// Isolated playtest-map substitution, not shipping mechanics or a human fun test.
import fs from 'node:fs';import {COLOSSUS} from '../src/maps/colossus.mjs';
const code=fs.readFileSync(new URL('../src/colossus.mjs',import.meta.url),'utf8'),rows=[];
for(const jumpSeconds of [1,1.2,1.4]){
 const data='data:text/javascript;base64,'+Buffer.from('export const COLOSSUS='+JSON.stringify({...COLOSSUS,jumpSeconds})).toString('base64');
 let source=code.replace("'./maps/colossus.mjs'",JSON.stringify(data));for(const file of ['engine.mjs','colossus-art.mjs'])source=source.replace("'./"+file+"'",JSON.stringify(new URL('../src/'+file,import.meta.url).href));
 const mod=await import('data:text/javascript;base64,'+Buffer.from(source).toString('base64')),s=mod.createColossus();let distance=496;
 while(distance>1e-8){const dt=Math.min(1/60,distance/156);mod.stepColossus(s,{direction:'right'},dt);distance-=dt*156;}mod.stepColossus(s,{direction:'up'},0);
 for(let n=0;n<1200&&!s.complete;n++)mod.stepColossus(s,{fire:true},1/60);
 rows.push({jumpSeconds,outcome:s.colossus.outcome,finishedAt:s.colossus.finishedAt,tankHP:s.colossus.tankHP,shots:s.shots,hitTimes:s.colossus.shotHits,after_aim_movement:false});
}
const report={method:'same current combat module with only jumpSeconds substituted in an isolated imported map; informed held-fire simulation, not browser/human testing',rows,decision:'retain approved1.2s;1.0/1.4 still permit a damage-free stationary lane and do not create ongoing responses; no HP/attack/sequence/vulnerability change adopted'};
fs.writeFileSync('evidence/m2/balance-parameter-check.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(rows.map(r=>({jump:r.jumpSeconds,win:r.finishedAt,hp:r.tankHP}))));
