import json
from pathlib import Path
base=Path(__file__).resolve().parent;d=json.load(open(base/'arena.json'));p=d['jump_order'];els=[]
els.append('<svg xmlns="http://www.w3.org/2000/svg" width="768" height="880" viewBox="0 0 768 880"><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0 0 L8 3 L0 6Z" fill="#b08a46"/></marker></defs><rect width="768" height="880" fill="#eef0e4"/><text x="24" y="32" font-family="sans-serif" font-size="20" fill="#24392c">PROPOSAL · 768×768 arena · coordinates are ground anchors</text><g transform="translate(0 56)"><rect x="1" y="1" width="766" height="766" fill="#53604a" stroke="#243b30"/>')
for x in range(64,768,64):els.append(f'<path d="M{x} 0 V768 M0 {x} H768" stroke="#829072" stroke-opacity=".16"/>')
for i,a in enumerate(p):
 b=p[(i+1)%5];els.append(f'<path d="M{a["x"]} {a["y"]} L{b["x"]} {b["y"]}" stroke="#d6b46d" stroke-width="3" fill="none" marker-end="url(#arrow)"/>')
for i,a in enumerate(p):
 x,y=a['x'],a['y'];els.append(f'<ellipse cx="{x}" cy="{y}" rx="112" ry="64" fill="#a5b78b" fill-opacity=".2" stroke="#e6d8ab" stroke-width="2"/><circle cx="{x}" cy="{y}" r="5" fill="#fff0bf"/><text x="{x}" y="{y-78}" text-anchor="middle" fill="#fff2c7" font-family="sans-serif" font-size="18">{i+1} {a["id"]} ({x},{y})</text>')
els.append('<path d="M64 704 H560 M560 704 V456 M208 704 V456" stroke="#b9d5ce" stroke-width="2" stroke-dasharray="7 7" fill="none"/>')
for x in [208,560]:els.append(f'<circle cx="{x}" cy="704" r="8" fill="#b9d5ce"/><text x="{x}" y="738" text-anchor="middle" font-family="sans-serif" fill="#e8f3e8" font-size="16">south firing station</text>')
els.append('<rect x="37" y="658" width="57.5" height="93" fill="#d2ae6a" stroke="#243b30"/><text x="28" y="638" font-family="sans-serif" fill="#fff0bc" font-size="16">spawn (64,704), ↑</text></g><text x="24" y="850" font-family="sans-serif" font-size="15" fill="#243b30">No walls. Pale ellipses = proposed contact footprints, not extra shockwave attacks.</text></svg>')
(base/'arena.svg').write_text(''.join(els))
