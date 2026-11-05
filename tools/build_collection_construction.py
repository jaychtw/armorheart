"""Original cosmetic tanks, authored geometry/materials; never changes accepted Guardian bytes."""
from pathlib import Path
import random,json,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/tanks/construction'
SPECS={
 'bulwark':{'base':'#777b54','light':'#b8bd82','dark':'#3c4834','track':'#343b2f','outer':'M12 80L22 70H188L198 80V101L188 108H22L12 100ZM12 155L22 147H188L198 156V176L188 185H22L12 176ZM24 103H178L198 116V143L178 154H24Z','hull':'M24 103H178L198 116V143L178 154H24Z','roof':'M58 96H142L177 109V145L142 157H58L45 143V111Z'},
 'vanguard':{'base':'#b1a27a','light':'#e4d4a5','dark':'#655a42','track':'#514b39','outer':'M12 82L36 70H177L198 84L187 104H35L12 96ZM12 158L35 150H187L198 172L177 185H36L12 174ZM22 107L145 97L198 126L145 158L22 147Z','hull':'M22 107L145 97L198 126L145 158L22 147Z','roof':'M58 109L121 99L174 126L121 154L58 145L46 126Z'},
 'sentinel':{'base':'#70817b','light':'#bac5ad','dark':'#344b45','track':'#303d37','outer':'M12 84Q12 70 27 70H75L92 81H129L143 73H184Q198 73 198 87V101L183 108H28L12 99ZM12 158L28 149H183L198 156V171Q198 185 183 185H143L129 177H92L75 185H27Q12 185 12 171ZM24 100H173L194 115V141L173 157H24Z','hull':'M24 100H173L194 115V141L173 157H24Z','roof':'M71 99Q105 85 138 101L162 116V139L138 154Q104 167 71 153L58 138V116Z'},
}
for n,(name,s) in enumerate(SPECS.items()):
 d=OUT/name;d.mkdir(parents=True,exist_ok=True);rng=random.Random(120+n)
 defs=f'''<defs><linearGradient id="plate" x2=".4" y2="1"><stop stop-color="{s['light']}"/><stop offset=".35" stop-color="{s['base']}"/><stop offset="1" stop-color="{s['dark']}"/></linearGradient><linearGradient id="steel" x2="0" y2="1"><stop stop-color="#bbc1a1"/><stop offset=".35" stop-color="#687968"/><stop offset=".7" stop-color="#87937a"/><stop offset="1" stop-color="#283b30"/></linearGradient><clipPath id="silhouette"><path d="{s['outer']}"/></clipPath><clipPath id="physical"><rect x="12" y="70" width="186" height="115"/></clipPath><pattern id="wear" width="48" height="48" patternUnits="userSpaceOnUse">'''
 for i in range(100):
  x,y=rng.randrange(48),rng.randrange(48);defs+=f'<path d="M{x} {y}h{rng.choice([1,1.5,2])}" stroke="{rng.choice([s["light"],s["dark"],"#dbcf9d"])}" stroke-width=".7" opacity=".38"/>'
 defs+='</pattern></defs>'
 body=f'<g id="hull" clip-path="url(#physical)"><path d="{s["outer"]}" fill="{s["track"]}" stroke="{s["dark"]}" stroke-width="2"/><g clip-path="url(#silhouette)">'
 # Individual broad tread plates retain visual direction and ground contact.
 for y in [73,156]:
  for x in range(20,193,13):
   body+=f'<path d="M{x} {y}h8v25h-8Z" fill="{s["track"]}" stroke="#899079" stroke-width="1.1"/><path d="M{x+1} {y+5}h6M{x+1} {y+20}h6" stroke="#242f27" stroke-width="2"/>'
 body+=f'<path d="{s["hull"]}" fill="url(#plate)" stroke="{s["light"]}" stroke-width="2"/><path d="{s["roof"]}" fill="{s["dark"]}" stroke="#24382b" stroke-width="3"/>'
 if name=='bulwark':
  body+=f'<path d="M59 101H139L168 112V142L139 152H59L51 139V114Z" fill="url(#plate)" stroke="{s["light"]}" stroke-width="2"/><path d="M63 110H103V143H63Z" fill="{s["dark"]}" stroke="#b4b38a" stroke-width="2"/><path d="M109 106H137L153 116V139L137 147H109Z" fill="{s["base"]}" stroke="#d1c89b" stroke-width="1.5"/><path d="M159 111H191L198 117V138L191 145H159Z" fill="url(#plate)" stroke="{s["dark"]}" stroke-width="2"/>'
  for x in [29,39]:body+=f'<path d="M{x} 111v31" stroke="#343d2e" stroke-width="3"/>'
  body+='<path d="M74 117H94M74 124H94M74 131H94M74 138H94" stroke="#8c9776" stroke-width="2"/>'
 elif name=='vanguard':
  body+=f'<path d="M59 113L119 104L166 126L119 149L59 141L51 126Z" fill="url(#plate)" stroke="{s["light"]}" stroke-width="2"/><path d="M107 109L151 126L107 145L93 133V121Z" fill="{s["dark"]}" stroke="#dad0aa" stroke-width="1.5"/><path d="M164 115L193 123L198 126L193 131L164 139Z" fill="url(#plate)" stroke="{s["dark"]}" stroke-width="2"/><path d="M28 114H44V139H28Z" fill="#5a5140" stroke="#decda0" stroke-width="1.5"/>'
  body+='<path d="M33 117V136M39 117V136M70 116L89 114M70 135L89 138" stroke="#b9aa85" stroke-width="2"/>'
 else:
  body+=f'<ellipse cx="108" cy="128" rx="47" ry="33" fill="url(#plate)" stroke="{s["light"]}" stroke-width="2"/><ellipse cx="108" cy="126" rx="34" ry="24" fill="{s["base"]}" stroke="{s["dark"]}" stroke-width="3"/><ellipse cx="107" cy="121" rx="16" ry="11" fill="{s["dark"]}" stroke="#c4c9ae" stroke-width="2"/><path d="M153 114H190L198 119V134L190 140H153Z" fill="url(#plate)" stroke="{s["dark"]}" stroke-width="2"/><path d="M26 108H51V149H26Z" fill="{s["dark"]}" stroke="{s["light"]}" stroke-width="1.5"/>'
  body+='<path d="M32 113H45M32 120H45M32 127H45M32 134H45M32 141H45" stroke="#8c9c83" stroke-width="2"/><path d="M72 116Q68 130 78 140" fill="none" stroke="#d2cfaa" stroke-width="2"/>'
 for x,y in [(54,107),(54,147),(140,110),(140,145),(179,113),(179,141)]:body+=f'<circle cx="{x}" cy="{y}" r="1.7" fill="{s["light"]}" stroke="{s["dark"]}" stroke-width=".7"/>'
 body+='<rect x="12" y="70" width="186" height="115" fill="url(#wear)"/></g></g>'
 # Each original gun has the exact accepted axis126, tip243 and moving mount.
 if name=='bulwark':barrel='<path d="M158 121H234V118H243V134H234V131H158Z" fill="url(#steel)" stroke="#2d3c2f" stroke-width="1.4"/><path d="M238 120V132M241 121V131" stroke="#202e25" stroke-width="1.5"/>'
 elif name=='vanguard':barrel='<path d="M158 122L229 123L233 120H243V132H233L229 129L158 130Z" fill="url(#steel)" stroke="#384335" stroke-width="1.3"/><path d="M241 121V131M205 123V129" stroke="#252f26" stroke-width="1.5"/>'
 else:barrel='<path d="M158 121H243V131H158Z" fill="url(#steel)" stroke="#26392f" stroke-width="1.3"/><path d="M208 119H215V133H208ZM235 120H243V132H235Z" fill="url(#steel)" stroke="#26382d" stroke-width="1.3"/><path d="M241 121V131" stroke="#182c22" stroke-width="1.5"/>'
 barrel='<g id="barrel">'+barrel+'</g>'
 start='<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">'
 (d/'source.svg').write_text(start+defs+barrel+body+'</svg>\n')
 (d/'hull.svg').write_text(start+defs+body+'</svg>\n');(d/'barrel.svg').write_text(start+defs+barrel+'</svg>\n')
manifest={'status':'Original game-ready cosmetic candidates for integrated v1 creative review','source':'Original authored vector geometry/materials; no alternate prototype bytes available in checkout','toolchain':'Python stdlib original SVG construction; native Canvas rendering/validation','physics':'All tanks use unmodified Guardian engine; hull master12,70,198,185; pivot107,128; muzzle243,126; scale0.5; identical recoil/cadence','tanks':{}}
for name in SPECS:
 manifest['tanks'][name]={'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((OUT/name).glob('*.svg'))},'palette':SPECS[name]['base'],'design':{'bulwark':'stepped armored shoulders and broad slab casemate','vanguard':'tapered prow and low angular arrowhead turret','sentinel':'separated track pods and round sensor turret'}[name]}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Three original independent cosmetic tank constructions exported; Guardian unchanged')
