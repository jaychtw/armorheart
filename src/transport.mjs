import {BREAKTHROUGH} from './maps/breakthrough.mjs';
const DIRECTIONS=[[0,-16],[16,0],[0,16],[-16,0]];
const poseKey=p=>`${p.x},${p.y},${p.heading}`;
export function transportBounds(p,pad=BREAKTHROUGH.margin){
 const w=p.heading%2===0?28+pad:64+pad,h=p.heading%2===0?64+pad:28+pad;
 return {left:p.x-w,right:p.x+w,top:p.y-h,bottom:p.y+h};
}
function boxClear(b,walls){
 const a=BREAKTHROUGH.bounds;
 return b.left>=a.left&&b.right<=a.right&&b.top>=a.top&&b.bottom<=a.bottom&&
  !walls.some(w=>b.right>w.x&&b.left<w.x+(w.width??64)&&b.bottom>w.y&&b.top<w.y+(w.height??64));
}
export function transportPoseClear(p,walls){return boxClear(transportBounds(p),walls);}
export function transportSegmentClear(a,b,walls){
 if(a.heading!==b.heading)return false;
 const c=transportBounds(a),d=transportBounds(b);
 return boxClear({left:Math.min(c.left,d.left),right:Math.max(c.right,d.right),top:Math.min(c.top,d.top),bottom:Math.max(c.bottom,d.bottom)},walls);
}
export function transportTurnClear(p,walls){
 const b=BREAKTHROUGH.bounds,r=BREAKTHROUGH.turnRadius;
 return p.x-r>=b.left&&p.x+r<=b.right&&p.y-r>=b.top&&p.y+r<=b.bottom&&walls.every(w=>
  Math.hypot(Math.max(w.x-p.x,0,p.x-w.x-(w.width??64)),Math.max(w.y-p.y,0,p.y-w.y-(w.height??64)))>=r);
}
export function transportInsideExit(p){
 if(p.heading!==0)return false;
 const b=transportBounds(p,0),e=BREAKTHROUGH.exit;
 return b.left>=e.left&&b.right<=e.right&&b.top>=e.top&&b.bottom<=e.bottom;
}
// Stable binary heap: predicted time first, then insertion order. No random routes.
class Heap{
 constructor(){this.items=[];}
 less(a,b){return a.cost<b.cost||(a.cost===b.cost&&a.serial<b.serial);}
 push(v){const a=this.items;a.push(v);let i=a.length-1;while(i){const p=(i-1)>>1;if(!this.less(a[i],a[p]))break;[a[i],a[p]]=[a[p],a[i]];i=p;}}
 pop(){const a=this.items,v=a[0],tail=a.pop();if(a.length){a[0]=tail;let i=0;while(true){let j=i;const l=i*2+1,r=l+1;if(l<a.length&&this.less(a[l],a[j]))j=l;if(r<a.length&&this.less(a[r],a[j]))j=r;if(j===i)break;[a[i],a[j]]=[a[j],a[i]];i=j;}}return v;}
}
export function planTransport(walls,start){
 if(!transportPoseClear(start,walls))throw new Error('Transport starts outside its clear envelope');
 const q=new Heap(),distance=new Map([[poseKey(start),0]]),parents=new Map();let serial=0,end=null;
 q.push({pose:{...start},cost:0,serial:serial++});
 while(q.items.length){
  const {pose:p,cost}=q.pop(),pk=poseKey(p);if(cost>distance.get(pk)+1e-10)continue;
  if(transportInsideExit(p)){end=p;break;}
  const [dx,dy]=DIRECTIONS[p.heading],to={x:p.x+dx,y:p.y+dy,heading:p.heading};const options=[];
  if(transportSegmentClear(p,to,walls))options.push({kind:'forward',from:p,to,duration:16/BREAKTHROUGH.speed});
  if(transportTurnClear(p,walls))for(const [kind,delta] of [['left',-1],['right',1]])options.push({kind,from:p,to:{...p,heading:(p.heading+delta+4)%4},duration:BREAKTHROUGH.turnSeconds});
  for(const action of options){const key=poseKey(action.to),next=cost+action.duration;
   if(next<(distance.get(key)??Infinity)-1e-10){distance.set(key,next);parents.set(key,action);q.push({pose:action.to,cost:next,serial:serial++});}
  }
 }
 if(!end)return {actions:[],reachable:false,seconds:null,distance:0,turns:0,visited:distance.size};
 const actions=[];let p=end;while(poseKey(p)!==poseKey(start)){const action=parents.get(poseKey(p));actions.push(structuredClone(action));p=action.from;}actions.reverse();
 return {actions,reachable:true,seconds:distance.get(poseKey(end)),distance:actions.filter(a=>a.kind==='forward').length*16,turns:actions.filter(a=>a.kind!=='forward').length,visited:distance.size};
}
