"""Compare clean tracked-source export/bundle against committed outputs."""
from pathlib import Path
import hashlib,io,json,subprocess,tarfile,tempfile
import PIL
ROOT=Path(__file__).resolve().parents[1]
source=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
files=['assets/colossus/manifest.json','assets/colossus/colossus-editable.svg','src/colossus-art.mjs','preview/guardian.html']+[str(p.relative_to(ROOT)) for p in sorted((ROOT/'assets/colossus/frames').glob('*.png'))]
with tempfile.TemporaryDirectory(prefix='armorheart-m2-rebuild-') as d:
 clean=Path(d)
 archive=subprocess.check_output(['git','archive',source],cwd=ROOT)
 with tarfile.open(fileobj=io.BytesIO(archive)) as t:t.extractall(clean,filter='data')
 subprocess.run(['python3','tools/export_colossus.py'],cwd=clean,check=True)
 subprocess.run(['python3','tools/build_preview.py'],cwd=clean,check=True)
 hashes={}
 for p in files:
  committed=subprocess.check_output(['git','show',source+':'+p],cwd=ROOT)
  assert (ROOT/p).read_bytes()==committed,'Working output differs from source commit: '+p
  assert (clean/p).read_bytes()==committed,'Clean rebuild differs: '+p
  hashes[p]=hashlib.sha256(committed).hexdigest()
report={'passed':True,'source_commit':source,'method':'git archive of tracked source; preserved original source sheets; fresh deterministic PNG/proxy/manifest/SVG export and embedded preview build, byte-for-byte comparison; same installed toolchain, not independent artwork generation or network clone','pillow':PIL.__version__,'files':hashes}
(ROOT/'evidence/m2/rebuild-check.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS clean rebuild:',len(files),'identical outputs')
