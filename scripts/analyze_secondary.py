from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from event_completion.analysis import load,summary
from event_completion.secondary import analyze,family_only_ci
from event_completion.primary import extract
paths=[ROOT/'data/analysis/main_planned.jsonl',ROOT/'data/analysis/stress_planned.jsonl']
rows=sum((load(p) for p in paths),[])
assert len(rows)==28764,'Only complete planned materialization may be analyzed'
stress_families={r['item']['family_id'] for r in rows if r['dataset']=='stress_core'}
matched=[]
for model in sorted({r['model'] for r in rows}):
 rr=[r for r in rows if r['model']==model and r['dataset'] in ['main_core','stress_core'] and r['item']['family_id'] in stress_families]
 assert len(rr)==540,'Stress comparison must use the same 30 families for every system'
 matched.append({'model':model,'families':30,'planned_cells':540,'accuracy_all_planned':sum(bool(r.get('correct')) for r in rr)/540,'macro_label_accuracy':sum(sum(bool(r.get('correct')) for r in rr if r['item']['gold']==g)/sum(r['item']['gold']==g for r in rr) for g in ['entailed','contradicted','unknown'])/3,'parse_valid':sum(r.get('parsed') is not None for r in rr),'cells':summary(rr)})
family_sensitivity=[]
for model in sorted({r['model'] for r in rows if r['dataset']=='main_core'}):
 for metric,records in extract(rows,model).items():
  valid=[r['value'] for r in records if r['valid']]
  family_sensitivity.append({'model':model,'metric':metric,'planned_families':len(records),'valid_families':len(valid),'ci95_family_only':family_only_ci(valid),'designation':'descriptive sensitivity; lexical hierarchy remains primary'})
report={'primary_family_only_sensitivity':family_sensitivity,'matched_stress_core':matched,'status':'secondary diagnostics; no selection by outcome','draws':10000,'seed':20271007,
 'multiplicity':'BH within named secondary families across all named systems/contrasts; diagnostic disagreement has no inferential test',
 'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'results':analyze(rows)}
(ROOT/'reports/secondary_results.json').write_text(json.dumps(report,indent=2)+'\n')
print('Complete secondary diagnostic matrix written:',len(report['results']))
