// Mathematical route/diagram utility only; not an M3 game adapter.
import {intersect} from '../../src/engine.mjs';
export function createGeometry(C){
 const r=C.route,R=r.leftCorner.radius,Q=Math.PI*R/2;
 const lengths=[r.start[1]-r.leftTangent[1],Q,r.topRight[0]-r.topLeft[0],Q,r.exit[1]-r.rightTangent[1]],routeLength=lengths.reduce((a,b)=>a+b,0);
 function poseAtDistance(distance){
  let d=Math.max(0,Math.min(routeLength,distance));
  if(d<=lengths[0])return{x:r.start[0],y:r.start[1]-d,heading:-Math.PI/2,leg:'left'};d-=lengths[0];
  if(d<=Q){const a=Math.PI+d/R;return{x:r.leftCorner.center[0]+R*Math.cos(a),y:r.leftCorner.center[1]+R*Math.sin(a),heading:a-3*Math.PI/2,leg:'leftTurn'};}d-=Q;
  if(d<=lengths[2])return{x:r.topLeft[0]+d,y:r.topLeft[1],heading:0,leg:'top'};d-=lengths[2];
  if(d<=Q){const a=3*Math.PI/2+d/R;return{x:r.rightCorner.center[0]+R*Math.cos(a),y:r.rightCorner.center[1]+R*Math.sin(a),heading:a-3*Math.PI/2,leg:'rightTurn'};}d-=Q;
  return{x:r.rightTangent[0],y:r.rightTangent[1]+d,heading:Math.PI/2,leg:'right'};
 }
 const pose=(t,speed=C.ship.speed)=>poseAtDistance(t*speed);
 function world(p,u,v){const a=p.heading;return{x:p.x+u*Math.cos(a)-v*Math.sin(a),y:p.y+u*Math.sin(a)+v*Math.cos(a)};}
 function local(p,x,y){const dx=x-p.x,dy=y-p.y,a=p.heading;return[dx*Math.cos(a)+dy*Math.sin(a),-dx*Math.sin(a)+dy*Math.cos(a)];}
 const hull=p=>C.ship.hullPolygon.map(([u,v])=>world(p,u,v));
 const muzzles=p=>C.ship.turretStations.map(u=>world(p,u,C.ship.muzzleStarboardOffset));
 const starboard=p=>({x:-Math.sin(p.heading),y:Math.cos(p.heading)});
 function fireWindow(p){if(C.volley.holdDuringTurns&&p.leg.endsWith('Turn'))return false;const s=starboard(p),l=C.land;return muzzles(p).every(m=>intersect(m.x,m.y,s.x*2000,s.y*2000,{x:l.left,y:l.top,width:l.right-l.left,height:l.bottom-l.top})!==null);}
 return{lengths,routeLength,poseAtDistance,pose,world,local,hull,muzzles,starboard,fireWindow};
}
