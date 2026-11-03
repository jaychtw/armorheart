"""Actual before/after marker-removal renders; natural shadow and simulation frozen."""
from pathlib import Path
import json,subprocess,time
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence/m2-final';BASE='4cef3e58a7a4b244a8630e29751b71e4006a7785';rows=[];states={}
def old(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=ROOT)
# The engine, complete boss model, original artwork and earlier ZIP remain byte-identical.
files=['src/engine.mjs','src/colossus.mjs','src/colossus-art.mjs','src/maps/colossus.mjs','src/breakthrough.mjs','src/maps/breakthrough.mjs','src/transport.mjs','artifacts/Armorheart-Colossus-M2.zip']
files += [str(p.relative_to(ROOT)) for p in (ROOT/'assets/colossus').rglob('*') if p.is_file()]
for p in files:assert (ROOT/p).read_bytes()==old(p),p
before=old('src/app.mjs').decode();after=(ROOT/'src/app.mjs').read_text()
shadow="ctx.fillStyle='#122a2355';ctx.beginPath();ctx.ellipse(p.x,p.y,112*(1-p.z/256),64*(1-p.z/256),0,0,Math.PI*2);ctx.fill();ctx.restore();"
assert shadow in before and shadow in after
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height,lang in [(1440,1000,'en'),(390,844,'en'),(320,740,'zh-TW')]:
  for version in ['before','after']:
   c=b.new_context(viewport=dict(width=width,height=height),device_scale_factor=1,has_touch=width<500)
   if version=='before':
    for f in ['app.mjs','i18n.mjs']:c.route('**/src/'+f,lambda route,request,f=f:route.fulfill(body=old('src/'+f),content_type='text/javascript'))
   pg=c.new_page();pg.clock.install();pg.add_init_script('''(()=>{const p=CanvasRenderingContext2D.prototype,e=p.ellipse,t=p.fillText,c=p.clearRect;window.paint={ellipses:[],texts:[]};p.clearRect=function(...a){if(this.canvas.id==='arena')paint={ellipses:[],texts:[]};return c.apply(this,a)};p.ellipse=function(...a){if(this.canvas.id==='arena')paint.ellipses.push(a);return e.apply(this,a)};p.fillText=function(...a){if(this.canvas.id==='arena')paint.texts.push(a);return t.apply(this,a)}})()''')
   pg.goto('http://127.0.0.1:8080/');pg.wait_for_function('window.guardianPOC');pg.clock.pause_at(int(time.time()*1000)+1000);pg.locator('#choose-colossus').click()
   if lang=='zh-TW':pg.locator('#language').click()
   pg.locator('#start').click()
   for name,ms in [('ground',650),('airborne',1950),('landing',700)]:
    pg.clock.run_for(ms);s=pg.evaluate('guardianPOC.snapshot().state');paint=pg.evaluate('paint');m=s['colossus'];key=(width,name)
    if version=='before':states[key]=s
    else:assert s==states[key],('simulation changed',key)
    marker=[a for a in paint['texts'] if a[0] in ['NEXT','下一站']]
    assert len(marker)==(1 if version=='before' else 0),(version,paint)
    # Arena draws one natural boss ellipse. Before adds one marker ellipse.
    assert len(paint['ellipses'])==(2 if version=='before' else 1),(version,name,paint)
    if version=='after':assert pg.locator('#boss-immunity').inner_text()==''
    pg.screenshot(path=str(OUT/f'{version}-{width}-{name}.png'),full_page=True)
    rows.append(dict(version=version,width=width,language=lang,phase=m['phase'],time=m['elapsed'],paint=paint))
   c.close()
 b.close()
report=dict(passed=True,baseline=BASE,render_pairs=9,simulation_states_identical=True,natural_shadow_expression_identical=True,unchanged_files=len(files),before_after=rows,physical_phone='Not performed',first_time_player='Not performed')
(OUT/'visual-check.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print('PASS9 before/after render pairs; exact natural shadow and simulation preserved')
