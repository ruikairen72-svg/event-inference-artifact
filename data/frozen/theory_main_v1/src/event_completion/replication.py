"""Original-gold accuracy and True-bias rates; disputed gold remains untouched."""
from collections import defaultdict,Counter
from .analysis import ROOT,load

def metrics(rows):
 flags={r['id']:r for r in load(ROOT/'data/original/disputed_items.jsonl')};models=sorted({r['model'] for r in rows});out=[]
 for model in models:
  mm=[r for r in rows if r['model']==model and r['dataset']=='original']
  for subset in ['original_400','published_vss_303','A_explicit_noncompletion_24']:
   rr=[r for r in mm if subset=='original_400' or (subset=='published_vss_303' and not flags[r['item_id']]['critique_vss_exclusion']) or (subset=='A_explicit_noncompletion_24' and r['item_id'].startswith('A_') and not flags[r['item_id']]['critique_no_explicit_noncompletion'])]
   by=defaultdict(list)
   for r in rr:by[r['item']['group'][0]].append(r)
   for group,gg in sorted(by.items()):
    valid=[r for r in gg if r.get('parsed')];n=len(gg);entailed=sum(r['parsed']['judgment']=='entailed' for r in valid)
    out.append({'model':model,'subset':subset,'group':group,'planned_n':n,'parse_valid_n':len(valid),'accuracy_original_gold_all_planned':sum(bool(r.get('correct')) for r in gg)/n,'true_rate_all_planned':entailed/n,'true_rate_valid':entailed/len(valid) if valid else None,'tbr_applicable':group in ['A','C'],'predicted_labels_valid':dict(Counter(r['parsed']['judgment'] for r in valid)),'gold_unchanged':True,'independent_new_human_validation':False})
 return out
