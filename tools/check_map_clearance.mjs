// Spatial samples of all brick-removal combinations; no browser/runtime dependency.
import {createState,canMove,step,VECTORS} from '../src/engine.mjs';
import fs from 'node:fs';
let max=0,count=0,worst=null;
for(let mask=0;mask<64;mask++){
 const base=createState();base.walls=base.walls.filter(w=>w.kind==='steel'||!(mask&(1<<w.id)));
 for(let x=30;x<740;x+=24)for(let y=30;y<740;y+=24)for(const f of Object.keys(VECTORS)){
  const s=structuredClone(base);s.tank={x,y,facing:f};if(!canMove(s,x,y))continue;
  for(const direction of Object.keys(VECTORS)){
   const t=structuredClone(s);step(t,{direction},0);const d=Math.hypot(t.tank.x-x,t.tank.y-y);
   if(d>max){max=d;worst={mask,x,y,f,direction,result:t.tank};}
   if(!canMove(t,t.tank.x,t.tank.y)||d>19.00001)throw Error(JSON.stringify({mask,x,y,f,direction,d}));count++;
  }
 }
}
fs.mkdirSync(new URL('../evidence/r2/',import.meta.url),{recursive:true});
fs.writeFileSync(new URL('../evidence/r2/map-clearance.json',import.meta.url),JSON.stringify({method:'24-unit spatial grid; all four initial and requested facings; all 64 subsets of destroyed bricks',count,max,worst},null,2)+'\n');
console.log({count,max});
