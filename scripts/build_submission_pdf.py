"""Export the multi-file paper using the retained unchanged official ACM class.

Uses an existing Tectonic compiler; never installs a TeX distribution or plugin.
"""
from pathlib import Path
import argparse,shutil,subprocess,json,hashlib,re,datetime
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--compiler');a=p.parse_args()
compiler=a.compiler or shutil.which('tectonic')
if not compiler and Path('/opt/homebrew/bin/tectonic').is_file():compiler='/opt/homebrew/bin/tectonic'
if not compiler:raise SystemExit('An existing Tectonic compiler is required for the retained multi-file figure/template project. Source and recorded final PDF remain available.')
provenance=json.loads((ROOT/'reports/template_provenance.json').read_text());cls=ROOT/'paper/template/acmart.cls'
assert hashlib.sha256(cls.read_bytes()).hexdigest()==provenance['acmart_cls_sha256']
out=ROOT/'output/pdf';out.mkdir(parents=True,exist_ok=True)
result=subprocess.run([compiler,'--only-cached','--print','-Z','search-path='+str(ROOT/'paper/template'),'--keep-logs','--outdir',str(out),'paper/manuscript.tex'],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
log=result.stdout
# Remove local machine paths from the review artifact, preserving diagnostics.
log=log.replace(str(ROOT),'.').replace(str(Path.home()),'<local-home>')
(ROOT/'reports/final_tex_compile.log').write_text(log)
if result.returncode:raise SystemExit('PDF compilation failed; inspect reports/final_tex_compile.log. Source retained.')
versions=re.findall(r'Document Class: acmart ([^\n]+)',log)
assert versions and all(v.startswith(provenance['acmart_version']) for v in versions)
last=log.rsplit('Document Class: acmart ',1)[-1]
assert not re.search(r'There were undefined|File .* not found|^!',last,re.M)
shutil.copyfile(out/'manuscript.pdf',out/'submission.pdf')
report={'success':True,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'compiler':'existing Tectonic','compiler_version':subprocess.check_output([compiler,'--version'],text=True).strip(),'selected_class_versions':versions,'official_class_sha256':provenance['acmart_cls_sha256'],'last_pass_has_unresolved_references':False,'overfull_hbox_warnings_last_pass':re.findall(r'Overfull \\hbox \(([^\n]+)',last),'source_sha256':hashlib.sha256((ROOT/'paper/manuscript.tex').read_bytes()).hexdigest(),'pdf_sha256':hashlib.sha256((out/'submission.pdf').read_bytes()).hexdigest(),'native_editor_disposition':'Source remains open. Built-in standalone compiler cannot resolve external figure resources and bundles acmart v1.83; final multi-file PDF is verified with the official retained v2.19 class using the existing compiler.'}
(ROOT/'reports/final_pdf_compile.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
