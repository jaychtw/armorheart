"""Deterministic M2 review ZIP; never replace previously accepted artifacts."""
from pathlib import Path
import hashlib,json,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[1]
target=ROOT/'artifacts/Armorheart-Colossus-M2-Final.zip'
payload={'guardian.html':(ROOT/'preview/guardian.html').read_bytes(),'README.md':(ROOT/'docs/PLAY_M2_FINAL.md').read_bytes()}
for label,directory in [('GUARDIAN','guardian'),('TRANSPORT','transport'),('COLOSSUS','colossus')]:
 payload[label+'_PROVENANCE.md']=(ROOT/'assets'/directory/'PROVENANCE.md').read_bytes()
source=subprocess.check_output(['git','log','-1','--format=%H','--','preview/guardian.html'],cwd=ROOT).decode().strip()
assert subprocess.check_output(['git','show',source+':preview/guardian.html'],cwd=ROOT)==payload['guardian.html'],'Commit preview before packaging'
manifest={'approved_offer':'e37d8d89e8834738680edee27d75c439cf6c37a7','accepted_r3_baseline':'1d6abaa4f8f98bb0034641bde855ac4b16786bed','preview_source_commit':source,'status':'Owner-accepted Colossus M2, authorized final presentation correction; no deployment/publication','sha256':{n:hashlib.sha256(v).hexdigest() for n,v in payload.items()}}
payload['SOURCE.json']=(json.dumps(manifest,indent=2)+'\n').encode()
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
 for n,v in payload.items():
  i=zipfile.ZipInfo('Colossus-M2/'+n,(2026,11,4,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o100644<<16;z.writestr(i,v)
with zipfile.ZipFile(target) as z:
 assert z.testzip() is None
 for n,v in payload.items():assert z.read('Colossus-M2/'+n)==v
report={'passed':True,'bytes':target.stat().st_size,'zip_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'preview_source_commit':source,'payload_sha256':manifest['sha256'],'payload_checksums_and_crc_verified':True}
(ROOT/'evidence/m2-final/package-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(target.name,report['bytes'],'bytes; source',source)
