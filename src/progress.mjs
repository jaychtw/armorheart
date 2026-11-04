// Cosmetic collection and campaign persistence only; never imported by a rule adapter.
export const MISSIONS=Object.freeze(['breakthrough','colossus','interception','siege']);
export const TANKS=Object.freeze(['guardian','bulwark','vanguard','sentinel']);
export const PROGRESS_KEY='armorheart-progress';
export function normalizeProgress(value){
 const raw=value&&typeof value==='object'&&!Array.isArray(value)&&[0,1].includes(value.version)?value:{};
 const input=raw.version===0?raw.completedMissions:raw.completed;
 const completed=[];
 if(Array.isArray(input))for(const id of input.slice(0,128))if(MISSIONS.includes(id)&&!completed.includes(id))completed.push(id);
 const allowed=TANKS.slice(0,1+Math.min(3,completed.length));
 const selected=raw.version===0?raw.selectedTank:raw.selected;
 return {version:1,completed,selected:allowed.includes(selected)?selected:'guardian'};
}
export function unlockedTanks(progress){return TANKS.slice(0,1+Math.min(3,normalizeProgress(progress).completed.length));}
export function nextMission(id){const i=MISSIONS.indexOf(id);return i>=0&&i<3?MISSIONS[i+1]:null;}
export function recordVictory(progress,id){
 const state=normalizeProgress(progress);if(!MISSIONS.includes(id))return {state,first:false,unlocked:null,commendation:false};
 const first=!state.completed.includes(id);if(first)state.completed.push(id);
 return {state,first,unlocked:first&&state.completed.length<=3?TANKS[state.completed.length]:null,commendation:first&&state.completed.length===4};
}
export function selectTank(progress,id){const p=normalizeProgress(progress);if(unlockedTanks(p).includes(id))p.selected=id;return p;}
export function createProgressStore(provider=()=>globalThis.localStorage){
 let state=normalizeProgress(null),status='saved',readOnly=false,storage,phase='read';
 try{
  storage=provider();const raw=storage.getItem(PROGRESS_KEY);phase='parse';
  if(raw!==null){
   if(raw.length>8192)throw Error('Oversized save');const parsed=JSON.parse(raw);
   if(!parsed||typeof parsed!=='object'||Array.isArray(parsed)||![0,1].includes(parsed.version)){
    if(parsed&&typeof parsed.version==='number'&&parsed.version>1){status='newer';readOnly=true;}
    else throw Error('Invalid save schema');
   }else{state=normalizeProgress(parsed);if(parsed.version===0){phase='write';storage.setItem(PROGRESS_KEY,JSON.stringify(state));}}
  }
 }catch{status=phase==='parse'?'recovered':'session';}
 function persist(){if(readOnly)return;try{storage??=provider();storage.setItem(PROGRESS_KEY,JSON.stringify(state));status='saved';}catch{status='session';}}
 return Object.freeze({
  snapshot:()=>structuredClone(state),status:()=>status,
  victory(id){const reward=recordVictory(state,id);state=reward.state;if(reward.first)persist();return structuredClone(reward);},
  select(id){const previous=state.selected;state=selectTank(state,id);if(state.selected!==previous)persist();return state.selected;},
 });
}
