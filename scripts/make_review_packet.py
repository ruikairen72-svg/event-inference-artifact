"""Create blind human review forms, without prefilled opinions or gold labels."""
from pathlib import Path
import json,csv,hashlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/human_review';OUT.mkdir(parents=True,exist_ok=True)
def load(name):return [json.loads(x) for x in (ROOT/f'data/generated/{name}.jsonl').read_text().splitlines()]
rows=load('pilot_core')+load('main_core')
fields=['item_id','family_id','split','premise','hypothesis','reviewer_id','acceptable_labels','preferred_label','vp_has_required_endpoint','grammar_ok','ambiguous_reading','notes']
with (OUT/'semantic_review_blank.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for r in rows:w.writerow({k:r.get(k,'') if k in ['item_id','family_id','split','premise','hypothesis'] else '' for k in fields})
prior=[r for r in load('pilot_prior')+load('main_prior') if r['context']=='neutral']
fields=['item_id','family_id','premise','hypothesis','reviewer_id','target_probability_0_to_1','required_endpoint_unchanged','notes']
with (OUT/'prior_ratings_blank.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for r in prior:w.writerow({k:r.get(k,'') if k in ['item_id','family_id','premise','hypothesis'] else '' for k in fields})
# Curated family layout makes the key contrasts reviewable without prefilled labels.
lines=['# Candidate matched families — blind review layout','', 'No independent human judgments have been recorded. Each entry shows the Real minimal contrast and outcome context, plus its Nonce and Micro translations. Respond in the blank semantic/prior CSV files; do not infer gold from file order.','']
by={}
for r in rows:by.setdefault(r['family_id'],[]).append(r)
for fid,rr in sorted(by.items()):
 lines+=['## '+fid+' ('+rr[0]['split']+')','']
 for knowledge in ['real','nonce','micro']:
  lines+=['### '+knowledge,'']
  for r in sorted([x for x in rr if x['knowledge']==knowledge],key=lambda x:(x['composition'],x['context'])):
   lines+=['**'+r['item_id']+'**',r['premise'],'Target: '+r['hypothesis'],'']
(OUT/'family_review.md').write_text('\n'.join(lines))
print('Blank forms:',len(rows),'semantic items;',len(prior),'neutral prior variants; no judgments prefilled.')
