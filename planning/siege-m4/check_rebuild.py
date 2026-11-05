"""Reconstruct the four generated planning outputs from committed input bytes."""
from pathlib import Path
import subprocess, tempfile, tarfile, io, json, hashlib
ROOT=Path(__file__).resolve().parents[2]
source=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
names=['art/fortress-study.svg','evidence/map.svg','evidence/clearance-certificate.json','evidence/feasibility.json']
commands=[['python3','planning/siege-m4/art/build_study.py'],['python3','planning/siege-m4/draw_map.py'],['python3','planning/siege-m4/certify_clearance.py'],['node','planning/siege-m4/assess.mjs']]
with tempfile.TemporaryDirectory(prefix='armorheart-siege-offer-',dir='/tmp') as folder:
 clean=Path(folder)
 archive=subprocess.check_output(['git','archive',source,'src','planning/siege-m4'],cwd=ROOT)
 with tarfile.open(fileobj=io.BytesIO(archive)) as t:t.extractall(clean,filter='data')
 for cmd in commands:subprocess.run(cmd,cwd=clean,check=True,stdout=subprocess.DEVNULL)
 hashes={}
 for name in names:
  path='planning/siege-m4/'+name;actual=(clean/path).read_bytes();expected=subprocess.check_output(['git','show',source+':'+path],cwd=ROOT)
  assert actual==expected,path
  hashes[path]=hashlib.sha256(actual).hexdigest()
report={'passed':True,'source_commit':source,'method':'Clean git archive of committed planning directory and read-only src dependencies; regenerate four planning outputs and compare bytes','steps':commands,'byte_identical_sha256':hashes,'limitations':'Same environment; no new browser renders or actual M4 gameplay verification. This is planning-source reconstruction, not a Stage4 game build.'}
(ROOT/'planning/siege-m4/evidence/rebuild-check.json').write_text(json.dumps(report,indent=2)+'\n')
print('Four clean planning outputs byte-identical; source',source)
