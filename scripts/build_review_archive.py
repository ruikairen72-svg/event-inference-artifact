"""Build a local anonymous reproducibility archive after final audit.
No publication, licensing grant, external upload, or credential is involved.
"""
from pathlib import Path
import json,hashlib,re,zipfile,datetime
ROOT=Path(__file__).resolve().parents[1]
final=ROOT/'reports/final_submission_audit.json'
if not final.exists() or not (json.loads(final.read_text()).get('submission_ready') or json.loads(final.read_text()).get('paper_ready')):
 raise SystemExit('Final scientific/PDF audit must explicitly establish readiness first.')
allow=['src','scripts','tests','config','data/generated','data/theory','data/frozen/theory_main_v1','data/frozen/grammar_initial_v1','data/analysis','data/raw_runs','figures','paper/manuscript.tex','paper/tables','paper/template','requirements-analysis.txt','README.md','STATUS.md','output/pdf/submission.pdf']
# Curate reports: sources are attributed, full copyrighted texts not bundled.
allow+=['reports/'+x for x in ['original_audit.json','run_metadata_audit.json','internal_review_pre_results.md','amendments.md','analysis_results.json','analysis_results.md','primary_results.json','secondary_results.json','mixed_models.json','surface_baselines.json','stimulus_wording_audit.json','secondary_analysis_plan.md','novelty_audit.md','literature_review.md','benchmark_audit.md','source_registry.json','novelty_sources.json','template_provenance.json','theoretical_predictions.md','data_audit.md','data_validation.json','phase5_checkpoint.md','integrity_audit.json','final_submission_audit.json','final_submission_audit.md','final_project_report.md']]
allow+=['data/original/upstream/data/imperfectiveNLI.json','data/original/disputed_items.jsonl','.research/figures']
allow+=['reports/final_pdf_compile.json','reports/figure_final_audit.json','reports/offline_reproduction_audit.json','reports/grammar_complete_design.json','reports/grammar_complete_sensitivity.json','reports/stress_descriptive_results.json','reports/main_authoring_primary.json','reports/main_descriptive_results.json','reports/main_descriptive_reconciliation.json','reports/completion_requirements.md','reports/pdf_technical_audit.json','reports/final_claim_ledger.json','reports/grammar_repair_design.json','reports/grammar_repair_sensitivity.json','reports/main_initial_collection_checkpoint.json','reports/main_collection_complete_checkpoint.json']
allow += ['reports/'+x for x in ['final_page_render_manifest.json','track_selection.md','study_blueprint.md','model_selection.md','pilot_report.md','pilot_diagnostics.md','pilot_v1_summary.json','pilot_v2_summary.json','scheduling_audit.json','data_validation.json','cost_plan.md','risk_register.md']]
allow += [str(p.relative_to(ROOT)) for p in (ROOT/'reports').glob('phase[6-9]*') if p.suffix in ['.md','.sha256']]
allow += [str(p.relative_to(ROOT)) for p in (ROOT/'reports').glob('phase1[0-2]*') if p.suffix in ['.md','.sha256']]
allow += ['paper/author_checklist.md','paper/research_tools_disclosure.md','paper/supplementary_results.md','reports/editorial_citation_audit.json','reports/editorial_revision_audit.json','reports/editorial_revision.sha256','reports/editorial_revision_checkpoint.md','data/frozen/editorial_prior_delivery']
allow += ['reports/literature_coverage_report.md','reports/literature_coverage_audit.json','reports/literature_citation_verification.json','reports/literature_revision_audit.json','reports/literature_revision.sha256','reports/literature_revision_checkpoint.md','data/frozen/literature_prior_delivery']
allow += ['data/supplementary','data/frozen/reviewer_prior_delivery','data/frozen/reviewer_binding_collection','data/frozen/reviewer_binding_initial_protocol.json','paper/supplementary.tex','output/pdf/supplementary.pdf']
allow += [str(p.relative_to(ROOT)) for p in (ROOT/'reports').glob('reviewer*') if p.suffix in ['.json','.md','.sha256']]
allow += ['reports/sac_reviewer_report.md','reports/supplementary_compile.json']
files=set()
for relative in allow:
 p=ROOT/relative
 if p.is_file():files.add(p)
 elif p.is_dir():files.update(q for q in p.rglob('*') if q.is_file() and '__pycache__' not in q.parts and q.suffix not in ['.log','.pyc','.lock'])
# Runtime progress/plan copies are provenance, not private API headers.
credential=re.compile(rb'sk-or-v1-[0-9a-f]{64}',re.I)
identity=re.compile(re.escape(b'/'+b'Users'+b'/')+b'|'+re.escape(b'/'+b'home'+b'/'),re.I)
for p in files:
 if p.suffix in ['.py','.R','.json','.jsonl','.txt','.md','.tex','.csv']:
  content=p.read_bytes()
  if credential.search(content):raise RuntimeError('Credential detected in: '+str(p.relative_to(ROOT)))
  if identity.search(content):raise RuntimeError('Local identifying path detected in: '+str(p.relative_to(ROOT)))
manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
notes='''Anonymous research review archive

This local archive accompanies a theory-derived event-inference study. It is not
an external publication and does not create a new public license grant.

All original ImperfectiveNLI labels are unchanged. The original dataset is
attributed to Bolei Ma and Yusuke Miyao (ACL 2026), official repository commit
938ef893c3368f3a597e6add2cfebdad02fddebf. Their paper specifies CC BY-NC 4.0 for
the dataset: https://creativecommons.org/licenses/by-nc/4.0/ . The original
400-item JSON is retained unchanged; the separately supplied concern flags and
our generated items/results are clearly distinguished. Upstream code and full
third-party papers/books are excluded; source URLs and audit notes are supplied.

ACM template files are unchanged official SAC 2027 resources. They retain their
own notices and terms; provenance is recorded. The study code and new artifacts
remain subject to their rights holders' decisions about a public release.

No API key is included. Offline analysis operates on the recorded outcomes.
All human-review forms are excluded; no human annotations or ratings exist.
See README.md for reproduction and the final audit for scientific limitations.
'''
archive=ROOT/'output/anonymous-reproducibility.zip';archive.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(files):z.write(p,str(p.relative_to(ROOT)))
 z.writestr('ARCHIVE_NOTICE.txt',notes)
 z.writestr('ARCHIVE_MANIFEST.json',json.dumps({'built_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':manifest},indent=2)+'\n')
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 for path,wanted in manifest.items():assert hashlib.sha256(z.read(path)).hexdigest()==wanted
(ROOT/'reports/review_archive_manifest.json').write_text(json.dumps({'archive':str(archive.relative_to(ROOT)),'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'files':len(manifest),'bytes':archive.stat().st_size,'verified_members':True},indent=2)+'\n')
print('Anonymous local research archive built and all members verified:',len(manifest))
