export const WORLD = 768, CELL = 64, HALF = 23;
export const VECTORS = {up: [0,-1], right: [1,0], down: [0,1], left: [-1,0]};
export const ANGLES = {right: 0, down: Math.PI/2, left: Math.PI, up: -Math.PI/2};
const targets = [[5,6],[5,4],[5,2],[8,3],[8,7],[2,4]];
const steel = [[2,7],[3,7],[8,5],[9,5],[2,2],[9,9]];
export function createState() {
  return {time:0, tank:{x:352,y:608,facing:'up'}, nextShot:0, firedAt:-100,
    shots:0, destroyed:0, hits:0, complete:false, shells:[], events:[],
    walls:[...targets.map(([x,y],id)=>({id,x:x*CELL,y:y*CELL,kind:'brick'})),
      ...steel.map(([x,y],i)=>({id:100+i,x:x*CELL,y:y*CELL,kind:'steel'}))]};
}
function overlaps(x,y,w) {return x+HALF>w.x && x-HALF<w.x+CELL && y+HALF>w.y && y-HALF<w.y+CELL;}
export function canMove(s,x,y) {
  return x>=HALF && y>=HALF && x<=WORLD-HALF && y<=WORLD-HALF && !s.walls.some(w=>overlaps(x,y,w));
}
// Earliest segment entry into an AABB, including a starting point on its edge.
export function intersect(x,y,dx,dy,w) {
  let near=0,far=1;
  for(const [p,d,min,max] of [[x,dx,w.x,w.x+CELL],[y,dy,w.y,w.y+CELL]]) {
    if(Math.abs(d)<1e-9) {if(p<min||p>max)return null;}
    else {let a=(min-p)/d,b=(max-p)/d;if(a>b)[a,b]=[b,a];near=Math.max(near,a);far=Math.min(far,b);if(near>far)return null;}
  }
  return near>=0&&near<=1?near:null;
}
function sweep(s,x,y,dx,dy) {
  let hit=null;
  for(const w of s.walls) {
    const t=intersect(x,y,dx,dy,w);
    if(t!==null&&(!hit||t<hit.t||(t===hit.t&&w.id<hit.wall.id)))hit={t,wall:w};
  }
  return hit;
}
function impact(s,hit,x,y) {
  const brick=hit.wall.kind==='brick';
  s.events.push({type:'impact',x,y,brick});s.hits++;
  if(brick){s.walls=s.walls.filter(w=>w.id!==hit.wall.id);s.destroyed++;}
}
export function step(s,input,dt) {
  s.events=[];
  if(s.complete)return s;
  dt=Math.max(0,Math.min(dt,.05));s.time+=dt;
  if(input.direction in VECTORS) {
    s.tank.facing=input.direction;
    const [dx,dy]=VECTORS[input.direction];const distance=156*dt;
    if(canMove(s,s.tank.x+dx*distance,s.tank.y+dy*distance)){s.tank.x+=dx*distance;s.tank.y+=dy*distance;}
  }
  if(input.fire&&s.time+1e-8>=s.nextShot) {
    const [dx,dy]=VECTORS[s.tank.facing];s.nextShot=s.time+1;s.firedAt=s.time;s.shots++;
    const muzzle=68;const hit=sweep(s,s.tank.x,s.tank.y,dx*muzzle,dy*muzzle);
    s.events.push({type:'fire',x:s.tank.x+dx*muzzle,y:s.tank.y+dy*muzzle,facing:s.tank.facing});
    if(hit)impact(s,hit,s.tank.x+dx*muzzle*hit.t,s.tank.y+dy*muzzle*hit.t);
    else s.shells.push({x:s.tank.x+dx*muzzle,y:s.tank.y+dy*muzzle,dx,dy});
  }
  s.shells=s.shells.filter(b=>{
    const dx=b.dx*480*dt,dy=b.dy*480*dt,hit=sweep(s,b.x,b.y,dx,dy);
    if(hit){impact(s,hit,b.x+dx*hit.t,b.y+dy*hit.t);return false;}
    b.x+=dx;b.y+=dy;return b.x>=0&&b.x<=WORLD&&b.y>=0&&b.y<=WORLD;
  });
  if(s.destroyed===targets.length){s.complete=true;s.events.push({type:'complete'});}
  return s;
}
export function recoil(age,reduced=false) {
  if(age<0||age>.24)return 0;
  const depth=reduced?4:12;
  return age<.045?depth*(age/.045):depth*Math.pow(1-(age-.045)/.195,2);
}
export function normalizeSettings(value) {
  return {language:value?.language==='zh-TW'?'zh-TW':'en',muted:value?.muted!==false,
    reduced:typeof value?.reduced==='boolean'?value.reduced:null};
}
