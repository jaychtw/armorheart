"""M2 actual-input browser verification; simulation snapshots read-only.
No modified gameplay/initial fixtures in these playthroughs. Clock is controlled.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,time,os
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence/m2';OUT.mkdir(parents=True,exist_ok=True);results=[];errors=[];plays=[];net=[]
def check(name,ok,detail=None):
 results.append(dict(name=name,passed=bool(ok),detail=detail))
 if not ok:raise AssertionError((name,detail))
def snap(pg):return pg.evaluate('guardianPOC.snapshot()')
def boss(pg):return snap(pg)['state']['colossus']
def pic(pg,name):pg.screenshot(path=str(OUT/(name+'.png')),full_page=True)
def ready(c,offline=False):
 pg=c.new_page();pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('request',lambda r:net.append(r.url) if r.url.startswith(('http:','https:')) else None);pg.clock.install();url='http://127.0.0.1:8080/'+('preview/guardian.html' if offline else '')
 if offline:pg.route('**/*',lambda r:r.continue_() if r.request.url==url else r.abort())
 pg.goto(url);pg.wait_for_function('window.guardianPOC');pg.clock.pause_at(int(time.time()*1000)+1000);pg.locator('#choose-colossus').click();return pg
class Touch:
 def __init__(self,pg,c):self.pg=pg;self.cdp=c.new_cdp_session(pg)
 def start(self,k=None,fire=False):
  self.pg.locator('#fire').scroll_into_view_if_needed();selectors=[]
  if k:selectors.append('[data-dir="'+{'ArrowUp':'up','ArrowDown':'down','ArrowLeft':'left','ArrowRight':'right'}[k]+'"]')
  if fire:selectors.append('#fire')
  points=[]
  for i,sel in enumerate(selectors):
   b=self.pg.locator(sel).bounding_box();points.append(dict(x=b['x']+b['width']/2,y=b['y']+b['height']/2,id=i+1))
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
def move(pg,k,axis,target,sign,touch=None):
 pg.locator('#arena').focus()
 if touch:touch.start(k)
 else:pg.keyboard.down(k)
 for _ in range(250):
  d=(target-snap(pg)['state']['tank'][axis])*sign
  if d<=0:break
  pg.clock.run_for(100 if d>30 else 16)
 else:raise AssertionError(('movement blocked',target,snap(pg)['state']['tank']))
 if touch:touch.end()
 else:pg.keyboard.up(k)
def until(pg,condition,limit=600):
 for _ in range(limit):
  if condition():return
  pg.clock.run_for(32)
 raise AssertionError(('condition not met',boss(pg)))
def wait_time(pg,t):until(pg,lambda:boss(pg)['elapsed']>=t)
def safe(pg,touch=None,name='keyboard-safe',scheduled=False):
 if not snap(pg)['started'] or snap(pg)['paused']:pg.locator('#start').click()
 move(pg,'ArrowRight','x',560,1,touch);hold(pg,'ArrowUp',32,touch);at=dict(snap(pg)['state']['tank']);timing=[]
 if scheduled:
  for t in [3.25,4.25,6.45,7.45]:wait_time(pg,t);hold(pg,None,32,touch,True)
  until(pg,lambda:boss(pg)['outcome'] is not None)
 else:
  if touch:touch.start(fire=True)
  else:pg.keyboard.down('Space')
  prev=4
  for _ in range(500):
   m=boss(pg)
   if m['bossHP']!=prev:
    timing.append(dict(hp=m['bossHP'],time=m['elapsed']));prev=m['bossHP']
    if prev>0:pg.clock.run_for(160);pic(pg,name+'-hp'+str(prev))
   if m['outcome']:break
   pg.clock.run_for(16)
  else:raise AssertionError('safe lane did not finish')
  if touch:touch.end()
  else:pg.keyboard.up('Space')
 m=boss(pg);check(name+' actual victory',m['outcome']=='success' and m['bossHP']==0 and m['tankHP']==3,m)
 check(name+' four effective hits and no damage',len(m['shotHits'])==4 and not m['tankHits'])
 check(name+' no movement/response after aiming',snap(pg)['state']['tank']==at,at)
 check(name+' no arbitrary deadline',not pg.locator('#mission-hud').is_visible() and pg.locator('#boss-hud').is_visible())
 pic(pg,name+'-victory');plays.append(dict(name=name,input='CDP touch' if touch else 'keyboard',scheduled=scheduled,finishedAt=m['finishedAt'],shots=snap(pg)['state']['shots'],position=at,hits=m['shotHits'],tankHP=m['tankHP'],response_after_aim='none; held Fire or four scheduled pulses',stages=timing))
 frozen=snap(pg)['state'];pg.locator('#arena').focus();hold(pg,'ArrowRight',100,None,True);check(name+' terminal state frozen',snap(pg)['state']==frozen)
 pg.locator('#start').click();check(name+' replay clean',boss(pg)['bossHP']==4 and boss(pg)['tankHP']==3 and boss(pg)['elapsed']==0 and snap(pg)['state']['shots']==0)
def lose(pg,touch=None,name='keyboard-contact-loss'):
 if not snap(pg)['started'] or snap(pg)['paused']:pg.locator('#start').click()
 move(pg,'ArrowRight','x',560,1,touch);move(pg,'ArrowUp','y',544,-1,touch);until(pg,lambda:boss(pg)['tankHP']==2);first=boss(pg);pic(pg,name+'-first-contact');hold(pg,None,64,touch,True)
 check(name+' fire works during protection',snap(pg)['state']['shots']>0 and boss(pg)['bossHP']==3)
 move(pg,'ArrowLeft','x',208,-1,touch);check(name+' movement works during protection',snap(pg)['state']['tank']['x']<210 and boss(pg)['tankHP']==2)
 until(pg,lambda:boss(pg)['tankHP']==1);pic(pg,name+'-second-contact');move(pg,'ArrowRight','x',384,1,touch);move(pg,'ArrowUp','y',416,-1,touch);until(pg,lambda:boss(pg)['outcome'] is not None)
 m=boss(pg);check(name+' real contact failure/retry path',m['outcome']=='defeat' and m['tankHP']==0 and len(m['tankHits'])==3,m)
 check(name+' all damage intervals honor3s immunity',all(b['time']-a['time']>=3-1e-8 for a,b in zip(m['tankHits'],m['tankHits'][1:])),m['tankHits']);pic(pg,name+'-defeat');plays.append(dict(name=name,input='CDP touch' if touch else 'keyboard',finishedAt=m['finishedAt'],outcome=m['outcome'],tankHits=m['tankHits'],bossHP=m['bossHP']))
 pg.locator('#start').click();check(name+' failure retry fresh',boss(pg)['tankHP']==3 and boss(pg)['bossHP']==4 and boss(pg)['elapsed']==0)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 c=b.new_context(viewport=dict(width=1440,height=1000));pg=ready(c);pic(pg,'desktop-entry');pg.clock.run_for(10000);check('entry spends no simulation time',boss(pg)['elapsed']==0);pg.locator('#start').click()
 # All five stops and jump directions in actual play, without firing or fixtures.
 captures=[]
 for index,t in enumerate([0.65,2.6,3.85,5.8,7.05,9.0,10.25,12.2,13.45,15.4,16.1]):
  wait_time(pg,t);pic(pg,f'cycle-{index:02d}');captures.append(boss(pg))
 check('full real-input idle cycle covers all five landings',boss(pg)['landings']>=5 and {x['stop'] for x in boss(pg)['history'] if x['event']=='landing'}=={'UL','UR','LR','LL','C'})
 check('waiting through a cycle does not win or time out',boss(pg)['outcome'] is None and boss(pg)['bossHP']==4 and boss(pg)['tankHP']==3)
 pg.locator('#pause').click();saved=boss(pg);pg.clock.run_for(5000);check('pause freezes HP, phases, motion and immunity',boss(pg)==saved);pg.locator('#start').click();pg.clock.run_for(16);check('resume has no catch-up',boss(pg)['elapsed']-saved['elapsed']<.04)
 pg.evaluate("Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'))");saved=boss(pg);pg.clock.run_for(5000);check('simulated hidden lifecycle pauses M2',snap(pg)['paused'] and boss(pg)==saved);pg.evaluate("Object.defineProperty(document,'hidden',{configurable:true,get:()=>false})");pg.locator('#start').click()
 pg.locator('#level-exit').click();check('exit asks and pauses',pg.locator('#reset-dialog').is_visible() and snap(pg)['paused']);pg.locator('#cancel-reset').click();check('cancel preserves current M2',snap(pg)['scene']=='colossus' and not snap(pg)['paused']);pg.locator('#restart').click();pg.locator('#confirm-reset').click();check('confirmed retry resets encounter',boss(pg)['elapsed']==0)
 # Existing language/mute/motion settings controls remain reachable during M2.
 before=boss(pg);pg.locator('#language').click();check('live Traditional Chinese preserves state',snap(pg)['settings']['language']=='zh-TW' and boss(pg)==before and pg.locator('#range-title').inner_text()=='巨獸');pg.locator('#language').click()
 pg.locator('#boss-sound').click();check('M2 mute control toggles existing setting',snap(pg)['settings']['muted'] is False);pg.locator('#boss-sound').click();pg.locator('#boss-motion').click();check('M2 reduced-motion control active',snap(pg)['reduced'] and pg.locator('#boss-motion').get_attribute('aria-pressed')=='true');pg.locator('#boss-motion').click()
 safe(pg,name='keyboard-held-safe');lose(pg,name='keyboard-contact-loss')
 pg.locator('#level-exit').click();pg.locator('#confirm-reset').click();check('exit returns accepted Guardian range',snap(pg)['scene']=='range' and len(snap(pg)['state']['walls'])==12 and not snap(pg)['started']);pg.locator('#choose-mission').click();check('R3 selection retains original maze/clock',snap(pg)['scene']=='breakthrough' and len(snap(pg)['state']['walls'])==9 and snap(pg)['state']['mission']['elapsed']==0);c.close()
 c=b.new_context(viewport=dict(width=390,height=844),device_scale_factor=2,is_mobile=True,has_touch=True);pg=ready(c);pic(pg,'phone-entry');touch=Touch(pg,c);safe(pg,touch,'touch-held-safe');lose(pg,touch,'touch-contact-loss')
 before=snap(pg)['state'];touch.start('ArrowRight',True);pg.clock.run_for(100);during=snap(pg)['state'];touch.end();check('actual simultaneous direction and Fire',during['tank']['x']>before['tank']['x'] and during['shots']>before['shots']);c.close()
 # Exact offered four-pulse strategy, no continued reactions.
 c=b.new_context();pg=ready(c);safe(pg,name='keyboard-scheduled-safe',scheduled=True);c.close()
 for width,height in [(320,740),(390,844),(768,1024),(1440,900),(844,390)]:
  c=b.new_context(viewport=dict(width=width,height=height),has_touch=True,reduced_motion='reduce');pg=ready(c)
  box=pg.locator('#arena').bounding_box();start=pg.locator('#start').bounding_box();check(str(width)+' entry action within arena',start['y']>=box['y'] and start['y']+start['height']<=box['y']+box['height'])
  pg.locator('#start').click()
  for lang in ['en','zh-TW']:
   if snap(pg)['settings']['language']!=lang:pg.locator('#language').click()
   pic(pg,f'viewport-{width}x{height}-{lang}');metrics=pg.evaluate("""()=>({overflow:document.documentElement.scrollWidth>innerWidth,targets:[...document.querySelectorAll('[data-dir],#fire,.boss-settings button')].map(x=>{const r=x.getBoundingClientRect();return[r.width,r.height]}),fire:document.querySelector('#fire').getBoundingClientRect().bottom,hud:document.querySelector('#boss-hud').getBoundingClientRect().top})""")
   check(f'{width} {lang} targets/layout/reduced-motion',not metrics['overflow'] and all(w>=44 and h>=44 for w,h in metrics['targets']) and snap(pg)['reduced'],metrics)
   if width in [320,390]:check(f'{width} {lang} HUD and Fire visible together',metrics['hud']>=-1 and metrics['fire']<=height,metrics)
   if width in [320,390,1440]:
    pg.locator('#pause').click();pg.clock.resume();pg.add_script_tag(path=os.environ.get('AXE_PATH','/tmp/armorheart-audit/node_modules/axe-core/axe.min.js'));audit=pg.evaluate("""async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}});return {violations:r.violations,passes:r.passes.length,incomplete:r.incomplete.map(x=>({id:x.id,impact:x.impact}))}}""");(OUT/f'axe-{width}-{lang}.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False));check(f'{width} {lang} axe zero violations',not audit['violations'],[x['id'] for x in audit['violations']]);pg.locator('#start').click()
  c.close()
 for fail in [False,True]:
  c=b.new_context();before=len(net);pg=ready(c,True)
  if fail:lose(pg,name='offline-contact-loss')
  else:safe(pg,name='offline-held-safe')
  check('offline bundle only initial HTML '+str(fail),net[before:]==['http://127.0.0.1:8080/preview/guardian.html'],net[before:]);c.close()
 check('no M2 JavaScript errors',not errors,errors);check('no external runtime HTTP',not [u for u in net if not u.startswith('http://127.0.0.1:8080')]);b.close()
(OUT/'browser-results.json').write_text(json.dumps(dict(date='2026-11-03 Asia/Taipei',passed=len(results),failed=0,tests=results,playthroughs=plays,errors=errors,independent_first_time_player='Not performed',physical_phone='Not performed',other_browser_engines='Not performed'),indent=2,ensure_ascii=False)+'\n');print(json.dumps(dict(passed=len(results),failed=0,plays=plays)))
