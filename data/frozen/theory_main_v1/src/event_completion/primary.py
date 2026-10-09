"""Prospective five-contrast extraction; no selection from observed effects."""
from collections import defaultdict
from .analysis import cluster_ci
METRICS=['neutral_cs_target_real','neutral_cs_real_minus_nonce','neutral_cs_real_minus_micro','bounded_real_cancel_minus_neutral_q','structural_rule_minus_baseline_accuracy']
def holm(ps):
 """Holm adjustment preserves positions and treats unavailable tests as p=1."""
 n=len(ps);order=sorted(range(n),key=lambda i:1 if ps[i] is None else ps[i]);out=[None]*n;last=0
 for rank,i in enumerate(order):
  value=1 if ps[i] is None else ps[i]
  last=max(last,min(1,(n-rank)*value));out[i]=None if ps[i] is None else last
 return out

def extract(rows,model):
 rr=[r for r in rows if r['model']==model];base={};rules={};verbs={}
 for r in rr:
  i=r['item'];f=i['family_id'];verbs[f]=i.get('verb',f)
  key=(f,i.get('knowledge'),i.get('composition'),i.get('context'))
  if r['dataset']=='main_core':
   if key in base:raise ValueError('Duplicate baseline analysis cell')
   base[key]=r
  elif r['dataset']=='structural_rule':
   if key in rules:raise ValueError('Duplicate rule analysis cell')
   rules[key]=r
 families=sorted({k[0] for k in base});rulefamilies=sorted({k[0] for k in rules});out={}
 def term(f,k,c,x,coef):return (base.get((f,k,c,x)),coef)
 for metric in METRICS:
  records=[]
  for f in rulefamilies if metric==METRICS[-1] else families:
   if metric==METRICS[-1]:
    keys=[k for k in rules if k[0]==f]
    if len(keys)!=12:raise ValueError('Rule family must contain all 12 neutral/cancelling cells')
    # All planned correctness: parse/transport missing outcomes count incorrect.
    value=sum(bool(rules[k].get('correct'))-bool(base.get(k,{}).get('correct')) for k in keys)/len(keys)
    records.append({'family':f,'verb':verbs[f],'value':value,'lower':value,'upper':value,'valid':True});continue
   if metric==METRICS[0]:terms=[term(f,'real','bounded','neutral',1),term(f,'real','unbounded','neutral',-1)]
   elif metric in METRICS[1:3]:
    knowledge='nonce' if metric==METRICS[1] else 'micro'
    terms=[term(f,'real','bounded','neutral',1),term(f,'real','unbounded','neutral',-1),term(f,knowledge,'bounded','neutral',-1),term(f,knowledge,'unbounded','neutral',1)]
   else:terms=[term(f,'real','bounded','cancelling',1),term(f,'real','bounded','neutral',-1)]
   value=0;lower=0;upper=0;valid=True
   for r,coef in terms:
    parsed=(r or {}).get('parsed') or {};q=parsed.get('hypothesis_probability')
    if q is None:valid=False;lower+=min(0,coef);upper+=max(0,coef)
    else:value+=coef*q;lower+=coef*q;upper+=coef*q
   records.append({'family':f,'verb':verbs[f],'value':value if valid else None,'lower':lower,'upper':upper,'valid':valid})
  out[metric]=records
 return out

def analyze_primary(rows,models,draws=10000):
 results=[]
 for model in models:
  extracted=extract(rows,model)
  for metric,rr in extracted.items():
   valid=[r for r in rr if r['valid']]
   ci=cluster_ci([r['value'] for r in valid],[r['verb'] for r in valid],b=draws) if valid else None
   results.append({'model':model,'metric':metric,'planned_families':len(rr),'valid_pairs_or_rule_families':len(valid),'missing_families':len(rr)-len(valid),'missing_q_adverse_bounds':[sum(r['lower'] for r in rr)/len(rr),sum(r['upper'] for r in rr)/len(rr)] if rr else None,'result':ci})
 adjusted=holm([r['result']['p_cluster_signflip'] if r['result'] else None for r in results])
 for r,p in zip(results,adjusted):r['p_holm_30']=p
 return results
