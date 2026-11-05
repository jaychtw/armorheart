"""Normal-TLS public identity plus actual desktop keyboard/mobile touch smoke."""
from pathlib import Path
from urllib.request import urlopen
from playwright.sync_api import sync_playwright
import os,json,hashlib,subprocess,datetime
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence/publication/live-game';OUT.mkdir(parents=True,exist_ok=True);URL='https://jaychtw.github.io/armorheart/';expected=os.environ.get('ARMORHEART_RELEASE_COMMIT','824618bed223c147a34562ff415e86a922594f7b');checks=[];errors=[]
with urlopen(URL+'build-info.json',timeout=30) as r:info=json.load(r);assert r.status==200
with urlopen(URL,timeout=30) as r:html=r.read();headers=dict(r.headers);assert r.status==200 and r.url==URL
assert info['source_commit']==expected and info['index_sha256']==hashlib.sha256(html).hexdigest()=='62f18789f7ac32b807f1ca5dff41f1b90d42997dc7bdaa356a3b80146bc42bb2'
assert html==(ROOT/'preview/guardian.html').read_bytes()
proxy={'server':os.environ['HTTPS_PROXY'],'bypass':'127.0.0.1,localhost'} if os.environ.get('HTTPS_PROXY') else None
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'],proxy=proxy)
 for mobile in [False,True]:
  c=b.new_context(viewport=dict(width=390,height=844) if mobile else dict(width=1440,height=1000),is_mobile=mobile,has_touch=True,device_scale_factor=1);pg=c.new_page();requests=[];pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None);pg.route('**/*',lambda r:r.continue_() if r.request.url==URL else r.abort());pg.goto(URL);pg.wait_for_function('guardianPOC');cdp=c.new_cdp_session(pg)
  def snap():return pg.evaluate('guardianPOC.snapshot()')
  def press(k=None,fire=False):
   if mobile:
    sel='#fire' if fire else '[data-dir="'+{'ArrowLeft':'left','ArrowUp':'up','ArrowRight':'right'}[k]+'"]';r=pg.locator(sel).bounding_box();cdp.send('Input.dispatchTouchEvent',dict(type='touchStart',touchPoints=[dict(id=1,x=r['x']+r['width']/2,y=r['y']+r['height']/2)]))
   else:pg.locator('#arena').focus();pg.keyboard.down('Space' if fire else k)
  def release(k=None,fire=False):
   if mobile:cdp.send('Input.dispatchTouchEvent',dict(type='touchEnd',touchPoints=[]))
   else:pg.keyboard.up('Space' if fire else k)
  pg.locator('#choose-siege' if mobile else '#choose-colossus').click();pg.locator('#start').click();press('ArrowLeft' if mobile else 'ArrowRight');pg.wait_for_function('mobile=>mobile?guardianPOC.snapshot().state.tank.x<=288:guardianPOC.snapshot().state.tank.x>=560',arg=mobile);release('ArrowLeft' if mobile else 'ArrowRight');press('ArrowUp');pg.wait_for_function("guardianPOC.snapshot().state.tank.facing==='up'");release('ArrowUp');pg.screenshot(path=str(OUT/('mobile-gameplay.png' if mobile else 'desktop-gameplay.png')),full_page=True);pg.locator('#arena').screenshot(path=str(OUT/('mobile-arena.png' if mobile else 'desktop-arena.png')));press(fire=True);pg.wait_for_function('guardianPOC.snapshot().state.complete',timeout=30000);release(fire=True);s=snap();m=s['state']['siege' if mobile else 'colossus'];assert m['outcome']=='success' and len(s['campaign']['completed'])==1;pg.screenshot(path=str(OUT/('mobile-victory.png' if mobile else 'desktop-victory.png')),full_page=True);pg.locator('#language').click();assert snap()['settings']['language']=='zh-TW';pg.screenshot(path=str(OUT/('mobile-victory-zh-TW.png' if mobile else 'desktop-victory-zh-TW.png')),full_page=True);pg.locator('#result-select').click();pg.locator('#tank-bulwark').click();before=snap()['campaign'];pg.reload();pg.wait_for_function('guardianPOC');s=snap();assert s['campaign']==before and s['activeTank']=='bulwark' and s['settings']['language']=='zh-TW';pg.screenshot(path=str(OUT/('mobile-saved-collection.png' if mobile else 'desktop-saved-collection.png')),full_page=True);assert requests==[URL,URL],requests;assert pg.evaluate('document.documentElement.scrollWidth<=innerWidth');checks.append(dict(viewport='390 phone emulation' if mobile else '1440 desktop',input='CDP touch' if mobile else 'keyboard',mission='siege' if mobile else 'colossus',outcome=m['outcome'],finishedAt=m['finishedAt'],tankHP=m['tankHP'],earned_progress=before,reload_selection='bulwark',language='zh-TW',http_requests=requests));c.close()
 b.close()
assert not errors,errors
report=dict(passed=True,url=URL,checkedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),tls='Normal system CA verification; browser HTTPS errors not ignored',build_info=info,html_sha256=hashlib.sha256(html).hexdigest(),headers=headers,plays=checks,errors=errors,limitations='Managed Chromium and emulated touch only; not physical-phone, independent first-time-player, other-engine or assistive-technology tests')
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':True,'source_commit':expected,'url':URL,'plays':checks}))
