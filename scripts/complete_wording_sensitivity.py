"""Post-analysis complete inherited-participle diagnostic, no new effect tests."""
from pathlib import Path
from types import SimpleNamespace
import sys,json,datetime,hashlib,fcntl,subprocess,statistics
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from event_completion.runner_main import load,make_jobs,all_spend
from event_completion.wording import REPAIRS
from event_completion.semantics import gold
lock=(ROOT/'.runtime/grammar_complete.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
assert json.loads((ROOT/'reports/pipeline_progress.json').read_text())['stage']=='analysis_complete_manuscript_revision_pending'
assert json.loads((ROOT/'reports/grammar_progress.json').read_text())['stage']=='grammar_analysis_complete'
models=json.loads((ROOT/'config/study_protocol_candidate.json').read_text())['main_models']
main=load(ROOT/'data/analysis/main_planned.jsonl');stress=load(ROOT/'data/analysis/stress_planned.jsonl')
source_datasets=['main_core','main_prior','label_order','template_ood','name','label_only','natural_rule','structural_rule','real_definition']
def corrected(items,datasets):
 out=[]
 for r in items:
  if r['dataset'] not in datasets:continue
  row=r['item'];hits=[a for a in REPAIRS if a in row['premise']]
  if not hits:continue
  assert len(hits)==1 and row['gold']==gold(row['state']['admissible_histories'],row['composition'])=='contradicted'
  out.append({**row,'item_id':row['item_id']+':complete_participle_repair',
    'premise':row['premise'].replace(hits[0],REPAIRS[hits[0]]),
    'wording_baseline_dataset':r['dataset'],'wording_baseline_item_id':row['item_id']})
 # Preserve original variant: label-only/order/rule instructions remain identical.
 return sorted(out,key=lambda r:(r['wording_baseline_dataset'],r['wording_baseline_item_id']))
inputs=[r for r in main if r['model']==models[0]]
a=corrected(inputs,source_datasets);b=corrected(stress,['stress_core','stress_prior'])
assert len(a)==83 and len(b)==20
for name,rows in [('grammar_complete_main',a),('grammar_complete_stress',b)]:
 (ROOT/f'data/generated/{name}.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
segments=[('grammar_complete_main',','.join(models),'grammar_complete_main_planned.jsonl'),('grammar_complete_stress','deepseek/deepseek-v3.2','grammar_complete_stress_planned.jsonl')]
jobs=[j for ds,mm,_ in segments for j in make_jobs(SimpleNamespace(datasets=ds,models=mm,items_per_model=None))]
done={r['request_id'] for p in (ROOT/'data/raw_runs').glob('*/responses.jsonl') for r in load(p) if r.get('transport_ok')}
design={'declared_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Post-analysis extension to every inherited defect in the formal main/stress suites; descriptive only. Initial 30-core repair remains separately predeclared. No model/item selection based on answers, no new p-values, no replacement of original estimates.', 'planned_cells':len(jobs),'unique_payloads':len({j['request_id'] for j in jobs}),'pending_unique_before_calls':len({j['request_id'] for j in jobs}-done),'source_counts':{'main_per_model':83,'stress':20},'original_variant_preserved':True,'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'data/analysis/main_planned.jsonl',ROOT/'data/analysis/stress_planned.jsonl',ROOT/'data/generated/grammar_complete_main.jsonl',ROOT/'data/generated/grammar_complete_stress.jsonl',Path(__file__)]},'budget_cap_usd':.5}
(ROOT/'reports/grammar_complete_design.json').write_text(json.dumps(design,indent=2)+'\n')
def state(stage,**kw):(ROOT/'reports/grammar_complete_progress.json').write_text(json.dumps({'stage':stage,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),**kw},indent=2)+'\n')
def pending(ds,mm):
 cache={r['request_id'] for p in (ROOT/'data/raw_runs').glob('*/responses.jsonl') for r in load(p) if r.get('transport_ok')}
 return {j['request_id'] for j in make_jobs(SimpleNamespace(datasets=ds,models=mm,items_per_model=None))}-cache
try:
 with (ROOT/'reports/grammar_complete_execution.log').open('a',buffering=1) as log:
  for ds,mm,out in segments:
   for invocation in range(3):
    missing=pending(ds,mm)
    if not missing or all_spend()>=8.99:break
    state('collecting_inherited_participle_control',dataset=ds,pending=len(missing),invocation=invocation)
    subprocess.run([sys.executable,str(ROOT/'scripts/run_recovery.py'),'--run-id','grammar_complete_v2','--datasets',ds,'--models',mm,'--concurrency','4','--cap','.5'],stdout=log,stderr=log,check=True)
   subprocess.run([sys.executable,str(ROOT/'scripts/collect_main_rows.py'),'--datasets',ds,'--models',mm,'--output','data/analysis/'+out],stdout=log,stderr=log,check=True)
 rows=load(ROOT/'data/analysis/grammar_complete_main_planned.jsonl')+load(ROOT/'data/analysis/grammar_complete_stress_planned.jsonl');assert len(rows)==518
 index={(r['model'],r['dataset'],r['item']['item_id']):r for r in main+stress};groups={}
 for r in rows:
  original=index[r['model'],r['item']['wording_baseline_dataset'],r['item']['wording_baseline_item_id']]
  assert original['item']['gold']==r['item']['gold'] and original['item']['hypothesis']==r['item']['hypothesis'] and original['item']['variant']==r['item']['variant']
  groups.setdefault((r['model'],original['dataset']),[]).append((original,r))
 result=[]
 for (model,dataset),pairs in sorted(groups.items()):
  qdiff=[r['parsed']['hypothesis_probability']-o['parsed']['hypothesis_probability'] for o,r in pairs if r.get('parsed') and 'hypothesis_probability' in r['parsed'] and 'hypothesis_probability' in o['parsed']]
  acc=lambda pos:sum(bool(pair[pos].get('correct')) for pair in pairs)/len(pairs)
  result.append({'model':model,'source_dataset':dataset,'planned_pairs':len(pairs),'original_accuracy':acc(0),'repaired_accuracy':acc(1),'paired_accuracy_change':acc(1)-acc(0),'valid_label_pairs':sum(bool(r.get('parsed')) for o,r in pairs),'judgment_disagreements':sum(o['parsed']['judgment']!=r['parsed']['judgment'] for o,r in pairs if r.get('parsed')),'q_pairs':len(qdiff),'mean_q_change':statistics.mean(qdiff) if qdiff else None,'source_run_counts':dict(__import__('collections').Counter(r.get('source_run','missing') for o,r in pairs))})
 attempts=[r for p in (ROOT/'data/raw_runs').glob('*/attempts.jsonl') for r in load(p)]
 report={'scope':design['scope'],'planned_pairs':len(rows),'parse_valid':sum(bool(r.get('parsed')) for r in rows),'transport_missing':sum(r.get('missing',False) for r in rows),'results':result,'final_known_returned_project_cost_usd':sum(r['charged_or_reserved_usd'] for r in attempts if not r['cost_is_estimate']),'final_conservative_project_ledger_usd':all_spend(),'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'data/analysis/grammar_complete_main_planned.jsonl',ROOT/'data/analysis/grammar_complete_stress_planned.jsonl']},'limitation':'Later calls/service variation limit causal wording attribution; corrected core cache reuses the initial repair calls. No new inferential tests.'}
 (ROOT/'reports/grammar_complete_sensitivity.json').write_text(json.dumps(report,indent=2)+'\n');state('complete',planned=518,missing=sum(r.get('missing',False) for r in rows))
 print(json.dumps({'planned':518,'parse_valid':report['parse_valid'],'known_cost':report['final_known_returned_project_cost_usd'],'ledger':all_spend()},indent=2))
except Exception as e:state('failed',error=type(e).__name__+': '+str(e));raise
