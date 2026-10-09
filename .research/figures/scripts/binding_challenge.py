"""Mechanism diagram: source-defined role swaps, not measured model predictions."""
from pathlib import Path
import json,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
ROOT=Path(__file__).resolve().parents[3]
source=ROOT/'data/supplementary/reviewer_binding.jsonl'
rows=[json.loads(l) for l in source.read_text().splitlines()]
case=[r for r in rows if r['family_id']=='RB01' and r['status_pair']==['idle','open'] and r['knowledge']=='real']
assert len(case)==4
for swap,labels in [(0,['contradicted','contradicted']),(1,['unknown','entailed'])]:
 assert [next(r['gold'] for r in case if r['swap']==swap and r['composition']==c) for c in ['bounded','unbounded']]==labels
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':7,'svg.fonttype':'none','pdf.fonttype':42})
fig,ax=plt.subplots(figsize=(8.5/2.54,7.0/2.54));fig.subplots_adjust(0,0,1,1)
ax.set(xlim=(0,10),ylim=(0,8));ax.axis('off')
blue='#2563EB';orange='#BD5A16';gray='#455166'
ax.text(.15,7.8,'Words stay fixed; actor bindings change',fontsize=8.1,weight='bold',va='top',color='#172D4B')
def scene(top,swap,title):
 ax.text(.15,top,title,weight='bold',fontsize=7.4,color='#172D4B',va='center')
 ys=[top-.75,top-1.77]
 for x,y,col,name in [(.85,ys[0],blue,'Nora'),(.85,ys[1],orange,'Alex')]:
  ax.add_patch(FancyBboxPatch((.15,y-.23),1.45,.46,boxstyle='round,pad=.02,rounding_size=.11',facecolor='#FFFFFF',edgecolor=col,lw=1.1))
  ax.text(x,y,name,ha='center',va='center',color=col,weight='bold',fontsize=7.6)
 for i,(y,first,second) in enumerate(zip(ys,['Zero coverage','¼ → ½ coverage'],['throughout the interval','observed by minute 3'])):
  ax.add_patch(FancyBboxPatch((4.05,y-.37),5.7,.74,boxstyle='round,pad=.025,rounding_size=.11',facecolor='#F3F6FA',edgecolor='#CBD4DF',lw=.7))
  ax.text(4.3,y+.10,first,va='center',fontsize=7.5,weight='bold',color=gray)
  ax.text(4.3,y-.16,second,va='center',fontsize=6.9,color=gray)
 for actor_idx,col,style in [(0,blue,'-'),(1,orange,(0,(3,2)))]:
  record_idx=actor_idx if not swap else 1-actor_idx
  ax.plot([1.7,3.92],[ys[actor_idx],ys[record_idx]],color=col,lw=1.5,ls=style,zorder=3)
 ax.text(.15,top-2.52,'Same Nora targets:',color=gray,va='center',fontsize=7)
 ax.text(4.15,top-2.52,'B = C     A = C' if not swap else 'B = U     A = E',color=blue,weight='bold',va='center',fontsize=8.2)
scene(7.08,0,'(a) Original assignment')
ax.plot([.15,9.8],[4.20,4.20],color='#D4DBE5',lw=.7)
scene(3.85,1,'(b) Swapped assignment')
ax.text(.15,.55,'B: all the water     A: some water',fontsize=7,color=gray,va='center')
ax.text(.15,.12,'Identical word counts  •  Different reference labels',fontsize=7.1,weight='bold',color='#172D4B',va='center')
paths=[]
for ext in ['pdf','svg','png']:
 p=ROOT/f'figures/binding_challenge.{ext}';fig.savefig(p,dpi=220,facecolor='white');paths.append(str(p.relative_to(ROOT)))
plt.close(fig)
manifest={'figure_id':'binding_challenge','archetype':'mechanism','source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'item_ids':[r['item_id'] for r in case],'selection':'first predefined idle/open drink pair, both swaps/targets; no API outcomes used',
 'script':str(Path(__file__).relative_to(ROOT)),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'outputs':paths,
 'output_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},'physical_cm':[8.5,7.0],'empirical_statistics':False}
(ROOT/'.research/figures/binding_source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
p=ROOT/'.research/figures/source_data_manifest.json';m=json.loads(p.read_text());m['figures']=[f for f in m['figures'] if f.get('figure_id')!='binding_challenge']+[manifest];p.write_text(json.dumps(m,indent=2)+'\n')
print('Exported exact role-binding mechanism and source manifest')
