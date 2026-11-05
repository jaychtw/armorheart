"""Original layered-vector pose study only. No runtime assets or game logic."""
from pathlib import Path
import xml.etree.ElementTree as ET,json,hashlib
HERE=Path(__file__).resolve().parent
ET.register_namespace('','http://www.w3.org/2000/svg')
poses={
 'idle':{},
 'airborne':{'near-arm':'rotate(8 159 187)','far-arm':'rotate(-8 353 184)','near-leg':'translate(18 -36) rotate(-12 204 340)','far-leg':'translate(-12 -34) rotate(12 308 340)','head':'translate(0 -8)'},
 'landing':{'torso':'translate(0 25) translate(256 160) scale(1 .9) translate(-256 -160)','head':'translate(0 20)','near-arm':'rotate(-3 159 187)','far-arm':'rotate(3 353 184)'},
 'hit':{'torso':'rotate(-4 256 330)','head':'translate(-6 3) rotate(-5 260 160)','near-arm':'rotate(-4 159 187)','far-arm':'rotate(-3 353 184)'},
 'fatigued':{'torso':'translate(0 8)','head':'translate(0 12) rotate(3 260 160)','brows':'translate(0 2)','stage-marks':'opacity:.5'},
 'wounded':{'torso':'rotate(-5 256 330) translate(0 10)','head':'translate(-10 19) rotate(-6 260 160)','near-arm':'rotate(-13 159 187) translate(0 -24)','brows':'translate(0 3)','stage-marks':'opacity:1'}
}
for name,changes in poses.items():
 root=ET.parse(HERE/'colossus-master.svg').getroot()
 for node in root.iter():
  change=changes.get(node.get('id'))
  if change:
   if change.startswith('opacity:'):node.set('opacity',change.split(':')[1])
   else:node.set('transform',change)
 title=next(x for x in root if x.tag.endswith('title'));title.text='Colossus '+name+' — original one-view assessment, unaccepted'
 ET.ElementTree(root).write(HERE/(name+'.svg'),encoding='unicode',xml_declaration=True)
metadata={'status':'original editable single front-quarter pose study; not production or four-facing proof','source':[512,512],'world_scale':.5,'ground_anchor':[256,442],'proposed_ground_contact_ellipse_world':[100,64],'pose_names':list(poses),'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(HERE.glob('*.svg'))}}
(HERE/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
print('Built six pose/state candidates from one editable original master')
