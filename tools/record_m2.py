"""Actual real-time Chromium compositor: full five-stop cycle and touch safe lane."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,base64,subprocess
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence/m2';reports=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for mode in ['cycle','touch-safe']:
  mobile=mode=='touch-safe';width,height,dpr=(390,844,2) if mobile else (1200,1000,1);c=b.new_context(viewport=dict(width=width,height=height),device_scale_factor=dpr,is_mobile=mobile,has_touch=mobile);pg=c.new_page();pg.goto('http://127.0.0.1:8080/');pg.wait_for_function('window.guardianPOC');pg.locator('#choose-colossus').click();pg.locator('#start').click();cdp=c.new_cdp_session(pg);frames=[];tmp=OUT/'tmp'/mode;tmp.mkdir(parents=True,exist_ok=True)
  def frame(e):
   f=tmp/f'{len(frames):05d}.jpg';f.write_bytes(base64.b64decode(e['data']));frames.append((f,e['metadata']['timestamp']));cdp.send('Page.screencastFrameAck',{'sessionId':e['sessionId']})
  cdp.on('Page.screencastFrame',frame)
  pg.evaluate('''async()=>{const {bossRender}=await import('/src/colossus.mjs');window.m2Frames=[];window.recordM2=true;let n=0;function sample(){if(n++%3===0){const s=guardianPOC.snapshot().state;m2Frames.push({time:s.colossus.elapsed,phase:s.colossus.phase,phaseTime:s.colossus.phaseTime,stop:s.colossus.stop,body:bossRender(s),bossHP:s.colossus.bossHP,tankHP:s.colossus.tankHP,tank:s.tank});}if(recordM2)requestAnimationFrame(sample);}requestAnimationFrame(sample);}''')
  cdp.send('Page.startScreencast',dict(format='jpeg',quality=90,maxWidth=width*dpr,maxHeight=height*dpr,everyNthFrame=1))
  aimed=None
  if mode=='cycle':pg.wait_for_function('guardianPOC.snapshot().state.colossus.landings>=5',timeout=45000)
  else:
   def touch(selector):
    box=pg.locator(selector).bounding_box();cdp.send('Input.dispatchTouchEvent',dict(type='touchStart',touchPoints=[dict(x=box['x']+box['width']/2,y=box['y']+box['height']/2,id=1)]))
   def end():cdp.send('Input.dispatchTouchEvent',dict(type='touchEnd',touchPoints=[]))
   touch('[data-dir="right"]');pg.wait_for_function('guardianPOC.snapshot().state.tank.x>=560',timeout=15000);end();touch('[data-dir="up"]');pg.wait_for_timeout(64);end();aimed=pg.evaluate('guardianPOC.snapshot().state.tank');touch('#fire');pg.wait_for_function('guardianPOC.snapshot().state.complete',timeout=20000);end()
  pg.wait_for_timeout(200);pg.evaluate('recordM2=false');trace=pg.evaluate('m2Frames');state=pg.evaluate('guardianPOC.snapshot().state');cdp.send('Page.stopScreencast');pg.screenshot(path=str(OUT/(mode+'-live-final.png')),full_page=True);c.close();assert len(frames)>60
  if mode=='cycle':assert state['colossus']['landings']>=5 and state['colossus']['bossHP']==4
  else:assert state['colossus']['outcome']=='success' and state['colossus']['tankHP']==3 and state['tank']==aimed
  concat=tmp/'frames.txt';concat.write_text('\n'.join("file '"+str(f)+"'\nduration "+str(max(.005,frames[i+1][1]-t) if i+1<len(frames) else .05) for i,(f,t) in enumerate(frames))+'\n');subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-c:v','libvpx-vp9','-crf','36','-b:v','0','-pix_fmt','yuv420p',str(OUT/(mode+'-live.webm'))],check=True)
  (OUT/(mode+'-live-trace.json')).write_text(json.dumps(trace,indent=2)+'\n');reports.append(dict(mode=mode,passed=True,frames=len(frames),real_seconds=frames[-1][1]-frames[0][1],simulation_elapsed=state['colossus']['elapsed'],finishedAt=state['colossus']['finishedAt'],bossHP=state['colossus']['bossHP'],tankHP=state['colossus']['tankHP'],hits=state['colossus']['shotHits'],tank=state['tank'],method='actual real-time compositor, no clock override/state mutation; CDP touch for safe lane'))
 b.close()
(OUT/'recording-check.json').write_text(json.dumps(reports,indent=2)+'\n');print(json.dumps(reports))
