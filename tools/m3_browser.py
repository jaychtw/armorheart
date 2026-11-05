"""Actual keyboard/CDP-touch M3 play. Controlled clock; game snapshots read-only."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,os,time,math
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/os.environ.get('EVIDENCE_DIR','evidence/m3');OUT.mkdir(parents=True,exist_ok=True);results=[];plays=[];errors=[];network=[]
def check(name,ok,detail=None):
 results.append(dict(name=name,passed=bool(ok),detail=detail))
 if not ok:raise AssertionError((name,detail))
def snap(pg):return pg.evaluate('guardianPOC.snapshot()')
def mission(pg):return snap(pg)['state']['interception']
def visual(pg):return pg.evaluate('guardianPOC.shipVisual()')
def pic(pg,name):pg.screenshot(path=str(OUT/(name+'.png')),full_page=True)
INIT='''(()=>{const p=CanvasRenderingContext2D.prototype,c=p.clearRect,d=p.drawImage,a=p.arc;window.m3Paint={ship:null,rounds:[]};p.clearRect=function(...args){if(this.canvas.id==='arena')window.m3Paint={ship:null,rounds:[]};return c.apply(this,args)};p.drawImage=function(im,...args){if(this.canvas.id==='arena'&&im.naturalWidth===664&&im.naturalHeight===260){const m=this.getTransform(),s=this.canvas.width/768;m3Paint.ship={a:m.a/s,b:m.b/s,c:m.c/s,d:m.d/s,x:m.e/s,y:m.f/s,args};}return d.call(this,im,...args)};p.arc=function(x,y,r,...rest){if(this.canvas.id==='arena'&&r===4)m3Paint.rounds.push({x,y,r});return a.call(this,x,y,r,...rest)}})()'''
def ready(c,offline=False):
 pg=c.new_page();pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('request',lambda r:network.append(r.url) if r.url.startswith(('http:','https:')) else None);pg.clock.install();pg.add_init_script(INIT);url='http://127.0.0.1:8080/'+('preview/guardian.html' if offline else '')
 if offline:pg.route('**/*',lambda r:r.continue_() if r.request.url==url else r.abort())
 pg.goto(url);pg.wait_for_function('window.guardianPOC');pg.clock.pause_at(int(time.time()*1000)+1000);pg.locator('#choose-ship').click();return pg
class Touch:
 def __init__(self,pg,c):self.pg=pg;self.cdp=c.new_cdp_session(pg)
 def start(self,k=None,fire=False):
  self.pg.locator('#fire').scroll_into_view_if_needed();sels=[]
  if k:sels.append('[data-dir="'+{'ArrowUp':'up','ArrowDown':'down','ArrowLeft':'left','ArrowRight':'right'}[k]+'"]')
  if fire:sels.append('#fire')
  points=[]
  for i,sel in enumerate(sels):
   b=self.pg.locator(sel).bounding_box();points.append(dict(id=i+1,x=b['x']+b['width']/2,y=b['y']+b['height']/2))
  self.cdp.send('Input.dispatchTouchEvent',dict(type='touchStart',touchPoints=points))
 def end(self):self.cdp.send('Input.dispatchTouchEvent',dict(type='touchEnd',touchPoints=[]))
def hold(pg,k,ms,touch=None,fire=False):
 pg.locator('#arena').focus()
 if touch:touch.start(k,fire)
 else:
  if k:pg.keyboard.down(k)
  if fire:pg.keyboard.down('Space')
 pg.clock.run_for(ms)
 if touch:touch.end()
 else:
  if k:pg.keyboard.up(k)
  if fire:pg.keyboard.up('Space')
def until(pg,fn,limit=1000):
 for _ in range(limit):
  if fn():return
  pg.clock.run_for(32)
 raise AssertionError(('condition timed out',mission(pg)))
def wait_time(pg,t):until(pg,lambda:mission(pg)['elapsed']>=t)
def move(pg,key,axis,target,sign,touch=None):
 if touch:touch.start(key)
 else:pg.locator('#arena').focus();pg.keyboard.down(key)
 for _ in range(250):
  d=(target-snap(pg)['state']['tank'][axis])*sign
  if d<=0:break
  pg.clock.run_for(100 if d>30 else 16)
 else:raise AssertionError(('blocked',snap(pg)))
 if touch:touch.end()
 else:pg.keyboard.up(key)
def render_check(pg,label):
 s=snap(pg);v=visual(pg);p=pg.evaluate('m3Paint');a=p['ship'];theta=v['pose']['heading'];check(label+' ship raster transform matches exact route',a is not None and max(abs(a['x']-v['pose']['x']),abs(a['y']-v['pose']['y']),abs(a['a']-math.cos(theta)),abs(a['b']-math.sin(theta)),abs(a['c']+math.sin(theta)),abs(a['d']-math.cos(theta)))<1e-4 and a['args']==[-166,-54,332,130]);rounds=s['state']['interception']['enemyShells'];check(label+' hostile shells actually rendered at collision positions',len(p['rounds'])==len(rounds) and all(abs(a['x']-b['x'])<1e-7 and abs(a['y']-b['y'])<1e-7 for a,b in zip(p['rounds'],rounds)))
def win(pg,touch=None,name='keyboard-informed'):
 pg.locator('#start').click();hold(pg,'ArrowLeft',675,touch);hold(pg,None,1225,touch,True);check(name+' two initial side hits',mission(pg)['shipHP']==4);pic(pg,name+'-smoking');hold(pg,'ArrowRight',675,touch);hold(pg,'ArrowUp',32,touch);aimed=snap(pg)['state']['tank']
 if touch:touch.start(fire=True)
 else:pg.keyboard.down('Space')
 saved=set()
 for _ in range(1000):
  m=mission(pg)
  if m['shipHP']<=2 and 'onFire' not in saved:saved.add('onFire');pic(pg,name+'-on-fire');check(name+' visible on-fire state',visual(pg)['stage']=='onFire')
  if snap(pg)['state']['complete']:break
  pg.clock.run_for(32)
 else:raise AssertionError(('no victory',m))
 if touch:touch.end()
 else:pg.keyboard.up('Space')
 m=mission(pg);check(name+' wins with six effective hull hits',m['outcome']=='success' and len(m['shotHits'])==6);check(name+' all three tankHP retained',m['tankHP']==3,m['tankHits']);check(name+' near modeled12.72s',12<=m['finishedAt']<=13.5,m['finishedAt']);check(name+' no movement after second aim',snap(pg)['state']['tank']==aimed);pic(pg,name+'-victory');plays.append(dict(name=name,input='CDP touch' if touch else 'keyboard',outcome=m['outcome'],finishedAt=m['finishedAt'],shots=snap(pg)['state']['shots'],tankHP=m['tankHP'],hits=m['shotHits'],lastAim=aimed,ongoing_response='none after initial two-station positioning/aim'))
def defeat(pg,touch=None,name='keyboard-tank-loss'):
 pg.locator('#start').click();move(pg,'ArrowUp','y',576,-1,touch);move(pg,'ArrowRight','x',416,1,touch);hold(pg,'ArrowUp',16,touch);until(pg,lambda:mission(pg)['tankHP']==2);m=mission(pg);pic(pg,name+'-first-hit');before=snap(pg)['state'];hold(pg,'ArrowRight',100,touch,True);after=snap(pg)['state'];check(name+' can move/fire while protected',after['tank']['x']>before['tank']['x'] and after['shots']>before['shots'] and after['interception']['tankHP']==2);move(pg,'ArrowLeft','x',416,-1,touch);hold(pg,'ArrowUp',16,touch)
 until(pg,lambda:snap(pg)['state']['complete']);m=mission(pg);check(name+' actual three-hit tank defeat',m['outcome']=='defeat' and m['tankHP']==0 and len(m['tankHits'])==3,m['tankHits']);check(name+' damage intervals respect3s',all(b['time']-a['time']>=3-1e-8 for a,b in zip(m['tankHits'],m['tankHits'][1:])));pic(pg,name+'-defeat');plays.append(dict(name=name,input='CDP touch' if touch else 'keyboard',outcome=m['outcome'],finishedAt=m['finishedAt'],tankHits=m['tankHits'],shipHP=m['shipHP']));pg.locator('#start').click();check(name+' fresh retry',mission(pg)['elapsed']==0 and mission(pg)['shipHP']==6 and mission(pg)['tankHP']==3);pg.locator('#level-exit').click();pg.locator('#confirm-reset').click();check(name+' exit to range',snap(pg)['scene']=='range')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);c=b.new_context(viewport=dict(width=1440,height=1000));pg=ready(c);pic(pg,'desktop-entry');pg.clock.run_for(5000);check('entry spends no simulation time',mission(pg)['elapsed']==0);pg.locator('#start').click();wait_time(pg,2.7);check('localized charge status is visible',visual(pg)['status']=='charging' and 'preparing' in pg.locator('#boss-phase').inner_text());pic(pg,'desktop-charge')
 pg.locator('#pause').click();saved=mission(pg);pg.clock.run_for(5000);check('pause freezes ship,charge,shells,health and immunity',mission(pg)==saved);pg.locator('#start').click();pg.clock.run_for(16);check('resume no catchup',mission(pg)['elapsed']-saved['elapsed']<.05)
 pg.evaluate("Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'))");saved=mission(pg);pg.clock.run_for(5000);check('simulated hidden lifecycle pauses M3',snap(pg)['paused'] and mission(pg)==saved);pg.evaluate("Object.defineProperty(document,'hidden',{configurable:true,get:()=>false})");pg.locator('#start').click()
 for label,t in [('left-volley',3.1),('left-turn',8.25),('top-charge',11.7),('top-volley',12.1),('right-turn',14.95),('right-charge',17.7),('right-volley',18.1),('last-charge',20.7),('last-volley',21.1)]:
  wait_time(pg,t);render_check(pg,label);pic(pg,label)
 until(pg,lambda:snap(pg)['state']['complete']);m=mission(pg);check('surviving ship causes exit loss',m['outcome']=='escaped' and m['shipHP']==6 and m['tankHP']==2);check('exact physical exit time',abs(m['finishedAt']-(1892.3893421169303/72))<1e-8,m['finishedAt']);check('all four eligible three-shell volleys',[(o['time'],len(o['muzzles'])) for o in m['opportunities'] if o['fired']]==[(3,3),(12,3),(18,3),(21,3)]);check('all held opportunities skip without deferred burst',[o['time'] for o in m['opportunities'] if not o['fired']]==[6,9,15,24]);pic(pg,'desktop-ship-escaped');plays.append(dict(name='no-fire-full-route',outcome=m['outcome'],finishedAt=m['finishedAt'],tankHP=m['tankHP'],opportunities=m['opportunities']));pg.locator('#start').click();check('escape retry resets route and all projectiles',mission(pg)['elapsed']==0 and not mission(pg)['enemyShells'] and mission(pg)['shipHP']==6)
 pg.locator('#restart').click();check('restart confirmation pauses',snap(pg)['paused']);pg.locator('#cancel-reset').click();check('cancel retains encounter',not snap(pg)['paused'] and mission(pg)['shipHP']==6);pg.locator('#restart').click();pg.locator('#confirm-reset').click();check('confirmed restart fresh',mission(pg)['elapsed']==0)
 before=snap(pg)['state'];pg.locator('#language').click();check('live zh-TW retains whole state',snap(pg)['state']==before and pg.locator('#range-title').inner_text()=='攔截');pg.locator('#language').click();pg.locator('#boss-sound').click();check('mission sound control toggles',not snap(pg)['settings']['muted']);pg.locator('#boss-sound').click();pg.locator('#boss-motion').click();check('reduced motion setting works',snap(pg)['reduced']);pg.locator('#boss-motion').click()
 pg.locator('#restart').click();pg.locator('#confirm-reset').click();pg.locator('#pause').click();win(pg,name='keyboard-informed');defeat(pg,name='keyboard-tank-loss');pg.locator('#choose-colossus').click();check('accepted M2 remains selectable',snap(pg)['state']['colossus']['bossHP']==4);pg.locator('#choose-mission').click();check('accepted R3 remains selectable',len(snap(pg)['state']['walls'])==9);c.close()
 c=b.new_context(viewport=dict(width=390,height=844),device_scale_factor=2,is_mobile=True,has_touch=True);pg=ready(c);touch=Touch(pg,c);win(pg,touch,'touch-informed');defeat(pg,touch,'touch-tank-loss');pg.locator('#choose-ship').click();pg.locator('#start').click();before=snap(pg)['state'];touch.start('ArrowLeft',True);pg.clock.run_for(100);touch.end();after=snap(pg)['state'];check('actual simultaneous two-finger move/fire',after['tank']['x']<before['tank']['x'] and after['shots']>before['shots']);pg.locator('#restart').tap();pg.locator('#confirm-reset').tap();until(pg,lambda:snap(pg)['state']['complete']);check('actual mobile ship-exit loss',mission(pg)['outcome']=='escaped' and mission(pg)['shipHP']==6);pic(pg,'touch-ship-escaped');pg.locator('#start').tap();check('touch exit-loss retry fresh',mission(pg)['elapsed']==0 and mission(pg)['tankHP']==3 and mission(pg)['shipHP']==6);pg.locator('#level-exit').tap();pg.locator('#confirm-reset').tap();check('touch confirmed level exit to range',snap(pg)['scene']=='range');c.close()
 for width,height in[(320,740),(390,844),(768,1024),(1440,900),(844,390)]:
  c=b.new_context(viewport=dict(width=width,height=height),has_touch=True,reduced_motion='reduce');pg=ready(c);a=pg.locator('#arena').bounding_box();start=pg.locator('#start').bounding_box();check(str(width)+' entry start fits canvas',start['y']>=a['y'] and start['y']+start['height']<=a['y']+a['height']);pg.locator('#start').click();wait_time(pg,8.25)
  for lang in['en','zh-TW']:
   if snap(pg)['settings']['language']!=lang:pg.locator('#language').click()
   pic(pg,f'viewport-{width}x{height}-{lang}');metrics=pg.evaluate("""()=>({overflow:document.documentElement.scrollWidth>innerWidth,targets:[...document.querySelectorAll('[data-dir],#fire,.boss-settings button,#choose-ship')].map(e=>{const b=e.getBoundingClientRect();return[b.width,b.height]}),pause:document.querySelector('#pause').getBoundingClientRect().top,settings:document.querySelector('.boss-settings').getBoundingClientRect().top,hud:document.querySelector('#boss-hud').getBoundingClientRect().top,fire:document.querySelector('#fire').getBoundingClientRect().bottom})""");check(f'{width} {lang} usable targets/layout',not metrics['overflow'] and all(w>=44 and h>=44 for w,h in metrics['targets']) and snap(pg)['reduced'],metrics)
   if width in[320,390]:check(f'{width} {lang} HUD/Pause/settings/Fire remain visible',metrics['hud']>=-1 and metrics['pause']>=-1 and metrics['settings']>=-1 and metrics['fire']<=height,metrics)
   if width in[320,390,1440]:
    pg.locator('#pause').click();pg.clock.resume();pg.add_script_tag(path=os.environ.get('AXE_PATH','/tmp/armorheart-audit/node_modules/axe-core/axe.min.js'));audit=pg.evaluate("""async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}});return{violations:r.violations,passes:r.passes.length,incomplete:r.incomplete.map(x=>({id:x.id,impact:x.impact}))}}""");(OUT/f'axe-{width}-{lang}.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n');check(f'{width} {lang} axe zero reported violations',not audit['violations'],[x['id'] for x in audit['violations']]);pg.locator('#start').click()
  c.close()
 for mode in['win','escape','defeat']:
  c=b.new_context();n=len(network);pg=ready(c,True)
  if mode=='win':win(pg,name='offline-informed')
  elif mode=='defeat':defeat(pg,name='offline-tank-loss')
  else:pg.locator('#start').click();until(pg,lambda:snap(pg)['state']['complete']);check('offline actual ship exit',mission(pg)['outcome']=='escaped');pic(pg,'offline-escaped')
  check('offline only initial HTML '+mode,network[n:]==['http://127.0.0.1:8080/preview/guardian.html'],network[n:]);c.close()
 check('no JavaScript errors',not errors,errors);check('no external runtime HTTP',not [u for u in network if not u.startswith('http://127.0.0.1:8080')]);b.close()
(OUT/'browser-results.json').write_text(json.dumps(dict(date='2026-11-04 Asia/Taipei',passed=len(results),failed=0,tests=results,playthroughs=plays,errors=errors,method='actual keyboard/CDP touch, controlled clock, read-only game snapshots and rendered Canvas command checks',independent_first_time_player='Not performed',physical_phone='Not performed',other_browser_engines='Not performed'),indent=2,ensure_ascii=False)+'\n');print(json.dumps(dict(passed=len(results),failed=0,plays=[{k:v for k,v in p.items() if k in['name','outcome','finishedAt','tankHP']} for p in plays])))
