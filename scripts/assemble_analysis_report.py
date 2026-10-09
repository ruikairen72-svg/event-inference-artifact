"""Dataset-separated descriptions from real planned outcomes, no simulated rows."""
from pathlib import Path
import sys,json,collections,statistics,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from event_completion.analysis import summary,load
from event_completion.replication import metrics
subprocess.run([sys.executable,str(ROOT/'scripts/analyze_secondary.py')],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/audit_stimulus_wording.py')],check=True)
main=load(ROOT/'data/analysis/main_planned.jsonl');stress=load(ROOT/'data/analysis/stress_planned.jsonl');primary=json.loads((ROOT/'reports/primary_results.json').read_text());data=main+stress
stats=[]
for m in sorted({r['model'] for r in data}):
 for ds in sorted({r['dataset'] for r in data if r['model']==m}):
  rr=[r for r in data if r['model']==m and r['dataset']==ds];valid=[r for r in rr if r.get('parsed')];labels=sorted({r['item']['gold'] for r in rr})
  stats.append({'model':m,'dataset':ds,'planned':len(rr),'transport_missing':sum(r.get('missing',False) for r in rr),'parse_valid':len(valid),'accuracy_all_planned':sum(bool(r.get('correct')) for r in rr)/len(rr),'accuracy_parse_valid':sum(bool(r.get('correct')) for r in valid)/len(valid) if valid else None,'macro_label_accuracy':statistics.mean(sum(bool(r.get('correct')) for r in rr if r['item']['gold']==g)/sum(r['item']['gold']==g for r in rr) for g in labels),'source_run_counts':dict(collections.Counter(r.get('source_run','missing') for r in rr)),'gold_counts':dict(collections.Counter(r['item']['gold'] for r in rr)),'cells':summary(rr)})
replication=metrics(main)
attempts=[a for f in (ROOT/'data/raw_runs').glob('*/attempts.jsonl') for a in load(f)]
report={'claim_status':'theory-derived operational evaluation, not human validated','externally_preregistered':False,'datasets':stats,'secondary_report':'reports/secondary_results.json','original_replication':replication,'primary':primary,'known_returned_cost_usd':sum(a['charged_or_reserved_usd'] for a in attempts if not a['cost_is_estimate']),'conservative_ledger_usd':sum(a['charged_or_reserved_usd'] for a in attempts),'analysis_source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'data/analysis/main_planned.jsonl',ROOT/'data/analysis/stress_planned.jsonl']}}
(ROOT/'reports/analysis_results.json').write_text(json.dumps(report,indent=2)+'\n')
lines=['# Main analysis results','',report['claim_status']+'. Local freeze is not external preregistration. All tables use real planned responses; no generated prediction is an observation.','',f'Known returned cost: ${report["known_returned_cost_usd"]:.6f}; conservative ledger: ${report["conservative_ledger_usd"]:.6f}. Unknown-charge attempts are reserved, not assumed free.','','| Model | Dataset | Planned | Missing | Parse valid | All-planned accuracy | Macro label accuracy |','|---|---|---:|---:|---:|---:|---:|']
for r in stats:lines.append(f'| {r["model"]} | {r["dataset"]} | {r["planned"]} | {r["transport_missing"]} | {r["parse_valid"]} | {r["accuracy_all_planned"]:.4f} | {r["macro_label_accuracy"]:.4f} |')
lines+=['','## Prespecified 30-test family','','Paired family contrasts, lexical-block sign flips, Holm correction across all five contrasts × six main systems. Values in q units or accuracy units; q is uncalibrated subjective target truth. Complete-pair counts and adverse missing-q bounds are retained in the JSON.','','| Model | Contrast | Valid/planned families | Estimate | Cluster CI95 | p Holm |','|---|---|---:|---:|---|---:|']
for r in primary['results']:
 x=r['result'];ci='NA' if not x else f'[{x["ci95"][0]:.4f}, {x["ci95"][1]:.4f}]';estimate='NA' if not x else f'{x["estimate"]:.4f}';p='NA' if r['p_holm_30'] is None else f'{r["p_holm_30"]:.6g}'
 lines.append(f'| {r["model"]} | {r["metric"]} | {r["valid_pairs_or_rule_families"]}/{r["planned_families"]} | {estimate} | {ci} | {p} |')
lines+=['','Do not interpret a probability difference with correct categorical labels as a logical error. Layer contrasts also change definitions/notation/length. Intended-prior effects lack human ratings and remain exploratory. Rule and robustness conditions are not pooled into baseline cell accuracy. Source/filter details and unchanged original-gold outcomes are in `analysis_results.json`; mixed-model convergence is reported separately.']
(ROOT/'reports/analysis_results.md').write_text('\n'.join(lines)+'\n');print('Dataset-separated empirical report written.')
