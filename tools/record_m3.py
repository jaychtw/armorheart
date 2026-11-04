"""Real-time unmodified-clock M3 compositor: complete route and touch victory."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,subprocess,base64,statistics,time
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence/m3';reports=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for mode in ['route','touch-win']:
  mobile=mode=='touch-win';width,height,dpr=(390,844,2) if mobile else (1200,1100,1);c=b.new_context(viewport=dict(width=width,height=height),device_scale_factor=dpr,is_mobile=mobile,has_touch=mobile);pg=c.new_page();start=time.perf_counter();pg.goto('http://127.0.0.1:8080/');pg.wait_for_function('window.guardianPOC');ready_ms=(time.perf_counter()-start)*1000;pg.locator('#choose-ship').click();cdp=c.new_cdp_session(pg);tmp=OUT/'tmp'/mode;tmp.mkdir(parents=True,exist_ok=True);frames=[]
  def frame(e):
   file=tmp/f'{len(frames):05d}.jpg';file.write_bytes(base64.b64decode(e['data']));frames.append((file,e['metadata']['timestamp']));cdp.send('Page.screencastFrameAck',{'sessionId':e['sessionId']})
  cdp.on('Page.screencastFrame',frame);pg.evaluate('''()=>{window.m3Live=[];window.m3RAF=[];window.recordM3=true;let old=0,n=0;function sample(now){if(old)m3RAF.push(now-old);old=now;if(n++%3===0){const a=guardianPOC.snapshot().state;m3Live.push({time:a.interception.elapsed,tank:a.tank,shipHP:a.interception.shipHP,tankHP:a.interception.tankHP,visual:guardianPOC.shipVisual(),enemyShells:a.interception.enemyShells.length});}if(recordM3)requestAnimationFrame(sample);}requestAnimationFrame(sample);}''');cdp.send('Page.startScreencast',dict(format='jpeg',quality=90,maxWidth=width*dpr,maxHeight=height*dpr,everyNthFrame=2));pg.locator('#start').click();aimed=None
  if mode=='route':pg.wait_for_function('guardianPOC.snapshot().state.complete',timeout=45000)
  else:
   def touch(sel):
    b=pg.locator(sel).bounding_box();cdp.send('Input.dispatchTouchEvent',dict(type='touchStart',touchPoints=[dict(x=b['x']+b['width']/2,y=b['y']+b['height']/2,id=1)]))
   def end():cdp.send('Input.dispatchTouchEvent',dict(type='touchEnd',touchPoints=[]))
   touch('[data-dir="left"]');pg.wait_for_function('guardianPOC.snapshot().state.tank.x<=279.5',timeout=10000);end();touch('#fire');pg.wait_for_function('guardianPOC.snapshot().state.interception.shipHP<=4',timeout=10000);end();touch('[data-dir="right"]');pg.wait_for_function('guardianPOC.snapshot().state.tank.x>=384',timeout=10000);end();touch('[data-dir="up"]');pg.wait_for_timeout(48);end();aimed=pg.evaluate('guardianPOC.snapshot().state.tank');touch('#fire');pg.wait_for_function('guardianPOC.snapshot().state.complete',timeout=30000);end()
  pg.wait_for_timeout(150);pg.evaluate('recordM3=false');trace=pg.evaluate('m3Live');intervals=pg.evaluate('m3RAF');s=pg.evaluate('guardianPOC.snapshot().state');m=s['interception'];cdp.send('Page.stopScreencast');pg.screenshot(path=str(OUT/f'{mode}-live-final.png'),full_page=True);c.close();assert len(frames)>100
  if mode=='route':assert m['outcome']=='escaped' and m['shipHP']==6 and [o['time'] for o in m['opportunities'] if o['fired']]==[3,12,18,21]
  else:assert m['outcome']=='success' and m['tankHP']==3 and s['tank']==aimed
  concat=tmp/'frames.txt';concat.write_text('\n'.join("file '"+str(f)+"'\nduration "+str(max(.005,frames[i+1][1]-t) if i+1<len(frames) else .05) for i,(f,t) in enumerate(frames))+'\n');subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-c:v','libvpx-vp9','-crf','36','-b:v','0','-pix_fmt','yuv420p',str(OUT/f'{mode}-live.webm')],check=True)
  (OUT/f'{mode}-live-trace.json').write_text(json.dumps(trace,indent=2)+'\n');ordered=sorted(intervals);reports.append(dict(mode=mode,passed=True,frames=len(frames),recording_real_seconds=frames[-1][1]-frames[0][1],finishedAt=m['finishedAt'],shipHP=m['shipHP'],tankHP=m['tankHP'],shotHits=m['shotHits'],tankHits=m['tankHits'],opportunities=m['opportunities'],lastAim=aimed,load_ready_ms=ready_ms,raf_samples=len(intervals),raf_median_ms=statistics.median(intervals),raf_p95_ms=ordered[int(len(ordered)*.95)],raf_max_ms=max(intervals),browser=b.version,method='real-time native RAF + compositor; actual CDP touch for victory; no virtual clock or game-state changes; viewport emulation,not physical phone or cold-network benchmark'))
 b.close()
(OUT/'recording-check.json').write_text(json.dumps(reports,indent=2)+'\n');print(json.dumps([{k:v for k,v in r.items() if k in ['mode','passed','finishedAt','tankHP','recording_real_seconds','raf_median_ms','raf_p95_ms','raf_max_ms']} for r in reports]))
