"""Clean committed-source reconstruction; original generated paint is an archived input."""
from pathlib import Path
import hashlib,io,json,subprocess,tarfile,tempfile
ROOT=Path(__file__).resolve().parents[1];SOURCE=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
OUTPUTS=['assets/tanks/manifest.json','preview/guardian.html']+[f'assets/tanks/{tank}/{part}' for tank in ['bulwark','vanguard','sentinel'] for part in ['source.svg','hull.png','barrel.png','hull.svg','barrel.svg']]
STEPS=[['python3','tools/export_collection.py'],['python3','tools/build_preview.py']]
with tempfile.TemporaryDirectory(prefix='armorheart-v1-rebuild-',dir='/tmp') as d:
 clean=Path(d)
 with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','archive',SOURCE],cwd=ROOT))) as tar:tar.extractall(clean,filter='data')
 for cmd in STEPS:subprocess.run(cmd,cwd=clean,check=True)
 hashes={}
 for name in OUTPUTS:
  expected=subprocess.check_output(['git','show',SOURCE+':'+name],cwd=ROOT);actual=(clean/name).read_bytes();assert actual==expected,'Non-identical reconstruction: '+name;hashes[name]=hashlib.sha256(actual).hexdigest()
report=dict(passed=True,source_commit=SOURCE,method='git archive into empty directory; rebuild from archived original paint/reference and accepted runtime assets; byte comparison against committed outputs',steps=STEPS,byte_identical_sha256=hashes,toolchain={'chromium':'154.0.8037.57','playwright':'1.62.0','Pillow':'12.3.0'},limitations='Same installed environment/toolchain; ImageGen source generation is not deterministic and is not rerun. Exact archived original PNG is a reconstruction input.')
(ROOT/'evidence/v1/rebuild-check.json').write_text(json.dumps(report,indent=2)+'\n');print('Clean v1 reconstruction:',len(hashes),'outputs byte-identical; source',SOURCE)
