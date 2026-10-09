"""Offline cost arithmetic from saved public prices; never calls inference."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
models=json.loads((ROOT/'config/models_candidate.json').read_text())['models']
counts={'main_core':2160,'original_replication':400,'world_prior':240,'label_controls':60,'robustness_six_variants':1728,'real_definition_control':288}
rows=[]
for i,m in enumerate(models):
 n=660 if m['tier']=='stress' else sum(counts.values())
 if i<2: n+=800
 a,b=m['input_usd_per_million'],m['output_usd_per_million']
 rows.append({'model':m['id'],'input_per_million':a,'output_per_million':b,'requests':n,'expected_usd':n*(750*a+128*b)/1e6,'conservative_usd':n*(1200*a+512*b)/1e6})
total=sum(r['expected_usd'] for r in rows); upper=sum(r['conservative_usd'] for r in rows)
result={'per_main_counts':counts,'rows':rows,'requests':sum(r['requests'] for r in rows),'expected_usd':total,'conservative_usd':upper,'contingency_25pct_usd':upper*1.25,'pilot_conservative_usd':sum(800*(1200*m['input_usd_per_million']+512*m['output_usd_per_million'])/1e6 for m in models[:2])}
assert result['contingency_25pct_usd']<10
(ROOT/'reports/cost_arithmetic.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
