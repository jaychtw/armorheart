"""Capture isolated art assessment at measured accepted-game canvas sizes.
Not Level2 gameplay, damage or a product accessibility audit.
"""
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import json,hashlib,subprocess,math
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];OUT=HERE/'evidence';OUT.mkdir(exist_ok=True)
checks=[];errors=[];requests=[]
def check(name,ok,detail=None):
 checks.append(dict(name=name,passed=bool(ok),detail=detail))
 if not ok:raise AssertionError((name,detail))
art=HERE/'art';meta=json.load(open(art/'metadata.json'));im=Image.open(art/'colossus-concept.png');a=im.getchannel('A');hist=a.histogram()
alpha=dict(size=list(im.size),mode=im.mode,alpha_extrema=list(a.getextrema()),transparent_fraction=hist[0]/sum(hist),bounds_alpha8=list(a.point(lambda p:255 if p>=8 else 0).getbbox()),bounds_alpha200=list(a.point(lambda p:255 if p>=200 else 0).getbbox()),sha256=hashlib.sha256((art/'colossus-concept.png').read_bytes()).hexdigest())
check('original master has actual transparent exterior and visible body',hist[0]>0 and hist[255]>0,alpha)
core=im.getpixel((625,600));check('analytical shot witness uses opaque visible torso point',core[3]>200,dict(point=[625,600],rgba=core))
pose=Image.open(art/'pose-concepts.png');cells=[]
for i,name in enumerate(['idle','airborne','landing','hit','fatigued','wounded']):
 x=i%3*512;y=i//3*512;pa=pose.getchannel('A').crop((x,y,x+512,y+512));cells.append(dict(name=name,alpha8_bounds=list(pa.point(lambda v:255 if v>=8 else 0).getbbox()),status='unregistered concept, not a finished sprite'))
alpha['pose_concepts']=dict(size=list(pose.size),transparent_gutter_samples=[pose.getpixel(q)[3] for q in [(0,0),(512,512),(768,500)]],cells=cells)
(OUT/'art-inspection.json').write_text(json.dumps(alpha,indent=2)+'\n')
# Frozen current game source/assets are exactly the accepted visual completion.
paths=['src','assets','preview','index.html','style.css','package.json','tests','docs/standards','docs/ARMORHEART_GDD_v1.0.md','artifacts']
changed=subprocess.check_output(['git','diff','--name-only','1d6abaa4f8f98bb0034641bde855ac4b16786bed','--',*paths],cwd=ROOT).decode().splitlines()
check('accepted runtime/assets/tests/pins and playable ZIPs unchanged',not changed,changed)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);metrics=[]
 for width,height,dpr in [(320,740,2),(390,844,2),(768,1024,1),(1440,1000,1)]:
  c=b.new_context(viewport=dict(width=width,height=height),device_scale_factor=dpr);pg=c.new_page();pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('request',lambda r:requests.append(r.url))
  pg.goto('http://127.0.0.1:8080/');pg.wait_for_function('window.guardianPOC');pg.locator('#choose-mission').click();accepted=pg.locator('#arena').bounding_box()['width']
  pg.goto('http://127.0.0.1:8080/planning/colossus-m2/lab.html');pg.wait_for_function('window.colossusStudy');box=pg.locator('#arena').bounding_box();w=box['width']
  check(f'{width} same actual accepted arena size',abs(w-accepted)<.1,dict(accepted=accepted,study=w,dpr=dpr))
  check(f'{width} no horizontal assessment overflow',not pg.evaluate('document.documentElement.scrollWidth>innerWidth'))
  bounds=alpha['bounds_alpha8'];body=(bounds[2]-bounds[0])*256/1254*w/768;face=180*256/1254*w/768
  metrics.append(dict(width=width,height=height,dpr=dpr,canvas_css=w,accepted_canvas_css=accepted,guardian_hull_css=93*w/768,painted_boss_width_css=body,approx_face_landmark_width_css=face,face_note='approx source180px landmark, not a readability pass'))
  pg.locator('#arena').screenshot(path=str(OUT/f'scale-{width}.png'));pg.locator('#arena').scroll_into_view_if_needed();pg.screenshot(path=str(OUT/f'viewport-{width}.png'))
  if width==1440:pg.locator('.pose-grid').screenshot(path=str(OUT/'original-master-inspection.png'))
  if width==320:
   for view,anchor in [('upper-left',[208,288]),('upper-right',[560,288]),('lower-right',[560,544]),('lower-left',[208,544]),('center',[384,416])]:
    pg.locator('#view').select_option(view);r=pg.evaluate('colossusStudy');check('320 ground registration '+view,r['anchor']==anchor and r['height']==0,r);pg.locator('#arena').screenshot(path=str(OUT/(view+'-320.png')))
   pg.locator('#view').select_option('hop')
   for t in [0,.25,.5,.75,1]:
    pg.locator('#progress').fill(str(t));pg.locator('#progress').dispatch_event('input');r=pg.evaluate('colossusStudy');check('hop registration sample '+str(t),abs(r['anchor'][0]-(208+352*t))<1e-8 and abs(r['height']-64*math.sin(math.pi*t))<1e-8,r);pg.locator('#arena').screenshot(path=str(OUT/f'height-{t}.png'))
  if width==390:
   for pose_name in ['idle','airborne','landing','hit','fatigued','wounded']:
    pg.locator('#pose').select_option('study-'+pose_name);check('concept cell '+pose_name,pg.evaluate('colossusStudy.pose')=='study-'+pose_name);pg.locator('#arena').screenshot(path=str(OUT/f'concept-{pose_name}-390.png'))
  c.close()
 check('no assessment JavaScript errors',not errors,errors)
 check('no external assessment runtime requests',not [u for u in requests if not u.startswith(('http://127.0.0.1:8080','data:'))]);b.close()
(OUT/'capture-results.json').write_text(json.dumps(dict(date='2026-11-03 Asia/Taipei',passed=len(checks),failed=0,checks=checks,scales=metrics,errors=errors,scope='isolated art/layout/registration and planning checks, not M2 gameplay or human acceptance',not_performed=['M2 combat/browser playthrough','physical phone','independent first-time-player','four-facing/side-back animation','product M2 bilingual/a11y/offline acceptance']),indent=2)+'\n')
print(json.dumps(dict(passed=len(checks),failed=0,scales=metrics)))
