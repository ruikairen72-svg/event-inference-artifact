"""Export complete evidence tables from finished analysis; no narrative inference."""
from pathlib import Path
import sys,json,csv,hashlib,collections,statistics
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from event_completion.analysis import load
from event_completion.primary import extract
state=json.loads((ROOT/'reports/pipeline_progress.json').read_text())
if state['stage']!='analysis_complete_manuscript_revision_pending':raise SystemExit('Wait for completed empirical analysis')
main=load(ROOT/'data/analysis/main_planned.jsonl');assert len(main)==28104
report=json.loads((ROOT/'reports/analysis_results.json').read_text());secondary=json.loads((ROOT/'reports/secondary_results.json').read_text());mixed=json.loads((ROOT/'reports/mixed_models.json').read_text())
out=ROOT/'paper/tables';out.mkdir(exist_ok=True)
def write(name,rows):
 keys=list(dict.fromkeys(k for r in rows for k in r))
 with (out/(name+'.csv')).open('w') as f:
  w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
  for r in rows:w.writerow({k:json.dumps(v,separators=(',',':')) if isinstance(v,(dict,list)) else v for k,v in r.items()})
models=json.loads((ROOT/'config/study_protocol_candidate.json').read_text())['main_models']
core=[];rep=[];controls=[];robust=[];tokens=[]
for m in models:
 rr=[r for r in main if r['model']==m]
 for k in ['real','nonce','micro']:
  g=[r for r in rr if r['dataset']=='main_core' and r['item']['knowledge']==k]
  d={'model':m,'knowledge':k,'planned':len(g),'parse_valid':sum(r.get('parsed') is not None for r in g),'accuracy':sum(bool(r.get('correct')) for r in g)/len(g)}
  for gold in ['entailed','contradicted','unknown']:
   gg=[r for r in g if r['item']['gold']==gold];d[gold+'_n']=len(gg);d[gold+'_accuracy']=sum(bool(r.get('correct')) for r in gg)/len(gg)
  d['macro_label_accuracy']=statistics.mean(d[x+'_accuracy'] for x in ['entailed','contradicted','unknown'])
  core.append(d)
 for gold in ['entailed','contradicted','unknown']:
  g=[r for r in rr if r['dataset']=='main_labels' and r['item']['gold']==gold]
  controls.append({'model':m,'gold':gold,'planned':len(g),'correct':sum(bool(r.get('correct')) for r in g),'parse_valid':sum(r.get('parsed') is not None for r in g),'source_run_counts':dict(collections.Counter(r.get('source_run','missing') for r in g)),'predicted_labels':dict(collections.Counter((r.get('parsed') or {}).get('judgment','missing_or_invalid') for r in g))})
 for subset in ['original_400','published_vss_303','A_explicit_noncompletion_24']:
  g=[r for r in report['original_replication'] if r['model']==m and r['subset']==subset]
  n=sum(r['planned_n'] for r in g)
  rep.append({'model':m,'subset':subset,'planned':n,'accuracy_original_gold':sum(r['planned_n']*r['accuracy_original_gold_all_planned'] for r in g)/n,**{f'TBR_{r["group"]}':r['true_rate_all_planned'] for r in g if r['tbr_applicable']}})
 for variant in ['label_order','template_ood','name','label_only','natural_rule','structural_rule','real_definition']:
  changed=[r for r in rr if r['dataset']==variant]
  keys={(r['item']['family_id'],r['item']['knowledge'],r['item']['composition'],r['item']['context']) for r in changed}
  base=[r for r in rr if r['dataset']=='main_core' and (r['item']['family_id'],r['item']['knowledge'],r['item']['composition'],r['item']['context']) in keys]
  assert len(base)==len(changed)
  robust.append({'model':m,'variant':variant,'planned':len(changed),'baseline_accuracy_matched':sum(bool(r.get('correct')) for r in base)/len(base),'variant_accuracy':sum(bool(r.get('correct')) for r in changed)/len(changed),'variant_parse_valid':sum(r.get('parsed') is not None for r in changed)})
 for k in ['real','nonce','micro']:
  g=[r for r in rr if r['dataset']=='main_core' and r['item']['knowledge']==k]
  valid=[r for r in g if isinstance((r.get('usage') or {}).get('prompt_tokens'),(int,float))]
  tokens.append({'model':m,'knowledge':k,'planned':len(g),'usage_available':len(valid),'mean_prompt_tokens':statistics.mean(r['usage']['prompt_tokens'] for r in valid) if valid else None,'mean_completion_tokens':statistics.mean(r['usage']['completion_tokens'] for r in valid) if valid else None})
write('core_accuracy',core);write('replication',rep);write('label_controls',controls);write('robustness',robust);write('prompt_lengths',tokens)

# Categorical confusions distinguish false endpoint entailment from false
# contradiction and from activity-occurrence rejection; q alone cannot do so.
confusions=[];judgment_cells=[]
for m in models:
 for k in ['real','nonce','micro']:
  g=[r for r in main if r['model']==m and r['dataset']=='main_core' and r['item']['knowledge']==k]
  for gold in ['entailed','contradicted','unknown']:
   gg=[r for r in g if r['item']['gold']==gold]
   counts=collections.Counter((r.get('parsed') or {}).get('judgment','missing_or_invalid') for r in gg)
   assert sum(counts.values())==len(gg)
   for predicted in ['entailed','contradicted','unknown','missing_or_invalid']:
    confusions.append({'model':m,'knowledge':k,'gold':gold,'predicted':predicted,'count':counts[predicted],'gold_n':len(gg),'rate_within_gold':counts[predicted]/len(gg)})
  for composition in ['bounded','unbounded']:
   for context in ['neutral','supportive','cancelling']:
    gg=[r for r in g if r['item']['composition']==composition and r['item']['context']==context]
    counts=collections.Counter((r.get('parsed') or {}).get('judgment','missing_or_invalid') for r in gg)
    assert sum(counts.values())==len(gg)
    judgment_cells.append({'model':m,'knowledge':k,'composition':composition,'context':context,'planned':len(gg),**{predicted+'_count':counts[predicted] for predicted in ['entailed','contradicted','unknown','missing_or_invalid']}})
write('core_confusions',confusions);write('core_judgment_cells',judgment_cells)

write('primary_family_only_sensitivity',secondary['primary_family_only_sensitivity']);write('primary_all_30',report['primary']['results']);write('secondary_all',secondary['results']);write('dataset_summaries',[{k:v for k,v in r.items() if k!='cells'} for r in report['datasets']])
write('core_cells',[c for r in report['datasets'] if r['dataset'] in ['main_core','stress_core'] for c in r['cells']])
write('matched_stress',[{k:v for k,v in r.items() if k!='cells'} for r in secondary['matched_stress_core']])
fits=[]
for model,r in mixed['model_reports'].items():
 if model in models:
  for outcome in ['binary','q']:
   for f in r[outcome].get('fits',[]):fits.append({'model':model,'outcome':outcome,**f})
  fits.append({'model':model,'outcome':'intended_prior',**r['intended_prior']})
 else:fits.append({'model':model,**r})
write('mixed_fit_diagnostics',fits)
manifest={'source_sha256':report['analysis_source_sha256'],'table_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.csv')},'status':'real completed outcomes; tables require manuscript interpretation; no effect-selected deletion'}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Complete evidence tables exported:',len(manifest['table_sha256']))
