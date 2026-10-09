"""Write a new-stage audit manifest without rewriting historical checkpoints."""
from pathlib import Path
import argparse,hashlib
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--phase',required=True,choices=['3','4','5']);a=p.parse_args()
if a.phase=='3':
 roots=['src','tests','scripts','config','data/generated','data/human_review','data/human_review_instructions.md','reports/data_audit.md','reports/data_validation.json','reports/amendments.md','reports/design_resolution_simulation.json','reports/scheduling_audit.json']
elif a.phase=='4':
 roots=['data/raw_runs/pilot_v1','data/raw_runs/pilot_v2','data/analysis/pilot_v2_planned.jsonl','reports/pilot_v1_summary.json','reports/pilot_v2_summary.json','reports/pilot_report.md','figures','.research/figures']
else:
 roots=['src','tests','scripts','config','data/generated','reports/amendments.md']
paths=set()
for rel in roots:
 q=ROOT/rel
 if q.is_file():paths.add(q)
 elif q.is_dir():paths.update(x for x in q.rglob('*') if x.is_file() and '__pycache__' not in x.parts)
out=ROOT/f'reports/phase{a.phase}.sha256'
if out.exists():raise SystemExit('Checkpoint already exists: preserve it; make a dated new checkpoint instead.')
out.write_text(''.join(hashlib.sha256(q.read_bytes()).hexdigest()+'  '+str(q.relative_to(ROOT))+'\n' for q in sorted(paths)))
print('Files checkpointed:',len(paths))
