"""Original editable vector direction study; not a production asset export."""
from pathlib import Path
P=Path(__file__).resolve().parent
parts=['''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="184" viewBox="0 0 256 184" role="img" aria-label="Proposed Armorheart fortress, three preliminary damage silhouettes">
<defs>
 <linearGradient id="stone" x2=".25" y2="1"><stop stop-color="#c2a575"/><stop offset=".5" stop-color="#a78c60"/><stop offset="1" stop-color="#776247"/></linearGradient>
 <linearGradient id="roof" x2=".5" y2="1"><stop stop-color="#8a8b6d"/><stop offset="1" stop-color="#4c5949"/></linearGradient>
 <linearGradient id="metal" x2="1" y2="0"><stop stop-color="#26382e"/><stop offset=".5" stop-color="#829079"/><stop offset="1" stop-color="#34453a"/></linearGradient>
 <pattern id="blocks" width="32" height="16" patternUnits="userSpaceOnUse"><path d="M0 16H32M16 0V16" stroke="#66543d" stroke-width="1.1" opacity=".6"/></pattern>
</defs>''']
for stage in ['intact','broken','half']:
 half=stage=='half';broken=stage!='intact'
 a=[f'<g id="{stage}" style="display:{"inline" if stage=="intact" else "none"}">']
 # All states retain an explicit opaque full-size foundation/physical footprint.
 a+=['<rect width="256" height="160" fill="#4b4636"/>','<path d="M0 10L10 0H246L256 10V150L246 160H10L0 150Z" fill="#4b4636"/>',
 '<path d="M3 12L12 3H244L253 12V147L244 156H12L3 147Z" fill="url(#stone)" stroke="#c9ae7c" stroke-width="2"/>',
 '<path d="M5 143H251V151L243 158H13L5 151Z" fill="#62513a"/>',
 '<path d="M13 146H243" stroke="#d7bc84" stroke-width="2"/>',
 '<path d="M65 42H191V134H65Z" fill="#736b50" stroke="#564b37" stroke-width="3"/>',
 '<path d="M70 47H186V126H70Z" fill="url(#roof)"/>']
 if not half:
  a+=['<path d="M81 17L96 4H160L175 17V108L163 120H93L81 108Z" fill="#5c503c" stroke="#3c4134" stroke-width="2"/>',
  '<path d="M85 16L98 8H158L171 16V97L159 106H97L85 97Z" fill="url(#stone)" stroke="#dfc18a" stroke-width="2"/>',
  '<path d="M97 21H159V92H97Z" fill="url(#roof)" stroke="#5a624c" stroke-width="3"/>',
  '<path d="M108 34H148V77H108Z" fill="#343f34" stroke="#b9a179" stroke-width="2"/>',
  '<path d="M114 38H142M114 47H142M114 56H142M114 65H142" stroke="#6b7861" stroke-width="3"/>',
  '<path d="M92 108H164V119H92Z" fill="url(#blocks)"/>']
 else:
  a+=['<path d="M82 96L87 44L107 56L113 31L135 40L141 61L163 49L174 96L164 117H92Z" fill="#685b43" stroke="#403f31" stroke-width="3"/>',
  '<path d="M97 72L112 56L124 76L141 70L154 90L148 107H108Z" fill="#2f3931"/>',
  '<path d="M90 102L106 95L116 108L135 97L154 103L164 116H94Z" fill="#a48c61" stroke="#554c39" stroke-width="2"/>']
 for x in [9,195]:
  damaged=broken and (x==9 or half)
  if not damaged:
   a += [f'<path d="M{x} 37L{x+11} 25H{x+41}L{x+52} 37V110L{x+42} 121H{x+10}L{x} 110Z" fill="url(#stone)" stroke="#e0c18b" stroke-width="2"/>',
    f'<path d="M{x+9} 40L{x+17} 32H{x+35}L{x+44} 40V100L{x+36} 109H{x+17}L{x+9} 100Z" fill="url(#roof)" stroke="#554d38" stroke-width="3"/>',
    f'<path d="M{x+17} 54H{x+36}V84H{x+17}Z" fill="#344337" stroke="#919477" stroke-width="2"/>',
    f'<path d="M{x+14} 30V20H{x+23}V27H{x+31}V20H{x+40}V32" fill="#bda272" stroke="#65553c" stroke-width="2"/>']
  else:
   a += [f'<path d="M{x} 74L{x+10} 45L{x+21} 57L{x+29} 39L{x+36} 74L{x+48} 61L{x+52} 109L{x+41} 121H{x+9}Z" fill="#948060" stroke="#544936" stroke-width="2"/>',
    f'<path d="M{x+10} 85L{x+20} 71L{x+39} 90L{x+43} 109H{x+13}Z" fill="#3b4233"/>',
    f'<path d="M{x+5} 114L{x+16} 104L{x+29} 115L{x+37} 103L{x+50} 117" fill="#be9e6f" stroke="#69563e" stroke-width="3"/>']
 a+=['<path d="M8 128H248V144H8Z" fill="url(#stone)" stroke="#5e513a" stroke-width="2"/>',
 '<path d="M8 129H248M19 132V141M67 132V141M115 132V141M163 132V141M211 132V141" stroke="#d4b783" stroke-width="2"/>']
 if broken:a+=['<path d="M171 39L159 55L165 71L153 88M66 91L72 109L60 124" stroke="#383e31" stroke-width="3" fill="none"/>']
 # Three casemate positions remain registered/readable in every damage state.
 for x in [32,128,224]:
  a += [f'<path d="M{x-20} 142L{x-14} 132H{x+14}L{x+20} 142V157H{x-20}Z" fill="#39473a" stroke="#adb092" stroke-width="2"/>',
   f'<circle cx="{x}" cy="152" r="12" fill="#58634e" stroke="#252f28" stroke-width="2"/>',
   f'<path d="M{x-4} 149H{x+4}V176H{x-4}Z" fill="url(#metal)" stroke="#293a2e" stroke-width="1.5"/>',
   f'<path d="M{x-5} 173H{x+5}V176H{x-5}Z" fill="#222e25"/>',
   f'<circle cx="{x-13}" cy="142" r="1.5" fill="#d8c18b"/><circle cx="{x+13}" cy="142" r="1.5" fill="#d8c18b"/>']
 a+=['</g>'];parts+=a
parts+=['</svg>'];(P/'fortress-study.svg').write_text('\n'.join(parts)+'\n')
print('Original editable fortress direction study built; preliminary, not production accepted')
