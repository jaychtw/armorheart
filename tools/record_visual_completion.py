"""Real-time Chromium compositor recording, all four facings; pose-only fixture."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import base64,json,subprocess
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence/r3-visual';TMP=OUT/'tmp/live';TMP.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);c=b.new_context(viewport=dict(width=1200,height=900));pg=c.new_page()
 src=(ROOT/'src/engine.mjs').read_text();a=src.index('export function createState()');z=src.index('\n}',a);part=src[a:z].replace('return {time:0','const initial={time:0');part+='\n initial.tank={x:384,y:384,facing:"up"}; initial.walls=[]; return initial;'
 c.route('**/src/engine.mjs',lambda r:r.fulfill(body=src[:a]+part+src[z:],content_type='text/javascript'))
 pg.goto('http://127.0.0.1:8080/');pg.wait_for_function('window.guardianPOC');pg.locator('#start').click();pg.locator('#arena').scroll_into_view_if_needed();pg.locator('#arena').focus();box=pg.locator('#arena').bounding_box();cx=int(box['x']+box['width']/2);cy=int(box['y']+box['height']/2)
 cdp=c.new_cdp_session(pg);frames=[]
 def frame(e):
  file=TMP/f'frame-{len(frames):04d}.jpg';file.write_bytes(base64.b64decode(e['data']));frames.append((file,e['metadata']['timestamp']));cdp.send('Page.screencastFrameAck',{'sessionId':e['sessionId']})
 cdp.on('Page.screencastFrame',frame);pg.evaluate('''()=>{window.visualLiveTrace=[];window.keepVisualTrace=true;function sample(){const s=guardianPOC.snapshot();visualLiveTrace.push({time:s.state.time,age:s.state.time-s.state.firedAt,offset:s.barrelOffsetMasterPx,tank:s.state.tank,shots:s.state.shots});if(keepVisualTrace)requestAnimationFrame(sample);}requestAnimationFrame(sample);}''')
 cdp.send('Page.startScreencast',dict(format='jpeg',quality=96,maxWidth=1200,maxHeight=900,everyNthFrame=1))
 for n,k in enumerate(['ArrowUp','ArrowRight','ArrowDown','ArrowLeft'],1):
  pg.keyboard.down(k);pg.wait_for_function('(key)=>guardianPOC.snapshot().state.tank.facing===key',arg={'ArrowUp':'up','ArrowRight':'right','ArrowDown':'down','ArrowLeft':'left'}[k]);pg.keyboard.up(k)
  pg.keyboard.down('Space');pg.wait_for_function('(n)=>guardianPOC.snapshot().state.shots===n',arg=n);pg.keyboard.up('Space');pg.wait_for_timeout(1050)
 pg.evaluate('keepVisualTrace=false');trace=pg.evaluate('visualLiveTrace');cdp.send('Page.stopScreencast');b.close()
assert len(frames)>60
for n,facing in enumerate(['up','right','down','left'],1):
 rows=[r for r in trace if r['shots']==n and 0<=r['age']<=.25];assert rows and max(r['offset'] for r in rows)>9,(facing,rows)
 assert all(r['tank']==rows[0]['tank'] for r in rows),facing
 assert rows[0]['tank']['facing']==facing
concat=TMP/'frames.txt';concat.write_text('\n'.join("file '"+str(f)+"'\nduration "+str(max(.005,frames[i+1][1]-t) if i+1<len(frames) else .05) for i,(f,t) in enumerate(frames))+'\n')
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-vf',f'crop=200:200:{cx-100}:{cy-100},scale=600:600:flags=neighbor','-c:v','libvpx-vp9','-crf','25','-b:v','0','-pix_fmt','yuv420p',str(OUT/'four-facing-live.webm')],check=True)
(OUT/'live-recoil-trace.json').write_text(json.dumps(trace,indent=2)+'\n')
report=dict(passed=True,method='actual real-time Chromium compositor; keyboard facing and fire; centered clear pose-only initial fixture;200px crop enlarged3x for inspection',order=['up','right','down','left'],frames=len(frames),trace_samples=len(trace),seconds=frames[-1][1]-frames[0][1],peak=max(r['offset'] for r in trace),hull_fixed_during_each_recoil=True)
(OUT/'live-recording-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
