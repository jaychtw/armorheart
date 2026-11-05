"""Render/record the isolated Offer diagram, not an M3 gameplay test."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,base64,subprocess
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'planning/interception-m3/evidence';rows=[];errors=[]
C=json.loads((ROOT/'planning/interception-m3/map.json').read_text());R=144;Q=3.141592653589793*R/2
stops=[('entry',0),('left-tangent',480),('left-turn-45',480+Q/2),('north-broadside',480+Q+128),('right-turn-45',480+Q+256+Q/2),('right-tangent',480+Q+256+Q),('right-broadside',480+Q+256+Q+320)]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height in [(1440,1100),(390,1000),(320,1000)]:
  c=b.new_context(viewport=dict(width=width,height=height),device_scale_factor=1);pg=c.new_page();pg.on('pageerror',lambda e:errors.append(str(e)));pg.goto('http://127.0.0.1:8080/planning/interception-m3/proof.html');pg.wait_for_function('window.m3Proof?.current');pg.wait_for_function("[...document.images].every(x=>x.complete)")
  for name,d in stops:
   pg.evaluate('(d)=>m3Proof.setDistance(d)',d);pg.wait_for_timeout(50);pg.screenshot(path=str(OUT/f'route-{width}-{name}.png'),full_page=True);pose=pg.evaluate('m3Proof.current');assert abs(pose['distance']-d)<1e-5;assert -90.0001<=pose['heading']*180/3.141592653589793<=90.0001
   rows.append(dict(width=width,name=name,pose=pose,canvas=pg.locator('#field').bounding_box()))
  assert not pg.evaluate('document.documentElement.scrollWidth>innerWidth')
  c.close()
 # Actual real-time motion proof: same ship source and route without clock overrides.
 c=b.new_context(viewport=dict(width=900,height=1080),device_scale_factor=1);pg=c.new_page();pg.goto('http://127.0.0.1:8080/planning/interception-m3/proof.html');pg.wait_for_function('window.m3Proof?.current');cdp=c.new_cdp_session(pg);tmp=OUT/'tmp/recording';tmp.mkdir(parents=True,exist_ok=True);frames=[]
 def frame(e):
  f=tmp/f'{len(frames):05d}.jpg';f.write_bytes(base64.b64decode(e['data']));frames.append((f,e['metadata']['timestamp']));cdp.send('Page.screencastFrameAck',{'sessionId':e['sessionId']})
 cdp.on('Page.screencastFrame',frame);pg.evaluate('''()=>{window.motionTrace=[];window.recordMotion=true;function sample(){if(recordMotion){motionTrace.push({...m3Proof.current});requestAnimationFrame(sample);}}requestAnimationFrame(sample);}''');cdp.send('Page.startScreencast',dict(format='jpeg',quality=88,maxWidth=900,maxHeight=1080,everyNthFrame=2));pg.locator('#play').click();pg.wait_for_function('m3Proof.current.distance>=m3Proof.geometry.routeLength',timeout=45000);pg.wait_for_timeout(100);pg.evaluate('recordMotion=false');cdp.send('Page.stopScreencast');trace=pg.evaluate('motionTrace');assert len(frames)>100
 concat=tmp/'frames.txt';concat.write_text('\n'.join("file '"+str(f)+"'\nduration "+str(max(.005,frames[i+1][1]-t) if i+1<len(frames) else .05) for i,(f,t) in enumerate(frames))+'\n');subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-c:v','libvpx-vp9','-crf','36','-b:v','0','-pix_fmt','yuv420p',str(OUT/'route-live.webm')],check=True)
 max_heading_step=max(abs(b['heading']-a['heading']) for a,b in zip(trace,trace[1:]));assert max_heading_step<.04,max_heading_step
 (OUT/'motion-trace.json').write_text(json.dumps(trace,indent=2)+'\n');c.close();b.close()
assert not errors
report=dict(status='Offer diagram verification only, not Stage3 gameplay or production-art acceptance',passed=True,rendered_frames=len(rows),views=rows,recording=dict(frames=len(frames),realSeconds=frames[-1][1]-frames[0][1],maximumAdjacentHeadingChangeRadians=max_heading_step,method='real-time native RAF route and SVG rotation; compositor frames; no virtual clock'),errors=errors,reference_image='Not accessible; attachment requested once',physical_phone='Not performed')
(OUT/'render-check.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(rows),'at-scale geometry frames and real-time full-route recording')
