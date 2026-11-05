"""Rasterize accepted editable SVG without repainting; source remains authoritative."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,base64,hashlib
ROOT=Path(__file__).resolve().parents[1];source=ROOT/'planning/interception-m3/art/battleship-editable.svg';raw=source.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='3eda4858e442181cf9125af205068e583390f7582e4a4bb4d35915e4e5cd71dd','Accepted ship SVG changed; do not silently repaint'

with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page();page.route('**/*',lambda r:r.abort());page.set_content('<canvas width="664" height="260"></canvas>');png=page.evaluate('''async(data)=>{const im=new Image();im.src='data:image/svg+xml;base64,'+data;await im.decode();const c=document.querySelector('canvas');c.getContext('2d').drawImage(im,0,0,664,260);return c.toDataURL('image/png').split(',')[1]}''',base64.b64encode(raw).decode());b.close()
out=ROOT/'assets/battleship/battleship.png';out.write_bytes(base64.b64decode(png));info={'source':str(source.relative_to(ROOT)),'accepted_art_commit':'29c5e871f6c7b92599880b60a3666943fa452a74','source_sha256':hashlib.sha256(raw).hexdigest(),'png_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'pixels':[664,260],'world_frame':[-166,-54,332,130],'body':[320,88],'muzzles':[[-88,66],[0,66],[88,66]],'method':'Chromium154 Canvas raster export of unchanged accepted SVG; no artistic correction','decoded_bytes':664*260*4};(ROOT/'assets/battleship/anchors.json').write_text(json.dumps(info,indent=2)+'\n');print(out.name,out.stat().st_size,'bytes')
