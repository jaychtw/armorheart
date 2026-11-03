"""Deterministic bounded R3 review ZIP; keep previous Guardian/M1 ZIPs intact."""
from pathlib import Path
import hashlib,json,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[1];target=ROOT/'artifacts/Armorheart-Breakthrough-R3.zip'
payload={'guardian.html':(ROOT/'preview/guardian.html').read_bytes(),'README.md':(ROOT/'docs/PLAY_R3.md').read_bytes(),'GUARDIAN_PROVENANCE.md':(ROOT/'assets/guardian/PROVENANCE.md').read_bytes(),'TRANSPORT_PROVENANCE.md':(ROOT/'assets/transport/PROVENANCE.md').read_bytes()}
source=subprocess.check_output(['git','log','-1','--format=%H','--','preview/guardian.html'],cwd=ROOT).decode().strip()
assert subprocess.check_output(['git','show',source+':preview/guardian.html'],cwd=ROOT)==payload['guardian.html'],'Commit preview before packaging'
manifest={'preview_source_commit':source,'approved_geometry_commit':'026fb7a68b6a2e6ae18c11e38fee6a75e8d9c931','status':'Bounded R3 prototype for creative-director Confirm & Close; no deployment/publication','sha256':{n:hashlib.sha256(v).hexdigest() for n,v in payload.items()}}
payload['SOURCE.json']=json.dumps(manifest,indent=2).encode()
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
 for n,v in payload.items():
  i=zipfile.ZipInfo('Breakthrough-R3/'+n,(2026,11,3,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o100644<<16;z.writestr(i,v)
with zipfile.ZipFile(target) as z:
 assert z.testzip() is None
 for n,h in manifest['sha256'].items():assert hashlib.sha256(z.read('Breakthrough-R3/'+n)).hexdigest()==h
(ROOT/'evidence/r3/package-check.json').write_text(json.dumps({'passed':True,'bytes':target.stat().st_size,'zip_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'preview_source_commit':source,'payload_checksums_verified':True},indent=2)+'\n')
print(target,target.stat().st_size,'bytes; source',source)
