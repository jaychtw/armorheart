"""Non-destructive normalization/export of original paint master into Guardian registration.
Original PNG is preserved. Editable SVG transforms/masks are the source of truth.
"""
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import hashlib,json,base64
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/tanks';source=OUT/'source/production-paint.png';raw=source.read_bytes();im=Image.open(source).convert('RGBA');width,height=im.size;data='data:image/png;base64,'+base64.b64encode(raw).decode();names=['bulwark','vanguard','sentinel'];manifest={'status':'Original mixed raster/vector cosmetic collection for integrated v1 creative review','source':'source/production-paint.png','source_sha256':hashlib.sha256(raw).hexdigest(),'prompt':'source/production-prompt.txt','reference':'source/construction-reference.png','reference_sha256':hashlib.sha256((OUT/'source/construction-reference.png').read_bytes()).hexdigest(),'generation':'Host-native ImageGen, original three-tank paint pass of the authored construction; no external provider account/job or additional paid service','physics':{'hullMaster':[12,70,198,185],'pivot':[107,128],'muzzle':[243,126],'scale':.5,'recoil':'unchanged accepted master12-pixel retraction'},'tanks':{}}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);pg=b.new_page();pg.route('**/*',lambda r:r.abort());pg.set_content('<canvas width="256" height="256"></canvas>')
 for i,name in enumerate(names):
  left=i*width//3;right=(i+1)*width//3;mask=im.crop((left,0,right,height)).getchannel('A').point(lambda a:255 if a>96 else 0);bbox=mask.getbbox();assert bbox
  x0,y0,xTip,y1=bbox;x0+=left;xTip+=left
  bodyRight=max(x for x in range(x0,xTip) if (lambda r:r and r[3]-r[1]>80)(im.crop((x,0,x+1,height)).getchannel('A').point(lambda a:255 if a>96 else 0).getbbox()))+1
  bodybox=im.crop((x0,0,bodyRight,height)).getchannel('A').point(lambda a:255 if a>96 else 0).getbbox();y0,y1=bodybox[1],bodybox[3]
  tipcol=im.crop((xTip-4,0,xTip-3,height)).getchannel('A').point(lambda a:255 if a>96 else 0).getbbox();axis=(tipcol[1]+tipcol[3])/2
  sx,sy=186/(bodyRight-x0),115/(y1-y0);bs=45/(xTip-bodyRight)
  bodyMatrix=f'{sx} 0 0 {sy} {12-sx*x0} {70-sy*y0}';barrelMatrix=f'{bs} 0 0 {sy} {198-bs*bodyRight} {126-sy*axis}'
  start='<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">'
  defs='<defs><clipPath id="bodyClip"><rect x="12" y="70" width="186" height="115"/></clipPath><clipPath id="barrelClip"><path d="M158 114H245V138H158Z"/></clipPath></defs>'
  body=f'<g id="hull" clip-path="url(#bodyClip)"><image width="{width}" height="{height}" transform="matrix({bodyMatrix})" href="{data}"/></g>'
  barrel=f'<g id="barrel" clip-path="url(#barrelClip)"><image width="{width}" height="{height}" transform="matrix({barrelMatrix})" href="{data}"/></g>'
  dest=OUT/name;dest.mkdir(exist_ok=True);(dest/'source.svg').write_text(start+defs+barrel+body+'</svg>\n')
  for part,group in [('hull',body),('barrel',barrel)]:
   svg=start+defs+group+'</svg>';encoded=pg.evaluate('''async data=>{const i=new Image();i.src='data:image/svg+xml;base64,'+data;await i.decode();const c=document.querySelector('canvas'),x=c.getContext('2d');x.clearRect(0,0,256,256);x.drawImage(i,0,0);return c.toDataURL('image/png').split(',')[1]}''',base64.b64encode(svg.encode()).decode());png=base64.b64decode(encoded);(dest/(part+'.png')).write_bytes(png);(dest/(part+'.svg')).write_text(start+'<image width="256" height="256" href="data:image/png;base64,'+base64.b64encode(png).decode()+'"/></svg>\n')
  manifest['tanks'][name]={'original_cell':[left,0,right,height],'original_hull':[x0,y0,bodyRight,y1],'original_muzzle':[xTip,axis],'body_transform':bodyMatrix,'barrel_transform':barrelMatrix,'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(dest.glob('*'))},'design':{'bulwark':'stepped heavy shoulders/slab casemate','vanguard':'tapered prow/arrowhead turret','sentinel':'track pods/round sensor turret'}[name]}
 b.close()
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Three original painted skins exported into the unchanged Guardian frame, with independently recoiling barrel layers')
