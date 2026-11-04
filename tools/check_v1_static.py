"""Local-only static /armorheart/ candidate path test. No Pages mutation/deployment."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import tempfile,threading,functools,json,hashlib,zipfile
ROOT=Path(__file__).resolve().parents[1]
with zipfile.ZipFile(ROOT/'artifacts/Armorheart-v1.0-RC.zip') as archive:raw=archive.read('Armorheart-v1.0-RC/index.html')
assert raw==(ROOT/'preview/guardian.html').read_bytes()
requests=[];errors=[]
with tempfile.TemporaryDirectory(prefix='armorheart-static-',dir='/tmp') as d:
 dest=Path(d)/'armorheart';dest.mkdir();(dest/'index.html').write_bytes(raw)
 class Quiet(SimpleHTTPRequestHandler):
  def log_message(self,*args):pass
 server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=d));threading.Thread(target=server.serve_forever,daemon=True).start();url=f'http://127.0.0.1:{server.server_port}/armorheart/'
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);c=b.new_context(viewport=dict(width=390,height=844));pg=c.new_page();pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None);pg.route('**/*',lambda r:r.continue_() if r.request.url==url else r.abort());pg.goto(url);pg.wait_for_function('guardianPOC');pg.locator('#choose-colossus').click();pg.locator('#start').click();pg.locator('#arena').focus();pg.keyboard.down('ArrowRight');pg.wait_for_function('guardianPOC.snapshot().state.tank.x>=560');pg.keyboard.up('ArrowRight');pg.keyboard.down('ArrowUp');pg.wait_for_function("guardianPOC.snapshot().state.tank.facing==='up'");pg.keyboard.up('ArrowUp');pg.keyboard.down('Space');pg.wait_for_function('guardianPOC.snapshot().state.complete',timeout=20000);pg.keyboard.up('Space');s=pg.evaluate('guardianPOC.snapshot()');assert s['state']['colossus']['outcome']=='success' and s['campaign']['completed']==['colossus'];pg.locator('#result-select').click();pg.locator('#tank-bulwark').click();pg.locator('#language').click();pg.reload();pg.wait_for_function('guardianPOC');s=pg.evaluate('guardianPOC.snapshot()');assert s['activeTank']=='bulwark' and s['campaign']['completed']==['colossus'] and s['settings']['language']=='zh-TW';assert requests==[url,url],requests;assert not errors,errors;pg.screenshot(path=str(ROOT/'evidence/v1/static-prefix-zh-TW.png'),full_page=True);b.close()
 server.shutdown()
report=dict(passed=True,method='Temporary local static folder /armorheart/index.html; native keyboard M2 win, earned Bulwark selection, live language and reload, all other requests blocked',tested_path='/armorheart/',http_requests=requests,embedded_html_sha256=hashlib.sha256(raw).hexdigest(),errors=errors,not_tested='Not a live GitHub Pages publication, HTTPS/custom-domain/CDN/header verification, direct file:// or offline first visit to a remote site')
(ROOT/'evidence/v1/static-check.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS local static /armorheart/ win, unlock, selection, Chinese and reload; initial HTML only per visit')
