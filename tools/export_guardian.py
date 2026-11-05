"""Rebuild editable SVG layers; standard library only, no raster processing."""
from pathlib import Path
import base64, xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / 'assets/guardian'
source = ASSET / 'guardian-source.svg'
if not source.exists():
    data = base64.b64encode((ASSET / 'original-master.png').read_bytes()).decode()
    source.write_text('''<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="256" height="256" viewBox="0 0 256 256">
<title>Guardian prototype — editable hull and sliding barrel</title>
<desc>Right-facing, source raster preserved. Hull center 107,128. Barrel axis y=126. Layers are editable masks and vector surface repair. Unapproved prototype.</desc>
<defs>
  <image id="master" width="256" height="256" href="data:image/png;base64,''' + data + '''"/>
  <mask id="fixedMask"><rect width="256" height="256" fill="white"/><path d="M168 119 H246 V134 H168Z" fill="black"/></mask>
  <clipPath id="barrelClip"><path d="M168 119 H246 V134 H168Z"/></clipPath>
  <linearGradient id="repair" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#e2c181"/><stop offset=".5" stop-color="#bc9457"/><stop offset="1" stop-color="#8c693a"/></linearGradient>
</defs>
<g id="hull" aria-label="Fixed hull and turret">
  <use href="#master" mask="url(#fixedMask)"/>
  <!-- Reconstructed stationary surface exposed as the gun slides back. -->
  <path d="M166 118 L188 118 L188 135 L166 135Z" fill="url(#repair)"/>
  <path d="M166 118 H188 M188 118 V135 M166 135 H188" fill="none" stroke="#73542e" stroke-width="1"/>
  <path d="M171 120 V133 M179 120 V133" stroke="#d0ad6c" stroke-width=".7"/>
</g>
<g id="barrel" aria-label="Sliding barrel, positive X axis"><use href="#master" clip-path="url(#barrelClip)"/></g>
</svg>''')
ET.register_namespace('', 'http://www.w3.org/2000/svg')
for layer in ['hull', 'barrel']:
    tree = ET.parse(source)
    root = tree.getroot()
    for node in list(root):
        if node.tag.endswith('g') and node.get('id') != layer:
            root.remove(node)
    target = ASSET / (layer + '.svg')
    tree.write(target, encoding='unicode', xml_declaration=True)
    target.write_text('\n'.join(line.rstrip() for line in target.read_text().splitlines()) + '\n')
print('Exported hull.svg and barrel.svg from editable guardian-source.svg')
