"""Actual-input Chromium evidence. Start npm start first. Requires Python Playwright.
Optional AXE_PATH points to axe.min.js installed as a dev-only auditing tool.
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import json,os,time
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/os.environ.get('EVIDENCE_DIR','evidence/r2');OUT.mkdir(parents=True,exist_ok=True)
URL=os.environ.get('POC_URL','http://127.0.0.1:8080')
results=[];errors=[];requests=[]
def check(name,condition,detail=None):
    results.append({'name':name,'pass':bool(condition),'detail':detail})
    if not condition:raise AssertionError(name+': '+str(detail))
def snap(page):return page.evaluate('guardianPOC.snapshot()')
def ready(page):
    page.goto(URL);page.wait_for_function('window.guardianPOC');page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda r:requests.append(r.url))
def start(page):page.locator('#start').click()
def move(page,key,axis,target,sign):
    page.locator('#arena').focus();page.keyboard.down(key)
    page.wait_for_function('([axis,target,sign])=>guardianPOC.snapshot().state.tank[axis]*sign>=target*sign',arg=[axis,target,sign],timeout=15000)
    page.keyboard.up(key)
def face(page,key,facing):
    page.locator('#arena').focus();page.keyboard.down(key)
    page.wait_for_function('(f)=>guardianPOC.snapshot().state.tank.facing===f',arg=facing)
    page.keyboard.up(key)
def fire_until(page,count):
    page.locator('#arena').focus();page.keyboard.down('Space')
    page.wait_for_function('(n)=>guardianPOC.snapshot().state.destroyed>=n',arg=count,timeout=12000);page.keyboard.up('Space')
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
    context=browser.new_context(viewport={'width':1440,'height':1100},device_scale_factor=1)
    page=context.new_page();ready(page);page.screenshot(path=str(OUT/'desktop-entry.png'),full_page=True);start(page)
    check('initial scene has six bricks, six permanent walls',len(snap(page)['state']['walls'])==12)
    page.keyboard.down('Space');page.wait_for_function('guardianPOC.snapshot().state.shots===1');page.wait_for_timeout(30)
    page.screenshot(path=str(OUT/'desktop-recoil.png'),full_page=True);page.wait_for_timeout(500);page.keyboard.up('Space')
    check('immediate shot and one-shot brick destruction',snap(page)['state']['shots']==1 and snap(page)['state']['destroyed']==1)
    page.screenshot(path=str(OUT/'desktop-first-impact.png'),full_page=True)
    # Language switches preserve the simulation, live tank position and firing count.
    before=snap(page)['state'];page.locator('#language').click();after=snap(page)
    check('live zh-TW switch preserves state',after['settings']['language']=='zh-TW' and after['state']['tank']==before['tank'] and after['state']['shots']==before['shots'])
    page.screenshot(path=str(OUT/'desktop-zh-TW.png'),full_page=True);page.locator('#language').click()
    # Six-block route through the owner-authorized clearance layout.
    fire_until(page,2)
    move(page,'ArrowRight','x',544,1);face(page,'ArrowUp','up');fire_until(page,4)
    move(page,'ArrowUp','y',544,-1);face(page,'ArrowLeft','left');fire_until(page,5)
    face(page,'ArrowRight','right');fire_until(page,6)
    check('actual keyboard complete six-block playthrough',snap(page)['state']['complete'] and snap(page)['state']['destroyed']==6)
    page.screenshot(path=str(OUT/'desktop-range-cleared.png'),full_page=True)
    page.locator('#start').click();check('replay restores all walls and starting shot count',snap(page)['state']['destroyed']==0 and snap(page)['state']['shots']==0)
    page.locator('#pause').click();before=snap(page)['state'];page.wait_for_timeout(150)
    check('pause freezes simulation',snap(page)['state']['time']==before['time']);page.locator('#start').click()
    page.locator('#layers').click();page.screenshot(path=str(OUT/'desktop-layer-inspection.png'),full_page=True)
    check('editable layers inspection toggles',snap(page)['exploded'])
    for size in [48,64,96,128]:
        page.locator(f'[data-size="{size}"]').click();page.locator('#facings').screenshot(path=str(OUT/f'cardinal-{size}px.png'))
        dims=page.locator('#facings canvas').evaluate_all('(xs)=>xs.map(x=>({w:x.getBoundingClientRect().width,h:x.getBoundingClientRect().height}))')
        check(f'four native CSS-size comparisons {size}px',len(dims)==4 and all(d['w']==size and d['h']==size for d in dims))
    # Keyboard focus progression is native DOM; focus and activate language via Enter.
    page.locator('#language').focus();page.keyboard.press('Enter');check('settings controls keyboard accessible',snap(page)['settings']['language']=='zh-TW')
    page.reload();page.wait_for_function('window.guardianPOC');check('language preference persists after reload',snap(page)['settings']['language']=='zh-TW')
    axe_path=os.environ.get('AXE_PATH')
    if axe_path:
        page.add_script_tag(path=axe_path)
        audit=page.evaluate('async()=>{const r=await axe.run(document,{runOnly:{type:"tag",values:["wcag2a","wcag2aa","wcag21aa"]}});return {violations:r.violations,passes:r.passes.length,incomplete:r.incomplete.map(x=>({id:x.id,impact:x.impact}))}}')
        (OUT/'axe-desktop.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False));check('desktop automated accessibility audit',len(audit['violations'])==0,[x['id'] for x in audit['violations']])
    timings=page.evaluate('''()=>new Promise(resolve=>{let last=0,a=[];function f(t){if(last)a.push(t-last);last=t;if(a.length<90)requestAnimationFrame(f);else resolve(a);}requestAnimationFrame(f);})''')
    (OUT/'frame-sample.json').write_text(json.dumps({'environment':'headless Chromium on cloud host; desktop idle render only; not physical phone performance','samples':len(timings),'median_ms':sorted(timings)[len(timings)//2],'max_ms':max(timings)},indent=2))
    context.close()
    # Actual two-finger touch, dispatched through Chromium's input pipeline.
    mobile=browser.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True)
    mp=mobile.new_page();ready(mp);start(mp);cdp=mobile.new_cdp_session(mp)
    mp.locator('#fire').scroll_into_view_if_needed();box=mp.locator('[data-dir="right"]').bounding_box();fb=mp.locator('#fire').bounding_box()
    points=[{'x':box['x']+box['width']/2,'y':box['y']+box['height']/2,'id':1},{'x':fb['x']+fb['width']/2,'y':fb['y']+fb['height']/2,'id':2}]
    cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':points});mp.wait_for_timeout(1200);cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
    ms=snap(mp);check('simultaneous direction plus held fire with two touch pointers',ms['state']['tank']['x']>450 and ms['state']['shots']>=2,{'x':ms['state']['tank']['x'],'shots':ms['state']['shots']})
    before=ms['state']['shots'];mp.wait_for_timeout(1100);check('touch release stops firing',snap(mp)['state']['shots']==before)
    mp.screenshot(path=str(OUT/'mobile-390-touch.png'),full_page=True)
    mp.locator('#language').click();mp.screenshot(path=str(OUT/'mobile-390-zh-TW.png'),full_page=True)
    check('mobile live localization',mp.locator('#fire').inner_text()=='開火')
    if axe_path:
        mp.add_script_tag(path=axe_path);audit=mp.evaluate('async()=>{const r=await axe.run(document,{runOnly:{type:"tag",values:["wcag2a","wcag2aa","wcag21aa"]}});return {violations:r.violations,passes:r.passes.length,incomplete:r.incomplete.map(x=>({id:x.id,impact:x.impact}))}}')
        (OUT/'axe-mobile.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False));check('mobile automated accessibility audit',len(audit['violations'])==0,[x['id'] for x in audit['violations']])
    mobile.close()
    for width,height,dpr in [(320,740,1),(390,844,2),(768,1024,1),(844,390,1),(1440,900,2)]:
        c=browser.new_context(viewport={'width':width,'height':height},device_scale_factor=dpr,is_mobile=width<500,has_touch=True,reduced_motion='reduce')
        pg=c.new_page();ready(pg);start(pg)
        pg.locator('#language').click()
        pg.screenshot(path=str(OUT/f'viewport-{width}x{height}-dpr{dpr}.png'),full_page=True)
        metrics=pg.evaluate('''()=>({overflow:document.documentElement.scrollWidth>innerWidth,arena:document.querySelector('#arena').getBoundingClientRect().width,targets:[...document.querySelectorAll('[data-dir],#fire')].map(x=>{const r=x.getBoundingClientRect();return [r.width,r.height]}),reduced:guardianPOC.snapshot().reduced})''')
        check(f'layout targets and reduced motion {width}x{height} DPR{dpr}',not metrics['overflow'] and metrics['reduced'] and all(x>=44 and y>=44 for x,y in metrics['targets']),metrics)
        c.close()
    blocked=browser.new_context();blocked.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Blocked','SecurityError')}})")
    pg=blocked.new_page();ready(pg);start(pg);check('blocked storage falls back without preventing play',pg.locator('#storage-warning').is_visible() and snap(pg)['started']);blocked.close()
    corrupt=browser.new_context();corrupt.add_init_script("localStorage.setItem('armorheart-guardian-settings','{broken')")
    pg=corrupt.new_page();ready(pg);start(pg);check('corrupt storage falls back without preventing play',snap(pg)['settings']['language']=='en' and snap(pg)['started']);corrupt.close()
    check('no JavaScript runtime errors',not errors,errors)
    check('no external runtime network requests',not [u for u in requests if not u.startswith(URL) and not u.startswith('data:')])
    browser.close()
(OUT/'browser-results.json').write_text(json.dumps({'date':os.environ.get('EVIDENCE_DATE','2026-11-03 Asia/Taipei'),'browser':'Chromium 154','tests':results,'passed':sum(x['pass'] for x in results),'failed':sum(not x['pass'] for x in results),'runtimeErrors':errors,'axe':bool(os.environ.get('AXE_PATH'))},indent=2,ensure_ascii=False))
print(json.dumps({'passed':sum(x['pass'] for x in results),'failed':sum(not x['pass'] for x in results)},indent=2))
