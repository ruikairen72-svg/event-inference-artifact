"""Technical PDF audit only; scientific/visual readiness requires separate review."""
from pathlib import Path
import argparse,json,hashlib,re
import pymupdf
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--pdf',default='output/pdf/submission.pdf');p.add_argument('--report',default='reports/pdf_technical_audit.json');a=p.parse_args()
path=ROOT/a.pdf
if not path.is_file():raise SystemExit('PDF is not yet available: '+a.pdf)
doc=pymupdf.open(path);text='\n'.join(page.get_text() for page in doc)
checks=[]
def check(name,ok,**detail):checks.append({'check':name,'pass':bool(ok),**detail})
check('US_Letter_all_pages',all(abs(page.rect.width-612)<.1 and abs(page.rect.height-792)<.1 for page in doc))
check('conservative_eight_page_target',4<=len(doc)<=8,pages=len(doc))
check('searchable_substantive_text',all(len(page.get_text().strip())>50 for page in doc),text_characters=len(text))
metadata=doc.metadata;creator=metadata.get('author','').strip().lower()
check('anonymous_author_metadata',creator in ['', 'anonymous','anonymous author(s)','anonymous authors'],author_field=creator)
home_prefixes=[str(Path.home())+'/', '/'+ 'Users'+'/', '/'+ 'home'+'/']
check('no_machine_home_path_in_text_or_metadata',not any(prefix in text+json.dumps(metadata) for prefix in home_prefixes))
check('no_placeholder_DOI_ISBN',not re.search(r'nnnnnnn|978-x+|xxxx-xxxx',text,re.I))
placeholder=re.findall(r'working draft|collection (?:and analysis )?(?:is |are )?(?:ongoing|incomplete)|results? (?:remain |are )?pending|\bTODO\b|\bTBD\b',text,re.I)
check('no_incomplete_research_placeholders',not placeholder,matches=placeholder)
check('no_unresolved_reference_markers','??' not in text and '\ufffd' not in text)
check('no_literal_broken_cross_reference',not re.search(r'\bef\s*\{?\s*(?:sec|fig|tab):',text))
check('no_double_period_after_et_al',not re.search(r'et\s+al\.\.',text))
check('unencrypted',not doc.is_encrypted)
fonts={}
for page in doc:
 for info in page.get_fonts(full=True):
  xref=info[0]
  if xref in fonts:continue
  name,ext,kind,buffer=doc.extract_font(xref)
  # Type3 stores glyph programs in the PDF rather than an external font file.
  embedded=bool(buffer) or kind.lower()=='type3'
  fonts[xref]={'name':name,'type':kind,'extension':ext,'embedded':embedded,'font_program_bytes':len(buffer)}
check('fonts_embedded',all(f['embedded'] for f in fonts.values()),fonts=list(fonts.values()))
bad_spans=[];sizes=[]
for i,page in enumerate(doc):
 for block in page.get_text('dict')['blocks']:
  for line in block.get('lines',[]):
   for span in line.get('spans',[]):
    x0,y0,x1,y1=span['bbox'];sizes.append(span['size'])
    if x0 < -.5 or y0 < -.5 or x1 > page.rect.width+.5 or y1 > page.rect.height+.5:
     bad_spans.append({'page':i+1,'bbox':span['bbox'],'text':span['text'][:80]})
check('text_inside_media_box',not bad_spans,violations=bad_spans)
report={'pdf':str(path.relative_to(ROOT)),'pdf_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'checks':checks,
 'technical_checks_passed':all(c['pass'] for c in checks),'font_size_range_points':[min(sizes),max(sizes)] if sizes else None,
 'submission_ready':False,'visual_QA_required':True,'scientific_claim_audit_required':True,
 'note':'Page/font/metadata checks do not establish placed-figure readability, source-number correctness, novelty, or scientific readiness.'}
out=ROOT/a.report;out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'pdf_pages':len(doc),'technical_checks_passed':report['technical_checks_passed'],'failed_checks':[c['check'] for c in checks if not c['pass']],'submission_ready':False},indent=2))
