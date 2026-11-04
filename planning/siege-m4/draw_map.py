"""Data-derived engineering diagram, distinct from the original art study."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent;C=json.loads((P/'map.json').read_text())
a=['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="990" viewBox="0 0 900 990"><rect width="900" height="990" fill="#f2f0e8"/><style>text{font-family:system-ui;fill:#26382f}.small{font-size:13px}.label{font-size:18px;font-weight:600}</style><defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10" fill="none" stroke="#e8d37b" stroke-width="2"/></marker></defs><text x="56" y="38" class="label">Siege M4 — proposed geometry / not implemented</text><text x="56" y="65" class="small">All coordinates in world units. 64-unit cells; Guardian hull unchanged.</text><g transform="translate(66 110)"><rect width="768" height="768" fill="#56634d"/>']
for v in range(0,769,64):
 a += [f'<path d="M{v} 0V768M0 {v}H768" stroke="#c3c9aa" opacity=".15"/>',f'<text x="{v}" y="-12" text-anchor="middle" class="small">{v}</text>',f'<text x="-10" y="{v+4}" text-anchor="end" class="small">{v}</text>']
for w in C['walls']:
 color='#b69a69' if w['kind']=='brick' else '#34483b'
 a += [f'<rect x="{w["x"]}" y="{w["y"]}" width="{w["width"]}" height="{w["height"]}" fill="{color}" stroke="#a9b095"/>']
 if w['id']<20:a += [f'<text x="{w["x"]+w["width"]/2}" y="{w["y"]+38}" text-anchor="middle" style="fill:#fff;font:16px system-ui">{("B" if w["kind"]=="brick" else "S")+str(w["id"])}</text>']
f=C['fortress'];a += [f'<rect x="256" y="64" width="256" height="160" fill="#b49b70" stroke="#f1dd9d" stroke-width="3"/><text x="384" y="136" text-anchor="middle" class="label">FORTRESS · 8 HP</text><text x="384" y="164" text-anchor="middle" class="small">(256,64), 256×160</text>']
for x,y in f['gunPivots']:a += [f'<circle cx="{x}" cy="{y}" r="7" fill="#edce80" stroke="#243c2e"/><path d="M{x} {y}v24" stroke="#edce80" stroke-width="4"/>']
for name in ['leftBypass','rightBypass']:
 points=' '.join(','.join(map(str,p)) for p in C['routes'][name]);a += [f'<polyline points="{points}" fill="none" stroke="#e8d37b" stroke-width="3" stroke-dasharray="8 5" marker-end="url(#arrow)"/>']
a += ['<circle cx="384" cy="688" r="13" fill="#e8ce91" stroke="#20392c" stroke-width="3"/><text x="384" y="731" text-anchor="middle" style="fill:#fff;font:16px system-ui">Spawn (384,688)</text><text x="600" y="485" style="fill:#f5f0d2;font:16px system-ui">128 clear</text></g><text x="66" y="926" class="small">B0–B3: one-shot destructible, player or enemy. S10/S11 and northern rock: permanent.</text><text x="66" y="951" class="small">Both bypasses verified in all 16 brick-removal states; central steel shelters cannot fire through.</text></svg>']
(P/'evidence/map.svg').write_text('\n'.join(a)+'\n')
