"""Technical planning diagram; no gameplay asset or renderer modification."""
import json,os
os.environ.setdefault("MPLCONFIGDIR","/tmp/armorheart-r3-mplconfig")
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle
from matplotlib.lines import Line2D
H=Path(__file__).resolve().parent;M=json.loads((H/'map.json').read_text());results=json.loads((H/'transport-results.json').read_text())['states']
fig,axes=plt.subplots(1,2,figsize=(10,11));fig.patch.set_facecolor('#f4f2e9')
for ax,mask,title in zip(axes,[3,15],['LONG BYPASS · 2 CELLS','SHORTCUT · 4 CELLS']):
 row=next(r for r in results if r['mask']==mask);removed=set(row['removed'])
 ax.set_facecolor('#e4e8df');ax.set_xlim(176,592);ax.set_ylim(784,-16);ax.set_aspect('equal')
 ax.axvline(192,color='#233c33',linewidth=4);ax.axvline(576,color='#233c33',linewidth=4)
 ex=M['exit'];ax.add_patch(Rectangle((ex['left'],ex['top']),ex['right']-ex['left'],ex['bottom']-ex['top'],facecolor='#cae3d0',alpha=.75,edgecolor='#325e45',linewidth=1))
 ax.text(384,42,'REFUGE',ha='center',va='center',fontsize=10,fontweight='bold',color='#234332')
 for w in M['walls']:
  gone=w['id'] in removed;steel=w['kind']=='steel';color='#485e55' if steel else '#bc9563'
  ax.add_patch(Rectangle((w['x'],w['y']),64,64,facecolor='none' if gone else color,edgecolor='#a65f27' if gone else '#253b31',linewidth=1.3,linestyle='--' if gone else '-'))
  ax.text(w['x']+32,w['y']+32,w['id']+(' ×' if gone else ''),ha='center',va='center',fontsize=8,color='#26382f' if gone else 'white')
 states=row['route_states'];ax.plot([s[0] for s in states],[s[1] for s in states],color='#12674e',linewidth=2.8,zorder=4)
 for a,b,action in zip(states,states[1:],row['actions']):
  if action!='forward':
   ax.add_patch(Circle((a[0],a[1]),76,fill=False,edgecolor='#12674e',linestyle=':',alpha=.35,linewidth=.9))
   ax.plot(a[0],a[1],'o',color='#12674e',markersize=4)
 tx,ty=M['truck']['x'],M['truck']['y'];ax.add_patch(Rectangle((tx-64,ty-28),128,56,fill=False,edgecolor='#1d4136',linewidth=2,zorder=6));ax.text(tx,ty,'TRUCK →',ha='center',va='center',fontsize=7,fontweight='bold')
 x,y=M['tank']['x'],M['tank']['y'];ax.add_patch(Rectangle((x-29,y-45.5),57.5,93,fill=False,edgecolor='#3559a0',linewidth=2));ax.text(x,y,'T',ha='center',va='center',color='#3559a0',fontweight='bold')
 ax.set_xticks([192,288,384,480,576]);ax.set_yticks(range(0,769,64));ax.tick_params(labelsize=8)
 ax.set_title(title+'\n'+f"{row['travel_units']} units · {row['quarter_turns']} pivots · {row['predicted_seconds']:.2f}s",fontsize=11,pad=15)
 ax.set_xlabel('World x');ax.set_ylabel('World y (south ↓)')
fig.suptitle('R3 VERIFIED GEOMETRY CANDIDATE — 384 × 768 corridor',fontsize=14,fontweight='bold',y=.98)
fig.text(.5,.045,'Dashed cells: individually destroyed · Green dots/circles: stop-pivots / conservative 76-unit swept disc\nTruck body 128 × 56, navigation margin 4 · T: Guardian spawn · Planning diagram, not game art or a browser capture',ha='center',fontsize=9)
fig.subplots_adjust(top=.90,bottom=.12,wspace=.28)
fig.savefig(H/'map.png',dpi=160,facecolor=fig.get_facecolor());fig.savefig(H/'map.svg',facecolor=fig.get_facecolor());plt.close(fig)

svg=H/'map.svg';svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
