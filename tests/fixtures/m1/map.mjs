export const BREAKTHROUGH = Object.freeze({
  bounds:Object.freeze({left:192,right:576,top:0,bottom:768}),
  exit:Object.freeze({left:320,right:448,top:0,bottom:96}),
  tank:Object.freeze({x:384,y:672,facing:'up'}),
  crowd:Object.freeze({x:384,y:704}), deadline:90, speed:48, radius:16, spacing:32,
});
export function missionWalls(){return [
  {id:100,x:192,y:128,kind:'steel'}, {id:0,x:320,y:128,kind:'brick'},
  {id:101,x:448,y:128,kind:'steel'}, {id:1,x:192,y:384,kind:'brick'},
  {id:102,x:320,y:384,kind:'steel'}, {id:2,x:448,y:384,kind:'brick'},
].map(w=>({...w,width:128,height:128}));}
export const CROWD_DOTS=Object.freeze([[-8,-8],[0,-11],[8,-8],[-11,0],[-4,-3],[4,-3],[11,0],[-8,8],[0,11],[8,8],[-4,4],[4,4]].map(p=>Object.freeze(p)));
