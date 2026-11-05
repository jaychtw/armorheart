"""Armorheart catalog/fact-sheet/Play verification; local candidate or live portal."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from urllib.request import urlopen
import argparse,os,json,datetime
ROOT=Path(__file__).resolve().parents[1];parser=argparse.ArgumentParser();parser.add_argument('--local',action='store_true');parser.add_argument('--source',required=True);a=parser.parse_args();BASE='http://127.0.0.1:4182' if a.local else 'https://jaychtw.github.io';OUT=ROOT/'evidence/publication'/('local-portal' if a.local else 'live-portal');OUT.mkdir(parents=True,exist_ok=True);views=[];errors=[];plays=[]
proxy={'server':os.environ['HTTPS_PROXY'],'bypass':'127.0.0.1,localhost'} if os.environ.get('HTTPS_PROXY') else None
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'],proxy=proxy)
 for width in [320,390,768,1440]:
  for theme in ['light','dark']:
   pg=b.new_page(viewport=dict(width=width,height=1000));pg.on('pageerror',lambda e:errors.append(str(e)));pg.goto(BASE+'/');assert pg.locator('[data-project]').first.get_attribute('data-project')=='armorheart';assert pg.locator('[data-project="armorheart"]').count()==1;card=pg.locator('[data-project="armorheart"]');assert card.get_attribute('href')=='https://jaychtw.github.io/armorheart/';assert 'Four tank missions' in card.inner_text();assert card.locator('[lang="zh-TW"]').count()==0;card.locator('img').evaluate('(e)=>e.decode()');image=card.locator('img').evaluate('(e)=>({url:e.currentSrc,width:e.naturalWidth,height:e.naturalHeight})');assert image['width']>0 and 'armorheart.' in image['url'];
   if pg.locator('html').get_attribute('data-theme')!=theme:pg.locator('.theme-toggle').click()
   assert pg.evaluate('document.documentElement.scrollWidth<=innerWidth')
   if width in [390,1440]:
    pg.locator('[data-project] img').evaluate_all('(es)=>Promise.all(es.filter(e=>e.getBoundingClientRect().top<innerHeight).map(e=>e.decode()))');pg.screenshot(path=str(OUT/f'games-{width}-{theme}.png'))
   pg.goto(BASE+'/games/armorheart/');pg.locator('.work-media img').evaluate('(e)=>e.decode()');assert pg.locator('h1').inner_text()=='Armorheart';assert '四個戰車任務' in pg.locator('p[lang="zh-TW"]').inner_text();assert pg.locator('.primary-action').get_attribute('href')=='https://jaychtw.github.io/armorheart/';assert pg.evaluate('document.documentElement.scrollWidth<=innerWidth');
   if width in[390,1440]:pg.screenshot(path=str(OUT/f'factsheet-{width}-{theme}.png'),full_page=True)
   views.append(dict(width=width,theme=theme,newest='armorheart',bilingual_fact_sheet=True,english_card=True,image=image,no_overflow=True));pg.close()
 for from_card in [True,False]:
  pg=b.new_page(viewport=dict(width=390 if from_card else 1440,height=1000));pg.goto(BASE+('/' if from_card else '/games/armorheart/'));pg.locator('[data-project="armorheart"]' if from_card else '.primary-action').click();pg.wait_for_url('https://jaychtw.github.io/armorheart/');pg.wait_for_function('guardianPOC');pg.locator('#choose-colossus').click();pg.locator('#start').click();pg.locator('#arena').focus();pg.keyboard.down('ArrowRight');pg.wait_for_function('guardianPOC.snapshot().state.tank.x>=560');pg.keyboard.up('ArrowRight');pg.keyboard.down('ArrowUp');pg.wait_for_function("guardianPOC.snapshot().state.tank.facing==='up'");pg.keyboard.up('ArrowUp');pg.keyboard.down('Space');pg.wait_for_function('guardianPOC.snapshot().state.complete',timeout=20000);pg.keyboard.up('Space');s=pg.evaluate('guardianPOC.snapshot()');assert s['state']['colossus']['outcome']=='success' and 'colossus'in s['campaign']['completed'];plays.append(dict(origin='Games card' if from_card else 'fact-sheet Play',url=pg.url,actual_victory='colossus',progress=s['campaign']['completed']));pg.close()
 with urlopen(BASE+'/build-info.json',timeout=30)as r:identity=json.load(r)
 assert identity['sourceCommit']==a.source
 if not a.local:assert identity['sourceDirty'] is False
 b.close()
assert not errors,errors
report=dict(passed=True,local=a.local,checkedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),base=BASE,source_commit=a.source,identity=identity,views=views,plays=plays,errors=errors,method='Actual Chromium gallery, bilingual fact sheet and followed Play destinations with real keyboard M2 victories; normal TLS/no ignored certificate errors. Managed viewport emulation, not independent human/physical-device testing.')
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':True,'local':a.local,'views':len(views),'plays':plays,'source':a.source}))
