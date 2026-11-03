"""Bind R3 evidence to accepted engine/assets/Guardian renderer and approved map."""
from pathlib import Path
import subprocess,hashlib,json
ROOT=Path(__file__).resolve().parents[1];BASE='bfd228359fbf56f03f921cb3d3439c7c26ed5c79';PLAN='026fb7a68b6a2e6ae18c11e38fee6a75e8d9c931'
def old(ref,path):return subprocess.check_output(['git','show',ref+':'+path],cwd=ROOT)
def digest(data):return hashlib.sha256(data).hexdigest()
paths=['src/engine.mjs','index.html','style.css','docs/ARMORHEART_GDD_v1.0.md','docs/standards/UGDS.md','docs/standards/AICP.md',*[str(p.relative_to(ROOT)) for p in sorted((ROOT/'assets/guardian').iterdir()) if p.is_file()]]
rows=[]
for path in paths:
 data=(ROOT/path).read_bytes();same=data==old(BASE,path);assert same,path;rows.append(dict(path=path,identical=True,sha256=digest(data)))
now=(ROOT/'src/app.mjs').read_text();before=old(BASE,'src/app.mjs').decode()
segments=[('tank draw','function tank(', '\nfunction drawComparisons'),('muzzle flash',' const flashAge=', '\n if(isMission())')]
for name,a,b in segments:
 x=now[now.index(a):now.index(b,now.index(a))];y=before[before.index(a):before.index(b,before.index(a))];assert x==y,name;rows.append(dict(path='src/app.mjs: '+name,identical=True,sha256=digest(x.encode())))
path='planning/r3-geometry/map.json';assert (ROOT/path).read_bytes()==old(PLAN,path)
report=dict(baseline=BASE,approved_geometry=PLAN,map_sha256=digest((ROOT/path).read_bytes()),checks=rows,guardian_unchanged=True)
(ROOT/'evidence/r3/baseline-comparison.json').write_text(json.dumps(report,indent=2)+'\n');print('Frozen engine, Guardian renderer/assets, UI shell and exact approved map verified')
