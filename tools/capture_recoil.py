"""Capture actual Chromium compositor frames and mux a local review recording."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import base64,json,subprocess,os
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/os.environ.get('EVIDENCE_DIR','evidence/r2');TMP=OUT/'tmp';TMP.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=b.new_page(viewport={'width':1200,'height':900},device_scale_factor=1)
    page.goto('http://127.0.0.1:8080');page.wait_for_function('window.guardianPOC');page.locator('#start').click()
    cdp=page.context.new_cdp_session(page);frames=[]
    def frame(event):
        file=TMP/f'frame-{len(frames):04d}.jpg';file.write_bytes(base64.b64decode(event['data']))
        frames.append((file,event['metadata']['timestamp']))
        cdp.send('Page.screencastFrameAck',{'sessionId':event['sessionId']})
    cdp.on('Page.screencastFrame',frame)
    cdp.send('Page.startScreencast',{'format':'jpeg','quality':92,'maxWidth':1200,'maxHeight':900,'everyNthFrame':1})
    page.evaluate('''()=>{window.recoilTrace=[];function sample(){const s=guardianPOC.snapshot();recoilTrace.push({time:s.state.time,offset:s.barrelOffsetMasterPx,tank:s.state.tank,shots:s.state.shots});if(recoilTrace.length<150)requestAnimationFrame(sample);}requestAnimationFrame(sample);}''')
    page.keyboard.down('Space');page.wait_for_timeout(2400);page.keyboard.up('Space');page.wait_for_timeout(400)
    trace=page.evaluate('recoilTrace');(OUT/'recoil-render-trace.json').write_text(json.dumps(trace,indent=2))
    page.locator('#asset-view').screenshot(path=str(OUT/'layered-guardian-closeup.png'))
    cdp.send('Page.stopScreencast');b.close()
concat=TMP/'frames.txt'
lines=[]
for i,(file,t) in enumerate(frames):
    lines.append("file '"+str(file)+"'")
    lines.append('duration '+str(max(.005,frames[i+1][1]-t) if i+1<len(frames) else .05))
concat.write_text('\n'.join(lines))
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-c:v','libvpx-vp9','-crf','35','-b:v','0','-pix_fmt','yuv420p',str(OUT/'guardian-recoil.webm')],check=True)
assert len(frames)>20
assert max(s['offset'] for s in trace)>9
assert all(s['tank']==trace[0]['tank'] for s in trace)
print(json.dumps({'frames':len(frames),'trace_samples':len(trace),'max_barrel_offset_master_px':max(s['offset'] for s in trace),'hull_stationary':True}))
# Managed Chromium prohibits file:// navigation. Validate self-contained preview
# over local HTTP while blocking every request except its initial document.
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page();errors=[];remote=[]
    page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:remote.append(r.url) if r.url.startswith(('http:','https:')) else None)
    url='http://127.0.0.1:8080/preview/guardian.html'
    page.route('**/*',lambda route:route.continue_() if route.request.url==url else route.abort())
    page.goto(url);page.wait_for_function('window.guardianPOC');page.locator('#start').click();page.keyboard.down('Space');page.wait_for_timeout(600);page.keyboard.up('Space')
    s=page.evaluate('guardianPOC.snapshot()');assert s['state']['shots']==1 and s['state']['destroyed']==1;assert not errors and remote==[url]
    (OUT/'offline-preview-check.json').write_text(json.dumps({'opened_via':'local HTTP, all requests other than initial HTML blocked','direct_file_test':'Not verified: managed Chromium ERR_BLOCKED_BY_ADMINISTRATOR','passed':True,'shots':s['state']['shots'],'walls_destroyed':s['state']['destroyed'],'runtime_errors':errors,'additional_requests':[u for u in remote if u!=url]},indent=2))
    b.close()
print('Self-contained preview shooting/destruction passed; only initial local HTML request permitted')
