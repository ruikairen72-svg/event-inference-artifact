"""Exploratory, fixed text-only baselines; no API or LLM outcomes used."""
from pathlib import Path
import json,hashlib,collections,sys
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,confusion_matrix
ROOT=Path(__file__).resolve().parents[1]
def load(name):return [json.loads(x) for x in (ROOT/'data/generated'/f'{name}.jsonl').read_text().splitlines()]
train=load('pilot_core')
assert len(train)==720
labels=['contradicted','entailed','unknown']
majority=collections.Counter(r['gold'] for r in train).most_common(1)[0][0]
outputs=[];predictions=[]
core=load('main_core')
key=lambda r:(r['family_id'],r['knowledge'],r['composition'],r['context'])
core_by_key={key(r):r for r in core}
for mode in ['majority','hypothesis_only','premise_only','premise_and_hypothesis']:
 def text(r):
  if mode=='hypothesis_only':return r['hypothesis']
  if mode=='premise_only':return r['premise']
  return r['premise']+' '+r['hypothesis']
 model=None
 if mode!='majority':
  model=make_pipeline(TfidfVectorizer(ngram_range=(1,1),lowercase=True,min_df=1),LogisticRegression(C=1.0,max_iter=1000,random_state=20271007))
  model.fit([text(r) for r in train],[r['gold'] for r in train])
 for dataset in ['main_core','template_ood','name','label_order','label_only','natural_rule','structural_rule','real_definition']:
  rows=load(dataset);assert not set(r['family_id'] for r in rows)&set(r['family_id'] for r in train)
  pred=[majority]*len(rows) if model is None else model.predict([text(r) for r in rows]).tolist()
  gold=[r['gold'] for r in rows]
  matched_base=[core_by_key[key(r)] for r in rows]
  assert [r['gold'] for r in matched_base]==gold
  base_pred=[majority]*len(rows) if model is None else model.predict([text(r) for r in matched_base]).tolist()
  base_accuracy=accuracy_score(gold,base_pred)
  def stats(indices):
   yy=[gold[j] for j in indices];pp=[pred[j] for j in indices]
   available=sorted(set(yy))
   return {'n':len(indices),'accuracy':accuracy_score(yy,pp),'macro_label_accuracy':sum(sum(pred[j]==g for j in indices if gold[j]==g)/sum(gold[j]==g for j in indices) for g in available)/len(available)}
  cells=[]
  for k in ['real','nonce','micro']:
   for c in ['bounded','unbounded']:
    for x in ['neutral','supportive','cancelling']:
     ids=[j for j,r in enumerate(rows) if (r['knowledge'],r['composition'],r['context'])==(k,c,x)]
     if ids:cells.append({'knowledge':k,'composition':c,'context':x,**stats(ids)})
  outputs.append({'baseline':mode,'dataset':dataset,**stats(list(range(len(rows)))),'baseline_accuracy_on_same_families_contexts':base_accuracy,'paired_accuracy_change':accuracy_score(gold,pred)-base_accuracy,'confusion_labels':labels,'confusion':confusion_matrix(gold,pred,labels=labels).tolist(),'cells':cells})
  predictions.extend({'baseline':mode,'dataset':dataset,'item_id':r['item_id'],'gold':r['gold'],'prediction':p} for r,p in zip(rows,pred))
report={'designation':'exploratory offline surface recoverability; not LLM inference or human validation','training':'720 disjoint pilot-core gold labels','features':'word unigrams only; fixed TF-IDF and logistic C=1.0; no output-based tuning',
 'instruction_limit':'uses item text, not the separate rule/order/JSON system instructions; identical item texts necessarily have identical baseline predictions',
 'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'data/generated/pilot_core.jsonl',ROOT/'data/generated/main_core.jsonl']},'results':outputs}
(ROOT/'reports/surface_baselines.json').write_text(json.dumps(report,indent=2)+'\n')
(ROOT/'data/analysis').mkdir(exist_ok=True)
(ROOT/'data/analysis/surface_baseline_predictions.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in predictions))
print(json.dumps([{k:r[k] for k in ['baseline','dataset','accuracy','macro_label_accuracy','baseline_accuracy_on_same_families_contexts','paired_accuracy_change']} for r in outputs if r['dataset'] in ['main_core','template_ood']],indent=2))
