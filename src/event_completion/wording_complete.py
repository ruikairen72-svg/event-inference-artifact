"""Deterministic inherited-defect counterparts, preserving original task variants."""
from .wording import REPAIRS
from .semantics import gold
MAIN_DATASETS=['main_core','main_prior','label_order','template_ood','name','label_only','natural_rule','structural_rule','real_definition']
STRESS_DATASETS=['stress_core','stress_prior']
def generate_rows(root,datasets):
 import json
 out=[]
 for dataset in datasets:
  for line in (root/f'data/generated/{dataset}.jsonl').read_text().splitlines():
   row={**json.loads(line),'dataset':dataset,'original':False}
   hits=[a for a in REPAIRS if a in row['premise']]
   if not hits:continue
   assert len(hits)==1 and row['gold']==gold(row['state']['admissible_histories'],row['composition'])=='contradicted'
   out.append({**row,'item_id':row['item_id']+':complete_participle_repair',
     'premise':row['premise'].replace(hits[0],REPAIRS[hits[0]]),
     'wording_baseline_dataset':dataset,'wording_baseline_item_id':row['item_id']})
 return sorted(out,key=lambda r:(r['wording_baseline_dataset'],r['wording_baseline_item_id']))
