import {createState,step,recoil,ANGLES,VECTORS,WORLD,normalizeSettings} from './engine.mjs';
import {createMission,refreshRoute,advanceMission,missionSnapshot,truckRenderHeading} from './breakthrough.mjs';
import {BREAKTHROUGH} from './maps/breakthrough.mjs';
import {createColossus,stepColossus,bossRender,bossStage,COLOSSUS_SPRITES} from './colossus.mjs';
import {createInterception,stepInterception,shipRender,shipStage,shipStatus,shipCharge,SHIP_ROUTE} from './interception.mjs';
import {INTERCEPTION} from './maps/interception.mjs';
import {messages} from './i18n.mjs';
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
let storageFailed=false,settings;
try{settings=normalizeSettings(JSON.parse(localStorage.getItem('armorheart-guardian-settings')));}catch{settings=normalizeSettings(null);storageFailed=true;}
const mq=matchMedia('(prefers-reduced-motion: reduce)');
let reduced=()=>settings.reduced??mq.matches;
let scene='range',dialogAction='reset',dialogWasPaused=false,announcementKey=null;
let state=createState(),started=false,paused=false,exploded=false,size=64,accumulator=0,last=0;
const held=new Map(),pointers=new Map();let order=0,fireKey=false;
const arena=$('#arena'),ctx=arena.getContext('2d'),asset=$('#asset-view'),ax=asset.getContext('2d');
const images=await Promise.all(['hull','barrel'].map(name=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=reject;im.src=`assets/guardian/${name}.svg`;})));
const truckImage=await new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=reject;im.src='assets/transport/transport.svg';});
const bossImages=Object.fromEntries(await Promise.all(COLOSSUS_SPRITES.keys.map(name=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve([name,im]);im.onerror=reject;im.src=`assets/colossus/frames/${name}.png`;}))));
const shipImage=await new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=reject;im.src='assets/battleship/battleship.png';});
function save(){try{localStorage.setItem('armorheart-guardian-settings',JSON.stringify(settings));storageFailed=false;}catch{storageFailed=true;}$('#storage-warning').hidden=!storageFailed;$('#storage-warning').textContent=t('storage');}
function t(key){return (messages[settings.language][key]??key).replace('{boss}',String(state.colossus?.bossHP??4)).replace('{tank}',String(state.interception?.tankHP??state.colossus?.tankHP??3)).replace('{ship}',String(state.interception?.shipHP??6)).replace('{next}',state.colossus?(messages[settings.language]['stop'+bossRender(state).next.id]??''):'');}
function announce(key){announcementKey=key;$('#announcement').textContent=t(key);}
function translate(){
 document.documentElement.lang=settings.language;
 $$('[data-i18n]').forEach(el=>el.textContent=t(el.dataset.i18n));
 $$('[data-label]').forEach(el=>el.setAttribute('aria-label',t(el.dataset.label)));
 arena.setAttribute('aria-label',t(isInterception()?'shipCanvas':isColossus()?'bossCanvas':isMission()?'missionCanvas':'canvas'));$('#asset-view').setAttribute('aria-label',t('assetText'));
 $('.dpad').setAttribute('aria-label',t('facing'));$('.sizes').setAttribute('aria-label',t('scale'));
 $('#sound').textContent=t(settings.muted?'mute':'sound');$('#sound').setAttribute('aria-pressed',String(!settings.muted));
 $('#boss-sound').textContent=settings.muted?'♩':'♪';$('#boss-sound').setAttribute('aria-label',t(settings.muted?'mute':'sound'));$('#boss-sound').setAttribute('aria-pressed',String(!settings.muted));$('#boss-motion').textContent='≈';$('#boss-motion').setAttribute('aria-label',t('motion'));$('#boss-motion').setAttribute('aria-pressed',String(reduced()));
 $('#motion').checked=reduced();$('#pause').textContent=t(paused?'resume':'pause');
 $('#asset-note').textContent=t(exploded?'layersNote':'art');$('#storage-warning').textContent=t('storage');$('#storage-warning').hidden=!storageFailed;
 if(announcementKey&&$('#announcement').textContent!==t(announcementKey))$('#announcement').textContent=t(announcementKey);
 updateSceneText();updateOverlay();drawComparisons();updateStats();draw();
}
function isBreakthrough(){return scene==='breakthrough';}
function isColossus(){return scene==='colossus';}
function isInterception(){return scene==='interception';}
function isCombat(){return isColossus()||isInterception();}
function isMission(){return scene!=='range';}
function freshScene(){return isInterception()?createInterception():isColossus()?createColossus():isBreakthrough()?createMission():createState();}
function updateSceneText(){
 document.body.classList.toggle('mission',isMission());$('#mission-hud').hidden=!isBreakthrough();$('#boss-hud').hidden=!isCombat();$('.boss-settings').hidden=!isCombat();document.body.classList.toggle('boss-mode',isCombat());$('#level-exit').hidden=!isMission();
 $('#choose-range').setAttribute('aria-pressed',String(!isMission()));$('#choose-mission').setAttribute('aria-pressed',String(isBreakthrough()));$('#choose-colossus').setAttribute('aria-pressed',String(isColossus()));$('#choose-ship').setAttribute('aria-pressed',String(isInterception()));$('#target-health-label').textContent=t(isInterception()?'shipHealth':'bossHealth');
 $('#range-title').textContent=t(isInterception()?'shipTitle':isColossus()?'bossTitle':isMission()?'missionTitle':'range');$('.panel-header p').textContent=t(isInterception()?'shipSub':isColossus()?'bossSub':isMission()?'missionSub':'rangeSub');
 $('#objective').textContent=t(isInterception()?'shipObjective':isColossus()?'bossObjective':isMission()?'missionObjective':'objective');$('.site-footer p').textContent=t(isInterception()?'shipFooter':isColossus()?'bossFooter':isMission()?'missionFooter':'footer');
 $('#reset-dialog p').textContent=t(dialogAction==='reset'?(isInterception()?'shipRestartConfirm':isColossus()?'bossRestartConfirm':isMission()?'missionRestartConfirm':'restartConfirm'):'exitConfirm');
 $('#restart').textContent=t(isMission()?'missionRetry':'reset');
}
function updateOverlay(){
 const overlay=$('#overlay');overlay.hidden=started&&!paused&&!state.complete;
 if(isInterception()){const m=state.interception;if(state.complete){const key=m.outcome==='success'?'shipVictory':m.outcome==='escaped'?'shipEscaped':'shipDefeat';$('#overlay-title').textContent=t(key);$('#overlay-text').textContent=t(key+'Text');$('#start').textContent=t(m.outcome==='success'?'missionReplay':'missionRetry');}else if(started){$('#overlay-title').textContent=t('paused');$('#overlay-text').textContent=t('pausedText');$('#start').textContent=t('resume');}else{$('#overlay-title').textContent=t('shipTitle');$('#overlay-text').textContent=t('shipObjective');$('#start').textContent=t('missionStart');}return;}
 if(state.complete){const won=isColossus()?state.colossus.outcome==='success':!isMission()||state.mission.phase==='success';$('#overlay-title').textContent=t(isColossus()?(won?'bossVictory':'bossDefeat'):isMission()?(won?'missionSuccess':'missionTimeout'):'success');$('#overlay-text').textContent=t(isColossus()?(won?'bossVictoryText':'bossDefeatText'):isMission()?(won?'missionSuccessText':'missionTimeoutText'):'successText');$('#start').textContent=t(isMission()?(won?'missionReplay':'missionRetry'):'reset');}
 else if(started){$('#overlay-title').textContent=t('paused');$('#overlay-text').textContent=t('pausedText');$('#start').textContent=t('resume');}
 else{$('#overlay-title').textContent=isColossus()?t('bossTitle'):isMission()?t('missionTitle'):'GUARDIAN';$('#overlay-text').textContent=t(isInterception()?'shipObjective':isColossus()?'bossObjective':isMission()?'missionObjective':'objective');$('#start').textContent=t(isMission()?'missionStart':'start');}
}
function selectScene(next){
 scene=next;state=freshScene();started=false;paused=false;particles=[];accumulator=0;clearInput();$('#pause').disabled=true;
 announcementKey=null;$('#announcement').textContent='';translate();$('#start').focus({preventScroll:true});
}
function confirmAction(action){dialogAction=action;dialogWasPaused=paused;setPaused(true);updateSceneText();$('#reset-dialog').showModal();}
function requestScene(next){if(started&&!state.complete)confirmAction(next);else selectScene(next);}
$('#choose-range').onclick=()=>requestScene('range');$('#choose-mission').onclick=()=>requestScene('breakthrough');$('#choose-colossus').onclick=()=>requestScene('colossus');$('#choose-ship').onclick=()=>requestScene('interception');
$('#level-exit').onclick=()=>{if(started&&!state.complete)confirmAction('exit');else selectScene('range');};
function clearInput(){held.clear();pointers.clear();fireKey=false;$$('.active').forEach(e=>e.classList.remove('active'));}
function reset(){announcementKey=null;$('#announcement').textContent='';state=freshScene();last=performance.now();accumulator=0;started=true;paused=false;particles=[];clearInput();$('#pause').disabled=false;updateOverlay();updateStats();arena.focus({preventScroll:true});}
function setPaused(value){if(isBreakthrough()){const now=performance.now();if(value&&started&&!paused&&!state.complete){advanceMission(state,Math.max(0,(now-last)/1000));if(state.complete)finishMission();}last=now;}else if(isCombat())last=performance.now();paused=value;clearInput();$('#pause').textContent=t(paused?'resume':'pause');updateOverlay();}
$('#start').onclick=()=>{if(state.complete)reset();else{started=true;setPaused(false);$('#pause').disabled=false;arena.focus({preventScroll:true});(isInterception()?$('.panel-header'):isCombat()?$('#boss-hud'):arena).scrollIntoView({block:'start',behavior:'instant'});}};
$('#pause').onclick=()=>{setPaused(!paused);if(!paused)arena.focus({preventScroll:true});};
$('#restart').onclick=()=>{clearInput();if(started&&!state.complete)confirmAction('reset');else reset();};
$('#cancel-reset').onclick=()=>{$('#reset-dialog').close();setPaused(dialogWasPaused);arena.focus({preventScroll:true});};
$('#confirm-reset').onclick=()=>{$('#reset-dialog').close();if(dialogAction==='reset')reset();else selectScene(dialogAction==='exit'?'range':dialogAction);};
$('#reset-dialog').addEventListener('cancel',()=>setPaused(dialogWasPaused));
$('#language').onclick=()=>{settings.language=settings.language==='en'?'zh-TW':'en';save();translate();};
$('#motion').onchange=e=>{settings.reduced=e.target.checked;save();};
mq.addEventListener('change',()=>{$('#motion').checked=reduced();$('#boss-motion').setAttribute('aria-pressed',String(reduced()));});
$('#boss-sound').onclick=()=>$('#sound').click();$('#boss-motion').onclick=()=>{settings.reduced=!reduced();save();translate();};
$('#sound').onclick=()=>{settings.muted=!settings.muted;save();if(!settings.muted)ensureAudio();translate();};
for(const id of ['assembled','layers'])$('#'+id).onclick=()=>{exploded=id==='layers';$('#assembled').setAttribute('aria-pressed',String(!exploded));$('#layers').setAttribute('aria-pressed',String(exploded));$('#asset-note').textContent=t(exploded?'layersNote':'art');};
$$('[data-size]').forEach(b=>b.onclick=()=>{size=Number(b.dataset.size);$$('[data-size]').forEach(el=>el.setAttribute('aria-pressed',String(el===b)));drawComparisons();});
const keyDirections={ArrowUp:'up',ArrowDown:'down',ArrowLeft:'left',ArrowRight:'right',w:'up',s:'down',a:'left',d:'right'};
function hasGameFocus(){return document.activeElement===arena||document.activeElement===$('#fire')||document.activeElement?.hasAttribute('data-dir');}
window.addEventListener('keydown',e=>{
 if(!started||!hasGameFocus())return;
 const direction=keyDirections[e.key]??keyDirections[e.key.toLowerCase()];
 if(direction||e.code==='Space'){e.preventDefault();if(paused||state.complete)return;if(!e.repeat){if(direction)held.set(e.code,{direction,order:++order});else fireKey=true;}}
 if(e.code==='Escape'&&!state.complete)setPaused(!paused);
});
window.addEventListener('keyup',e=>{held.delete(e.code);if(e.code==='Space')fireKey=false;});
window.addEventListener('blur',()=>{if(started&&!state.complete)setPaused(true);});
document.addEventListener('visibilitychange',()=>{if(document.hidden&&started&&!state.complete)setPaused(true);});
$$('[data-dir],#fire').forEach(b=>{
 b.addEventListener('pointerdown',e=>{if(!started||paused||state.complete)return;e.preventDefault();b.setPointerCapture(e.pointerId);pointers.set(e.pointerId,{direction:b.dataset.dir??null,order:++order});b.classList.add('active');arena.focus({preventScroll:true});});
 b.addEventListener('pointermove',e=>{const old=pointers.get(e.pointerId);if(!old?.direction)return;const under=document.elementFromPoint(e.clientX,e.clientY)?.closest('[data-dir]');if(under&&old.direction!==under.dataset.dir){old.direction=under.dataset.dir;old.order=++order;}});
 for(const event of ['pointerup','pointercancel','lostpointercapture'])b.addEventListener(event,e=>{pointers.delete(e.pointerId);b.classList.remove('active');});
});
function input(){const dirs=[...held.values(),...[...pointers.values()].filter(x=>x.direction)].sort((a,b)=>b.order-a.order);return {direction:dirs[0]?.direction,fire:fireKey||[...pointers.values()].some(x=>!x.direction)};}
let audio;
function ensureAudio(){try{audio??=new AudioContext();audio.resume().catch(()=>{});}catch{}}
function sound(kind){if(settings.muted)return;ensureAudio();if(!audio)return;const osc=audio.createOscillator(),gain=audio.createGain();osc.type='triangle';osc.frequency.setValueAtTime(kind==='fire'?125:65,audio.currentTime);osc.frequency.exponentialRampToValueAtTime(35,audio.currentTime+.12);gain.gain.setValueAtTime(.07,audio.currentTime);gain.gain.exponentialRampToValueAtTime(.001,audio.currentTime+.15);osc.connect(gain);gain.connect(audio.destination);osc.start();osc.stop(audio.currentTime+.16);}
let particles=[];
function events(){for(const e of state.events){if(e.type==='fire')sound('fire');if(e.type==='impact'){sound('impact');particles.push({x:e.x,y:e.y,age:0,brick:e.brick});}if(e.type==='shipHit')announce('shipHitStatus');if(e.type==='shipVolley'){sound('fire');announce('shipVolleyStatus');}if(e.type==='interceptionComplete'){clearInput();updateOverlay();$('#pause').disabled=true;announce(state.interception.outcome==='success'?'shipVictoryText':state.interception.outcome==='escaped'?'shipEscapedText':'shipDefeatText');$('#start').focus({preventScroll:true});}if(e.type==='bossHit')announce('bossHitStatus');if(e.type==='tankHit')announce('tankHitStatus');if(e.type==='bossLanding')announce('bossLandingStatus');if(e.type==='colossusComplete'){clearInput();updateOverlay();$('#pause').disabled=true;announce(state.colossus.outcome==='success'?'bossVictoryText':'bossDefeatText');$('#start').focus({preventScroll:true});}if(e.type==='complete'){clearInput();updateOverlay();$('#pause').disabled=true;announce('successText');$('#start').focus({preventScroll:true});}}}
function tank(c,x,y,scale,facing,age,split=false){
 c.save();c.translate(x,y);c.rotate(ANGLES[facing]);c.scale(scale,scale);
 if(split){c.save();c.translate(-10,22);c.drawImage(images[0],-107,-128);c.restore();c.save();c.translate(10,-34);c.drawImage(images[1],-107,-128);c.restore();}
 // Fixed turret covers the sliding mount; the barrel transform is unchanged.
 else{c.drawImage(images[1],-107-recoil(age,reduced()),-128);c.drawImage(images[0],-107,-128);}
 c.restore();
}
function drawComparisons(){const root=$('#facings');root.replaceChildren();root.style.gridTemplateColumns=`repeat(auto-fit,minmax(${size}px,1fr))`;const dpr=Math.min(devicePixelRatio||1,2);
 for(const facing of ['up','right','down','left']){const wrap=document.createElement('div');wrap.className='facing-item';const c=document.createElement('canvas');c.width=size*dpr;c.height=size*dpr;c.style.width=size+'px';c.style.height=size+'px';const context=c.getContext('2d');context.scale(dpr,dpr);
 // Identical square canvas and hull anchors for each facing; fit the protruding barrel.
 const angle=ANGLES[facing],scale=size/256;
 tank(context,size/2-Math.cos(angle)*21*scale,size/2-Math.sin(angle)*21*scale,scale,facing,100);
 const label=document.createElement('span');label.textContent=t(facing+'Name');wrap.append(c,label);root.append(wrap);}
}
function brick(w){const x=w.x,y=w.y;cFill('#504d3a',x+2,y+5,61,61);cFill('#ad9264',x+1,y+1,62,59);cFill('#c1aa7c',x+2,y+2,60,4);cFill('#776748',x+2,y+57,60,5);ctx.strokeStyle='#756344';ctx.lineWidth=2;ctx.beginPath();for(let r=1;r<4;r++){ctx.moveTo(x+2,y+r*15);ctx.lineTo(x+62,y+r*15);}for(let r=0;r<4;r++){for(let col=0;col<2;col++){const xx=x+16+col*31+(r%2?10:0);ctx.moveTo(xx,y+r*15+2);ctx.lineTo(xx,y+(r+1)*15-1);}}ctx.stroke();}
function cFill(color,x,y,w,h){ctx.fillStyle=color;ctx.fillRect(x,y,w,h);}
function drawWall(w){if(w.kind==='brick')brick(w);else{cFill('#2c3e34',w.x+1,w.y+4,62,61);cFill('#6b7864',w.x+1,w.y+1,62,59);cFill('#34483b',w.x+5,w.y+5,54,51);ctx.strokeStyle='#79866c';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(w.x+10,w.y+10);ctx.lineTo(w.x+54,w.y+50);ctx.moveTo(w.x+54,w.y+10);ctx.lineTo(w.x+10,w.y+50);ctx.stroke();for(const [dx,dy]of [[8,8],[56,8],[8,54],[56,54]])cFill('#b4b99b',w.x+dx-1,w.y+dy-1,3,3);}}
function draw(){
 ctx.setTransform(arena.width/WORLD,0,0,arena.height/WORLD,0,0);
 ctx.clearRect(0,0,WORLD,WORLD);cFill('#53604a',0,0,WORLD,WORLD);
 for(let y=0;y<12;y++)for(let x=0;x<12;x++){const n=(x*17+y*31)%7;cFill(n<3?'#56634d':'#535f49',x*64,y*64,64,64);}
 ctx.strokeStyle='#d4d5b50e';ctx.lineWidth=1;ctx.beginPath();for(let v=0;v<=WORLD;v+=64){ctx.moveTo(v,0);ctx.lineTo(v,WORLD);ctx.moveTo(0,v);ctx.lineTo(WORLD,v);}ctx.stroke();
 // Non-colliding ground markings, deliberately subordinate to wall geometry.
 ctx.strokeStyle='#d9d5ac32';ctx.lineWidth=2;ctx.setLineDash([9,12]);ctx.strokeRect(22,22,724,724);ctx.setLineDash([]);
 ctx.fillStyle='#dee0c33a';ctx.font='10px monospace';for(let x=0;x<12;x++)ctx.fillText(String(x+1).padStart(2,'0'),x*64+8,15);
 if(isBreakthrough())drawMissionGround();if(isColossus())drawBossGround();if(isInterception())drawSea();
 for(const w of state.walls){ctx.save();ctx.translate(w.x,w.y);ctx.scale((w.width??64)/64,(w.height??64)/64);drawWall({...w,x:0,y:0});ctx.restore();}
 for(const p of particles){const progress=p.age/.5;if(progress>=1)continue;ctx.save();ctx.globalAlpha=1-progress;ctx.fillStyle=p.brick?'#e6c88e':'#f9d99a';const count=reduced()?3:9;for(let i=0;i<count;i++){const a=i*2.399,dist=progress*(18+i*3);ctx.fillRect(p.x+Math.cos(a)*dist-2,p.y+Math.sin(a)*dist-2,4,4);}ctx.restore();}
 for(const b of state.shells){ctx.save();ctx.translate(b.x,b.y);ctx.rotate(Math.atan2(b.dy,b.dx));cFill('#f5e5b2',-7,-2,14,4);ctx.restore();}
 if(isInterception()){drawShip();drawEnemyShells();}
 if(isColossus()&&state.tank.y>=bossRender(state).y)drawBoss();
 ctx.save();const healthState=isInterception()?state.interception:isColossus()?state.colossus:null;if(healthState&&healthState.immuneUntil>healthState.elapsed)ctx.globalAlpha=reduced()?.7:.72+.28*Math.cos(healthState.elapsed*Math.PI*2)**2;
 tank(ctx,state.tank.x,state.tank.y,.5,state.tank.facing,state.time-state.firedAt);
 ctx.restore();
 const flashAge=state.time-state.firedAt;
 if(flashAge>=0&&flashAge<.09){
   const [dx,dy]=VECTORS[state.tank.facing],offset=recoil(flashAge,reduced())*.5;
   ctx.save();ctx.translate(state.tank.x+dx*(68-offset)+dy,state.tank.y+dy*(68-offset)-dx);
   ctx.rotate(ANGLES[state.tank.facing]);
   const life=1-flashAge/.09;ctx.globalAlpha=.65+.35*life;
   const glow=ctx.createRadialGradient(22,0,1,22,0,34);
   glow.addColorStop(0,'#ffdc7ac0');glow.addColorStop(.45,'#ffad3438');glow.addColorStop(1,'#ff7b1700');
   ctx.fillStyle=glow;ctx.fillRect(0,-34,58,68);
   // Narrow connected root, directed jet and irregular warm forward bloom.
   const flame=ctx.createLinearGradient(0,0,52,0);
   flame.addColorStop(0,'#fffde5');flame.addColorStop(.35,'#fff3a2');flame.addColorStop(.7,'#ffc14f');flame.addColorStop(1,'#f07822aa');
   ctx.fillStyle=flame;ctx.beginPath();ctx.moveTo(0,-1.4);
   for(const [x,y] of [[12,-3],[20,-10],[25,-8],[31,-16],[34,-10],[43,-13],[41,-5],[52,-2],[44,3],[47,10],[38,9],[34,16],[28,11],[21,12],[16,5],[0,1.4]])ctx.lineTo(x,y);
   ctx.closePath();ctx.fill();
   ctx.fillStyle='#fffde9';ctx.beginPath();ctx.moveTo(0,-.8);ctx.lineTo(18,-2);ctx.lineTo(31,-6);ctx.lineTo(29,-1);ctx.lineTo(43,0);ctx.lineTo(29,3);ctx.lineTo(23,6);ctx.lineTo(17,2);ctx.lineTo(0,.8);ctx.closePath();ctx.fill();ctx.restore();
 }
 if(isBreakthrough())drawTransport();if(isColossus()&&state.tank.y<bossRender(state).y){drawBoss();const p=bossRender(state);if(Math.abs(state.tank.x-p.x)<150&&Math.abs(state.tank.y-p.y)<230){ctx.save();ctx.globalAlpha=.45;tank(ctx,state.tank.x,state.tank.y,.5,state.tank.facing,state.time-state.firedAt);ctx.restore();}}
 // Static inspection renderer uses the same two SVGs and pivot as gameplay.
 ax.clearRect(0,0,600,400);tank(ax,280,218,.92,'up',state.time-state.firedAt,exploded);
}
function drawSea(){
 cFill('#294e5d',0,0,768,768);ctx.strokeStyle='#78999b25';ctx.lineWidth=1;ctx.beginPath();for(let y=20;y<768;y+=64)for(let x=4;x<768;x+=64){ctx.moveTo(x,y);ctx.lineTo(x+22,y);}ctx.stroke();
 const l=INTERCEPTION.land;cFill('#55644c',l.left,l.top,l.right-l.left,768-l.top);for(let y=l.top;y<768;y+=32)for(let x=l.left;x<l.right;x+=32)if(((x-l.left+y-l.top)/32)%2===0)cFill('#5b6a50',x,y,32,Math.min(32,768-y));cFill('#c8bd92',l.left,l.top,l.right-l.left,6);cFill('#c8bd92',l.left,l.top,6,768-l.top);cFill('#c8bd92',l.right-6,l.top,6,768-l.top);
}
function drawEnemyShells(){for(const b of state.interception.enemyShells){ctx.save();if(!reduced()){ctx.strokeStyle='#e6c58388';ctx.lineWidth=1.6;ctx.beginPath();ctx.moveTo(b.x-b.dx*10,b.y-b.dy*10);ctx.lineTo(b.x,b.y);ctx.stroke();}ctx.fillStyle='#f6d08a';ctx.strokeStyle='#273d30';ctx.lineWidth=1;ctx.beginPath();ctx.arc(b.x,b.y,4,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.restore();}}
function drawShip(){
 const m=state.interception,p=shipRender(state),charge=shipCharge(state);ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.heading);if(!m.shipHP)ctx.globalAlpha=.65;ctx.drawImage(shipImage,-166,-54,332,130);
 for(const x of INTERCEPTION.ship.turretStations){if(shipStatus(state)==='charging'){ctx.fillStyle=`rgba(255,213,114,${.3+.5*charge})`;ctx.beginPath();ctx.ellipse(x,62,5,8,0,0,Math.PI*2);ctx.fill();}const age=m.elapsed-m.lastVolleyAt;if(age>=0&&age<.09){ctx.save();ctx.translate(x,66);ctx.globalAlpha=.9;ctx.fillStyle='#ffe3a3';ctx.beginPath();ctx.moveTo(-2,0);ctx.lineTo(-6,13);ctx.lineTo(-3,19);ctx.lineTo(0,31);ctx.lineTo(4,17);ctx.lineTo(7,10);ctx.lineTo(2,0);ctx.closePath();ctx.fill();ctx.restore();}}
 ctx.restore();const stage=shipStage(m.shipHP);if(stage==='smoking'||stage==='onFire'){const anchors=stage==='onFire'?[[-42,-6],[42,-5]]:[[-42,-6]];for(const [i,a]of anchors.entries()){const q=SHIP_ROUTE.world(p,...a),time=reduced()?1.2:m.elapsed;ctx.save();for(let n=0;n<4;n++){const f=(time*.55+n*.24)%1;ctx.fillStyle=`rgba(40,43,36,${.3*(1-f)})`;ctx.beginPath();ctx.arc(q.x+Math.sin(n*2.1+time)*4,q.y-6-f*32,5+f*7,0,Math.PI*2);ctx.fill();}if(stage==='onFire'){ctx.translate(q.x,q.y);ctx.fillStyle='#ed9b41';ctx.beginPath();ctx.moveTo(-5,3);ctx.lineTo(-7,-8);ctx.lineTo(-2,-5);ctx.lineTo(1,-18-(reduced()?0:Math.sin(time*5+i)*2));ctx.lineTo(6,-8);ctx.lineTo(5,3);ctx.closePath();ctx.fill();ctx.fillStyle='#ffe1a2';ctx.beginPath();ctx.moveTo(-2,2);ctx.lineTo(0,-10);ctx.lineTo(3,2);ctx.fill();}ctx.restore();}}
}
function drawBossGround(){
 const p=bossRender(state);ctx.save();ctx.fillStyle='#122a2355';ctx.beginPath();ctx.ellipse(p.x,p.y,112*(1-p.z/256),64*(1-p.z/256),0,0,Math.PI*2);ctx.fill();ctx.restore();
}
function drawBoss(){const p=bossRender(state);ctx.save();if(state.colossus.bossHP===0)ctx.globalAlpha=.6;ctx.drawImage(bossImages[p.view+'_'+p.pose],p.x-COLOSSUS_SPRITES.anchor[0],p.y-COLOSSUS_SPRITES.anchor[1]-p.z,COLOSSUS_SPRITES.size,COLOSSUS_SPRITES.size);ctx.restore();}
function drawMissionGround(){
 cFill('#273a31',0,0,192,WORLD);cFill('#273a31',576,0,192,WORLD);
 ctx.strokeStyle='#8f9b76';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(192,0);ctx.lineTo(192,768);ctx.moveTo(576,0);ctx.lineTo(576,768);ctx.stroke();
 for(let y=24;y<768;y+=64){cFill('#5c6c50',172,y,12,24);cFill('#5c6c50',584,y,12,24);}
 const e=BREAKTHROUGH.exit;cFill('#294e41',e.left,e.top,e.right-e.left,e.bottom-e.top);
 ctx.strokeStyle='#f2ebbb';ctx.lineWidth=3;ctx.strokeRect(e.left+4,e.top+4,e.right-e.left-8,e.bottom-e.top-8);
 ctx.fillStyle='#fff5cc';ctx.font='bold 22px system-ui';ctx.textAlign='center';ctx.fillText(t('exitMark'),384,45);ctx.textAlign='start';
}
function drawTransport(){
 const m=state.mission,truck=m.truck;ctx.save();ctx.translate(truck.x,truck.y);ctx.rotate((truckRenderHeading(truck)-1)*Math.PI/2);
 ctx.save();ctx.fillStyle='#13251b44';ctx.beginPath();ctx.ellipse(-1,4,64,27,0,0,Math.PI*2);ctx.fill();ctx.restore();
 ctx.drawImage(truckImage,-64,-28,128,56);
 ctx.restore();
 if(m.phase==='waiting'){ctx.fillStyle='#fff2c4';ctx.strokeStyle='#21372a';ctx.lineWidth=3;ctx.font='bold 20px system-ui';ctx.textAlign='center';ctx.strokeText(t('transportMark'),truck.x,truck.y+48);ctx.fillText(t('transportMark'),truck.x,truck.y+48);ctx.textAlign='start';}
}
function finishMission(){clearInput();updateOverlay();$('#pause').disabled=true;announce(state.mission.phase==='success'?'missionSuccessText':'missionTimeoutText');$('#start').focus({preventScroll:true});}
let lastShipAnnouncement=null;
function updateStats(){if(isInterception()){const m=state.interception,status=shipStatus(state);$('#tank-health').textContent=m.tankHP+' / 3';$('#boss-health').textContent=m.shipHP+' / 6';$('#boss-phase').textContent=t('shipStage'+shipStage(m.shipHP))+' · '+t('shipStatus'+status);$('#boss-immunity').textContent=m.immuneUntil>m.elapsed?t('bossProtected'):'';if(status!==lastShipAnnouncement){lastShipAnnouncement=status;if(status==='charging')announce('shipStatuscharging');}}if(isColossus()){const m=state.colossus;$('#tank-health').textContent=m.tankHP+' / 3';$('#boss-health').textContent=m.bossHP+' / 4';$('#boss-phase').textContent=t(m.outcome==='success'?'bossVictory':m.outcome==='defeat'?'bossDefeat':m.phase==='airborne'?'bossAirborne':'bossGrounded')+' · '+t('stage'+bossStage(m.bossHP));$('#boss-immunity').textContent=m.immuneUntil>m.elapsed?t('bossProtected'):'';}if(isBreakthrough()){const m=state.mission;$('#mission-clock').textContent=String(Math.ceil(Math.max(0,90-m.elapsed)));const status=t(m.phase==='success'?'missionSuccess':m.phase==='timeout'?'missionTimeout':m.phase==='evacuating'?'evacuating':'waiting');if($('#mission-status').textContent!==status)$('#mission-status').textContent=status;$('#mission-ready').textContent=t(state.time+1e-8>=state.nextShot?'ready':'cooldown');$('#mission-hud').classList.toggle('route-open',m.phase==='evacuating');}$('#shot-count').textContent=state.shots;$('#wall-count').innerHTML=`${state.destroyed} <small>/ 6</small>`;const ready=state.time+1e-8>=state.nextShot;$('#reload-label').textContent=t(ready?'ready':'cooldown');$('#reload-fill').style.width=Math.min(1,Math.max(0,1-(state.nextShot-state.time)))*100+'%';$('#facing-label').textContent=t('facing')+' / '+t(state.tank.facing+'Name');}
function frame(now){
 const rawElapsed=last?Math.max(0,(now-last)/1000):0,elapsed=Math.min(rawElapsed,.1);last=now;
 if(started&&!paused&&!state.complete){
   if(isBreakthrough()){advanceMission(state,rawElapsed);if(state.complete)finishMission();}
   if(!state.complete){accumulator+=elapsed;while(accumulator>=1/60){if(isInterception())stepInterception(state,input(),1/60);else if(isColossus())stepColossus(state,input(),1/60);else step(state,input(),1/60);events();for(const p of particles)p.age+=1/60;particles=particles.filter(p=>p.age<.5);accumulator-=1/60;if(state.complete)break;}
     if(isBreakthrough()&&refreshRoute(state)){announce('evacCue');}
   }
 }else accumulator=0;
 draw();updateStats();requestAnimationFrame(frame);
}
new ResizeObserver(()=>{const pixels=Math.round(arena.getBoundingClientRect().width*Math.min(devicePixelRatio||1,2));if(pixels>0&&arena.width!==pixels){arena.width=pixels;arena.height=pixels;draw();}}).observe(arena);
translate();requestAnimationFrame(frame);
// Read-only diagnostics for reproducible evidence; gameplay tests use actual inputs.
Object.defineProperty(window,'guardianPOC',{value:Object.freeze({snapshot:()=>structuredClone({scene,state:state.mission?{...state,mission:missionSnapshot(state)}:state,started,paused,settings,reduced:reduced(),exploded,size,barrelOffsetMasterPx:recoil(state.time-state.firedAt,reduced())}),shipVisual:()=>isInterception()?structuredClone({pose:shipRender(state),muzzles:SHIP_ROUTE.muzzles(shipRender(state)),stage:shipStage(state.interception.shipHP),status:shipStatus(state),charge:shipCharge(state)}):null,assetAnchors:{hull:[107,128],muzzle:[243,126],scale:.5}})});
