"""Paper candidates from completed analysis only; no model-response synthesis."""
from pathlib import Path
import sys,json,hashlib
from collections import defaultdict
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'src'))
from event_completion.analysis import cluster_ci
source=ROOT/'data/analysis/main_planned.jsonl';rows=[json.loads(l) for l in source.read_text().splitlines()]
assert len(rows)==28104,'All planned main rows required, including missing outcomes.'
models=json.loads((ROOT/'config/study_protocol_candidate.json').read_text())['main_models'];labels=['Qwen8','Llama8','Ministral8','Gemma12','Qwen14','Qwen32']
base={(r['model'],r['item']['family_id'],r['item'].get('knowledge'),r['item'].get('composition'),r['item'].get('context')):r for r in rows if r['dataset']=='main_core'}
families=sorted({r['item']['family_id'] for r in rows if r['dataset']=='main_core'});verbs={r['item']['family_id']:r['item']['verb'] for r in rows if r['dataset']=='main_core'}
colors=['#0072B2','#009E73','#D55E00'];markers=['o','s','^'];manifest=[];denominators=[]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':7.5,'axes.titlesize':8,'axes.labelsize':7.5,'xtick.labelsize':7,'ytick.labelsize':7,'legend.fontsize':7,'pdf.fonttype':42,'svg.fonttype':'none','axes.spines.right':False,'axes.spines.top':False})
def q(r):return (r.get('parsed') or {}).get('hypothesis_probability') if r else None
def ci(values,lexical,description,planned):
 result=cluster_ci(values,lexical,b=10000,test=False)
 denominators.append({'cell':description,'planned_families':planned,'valid_values':len(values),'lexical_blocks':len(set(lexical)),'metric':result})
 return result
def point(ax,x,result,color,marker,label=None):
 if result:
  y=result['estimate'];lo,hi=result['ci95'];ax.errorbar(x,y,yerr=[[max(0,y-lo)],[max(0,hi-y)]],fmt=marker,color=color,label=label,markersize=3,capsize=2,elinewidth=.7,clip_on=False)
def categorical(ax,ylabel,ylim=(-1,1)):
 ax.set_xticks(range(6),labels,rotation=25,ha='right');ax.set_xlim(-.5,5.5);ax.set_ylim(*ylim);ax.set_ylabel(ylabel);ax.axhline(0,color='#525252',ls=':',lw=.7);ax.grid(axis='y',alpha=.13)
