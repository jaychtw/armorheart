from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'planning/siege-m4/map.json').read_text())
(ROOT/'src/maps/siege.mjs').write_text('// Exact owner-approved Siege Offer data; reproduced by tools/export_m4_map.py.\nexport const SIEGE = '+json.dumps(data,indent=2,ensure_ascii=False)+';\n')
