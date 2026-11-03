"""Label unaltered actual-render PNG crops for compact human review."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence/r3-visual'
rows=[]
for state,label in [('rest','Rest'),('peak','Near peak recoil'),('returning','Recovering'),('returned','Returned')]:
 cells=''.join(f'<figure><img src="http://127.0.0.1:8080/evidence/r3-visual/{state}-1440-{f}.png"><figcaption>{f.upper()}</figcaption></figure>' for f in ['up','right','down','left'])
 rows.append('<section><h2>'+label+'</h2><div>'+cells+'</div></section>')
html='''<html lang="en"><meta charset="utf-8"><title>R3 occlusion evidence</title><style>body{margin:20px;background:#eeeede;color:#24392e;font:16px system-ui}h1{font-size:24px}h2{font-size:17px;margin:12px 0 4px}section>div{display:flex;gap:12px}figure{margin:0;background:#d9decd}img{display:block;width:200px;height:200px}figcaption{text-align:center;font-size:12px;padding:3px}</style><h1>Guardian — fixed turret covers the sliding barrel mount</h1><p>Actual corrected Chromium render crops. Rest → recoil → recovery; artwork, scale and recoil transform unchanged.</p>'''+''.join(rows)+'</html>'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);pg=b.new_page(viewport=dict(width=900,height=1150));pg.set_content(html);pg.evaluate('async()=>{await Promise.all([...document.images].map(im=>im.decode()))}');pg.screenshot(path=str(OUT/'occlusion-review.png'),full_page=True);b.close()
print(OUT/'occlusion-review.png')
