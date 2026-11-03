"""Render the standalone map SVG in HTML; retain all original relative art links."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1040,'height':1040})
 page.goto('http://127.0.0.1:8080/planning/interception-m3/proof.html')
 page.set_content('<html><head><base href="http://127.0.0.1:8080/planning/interception-m3/"></head><body style="margin:0">'+(ROOT/'planning/interception-m3/map.svg').read_text()+'</body></html>')
 page.wait_for_timeout(500)
 page.screenshot(path=str(ROOT/'planning/interception-m3/evidence/map.png'),timeout=10000)
 b.close()
print('Rendered map overview')
