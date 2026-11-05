"""Deterministic unified offline release candidate; does not deploy or publish."""
from pathlib import Path
import hashlib,json,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/'artifacts/Armorheart-v1.0-RC.zip';PREFIX='Armorheart-v1.0-RC/'
payload={'index.html':(ROOT/'preview/guardian.html').read_bytes(),'README.md':(ROOT/'docs/PLAY_V1.md').read_bytes()}
for label,directory in [('GUARDIAN','guardian'),('TRANSPORT','transport'),('COLOSSUS','colossus'),('BATTLESHIP','battleship'),('FORTRESS','fortress'),('COLLECTION','tanks')]:payload[label+'_PROVENANCE.md']=(ROOT/'assets'/directory/'PROVENANCE.md').read_bytes()
source=subprocess.check_output(['git','log','-1','--format=%H','--','preview/guardian.html'],cwd=ROOT).decode().strip();assert subprocess.check_output(['git','show',source+':preview/guardian.html'],cwd=ROOT)==payload['index.html'],'Commit preview before packaging'
manifest=dict(version='1.0.0-rc.1',status='Integrated release candidate for final Confirm & Close; no merge/deployment/publication authorized',authority='eb01bdb18ab1ccc5232009ccb244e1f8ca79c219',accepted_four_mission_baseline='ebf7d3e95c9e6076434efa50e6f662ce674bdfe8',preview_source_commit=source,collection_manifest_sha256=hashlib.sha256((ROOT/'assets/tanks/manifest.json').read_bytes()).hexdigest(),original_m3_reference_archive='Still unavailable; historical pending archival, not asserted received or hash-verified',sha256={n:hashlib.sha256(v).hexdigest()for n,v in payload.items()})
payload['SOURCE.json']=(json.dumps(manifest,indent=2)+'\n').encode()
def package():
 with zipfile.ZipFile(TARGET,'w',zipfile.ZIP_DEFLATED) as archive:
  for name,value in payload.items():
   info=zipfile.ZipInfo(PREFIX+name,(2026,11,4,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;archive.writestr(info,value)
package();first=TARGET.read_bytes();package();assert first==TARGET.read_bytes(),'Non-reproducible ZIP'
with zipfile.ZipFile(TARGET) as archive:
 assert archive.testzip() is None
 for name,value in payload.items():assert archive.read(PREFIX+name)==value
report=dict(passed=True,bytes=TARGET.stat().st_size,zip_sha256=hashlib.sha256(first).hexdigest(),preview_source_commit=source,payload_sha256=manifest['sha256'],crc_and_payload_verified=True,repeated_zip_identical=True)
(ROOT/'evidence/v1/package-check.json').write_text(json.dumps(report,indent=2)+'\n');print(TARGET.name,report['bytes'],'bytes; SHA256',report['zip_sha256'])
