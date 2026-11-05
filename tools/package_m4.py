"""Deterministic bounded M4 review ZIP, with committed-preview provenance."""
from pathlib import Path
import hashlib
import json
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'artifacts/Armorheart-Siege-M4.zip'
payload = {
    'guardian.html': (ROOT / 'preview/guardian.html').read_bytes(),
    'README.md': (ROOT / 'docs/PLAY_M4.md').read_bytes(),
}
for label, directory in [('GUARDIAN', 'guardian'), ('TRANSPORT', 'transport'),
                         ('COLOSSUS', 'colossus'), ('BATTLESHIP', 'battleship'), ('FORTRESS', 'fortress')]:
    payload[label + '_PROVENANCE.md'] = (ROOT / 'assets' / directory / 'PROVENANCE.md').read_bytes()
source = subprocess.check_output(
    ['git', 'log', '-1', '--format=%H', '--', 'preview/guardian.html'], cwd=ROOT,
).decode().strip()
assert subprocess.check_output(['git', 'show', source + ':preview/guardian.html'], cwd=ROOT) == payload['guardian.html'], 'Commit preview before packaging'
manifest = {
    'execution_authorization': 'ce298580273e34da872f1d99e5150edbcc109c12',
    'accepted_siege_offer': 'a44485475d573d65228d70e377e2561fed9f0e47',
    'accepted_m3_baseline': '108515a2f63c4818567d46de6bbcc0aa0611af07',
    'accepted_r3_baseline': '1d6abaa4f8f98bb0034641bde855ac4b16786bed',
    'accepted_corrected_m2': '94493a6380f5fd34a6f56e059728c7b6ec69e21e',
    'preview_source_commit': source,
    'approved_map_sha256': hashlib.sha256((ROOT / 'planning/siege-m4/map.json').read_bytes()).hexdigest(),
    'status': 'Bounded playable M4 for creative-director Confirm & Close; not a deployment/publication',
    'original_reference_archive': 'Pending: promised ZIP/PNG/manifest not exposed in this session; expected hash is unverified',
    'sha256': {name: hashlib.sha256(value).hexdigest() for name, value in payload.items()},
}
payload['SOURCE.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
with zipfile.ZipFile(TARGET, 'w', zipfile.ZIP_DEFLATED) as archive:
    for name, value in payload.items():
        info = zipfile.ZipInfo('Siege-M4/' + name, (2026, 11, 4, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, value)
with zipfile.ZipFile(TARGET) as archive:
    assert archive.testzip() is None
    for name, value in payload.items():
        assert archive.read('Siege-M4/' + name) == value
report = {
    'passed': True, 'bytes': TARGET.stat().st_size,
    'zip_sha256': hashlib.sha256(TARGET.read_bytes()).hexdigest(),
    'preview_source_commit': source, 'payload_sha256': manifest['sha256'],
    'payload_checksums_and_crc_verified': True,
}
(ROOT / 'evidence/m4/package-check.json').write_text(json.dumps(report, indent=2) + '\n')
print(TARGET.name, report['bytes'], 'bytes; source', source)
