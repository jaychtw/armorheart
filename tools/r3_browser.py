"""R3 real-input/render evidence; snapshots read-only, no gameplay fixtures.
Loopback server :8080 required. Playwright controls time, not simulation state.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,time,os,math
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/os.environ.get('EVIDENCE_DIR','evidence/r3');OUT.mkdir(parents=True,exist_ok=True)
results=[];errors=[];requests=[];plays=[]
def check(name,ok,detail=None):
 results.append(dict(name=name,passed=bool(ok),detail=detail))
 if not ok:raise AssertionError((name,detail))
def snap(pg):return pg.evaluate('guardianPOC.snapshot()')
def mission(pg):return snap(pg)['state']['mission']
def capture(pg,name):pg.screenshot(path=str(OUT/(name+'.png')),full_page=True)
def ready(c,offline=False):
 pg=c.new_page();pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('request',lambda r:requests.append(r.url))
 pg.clock.install();url='http://127.0.0.1:8080'+('/preview/guardian.html' if offline else '/')
 if offline:pg.route('**/*',lambda r:r.continue_() if r.request.url==url else r.abort())
 pg.goto(url);pg.wait_for_function('window.guardianPOC');pg.clock.pause_at(int(time.time()*1000)+1000);pg.locator('#choose-mission').click();return pg
class Touch:
 def __init__(self,pg,c):self.pg=pg;self.cdp=c.new_cdp_session(pg)
 def start(self,key=None,fire=False):
  self.pg.locator('#fire').scroll_into_view_if_needed();selectors=[]
  if key:selectors.append('[data-dir="'+{'ArrowUp':'up','ArrowDown':'down','ArrowLeft':'left','ArrowRight':'right'}[key]+'"]')
  if fire:selectors.append('#fire')
  pts=[]
  for i,sel in enumerate(selectors):
   b=self.pg.locator(sel).bounding_box();pts.append(dict(x=b['x']+b['width']/2,y=b['y']+b['height']/2,id=i+1))
  self.cdp.send('Input.dispatchTouchEvent',dict(type='touchStart',touchPoints=pts))
 def end(self):self.cdp.send('Input.dispatchTouchEvent',dict(type='touchEnd',touchPoints=[]))
def face(pg,k,touch=None):
 pg.locator('#arena').focus()
 if touch:touch.start(k)
 else:pg.keyboard.down(k)
 pg.clock.run_for(64)
 if touch:touch.end()
 else:pg.keyboard.up(k)
def move(pg,k,axis,target,sign,touch=None):
 pg.locator('#arena').focus()
 if touch:touch.start(k)
 else:pg.keyboard.down(k)
 for i in range(250):
  pos=snap(pg)['state']['tank'][axis];d=(target-pos)*sign
  if d<=0:break
  pg.clock.run_for(100 if d>30 else 16)
 else:raise AssertionError(('movement blocked',axis,target,snap(pg)['state']['tank']))
 if touch:touch.end()
 else:pg.keyboard.up(k)
def fire_to(pg,cell,touch=None):
 if touch:touch.start(fire=True)
 else:pg.keyboard.down('Space')
 for i in range(100):
  if not any(w['id']==cell for w in snap(pg)['state']['walls']):break
  pg.clock.run_for(16)
 else:raise AssertionError(('fire blocked',cell,snap(pg)['state']))
 if touch:touch.end()
 else:pg.keyboard.up('Space')
def play(pg,shortcut,touch=None,prefix='keyboard-bypass',offline=False):
 if not snap(pg)['started'] or snap(pg)['paused'] or snap(pg)['state']['complete']:pg.locator('#start').click()
 if shortcut:
  move(pg,'ArrowLeft','x',320,-1,touch);face(pg,'ArrowUp',touch);fire_to(pg,'L1',touch)
  check(prefix+' one lower cell only',snap(pg)['state']['destroyed']==1 and any(w['id']=='L0' for w in snap(pg)['state']['walls']) and mission(pg)['phase']=='waiting')
  capture(pg,prefix+'-one-cell');fire_to(pg,'L0',touch);move(pg,'ArrowUp','y',400,-1,touch)
 else:move(pg,'ArrowUp','y',400,-1,touch)
 move(pg,'ArrowLeft','x',288,-1,touch);move(pg,'ArrowUp','y',160,-1,touch);face(pg,'ArrowRight',touch);fire_to(pg,'U0',touch)
 check(prefix+' one upper cell does not release truck',mission(pg)['phase']=='waiting' and mission(pg)['truck']['x']==272 and any(w['id']=='U1' for w in snap(pg)['state']['walls']))
 capture(pg,prefix+'-upper-partial');fire_to(pg,'U1',touch)
 m=mission(pg);expected=4 if shortcut else 2
 check(prefix+' correct cells and exact effective shots',snap(pg)['state']['destroyed']==expected and snap(pg)['state']['shots']==expected,dict(shots=snap(pg)['state']['shots'],destroyed=snap(pg)['state']['destroyed']))
 check(prefix+' localized departure cue',m['phase']=='evacuating' and pg.locator('#announcement').inner_text() in ['Route open. The transport is evacuating.','路線已暢通，運輸車開始撤離。'],pg.locator('#announcement').inner_text())
 check(prefix+' shortest route matches approved cost',abs(m['predictedRouteSeconds']-(14.7166666667 if shortcut else 22.0833333333))<1e-6 and m['routeDistance']==(656 if shortcut else 976) and m['routeTurns']==(3 if shortcut else 5),m['predictedRouteSeconds'])
 capture(pg,prefix+'-departure');before=m['elapsed'];pg.locator('#language').click()
 check(prefix+' live locale preserves mission',mission(pg)['elapsed']==before and mission(pg)['phase']=='evacuating');capture(pg,prefix+'-departure-other-language')
 # Inspect actual body raster while runtime drives and pivots. Never mutate it.
 turns=[];last=None;max_overlap=0
 for i in range(300):
  m=mission(pg)
  if m['phase']=='success':break
  a=m['truck']['action']
  if a and a['kind']!='forward' and a['from']!=last:
   last=a['from'];turns.append(dict(pose=last,kind=a['kind'],elapsed=m['elapsed']))
   if not offline:
    max_overlap=max(max_overlap,truck_pixels(pg)['overlap'])
   if len(turns)==1:
    pg.clock.run_for(100);capture(pg,prefix+'-pivot')
    if prefix=='keyboard-bypass':
     pg.locator('#pause').click();frozen=mission(pg);pg.clock.run_for(2000)
     check('pause freezes in-progress truck pivot and timer',mission(pg)==frozen)
     pg.locator('#start').click();pg.clock.run_for(16)
     check('resume pivot has no catch-up jump',mission(pg)['elapsed']-frozen['elapsed']<.05)
  pg.clock.run_for(100)
 else:raise AssertionError(('evacuation stuck',mission(pg)))
 m=mission(pg);check(prefix+' success before deadline',m['phase']=='success' and m['elapsed']<90 and snap(pg)['state']['complete'],m['elapsed'])
 t=m['truck'];check(prefix+' full visible body north inside exit',t['heading']==0 and t['x']-28>=320 and t['x']+28<=448 and t['y']-64>=0 and t['y']+64<=192,t)
 check(prefix+' all observed pivots have no visible wall overlap',max_overlap==0,dict(overlap=max_overlap,turns=turns))
 capture(pg,prefix+'-success');plays.append(dict(name=prefix,input='CDP touch' if touch else 'keyboard',shortcut=shortcut,offline=offline,elapsed=m['elapsed'],shots=snap(pg)['state']['shots'],destroyed=snap(pg)['state']['destroyed'],turns=turns))
 pg.locator('#start').click();check(prefix+' clean retry',mission(pg)['phase']=='waiting' and mission(pg)['elapsed']==0 and snap(pg)['state']['shots']==0 and len(snap(pg)['state']['walls'])==9)
def truck_pixels(pg):
 return pg.evaluate('''async()=>{const s=guardianPOC.snapshot().state,t=s.mission.truck,a=t.action;let h=t.heading;if(a&&a.kind!=='forward')h=a.from.heading+(a.kind==='left'?-1:1)*a.progress/a.duration;
 const c=document.createElement('canvas');c.width=c.height=768;const g=c.getContext('2d'),im=new Image();im.src='/assets/transport/transport.svg';await im.decode();g.translate(t.x,t.y);g.rotate((h-1)*Math.PI/2);g.drawImage(im,-64,-28,128,56);const d=g.getImageData(0,0,768,768).data;let overlap=0;
 for(const w of s.walls)for(let y=w.y+1;y<w.y+63;y++)for(let x=w.x+1;x<w.x+63;x++)if(d[(y*768+x)*4+3]>200)overlap++;return {overlap,heading:h};}''')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 c=b.new_context(viewport=dict(width=1440,height=1000));pg=ready(c);capture(pg,'desktop-entry');pg.clock.run_for(10000);check('entry does not spend timer',mission(pg)['elapsed']==0)
 # Actual source SVG raster extents and cardinal render plate (not gameplay).
 art=pg.evaluate('''async()=>{const im=new Image();im.src='/assets/transport/transport.svg';await im.decode();const c=document.createElement('canvas');c.width=256;c.height=112;const g=c.getContext('2d');g.drawImage(im,0,0);const d=g.getImageData(0,0,256,112).data;let l=256,r=-1,t=112,b=-1,count=0;for(let y=0;y<112;y++)for(let x=0;x<256;x++)if(d[(y*256+x)*4+3]){l=Math.min(l,x);r=Math.max(r,x);t=Math.min(t,y);b=Math.max(b,y);count++;}return {source:[256,112],alphaBounds:[l,t,r+1,b+1],opaquePixels:count,worldScale:.5,body:[128,56],padding:4,rotationCornerRadius:Math.hypot(68,32)};}''')
 check('actual SVG body fits and fills declared envelope',art['alphaBounds']==[0,0,256,112] and art['rotationCornerRadius']<76,art)
 (OUT/'art-footprint.json').write_text(json.dumps(art,indent=2)+'\n')
 plate=c.new_page();plate.goto('http://127.0.0.1:8080/');plate.set_content('''<body style="margin:24px;background:#56634c;color:#fff4ca;font:16px system-ui"><p>R3 original transport — artwork/envelope inspection, 4× display</p><canvas width="1200" height="650"></canvas></body>''')
 plate.evaluate('''async()=>{const im=new Image();im.src='/assets/transport/transport.svg';await im.decode();const g=document.querySelector('canvas').getContext('2d');for(let h=0;h<4;h++){g.save();g.translate(300+(h%2)*600,160+Math.floor(h/2)*320);g.scale(2,2);g.rotate((h-1)*Math.PI/2);g.drawImage(im,-64,-28,128,56);g.strokeStyle='#fff4c4';g.lineWidth=.5;g.strokeRect(-64,-28,128,56);g.setLineDash([2,2]);g.strokeStyle='#9be3dd';g.strokeRect(-68,-32,136,64);g.restore();g.fillText(['NORTH','EAST','SOUTH','WEST'][h],80+(h%2)*600,300+Math.floor(h/2)*320);}}''');plate.screenshot(path=str(OUT/'transport-four-facings.png'),full_page=True);plate.close()
 # Production ES modules tested in Chromium for all sixteen demolition masks.
 rows=pg.evaluate('''async()=>{const {missionWalls,BREAKTHROUGH:m}=await import('/src/maps/breakthrough.mjs'),{planTransport,transportPoseClear,transportSegmentClear,transportTurnClear}=await import('/src/transport.mjs');const all=missionWalls(),bricks=all.filter(w=>w.kind==='brick');return Array.from({length:16},(_,mask)=>{const walls=all.filter(w=>!bricks.some((b,i)=>b.id===w.id&&(mask>>i&1))),route=planTransport(walls,m.truck);return {mask,removed:bricks.filter((w,i)=>mask>>i&1).map(w=>w.id),reachable:route.reachable,seconds:route.seconds,distance:route.distance,turns:route.turns,clear:route.actions.every(a=>transportPoseClear(a.from,walls)&&transportPoseClear(a.to,walls)&&(a.kind==='forward'?transportSegmentClear(a.from,a.to,walls):transportTurnClear(a.from,walls)))};});}''')
 for row in rows:check('Chromium production planner mask '+str(row['mask']),row['reachable']==('U0' in row['removed'] and 'U1' in row['removed']) and row['clear'],row)
 (OUT/'browser-all16.json').write_text(json.dumps(rows,indent=2)+'\n')
 pg.locator('#start').click();pg.locator('#arena').focus();pg.keyboard.down('Space');pg.clock.run_for(2000);pg.keyboard.up('Space');check('spawn fire hits steel without route or damage',snap(pg)['state']['destroyed']==0 and mission(pg)['replans']==1)
 pg.locator('#pause').click();before=mission(pg)['elapsed'];pg.clock.run_for(5000);check('pause freezes timer',mission(pg)['elapsed']==before);pg.locator('#start').click();pg.clock.run_for(16);check('resume rebases real clock',mission(pg)['elapsed']-before<.1)
 pg.evaluate("Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'))");before=mission(pg)['elapsed'];pg.clock.run_for(5000);check('simulated hidden lifecycle pauses',snap(pg)['paused'] and mission(pg)['elapsed']==before)
 pg.evaluate("Object.defineProperty(document,'hidden',{configurable:true,get:()=>false})");pg.locator('#start').click();pg.locator('#level-exit').click();check('exit confirmation pauses',snap(pg)['paused'] and pg.locator('#reset-dialog').is_visible());pg.locator('#cancel-reset').click();check('cancel exit preserves mission',not snap(pg)['paused'] and snap(pg)['scene']=='breakthrough')
 pg.locator('#restart').click();pg.locator('#confirm-reset').click()
 # Reset confirmation starts a clean mission; play() expects entry/start overlay.
 pg.locator('#pause').click();play(pg,False,prefix='keyboard-bypass')
 play(pg,True,prefix='keyboard-shortcut')
 pg.clock.fast_forward(90100);check('uncapped real-time visible-frame timeout',mission(pg)['phase']=='timeout' and mission(pg)['elapsed']==90);capture(pg,'desktop-timeout');frozen=snap(pg)['state'];pg.locator('#arena').focus();pg.keyboard.down('Space');pg.clock.run_for(1000);pg.keyboard.up('Space');check('timeout is terminal',snap(pg)['state']==frozen)
 pg.locator('#start').click();check('timeout retry resets map and clock',mission(pg)['elapsed']==0 and len(snap(pg)['state']['walls'])==9);pg.locator('#level-exit').click();pg.locator('#confirm-reset').click();check('confirmed exit returns range entry',snap(pg)['scene']=='range' and not snap(pg)['started']);c.close()
 c=b.new_context(viewport=dict(width=390,height=844),device_scale_factor=2,is_mobile=True,has_touch=True);pg=ready(c);touch=Touch(pg,c);play(pg,False,touch,'touch-bypass');play(pg,True,touch,'touch-shortcut')
 # Two actual simultaneous pointers, on a fresh mission, independent of routes.
 pg.locator('#arena').focus();before=snap(pg)['state'];touch.start('ArrowLeft',True);pg.clock.run_for(100);during=snap(pg)['state'];touch.end();check('simultaneous touch moves and fires',during['tank']['x']<before['tank']['x'] and during['shots']>before['shots']);c.close()
 for w,h in [(320,740),(390,844),(768,1024),(1440,900),(844,390)]:
  c=b.new_context(viewport=dict(width=w,height=h),has_touch=True,reduced_motion='reduce');pg=ready(c);pg.locator('#start').click()
  for lang in ['en','zh-TW']:
   if snap(pg)['settings']['language']!=lang:pg.locator('#language').click()
   capture(pg,f'viewport-{w}x{h}-{lang}')
   pixel=pg.evaluate("()=>{const c=document.querySelector('#arena');return [...c.getContext('2d').getImageData(Math.round(336*c.width/768),Math.round(144*c.height/768),1,1).data]}")
   check(f'{w} {lang} actual cell rendered after scene switch',pixel[0]>pixel[1]>pixel[2],pixel)
   metrics=pg.evaluate("""()=>({overflow:document.documentElement.scrollWidth>innerWidth,targets:[...document.querySelectorAll('[data-dir],#fire')].map(x=>{const r=x.getBoundingClientRect();return[r.width,r.height]}),fire:document.querySelector('#fire').getBoundingClientRect().bottom,arena:document.querySelector('#arena').getBoundingClientRect().width})""")
   check(f'{w} {lang} layout targets reduced motion',not metrics['overflow'] and all(x>=44 and y>=44 for x,y in metrics['targets']) and snap(pg)['reduced'],metrics)
   if w in [320,390]:check(f'{w} {lang} portrait Fire within viewport',metrics['fire']<=h,metrics)
   if w in [320,390,1440]:
    pg.clock.resume();pg.add_script_tag(path=os.environ.get('AXE_PATH','/tmp/armorheart-audit/node_modules/axe-core/axe.min.js'))
    audit=pg.evaluate("""async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}});return {violations:r.violations,passes:r.passes.length,incomplete:r.incomplete.map(x=>({id:x.id,impact:x.impact}))}}""")
    (OUT/f'axe-{w}-{lang}.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False));check(f'{w} {lang} axe no violations',not audit['violations'],[x['id'] for x in audit['violations']])
  c.close()
 for shortcut in [False,True]:
  c=b.new_context();before=len(requests);pg=ready(c,True);play(pg,shortcut,prefix='offline-'+('shortcut' if shortcut else 'bypass'),offline=True)
  net=[u for u in requests[before:] if u.startswith(('http:','https:'))];check('offline no subsequent HTTP '+str(shortcut),net==['http://127.0.0.1:8080/preview/guardian.html'],net);c.close()
 check('no JavaScript errors',not errors,errors);check('no external runtime network',not [u for u in requests if u.startswith(('http:','https:')) and not u.startswith('http://127.0.0.1:8080')]);b.close()
(OUT/'browser-results.json').write_text(json.dumps(dict(date='2026-11-03 Asia/Taipei',passed=len(results),failed=0,tests=results,playthroughs=plays,errors=errors,independent_human_playtest='Not performed',physical_phone='Not performed',other_browser_engines='Not performed'),indent=2,ensure_ascii=False)+'\n')
print(json.dumps(dict(passed=len(results),failed=0)))
