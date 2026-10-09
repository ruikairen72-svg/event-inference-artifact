"""One sequential owner: wait collection, recover transport, stress, then analysis."""
from pathlib import Path
import sys,os,time,json,subprocess,argparse,fcntl,datetime
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from event_completion.runner_main import make_jobs,load,all_spend
MODELS='qwen/qwen3-8b,meta-llama/llama-3.1-8b-instruct,mistralai/ministral-8b-2512,google/gemma-3-12b-it,qwen/qwen3-14b,qwen/qwen3-32b'
DATASETS='original,main_core,main_prior,main_labels,label_order,template_ood,name,label_only,natural_rule,structural_rule,real_definition'
p=argparse.ArgumentParser();p.add_argument('--wait-pid',required=True,type=int);a=p.parse_args()
lockfile=(ROOT/'.runtime/pipeline.lock').open('w')
fcntl.flock(lockfile,fcntl.LOCK_EX|fcntl.LOCK_NB)
log=(ROOT/'reports/pipeline_execution.log').open('a',buffering=1)
def state(stage,**extra):
 (ROOT/'reports/pipeline_progress.json').write_text(json.dumps({'stage':stage,'pid':os.getpid(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),**extra},indent=2)+'\n')
def run(args,env=None):
 log.write('\n'+str(args)+'\n');log.flush();subprocess.run(args,cwd=ROOT.parent,stdout=log,stderr=log,check=True,env=env)
def pending(datasets,models):
 done={r['request_id'] for f in (ROOT/'data/raw_runs').glob('*/responses.jsonl') for r in load(f) if r.get('transport_ok')}
 return {j['request_id'] for j in make_jobs(SimpleNamespace(datasets=datasets,models=models,items_per_model=None))}-done
def recover(run_id,datasets,models,cap):
 for attempt in range(3):
  missing=pending(datasets,models)
  if not missing or all_spend()>=8.99:break
  state('collect_'+run_id,pending_unique=len(missing),invocation=attempt)
  run([sys.executable,str(ROOT/'scripts/run_recovery.py'),'--run-id',run_id,'--datasets',datasets,'--models',models,'--concurrency','4','--cap',str(cap)])
 return len(pending(datasets,models))
try:
 while True:
  try:os.kill(a.wait_pid,0)
  except ProcessLookupError:break
  state('waiting_existing_main',wait_pid=a.wait_pid);time.sleep(10)
 main_missing=recover('main_v1',DATASETS,MODELS,8.7)
 stress_missing=recover('stress_v1','stress_core,stress_prior','deepseek/deepseek-v3.2',2)
 state('materializing',main_missing=main_missing,stress_missing=stress_missing)
 for datasets,models,out in [(DATASETS,MODELS,'main'),('stress_core,stress_prior','deepseek/deepseek-v3.2','stress')]:
  run([sys.executable,str(ROOT/'scripts/collect_main_rows.py'),'--datasets',datasets,'--models',models,'--output',f'data/analysis/{out}_planned.jsonl'])
 state('primary_analysis')
 run([sys.executable,str(ROOT/'scripts/analyze_primary.py'),'--input',str(ROOT/'data/analysis/main_planned.jsonl'),'--protocol',str(ROOT/'config/study_protocol_frozen.json'),'--output',str(ROOT/'reports/primary_results.json')])
 run([sys.executable,str(ROOT/'scripts/export_model_frame.py'),str(ROOT/'data/analysis/main_planned.jsonl'),str(ROOT/'data/analysis/mixed_model_frame.csv')])
 state('mixed_models')
 env=dict(os.environ);env['R_LIBS_USER']=str(ROOT/'.runtime/Rlib')
 run(['Rscript',str(ROOT/'scripts/fit_mixed_models.R'),str(ROOT/'data/analysis/mixed_model_frame.csv'),str(ROOT/'reports/mixed_models.json')],env=env)
 run([sys.executable,str(ROOT/'scripts/assemble_analysis_report.py')])
 state('analysis_complete_manuscript_revision_pending',main_missing=main_missing,stress_missing=stress_missing,conservative_ledger_usd=all_spend())
except Exception as e:
 state('pipeline_failed',error=type(e).__name__+': '+str(e));raise
