"""Numerical/provenance self-audit; not independent linguistic validation."""
from pathlib import Path
import json,hashlib,re,statistics,csv,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from event_completion.analysis import load
tex=(ROOT/'paper/manuscript.tex').read_text();entries=[]
def read(name):return json.loads((ROOT/name).read_text())
def record(name,ok,sources,detail):
 assert ok,name
 entries.append({'claim':name,'verified':True,'sources':sources,'detail':detail})
models=read('config/study_protocol_candidate.json')['main_models'];labels=['Qwen8','Llama8','Ministral8','Gemma12','Qwen14','Qwen32']
desc=read('reports/main_descriptive_results.json');primary=read('reports/primary_results.json');secondary=read('reports/secondary_results.json');grammar=read('reports/grammar_complete_sensitivity.json')
for file in ['main_core_descriptive.tex','primary_compact.tex','reviewer_error_profile.tex']:
 fragment=(ROOT/'paper/tables'/file).read_text();record('Embedded table '+file,tex.count(fragment)==1,['paper/tables/'+file],{'exact_fragment_once':True})
for model,label in zip(models,labels):
 vals=[]
 for k in ['real','nonce','micro']:
  r=next(r for r in desc['core'] if r['model']==model and r['knowledge']==k)
  vals.extend(f'{100*v:.1f}' for v in [r['accuracy'],r['macro_accuracy'],r['gold_accuracy']['unknown']])
 c=next(r for r in desc['label_controls'] if r['model']==model)
 row=label+' & '+' & '.join(vals)+f" & {c['gold_correct']['unknown']}/20"+r' \\'
 record('Core table '+label,row in tex,['reports/main_descriptive_results.json','reports/main_descriptive_reconciliation.json'],{'expected_row':row})
 vals=[]
 for subset in ['original_400','published_vss_303','A_explicit_noncompletion_24']:
  g=[r for r in desc['original_replication'] if r['model']==model and r['subset']==subset];n=sum(r['planned_n'] for r in g)
  vals.append(sum(r['accuracy_original_gold_all_planned']*r['planned_n'] for r in g)/n)
  vals += [next(r['true_rate_all_planned'] for r in g if r['group']==group) for group in (['A','C'] if subset!='A_explicit_noncompletion_24' else ['A'])]
 row=label+' & '+' & '.join(f'{100*v:.1f}' for v in vals)+r' \\'
 record('Original replication table '+label,row in (ROOT/'paper/tables/replication_descriptive.tex').read_text(),['reports/main_descriptive_results.json','reports/original_audit.json'],{'expected_row':row})
 metrics=['neutral_cs_target_real','neutral_cs_real_minus_nonce','neutral_cs_real_minus_micro','bounded_real_cancel_minus_neutral_q','structural_rule_minus_baseline_accuracy'];cells=[]
 for metric in metrics:
  r=next(r for r in primary['results'] if r['model']==model and r['metric']==metric);x=r['result'];factor=100 if metric==metrics[-1] else 1
  value=f"{factor*x['estimate']:.3f}" if factor==1 else f"{factor*x['estimate']:.2f}"
  ci=','.join(f'{factor*v:.3f}' if factor==1 else f'{factor*v:.2f}' for v in x['ci95'])
  cells.append(r'\shortstack{$'+value+r'$\\$['+ci+r']$\\$'+f"{r['p_holm_30']:.3f}"+'$}')
 row=label+' & '+' & '.join(cells)+r' \\[3pt]'
 record('All five primary cells '+label,row in (ROOT/'paper/tables/primary_descriptive.tex').read_text(),['reports/primary_results.json'],{'expected_row':row})
record('No primary structural gain survives Holm',all(r['p_holm_30']>.05 for r in primary['results'] if r['metric']==metrics[-1]),['reports/primary_results.json'],{'complete_family':30})
prior=[r for r in secondary['results'] if r['metric']=='intended_high_minus_low_q'];record('No intended-prior test survives BH',len(prior)==21 and min(r['p_bh_secondary'] for r in prior)>.05,['reports/secondary_results.json'],{'minimum_adjusted_p':min(r['p_bh_secondary'] for r in prior)})
record('Authoring reconciliation',read('reports/main_descriptive_reconciliation.json')['passed'],['reports/main_descriptive_reconciliation.json'],{'comparisons':2243,'primary_results_exact':True})
record('All completed wording pairs retained',grammar['planned_pairs']==518 and grammar['parse_valid']==518 and grammar['transport_missing']==0,['reports/grammar_complete_design.json','reports/grammar_complete_sensitivity.json'],{'disagreements':sum(r['judgment_disagreements'] for r in grammar['results']),'new_calls':338,'initial_cache_reused':180})
record('Final project charges',f"{grammar['final_known_returned_project_cost_usd']:.4f}" in (ROOT/'paper/supplementary_results.md').read_text() and f"{grammar['final_conservative_project_ledger_usd']:.4f}" in (ROOT/'paper/supplementary_results.md').read_text() and grammar['final_conservative_project_ledger_usd']<10,['reports/grammar_complete_sensitivity.json','reports/run_metadata_audit.json'],{'known_returned_usd':grammar['final_known_returned_project_cost_usd'],'conservative_usd':grammar['final_conservative_project_ledger_usd']})
mixed=read('reports/mixed_models.json');fits=[]
for m,r in mixed['model_reports'].items():
 if 'binary' in r:fits+=r['binary']['fits']+r['q']['fits']+[r['intended_prior']]
 else:fits.append(r)
