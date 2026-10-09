"""Analyze all frozen supplementary cells; earliest response per exact payload.

Retains failures in denominators. The technical probe's Qwen payloads do not
match the main protocol and are never substituted for main outcomes.
"""
from pathlib import Path
from collections import Counter,defaultdict
from types import SimpleNamespace
import hashlib,json,sys
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from event_completion.runner_binding import make_jobs
def load(p):return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 protocol=json.loads((ROOT/'reports/reviewer_binding_protocol.json').read_text())
 assert sha(ROOT/'data/supplementary/reviewer_binding.jsonl')==protocol['dataset_sha256']
 definition=json.loads((ROOT/'reports/reviewer_binding_definition_protocol.json').read_text())
 assert sha(ROOT/'data/supplementary/reviewer_binding_v2.jsonl')==definition['dataset_sha256']
 args=SimpleNamespace(datasets='reviewer_binding_v2',models=','.join(protocol['models']),items_per_model=None)
 jobs=make_jobs(args);assert len(jobs)==5040
 allresponses=[]
 for p in sorted((ROOT/'data/raw_runs').glob('*/responses.jsonl')):
  allresponses.extend((x,str(p.relative_to(ROOT))) for x in load(p) if x.get('dataset') in ['reviewer_binding','reviewer_binding_v2'] and x.get('transport_ok'))
 byhash={};duplicates=[]
 for x,source in sorted(allresponses,key=lambda t:(t[0]['started_utc'],t[1])):
  if x['request_id'] in byhash:duplicates.append(x['request_id'])
  else:byhash[x['request_id']]=(x,source)
 missing=[j['request_id'] for j in jobs if j['request_id'] not in byhash]
 if missing:raise SystemExit(f'Full challenge collection not complete: {len(missing)} missing exact payloads; no final estimates written.')
 rows=[]
 for j in jobs:
  x,source=byhash[j['request_id']]
  assert x['payload']==j['payload']
  rows.append({**x,'item':j['item'],'source':source,'correct':bool(x.get('parsed') and x['parsed']['judgment']==j['item']['gold'])})
 (ROOT/'data/analysis/reviewer_binding_planned.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
 rng=np.random.default_rng(20271009)
 def ci(rs,field='correct'):
  blocks=sorted({r['item']['family_id'] for r in rs})
  means=np.array([np.mean([float(r[field]) for r in rs if r['item']['family_id']==b]) for b in blocks])
  samples=rng.choice(means,size=(10000,len(means)),replace=True).mean(axis=1)
  return np.quantile(samples,[.025,.975]).tolist()
 def stats(rs):
  goldcounts=Counter(r['item']['gold'] for r in rs)
  correct=sum(r['correct'] for r in rs)
  recalls={g:sum(r['correct'] for r in rs if r['item']['gold']==g)/n for g,n in goldcounts.items()}
  return {'n':len(rs),'correct':correct,'accuracy':correct/len(rs),'accuracy_ci95_lemma_bootstrap':ci(rs),
   'macro_recall':float(np.mean(list(recalls.values()))),'gold_recall':recalls,
   'invalid':sum(r.get('parsed') is None for r in rs),
   'confusion':{g:dict(Counter((r.get('parsed') or {}).get('judgment','invalid') for r in rs if r['item']['gold']==g)) for g in goldcounts}}
 results=[];cells=[];lemmas=[];strata=[]
 for m in protocol['models']:
  mr=[r for r in rows if r['model']==m];pairs=defaultdict(list)
  for r in mr:pairs[r['item']['pair_id']].append(r)
  different=[p for p in pairs.values() if len({r['item']['gold'] for r in p})==2]
  assert len(different)==288 and all(len(p)==2 for p in pairs.values())
  paired=[{'item':p[0]['item'],'correct':all(r['correct'] for r in p)} for p in different]
  results.append({'model':m,'all':stats(mr),'by_presentation':{k:stats([r for r in mr if r['item']['knowledge']==k]) for k in ['real','nonce','micro']},
   'by_split':{s:stats([r for r in mr if r['item']['lexical_split']==s]) for s in ['seen','held_out']},
   'different_gold_pair_both_correct':{'n':288,'both_correct':sum(r['correct'] for r in paired),'rate':float(np.mean([r['correct'] for r in paired])),'ci95_lemma_bootstrap':ci(paired)}})
  for k in ['real','nonce','micro']:
   for comp in ['bounded','unbounded']:
    for g in ['entailed','contradicted','unknown']:
     rs=[r for r in mr if (r['item']['knowledge'],r['item']['composition'],r['item']['gold'])==(k,comp,g)]
     cells.append({'model':m,'knowledge':k,'composition':comp,'gold':g,**stats(rs)})
  for lemma in sorted({r['item']['lemma'] for r in mr}):
   rs=[r for r in mr if r['item']['lemma']==lemma];lemmas.append({'model':m,'lemma':lemma,'split':rs[0]['item']['lexical_split'],**stats(rs)})
  for s in ['quantity','path','incremental']:
   strata.append({'model':m,'stratum':s,**stats([r for r in mr if r['item']['verb_class']==s])})
 items=load(ROOT/'data/supplementary/reviewer_binding_v2.jsonl');train=load(ROOT/'data/generated/pilot_core.jsonl')
 trainlemmas={r['verb'] for r in train};assert not trainlemmas&set(protocol['held_out_lemmas'])
 text=lambda r:r['premise']+' '+r['hypothesis']
 baseline=make_pipeline(TfidfVectorizer(ngram_range=(1,1),lowercase=True,min_df=1),LogisticRegression(C=1,max_iter=1000,random_state=20271007))
 baseline.fit([text(r) for r in train],[r['gold'] for r in train]);pred=baseline.predict([text(r) for r in items]).tolist()
 br=[{'item':r,'correct':p==r['gold'],'parsed':{'judgment':p}} for r,p in zip(items,pred)]
 vectors=baseline[0].transform([text(r) for r in items]); pairindices=defaultdict(list)
 for i,r in enumerate(items):pairindices[r['pair_id']].append(i)
 assert all((vectors[p[0]]!=vectors[p[1]]).nnz==0 and pred[p[0]]==pred[p[1]] for p in pairindices.values())
 bs={'training':'unchanged 720 labeled pilot core items; original settings; no challenge fitting','all':stats(br),
     'by_presentation':{k:stats([r for r in br if r['item']['knowledge']==k]) for k in ['real','nonce','micro']},'different_gold_pair_both_correct':0,
     'exact_feature_collisions_verified':True,'finite_set_unigram_accuracy_ceiling':.6}
 assert bs['all']['accuracy']<=.6
 attempts=[x for p in sorted((ROOT/'data/raw_runs').glob('*/attempts.jsonl')) for x in load(p)]
 challengeattempts=[x for x in attempts if x.get('dataset') in ['reviewer_binding','reviewer_binding_v2']]
 initial=load(ROOT/'data/analysis/reviewer_binding_initial_planned.jsonl')
 old_by={(r['model'],r['item']['item_id']):r for r in initial}
 sensitivity=[]
 for m in protocol['models']:
  nr=[r for r in rows if r['model']==m and r['item']['knowledge']=='nonce']
  oldrows=[old_by[(m,r['item']['item_id'])] for r in nr]
  assert len(nr)==len(oldrows)==240
  assert all(a['item']['gold']==b['item']['gold'] and a['item']['compatible_histories']==b['item']['compatible_histories'] for a,b in zip(nr,oldrows))
  sensitivity.append({'model':m,'paired_n':240,'initial_correct':sum(r['correct'] for r in oldrows),'precise_definition_correct':sum(r['correct'] for r in nr),
    'judgment_disagreements':sum(a['parsed']['judgment']!=b['parsed']['judgment'] for a,b in zip(nr,oldrows)),
    'scope':'Complete paired text-definition sensitivity; includes service/order variation; no inferential tests.'})
 report={'analysis_status':'post-review supplementary, not original primary or secondary test family','planned_cells':5040,'transport_missing':0,
  'parse_invalid':sum(r.get('parsed') is None for r in rows),'results':results,'cells':cells,'per_lemma':lemmas,'per_stratum':strata,'surface_baseline':bs,'definition_precision_pairs':sensitivity,
  'collection':{'all_retained_probe_and_main_responses':len(allresponses),'main_exact_payloads':5040,'main_extra_same_payload_responses':sum(j['request_id'] in set(duplicates) for j in jobs),
   'deduplication':'earliest started_utc per exact payload, irrespective of judgment/correctness','main_selected_source_counts':dict(Counter(r['source'] for r in rows)),
   'challenge_attempts_including_probe':len(challengeattempts),'returned_known_usd':sum(x['charged_or_reserved_usd'] for x in challengeattempts if not x['cost_is_estimate']),
   'recorded_conservative_usd':sum(x['charged_or_reserved_usd'] for x in challengeattempts),'project_recorded_conservative_usd':sum(x['charged_or_reserved_usd'] for x in attempts),
   'interrupted_probe_unrecorded_calls_upper_bound':16,'unrecorded_call_reserve_usd':.02,
   'budget_check_with_interruption_reserve':sum(x['charged_or_reserved_usd'] for x in challengeattempts)+.02<1.25},
  'source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'reports/reviewer_binding_protocol.json',ROOT/'reports/reviewer_binding_definition_protocol.json',ROOT/'data/supplementary/reviewer_binding_v2.jsonl',ROOT/'src/event_completion/runner_binding.py',ROOT/'scripts/analyze_binding_challenge.py']},
  'bootstrap':'10000 percentile draws of 12 lemma blocks, seed20271009; split intervals6blocks; no p-values or new primary designation'}
 (ROOT/'reports/reviewer_binding_results.json').write_text(json.dumps(report,indent=2)+'\n')
 names=['Qwen8','Llama8','Ministral8','Gemma12','Qwen14','Qwen32','DeepSeek']
 table=r'''\begin{table}[t]
\centering
\caption{Post-review role-binding challenge (percent). Each system has 720 cells; R/N/M each 240. All uses all cells; CI is the 12-lemma bootstrap interval. Pair is both-correct recall on 288 pairs with different gold. Any deterministic word-unigram classifier has a 60\% accuracy ceiling and 0\% Pair.}
\label{tab:binding}
\setlength{\tabcolsep}{2.5pt}
\begin{tabular}{lrrrrr}
\toprule
System & R & N & M & All [95\% CI] & Pair\\
\midrule
'''
 for name,r in zip(names,results):
  by=r['by_presentation'];a=r['all'];lo,hi=a['accuracy_ci95_lemma_bootstrap']
  table+=name+' & '+' & '.join(f"{100*by[k]['accuracy']:.1f}" for k in ['real','nonce','micro'])+f" & {100*a['accuracy']:.1f} [{100*lo:.1f},{100*hi:.1f}] & {100*r['different_gold_pair_both_correct']['rate']:.1f}"+r' \\'+'\n'
 table+='Unigram & '+' & '.join(f"{100*bs['by_presentation'][k]['accuracy']:.1f}" for k in ['real','nonce','micro'])+f" & {100*bs['all']['accuracy']:.1f} & 0.0"+r' \\'+'\n'+r'\bottomrule'+'\n'+r'\end{tabular}'+'\n'+r'\end{table}'+'\n'
 (ROOT/'paper/tables/reviewer_binding.tex').write_text(table)
 print(json.dumps({'results':[{'model':r['model'],'all':r['all']['accuracy'],'R':r['by_presentation']['real']['accuracy'],'N':r['by_presentation']['nonce']['accuracy'],'M':r['by_presentation']['micro']['accuracy'],'pair':r['different_gold_pair_both_correct']['rate']} for r in results],'baseline':bs['all']['accuracy'],'cost':report['collection']},indent=2))
if __name__=='__main__':main()
