"""Reproduce planning calculations/diagram from a clean tracked-source archive.
Original generated rasters are preserved, not claimed to regenerate identically.
"""
from pathlib import Path
import base64,hashlib,io,json,subprocess,tarfile,tempfile,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();archive=subprocess.check_output(['git','archive',revision],cwd=ROOT)
with tempfile.TemporaryDirectory(prefix='colossus-offer-recovery-') as tmp:
 d=Path(tmp)
 with tarfile.open(fileobj=io.BytesIO(archive)) as tar:tar.extractall(d,filter='data')
 base=d/'planning/colossus-m2';expected=(base/'evidence/assessment.json').read_bytes();expected_map=(base/'arena.svg').read_bytes()
 subprocess.run(['node','planning/colossus-m2/assess.mjs'],cwd=d,check=True,capture_output=True);assert (base/'evidence/assessment.json').read_bytes()==expected
 subprocess.run(['python3','planning/colossus-m2/make_diagram.py'],cwd=d,check=True,capture_output=True);assert (base/'arena.svg').read_bytes()==expected_map
 output=d/'composition.svg';subprocess.run(['python3','planning/colossus-m2/art/build_composition.py',str(output)],cwd=d,check=True,capture_output=True)
 image=next(n for n in ET.parse(output).getroot().iter() if n.tag.endswith('image'));data=base64.b64decode(image.get('href').split(',',1)[1]);assert data==(base/'art/colossus-concept.png').read_bytes()
 names=['colossus-concept.png','pose-concepts.png'];images={n:hashlib.sha256((base/'art'/n).read_bytes()).hexdigest() for n in names}
 for n,h in images.items():assert hashlib.sha256((HERE/'art'/n).read_bytes()).hexdigest()==h
report={'passed':True,'source_commit':revision,'method':'clean local git archive, original PNG hashes, byte-identical planning report and diagram rebuild, SVG embedded raster byte comparison','independent_network_clone':False,'art_regeneration_claimed':False,'original_image_sha256':images,'not_retested':'M2 combat/four-view animation/human/physical-phone behavior; none implemented or claimed'}
(HERE/'evidence/recovery-results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
