import {BREAKTHROUGH} from './map.mjs';
const NAV_DIRECTIONS=[[0,-32],[-32,0],[32,0],[0,32]];
const nodeKey=(x,y)=>`${x},${y}`;
export function groupInsideExit(p,exit=BREAKTHROUGH.exit,r=BREAKTHROUGH.radius){
  return p.x-r>=exit.left&&p.x+r<=exit.right&&p.y-r>=exit.top&&p.y+r<=exit.bottom;
}
// The whole swept square envelope is conservative for the circular dot group.
export function crowdSegmentClear(a,b,walls,bounds=BREAKTHROUGH.bounds,r=BREAKTHROUGH.radius){
  const left=Math.min(a.x,b.x)-r,right=Math.max(a.x,b.x)+r,top=Math.min(a.y,b.y)-r,bottom=Math.max(a.y,b.y)+r;
  return left>=bounds.left&&right<=bounds.right&&top>=bounds.top&&bottom<=bounds.bottom&&
    !walls.some(w=>right>w.x&&left<w.x+(w.width??64)&&bottom>w.y&&top<w.y+(w.height??64));
}
export function buildNavigation(walls){
  const nodes=new Map(),distances=new Map(),queue=[];
  for(let y=32;y<=736;y+=32)for(let x=224;x<=544;x+=32){
    const p={x,y};if(!crowdSegmentClear(p,p,walls))continue;
    const k=nodeKey(x,y);nodes.set(k,p);if(groupInsideExit(p)){distances.set(k,0);queue.push(p);}
  }
  for(let head=0;head<queue.length;head++){
    const p=queue[head],distance=distances.get(nodeKey(p.x,p.y));
    for(const [dx,dy] of NAV_DIRECTIONS){
      const k=nodeKey(p.x+dx,p.y+dy),n=nodes.get(k);
      if(n&&!distances.has(k)&&crowdSegmentClear(p,n,walls)){distances.set(k,distance+1);queue.push(n);}
    }
  }
  return {nodes,distances,walls};
}
export function planRoute(nav,position,endpoints=[]){
  const exact=nav.nodes.get(nodeKey(position.x,position.y));
  const candidates=exact?[exact]:endpoints;
  let best=null;
  for(const p of candidates){
    const d=nav.distances.get(nodeKey(p.x,p.y));
    if(d===undefined||!crowdSegmentClear(position,p,nav.walls))continue;
    const cost=Math.hypot(p.x-position.x,p.y-position.y)+d*32;
    // Endpoints are ordered continuation first; an exact tie keeps it.
    if(!best||cost<best.cost-1e-8)best={p,cost};
  }
  if(!best)return [];
  let p=best.p,route=[];
  if(p.x!==position.x||p.y!==position.y)route.push({...p});
  while(nav.distances.get(nodeKey(p.x,p.y))>0){
    const d=nav.distances.get(nodeKey(p.x,p.y));let next=null;
    for(const [dx,dy] of NAV_DIRECTIONS){
      const n=nav.nodes.get(nodeKey(p.x+dx,p.y+dy));
      if(n&&nav.distances.get(nodeKey(n.x,n.y))===d-1&&crowdSegmentClear(p,n,nav.walls)){next=n;break;}
    }
    if(!next)throw new Error('Broken navigation distance field');route.push({...next});p=next;
  }
  return route;
}
