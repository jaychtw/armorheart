"""Stage only the accepted self-contained runtime and public build identity."""
from pathlib import Path
import hashlib,json,re,subprocess,shutil,zipfile
ROOT=Path(__file__).resolve().parents[1]
COMMIT=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
EXPECTED_HTML='62f18789f7ac32b807f1ca5dff41f1b90d42997dc7bdaa356a3b80146bc42bb2'
EXPECTED_ZIP='6afd0bb8771494e96d9625e23f74e76e13c486061d8ace702849c5d7ad4ec466'
assert re.fullmatch('[0-9a-f]{40}',COMMIT)
html=(ROOT/'preview/guardian.html').read_bytes();archive=ROOT/'artifacts/Armorheart-v1.0-RC.zip'
assert hashlib.sha256(html).hexdigest()==EXPECTED_HTML,'Runtime differs from accepted RC1'
assert hashlib.sha256(archive.read_bytes()).hexdigest()==EXPECTED_ZIP,'Review ZIP differs from accepted RC1'
assert subprocess.check_output(['git','show',COMMIT+':preview/guardian.html'],cwd=ROOT)==html,'Uncommitted runtime'
with zipfile.ZipFile(archive) as z:assert z.read('Armorheart-v1.0-RC/index.html')==html
out=ROOT/'.release-site';out.mkdir(exist_ok=True)
for p in out.iterdir():
 if p.is_dir():shutil.rmtree(p)
 else:p.unlink()
(out/'index.html').write_bytes(html)
info={'project':'Armorheart','version':'1.0.0','source_commit':COMMIT,'reviewed_candidate':'42e98a6233faf4e126d54e05dac5806c44469489','runtime_source_commit':'f1a0f2379ccddbae4a3f97dd2901743ccdadec38','publication_authority':'3b8d7fe4d6a46f451d2c4fdb6e808f4bba900d72','index_sha256':EXPECTED_HTML,'review_zip_sha256':EXPECTED_ZIP,'runtime_note':'Exact creatively accepted RC1 payload; in-game candidate labeling retained to avoid changing reviewed executable'}
(out/'build-info.json').write_text(json.dumps(info,indent=2)+'\n')
(out/'.nojekyll').write_bytes(b'')
assert {p.name for p in out.iterdir()}=={'index.html','build-info.json','.nojekyll'}
print(json.dumps(info))
