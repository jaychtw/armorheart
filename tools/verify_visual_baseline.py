"""Verify the visual correction is exactly two authorized app changes."""
from pathlib import Path
import subprocess,json,hashlib
ROOT=Path(__file__).resolve().parents[1];BASE='7d9720d8cee846735d5f1bb2dfc231b66eb4af7c';OUT=ROOT/'evidence/r3-visual';OUT.mkdir(parents=True,exist_ok=True)
def old(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
paths=['src/engine.mjs','src/breakthrough.mjs','src/transport.mjs','src/maps/breakthrough.mjs','src/i18n.mjs','index.html','style.css','planning/r3-geometry/map.json','docs/ARMORHEART_GDD_v1.0.md','docs/standards/UGDS.md','docs/standards/AICP.md','artifacts/Armorheart-Guardian-POC.zip','artifacts/Armorheart-Breakthrough-M1.zip','artifacts/Armorheart-Breakthrough-R3.zip']
paths += [str(p.relative_to(ROOT)) for d in ['guardian','transport'] for p in sorted((ROOT/'assets'/d).iterdir()) if p.is_file()]
rows=[]
for path in paths:
 data=(ROOT/path).read_bytes();assert data==old(path),path;rows.append(dict(path=path,identical=True,sha256=hashlib.sha256(data).hexdigest()))
app=old('src/app.mjs').decode();a="else{c.drawImage(images[0],-107,-128);c.drawImage(images[1],-107-recoil(age,reduced()),-128);}"
b="// Fixed turret covers the sliding mount; the barrel transform is unchanged.\n else{c.drawImage(images[1],-107-recoil(age,reduced()),-128);c.drawImage(images[0],-107,-128);}"
c=" if(m.evacuatingAt!==null&&m.elapsed-m.evacuatingAt<2){ctx.strokeStyle='#fff4c4';ctx.lineWidth=2;ctx.strokeRect(-67,-31,134,62);}\n"
assert app.count(a)==1 and app.count(c)==1
expected=app.replace(a,b).replace(c,'');assert expected==(ROOT/'src/app.mjs').read_text(),'Unexpected app changes'
report=dict(baseline=BASE,frozen_files=rows,app_exactly_authorized_composition_and_outline_changes=True,recoil_muzzle_input_ui_and_gameplay_unchanged=True,accepted_limitation='Tank and transport remain nonblocking; optional future consideration, not a required task')
(OUT/'baseline-comparison.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS: two app edits only; frozen engine, assets, navigation, geometry, UI and pins identical')
