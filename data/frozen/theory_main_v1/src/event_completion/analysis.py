"""Paired behavioral metrics from real response records only."""
from pathlib import Path
from collections import Counter,defaultdict
import json,math
import numpy as np
from scipy.stats import binomtest
ROOT=Path(__file__).resolve().parents[2]
def load(p):return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []
def summary(rows):
 groups=defaultdict(list)
 for r in rows:
  i=r['item'];groups[(r['model'],i.get('knowledge','original'),i.get('composition','original'),i.get('context',i.get('group','original')))].append(r)
 cells=[]
 for key,rr in sorted(groups.items()):
  valid=[r for r in rr if r.get('parsed')];qs=[r['parsed']['hypothesis_probability'] for r in valid if 'hypothesis_probability' in r['parsed']]
  cells.append({'model':key[0],'knowledge':key[1],'composition':key[2],'context':key[3],'n':len(rr),'parsed_n':len(valid),'accuracy':sum(r['correct'] for r in rr)/len(rr),'entailed_rate':sum(r.get('parsed',{}).get('judgment')=='entailed' if r.get('parsed') else False for r in rr)/len(rr),'mean_q':float(np.mean(qs)) if qs else None,'q_sd':float(np.std(qs,ddof=1)) if len(qs)>1 else None,'gold_labels':dict(Counter(r['item']['gold'] for r in rr))})
 return cells

def cluster_ci(values,clusters=None,seed=20271007,b=10000,test=True):
 vals=np.asarray(values,float);n=len(vals)
 if not n:return None
 if clusters is None:clusters=list(range(n))
 # Resample lexical blocks then families within each drawn block.
 by=defaultdict(list)
 for v,c in zip(vals,clusters):by[c].append(v)
 keys=list(by);rng=np.random.default_rng(seed);boots=[]
 for _ in range(b):
  sample=[]
  for k in rng.choice(len(keys),len(keys),replace=True):
   vv=by[keys[k]];sample.extend(rng.choice(vv,len(vv),replace=True))
  boots.append(np.mean(sample))
 lo,hi=np.quantile(boots,[.025,.975])
 if not test:return {'estimate':float(np.mean(vals)),'ci95':[float(lo),float(hi)],'n_families':n,'n_lexical_blocks':len(keys),'bootstrap_draws':b}
 # Exact block sign-flip test if feasible; cluster means weighted by cluster size.
 means=[sum(by[k]) for k in keys];denom=sum(len(by[k]) for k in keys);obs=abs(np.mean(vals))
 if len(keys)<=16:
  perm=[abs(sum(v*(1 if mask>>j&1 else -1) for j,v in enumerate(means))/denom) for mask in range(1<<len(keys))]
  p=sum(x>=obs-1e-12 for x in perm)/len(perm)
 else:
  signs=rng.choice([-1,1],size=(10000,len(keys)));perm=abs(signs.dot(means)/denom);p=(1+sum(perm>=obs-1e-12))/(len(perm)+1)
 return {'estimate':float(np.mean(vals)),'ci95':[float(lo),float(hi)],'n_families':n,'n_lexical_blocks':len(keys),'p_cluster_signflip':float(p),'bootstrap_draws':b}

def contrasts(rows,pilot=False):
 # Keep one request per cell: successful outputs are never replaced by better answers.
 rr={ (r['model'],r['item']['family_id'],r['item'].get('knowledge'),r['item'].get('composition'),r['item'].get('context'),r['item'].get('prior'),r['item'].get('variant','baseline')):r for r in rows if r.get('parsed')}
 models=sorted({r['model'] for r in rows});out=[]
 for model in models:
  families=sorted({r['item']['family_id'] for r in rows if r['model']==model and r['item'].get('stratum')!='label_control' and not r['item'].get('original')})
  for know in ['real','nonce','micro']:
   for context in ['neutral','supportive','cancelling']:
    vals=[];verbs=[]
    for f in families:
     a=rr.get((model,f,know,'bounded',context,None,'baseline'));b=rr.get((model,f,know,'unbounded',context,None,'baseline'))
     if a and b and 'hypothesis_probability' in a['parsed'] and 'hypothesis_probability' in b['parsed']:
      vals.append(a['parsed']['hypothesis_probability']-b['parsed']['hypothesis_probability']);verbs.append(a['item']['verb'])
    if vals:out.append({'model':model,'metric':'CS_target','knowledge':know,'context':context,**cluster_ci(vals,verbs,b=2000 if pilot else 10000)})
  for context in ['neutral','supportive','cancelling']:
   vals=[];verbs=[]
   for f in families:
    a=rr.get((model,f,'real','bounded',context,'high','baseline'));b=rr.get((model,f,'real','bounded',context,'low','baseline'))
    if a and b:
     vals.append(a['parsed']['hypothesis_probability']-b['parsed']['hypothesis_probability']);verbs.append(a['item']['verb'])
   if vals:out.append({'model':model,'metric':'WKE_intended_exploratory','context':context,**cluster_ci(vals,verbs,b=2000 if pilot else 10000)})
 return out

def analyze_run(run_id,pilot=False):
 folder=ROOT/'data/raw_runs'/run_id;rows=load(folder/'responses.jsonl');attempts=load(folder/'attempts.jsonl');cells=summary(rows)
 stats={'run_id':run_id,'responses':len(rows),'parse_valid':sum(r.get('parsed') is not None for r in rows),'parse_valid_rate':sum(r.get('parsed') is not None for r in rows)/len(rows) if rows else 0,'transport_attempts':len(attempts),'http_failures':sum(not r.get('transport_ok') for r in attempts),'known_actual_cost_usd':sum(r['charged_or_reserved_usd'] for r in attempts if not r['cost_is_estimate']),'conservative_ledger_usd':sum(r['charged_or_reserved_usd'] for r in attempts),'finish_reasons':dict(Counter(r['finish_reason'] for r in rows)),'returned_providers':dict(Counter((r['returned_provider'] or 'unspecified') for r in rows)),'model_counts':dict(Counter(r['model'] for r in rows)),'cells':cells}
 (ROOT/f'reports/{run_id}_summary.json').write_text(json.dumps(stats,indent=2)+'\n')
 if not pilot:(ROOT/f'reports/{run_id}_contrasts.json').write_text(json.dumps(contrasts(rows),indent=2)+'\n')
 print(json.dumps({k:v for k,v in stats.items() if k!='cells'},indent=2));return stats
if __name__=='__main__':
 import sys
 analyze_run(sys.argv[1],pilot='pilot' in sys.argv[1])
