"""Bundle local ES modules as data URLs; static/offline, Python stdlib only."""
from pathlib import Path
import re,base64,json
ROOT=Path(__file__).resolve().parents[1]
cache={}
def module(path):
    path=path.resolve()
    if path in cache:return cache[path]
    if not path.is_relative_to(ROOT/'src'):raise ValueError('Nonlocal source import')
    source=path.read_text()
    if path.name=='app.mjs':
        images={name:'data:image/svg+xml;base64,'+base64.b64encode((ROOT/f'assets/guardian/{name}.svg').read_bytes()).decode() for name in ['hull','barrel']}
        truck='data:image/svg+xml;base64,'+base64.b64encode((ROOT/'assets/transport/transport.svg').read_bytes()).decode()
        colossus={p.stem:'data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode() for p in sorted((ROOT/'assets/colossus/frames').glob('*.png'))}
        fortress={p.stem:'data:'+('image/svg+xml' if p.suffix=='.svg' else 'image/png')+';base64,'+base64.b64encode(p.read_bytes()).decode() for p in sorted((ROOT/'assets/fortress').glob('*')) if p.name in ['intact.png','broken.png','half.png','barrel.svg','gun-cap.svg']}
        battleship='data:image/png;base64,'+base64.b64encode((ROOT/'assets/battleship/battleship.png').read_bytes()).decode()
        source='const EMBEDDED_FORTRESS='+json.dumps(fortress)+';\nconst EMBEDDED_BATTLESHIP='+json.dumps(battleship)+';\nconst EMBEDDED_COLOSSUS='+json.dumps(colossus)+';\nconst EMBEDDED_TRUCK='+json.dumps(truck)+';\nconst EMBEDDED_LAYERS='+json.dumps(images)+';\n'+source.replace('im.src=`assets/guardian/${name}.svg`','im.src=EMBEDDED_LAYERS[name]').replace("im.src='assets/transport/transport.svg'",'im.src=EMBEDDED_TRUCK').replace('im.src=`assets/colossus/frames/${name}.png`','im.src=EMBEDDED_COLOSSUS[name]').replace("im.src='assets/battleship/battleship.png'",'im.src=EMBEDDED_BATTLESHIP').replace("im.src=`assets/fortress/${name}.${['barrel','gun-cap'].includes(name)?'svg':'png'}`",'im.src=EMBEDDED_FORTRESS[name]')
    source=re.sub(r'from\s+([\'"])(\.[^\'\"]+)\1',lambda m:'from '+json.dumps(module(path.parent/m[2])),source)
    url='data:text/javascript;base64,'+base64.b64encode(source.encode()).decode();cache[path]=url;return url
html=(ROOT/'index.html').read_text().replace('<link rel="stylesheet" href="style.css">','<style>'+(ROOT/'style.css').read_text()+'</style>')
html=html.replace('<script type="module" src="src/app.mjs"></script>','<script type="module">import '+json.dumps(module(ROOT/'src/app.mjs'))+';</script>')
out=ROOT/'preview/guardian.html';out.write_text(html);print(out,out.stat().st_size,'bytes;',len(cache),'local modules bundled')
