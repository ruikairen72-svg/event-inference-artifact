"""Readable supplementary tables/stimuli, generated from all retained outcomes."""
from pathlib import Path
import json,hashlib,subprocess,shutil,re
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def esc(s):
 return ''.join({'&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}'}.get(c,c) for c in s)
def table(caption,label,headers,rows,wide=True):
 env='table'
 return ('\\begin{'+env+'}[H]\n\\centering\n\\small\n\\caption{'+caption+'}\n\\label{'+label+'}\n\\setlength{\\tabcolsep}{4pt}\n\\begin{tabular}{l'+'r'*(len(headers)-1)+'}\n\\toprule\n'+' & '.join(headers)+r' \\'+'\n'+r'\midrule'+'\n'+'\n'.join(' & '.join(row)+r' \\' for row in rows)+'\n'+r'\bottomrule'+'\n'+r'\end{tabular}'+'\n'+r'\end{'+env+'}\n')
def main():
 result=read('reports/reviewer_binding_results.json');assert 'definition_precision_pairs' in result, 'Complete precise-definition collection first.'
 core=read('reports/reviewer_core_diagnostics.json');protocol=read('reports/reviewer_binding_protocol.json');names=['Qwen8','Llama8','Ministral8','Gemma12','Qwen14','Qwen32','DeepSeek'];models=protocol['models']
 s=r'''\documentclass[acmlarge,anonymous,review,nonacm]{acmart}
\usepackage{booktabs,amsmath,array,float}
\setlength{\emergencystretch}{1em}
\setcopyright{none}
\settopmatter{printacmref=false}
\acmConference[SAC '27]{ACM Symposium on Applied Computing}{April 5--9, 2027}{Gwangju, Republic of Korea}
\acmYear{2027}\acmDOI{}\acmISBN{}
\title{Supplementary Material: Endpoint Inference under Compatible Histories}
\author{Anonymous Author(s)}
\begin{document}
\maketitle
\section{Evidence and Analysis Boundaries}
This supplement preserves the complete original primary interval table and replication table, then documents the supplementary role-binding task and descriptive breakdowns. Original gold, the 30-test Holm family and all 380 secondary rows are unchanged. The challenge and its definition-precision check are post-review supplements, not additional prespecified primary tests. Full rows, request hashes and scripts are included in the anonymous archive.

\section{Complete Original Results}
The first two tables retain the full original primary contrasts and original-benchmark replication. Primary marginal intervals resample verbs then families within verbs; Holm correction applies to the complete thirty-test family. Original replication subsets retain distinct denominators and unchanged labels.

'''
 for name in ['primary_descriptive.tex','replication_descriptive.tex']:
  fragment=(ROOT/'paper/tables'/name).read_text().replace(r'\begin{table*}[t]',r'\begin{table}[H]').replace(r'\end{table*}',r'\end{table}').replace(r'\centering',r'\centering\small')
  s+=fragment+'\n'
 s+=r'''\section{Role-Binding Construction and Full Stimuli}
Each lexical block covers five status pairs, both actor assignments, both targets and all three presentations (60 cells). Six lemmas are reused from the main inventory and six are held out of that inventory. This describes benchmark lexical holdout, not model pretraining exclusion. Each actor has a separate identical assignment; coverage is monotone within the same ten-minute interval.

The oracle evaluates bounded truth by stage 4 and occurrence truth by at least two positive stages. It uses three representative histories: $h_0=()$, $h_-=(1,2,S)$, and $h_+=(1,2,3,4,S)$. No activity retains $h_0$ ($C/C$); partial open evidence retains $h_-,h_+$ ($U/E$); final partial coverage retains $h_-$ ($C/E$); full coverage retains $h_+$ ($E/E$); unrelated observation retains all three ($U/U$). The histories represent target truth alternatives, not sampled event frequencies.

Every bounded swap pair changes gold. Three of five activity swap pairs change gold; the other two retain entailed activity. Identical word counts force identical predictions for any deterministic word-count-invariant classifier. Its maximum finite-set accuracy is therefore $1/2$ for bounded targets and $(3+2\cdot2)/10=7/10$ for activity, or $60\%$ overall. On the 288 pairs whose gold differs, such a classifier cannot get both items right. This bound also applies to word-unigram TF-IDF classification.

Below are the complete RB01 idle/open stimuli. Within either assignment, the two targets have exactly the same premise. The diagrams abbreviate these full texts; the empirical tasks use them without abbreviation.

'''
 rows=[json.loads(l) for l in (ROOT/'data/supplementary/reviewer_binding_v2.jsonl').read_text().splitlines()]
 for k in ['real','nonce','micro']:
  s+='\\subsection{'+k.title()+'}\n'
  for swap in [0,1]:
   rs=[r for r in rows if r['family_id']=='RB01' and r['status_pair']==['idle','open'] and r['knowledge']==k and r['swap']==swap]
   s+='\\paragraph{'+('Original assignment' if not swap else 'Swapped assignment')+'} '+esc(rs[0]['premise'])+'\n\n'
   for r in rs:s+='\\noindent\\textbf{'+r['composition'].title()+' target ('+r['gold']+'):} '+esc(r['hypothesis'])+'\\par\n'
   s+='\n'
 s+=r'''\section{Complete Supplementary Profiles}
Each system has 720 cells; 288 are entailed and 216 each are contradicted and unknown. Macro recall averages the three label recalls. Bootstrap intervals use 10,000 draws of the twelve lemma blocks (seed 20271009); the seen/held-out split intervals each use six blocks. They describe lexical variation within the specified construction inventory, not decoding variation across repeated seeds. Every outcome is retained; all labels parse successfully.

'''
 data=[]
 for n,r in zip(names,result['results']):
  a=r['all'];cells=[n,f"{100*a['macro_recall']:.1f}"]+[f"{100*a['gold_recall'][g]:.1f}" for g in ['entailed','contradicted','unknown']]
  for split in ['seen','held_out']:
   x=r['by_split'][split];lo,hi=x['accuracy_ci95_lemma_bootstrap'];cells.append(f"{100*x['accuracy']:.1f} [{100*lo:.1f},{100*hi:.1f}]")
  data.append(cells)
 s+=table('Supplementary macro and gold-label recall, and lexical split accuracy (percent). Split intervals resample six lemma blocks.','tab:splits',['System','Macro','E','C','U','Seen [CI]','Held out [CI]'],data)
 s+=r'''\subsection{Definition-Precision Sensitivity}
The initial nonce-some gloss required an ``observed increase,'' conflating occurrence with the availability of observation records. The precise gloss requires reaching at least two positive coverage landmarks. All 240 Nonce cells per system were retested with this replacement; records, actors, targets, histories and gold were unchanged. The final main-paper challenge uses this precise definition and reuses all 480 content-identical Real/Micro cells per system. Initial stimuli and all initial outcomes remain available. The paired check includes service/order variation and adds no inferential tests.

'''
 data=[]
 for n,r in zip(names,result['definition_precision_pairs']):data.append([n,str(r['initial_correct']),str(r['precise_definition_correct']),str(r['judgment_disagreements'])])
 s+=table('Complete Nonce definition-precision pairs: correct counts out of 240 and changed judgment counts. Both directions of changes are retained.','tab:precision',['System','Initial correct','Precise correct','Changed labels'],data,False)
 s+=r'''\section{Original-Core Lexical and Definition Diagnostics}
The next tables retain all Real unknown counts per lemma and all four Real-definition cells per system. Each original lemma contributes ten unknown targets; each definition cell contains 24 matched families. The underlying outcomes and original primary and secondary estimates are unchanged. Complete presentation profiles, all 216 per-lemma rows and 54 stratum rows are in the diagnostic report.

'''
 data=[]
 for lemma in sorted({r['lemma'] for r in core['per_lemma']}):
  data.append([lemma]+[str(next(r['unknown']['correct'] for r in core['per_lemma'] if (r['model'],r['knowledge'],r['lemma'])==(m,'real',lemma))) for m in models[:6]])
 s+=table('All Real unknown judgments correct out of ten per lemma. No lemma is omitted.','tab:lemmas',['Lemma']+names[:6],data)
 data=[]
 for m,n in zip(models[:6],names[:6]):
  data.append([n]+[f"{d['baseline']['correct']} / {d['definition']['correct']}" for comp,ctx in [('bounded','neutral'),('bounded','cancelling'),('unbounded','neutral'),('unbounded','cancelling')] for d in core['real_definition_cells'] if (d['model'],d['composition'],d['context'])==(m,comp,ctx)])
 s+=table('Real-definition controls: baseline / definition correct counts out of 24. Columns distinguish bounded (B) and activity (A), neutral (N) and cancellation (C).','tab:definitions',['System','B,N','B,C','A,N','A,C'],data)
 s+=r'''\section{Collection and Reproduction}
All original and supplementary payloads use pinned suppliers and the recorded decoding settings. A technical probe initially used an older collector without the main Qwen disable controls; those Qwen payloads are excluded from the corrected analysis and retained. Content-identical non-Qwen probe responses can be reused. Shutdown overlap duplicates are retained; the earliest timestamp per exact payload is selected regardless of correctness. No successful output is retried for its answer.

Collection-time generator, collector, protocol and dataset copies are frozen separately. Supplementary files are outside the original generated-data directory, preserving the original generator replay contract. The definition-precision amendment precedes all amended calls. Offline analysis needs no API key or network. API attempts, unknown-charge reserves and the interrupted-probe reserve are described in the supporting index; original ledgers remain unchanged.

\end{document}
'''
 source=ROOT/'paper/supplementary.tex';source.write_text(s)
 provenance=read('reports/template_provenance.json')
 assert hashlib.sha256((ROOT/'paper/template/acmart.cls').read_bytes()).hexdigest()==provenance['acmart_cls_sha256']
 compiler=shutil.which('tectonic') or '/opt/homebrew/bin/tectonic';out=ROOT/'output/pdf'
 proc=subprocess.run([compiler,'--only-cached','--print','-Z','search-path='+str(ROOT/'paper/template'),'--outdir',str(out),str(source)],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 log=proc.stdout.replace(str(ROOT),'.').replace(str(Path.home()),'<local-home>');(ROOT/'reports/supplementary_compile.log').write_text(log)
 if proc.returncode:raise SystemExit('Supplement compilation failed; source retained.')
 last=log.rsplit('Document Class: acmart ',1)[-1]
 versions=re.findall(r'Document Class: acmart ([^\n]+)',log)
 assert versions and all(v.startswith(provenance['acmart_version']) for v in versions)
 assert not re.search(r'There were undefined|File .* not found|^!',last,re.M)
 report={'success':True,'compiler':'existing Tectonic with official unchanged acmart2.19','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'pdf_sha256':hashlib.sha256((out/'supplementary.pdf').read_bytes()).hexdigest(),'overfull_hbox_last_pass':re.findall(r'Overfull \\hbox \([^\n]+',last)}
 (ROOT/'reports/supplementary_compile.json').write_text(json.dumps(report,indent=2)+'\n');print('Complete readable supplement compiled:',report)
if __name__=='__main__':main()
