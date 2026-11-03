"""Actual-render P1 evidence, with baseline positive controls.
Initial pose-only HTTP fixtures isolate recoil. Departure uses real maze/keyboard.
Browser clock controls time; simulation state is read-only.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,time,subprocess,os
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/os.environ.get('EVIDENCE_DIR','evidence/r3-visual');TMP=OUT/'tmp';TMP.mkdir(parents=True,exist_ok=True)
BASE='7d9720d8cee846735d5f1bb2dfc231b66eb4af7c';oldapp=subprocess.check_output(['git','show',BASE+':src/app.mjs'],cwd=ROOT).decode()
results=[];traces=[];errors=[];film=[]
def check(name,ok,detail=None):
 results.append(dict(name=name,passed=bool(ok),detail=detail))
 if not ok:raise AssertionError((name,detail))
def snap(pg):return pg.evaluate('guardianPOC.snapshot()')
def fixture(c,facing):
 src=(ROOT/'src/engine.mjs').read_text();a=src.index('export function createState()');b=src.index('\n}',a)
 part=src[a:b].replace('return {time:0','const initial={time:0');part+='\n initial.tank='+json.dumps(dict(x=384,y=384,facing=facing))+'; initial.walls=[]; return initial;'
 c.route('**/src/engine.mjs',lambda r:r.fulfill(body=src[:a]+part+src[b:],content_type='text/javascript'))
def ready(c,baseline=False):
 if baseline:c.route('**/src/app.mjs',lambda r:r.fulfill(body=oldapp,content_type='text/javascript'))
 pg=c.new_page();pg.on('pageerror',lambda e:errors.append(str(e)));pg.clock.install();pg.goto('http://127.0.0.1:8080/');pg.wait_for_function('window.guardianPOC');pg.clock.pause_at(int(time.time()*1000)+1000);return pg
def audit(pg):
 return pg.evaluate('''async()=>{
 const s=guardianPOC.snapshot(),arena=document.querySelector('#arena'),w=arena.width,k=w/768;
 window.__visualLayers??=await Promise.all(['hull','barrel'].map(async n=>{const im=new Image();im.src='/assets/guardian/'+n+'.svg';await im.decode();return im;}));
 const render=(order)=>{const c=document.createElement('canvas');c.width=c.height=w;const g=c.getContext('2d');g.scale(k,k);g.translate(s.state.tank.x,s.state.tank.y);g.rotate({up:-Math.PI/2,right:0,down:Math.PI/2,left:Math.PI}[s.state.tank.facing]);g.scale(.5,.5);for(const i of order)g.drawImage(__visualLayers[i],-107-(i===1?s.barrelOffsetMasterPx:0),-128);return g.getImageData(0,0,w,w).data;};
 const hull=render([0]),barrel=render([1]),want=render([1,0]),old=render([0,1]),actual=arena.getContext('2d').getImageData(0,0,w,w).data;
 let overlap=0,mismatches=0,oldWitness=0,visibleBarrel=0;
 for(let i=0;i<hull.length;i+=4){if(hull[i+3]===255&&barrel[i+3]>0){overlap++;if([0,1,2].some(j=>Math.abs(actual[i+j]-want[i+j])>1))mismatches++;if([0,1,2].some(j=>Math.abs(old[i+j]-want[i+j])>1))oldWitness++;}if(hull[i+3]===0&&barrel[i+3]>200)visibleBarrel++;}
 return {age:s.state.time-s.state.firedAt,offset:s.barrelOffsetMasterPx,tank:s.state.tank,shots:s.state.shots,overlapPixels:overlap,mismatches,oldOrderWitnessPixels:oldWitness,visibleBarrelPixels:visibleBarrel};}''')
def closeup(pg,file):
 b=pg.locator('#arena').bounding_box();t=snap(pg)['state']['tank'];pg.screenshot(path=str(file),clip=dict(x=b['x']+t['x']*b['width']/768-100,y=b['y']+t['y']*b['height']/768-100,width=200,height=200))
def key(pg,k,ms):
 pg.locator('#arena').focus();pg.keyboard.down(k);pg.clock.run_for(ms);pg.keyboard.up(k)
def move(pg,k,axis,target,sign):
 pg.locator('#arena').focus();pg.keyboard.down(k)
 for _ in range(250):
  d=(target-snap(pg)['state']['tank'][axis])*sign
  if d<=0:break
  pg.clock.run_for(100 if d>30 else 16)
 else:raise AssertionError(('blocked',snap(pg)['state']['tank']))
 pg.keyboard.up(k)
def fire(pg,cell):
 pg.keyboard.down('Space')
 for _ in range(100):
  if not any(w['id']==cell for w in snap(pg)['state']['walls']):break
  pg.clock.run_for(16)
 else:raise AssertionError('shot blocked')
 pg.keyboard.up('Space')
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 # A positive control renders the exact old app with otherwise byte-identical data.
 c=browser.new_context(viewport=dict(width=1440,height=1000));fixture(c,'right');pg=ready(c,True);pg.locator('#start').click();key(pg,'Space',64);r=audit(pg)
 check('baseline reproduces barrel-over-turret defect',r['mismatches']>0,r);closeup(pg,OUT/'before-barrel-right.png');c.close()
 for width,height,dpr in [(1440,1000,1),(390,844,2)]:
  for facing in ['up','right','down','left']:
   c=browser.new_context(viewport=dict(width=width,height=height),device_scale_factor=dpr,is_mobile=width<500,has_touch=True);fixture(c,facing);pg=ready(c);pg.locator('#start').click();pg.locator('#arena').scroll_into_view_if_needed();pg.clock.run_for(32)
   r=audit(pg);check(f'{width} {facing} rest mounting occlusion',r['mismatches']==0 and r['oldOrderWitnessPixels']>0 and r['visibleBarrelPixels']>0,r);closeup(pg,OUT/f'rest-{width}-{facing}.png')
   initial=snap(pg)['state']['tank'];pg.locator('#arena').focus();pg.keyboard.down('Space');rows=[];peak=-1
   for i in range(19):
    pg.clock.run_for(17);r=audit(pg);rows.append(r)
    check(f'{width} {facing} recoil frame{i} mounting occlusion',r['mismatches']==0 and r['visibleBarrelPixels']>0 and r['tank']==initial,r)
    if r['offset']>peak:peak=r['offset'];closeup(pg,OUT/f'peak-{width}-{facing}.png')
    if i==7:closeup(pg,OUT/f'returning-{width}-{facing}.png')
    if width==1440:
     file=TMP/f'film-{facing}-{i:02d}.png';closeup(pg,file);film.append((file,1/60))
   pg.keyboard.up('Space');check(f'{width} {facing} fixed hull and accepted recoil range',9<peak<=12 and rows[-1]['offset']==0 and rows[-1]['shots']==1,dict(peak=peak,returned=rows[-1]['offset']))
   closeup(pg,OUT/f'returned-{width}-{facing}.png');pg.screenshot(path=str(OUT/f'actual-range-{width}-{facing}.png'),full_page=True)
   if width==1440:film.append((file,.7))
   traces.append(dict(viewport=[width,height],dpr=dpr,facing=facing,rows=rows));c.close()
 # Capture true route opening in baseline/current desktop and narrow-phone apps.
 for width,height in [(1440,1000),(320,740)]:
  for baseline in [True,False]:
   c=browser.new_context(viewport=dict(width=width,height=height),device_scale_factor=1,has_touch=True)
   c.add_init_script('''(()=>{window.__truckBoxes=[];const f=CanvasRenderingContext2D.prototype.strokeRect;CanvasRenderingContext2D.prototype.strokeRect=function(x,y,w,h){if(this.canvas.id==='arena'&&x<0&&y<0&&w>=120&&w<=160&&h>=50&&h<=100)__truckBoxes.push({x,y,w,h,time:performance.now()});return f.call(this,x,y,w,h);};})();''')
   pg=ready(c,baseline);pg.locator('#choose-mission').click();pg.locator('#start').click();pg.locator('#arena').scroll_into_view_if_needed();name=('before' if baseline else 'after')+f'-departure-{width}'
   check(name+' waiting has no box',pg.evaluate('__truckBoxes.length')==0)
   move(pg,'ArrowUp','y',400,-1);move(pg,'ArrowLeft','x',288,-1);move(pg,'ArrowUp','y',160,-1);key(pg,'ArrowRight',64);fire(pg,'U0');fire(pg,'U1')
   for stage,ms in [('open',17),('moving',250),('cue-window',1000),('post-cue',1200)]:
    pg.clock.run_for(ms);m=snap(pg)['state']['mission'];n=pg.evaluate('__truckBoxes.length')
    check(name+' '+stage+' box '+('reproduced' if baseline else 'absent'),n>0 if baseline else n==0,dict(strokes=n,phase=m['phase'],truck=m['truck']))
    if stage in ['open','cue-window']:pg.screenshot(path=str(OUT/f'{name}-{stage}.png'),full_page=True)
   check(name+' localized announcement and HUD retained',pg.locator('#announcement').inner_text()=='Route open. The transport is evacuating.' and pg.locator('#mission-status').inner_text()=='Route open · evacuating')
   before=snap(pg)['state']['mission'];pg.locator('#language').click();check(name+' live Traditional Chinese cue retained',pg.locator('#announcement').inner_text()=='路線已暢通，運輸車開始撤離。' and snap(pg)['state']['mission']==before);pg.screenshot(path=str(OUT/f'{name}-zh-TW.png'),full_page=True);c.close()
 check('no visual-suite runtime errors',not errors,errors);browser.close()
# Encode the actual screenshot samples, never synthesize the occlusion.
concat=TMP/'visual-frames.txt';concat.write_text('\n'.join("file '"+str(f)+"'\nduration "+str(d) for f,d in film)+'\n')
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-vf','scale=600:600:flags=neighbor','-c:v','libvpx-vp9','-crf','28','-b:v','0','-pix_fmt','yuv420p',str(OUT/'four-facing-occlusion.webm')],check=True)
(OUT/'occlusion-traces.json').write_text(json.dumps(traces,indent=2)+'\n')
(OUT/'visual-results.json').write_text(json.dumps(dict(date='2026-11-03 Asia/Taipei',baseline=BASE,passed=len(results),failed=0,tests=results,method='Actual Chromium frames; initial-pose-only fixtures for recoil, real keyboard maze for departure; clock controlled; read-only simulation',recording='Actual 60Hz screenshot samples, enlarged3x nearest-neighbor; one shot per facing, up/right/down/left, rest hold between facings; not generated animation',errors=errors),indent=2,ensure_ascii=False)+'\n')
print(json.dumps(dict(passed=len(results),failed=0)))
