export const WORLD = 768, CELL = 64;
// Conservative opaque hull/track envelope in the original 256px artwork.
// Barrel is excluded; same pivot and scale as the frozen renderer.
export const HULL_MASTER = Object.freeze({left:12, top:70, right:198, bottom:185});
export function hullBounds(x,y,facing) {
  const {left,top,right,bottom}=HULL_MASTER;
  const local=[[left,top],[right,top],[right,bottom],[left,bottom]].map(([a,b])=>[(a-107)*.5,(b-128)*.5]);
  const rotate=([a,b])=>facing==='up'?[b,-a]:facing==='down'?[-b,a]:facing==='left'?[-a,-b]:[a,b];
  const points=local.map(rotate);
  return {left:x+Math.min(...points.map(p=>p[0])),right:x+Math.max(...points.map(p=>p[0])),
    top:y+Math.min(...points.map(p=>p[1])),bottom:y+Math.max(...points.map(p=>p[1]))};
}
export const VECTORS = {up: [0,-1], right: [1,0], down: [0,1], left: [-1,0]};
export const ANGLES = {right: 0, down: Math.PI/2, left: Math.PI, up: -Math.PI/2};
const targets = [[5,5],[5,2],[8,2],[8,5],[6,8],[9,8]];
const steel = [[2,2],[2,3],[2,4],[2,5],[2,6],[2,7]];
export function createState() {
  return {time:0, tank:{x:352,y:608,facing:'up'}, nextShot:0, firedAt:-100,
    shots:0, destroyed:0, hits:0, complete:false, shells:[], events:[],
    walls:[...targets.map(([x,y],id)=>({id,x:x*CELL,y:y*CELL,kind:'brick'})),
      ...steel.map(([x,y],i)=>({id:100+i,x:x*CELL,y:y*CELL,kind:'steel'}))]};
}
const EPS=1e-8;
export function canMove(s,x,y,facing=s.tank.facing) {
  const b=hullBounds(x,y,facing);
  return b.left>=-EPS&&b.top>=-EPS&&b.right<=WORLD+EPS&&b.bottom<=WORLD+EPS&&
    !s.walls.some(w=>b.right>w.x+EPS&&b.left<w.x+CELL-EPS&&b.bottom>w.y+EPS&&b.top<w.y+CELL-EPS);
}
function turn(s,facing) {
  if(s.tank.facing===facing)return;
  const {x,y}=s.tank,b=hullBounds(0,0,facing);
  s.tank.facing=facing;
  if(canMove(s,x,y))return;
  // Immediate cardinal rotation has no intermediate arc. Find the nearest legal
  // center on obstacle/world faces instead of drawing an expanded hull in a wall.
  const xs=[x,-b.left,WORLD-b.right],ys=[y,-b.top,WORLD-b.bottom];
  for(const w of s.walls){xs.push(w.x-b.right,w.x+CELL-b.left);ys.push(w.y-b.bottom,w.y+CELL-b.top);}
  let best=null;
  for(const xx of xs)for(const yy of ys){const d=(xx-x)**2+(yy-y)**2;
    if((!best||d<best.d-EPS)&&canMove(s,xx,yy))best={x:xx,y:yy,d};}
  if(!best)throw new Error('No legal hull placement for cardinal turn');
  s.tank.x=best.x;s.tank.y=best.y;
}
function moveTank(s,dx,dy,distance) {
  const {x,y,facing}=s.tank,b=hullBounds(x,y,facing);
  let allowed=distance;
  if(dx)allowed=Math.min(allowed,dx>0?WORLD-b.right:b.left);
  else allowed=Math.min(allowed,dy>0?WORLD-b.bottom:b.top);
  for(const w of s.walls){
    if(dx&&b.bottom>w.y+EPS&&b.top<w.y+CELL-EPS){
      if(dx>0&&w.x>=b.right-EPS)allowed=Math.min(allowed,w.x-b.right);
      if(dx<0&&w.x+CELL<=b.left+EPS)allowed=Math.min(allowed,b.left-w.x-CELL);
    }
    if(dy&&b.right>w.x+EPS&&b.left<w.x+CELL-EPS){
      if(dy>0&&w.y>=b.bottom-EPS)allowed=Math.min(allowed,w.y-b.bottom);
      if(dy<0&&w.y+CELL<=b.top+EPS)allowed=Math.min(allowed,b.top-w.y-CELL);
    }
  }
  allowed=Math.max(0,allowed);s.tank.x+=dx*allowed;s.tank.y+=dy*allowed;
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
    turn(s,input.direction);
    const [dx,dy]=VECTORS[input.direction];const distance=156*dt;
    moveTank(s,dx,dy,distance);
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
