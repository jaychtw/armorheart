"""Render a non-playable Offer study at the accepted game's actual arena CSS sizes."""
from pathlib import Path
import http.server,threading,json,hashlib,functools
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'planning/siege-m4/evidence';OUT.mkdir(exist_ok=True)
server=http.server.ThreadingHTTPServer(('127.0.0.1',8082),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start();report=[];errors=[]
try:
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for width,height in [(320,740),(390,844),(768,1024),(1440,1000)]:
   c=b.new_context(viewport=dict(width=width,height=height),device_scale_factor=2);pg=c.new_page();pg.on('pageerror',lambda e:errors.append(str(e)));pg.goto('http://127.0.0.1:8082/');pg.wait_for_function('window.guardianPOC');pg.locator('#choose-ship').click();arena=pg.locator('#arena').bounding_box()['width']
   for lang in ['en','zh-TW']:
    for stage in ['intact','broken','half'] if lang=='en' else ['intact']:
     url=f'http://127.0.0.1:8082/planning/siege-m4/review.html?arena={arena}&stage={stage}&lang={lang}&fan=.5';pg.goto(url);pg.wait_for_function('window.study?.ready');d=pg.evaluate('study');assert d['renderedRounds']==5;assert all(a==255 for a in d['assetRegistration']['solidFoundationCorners']);assert all(a>=200 for a in d['assetRegistration']['muzzleAlpha']);assert abs(d['canvasCSS']-arena)<.02,(width,d,arena);assert pg.evaluate('document.documentElement.scrollWidth<=innerWidth');file=f'study-{width}-{lang}-{stage}.png';pg.screenshot(path=str(OUT/file),full_page=True);report.append(dict(file=file,viewport=[width,height],accepted_game_arena_css=arena,study=d))
   c.close()
  b.close()
 assert not errors,errors
 (OUT/'render-check.json').write_text(json.dumps({'passed':True,'method':'Actual Chromium static-study rendering, CSS arena width measured from accepted M3 page at each viewport; unchanged Guardian .5 world scale; no M4 game/input verification','renders':report,'errors':errors,'editable_svg_sha256':hashlib.sha256((ROOT/'planning/siege-m4/art/fortress-study.svg').read_bytes()).hexdigest(),'production_visual_acceptance':'Not performed; proposed direction only'},indent=2)+'\n')
 print('Static study:',len(report),'render/scale/overflow checks passed')
finally:server.shutdown()
