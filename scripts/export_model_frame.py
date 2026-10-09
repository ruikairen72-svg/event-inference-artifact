from pathlib import Path
import sys,json,csv
p=Path(sys.argv[1]);rows=[json.loads(l) for l in p.read_text().splitlines()];out=Path(sys.argv[2])
keys=['model','dataset','family_id','verb','composition','knowledge','context','stratum','template','prior','correct','q','missing','parse_valid']
with out.open('w') as f:
 w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
 for r in rows:
  if r['dataset'] not in ['main_core','main_prior']:continue
  i=r['item'];d={k:i.get(k) for k in keys};d.update(model=r['model'],dataset=r['dataset'],correct=int(bool(r.get('correct'))),q=(r.get('parsed') or {}).get('hypothesis_probability'),missing=int(bool(r.get('missing'))),parse_valid=int(r.get('parsed') is not None));w.writerow(d)
print('Exported all-planned model frame.')
