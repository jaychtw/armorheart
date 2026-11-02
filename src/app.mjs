import {createState,step,recoil,ANGLES,VECTORS,WORLD,normalizeSettings} from './engine.mjs';
import {messages} from './i18n.mjs';
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
let storageFailed=false,settings;
try{settings=normalizeSettings(JSON.parse(localStorage.getItem('armorheart-guardian-settings')));}catch{settings=normalizeSettings(null);storageFailed=true;}
const mq=matchMedia('(prefers-reduced-motion: reduce)');
let reduced=()=>settings.reduced??mq.matches;
let state=createState(),started=false,paused=false,exploded=false,size=64,accumulator=0,last=0;
const held=new Map(),pointers=new Map();let order=0,fireKey=false;
const arena=$('#arena'),ctx=arena.getContext('2d'),asset=$('#asset-view'),ax=asset.getContext('2d');
const images=await Promise.all(['hull','barrel'].map(name=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=reject;im.src=`assets/guardian/${name}.svg`;})));
function save(){try{localStorage.setItem('armorheart-guardian-settings',JSON.stringify(settings));storageFailed=false;}catch{storageFailed=true;}$('#storage-warning').hidden=!storageFailed;$('#storage-warning').textContent=t('storage');}
function t(key){return messages[settings.language][key]??key;}
function translate(){
 document.documentElement.lang=settings.language;
 $$('[data-i18n]').forEach(el=>el.textContent=t(el.dataset.i18n));
 $$('[data-label]').forEach(el=>el.setAttribute('aria-label',t(el.dataset.label)));
 arena.setAttribute('aria-label',t('canvas'));$('#asset-view').setAttribute('aria-label',t('assetText'));
 $('.dpad').setAttribute('aria-label',t('facing'));$('.sizes').setAttribute('aria-label',t('scale'));
 $('#sound').textContent=t(settings.muted?'mute':'sound');$('#sound').setAttribute('aria-pressed',String(!settings.muted));
 $('#motion').checked=reduced();$('#pause').textContent=t(paused?'resume':'pause');
 $('#asset-note').textContent=t(exploded?'layersNote':'art');$('#storage-warning').textContent=t('storage');$('#storage-warning').hidden=!storageFailed;
 updateOverlay();drawComparisons();updateStats();
}
function updateOverlay(){
 const overlay=$('#overlay');overlay.hidden=started&&!paused&&!state.complete;
 if(state.complete){$('#overlay-title').textContent=t('success');$('#overlay-text').textContent=t('successText');$('#start').textContent=t('reset');}
 else if(started){$('#overlay-title').textContent=t('paused');$('#overlay-text').textContent=t('pausedText');$('#start').textContent=t('resume');}
 else{$('#overlay-title').textContent='GUARDIAN';$('#overlay-text').textContent=t('objective');$('#start').textContent=t('start');}
}
function clearInput(){held.clear();pointers.clear();fireKey=false;$$('.active').forEach(e=>e.classList.remove('active'));}
function reset(){state=createState();started=true;paused=false;particles=[];clearInput();$('#pause').disabled=false;updateOverlay();updateStats();arena.focus({preventScroll:true});}
function setPaused(value){paused=value;clearInput();$('#pause').textContent=t(paused?'resume':'pause');updateOverlay();}
$('#start').onclick=()=>{if(state.complete)reset();else{started=true;setPaused(false);$('#pause').disabled=false;arena.focus({preventScroll:true});arena.scrollIntoView({block:'start',behavior:'instant'});}};
$('#pause').onclick=()=>{setPaused(!paused);if(!paused)arena.focus({preventScroll:true});};
$('#restart').onclick=()=>{clearInput();if(started&&!state.complete){setPaused(true);$('#reset-dialog').showModal();}else reset();};
$('#cancel-reset').onclick=()=>{$('#reset-dialog').close();setPaused(false);};
$('#confirm-reset').onclick=()=>{$('#reset-dialog').close();reset();};
$('#reset-dialog').addEventListener('cancel',()=>setPaused(false));
$('#language').onclick=()=>{settings.language=settings.language==='en'?'zh-TW':'en';save();translate();};
$('#motion').onchange=e=>{settings.reduced=e.target.checked;save();};
mq.addEventListener('change',()=>{$('#motion').checked=reduced();});
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
function events(){for(const e of state.events){if(e.type==='fire')sound('fire');if(e.type==='impact'){sound('impact');particles.push({x:e.x,y:e.y,age:0,brick:e.brick});}if(e.type==='complete'){clearInput();updateOverlay();$('#pause').disabled=true;$('#announcement').textContent=t('successText');$('#start').focus({preventScroll:true});}}}
function tank(c,x,y,scale,facing,age,split=false){
 c.save();c.translate(x,y);c.rotate(ANGLES[facing]);c.scale(scale,scale);
 if(split){c.save();c.translate(-10,22);c.drawImage(images[0],-107,-128);c.restore();c.save();c.translate(10,-34);c.drawImage(images[1],-107,-128);c.restore();}
 else{c.drawImage(images[0],-107,-128);c.drawImage(images[1],-107-recoil(age,reduced()),-128);}
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
function draw(){
 ctx.setTransform(arena.width/WORLD,0,0,arena.height/WORLD,0,0);
 ctx.clearRect(0,0,WORLD,WORLD);cFill('#53604a',0,0,WORLD,WORLD);
 for(let y=0;y<12;y++)for(let x=0;x<12;x++){const n=(x*17+y*31)%7;cFill(n<3?'#56634d':'#535f49',x*64,y*64,64,64);}
 ctx.strokeStyle='#d4d5b50e';ctx.lineWidth=1;ctx.beginPath();for(let v=0;v<=WORLD;v+=64){ctx.moveTo(v,0);ctx.lineTo(v,WORLD);ctx.moveTo(0,v);ctx.lineTo(WORLD,v);}ctx.stroke();
 // Non-colliding ground markings, deliberately subordinate to wall geometry.
 ctx.strokeStyle='#d9d5ac32';ctx.lineWidth=2;ctx.setLineDash([9,12]);ctx.strokeRect(22,22,724,724);ctx.setLineDash([]);
 ctx.fillStyle='#dee0c33a';ctx.font='10px monospace';for(let x=0;x<12;x++)ctx.fillText(String(x+1).padStart(2,'0'),x*64+8,15);
 for(const w of state.walls){if(w.kind==='brick')brick(w);else{cFill('#2c3e34',w.x+1,w.y+4,62,61);cFill('#6b7864',w.x+1,w.y+1,62,59);cFill('#34483b',w.x+5,w.y+5,54,51);ctx.strokeStyle='#79866c';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(w.x+10,w.y+10);ctx.lineTo(w.x+54,w.y+50);ctx.moveTo(w.x+54,w.y+10);ctx.lineTo(w.x+10,w.y+50);ctx.stroke();for(const [dx,dy]of [[8,8],[56,8],[8,54],[56,54]])cFill('#b4b99b',w.x+dx-1,w.y+dy-1,3,3);}}
 for(const p of particles){const progress=p.age/.5;if(progress>=1)continue;ctx.save();ctx.globalAlpha=1-progress;ctx.fillStyle=p.brick?'#e6c88e':'#f9d99a';const count=reduced()?3:9;for(let i=0;i<count;i++){const a=i*2.399,dist=progress*(18+i*3);ctx.fillRect(p.x+Math.cos(a)*dist-2,p.y+Math.sin(a)*dist-2,4,4);}ctx.restore();}
 for(const b of state.shells){ctx.save();ctx.translate(b.x,b.y);ctx.rotate(Math.atan2(b.dy,b.dx));cFill('#f5e5b2',-7,-2,14,4);ctx.restore();}
 tank(ctx,state.tank.x,state.tank.y,.5,state.tank.facing,state.time-state.firedAt);
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
 // Static inspection renderer uses the same two SVGs and pivot as gameplay.
 ax.clearRect(0,0,600,400);tank(ax,280,218,.92,'up',state.time-state.firedAt,exploded);
}
function updateStats(){$('#shot-count').textContent=state.shots;$('#wall-count').innerHTML=`${state.destroyed} <small>/ 6</small>`;const ready=state.time+1e-8>=state.nextShot;$('#reload-label').textContent=t(ready?'ready':'cooldown');$('#reload-fill').style.width=Math.min(1,Math.max(0,1-(state.nextShot-state.time)))*100+'%';$('#facing-label').textContent=t('facing')+' / '+t(state.tank.facing+'Name');}
function frame(now){const elapsed=last?Math.min((now-last)/1000,.1):0;last=now;if(started&&!paused&&!state.complete){accumulator+=elapsed;while(accumulator>=1/60){step(state,input(),1/60);events();for(const p of particles)p.age+=1/60;particles=particles.filter(p=>p.age<.5);accumulator-=1/60;if(state.complete)break;}}else accumulator=0;draw();updateStats();requestAnimationFrame(frame);}
new ResizeObserver(()=>{const pixels=Math.round(arena.getBoundingClientRect().width*Math.min(devicePixelRatio||1,2));if(pixels>0){arena.width=pixels;arena.height=pixels;}}).observe(arena);
translate();requestAnimationFrame(frame);
// Read-only diagnostics for reproducible evidence; gameplay tests use actual inputs.
Object.defineProperty(window,'guardianPOC',{value:Object.freeze({snapshot:()=>structuredClone({state,started,paused,settings,reduced:reduced(),exploded,size,barrelOffsetMasterPx:recoil(state.time-state.firedAt,reduced())}),assetAnchors:{hull:[107,128],muzzle:[243,126],scale:.5}})});
