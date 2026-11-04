"""Actual keyboard/CDP-touch M3 play. Controlled clock; game snapshots read-only."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,os,time,math
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/os.environ.get('EVIDENCE_DIR','evidence/m4');OUT.mkdir(parents=True,exist_ok=True);results=[];plays=[];errors=[];network=[]
def check(name,ok,detail=None):
 results.append(dict(name=name,passed=bool(ok),detail=detail))
 if not ok:raise AssertionError((name,detail))
def snap(pg):return pg.evaluate('guardianPOC.snapshot()')
def mission(pg):return snap(pg)['state']['siege']
def visual(pg):return pg.evaluate('guardianPOC.fortressVisual()')
def pic(pg,name):pg.screenshot(path=str(OUT/(name+'.png')),full_page=True)
INIT='''(()=>{const p=CanvasRenderingContext2D.prototype,c=p.clearRect,d=p.drawImage,a=p.arc;window.m4Paint={body:null,guns:[],rounds:[]};p.clearRect=function(...args){if(this.canvas.id==='arena')window.m4Paint={body:null,guns:[],rounds:[]};return c.apply(this,args)};p.drawImage=function(im,...args){if(this.canvas.id==='arena'){const m=this.getTransform(),s=this.canvas.width/768,data={x:m.e/s,y:m.f/s,a:m.a/s,b:m.b/s,c:m.c/s,d:m.d/s,args};if(im.naturalWidth===512&&im.naturalHeight===320)m4Paint.body=data;if(im.naturalWidth===16&&im.naturalHeight===40)m4Paint.guns.push(data);}return d.call(this,im,...args)};p.arc=function(x,y,r,...rest){if(this.canvas.id==='arena'&&r===4&&this.fillStyle==='#f6d08a')m4Paint.rounds.push({x,y,r});return a.call(this,x,y,r,...rest)}})()'''

def ready(c,offline=False):
 pg=c.new_page();pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('request',lambda r:network.append(r.url) if r.url.startswith(('http:','https:')) else None);pg.clock.install();pg.add_init_script(INIT);url='http://127.0.0.1:8080/'+('preview/guardian.html' if offline else '')
 if offline:pg.route('**/*',lambda r:r.continue_() if r.request.url==url else r.abort())
 pg.goto(url);pg.wait_for_function('window.guardianPOC');pg.clock.pause_at(int(time.time()*1000)+1000);pg.locator('#choose-siege').click();return pg
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
 v=visual(pg);p=pg.evaluate('m4Paint');check(label+' actual body uses physical rectangle',p['body'] is not None and p['body']['args']==[256,64,256,160]);check(label+' three rendered gun layers',len(p['guns'])==3)
 for actual,g in zip(p['guns'],v['guns']):
  tip=[actual['x']+actual['c']*24,actual['y']+actual['d']*24];check(label+' rendered muzzle '+str(g['i']),max(abs(actual['x']-g['x']),abs(actual['y']-g['y']),abs(tip[0]-g['muzzle']['x']),abs(tip[1]-g['muzzle']['y']))<1e-4,(tip,g))
 rounds=mission(pg)['enemyShells'];check(label+' drawn rounds match live collisions',len(p['rounds'])==len(rounds) and all(abs(a['x']-b['x'])<1e-6 and abs(a['y']-b['y'])<1e-6 for a,b in zip(p['rounds'],rounds)))
stage_seen={}
def fire_to(pg,target,touch=None,name='play'):
 if touch:touch.start(fire=True)
 else:pg.locator('#arena').focus();pg.keyboard.down('Space')
 seen=stage_seen.setdefault(name,set())
 for _ in range(1600):
  m=mission(pg)
  for hp,stage in[(5,'broken'),(2,'half')]:
   if m['fortressHP']<=hp and stage not in seen:seen.add(stage);pic(pg,name+'-'+stage);check(name+' '+stage+' visual threshold',visual(pg)['stage'] in [stage,'defeated']);render_check(pg,name+' '+stage)
  if snap(pg)['state']['complete'] or m['elapsed']>=target:break
  pg.clock.run_for(16)
 else:raise AssertionError(('fire timed out',m))
 if touch:touch.end()
 else:pg.keyboard.up('Space')
def play(pg,style,touch=None,name='play'):
 pg.locator('#start').click()
 if style=='aggressive':move(pg,'ArrowLeft','x',288,-1,touch);hold(pg,'ArrowUp',17,touch);fire_to(pg,30,touch,name)
 else:
  move(pg,'ArrowLeft','x',192,-1,touch);move(pg,'ArrowUp','y',480,-1,touch);move(pg,'ArrowRight','x',288,1,touch);hold(pg,'ArrowUp',17,touch);fire_to(pg,6,touch,name)
  for n in range(6,34,3):
   if snap(pg)['state']['complete']:break
   move(pg,'ArrowRight','x',384,1,touch);wait_time(pg,n+1.8);move(pg,'ArrowLeft','x',288,-1,touch);hold(pg,'ArrowUp',17,touch);fire_to(pg,n+3,touch,name)
 m=mission(pg);check(name+' localized result',pg.locator('#overlay-title').inner_text()==('砲壘已擊敗。' if snap(pg)['settings']['language']=='zh-TW' else 'Fortress defeated.'));check(name+' actual eight-hit victory',m['outcome']=='success' and len(m['shotHits'])==8,m);check(name+' expected health tradeoff',m['tankHP']==1 if style=='aggressive' else m['tankHP']>=2,m['tankHits']);check(name+' expected timing',9.5<=m['finishedAt']<=12 if style=='aggressive' else 20<=m['finishedAt']<=27,m['finishedAt']);check(name+' all steel remains',len([w for w in snap(pg)['state']['walls'] if w['kind']=='steel'])==5);pic(pg,name+'-victory');plays.append(dict(name=name,style=style,input='CDP touch' if touch else 'keyboard',finishedAt=m['finishedAt'],tankHP=m['tankHP'],shotHits=m['shotHits'],tankHits=m['tankHits'],coverHits=m['coverHits'],volleys=m['volleys']));pg.locator('#start').click();check(name+' fresh retry cover and health',mission(pg)['elapsed']==0 and mission(pg)['fortressHP']==8 and mission(pg)['tankHP']==3 and len([w for w in snap(pg)['state']['walls'] if w['kind']=='brick'])==4);pg.locator('#pause').click()
def defeat(pg,touch=None,name='defeat'):
 pg.locator('#start').click();move(pg,'ArrowLeft','x',288,-1,touch);until(pg,lambda:snap(pg)['state']['complete']);m=mission(pg);check(name+' localized defeat',pg.locator('#overlay-title').inner_text()==('守護者已被摧毀。' if snap(pg)['settings']['language']=='zh-TW' else 'Guardian destroyed.'));check(name+' three effective hits cause defeat',m['outcome']=='defeat' and m['tankHP']==0 and len(m['tankHits'])==3);check(name+' immunity intervals',all(b['time']-a['time']>=3-1e-8 for a,b in zip(m['tankHits'],m['tankHits'][1:])));pic(pg,name);plays.append(dict(name=name,style='no-fire defeat',finishedAt=m['finishedAt'],tankHP=m['tankHP'],tankHits=m['tankHits']));pg.locator('#start').click();pg.locator('#level-exit').click();pg.locator('#confirm-reset').click();check(name+' actual exit returns range',snap(pg)['scene']=='range');pg.locator('#choose-siege').click()
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);c=b.new_context(viewport=dict(width=1440,height=1000));pg=ready(c);pic(pg,'desktop-entry');pg.clock.run_for(3000);check('entry waits for input',mission(pg)['elapsed']==0);pg.locator('#start').click();wait_time(pg,2.7);check('precharge localized and locked',visual(pg)['status']=='charging' and mission(pg)['chargedGun']==1);pic(pg,'desktop-charge');render_check(pg,'charge');pg.locator('#pause').click();before=snap(pg)['state'];pg.clock.run_for(5000);check('pause freezes all state/charge/protection',before==snap(pg)['state']);pg.locator('#start').click();pg.clock.run_for(16);check('resume no catchup',mission(pg)['elapsed']-before['siege']['elapsed']<.05)
 pg.evaluate("Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'))");saved=snap(pg)['state'];pg.clock.run_for(3000);check('hidden lifecycle freezes',snap(pg)['paused'] and snap(pg)['state']==saved);pg.evaluate("Object.defineProperty(document,'hidden',{configurable:true,get:()=>false})");pg.locator('#start').click();wait_time(pg,3.2);render_check(pg,'five-shot fan');check('exact five-round launch',len(mission(pg)['enemyShells'])==5 and len(mission(pg)['volleys'][0]['directions'])==5);pic(pg,'desktop-five-shells');wait_time(pg,6.2);check('cadence remains3s',[v['time'] for v in mission(pg)['volleys']]==[3,6]);pg.locator('#restart').click();pg.locator('#cancel-reset').click();check('cancel restart retains encounter',mission(pg)['elapsed']>6 and not snap(pg)['paused']);pg.locator('#restart').click();pg.locator('#confirm-reset').click();before=snap(pg)['state'];pg.locator('#language').click();check('live Chinese preserves full state',snap(pg)['state']==before and pg.locator('#range-title').inner_text()=='圍城');pg.locator('#language').click();pg.locator('#boss-motion').click();check('reduced motion toggle',snap(pg)['reduced']);pg.locator('#boss-motion').click();pg.locator('#boss-sound').click();check('sound toggle',not snap(pg)['settings']['muted']);pg.locator('#boss-sound').click();pg.locator('#pause').click();play(pg,'aggressive',name='keyboard-aggressive');play(pg,'tactical',name='keyboard-tactical');defeat(pg,name='keyboard-defeat');pg.locator('#start').click();move(pg,'ArrowRight','x',608,1);move(pg,'ArrowUp','y',288,-1);wait_time(pg,5.7);check('right roof gun selected in actual oblique approach',mission(pg)['chargedGun']==2);render_check(pg,'right-gun-charge');pic(pg,'right-gun-charge');wait_time(pg,6.15);render_check(pg,'right-gun-volley');check('right roof gun launch emits five fixed rays',mission(pg)['lastVolley']['gun']==2 and len(mission(pg)['volleys'][-1]['directions'])==5);pic(pg,'right-gun-volley');c.close()
 c=b.new_context(viewport=dict(width=390,height=844),device_scale_factor=2,is_mobile=True,has_touch=True);pg=ready(c);touch=Touch(pg,c);play(pg,'aggressive',touch,'touch-aggressive');play(pg,'tactical',touch,'touch-tactical');defeat(pg,touch,'touch-defeat');pg.locator('#start').click();before=snap(pg)['state'];touch.start('ArrowLeft',True);pg.clock.run_for(100);touch.end();after=snap(pg)['state'];check('simultaneous two-finger move/fire',after['tank']['x']<before['tank']['x'] and after['shots']>before['shots']);c.close()
 for width,height in[(320,740),(390,844),(768,1024),(1440,900),(844,390)]:
  c=b.new_context(viewport=dict(width=width,height=height),has_touch=True,reduced_motion='reduce');pg=ready(c);a=pg.locator('#arena').bounding_box();start=pg.locator('#start').bounding_box();check(str(width)+' entry fits',start['y']>=a['y'] and start['y']+start['height']<=a['y']+a['height']);pg.locator('#start').click();wait_time(pg,3.2)
  for lang in['en','zh-TW']:
   if snap(pg)['settings']['language']!=lang:pg.locator('#language').click()
   pic(pg,f'viewport-{width}x{height}-{lang}');metrics=pg.evaluate("""()=>({overflow:document.documentElement.scrollWidth>innerWidth,targets:[...document.querySelectorAll('[data-dir],#fire,.boss-settings button,#choose-siege')].map(e=>{const b=e.getBoundingClientRect();return[b.width,b.height]}),pause:document.querySelector('#pause').getBoundingClientRect().top,hud:document.querySelector('#boss-hud').getBoundingClientRect().top,fire:document.querySelector('#fire').getBoundingClientRect().bottom})""");check(f'{width} {lang} layout/44px targets',not metrics['overflow'] and all(w>=44 and h>=44 for w,h in metrics['targets']),metrics)
   if width in[320,390]:check(f'{width} {lang} portrait controls/HUD visible',metrics['pause']>=-1 and metrics['hud']>=-1 and metrics['fire']<=height,metrics)
   if width in[320,390,1440]:
    pg.locator('#pause').click();pg.clock.resume();pg.add_script_tag(path=os.environ.get('AXE_PATH','/tmp/armorheart-audit/node_modules/axe-core/axe.min.js'));audit=pg.evaluate("""async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}});return{violations:r.violations,passes:r.passes.length,incomplete:r.incomplete.map(x=>({id:x.id,impact:x.impact}))}}""");(OUT/f'axe-{width}-{lang}.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n');check(f'{width} {lang} axe zero reported violations',not audit['violations'],[v['id'] for v in audit['violations']]);pg.locator('#start').click()
  c.close()
 for style in['aggressive','tactical','defeat']:
  c=b.new_context();n=len(network);pg=ready(c,True)
  if style in ['aggressive','defeat']:pg.locator('#language').click()
  if style=='defeat':defeat(pg,name='offline-defeat')
  else:play(pg,style,name='offline-'+style)
  check('offline only initial HTML '+style,network[n:]==['http://127.0.0.1:8080/preview/guardian.html'],network[n:]);c.close()
 check('no page JavaScript errors',not errors,errors);check('no external runtime HTTP',not[u for u in network if not u.startswith('http://127.0.0.1:8080')]);b.close()
(OUT/'browser-results.json').write_text(json.dumps(dict(date='2026-11-04 Asia/Taipei',passed=len(results),failed=0,tests=results,playthroughs=plays,errors=errors,method='Actual keyboard/CDP touch with controlled clock, forwarding Canvas measurements and read-only game snapshots; no gameplay fixtures',independent_first_time_player='Not performed',physical_phone='Not performed',other_browser_engines='Not performed'),indent=2,ensure_ascii=False)+'\n');print(json.dumps(dict(passed=len(results),failed=0,plays=[{k:v for k,v in r.items() if k in['name','finishedAt','tankHP']}for r in plays])))
