"""Export pilot diagnostic using real, planned records only."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'src'))
from event_completion.analysis import cluster_ci
source=ROOT/'data/analysis/pilot_v2_planned.jsonl'
rows=[json.loads(l) for l in source.read_text().splitlines()]
if len(rows)!=1600 or any(r.get('missing') for r in rows):
 raise SystemExit('Full 1,600-cell pilot collection required for this figure.')
core=[r for r in rows if r['dataset']=='pilot_core']
models=sorted({r['model'] for r in core});layers=['real','nonce','micro'];contexts=['neutral','supportive','cancelling']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':7.5,'axes.labelsize':7.5,'axes.titlesize':8,'xtick.labelsize':7,'ytick.labelsize':7,'legend.fontsize':7,'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
fig,axes=plt.subplots(2,3,figsize=(17.8/2.54,10.4/2.54),sharex=True,sharey=True)
counts=[]
for mi,model in enumerate(models):
 for ki,know in enumerate(layers):
  ax=axes[mi,ki]
  for comp,color,marker,linestyle in [('bounded','#0072B2','o','-'),('unbounded','#D55E00','s','--')]:
   means=[];los=[];his=[]
   for context in contexts:
    rr=[r for r in core if r['model']==model and r['item']['knowledge']==know and r['item']['composition']==comp and r['item']['context']==context]
    valid=[r for r in rr if r.get('parsed') and 'hypothesis_probability' in r['parsed']]
    result=cluster_ci([r['parsed']['hypothesis_probability'] for r in valid],[r['item']['verb'] for r in valid],b=2000,test=False)
    counts.append({'model':model,'knowledge':know,'composition':comp,'context':context,'planned':len(rr),'valid':len(valid)})
    means.append(result['estimate'] if result else np.nan);los.append(result['ci95'][0] if result else np.nan);his.append(result['ci95'][1] if result else np.nan)
   ax.plot(range(3),means,color=color,marker=marker,ls=linestyle,linewidth=1,markersize=3,clip_on=False,label=comp.capitalize())
   ax.fill_between(range(3),los,his,color=color,alpha=.15,lw=0)
  ax.set_xlim(-.35,2.35);ax.set_ylim(0,1);ax.set_yticks([0,.25,.5,.75,1]);ax.set_xticks(range(3),['Neutral','Support','Cancel']);ax.grid(axis='y',alpha=.15)
  if mi==0:ax.set_title(know.capitalize())
  if ki==0:ax.set_ylabel(model.split('/')[-1]+'\nMean subjective q')
fig.legend(*axes[0,0].get_legend_handles_labels(),loc='lower center',ncol=2,frameon=False,bbox_to_anchor=(.5,0))
fig.subplots_adjust(left=.13,right=.99,top=.93,bottom=.13,wspace=.22,hspace=.22)
for ext in ['pdf','svg','png']:fig.savefig(ROOT/f'figures/pilot_diagnostic.{ext}',dpi=300)
plt.close(fig)
manifest={'figure':'pilot_diagnostic','purpose':'pilot diagnostic, not confirmation','source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'seed':20271007,'bootstrap_draws':2000,'bootstrap':'verbs then families within verbs','human_review':False,'cells':counts}
(ROOT/'.research/figures/source_data_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(ROOT/'figures/pilot_diagnostic_caption.md').write_text('Pilot prompt diagnostic. Mean subjective target-truth q across 40 held-out pilot families per cell, with descriptive 95% percentile intervals from 2,000 seeded verb-then-family bootstrap draws (12 lexical blocks). Bounded targets require their endpoint; unbounded targets require sufficient activity occurrence. These q values are elicited judgments, not calibrated probabilities. Panels use genuine pilot responses and operational gold; independent human validation is pending. Scenario variants share process mechanisms and are not independent logical types. No pilot significance testing or outcome-based item/model selection was performed.\n')
print('Exported pilot diagnostic and source manifest.')
