"""Assemble original editable vector ship components over preserved raster paint.
No reference-sheet pixels are used. Selected source PNG is never re-encoded.
"""
from pathlib import Path
from PIL import Image
import base64,hashlib,json
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
source=HERE/'source/hull-underpainting.png';im=Image.open(source);alpha=im.getchannel('A');box=alpha.point(lambda v:255 if v>=16 else 0).getbbox();x0,y0,x1,y1=box
turret=HERE/'source/turret-house.png';ti=Image.open(turret);tb=ti.getchannel('A').point(lambda v:255 if v>=16 else 0).getbbox();tx0,ty0,tx1,ty1=tb;tdata=base64.b64encode(turret.read_bytes()).decode()
config=json.loads((HERE.parent/'map.json').read_text());points=config['ship']['hullPolygon'];path='M'+' '.join(f'{x},{y}' for x,y in points)+'Z';data=base64.b64encode(source.read_bytes()).decode()
# Registration is an explicit editable SVG transform, not a replacement master.
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="664" height="260" viewBox="-166 -54 332 130">
<title>Armorheart Interception — original editable battleship study A</title><desc>Bow +X; starboard +Y. Accepted320×88 hull polygon,3 single heavy main bores at localX−88,0,+88 and muzzleY66. Mixed raster/vector art, not a vector-redrawn deck. No reference pixels. Pending creative review; no Stage3 integration.</desc>
<defs>
 <clipPath id="hull-clip"><path d="{path}"/></clipPath>
 <linearGradient id="hull-metal" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#69715e"/><stop offset=".35" stop-color="#8a8d72"/><stop offset=".6" stop-color="#4f5a4c"/><stop offset="1" stop-color="#293e38"/></linearGradient>
 <linearGradient id="turret-top" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#c6b27d"/><stop offset=".48" stop-color="#8f9272"/><stop offset="1" stop-color="#606e59"/></linearGradient>
 <linearGradient id="barrel-metal"><stop stop-color="#343f36"/><stop offset=".32" stop-color="#a3a080"/><stop offset=".53" stop-color="#c5bc98"/><stop offset="1" stop-color="#554f3e"/></linearGradient>
 <g id="primary-bore-component">

   <path d="M-5,12H5V37L3.5,45V66H-3.5V45L-5,37Z" fill="url(#barrel-metal)" stroke="#2b3d2e" stroke-width=".9"/>
   <path d="M-2.8,15V35L-1.7,44V63" fill="none" stroke="#ddd5aa" stroke-width="1" opacity=".85"/>
   <path d="M-4.7,28H4.7M-4.7,31H4.7M-3.5,48H3.5M-3.5,52H3.5" stroke="#495c43" stroke-width=".8"/>
   <rect x="-4.3" y="59" width="8.6" height="6" rx=".9" fill="#697858" stroke="#cad1a4" stroke-width=".6"/>
   <path d="M-3.3,65H3.3" stroke="#172b20" stroke-width="2"/>
   <path d="M-2.4,64.3H2.4" stroke="#b4bf91" stroke-width=".6"/>
 </g>
 <g id="battery-component">
  <ellipse cy="1" rx="25" ry="20" fill="#263a2e" stroke="#9d9b75" stroke-width=".8"/>
  <use href="#primary-bore-component"/>
  <svg x="-22" y="-18" width="44" height="38" viewBox="{tx0} {ty0} {tx1-tx0} {ty1-ty0}" preserveAspectRatio="none" overflow="hidden"><image id="painted-turret-house" width="{ti.width}" height="{ti.height}" href="data:image/png;base64,{tdata}"/></svg>
 </g>
</defs>
<g id="hull-silhouette" inkscape:groupmode="layer" inkscape:label="Hull silhouette"><path d="{path}" fill="url(#hull-metal)"/></g>
<g inkscape:groupmode="layer" inkscape:label="Painted deck and superstructure" id="deck-and-superstructure" clip-path="url(#hull-clip)">
 <svg x="-158" y="-41" width="316" height="82" viewBox="{x0} {y0} {x1-x0} {y1-y0}" preserveAspectRatio="none" overflow="hidden"><image id="original-painted-underlay" width="{im.width}" height="{im.height}" href="data:image/png;base64,{data}"/></svg>
</g>
<g inkscape:groupmode="layer" inkscape:label="Hull edge" id="hull-edge" clip-path="url(#hull-clip)"><path d="{path}" fill="none" stroke="#25382f" stroke-width="2.2"/><path d="M-148,-23 -118,-40 122,-30 152,-1" fill="none" stroke="#c5ba8d" stroke-width=".9" opacity=".75"/><path d="M-148,24 -118,41 122,31 151,2" fill="none" stroke="#1d332a" stroke-width="1.1" opacity=".8"/></g>
<g id="main-batteries-fixed-starboard" inkscape:groupmode="layer" inkscape:label="Three fixed starboard batteries">
 <use id="aft-battery" href="#battery-component" transform="translate(-88 0)"/>
 <use id="mid-battery" href="#battery-component"/>
 <use id="forward-battery" href="#battery-component" transform="translate(88 0)"/>
</g>
<g inkscape:groupmode="layer" inkscape:label="Hidden registration guide" id="muzzle-registration" display="none" fill="none" stroke="#ffbe5e"><circle cx="-88" cy="66" r="2"/><circle cy="66" r="2"/><circle cx="88" cy="66" r="2"/></g>
</svg>'''
(HERE/'battleship-editable.svg').write_text(svg)
metadata={'status':'One original editable visual assessment; pending creative review, not Stage3 production integration','source_png':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_dimensions':list(im.size),'turret_source_png':str(turret.relative_to(ROOT)),'turret_source_sha256':hashlib.sha256(turret.read_bytes()).hexdigest(),'turret_source_dimensions':list(ti.size),'turret_alpha16_box':list(tb),'alpha16_registration_box':list(box),'registration':{'destination_deck_rect':[-158,-41,316,82],'aspect':'explicit nonuniform underpainting registration inside exact hull; original PNG untouched'},'body_polygon':points,'body_dimensions':[320,88],'muzzles':[{'mount':[x,0],'mouth':[x,66],'local_direction':[0,1]} for x in config['ship']['turretStations']],'barrel_render':'one visible heavy bore per battery, one-to-one with approved3-shell volley','svg_sha256':hashlib.sha256(svg.encode()).hexdigest(),'reference_pixels_in_asset':False,'editable_layers':['hull-silhouette','deck-and-superstructure (preserved raster)','hull-edge','main-batteries-fixed-starboard','battery-component/painted-turret-house (preserved raster)','primary-bore-component (vector; beneath turret)','muzzle-registration (hidden diagnostic)'],'limitation':'painted deck and turret houses are raster, not separated original architecture layers or fully vector; original poster binary not exposed'}
(HERE/'sample.json').write_text(json.dumps(metadata,indent=2)+'\n');print('Built original editable sample:',len(svg),'bytes; source',im.size,'registration',box)
