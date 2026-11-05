"""Rebuild preview from a clean local Git source archive (not a remote clone)."""
from pathlib import Path
import hashlib,io,json,subprocess,tarfile,tempfile,os
ROOT=Path(__file__).resolve().parents[1]
revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
archive=subprocess.check_output(['git','archive',revision],cwd=ROOT)
with tempfile.TemporaryDirectory(prefix='armorheart-r3-rebuild-') as tmp:
 directory=Path(tmp)
 with tarfile.open(fileobj=io.BytesIO(archive)) as tar:tar.extractall(directory,filter='data')
 expected=(directory/'preview/guardian.html').read_bytes()
 subprocess.run(['python3','tools/build_preview.py'],cwd=directory,check=True,capture_output=True)
 actual=(directory/'preview/guardian.html').read_bytes();assert actual==expected,'Nonreproducible preview'
report=dict(passed=True,source_commit=revision,method='clean tracked-source git archive, extract to temporary directory, rebuild using Python standard library, compare byte-for-byte',independent_network_clone=False,bytes=len(actual),sha256=hashlib.sha256(actual).hexdigest())
(ROOT/os.environ.get('EVIDENCE_DIR','evidence/r3')/'rebuild-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
