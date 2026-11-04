"""Native-clock four-mission campaign: earned skins, actual phone-emulated touch.
No virtual clock, storage fixtures, synthetic animation or game-state modifications.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,base64,subprocess,statistics
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence/v1';TMP=OUT/'tmp/native';TMP.mkdir(parents=True,exist_ok=True)
order=['siege','interception','colossus','breakthrough'];tanks=['guardian','bulwark','vanguard','sentinel'];nav=['#choose-siege','#choose-ship','#choose-colossus','#choose-mission'];frames=[];plays=[];errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);c=b.new_context(viewport=dict(width=390,height=844),device_scale_factor=1,is_mobile=True,has_touch=True);pg=c.new_page();pg.on('pageerror',lambda e:errors.append(str(e)));pg.goto('http://127.0.0.1:8080/preview/guardian.html');pg.wait_for_function('guardianPOC');cdp=c.new_cdp_session(pg)
 def frame(e):
  file=TMP/f'{len(frames):05d}.jpg';file.write_bytes(base64.b64decode(e['data']));frames.append((file,e['metadata']['timestamp']));cdp.send('Page.screencastFrameAck',{'sessionId':e['sessionId']})
 cdp.on('Page.screencastFrame',frame);cdp.send('Page.startScreencast',dict(format='jpeg',quality=85,maxWidth=390,maxHeight=844,everyNthFrame=2));pg.evaluate('''()=>{window.v1Intervals=[];window.v1NativeTrace=[];window.v1Recording=true;let old=0,n=0;function sample(t){if(old)v1Intervals.push(t-old);old=t;if(n++%12===0){const s=guardianPOC.snapshot(),m=s.state[s.scene]||s.state.mission;v1NativeTrace.push({scene:s.scene,tank:s.activeTank,time:m?.elapsed,x:s.state.tank.x,y:s.state.tank.y,complete:s.state.complete,progress:s.campaign.completed});}if(v1Recording)requestAnimationFrame(sample);}requestAnimationFrame(sample);}''')
 def snap():return pg.evaluate('guardianPOC.snapshot()')
 def press(key=None,fire=False):
  pts=[];selectors=[]
  if key:selectors.append('[data-dir="'+{'ArrowLeft':'left','ArrowRight':'right','ArrowUp':'up','ArrowDown':'down'}[key]+'"]')
  if fire:selectors.append('#fire')
  for i,sel in enumerate(selectors):
   r=pg.locator(sel).bounding_box();assert r['y']>=0 and r['y']+r['height']<=844,r;pts.append(dict(id=i+1,x=r['x']+r['width']/2,y=r['y']+r['height']/2))
  cdp.send('Input.dispatchTouchEvent',dict(type='touchStart',touchPoints=pts))
 def release():cdp.send('Input.dispatchTouchEvent',dict(type='touchEnd',touchPoints=[]))
 def move(key,axis,target,sign):
  press(key);pg.wait_for_function('p=>(guardianPOC.snapshot().state.tank[p.axis]-p.target)*p.sign>=0',arg=dict(axis=axis,target=target,sign=sign),timeout=12000);release()
 def face(key):
  press(key);pg.wait_for_function('f=>guardianPOC.snapshot().state.tank.facing===f',arg={'ArrowUp':'up','ArrowRight':'right','ArrowLeft':'left'}[key]);release()
 def fire(test,timeout=40000):press(fire=True);pg.wait_for_function(test,timeout=timeout);release()
 pg.locator('#tank-guardian').scroll_into_view_if_needed();pg.wait_for_timeout(700)
 for i,id in enumerate(order):
  pg.locator('#tank-'+tanks[i]).click();pg.wait_for_timeout(500);pg.locator(nav[i]).click();pg.locator('#start').click()
  if id=='siege':move('ArrowLeft','x',288,-1);face('ArrowUp');fire('guardianPOC.snapshot().state.complete')
  elif id=='interception':
   press('ArrowLeft');pg.wait_for_timeout(675);release();press(fire=True);pg.wait_for_timeout(1225);release();assert snap()['state']['interception']['shipHP']==4,snap()['state']['interception'];move('ArrowRight','x',384,1);face('ArrowUp');fire('guardianPOC.snapshot().state.complete')
  elif id=='colossus':move('ArrowRight','x',560,1);face('ArrowUp');fire('guardianPOC.snapshot().state.complete')
  else:
   move('ArrowUp','y',400,-1);move('ArrowLeft','x',288,-1);move('ArrowUp','y',160,-1);face('ArrowRight')
   for cell in ['U0','U1']:fire('!guardianPOC.snapshot().state.walls.some(w=>w.id==='+json.dumps(cell)+')')
   pg.wait_for_function('guardianPOC.snapshot().state.complete',timeout=45000)
  s=snap();m=s['state']['mission'] if id=='breakthrough' else s['state'][id];assert m.get('outcome',m.get('phase'))=='success',m;assert s['campaign']['completed']==order[:i+1] and s['activeTank']==tanks[i];plays.append(dict(mission=id,tank=tanks[i],time=m.get('finishedAt',m.get('elapsed')),hp=m.get('tankHP'),completed=s['campaign']['completed']));pg.screenshot(path=str(OUT/f'native-{id}-victory.png'),full_page=True);pg.wait_for_timeout(1000);pg.locator('#result-select').click()
  pg.locator('#tank-'+tanks[min(3,i+1)]).scroll_into_view_if_needed();pg.wait_for_timeout(700)
 pg.screenshot(path=str(OUT/'native-collection-complete.png'),full_page=True);pg.wait_for_timeout(1200);pg.evaluate('v1Recording=false');intervals=pg.evaluate('v1Intervals');trace=pg.evaluate('v1NativeTrace');cdp.send('Page.stopScreencast');assert not errors,errors;b.close()
concat=TMP/'frames.txt';concat.write_text('\n'.join("file '"+str(file)+"'\nduration "+str(max(.005,frames[i+1][1]-t) if i+1<len(frames) else .05) for i,(file,t) in enumerate(frames))+'\n');subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-c:v','libvpx-vp9','-crf','35','-b:v','0','-pix_fmt','yuv420p',str(OUT/'campaign-native.webm')],check=True)
(OUT/'native-trace.json').write_text(json.dumps(trace,indent=2)+'\n');report=dict(passed=True,method='Unmodified native RAF/compositor; genuine four-mission campaign with CDP touch; no virtual clock or save/gameplay fixtures; phone viewport emulation, not physical hardware or independent player',plays=plays,frames=len(frames),recording_seconds=frames[-1][1]-frames[0][1],raf_samples=len(intervals),raf_median_ms=statistics.median(intervals),raf_p95_ms=sorted(intervals)[int(len(intervals)*.95)],errors=errors);(OUT/'native-recording.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
