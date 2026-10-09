"""Audit reviewer-driven evidence and continuity with all frozen original analyses."""
from pathlib import Path
from types import SimpleNamespace
from collections import Counter
import json,hashlib,sys,re,datetime
import fitz
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from event_completion.runner_binding import make_jobs
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads((ROOT/p).read_text())
def load(p):return [json.loads(l) for l in (ROOT/p).read_text().splitlines() if l.strip()]
def main():
 checks=[]
 def check(name,ok,detail=None):
  assert ok,name
  checks.append({'name':name,'passed':True,'detail':detail})
 old=read('reports/offline_reproduction_audit.json')['tested_component_sha256']
 check('all_60_original_scientific_components_unchanged',len(old)==60 and all(sha(ROOT/p)==h for p,h in old.items()),{'components':60})
 snapshot=ROOT/'data/frozen/reviewer_prior_delivery';sm=json.loads((snapshot/'snapshot_manifest.json').read_text())['sha256']
 check('previous_literature_delivery_preserved',all(sha(snapshot/p)==h for p,h in sm.items()),{'files':len(sm)})
 for line in (snapshot/'reports/literature_revision.sha256').read_text().splitlines():
  h,p=line.split('  ',1);candidate=snapshot/p
  check('historical_literature_checkpoint:'+p,candidate.exists() and sha(candidate)==h)
 protocol=read('reports/reviewer_binding_protocol.json');result=read('reports/reviewer_binding_results.json')
 rows=load('data/analysis/reviewer_binding_planned.jsonl');args=SimpleNamespace(datasets='reviewer_binding_v2',models=','.join(protocol['models']),items_per_model=None);jobs=make_jobs(args)
 check('all_challenge_payloads_and_denominators',len(rows)==len(jobs)==5040 and {r['request_id'] for r in rows}=={j['request_id'] for j in jobs} and result['transport_missing']==0)
 earliest=min(r['started_utc'] for r in rows if r['source'].startswith('data/raw_runs/reviewer_binding_main/'))
 check('corrected_protocol_amendment_precedes_full_collection',protocol['amended_before_corrected_full_collection_utc']<earliest,{'amendment_utc':protocol['amended_before_corrected_full_collection_utc'],'first_main_utc':earliest})
 check('challenge_oracle_and_protocol_frozen',sha(ROOT/'data/supplementary/reviewer_binding.jsonl')==protocol['dataset_sha256'] and sha(ROOT/'data/frozen/reviewer_binding_collection/scripts/build_binding_challenge.py')==protocol['generator_sha256'] and sha(ROOT/'data/frozen/reviewer_binding_collection/src/event_completion/runner_binding.py')==protocol['collector_sha256'])
 definition=read('reports/reviewer_binding_definition_protocol.json')
 corrected=min(r['started_utc'] for r in rows if r['source'].startswith('data/raw_runs/reviewer_binding_definition/'))
 check('definition_amendment_frozen_before_collection',definition['created_utc']<corrected and sha(ROOT/'data/supplementary/reviewer_binding_v2.jsonl')==definition['dataset_sha256'] and sha(ROOT/'scripts/repair_binding_definition.py')==definition['repair_script_sha256'] and sha(ROOT/'src/event_completion/runner_binding.py')==definition['collector_sha256'])
 check('all_definition_precision_pairs_retained',len(result['definition_precision_pairs'])==7 and all(r['paired_n']==240 for r in result['definition_precision_pairs']))
 check('word_unigram_bound_and_pair_control',result['surface_baseline']['exact_feature_collisions_verified'] and result['surface_baseline']['finite_set_unigram_accuracy_ceiling']==.6 and result['surface_baseline']['all']['accuracy']<=.6 and all(r['different_gold_pair_both_correct']['n']==288 for r in result['results']))
 tex=(ROOT/'paper/manuscript.tex').read_text();prior_tex=(snapshot/'paper/manuscript.tex').read_text()
 for path in ['replication_descriptive.tex','primary_descriptive.tex']:
  fragment=(ROOT/'paper/tables'/path).read_text()
  check('complete_original_table_retained:'+path,fragment in prior_tex)
 for path in ['primary_compact.tex','reviewer_error_profile.tex','reviewer_binding.tex']:
  check('new_table_embedded_exactly_once:'+path,tex.count((ROOT/'paper/tables'/path).read_text())==1)
 check('all_30_primary_tests_preserved',len(read('reports/primary_results.json')['results'])==30 and 'post-review' in tex.lower())
 check('all_380_secondary_rows_preserved',len(read('reports/secondary_results.json')['results'])==380)
 core=read('reports/reviewer_core_diagnostics.json')
 check('complete_core_breakdown',len(core['profiles'])==18 and len(core['per_lemma'])==216 and len(core['per_stratum'])==54 and len(core['real_definition_cells'])==24)
 pdf=ROOT/'output/pdf/submission.pdf';doc=fitz.open(pdf);text='\n'.join(p.get_text() for p in doc)
 check('eight_page_official_compilation',len(doc)<=8 and read('reports/final_pdf_compile.json')['success'] and not read('reports/final_pdf_compile.json')['overfull_hbox_warnings_last_pass'],{'pages':len(doc)})
 check('no_broken_reference_or_double_period',not re.search(r'\bef\s*\{?\s*(?:sec|fig|tab):|et\s+al\.\.',text))
 check('all_32_verified_references_cited',len(re.findall(r'\\bibitem\{',tex))==32 and read('reports/literature_coverage_audit.json')['all_bibliography_items_cited_in_body'])
 lo=min(r['all']['accuracy'] for r in result['results'])*100;hi=max(r['all']['accuracy'] for r in result['results'])*100
 check('final_challenge_range_in_abstract',f'{lo:.1f}--{hi:.1f}' in tex.split('\\end{abstract}')[0])
 supp=ROOT/'output/pdf/supplementary.pdf';sd=fitz.open(supp);st='\n'.join(p.get_text() for p in sd)
 check('all_six_readable_supplement_tables_present',all(re.search(r'Table\s+'+str(i)+r'[.:]',st) for i in range(1,7)) and 'Precise correct' in st and len(sd)==5)
 check('supplement_official_compile_without_overflow',read('reports/supplementary_compile.json')['success'] and not read('reports/supplementary_compile.json')['overfull_hbox_last_pass'])
 check('incremental_budget_including_interruption_reserve',result['collection']['budget_check_with_interruption_reserve'],result['collection'])
 report={'passed':True,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'manuscript_sha256':sha(ROOT/'paper/manuscript.tex'),'pdf_sha256':sha(pdf),
 'original_scientific_components_unchanged':60,'primary_tests':30,'secondary_rows':380,'supplementary_design':'shared-premise word-count-collision role-binding challenge; post-review, not relabeled primary',
 'review_status':'agent evidence/visual self-audit; no independent human peer review or acceptance prediction claimed'}
 (ROOT/'reports/reviewer_revision_audit.json').write_text(json.dumps(report,indent=2)+'\n')
 print('Reviewer revision checks passed:',len(checks))
if __name__=='__main__':main()
