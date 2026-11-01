"""Build a double-clickable offline preview using only the Python standard library."""
from pathlib import Path
import re,base64,json
ROOT=Path(__file__).resolve().parents[1]
def read(path):return (ROOT/path).read_text()
engine=read('src/engine.mjs').replace('export ','')
i18n=read('src/i18n.mjs').replace('export ','')
app=re.sub(r'^import .*?;\n','',read('src/app.mjs'),flags=re.M)
images={name:'data:image/svg+xml;base64,'+base64.b64encode((ROOT/f'assets/guardian/{name}.svg').read_bytes()).decode() for name in ['hull','barrel']}
app=app.replace('im.src=`assets/guardian/${name}.svg`','im.src=EMBEDDED_LAYERS[name]')
js='const EMBEDDED_LAYERS='+json.dumps(images)+';\n'+engine+'\n'+i18n+'\n'+app
html=read('index.html').replace('<link rel="stylesheet" href="style.css">','<style>'+read('style.css')+'</style>').replace('<script type="module" src="src/app.mjs"></script>','<script type="module">'+js+'</script>')
out=ROOT/'preview/guardian.html';out.parent.mkdir(exist_ok=True);out.write_text(html)
print(out, out.stat().st_size, 'bytes; no network requests required')
