"""R2 input/render checks. Fixtures replace createState's initial data only, via
Playwright's HTTP routing; production renderer/physics/input remain unchanged.
No runtime debug UI or mutable simulation API is added.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,time
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence/r2';OUT.mkdir(parents=True,exist_ok=True)
results=[]
def check(name,ok,detail=None):
    results.append(dict(name=name,passed=bool(ok),detail=detail))
    if not ok:raise AssertionError((name,detail))
def snap(pg):return pg.evaluate('guardianPOC.snapshot()')
def key(pg,key,duration):
    pg.locator('#arena').focus();pg.keyboard.down(key);pg.clock.run_for(duration);pg.keyboard.up(key)
def fixture(context,tank,walls):
    src=(ROOT/'src/engine.mjs').read_text();start=src.index('export function createState()');end=src.index('\n}',start)
    part=src[start:end].replace('return {time:0','const initial={time:0')
    part+='\n initial.tank='+json.dumps(tank)+'; initial.walls='+json.dumps(walls)+'; return initial;'
    src=src[:start]+part+src[end:]
    context.route('**/src/engine.mjs',lambda r:r.fulfill(body=src,content_type='text/javascript'))
def ready(pg):
    pg.clock.install();pg.goto('http://127.0.0.1:8080');pg.wait_for_function('window.guardianPOC')
    pg.clock.pause_at(int(time.time()*1000)+1000);pg.locator('#start').click()
def edges(pg):
    # Rasterize the actual fixed SVG layer at the runtime transform; test its
    # opaque pixels against physical wall interiors, independently of collider.
    return pg.evaluate('''async()=>{
      const s=guardianPOC.snapshot().state,c=document.createElement('canvas');c.width=c.height=768;
      const g=c.getContext('2d'),im=new Image();im.src='assets/guardian/hull.svg';await im.decode();
      g.translate(s.tank.x,s.tank.y);g.rotate({up:-Math.PI/2,right:0,down:Math.PI/2,left:Math.PI}[s.tank.facing]);g.scale(.5,.5);g.drawImage(im,-107,-128);
      const a=g.getImageData(0,0,768,768).data;let overlap=0;
      for(const w of s.walls)for(let y=w.y+1;y<w.y+63;y++)for(let x=w.x+1;x<w.x+63;x++)if(a[(y*768+x)*4+3]>200)overlap++;
      return {overlap,tank:s.tank};}''')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height,dpr in [(1440,1000,1),(390,844,2)]:
  for kind in ['brick','steel']:
   for facing,dx,dy,keyname in [('up',0,-1,'ArrowUp'),('right',1,0,'ArrowRight'),('down',0,1,'ArrowDown'),('left',-1,0,'ArrowLeft')]:
    c=b.new_context(viewport=dict(width=width,height=height),device_scale_factor=dpr)
    fixture(c,dict(x=352-dx*130,y=352-dy*130,facing=facing),[dict(id=0,x=320,y=320,kind=kind)])
    pg=c.new_page();ready(pg);key(pg,keyname,1500);a=edges(pg)
    check(f'{width} {kind} {facing} actual input: visible hull outside wall',a['overlap']==0,a)
    pg.locator('#arena').screenshot(path=str(OUT/f'collision-{width}-{kind}-{facing}.png'))
    before=snap(pg)['state']['tank'];key(pg,keyname,500)
    check(f'{width} {kind} {facing} stable contact',snap(pg)['state']['tank']==before)
    # Switch to a perpendicular facing and back at contact.
    key(pg,'ArrowRight' if dy else 'ArrowUp',17);key(pg,keyname,17)
    check(f'{width} {kind} {facing} immediate blocked turn clear',snap(pg)['state']['tank']['facing']==facing and edges(pg)['overlap']==0)
    pg.locator('#arena').focus();pg.keyboard.down('Space');pg.clock.run_for(64)
    fs=snap(pg);check(f'{width} {kind} {facing} flash synchronized to shot',fs['state']['shots']==1 and 0<=fs['state']['time']-fs['state']['firedAt']<.09 and fs['barrelOffsetMasterPx']>0,dict(age=fs['state']['time']-fs['state']['firedAt'],offset=fs['barrelOffsetMasterPx']))
    pg.locator('#arena').screenshot(path=str(OUT/f'flash-{width}-{kind}-{facing}.png'));pg.keyboard.up('Space');c.close()
 # Adjacent wall corner, parallel motion then blocked turns.
 c=b.new_context(viewport=dict(width=1440,height=1000))
 fixture(c,dict(x=270,y=291.5,facing='right'),[dict(id=0,x=320,y=320,kind='brick'),dict(id=1,x=384,y=320,kind='steel')])
 pg=c.new_page();ready(pg);key(pg,'ArrowRight',1000)
 check('actual input parallel sliding along adjacent blocks',abs(snap(pg)['state']['tank']['x']-426)<3 and edges(pg)['overlap']==0)
 for k in ['ArrowDown','ArrowLeft','ArrowUp','ArrowRight']:
  key(pg,k,17);check('corner turn '+k,edges(pg)['overlap']==0)
 pg.locator('#arena').screenshot(path=str(OUT/'collision-corner.png'));c.close()
 # Both languages at the requested widths; verify no additional overflow.
 for width,height in [(320,740),(390,844),(1440,900)]:
  c=b.new_context(viewport=dict(width=width,height=height),reduced_motion='reduce');pg=c.new_page();ready(pg)
  for language in ['en','zh-TW']:
   if snap(pg)['settings']['language']!=language:pg.locator('#language').click()
   pg.screenshot(path=str(OUT/f'theme-{width}-{language}.png'),full_page=True)
   check(f'theme {width} {language} no horizontal overflow',pg.evaluate('document.documentElement.scrollWidth<=innerWidth'))
   check(f'theme {width} {language} reduced motion',snap(pg)['reduced'])
  c.close()
 b.close()
(OUT/'r2-browser-results.json').write_text(json.dumps(dict(date='2026-11-03 Asia/Taipei',fixture_method='HTTP initial-state substitution only; real keyboard input and unchanged production rendering/physics',passed=sum(r['passed'] for r in results),failed=sum(not r['passed'] for r in results),tests=results),indent=2))
print('R2 browser checks:',len(results),'passed')
