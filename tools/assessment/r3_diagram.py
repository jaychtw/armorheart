"""Generate a coordinate schematic, not game artwork or a gameplay screenshot."""
from pathlib import Path
import json,os
os.environ.setdefault("MPLCONFIGDIR","/tmp/armorheart-matplotlib")
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['svg.hashsalt']='armorheart-r3-geometry'
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Polygon
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'docs/geometry/r3';s=json.loads((P/'map.json').read_text());report=json.loads((P/'transport-results.json').read_text())
fig,axs=plt.subplots(1,2,figsize=(10,11),layout='constrained')
for ax,(name,mask,title) in zip(axs,[('lowerDemolition',12,'2 cells: C + D · bypass'),('shortcut',14,'3 cells: B + C + D · shortcut')]):
 ax.set_facecolor('#e7ece1');ax.set_xlim(176,592);ax.set_ylim(784,-16);ax.set_aspect('equal');ax.set_xticks(range(192,577,64));ax.set_yticks(range(0,769,64));ax.grid(color='#cad1c2',linewidth=.5);ax.set_axisbelow(True)
 ax.add_patch(Rectangle((192,0),384,768,fill=False,edgecolor='#273a31',linewidth=2))
 for w in s['steel']:
  ax.add_patch(Rectangle((w['x'],w['y']),64,64,facecolor='#53685a',edgecolor='#20392a',linewidth=1))
 for w in s['brick']:
  gone=bool(mask>>w['id']&1)
  ax.add_patch(Rectangle((w['x'],w['y']),64,64,facecolor='#f4eedb' if gone else '#c3a16a',edgecolor='#80623b',linewidth=1,linestyle='--' if gone else '-'))
  ax.text(w['x']+32,w['y']+32,w['label']+(' ×' if gone else ''),ha='center',va='center',fontsize=11,color='#6b4b23')
 e=s['exit'];ax.add_patch(Rectangle((e['left'],e['top']),e['right']-e['left'],e['bottom']-e['top'],facecolor='#c7dfd3',edgecolor='#21644c',linewidth=1.5,alpha=.6));ax.text(400,55,'EXIT\n96 × 192',ha='center',fontsize=10,color='#15563d')
 r=report['all_destruction_states'][mask];poses=r['poses'];xy=[]
 for x,y,h in poses:
  if not xy or xy[-1]!=(x,y):xy.append((x,y))
 ax.plot([p[0] for p in xy],[p[1] for p in xy],color='#a34829' if mask==12 else '#1a5881',linewidth=2.2,zorder=4)
 for a,b in zip(poses,poses[1:]):
  if a[2]!=b[2]:ax.plot(a[0],a[1],'o',color='#823a22' if mask==12 else '#1a5881',markersize=5)
 t=s['truckSpawn'];ax.add_patch(Rectangle((t['x']-28,t['y']-64),56,128,facecolor='#8f9c77',edgecolor='#243a2c',linewidth=1.5,zorder=5));ax.text(t['x'],t['y']+5,'T',ha='center',fontsize=11,color='#fff',zorder=6)
 q=s['tankSpawn'];ax.plot(q['x'],q['y'],'^',markersize=9,color='#ba853c',markeredgecolor='#513a19',zorder=7)
 ax.set_title(title+'\n'+f'{r["distance"]} units · {r["quarter_turns"]} turns · {r["seconds"]:.2f}s transport only',fontsize=11)
 ax.set_xlabel('world x');ax.set_ylabel('world y')
fig.suptitle('R3 geometry assessment — fixed 768-square world / 384-wide active strip\nDashed cells removed; dots = certified truck pivots; T = 128×56 truck envelope; triangle = Guardian spawn\nPlanning schematic only. Guardian mechanics and runtime map unchanged.',fontsize=12)
fig.savefig(P/'map-diagram.svg',metadata={'Date':None});fig.savefig(P/'map-diagram.png',dpi=140);plt.close(fig)

svg=P/'map-diagram.svg'
svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