def finish(fig,number,caption):
 name=f'main_fig{number}'
 for ext in ['pdf','svg','png']:fig.savefig(ROOT/f'figures/{name}.{ext}',dpi=300,bbox_inches='tight')
 plt.close(fig);(ROOT/f'figures/{name}_caption.md').write_text(caption+'\n')
 manifest.append({'figure':name,'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'script':str(Path(__file__).relative_to(ROOT)),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'caption':caption,'bootstrap_draws':10000,'seed':20271007})
# Fig2: score levels distinguish bounded target from occurrence, Real only.
fig,axes=plt.subplots(1,2,figsize=(17.8/2.54,7.1/2.54),sharey=True)
for j,comp in enumerate(['bounded','unbounded']):
 for z,context in enumerate(['neutral','supportive','cancelling']):
  for i,m in enumerate(models):
   rr=[base[m,f,'real',comp,context] for f in families];valid=[r for r in rr if q(r) is not None];result=ci([q(r) for r in valid],[r['item']['verb'] for r in valid],f'fig2:{m}:{comp}:{context}',120)
   point(axes[j],i+(z-1)*.17,result,colors[z],markers[z],context.capitalize() if i==0 else None)
 categorical(axes[j],'Mean subjective target-truth q',(0,1));axes[j].set_title('Bounded target' if comp=='bounded' else 'Activity occurrence')
fig.legend(*axes[0].get_legend_handles_labels(),loc='upper center',ncol=3,frameon=False);fig.subplots_adjust(top=.81,bottom=.28,wspace=.16)
finish(fig,2,'Real-presentation target-truth scores for bounded versus activity targets across contexts. Points are means over up to 120 planned families; intervals use 10,000 seeded verb-then-family percentile bootstrap draws. Full q domain [0,1]. Scores are elicited and uncalibrated. Missing/invalid q is excluded with denominators recorded; no unknown target receives an invented outcome.')
# Fig3: paired composition contrasts by presentation.
contrasts={}
fig,ax=plt.subplots(figsize=(17.8/2.54,6.6/2.54))
for z,k in enumerate(['real','nonce','micro']):
 for i,m in enumerate(models):
  vv=[];lex=[]
  for f in families:
   a=q(base[m,f,k,'bounded','neutral']);b=q(base[m,f,k,'unbounded','neutral'])
   if a is not None and b is not None:vv.append(a-b);lex.append(verbs[f])
  result=ci(vv,lex,f'fig3:{m}:{k}',120);contrasts[m,k]=result;point(ax,i+(z-1)*.18,result,colors[z],markers[z],k.capitalize() if i==0 else None)
categorical(ax,'Neutral CS: q(B) − q(activity)');fig.legend(*ax.get_legend_handles_labels(),loc='upper center',ncol=3,frameon=False);fig.subplots_adjust(top=.82,bottom=.28)
finish(fig,3,'Paired neutral compositional sensitivity across the three presentations, using up to 120 complete family pairs per system. A negative score distinguishes endpoint belief from activity occurrence; logic alone does not specify its magnitude, and a negative contrast alone does not certify categorical correctness. Intervals resample lexical verbs then families. Definitions, notation and length also differ across presentations, so layer gaps do not identify internal knowledge removal.')
# Fig4: intended prior, exploratory.
prior={(r['model'],r['item']['family_id'],r['item']['prior'],r['item']['context']):r for r in rows if r['dataset']=='main_prior'};pf=sorted({key[1] for key in prior})
fig,ax=plt.subplots(figsize=(17.8/2.54,6.6/2.54))
for z,context in enumerate(['neutral','supportive','cancelling']):
 for i,m in enumerate(models):
  vv=[];lex=[]
  for f in pf:
   a=q(prior[m,f,'high',context]);b=q(prior[m,f,'low',context])
   if a is not None and b is not None:vv.append(a-b);lex.append(verbs[f])
  point(ax,i+(z-1)*.18,ci(vv,lex,f'fig4:{m}:{context}',40),colors[z],markers[z],context.capitalize() if i==0 else None)
categorical(ax,'Intended-prior q(high) − q(low)');fig.legend(*ax.get_legend_handles_labels(),loc='upper center',ncol=3,frameon=False);fig.subplots_adjust(top=.82,bottom=.28)
finish(fig,4,'Exploratory intended completion-burden sensitivity in bounded Real targets, with up to 40 paired families per context and system. High/low are intended directions without human prior ratings; no causal world-knowledge effect is identified. Interval procedure matches Figure 3. Supporting/cancelling evidence determines the theory label regardless of burden cue.')
# Fig5: three-point association, no causal scale claim.
fig,ax=plt.subplots(figsize=(8.5/2.54,6.375/2.54));qm=['qwen/qwen3-8b','qwen/qwen3-14b','qwen/qwen3-32b'];xx=np.log2([8.2,14.8,32.8])
for z,k in enumerate(['real','nonce','micro']):
 ys=[]
 for x,m in zip(xx,qm):
  result=contrasts[m,k];ys.append(result['estimate'] if result else np.nan);point(ax,x,result,colors[z],markers[z])
 ax.plot(xx,ys,color=colors[z],ls=['-','--',':'][z],lw=.8,label=k.capitalize())
ax.set_xticks(xx,['8.2','14.8','32.8']);ax.set_xlabel('Dense parameters (billions; log scale)');ax.set_ylabel('Neutral CS');ax.set_ylim(-1,1);ax.axhline(0,color='#525252',ls=':',lw=.7);ax.legend(frameon=False,fontsize=7);fig.tight_layout()
finish(fig,5,'Within-Qwen three-size association in neutral paired composition scores. Points use the same 120 planned family pool and intervals as Figure 3; lines connect three observations rather than establish a scaling law. Qwen8 uses Alibaba with unspecified precision; Qwen14/32 use DeepInfra FP8. Training and provider confounds prevent a parameter-count causal interpretation.')
# Fig6: cancellation q and paired rule accuracy gains.
fig,axes=plt.subplots(1,2,figsize=(17.8/2.54,7.1/2.54))
for i,m in enumerate(models):
 vv=[];lex=[]
 for f in families:
  a=q(base[m,f,'real','bounded','cancelling']);b=q(base[m,f,'real','bounded','neutral'])
  if a is not None and b is not None:vv.append(a-b);lex.append(verbs[f])
 point(axes[0],i,ci(vv,lex,f'fig6:cancel:{m}',120),colors[0],markers[0])
 for z,variant in enumerate(['natural_rule','structural_rule']):
  by=defaultdict(list)
  for r in rows:
   if r['model']==m and r['dataset']==variant:
    j=r['item'];b=base[m,j['family_id'],j['knowledge'],j['composition'],j['context']];by[j['family_id']].append(int(bool(r.get('correct')))-int(bool(b.get('correct'))))
  ordered=sorted(by);vv=[np.mean(by[f]) for f in ordered];lex=[verbs[f] for f in ordered]
  point(axes[1],i+(z-.5)*.18,ci(vv,lex,f'fig6:{variant}:{m}',24),colors[z+1],markers[z+1],variant.replace('_',' ').capitalize() if i==0 else None)
categorical(axes[0],'Bounded Real q(cancel) − q(neutral)');categorical(axes[1],'Paired all-planned accuracy gain');axes[0].set_title('Contextual override');axes[1].set_title('Rule intervention');fig.legend(*axes[1].get_legend_handles_labels(),loc='upper center',ncol=2,frameon=False);fig.subplots_adjust(top=.8,bottom=.28,wspace=.3)
finish(fig,6,'Contextual override and guidance gains use different units/populations. Left: bounded Real cancellation-minus-neutral q on up to 120 complete pairs. Right: rule-minus-baseline accuracy, averaged within each of 24 fixed families across 12 matched neutral/cancelling cells; parse/transport failures count incorrect. Lexical/family bootstrap intervals, no outcome-selected exclusions. A correct ceiling can give zero gain; guidance is not proof of an internal semantic mechanism.')
(ROOT/'.research/figures/main_source_manifest.json').write_text(json.dumps({'figures':manifest,'cell_denominators_and_estimates':denominators,'requires_visual_QA':True},indent=2)+'\n')
print('Exported five empirical figure candidates with manifests; visual QA pending.')
