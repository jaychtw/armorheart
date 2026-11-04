"""Native-clock actual-input M4 recordings; no state fixtures or virtual clock."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,subprocess,base64,statistics,time
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence/m4';reports=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for mode in ['aggressive','tactical']:
  mobile=mode=='tactical';width,height,dpr=(390,844,2) if mobile else (1200,1100,1);c=b.new_context(viewport=dict(width=width,height=height),device_scale_factor=dpr,is_mobile=mobile,has_touch=mobile);pg=c.new_page();load=time.perf_counter();pg.goto('http://127.0.0.1:8080/');pg.wait_for_function('window.guardianPOC');ready_ms=(time.perf_counter()-load)*1000;pg.locator('#choose-siege').click();cdp=c.new_cdp_session(pg);tmp=OUT/'tmp'/mode;tmp.mkdir(parents=True,exist_ok=True);frames=[]
  def frame(e):
   file=tmp/f'{len(frames):05d}.jpg';file.write_bytes(base64.b64decode(e['data']));frames.append((file,e['metadata']['timestamp']));cdp.send('Page.screencastFrameAck',{'sessionId':e['sessionId']})
  cdp.on('Page.screencastFrame',frame);pg.evaluate('''()=>{window.m4Trace=[];window.m4RAF=[];window.recordM4=true;let old=0,n=0;function sample(now){if(old)m4RAF.push(now-old);old=now;if(n++%3===0){const s=guardianPOC.snapshot().state;m4Trace.push({time:s.siege.elapsed,tank:s.tank,hp:s.siege.tankHP,target:s.siege.fortressHP,stage:guardianPOC.fortressVisual().stage,rounds:s.siege.enemyShells.length,walls:s.walls.map(w=>w.id)});}if(recordM4)requestAnimationFrame(sample);}requestAnimationFrame(sample);}''');cdp.send('Page.startScreencast',dict(format='jpeg',quality=90,maxWidth=width*dpr,maxHeight=height*dpr,everyNthFrame=2));pg.locator('#start').click()
  def press(key=None,fire=False):
   if mobile:
    sel='#fire' if fire else '[data-dir="'+{'ArrowLeft':'left','ArrowRight':'right','ArrowUp':'up','ArrowDown':'down'}[key]+'"]';r=pg.locator(sel).bounding_box();cdp.send('Input.dispatchTouchEvent',dict(type='touchStart',touchPoints=[dict(id=1,x=r['x']+r['width']/2,y=r['y']+r['height']/2)]))
   else:
    pg.evaluate("document.querySelector('#arena').focus({preventScroll:true})");pg.keyboard.down('Space' if fire else key)
  def end(key=None,fire=False):
   if mobile:cdp.send('Input.dispatchTouchEvent',dict(type='touchEnd',touchPoints=[]))
   else:pg.keyboard.up('Space' if fire else key)
  def move(key,axis,target,sign):
   press(key);pg.wait_for_function('p=>guardianPOC.snapshot().state.complete||(guardianPOC.snapshot().state.tank[p.axis]-p.target)*p.sign>=0',arg=dict(axis=axis,target=target,sign=sign),timeout=10000);end(key)
  def until(t):pg.wait_for_function('t=>guardianPOC.snapshot().state.complete||guardianPOC.snapshot().state.siege.elapsed>=t',arg=t,timeout=40000)
  def shoot(t):press(fire=True);until(t);end(fire=True)
  def aim():press('ArrowUp');pg.wait_for_function("guardianPOC.snapshot().state.tank.facing==='up'");end('ArrowUp')
  if mode=='aggressive':move('ArrowLeft','x',288,-1);aim();shoot(30)
  else:
   move('ArrowLeft','x',192,-1);move('ArrowUp','y',480,-1);move('ArrowRight','x',288,1);aim();shoot(6)
   for at in range(6,34,3):
    if pg.evaluate('guardianPOC.snapshot().state.complete'):break
    if pg.evaluate('guardianPOC.snapshot().state.tank.y')<480:move('ArrowDown','y',480,1)
    move('ArrowRight','x',384,1);until(at+1.8);move('ArrowLeft','x',288,-1);aim();shoot(at+3)
  pg.wait_for_timeout(150);pg.evaluate('recordM4=false');s=pg.evaluate('guardianPOC.snapshot().state');m=s['siege'];trace=pg.evaluate('m4Trace');intervals=pg.evaluate('m4RAF');cdp.send('Page.stopScreencast');pg.screenshot(path=str(OUT/f'{mode}-live-final.png'),full_page=True);c.close();assert m['outcome']=='success',m;assert m['tankHP']==1 if mode=='aggressive' else m['tankHP']>=2,m;assert len(frames)>100
  concat=tmp/'frames.txt';concat.write_text('\n'.join("file '"+str(f)+"'\nduration "+str(max(.005,frames[i+1][1]-t) if i+1<len(frames) else .05) for i,(f,t) in enumerate(frames))+'\n');subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-c:v','libvpx-vp9','-crf','36','-b:v','0','-pix_fmt','yuv420p',str(OUT/f'{mode}-live.webm')],check=True)
  (OUT/f'{mode}-live-trace.json').write_text(json.dumps(trace,indent=2)+'\n');ordered=sorted(intervals);reports.append(dict(mode=mode,passed=True,input='CDP touch' if mobile else 'keyboard',frames=len(frames),recording_real_seconds=frames[-1][1]-frames[0][1],finishedAt=m['finishedAt'],tankHP=m['tankHP'],shotHits=m['shotHits'],tankHits=m['tankHits'],coverHits=m['coverHits'],volleys=m['volleys'],source_ready_ms=ready_ms,raf_samples=len(intervals),raf_median_ms=statistics.median(intervals),raf_p95_ms=ordered[int(len(ordered)*.95)],raf_max_ms=max(intervals),browser=b.version,method='Native RAF/compositor + actual input; no virtual clock or game-state changes; managed viewport emulation,not physical hardware or cold-network benchmark'))
 b.close()
(OUT/'recording-check.json').write_text(json.dumps(reports,indent=2)+'\n');print(json.dumps([{k:v for k,v in r.items() if k in ['mode','finishedAt','tankHP','recording_real_seconds','raf_median_ms','raf_p95_ms']}for r in reports]))
