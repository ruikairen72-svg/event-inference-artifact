"""Technical collection diagnostics only; does not select semantic outcomes."""
from pathlib import Path
from collections import Counter,defaultdict
import json,math,statistics,hashlib
ROOT=Path(__file__).resolve().parents[1]
records=defaultdict(list);attempts=[]
for p in (ROOT/'data/raw_runs').glob('*/responses.jsonl'):
 if p.parent.name not in ['main_v1','stress_v1','grammar_v1','grammar_complete_v2']:continue
 with p.open() as f:
  for line in f:
   r=json.loads(line);records[(p.parent.name,r['model'])].append(r)
for p in (ROOT/'data/raw_runs').glob('*/attempts.jsonl'):
 with p.open() as f:attempts.extend(json.loads(line) for line in f)
summary=[]
for (run,model),rr in sorted(records.items()):
 usage=[r.get('usage') or {} for r in rr]
 prompt=[u['prompt_tokens'] for u in usage if isinstance(u.get('prompt_tokens'),(int,float))]
 output=[u['completion_tokens'] for u in usage if isinstance(u.get('completion_tokens'),(int,float))]
 reason=[u.get('completion_tokens_details',{}).get('reasoning_tokens') for u in usage]
 estimates=[math.ceil(len(json.dumps(r['payload']['messages']))/2)+100 for r in rr]
 comparisons=[(r.get('usage') or {})['prompt_tokens']<=e for r,e in zip(rr,estimates) if isinstance((r.get('usage') or {}).get('prompt_tokens'),(int,float))]
 summary.append({'run':run,'model':model,'successful_unique_calls':len(rr),'returned_model_counts':dict(Counter(str(r.get('returned_model')) for r in rr)),
 'provider_counts':dict(Counter(str(r.get('returned_provider')) for r in rr)),
 'finish_reason_counts':dict(Counter(str(r.get('finish_reason')) for r in rr)),
 'parse_status_counts':dict(Counter(r['parse_status'] for r in rr)),
 'prompt_tokens_mean':statistics.mean(prompt) if prompt else None,'prompt_tokens_max':max(prompt) if prompt else None,
 'completion_tokens_mean':statistics.mean(output) if output else None,'completion_tokens_max':max(output) if output else None,
 'reasoning_tokens_histogram':dict(Counter(str(v) for v in reason)),
 'observed_prompt_under_reservation_estimate':all(comparisons),'usage_comparisons':len(comparisons),
 'max_tokens_values':dict(Counter(r['payload']['max_tokens'] for r in rr)),
 'qwen_suffix_uniform':all(r['payload']['messages'][-1]['content'].endswith('/no_think') for r in rr) if model.startswith('qwen/qwen3-') else None,
 'fallback_disabled_uniform':all(r['payload']['provider']['allow_fallbacks'] is False for r in rr)})
report={'scope':'technical metadata on main/stress/grammar calls and the separately identified cached main label controls; not semantic results or independent invoice verification',
 'complete_collection':json.loads((ROOT/'reports/pipeline_progress.json').read_text())['stage']=='analysis_complete_manuscript_revision_pending' and json.loads((ROOT/'reports/grammar_progress.json').read_text())['stage']=='grammar_analysis_complete' and json.loads((ROOT/'reports/grammar_complete_progress.json').read_text())['stage']=='complete',
 'runs':summary,'known_returned_cost_usd':sum(a['charged_or_reserved_usd'] for a in attempts if not a['cost_is_estimate']),
 'conservative_ledger_usd':sum(a['charged_or_reserved_usd'] for a in attempts),
 'unknown_charge_attempts':sum(a['cost_is_estimate'] for a in attempts)}
cached=[json.loads(l) for l in (ROOT/'data/analysis/main_planned.jsonl').read_text().splitlines()]
cached=[r for r in cached if r['dataset']=='main_labels' and r['source_run']!='main_v1']
assert len(cached)==35 and len({r['request_id'] for r in cached})==35
report['cached_main_control_metadata']=[{'model':r['model'],'source_run':r['source_run'],'request_id':r['request_id'],'returned_model':r.get('returned_model'),'returned_provider':r.get('returned_provider'),'parse_status':r['parse_status'],'finish_reason':r.get('finish_reason'),'usage':r.get('usage'),'fallback_disabled':r['payload']['provider']['allow_fallbacks'] is False} for r in cached]
report['cached_control_parse_and_finish_checks']=all(r.get('parsed') and r.get('finish_reason')=='stop' and r['payload']['provider']['allow_fallbacks'] is False for r in cached)
(ROOT/'reports/run_metadata_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'systems':len(summary),'observed_prompt_estimates_cover_usage':all(r['observed_prompt_under_reservation_estimate'] for r in summary),'known_returned_cost_usd':report['known_returned_cost_usd'],'conservative_ledger_usd':report['conservative_ledger_usd'],'complete_collection':report['complete_collection']},indent=2))
