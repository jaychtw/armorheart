"""Create a deterministic playable ZIP from the already-tested self-contained HTML."""
from pathlib import Path
import hashlib
import json
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
target = ROOT / 'artifacts/Armorheart-Guardian-POC.zip'
target.parent.mkdir(exist_ok=True)
payload = {
    'guardian.html': (ROOT / 'preview/guardian.html').read_bytes(),
    'README.md': (ROOT / 'docs/PLAY_PREVIEW.md').read_bytes(),
    'PROVENANCE.md': (ROOT / 'assets/guardian/PROVENANCE.md').read_bytes(),
}
source = subprocess.check_output(
    ['git', 'log', '-1', '--format=%H', '--', 'preview/guardian.html'], cwd=ROOT
).decode().strip()
payload['SOURCE.json'] = json.dumps({
    'preview_source_commit': source,
    'sha256': {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()},
    'status': 'Guardian POC; no merge, deployment or production acceptance',
}, indent=2).encode()
with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
    for name, data in payload.items():
        info = zipfile.ZipInfo('Guardian-POC/' + name, (2026, 11, 2, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, data)
with zipfile.ZipFile(target) as archive:
    assert archive.testzip() is None
    assert archive.read('Guardian-POC/guardian.html') == payload['guardian.html']
print(target)
print('Bytes:', target.stat().st_size)
print('SHA256:', hashlib.sha256(target.read_bytes()).hexdigest())