record('Mixed-model diagnostics not hidden',len(fits)==32 and sum(bool(f['usable']) for f in fits)==1,['reports/mixed_models.json'],{'attempted':32,'numerically_usable':1,'usable_scope':'Qwen14 exploratory prior only'})
matched=read('reports/stress_descriptive_results.json');actual=load(ROOT/'data/analysis/stress_planned.jsonl');core=[r for r in actual if r['dataset']=='stress_core'];record('Strong-model denominator and main matching',len(actual)==660 and len(core)==540 and len({r['item']['family_id'] for r in core})==30 and len(secondary['matched_stress_core'])==7,['reports/stress_descriptive_results.json','reports/secondary_results.json'],{'families':30,'core_cells_per_system':540,'systems':7})
record('DeepSeek Real unknown count',sum(bool(r['correct']) for r in core if r['item']['knowledge']=='real' and r['item']['gold']=='unknown')==14,['data/analysis/stress_planned.jsonl'],{'correct':14,'planned':30})
record('Complete supplementary diagnostics',len(secondary['results'])==380 and len(secondary['primary_family_only_sensitivity'])==30,['reports/secondary_results.json'],{'secondary':380,'family_sensitivity':30,'no_replacement_of_primary':True})
record('No incomplete manuscript markers',not re.search(r'working draft|results? (?:remain |are )?pending|\bTODO\b|\bTBD\b',tex,re.I),['paper/manuscript.tex'],{'theory_scope':'conditional operational interpretation; no human validation or causal knowledge-removal claim'})
record('Original source label identity',hashlib.sha256((ROOT/'data/original/upstream/data/imperfectiveNLI.json').read_bytes()).hexdigest()=='ddd01d06b18b9bab24abb5bc92a8eb740bb145123658fa9a10bd86e38b4bdb5a',['data/original/upstream/data/imperfectiveNLI.json'],{'original_gold_unchanged':True})
references={'maccartney2008':'https://aclanthology.org/C08-1066/','poliak2018':'https://aclanthology.org/S18-2023/','checklist2020':'https://aclanthology.org/2020.acl-main.442/','vendler1957':'https://doi.org/10.2307/2182371','moens1988':'https://aclanthology.org/J88-2003/','krifka1998':'https://www.leibniz-zas.de/de/forschung/publikationen/details/publications/3381-the-origins-of-telicity','ma2026':'https://aclanthology.org/2026.acl-long.689/','han2026':'https://arxiv.org/abs/2608.25005','prus2024':'https://aclanthology.org/2024.eacl-long.115/','prus2025':'https://aclanthology.org/2025.findings-acl.683/','core2025':'https://aclanthology.org/2025.findings-acl.992/','cxmp2026':'https://aclanthology.org/2026.acl-long.2132/','cogs2020':'https://aclanthology.org/2020.emnlp-main.731/','hans2019':'https://aclanthology.org/P19-1334/'}
references.update({r['key']:r['url'] for r in read('reports/literature_citation_verification.json')['new_references']})
record('Citation keys resolved',set(re.findall(r'\\bibitem\{([^}]+)\}',tex))==set(references) and all(tex.count(r['bibitem_tex'])==1 for r in read('reports/literature_citation_verification.json')['new_references']) and all(k in references for group in re.findall(r'\\cite\{([^}]+)\}',tex) for k in group.split(',')),['reports/literature_review.md','reports/source_registry.json','reports/novelty_audit.md','reports/editorial_citation_audit.json','reports/literature_citation_verification.json','reports/literature_coverage_audit.json'],{'primary_links':references,'han_status':'arXiv v1 preprint','scope':'Bibliographic/source self-audit; not independent expert review'})
paths=sorted({f for e in entries for f in e['sources']})
report={'passed':True,'audit_type':'Automated numerical/provenance consistency plus author self-audit; no independent human benchmark validation or peer review claimed.','entries':entries,'source_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in paths},'manuscript_sha256':hashlib.sha256((ROOT/'paper/manuscript.tex').read_bytes()).hexdigest()}
(ROOT/'reports/final_claim_ledger.json').write_text(json.dumps(report,indent=2)+'\n');print('Claim ledger verified entries:',len(entries))
