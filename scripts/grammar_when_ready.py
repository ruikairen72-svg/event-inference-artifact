"""Sequential supplementary owner: no calls until the existing pipeline exits."""
from pathlib import Path
from types import SimpleNamespace
import sys,os,time,json,fcntl,subprocess,hashlib,datetime,statistics
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from event_completion.runner_main import make_jobs,load,all_spend
MODELS=','.join(json.loads((ROOT/'config/study_protocol_candidate.json').read_text())['main_models'])
lock=(ROOT/'.runtime/grammar.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
def state(stage,**kw):
 (ROOT/'reports/grammar_progress.json').write_text(json.dumps({'stage':stage,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),**kw},indent=2)+'\n')
def pending():
 done={r['request_id'] for p in (ROOT/'data/raw_runs').glob('*/responses.jsonl') for r in load(p) if r.get('transport_ok')}
 return {j['request_id'] for j in make_jobs(SimpleNamespace(datasets='grammar_repair',models=MODELS,items_per_model=None))}-done
try:
 state('waiting_existing_pipeline',wait_pid=1604)
 while True:
  try:current=json.loads((ROOT/'reports/pipeline_progress.json').read_text())
  except (FileNotFoundError,json.JSONDecodeError):
   time.sleep(10);continue
  if current['stage']=='pipeline_failed':raise RuntimeError('Existing main/stress pipeline failed')
  try:os.kill(1604,0);alive=True
  except ProcessLookupError:alive=False
  if not alive:
   if current['stage']!='analysis_complete_manuscript_revision_pending':raise RuntimeError('Unexpected pipeline exit')
   break
  time.sleep(10)
 with (ROOT/'reports/grammar_execution.log').open('a',buffering=1) as log:
  for invocation in range(3):
   missing=pending()
   if not missing or all_spend()>=8.99:break
   state('collecting_supplementary_grammar',pending_unique=len(missing),invocation=invocation)
   subprocess.run([sys.executable,str(ROOT/'scripts/run_recovery.py'),'--run-id','grammar_v1','--datasets','grammar_repair','--models',MODELS,'--concurrency','4','--cap','.5'],stdout=log,stderr=log,check=True)
  subprocess.run([sys.executable,str(ROOT/'scripts/collect_main_rows.py'),'--datasets','grammar_repair','--models',MODELS,'--output','data/analysis/grammar_repair_planned.jsonl'],stdout=log,stderr=log,check=True)
 baseline=load(ROOT/'data/analysis/main_planned.jsonl');corrected=load(ROOT/'data/analysis/grammar_repair_planned.jsonl')
 assert len(corrected)==180
 index={(r['model'],r['item']['item_id']):r for r in baseline if r['dataset']=='main_core'}
 reports=[]
 for model in MODELS.split(','):
  pairs=[(index[(model,r['item']['grammar_repair_baseline_item_id'])],r) for r in corrected if r['model']==model]
  assert len(pairs)==30
  differences=[];disagreement=0;valid_labels=0
  for original,repaired in pairs:
   assert original['item']['gold']==repaired['item']['gold']
   a=original.get('parsed') or {};b=repaired.get('parsed') or {}
   if a and b:valid_labels+=1;disagreement+=a['judgment']!=b['judgment']
   if a.get('hypothesis_probability') is not None and b.get('hypothesis_probability') is not None:
    differences.append(b['hypothesis_probability']-a['hypothesis_probability'])
  acc=lambda pos:sum(bool(pair[pos].get('correct')) for pair in pairs)/len(pairs)
  reports.append({'model':model,'planned_pairs':30,'original_accuracy_all_planned':acc(0),
    'corrected_accuracy_all_planned':acc(1),'paired_accuracy_change':acc(1)-acc(0),
    'corrected_transport_missing':sum(pair[1].get('missing',False) for pair in pairs),
    'corrected_parse_valid':sum(bool(pair[1].get('parsed')) for pair in pairs),
    'valid_label_pairs':valid_labels,'judgment_disagreements':disagreement,
    'valid_q_pairs':len(differences),'mean_corrected_minus_original_q':statistics.mean(differences) if differences else None})
 attempts=[r for p in (ROOT/'data/raw_runs').glob('*/attempts.jsonl') for r in load(p)]
 result={'status':'post-freeze descriptive paired wording control, not confirmatory inference',
  'primary_unchanged':True,'results':reports,'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'data/analysis/main_planned.jsonl',ROOT/'data/analysis/grammar_repair_planned.jsonl']},
  'final_known_returned_project_cost_usd':sum(r['charged_or_reserved_usd'] for r in attempts if not r['cost_is_estimate']),
  'final_conservative_project_ledger_usd':all_spend(),
  'limitation':'Later requests and service variability confound pure causal wording attribution. Original failed/malformed responses are retained. No new p-values.'}
 (ROOT/'reports/grammar_repair_sensitivity.json').write_text(json.dumps(result,indent=2)+'\n')
 state('grammar_analysis_complete',missing_unique=len(pending()),submission_ready=False)
except Exception as error:
 state('grammar_pipeline_failed',error=type(error).__name__+': '+str(error));raise
