from pathlib import Path
from PIL import Image,ImageChops
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'assets/fortress';A=json.loads((D/'anchors.json').read_text());images=[]
raw=(ROOT/'planning/siege-m4/art/fortress-study.svg').read_bytes();assert raw==subprocess.check_output(['git','show','a44485475d573d65228d70e377e2561fed9f0e47:planning/siege-m4/art/fortress-study.svg'],cwd=ROOT)
checks=[]
for name in ['intact','broken','half']:
 p=D/(name+'.png');im=Image.open(p).convert('RGBA');assert im.size==(512,320);assert im.getchannel('A').getextrema()==(255,255);assert hashlib.sha256(p.read_bytes()).hexdigest()==A['sha256'][p.name];images.append(im);checks.append(dict(stage=name,pixels=list(im.size),all_physical_body_pixels_opaque=True,bytes=p.stat().st_size))
assert ImageChops.difference(images[0].convert('RGB'),images[1].convert('RGB')).getbbox();assert ImageChops.difference(images[1].convert('RGB'),images[2].convert('RGB')).getbbox()
r={'passed':True,'approved_study_unchanged':True,'decoded_body_bytes':3*512*320*4,'body_states':checks,'registration':A,'note':'Pixel/registration consistency, not creative acceptance. Actual barrel draw transforms/muzzles are checked separately in browser-results.json.'}
(ROOT/'evidence/m4/asset-check.json').write_text(json.dumps(r,indent=2)+'\n');print('PASS3distinct opaque physical foundations and preserved approved study; decoded body memory1.875MiB')
