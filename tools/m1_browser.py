"""Historical M1 only: run from frozen M1 revision, not the current R3 map.
Real-input M1 evidence. Only Playwright controls time; game state is read-only.
Run a loopback server on8080. No scenario fixtures in the main playthroughs.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,time,os
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence/m1';OUT.mkdir(parents=True,exist_ok=True)
results=[];errors=[];requests=[]
def check(name,ok,detail=None):
 results.append(dict(name=name,passed=bool(ok),detail=detail))
 if not ok:raise AssertionError((name,detail))
def snap(pg):return pg.evaluate('guardianPOC.snapshot()')
def mission(pg):return snap(pg)['state']['mission']
def capture(pg,name):pg.screenshot(path=str(OUT/(name+'.png')),full_page=True)
def ready(c):
 pg=c.new_page();pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('request',lambda r:requests.append(r.url))
 pg.clock.install();pg.goto('http://127.0.0.1:8080');pg.wait_for_function('window.guardianPOC');pg.clock.pause_at(int(time.time()*1000)+1000);pg.locator('#choose-mission').click();return pg
def key(pg,k,ms):
 pg.locator('#arena').focus();pg.keyboard.down(k);pg.clock.run_for(ms);pg.keyboard.up(k)
def move(pg,k,axis,target,sign,touch=None,fire=False):
 pg.locator('#arena').focus()
 if touch:touch.start(k,fire)
 else:pg.keyboard.down(k)
 for i in range(120):
  if snap(pg)['state']['tank'][axis]*sign>=target*sign:break
  pg.clock.run_for(100)
 else:raise AssertionError(('movement blocked',axis,target,snap(pg)['state']['tank']))
 if touch:touch.end()
 else:pg.keyboard.up(k)
def fire_to(pg,count,touch=None):
 if touch:touch.start('ArrowUp',True)
 else:
  key(pg,'ArrowUp',64);pg.keyboard.down('Space')
 for i in range(30):
  if snap(pg)['state']['destroyed']>=count:break
  pg.clock.run_for(100)
 else:raise AssertionError(('fire blocked',count,snap(pg)['state']))
 if touch:touch.end()
 else:pg.keyboard.up('Space')
class Touch:
 def __init__(self,pg,c):self.pg=pg;self.cdp=c.new_cdp_session(pg)
 def start(self,key,fire=False):
  self.pg.locator('#fire').scroll_into_view_if_needed();name={'ArrowUp':'up','ArrowDown':'down','ArrowLeft':'left','ArrowRight':'right'}[key]
  selectors=[f'[data-dir="{name}"]']+(['#fire'] if fire else []);points=[]
  for i,sel in enumerate(selectors):
   b=self.pg.locator(sel).bounding_box();points.append(dict(x=b['x']+b['width']/2,y=b['y']+b['height']/2,id=i+1))
  self.cdp.send('Input.dispatchTouchEvent',dict(type='touchStart',touchPoints=points))
 def end(self):self.cdp.send('Input.dispatchTouchEvent',dict(type='touchEnd',touchPoints=[]))
def play(pg,side,touch=None,prefix='keyboard'):
 target=256 if side=='left' else 512;keyname='ArrowLeft' if side=='left' else 'ArrowRight';sign=-1 if side=='left' else 1
 move(pg,keyname,'x',target,sign,touch,fire=bool(touch));fire_to(pg,1,touch)
 check(prefix+' one lower gate does not release crowd',mission(pg)['phase']=='waiting' and mission(pg)['crowd']['y']==704)
 capture(pg,prefix+'-lower-open')
 move(pg,'ArrowUp','y',320,-1,touch,fire=bool(touch))
 move(pg,'ArrowRight' if side=='left' else 'ArrowLeft','x',384,1 if side=='left' else -1,touch,fire=bool(touch));fire_to(pg,2,touch)
 check(prefix+' route opening announces evacuation',mission(pg)['phase']=='evacuating' and pg.locator('#announcement').inner_text() in ['Route open. Evacuation has begun.','路線已暢通，人群開始撤離。'])
 check(prefix+' alternate gate remains optional',snap(pg)['state']['destroyed']==2)
 capture(pg,prefix+'-evacuating');before=mission(pg)['elapsed'];pg.locator('#language').click();after=mission(pg)['elapsed']
 check(prefix+' language switch preserves deadline and route',abs(before-after)<.1 and mission(pg)['phase']=='evacuating');capture(pg,prefix+'-evacuating-other-language')
 pg.clock.run_for(18000)
 check(prefix+' actual full mission success',mission(pg)['phase']=='success' and snap(pg)['state']['complete'] and mission(pg)['elapsed']<90,dict(elapsed=mission(pg)['elapsed'],shots=snap(pg)['state']['shots']))
 check(prefix+' all crowd envelope inside exit',336<=mission(pg)['crowd']['x']<=432 and 16<=mission(pg)['crowd']['y']<=80)
 capture(pg,prefix+'-success');pg.locator('#start').click();check(prefix+' replay clean',mission(pg)['phase']=='waiting' and mission(pg)['elapsed']==0 and snap(pg)['state']['shots']==0 and len(snap(pg)['state']['walls'])==6)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 c=b.new_context(viewport=dict(width=1440,height=1000));pg=ready(c);capture(pg,'desktop-entry');pg.clock.run_for(10000)
 check('entry does not spend timer',mission(pg)['elapsed']==0);pg.locator('#start').click();key(pg,'Space',2000)
 check('stationary spawn fire does not solve',snap(pg)['state']['destroyed']==0 and mission(pg)['phase']=='waiting');pg.locator('#pause').click();before=mission(pg)['elapsed'];pg.clock.run_for(5000)
 check('pause stops mission time',mission(pg)['elapsed']==before);pg.locator('#start').click();pg.clock.run_for(64);check('resume rebases clock without catch-up',mission(pg)['elapsed']-before<.1)
 # Visibility handler is exercised explicitly; this is lifecycle-event simulation,
 # not a claim of real-device background behavior.
 pg.evaluate("Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'))")
 before=mission(pg)['elapsed'];pg.clock.run_for(5000);check('simulated hidden-tab lifecycle pauses clock',snap(pg)['paused'] and mission(pg)['elapsed']==before)
 pg.evaluate("Object.defineProperty(document,'hidden',{configurable:true,get:()=>false})");pg.locator('#start').click()
 pg.locator('#level-exit').click();check('level exit pauses for confirmation',snap(pg)['paused'] and pg.locator('#reset-dialog').is_visible());pg.locator('#cancel-reset').click();check('cancel exit preserves mission',snap(pg)['scene']=='breakthrough' and not snap(pg)['paused'])
 play(pg,'left',prefix='keyboard-left')
 # One long visible frame must time out rather than discard capped physics time.
 pg.clock.fast_forward(90100);check('long visible frame timeout uses real active time',mission(pg)['phase']=='timeout' and mission(pg)['elapsed']==90);capture(pg,'desktop-timeout')
 frozen=snap(pg)['state'];key(pg,'Space',1000);check('timeout is terminal',snap(pg)['state']==frozen)
 pg.locator('#start').click();check('timeout retry resets clock and map',mission(pg)['elapsed']==0 and mission(pg)['phase']=='waiting' and len(snap(pg)['state']['walls'])==6)
 pg.locator('#level-exit').click();pg.locator('#confirm-reset').click();check('confirmed level exit returns to range entry',snap(pg)['scene']=='range' and not snap(pg)['started'])
 c.close()
 # Independent right entrance completion through actual two-finger input.
 c=b.new_context(viewport=dict(width=390,height=844),device_scale_factor=2,is_mobile=True,has_touch=True);pg=ready(c);pg.locator('#start').click();play(pg,'right',Touch(pg,c),'touch-right');c.close()
 for width,height in [(320,740),(390,844),(768,1024),(1440,900),(844,390)]:
  c=b.new_context(viewport=dict(width=width,height=height),has_touch=True,reduced_motion='reduce');pg=ready(c);pg.locator('#start').click()
  for lang in ['en','zh-TW']:
   if snap(pg)['settings']['language']!=lang:pg.locator('#language').click()
   capture(pg,f'viewport-{width}x{height}-{lang}')
   pixel=pg.evaluate("""()=>{const c=document.querySelector('#arena'),g=c.getContext('2d');return [...g.getImageData(Math.round(256*c.width/768),Math.round(448*c.height/768),1,1).data]}""")
   check(f'{width} {lang} actual mission brick rendered after scene switch',pixel[0]>pixel[1]>pixel[2],pixel)
   metrics=pg.evaluate("""()=>({overflow:document.documentElement.scrollWidth>innerWidth,targets:[...document.querySelectorAll('[data-dir],#fire')].map(x=>{const r=x.getBoundingClientRect();return[r.width,r.height]}),fire:document.querySelector('#fire').getBoundingClientRect().bottom,arena:document.querySelector('#arena').getBoundingClientRect().width})""")
   check(f'{width} {lang} layout/targets/reduced motion',not metrics['overflow'] and all(x>=44 and y>=44 for x,y in metrics['targets']) and snap(pg)['reduced'],metrics)
   if width in [320,390]:check(f'{width} {lang} arena and Fire usable in portrait viewport',metrics['fire']<=height,metrics)
   if width in [320,390,1440]:
    # axe schedules async timers; resume the browser clock for its audit.
    pg.clock.resume()
    pg.add_script_tag(path=os.environ.get('AXE_PATH','/tmp/armorheart-audit/node_modules/axe-core/axe.min.js'))
    audit=pg.evaluate("""async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}});return {violations:r.violations,passes:r.passes.length,incomplete:r.incomplete.map(x=>({id:x.id,impact:x.impact}))}}""")
    (OUT/f'axe-{width}-{lang}.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False));check(f'{width} {lang} axe no violations',not audit['violations'],[x['id'] for x in audit['violations']])
  c.close()
 # Self-contained application: both mission routes must remain playable with
 # every network request besides the initial HTML denied.
 c=b.new_context();pg=c.new_page();pg.clock.install();url='http://127.0.0.1:8080/preview/guardian.html';network=[]
 pg.on('request',lambda r:network.append(r.url) if r.url.startswith(('http:','https:')) else None)
 pg.route('**/*',lambda r:r.continue_() if r.request.url==url else r.abort());pg.goto(url);pg.wait_for_function('window.guardianPOC');pg.clock.pause_at(int(time.time()*1000)+1000);pg.locator('#choose-mission').click();pg.locator('#start').click();play(pg,'right',prefix='offline-right')
 check('bundled mission no additional network',network==[url],network);c.close()
 check('no JavaScript errors',not errors,errors)
 check('no external runtime requests',not [u for u in requests if u.startswith(('http:','https:')) and not u.startswith('http://127.0.0.1:8080')])
 b.close()
(OUT/'browser-results.json').write_text(json.dumps(dict(date='2026-11-03 Asia/Taipei',passed=sum(x['passed'] for x in results),failed=sum(not x['passed'] for x in results),tests=results,errors=errors,independent_human_playtest='Not performed; pending human review'),indent=2,ensure_ascii=False))
print(json.dumps(dict(passed=len(results),failed=0)))
