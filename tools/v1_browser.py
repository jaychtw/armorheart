"""Integrated RC actual-input campaigns, cosmetic equivalence, storage and layout checks.
Main campaigns earn unlocks through real input; storage/equivalence fixtures are labeled.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,os,time,math,base64,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence/v1';OUT.mkdir(exist_ok=True)
IDS=['breakthrough','colossus','interception','siege'];TANKS=['guardian','bulwark','vanguard','sentinel'];NAV=dict(zip(IDS,['#choose-mission','#choose-colossus','#choose-ship','#choose-siege']));KEY='armorheart-progress'
STAMP=hashlib.sha256(b''.join((ROOT/p).read_bytes() for p in ['src/app.mjs','src/progress.mjs','src/i18n.mjs','index.html','style.css','assets/tanks/manifest.json','preview/guardian.html'])).hexdigest()
assets={}
for n in TANKS:
 for part in ['hull','barrel']:
  path=('assets/guardian/' if n=='guardian' else 'assets/tanks/'+n+'/')+part+'.svg';uri='data:image/svg+xml;base64,'+base64.b64encode((ROOT/path).read_bytes()).decode();assets[uri]=[n,part];assets[path]=[n,part]
INIT='''(()=>{const pairs=PAIRS,m=new Map();for(const[k,v]of Object.entries(pairs))m.set(k.startsWith('data:')?k:new URL(k,location.href).href,v);const p=CanvasRenderingContext2D.prototype,c=p.clearRect,d=p.drawImage;window.tankPaint=[];p.clearRect=function(...args){if(this.canvas.id==='arena')window.tankPaint=[];return c.apply(this,args)};p.drawImage=function(im,...args){const id=m.get(im.currentSrc||im.src);if(id&&this.canvas.id==='arena'){const q=this.getTransform(),s=this.canvas.width/768;tankPaint.push({id, args,x:q.e/s,y:q.f/s,a:q.a/s,b:q.b/s,c:q.c/s,d:q.d/s});}return d.call(this,im,...args)}})()'''.replace('PAIRS',json.dumps(assets))
results=[];errors=[];requests=[];plays=[]
def check(name,ok,detail=None):
 results.append(dict(name=name,passed=bool(ok),detail=detail))
 if not ok:raise AssertionError((name,detail))
def snap(pg):return pg.evaluate('guardianPOC.snapshot()')
def photo(pg,name):pg.screenshot(path=str(OUT/(name+'.png')),full_page=True)
def ready(c,offline=False,seed=None,deny=False,quota=False):
 pg=c.new_page();pg.clock.install();pg.add_init_script(INIT);pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
 if seed is not None:pg.add_init_script('''if(!sessionStorage.getItem('v1-test-fixture')){localStorage.setItem('armorheart-progress',RAW);sessionStorage.setItem('v1-test-fixture','yes');}'''.replace('RAW',json.dumps(seed if isinstance(seed,str) else json.dumps(seed))))
 if deny:pg.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Blocked','SecurityError')}})")
 if quota:pg.add_init_script("const set=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k==='armorheart-progress')throw new DOMException('Quota','QuotaExceededError');return set.call(this,k,v)}")
 url='http://127.0.0.1:8080/'+('preview/guardian.html' if offline else '')
 if offline:pg.route('**/*',lambda r:r.continue_() if r.request.url==url else r.abort())
 pg.goto(url);pg.wait_for_function('window.guardianPOC');pg.clock.pause_at(int(time.time()*1000)+1000);return pg
class Touch:
 def __init__(self,pg,c):self.pg=pg;self.cdp=c.new_cdp_session(pg)
 def start(self,k=None,fire=False):
  self.pg.locator('#fire').scroll_into_view_if_needed();sels=[]
  if k:sels.append('[data-dir="'+{'ArrowUp':'up','ArrowDown':'down','ArrowLeft':'left','ArrowRight':'right'}[k]+'"]')
  if fire:sels.append('#fire')
  pts=[]
  for i,sel in enumerate(sels):
   r=self.pg.locator(sel).bounding_box();pts.append(dict(id=i+1,x=r['x']+r['width']/2,y=r['y']+r['height']/2))
  self.cdp.send('Input.dispatchTouchEvent',dict(type='touchStart',touchPoints=pts))
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
 for _ in range(300):
  d=(target-snap(pg)['state']['tank'][axis])*sign
  if d<=0:break
  pg.clock.run_for(100 if d>30 else 16)
 else:raise AssertionError(('blocked actual movement',target,snap(pg)['state']['tank']))
 if touch:touch.end()
 else:pg.keyboard.up(k)
def until(pg,fn,limit=1800):
 for _ in range(limit):
  if fn():return
  pg.clock.run_for(32)
 raise AssertionError(('condition timeout',snap(pg)))
def fire_until(pg,fn,touch=None):
 if touch:touch.start(fire=True)
 else:pg.locator('#arena').focus();pg.keyboard.down('Space')
 until(pg,fn)
 if touch:touch.end()
 else:pg.keyboard.up('Space')
def render_check(pg,label):
 s=snap(pg);draws=pg.evaluate('tankPaint');check(label+' actual registered tank pair',len(draws)>=2 and [d['id'] for d in draws[-2:]]==[[s['activeTank'],'barrel'],[s['activeTank'],'hull']]);b,h=draws[-2:];check(label+' shared barrel recoil/occlusion',abs(b['args'][0]+107+s['barrelOffsetMasterPx'])<1e-6 and b['args'][1]==-128 and h['args']==[-107,-128]);a={'right':0,'down':math.pi/2,'left':math.pi,'up':-math.pi/2}[s['state']['tank']['facing']];check(label+' same tank pivot/scale',max(abs(h['x']-s['state']['tank']['x']),abs(h['y']-s['state']['tank']['y']),abs(h['a']-.5*math.cos(a)),abs(h['b']-.5*math.sin(a)))<1e-4)
def play_current(pg,id,touch=None,label='play'):
 if not snap(pg)['started'] or snap(pg)['paused'] or snap(pg)['state']['complete']:pg.locator('#start').click()
 skin=snap(pg)['activeTank']
 if id=='siege':move(pg,'ArrowLeft','x',288,-1,touch);hold(pg,'ArrowUp',17,touch);fire_until(pg,lambda:snap(pg)['state']['complete'],touch)
 elif id=='colossus':move(pg,'ArrowRight','x',560,1,touch);hold(pg,'ArrowUp',32,touch);fire_until(pg,lambda:snap(pg)['state']['complete'],touch)
 elif id=='interception':
  hold(pg,'ArrowLeft',675,touch);hold(pg,None,1225,touch,True);move(pg,'ArrowRight','x',384,1,touch);hold(pg,'ArrowUp',32,touch);fire_until(pg,lambda:snap(pg)['state']['complete'],touch)
 else:
  move(pg,'ArrowUp','y',400,-1,touch);move(pg,'ArrowLeft','x',288,-1,touch);move(pg,'ArrowUp','y',160,-1,touch);hold(pg,'ArrowRight',64,touch)
  for cell in ['U0','U1']:fire_until(pg,lambda cell=cell:not any(w['id']==cell for w in snap(pg)['state']['walls']),touch)
  until(pg,lambda:snap(pg)['state']['complete'])
 s=snap(pg);m=s['state']['mission'] if id=='breakthrough' else s['state'][id];won=m['phase']=='success' if id=='breakthrough' else m['outcome']=='success';check(label+' actual mission victory',won,m);render_check(pg,label);photo(pg,label+'-victory');plays.append(dict(name=label,mission=id,tank=skin,input='CDP touch' if touch else 'keyboard',time=m.get('finishedAt',m.get('elapsed')),hp=m.get('tankHP'),completed=s['campaign']['completed']))
 return s

def campaigns(b):
 for mode,order in [('keyboard',['siege','interception','colossus','breakthrough']),('touch',IDS),('offline',['colossus','siege','breakthrough','interception'])]:
  mobile=mode=='touch';c=b.new_context(viewport=dict(width=390,height=844) if mobile else dict(width=1440,height=1000),device_scale_factor=2 if mobile else 1,is_mobile=mobile,has_touch=mobile);n=len(requests);pg=ready(c,offline=mode=='offline');touch=Touch(pg,c) if mobile else None
  if mode=='offline':pg.locator('#language').click()
  check(mode+' fresh collection',snap(pg)['campaign']['completed']==[] and pg.locator('#tank-sentinel').is_disabled());photo(pg,mode+'-collection-zero')
  for i,id in enumerate(order):
   if snap(pg)['scene']!='range':pg.locator('#choose-range').click()
   pg.locator('#tank-'+TANKS[i]).click();check(mode+' selects earned tank '+TANKS[i],snap(pg)['campaign']['selected']==TANKS[i]);pg.locator(NAV[id]).click();check(mode+' applies selection on new mission '+id,snap(pg)['activeTank']==TANKS[i]);play_current(pg,id,touch,mode+'-'+id)
   p=snap(pg)['campaign'];check(mode+' exactly one distinct grant '+id,p['completed']==order[:i+1]);check(mode+' no fifth tank',len(pg.locator('.tank-grid button').all())==4);check(mode+' reward is visible '+id,pg.locator('#result-reward').is_visible());check(mode+' canonical Next '+id,pg.locator('#result-next').is_visible()==(id!='siege'));before=p;pg.locator('#language').click();pg.locator('#language').click();check(mode+' re-rendering result does not regrant '+id,snap(pg)['campaign']==before)
   if i==0 and mode=='keyboard':
    pg.locator('#start').click();check('Replay does not clear campaign',snap(pg)['campaign']==before);play_current(pg,id,touch,'keyboard-repeat-siege');check('actual repeated win grants nothing',snap(pg)['campaign']==before and 'unchanged' in pg.locator('#result-reward').inner_text())
   if i==3:check(mode+' fourth distinct clear earns commendation',snap(pg)['campaign']['completed']==order and ('commendation' in pg.locator('#result-reward').inner_text().lower() or '嘉獎' in pg.locator('#result-reward').inner_text()));photo(pg,mode+'-commendation')
   if id!='siege':
    pg.locator('#result-next').click();check(mode+' Next navigates only '+id,snap(pg)['scene']==IDS[IDS.index(id)+1] and snap(pg)['campaign']==before and not snap(pg)['started']);pg.locator('#choose-range').click()
   else:pg.locator('#result-select').click();check(mode+' last-stage Missions returns selector',snap(pg)['scene']=='range')
  check(mode+' all four persistent marks',len(pg.locator('.completion-mark').all())==4);check(mode+' commendation visible on selector',pg.locator('#campaign-commendation').is_visible());check(mode+' four selectable cosmetics',all(pg.locator('#tank-'+x).is_enabled() for x in TANKS));photo(pg,mode+'-collection-complete')
  if mode!='offline':
   before=snap(pg)['campaign'];pg.reload();pg.wait_for_function('guardianPOC');pg.clock.pause_at(int(time.time()*1000)+1000);check(mode+' reload retains history/selection',snap(pg)['campaign']==before and snap(pg)['activeTank']==before['selected']);check(mode+' reload retains commendation',pg.locator('#campaign-commendation').is_visible())
  else:check('offline full campaign uses initial HTML only',requests[n:]==['http://127.0.0.1:8080/preview/guardian.html'],requests[n:])
  c.close()

def cosmetics(b):
 traces=[]
 for name in TANKS:
  # Explicit earned-progress storage fixture isolates visual/physical equivalence; campaigns above earn it normally.
  c=b.new_context(viewport=dict(width=390,height=844),device_scale_factor=2,has_touch=True);pg=ready(c,seed={'version':1,'completed':IDS,'selected':name});pg.locator('#start').click();check(name+' selected fixture applies visually',snap(pg)['activeTank']==name)
  for direction in ['ArrowUp','ArrowRight','ArrowDown','ArrowLeft']:
   hold(pg,direction,64);render_check(pg,name+' '+direction+' rest');photo(pg,name+'-'+direction+'-rest');hold(pg,None,48,fire=True);render_check(pg,name+' '+direction+' recoil');check(name+' '+direction+' recoil actually active',snap(pg)['barrelOffsetMasterPx']>0);photo(pg,name+'-'+direction+'-recoil');pg.clock.run_for(1050)
  pg.locator('#restart').click();pg.locator('#confirm-reset').click();move(pg,'ArrowLeft','x',288,-1);move(pg,'ArrowUp','y',400,-1);hold(pg,'ArrowLeft',1000);before=snap(pg)['state']['tank'];hold(pg,'ArrowUp',32);hold(pg,'ArrowLeft',32);after=snap(pg)['state']['tank'];check(name+' blocked turn remains immediate',after['facing']=='left' and abs(after['x']-before['x'])<1e-6,(before,after));render_check(pg,name+' blocked turn');traces.append(dict(tank=name,pose=after,shots=snap(pg)['state']['shots'],time=snap(pg)['state']['time']));c.close()
 for r in traces[1:]:check(r['tank']+' actual blocked physical pose matches Guardian',r['pose']==traces[0]['pose'],r['pose'])
 c=b.new_context(viewport=dict(width=390,height=844),is_mobile=True,has_touch=True);pg=ready(c,seed={'version':1,'completed':IDS,'selected':'sentinel'});pg.locator('#choose-siege').click();pg.locator('#start').click();t=Touch(pg,c);before=snap(pg)['state'];t.start('ArrowLeft',True);pg.clock.run_for(100);t.end();after=snap(pg)['state'];check('alternate skin simultaneous two-finger move/fire',after['tank']['x']<before['tank']['x'] and after['shots']>before['shots']);render_check(pg,'Sentinel two-finger');photo(pg,'sentinel-touch-simultaneous');c.close()
 (OUT/'cosmetic-traces.json').write_text(json.dumps({'method':'Actual unchanged game input; earned-progress fixture only for access; no pose or rule fixtures','traces':traces},indent=2)+'\n')

def storage_checks(b):
 for n in range(5):
  c=b.new_context();pg=ready(c,seed={'version':1,'completed':IDS[:n],'selected':'sentinel'});p=snap(pg)['campaign'];check(str(n)+' completion-count state validates',len(p['completed'])==n and p['selected']==('sentinel' if n>=3 else 'guardian'));check(str(n)+' unlocked button count',sum(pg.locator('#tank-'+t).is_enabled() for t in TANKS)==min(4,n+1));check(str(n)+' commendation threshold',pg.locator('#campaign-commendation').is_visible()==(n==4));before=p;pg.reload();pg.wait_for_function('guardianPOC');check(str(n)+' completion state survives reload',snap(pg)['campaign']==before);c.close()
 for label,kwargs in [('denied',dict(deny=True)),('quota',dict(quota=True)),('corrupt',dict(seed='{bad')),('future',dict(seed={'version':99,'completed':IDS,'selected':'sentinel'}))]:
  c=b.new_context(viewport=dict(width=320,height=740));pg=ready(c,**kwargs);check(label+' no unearned unlock',snap(pg)['campaign']['completed']==[]);pg.locator('#choose-siege').click();play_current(pg,'siege',label=label+'-actual-win');check(label+' session win retained',snap(pg)['campaign']['completed']==['siege']);pg.locator('#result-select').click();pg.locator('#tank-bulwark').click();check(label+' earned selection works',snap(pg)['activeTank']=='bulwark');photo(pg,label+'-save-state')
  if label in ['denied','quota']:check(label+' session disclosure visible',snap(pg)['progressStorage']=='session' and pg.locator('#progress-warning').is_visible())
  elif label=='corrupt':check('corrupt save recovers after actual victory',snap(pg)['progressStorage']=='saved' and json.loads(pg.evaluate("localStorage.getItem('armorheart-progress')"))['completed']==['siege'])
  else:check('future save preserved after actual win',snap(pg)['progressStorage']=='newer' and json.loads(pg.evaluate("localStorage.getItem('armorheart-progress')"))['version']==99)
  pg.reload();pg.wait_for_function('guardianPOC');check(label+' reload degrades safely',len(snap(pg)['campaign']['completed'])==(1 if label=='corrupt' else 0));c.close()
 c=b.new_context();pg=ready(c,seed={'version':0,'completedMissions':['siege','colossus'],'selectedTank':'vanguard'});check('v0 persisted migration',snap(pg)['campaign']=={'version':1,'completed':['siege','colossus'],'selected':'vanguard'} and json.loads(pg.evaluate("localStorage.getItem('armorheart-progress')"))['version']==1);c.close()
 c=b.new_context();pg=ready(c);pg.locator('#choose-siege').click();pg.locator('#start').click();move(pg,'ArrowLeft','x',288,-1);until(pg,lambda:snap(pg)['state']['complete']);check('actual defeat grants no campaign progress',snap(pg)['state']['siege']['outcome']=='defeat' and not snap(pg)['campaign']['completed']);check('defeat offers Retry/Missions without Next',pg.locator('#start').is_visible() and pg.locator('#result-select').is_visible() and not pg.locator('#result-next').is_visible());photo(pg,'campaign-defeat-no-reward');pg.locator('#start').click();check('Retry is level-only',snap(pg)['state']['siege']['fortressHP']==8 and not snap(pg)['campaign']['completed']);c.close()

def layouts(b):
 for w,h in[(320,740),(390,844),(768,1024),(1440,1000),(844,390)]:
  for completed in [[],IDS]:
   c=b.new_context(viewport=dict(width=w,height=h),has_touch=True,reduced_motion='reduce');pg=ready(c,seed={'version':1,'completed':completed,'selected':'sentinel' if completed else 'guardian'})
   for lang in ['en','zh-TW']:
    if snap(pg)['settings']['language']!=lang:pg.locator('#language').click()
    photo(pg,f'menu-{w}-{lang}-count{len(completed)}');m=pg.evaluate("""()=>({overflow:document.documentElement.scrollWidth>innerWidth,targets:[...document.querySelectorAll('#scenario-chooser button,.tank-grid button')].map(e=>{const r=e.getBoundingClientRect();return[r.width,r.height]})})""");check(f'{w} {lang} menu{len(completed)} responsive/targets',not m['overflow'] and all(x>=44 and y>=44 for x,y in m['targets']),m)
    if w in[320,390,1440] and (completed or w==320):
     pg.clock.resume();pg.add_script_tag(path='/tmp/armorheart-audit/node_modules/axe-core/axe.min.js');audit=pg.evaluate("""async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}});return{violations:r.violations,passes:r.passes.length,incomplete:r.incomplete.map(x=>({id:x.id,impact:x.impact}))}}""");(OUT/f'axe-{w}-{lang}-count{len(completed)}.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n');check(f'{w} {lang} count{len(completed)} axe zero violations',not audit['violations'],[v['id'] for v in audit['violations']]);pg.clock.pause_at(int(time.time()*1000)+1000)
   pg.locator('#choose-siege').click();pg.locator('#start').click();pg.clock.run_for(100);m=pg.evaluate("""()=>({overflow:document.documentElement.scrollWidth>innerWidth,head:document.querySelector('#pause').getBoundingClientRect().top,fire:document.querySelector('#fire').getBoundingClientRect().bottom})""");check(f'{w} play layout no overflow',not m['overflow']);
   if w in[320,390]:check(f'{w} play Pause/Fire fit portrait',m['head']>=-1 and m['fire']<=h,m)
   check(f'{w} reduced motion applies',snap(pg)['reduced'] and pg.evaluate("document.body.classList.contains('reduce-motion')"));c.close()
 # Final result must fit the smallest arena with all three navigation actions and reward text.
 c=b.new_context(viewport=dict(width=320,height=740));pg=ready(c);pg.locator('#choose-colossus').click();play_current(pg,'colossus',label='small-first-unlock')
 for lang in ['en','zh-TW']:
  if snap(pg)['settings']['language']!=lang:pg.locator('#language').click()
  a=pg.locator('#arena').bounding_box();buttons=[pg.locator(s).bounding_box() for s in ['#start','#result-next','#result-select']];check(lang+' smallest result actions fit/44px',all(r['height']>=44 and r['y']>=a['y'] and r['y']+r['height']<=a['y']+a['height'] for r in buttons),(a,buttons));photo(pg,'result-320-'+lang)
 c.close()


def access(b):
 c=b.new_context(viewport=dict(width=320,height=740),reduced_motion='reduce');pg=ready(c,seed={'version':1,'completed':IDS,'selected':'guardian'});pairs=[]
 def contrast(a,b):
  def lum(c):
   q=[x/255 for x in c];q=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in q];return .2126*q[0]+.7152*q[1]+.0722*q[2]
  x,y=lum(a),lum(b);return(max(x,y)+.05)/(min(x,y)+.05)
 for name,fg,bg in [('main text',(38,56,47),(242,240,232)),('card text',(38,56,47),(250,249,244)),('locked label',(77,94,76),(226,229,217)),('collection note',(75,89,74),(236,238,227)),('commendation',(99,69,22),(239,223,180)),('reward on worst-case light underlay',(255,237,188),(57,77,64))]:
  ratio=contrast(fg,bg);pairs.append(dict(name=name,foreground=fg,background=bg,ratio=ratio));check('manual numeric contrast '+name,ratio>=4.5,ratio)
 for name in TANKS:
  pg.locator('#tank-'+name).focus();pg.keyboard.press('Enter');check('keyboard earned selection '+name,snap(pg)['campaign']['selected']==name and snap(pg)['activeTank']==name);pg.locator('#start').focus();pg.keyboard.press('Enter');hold(pg,'ArrowUp',48);hold(pg,None,48,fire=True);render_check(pg,'320px '+name);photo(pg,'game-320-'+name);pg.locator('#choose-range').click();pg.locator('#confirm-reset').click()
 pg.locator('#boss-sound').focus();pg.keyboard.press('Enter');check('keyboard sound toggle',not snap(pg)['settings']['muted']);pg.keyboard.press('Enter');pg.locator('#boss-motion').focus();pg.keyboard.press('Enter');check('keyboard motion setting overrides OS',not snap(pg)['reduced']);pg.keyboard.press('Enter');check('reduced motion restored',snap(pg)['reduced']);c.close()
 c=b.new_context(viewport=dict(width=390,height=844));pg=ready(c,seed={'version':1,'completed':['siege','interception','breakthrough'],'selected':'sentinel'});pg.locator('#choose-colossus').focus();pg.keyboard.press('Enter');play_current(pg,'colossus',label='keyboard-final-commendation');before=snap(pg)['campaign'];pg.locator('#result-next').focus();pg.keyboard.press('Enter');check('keyboard Next is canonical without reward',snap(pg)['scene']=='interception' and snap(pg)['campaign']==before);pg.locator('#choose-siege').click();pg.locator('#start').click();move(pg,'ArrowLeft','x',288,-1);until(pg,lambda:snap(pg)['state']['complete']);check('selected Sentinel defeat is labeled',pg.locator('#overlay-title').inner_text()=='Sentinel destroyed.');check('failure has no reward/Next',not pg.locator('#result-reward').is_visible() and not pg.locator('#result-next').is_visible() and snap(pg)['campaign']==before);pg.locator('#result-select').focus();pg.keyboard.press('Enter');check('keyboard Missions returns selector',snap(pg)['scene']=='range' and pg.locator('#campaign-commendation').is_visible());c.close()
 (OUT/'contrast-check.json').write_text(json.dumps({'passed':True,'method':'WCAG sRGB numeric checks of declared UI palette pairs, not full canvas/nonvisual certification; screenshots also inspected by assistant','pairs':pairs,'remaining':'Canvas contrast and human assistive-technology testing remain incomplete'},indent=2)+'\n')

PHASES={'access':access,'campaign':campaigns,'cosmetics':cosmetics,'storage':storage_checks,'layout':layouts}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for phase in (list(PHASES) if os.environ.get('V1_PHASE','all')=='all' else [os.environ['V1_PHASE']]):
  results=[];plays=[];errors=[];requests=[];PHASES[phase](b);check(phase+' no JavaScript errors',not errors,errors);check(phase+' no external runtime HTTP',not[u for u in requests if not u.startswith('http://127.0.0.1:8080')]);report={'date':'2026-11-04 Asia/Taipei','phase':phase,'product_sha256':STAMP,'passed':len(results),'failed':0,'tests':results,'playthroughs':plays,'errors':errors,'method':'Actual keyboard/CDP touch and controlled clock; main campaigns earn unlocks without fixtures; explicitly labeled storage fixtures isolate save/equivalence cases','independent_first_time_player':'Not performed','physical_phone':'Not performed'};(OUT/(phase+'-browser.json')).write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps({'phase':phase,'passed':len(results),'plays':[{'name':q['name'],'tank':q['tank'],'time':q['time']}for q in plays]}),flush=True)
 b.close()
reports=[]
for phase in PHASES:
 path=OUT/(phase+'-browser.json')
 if path.exists():
  r=json.loads(path.read_text())
  if r['product_sha256']==STAMP:reports.append(r)
if len(reports)==len(PHASES):(OUT/'browser-results.json').write_text(json.dumps({'passed':sum(r['passed'] for r in reports),'failed':0,'product_sha256':STAMP,'phases':[{k:r[k] for k in ['phase','passed','failed']}for r in reports],'reports':[r['phase']+'-browser.json'for r in reports]},indent=2)+'\n')
