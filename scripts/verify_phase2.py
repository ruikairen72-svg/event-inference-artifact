"""Offline consistency checks for research planning; these are not experiments."""
from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parents[1]/'data/frozen/phase2_design_snapshot'
reports=['literature_review','benchmark_audit','track_selection','study_blueprint','model_selection','cost_plan','risk_register']
assert all((ROOT/'reports'/(x+'.md')).stat().st_size>1000 for x in reports)
p=json.loads((ROOT/'config/study_protocol_candidate.json').read_text())
c=json.loads((ROOT/'reports/cost_arithmetic.json').read_text())
a=json.loads((ROOT/'reports/original_audit.json').read_text())
assert p['inference_calls_made']==p['new_human_annotations']==0
assert len(p['main_models'])==6 and len(p['stress_model'])==1
assert p['confirmatory_families']*len(p['composition'])*len(p['knowledge'])*len(p['context'])==2160
assert p['robustness_families']*2*3*2*len(p['robustness_variants'])==1728
assert sum(r['requests'] for r in c['rows'])==31516
assert c['contingency_25pct_usd']<p['total_target_usd']
assert a['n']==400 and a['critique_vss_exclusions']==97 and a['critique_no_explicit_noncompletion']==76
assert a['data_blob_unchanged_since_initial']
for manifest in [ROOT/'phase2.sha256']:
 for row in manifest.read_text().splitlines():
  expected,filename=row.split('  ',1)
  assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()==expected, filename
print('PASS: historical Phase 2 snapshot reports, protocol/cost arithmetic, original provenance and SHA-256 manifest. The historical snapshot had no inference; current continuation does.')
