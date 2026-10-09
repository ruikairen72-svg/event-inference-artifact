"""Completed-main descriptive label diagnostics; no new hypothesis tests."""
from pathlib import Path
import sys,json,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'src'))
from event_completion.analysis import load,cluster_ci
source=ROOT/'data/analysis/main_planned.jsonl';rows=load(source);assert len(rows)==28104
models=json.loads((ROOT/'config/study_protocol_candidate.json').read_text())['main_models']
labels=['Qwen8','Llama8','Ministral8','Gemma12','Qwen14','Qwen32']
colors=['#0072B2','#009E73','#D55E00'];markers=['o','s','^']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':7.5,'axes.titlesize':8,'axes.labelsize':7.5,'xtick.labelsize':7,'ytick.labelsize':7,'legend.fontsize':7,'pdf.fonttype':42,'svg.fonttype':'none','axes.spines.right':False,'axes.spines.top':False})
fig,axes=plt.subplots(1,2,figsize=(17.8/2.54,7.1/2.54),sharey=True);estimates=[]
for panel,composition in enumerate(['bounded','unbounded']):
 ax=axes[panel]
 for z,k in enumerate(['real','nonce','micro']):
  for i,m in enumerate(models):
   g=sorted([r for r in rows if r['model']==m and r['dataset']=='main_core' and r['item']['knowledge']==k and r['item']['composition']==composition and r['item']['context']=='neutral'],key=lambda r:r['item']['family_id'])
   assert len(g)==120 and len({r['item']['family_id'] for r in g})==120
   assert {r['item']['gold'] for r in g}==({'unknown'} if composition=='bounded' else {'entailed'})
   result=cluster_ci([int(bool(r.get('correct'))) for r in g],[r['item']['verb'] for r in g],b=10000,test=False)
   estimates.append({'model':m,'knowledge':k,'composition':composition,'context':'neutral','planned':len(g),'parsed':sum(bool(r.get('parsed')) for r in g),**result})
   y=result['estimate']*100;lo,hi=[v*100 for v in result['ci95']]
   ax.errorbar(i+(z-1)*.18,y,yerr=[[max(0,y-lo)],[max(0,hi-y)]],fmt=markers[z],color=colors[z],markersize=3,capsize=2,elinewidth=.7,clip_on=False,label=k.capitalize() if i==0 else None)
 ax.set_xticks(range(6),labels,rotation=25,ha='right');ax.set_xlim(-.5,5.5);ax.set_ylim(0,100);ax.set_yticks([0,25,50,75,100]);ax.grid(axis='y',alpha=.15)
 ax.set_title('Bounded target: unknown recall' if composition=='bounded' else 'Activity target: entailed recall')
 ax.set_xlabel('Named main system')
axes[0].set_ylabel('Correct neutral judgments (%)')
fig.legend(*axes[0].get_legend_handles_labels(),loc='upper center',ncol=3,frameon=False)
fig.subplots_adjust(top=.81,bottom=.31,wspace=.18)
for ext in ['pdf','svg','png']:fig.savefig(ROOT/f'figures/main_category_accuracy.{ext}',dpi=300,bbox_inches='tight')
plt.close(fig)
caption='Neutral categorical correctness separates unresolved bounded endpoints (gold unknown) from witnessed activity occurrence (gold entailed). All six systems and three presentations retain 120 planned families per cell; missing/invalid judgments count incorrect. Marginal 95% intervals use 10,000 seeded verb-then-family bootstrap draws across 12 retained lexical blocks. Floor/ceiling intervals describe this construction pool, not deterministic service behavior or arbitrary English. No new p-values; presentation gaps also include definitions, notation and length.'
(ROOT/'figures/main_category_accuracy_caption.md').write_text(caption+'\n')
(ROOT/'.research/figures/category_source_manifest.json').write_text(json.dumps({'figure':'main_category_accuracy','designation':'post-freeze descriptive diagnostic, not a new confirmatory test','caption':caption,'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,Path(__file__),ROOT/'src/event_completion/analysis.py']},'seed':20271007,'estimates':estimates,'requires_visual_QA':True},indent=2)+'\n')
print('Categorical diagnostic exported; visual QA required.')
