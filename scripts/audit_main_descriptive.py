"""Reconcile early completed-main descriptions against official planned cells.

This audit adds no tests of effects and never changes observations or estimates.
"""
from pathlib import Path
from collections import Counter
import sys,json,math,statistics,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from event_completion.analysis import load,summary
from event_completion.replication import metrics
rows=load(ROOT/'data/analysis/main_planned.jsonl')
assert len(rows)==28104 and all(r.get('parsed') for r in rows)
desc=json.loads((ROOT/'reports/main_descriptive_results.json').read_text())
checks=0
def equal(a,b):
 global checks
 if isinstance(a,(int,float)) and not isinstance(a,bool):assert math.isclose(a,b,abs_tol=1e-12), (a,b)
 else:assert a==b,(a,b)
 checks+=1
for row in desc['core']:
 g=[r for r in rows if r['model']==row['model'] and r['dataset']=='main_core' and r['item']['knowledge']==row['knowledge']]
 equal(row['n'],len(g));equal(row['accuracy'],statistics.mean(bool(r['correct']) for r in g))
 recalls={gold:statistics.mean(bool(r['correct']) for r in g if r['item']['gold']==gold) for gold in ['entailed','contradicted','unknown']}
 for k,v in recalls.items():equal(row['gold_accuracy'][k],v)
 equal(row['macro_accuracy'],statistics.mean(recalls.values()))
cellkey=lambda x:tuple(x[k] for k in ['model','knowledge','composition','context'])
official={cellkey(x):x for x in summary([r for r in rows if r['dataset']=='main_core'])}
for c in desc['core_cells']:
 for k,v in c.items():equal(v,official[cellkey(c)][k])
for c in desc['label_controls']:
 g=[r for r in rows if r['model']==c['model'] and r['dataset']=='main_labels']
 equal(c['n'],len(g));equal(c['source_run_counts'],dict(Counter(r['source_run'] for r in g)))
 for gold,v in c['gold_correct'].items():equal(v,sum(bool(r['correct']) for r in g if r['item']['gold']==gold))
for c in desc['intended_prior']:
 g=[r for r in rows if r['model']==c['model'] and r['dataset']=='main_prior' and r['item']['context']==c['context']]
 pairs={}
 for r in g:pairs.setdefault(r['item']['family_id'],{})[r['item']['prior']]=r['parsed']['hypothesis_probability']
 equal(c['paired_families'],len(pairs));equal(c['mean_high_minus_low_q'],statistics.mean(v['high']-v['low'] for v in pairs.values()));equal(c['accuracy_all_planned'],statistics.mean(bool(r['correct']) for r in g))
for c in desc['robustness']:
 g=[r for r in rows if r['model']==c['model'] and r['dataset']==c['variant']]
 key=lambda r:tuple(r['item'][k] for k in ['family_id','knowledge','composition','context'])
 keys={key(r) for r in g};base=[r for r in rows if r['model']==c['model'] and r['dataset']=='main_core' and key(r) in keys]
 equal(c['n'],len(g));equal(len(base),len(g));a=statistics.mean(bool(r['correct']) for r in base);b=statistics.mean(bool(r['correct']) for r in g)
 equal(c['matched_baseline_accuracy'],a);equal(c['variant_accuracy'],b);equal(c['paired_accuracy_change'],b-a)
repkey=lambda r:tuple(r[k] for k in ['model','subset','group'])
rep={repkey(r):r for r in metrics(rows)}
for c in desc['original_replication']:
 for k,v in c.items():equal(v,rep[repkey(c)][k])
checkpoint=json.loads((ROOT/'reports/main_collection_complete_checkpoint.json').read_text())
for filename,wanted in checkpoint['main_raw_sha256'].items():equal(hashlib.sha256((ROOT/'data/raw_runs/main_v1'/filename).read_bytes()).hexdigest(),wanted)
authoring=json.loads((ROOT/'reports/main_authoring_primary.json').read_text())
primary=json.loads((ROOT/'reports/primary_results.json').read_text())
equal(authoring['results'],primary['results'])
equal(authoring['snapshot_sha256'],hashlib.sha256((ROOT/'data/analysis/main_planned.jsonl').read_bytes()).hexdigest())
report={'passed':True,'comparisons':checks,'planned_main_cells':len(rows),'scope':'Every early main descriptive estimate and original subset reconciles with official complete planned cells. The authoring snapshot is byte-identical to official main materialization and all 30 primary results match exactly. No new effect testing or deletion.', 'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'reports/main_descriptive_results.json',ROOT/'data/analysis/main_planned.jsonl']}}
(ROOT/'reports/main_descriptive_reconciliation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
