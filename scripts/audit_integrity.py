"""Read-only integrity audit; explicitly distinguishes pending deliverables."""
from pathlib import Path
import hashlib,json,re,datetime,collections,sys
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(name,ok,**detail):checks.append({'check':name,'pass':bool(ok),**detail})
for folder,manifest in [('phase2_design_snapshot','phase2.sha256'),('phase3_snapshot','phase3.sha256'),('phase4_snapshot','phase4.sha256'),('theory_main_v1','manifest.sha256'),('grammar_initial_v1','manifest.sha256')]:
 base=ROOT/'data/frozen'/folder; bad=[];n=0
 for line in (base/manifest).read_text().splitlines():
  wanted,relative=line.split(None,1);p=base/relative.strip();n+=1
  if not p.is_file() or sha(p)!=wanted:bad.append(relative)
 check('historical_snapshot_'+folder,not bad,files=n,mismatch_paths=bad)
# The collector, runtime settings, source stimuli and primary specification must
# still match the precollection freeze. Later reporting/secondary code may evolve.
base=ROOT/'data/frozen/theory_main_v1';required=[]
for line in (base/'manifest.sha256').read_text().splitlines():
 wanted,relative=line.split(None,1);relative=relative.strip()
 if relative.startswith('data/generated/') or relative in ['config/runtime_main.json','config/study_protocol_frozen.json','src/event_completion/runner_main.py','src/event_completion/primary.py']:
  required.append((relative,(ROOT/relative).is_file() and sha(ROOT/relative)==wanted))
check('active_frozen_inputs',all(ok for _,ok in required),files=len(required),mismatch_paths=[p for p,ok in required if not ok])
original=ROOT/'data/original/upstream/data/imperfectiveNLI.json'
check('original_gold_file_unchanged',sha(original)=='ddd01d06b18b9bab24abb5bc92a8eb740bb145123658fa9a10bd86e38b4bdb5a')
# Only report paths for credential hits, never matched strings or file contents.
pattern=re.compile(rb'sk-or-v1-[0-9a-f]{64}',re.I);hits=[]
for folder in ['src','scripts','config','reports','data','paper']:
 for p in (ROOT/folder).rglob('*'):
  if p.is_file() and p.suffix in ['.py','.R','.json','.jsonl','.txt','.md','.tex','.csv'] and pattern.search(p.read_bytes()):hits.append(str(p.relative_to(ROOT)))
check('no_openrouter_credential_in_research_files',not hits,hit_paths=hits)
seen={};duplicates=[];models=collections.Counter();providers=collections.Counter();parse=collections.Counter();finish=collections.Counter()
for p in (ROOT/'data/raw_runs').glob('*/responses.jsonl'):
 with p.open() as f:
  for line in f:
   r=json.loads(line);rid=r['request_id']
   if rid in seen:duplicates.append({'request_id':rid,'runs':[seen[rid],p.parent.name]})
   seen[rid]=p.parent.name
   if p.parent.name in ['main_v1','stress_v1']:
    models[r['model']]+=1;providers[str(r.get('returned_provider'))]+=1;parse[str(r['parse_status'])]+=1;finish[str(r.get('finish_reason'))]+=1
check('unique_successful_payload_cache',not duplicates,unique_responses=len(seen),duplicates=duplicates)
pending=[p for p in ['reports/analysis_results.json','reports/secondary_results.json','reports/mixed_models.json','reports/grammar_repair_sensitivity.json','reports/figure_progress.json','output/pdf/submission.pdf','reports/final_submission_audit.md'] if not (ROOT/p).exists()]
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'collection_diagnostics':{'model_transport_success_counts':dict(models),'providers':dict(providers),'parse_status':dict(parse),'finish_reasons':dict(finish)},'pending_artifacts':pending,'submission_ready':False,'note':'Integrity checks do not establish semantic population validity, final scientific interpretation or visual PDF quality.'}
(ROOT/'reports/integrity_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'passed':sum(c['pass'] for c in checks),'total_checks':len(checks),'failed':[c for c in checks if not c['pass']],'pending_artifacts':pending},indent=2))
if not all(c['pass'] for c in checks):sys.exit(1)
