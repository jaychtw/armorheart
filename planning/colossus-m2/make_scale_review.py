"""Show actual captures at their CSS sizes, compensating for phone DPR2."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
HERE=Path(__file__).resolve().parent;OUT=HERE/'evidence';r=json.load(open(OUT/'capture-results.json'));metrics={m['width']:m for m in r['scales']};url='http://127.0.0.1:8080/planning/colossus-m2/evidence/'
def figure(width):
 m=metrics[width];return f'<figure style="width:{m["canvas_css"]}px"><img style="width:{m["canvas_css"]}px" src="{url}scale-{width}.png"><figcaption>{width}px viewport · canvas{m["canvas_css"]:.1f}px<br>boss{m["painted_boss_width_css"]:.1f}px / Guardian{m["guardian_hull_css"]:.1f}px</figcaption></figure>'
html='<html lang="en"><meta charset="utf-8"><title>Colossus actual CSS-scale review</title><style>body{margin:20px;background:#e8ebde;color:#263d31;font:16px system-ui}h1{font-size:21px}p{max-width:640px}figure{margin:0}img{display:block;height:auto}figcaption{padding:8px 0;font-size:13px}.phones{display:flex;gap:20px;align-items:start}</style><h1>Original Colossus candidate · actual CSS-size comparison</h1><p>Isolated assessment, not Level2 gameplay. Phone DPR2 captures are displayed here at their original CSS width. Same master image and accepted Guardian assets/scale; artistic acceptance remains pending.</p><div class="phones">'+figure(320)+figure(390)+'</div><h2>Desktop canvas</h2>'+figure(1440)+'</html>'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);pg=b.new_page(viewport=dict(width=700,height=1300),device_scale_factor=1);pg.set_content(html);pg.evaluate('async()=>{await Promise.all([...document.images].map(x=>x.decode()))}');pg.screenshot(path=str(OUT/'actual-css-scale-review.png'),full_page=True);b.close()
print(OUT/'actual-css-scale-review.png')
