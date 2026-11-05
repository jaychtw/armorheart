"""Export editable composition with its original raster embedded; no redrawing."""
from pathlib import Path
import argparse,base64
HERE=Path(__file__).resolve().parent;p=argparse.ArgumentParser();p.add_argument('output',type=Path);a=p.parse_args()
s=(HERE/'colossus-editable.svg').read_text();s=s.replace('href="colossus-concept.png"','href="data:image/png;base64,'+base64.b64encode((HERE/'colossus-concept.png').read_bytes()).decode()+'"');a.output.write_text(s);print(a.output)
