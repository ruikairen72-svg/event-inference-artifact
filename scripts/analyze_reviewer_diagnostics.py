"""Post-review categorical/lexical descriptions of unchanged original outcomes."""
from pathlib import Path
from collections import defaultdict, Counter
import hashlib,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def load(p):return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
def main():
 rows=load(ROOT/'data/analysis/main_planned.jsonl')
 core=[r for r in rows if r['dataset']=='main_core']
 def summary(rs):
  return {'n':len(rs),'correct':sum(bool(r['correct']) for r in rs),'accuracy':sum(bool(r['correct']) for r in rs)/len(rs),
          'predictions':dict(Counter((r.get('parsed') or {}).get('judgment','invalid') for r in rs))}
 profiles=[];lexical=[];definitions=[];examples=[]
 for model in sorted({r['model'] for r in core}):
  mc=[r for r in core if r['model']==model]
  for k in ['real','nonce','micro']:
   sub=[r for r in mc if r['item']['knowledge']==k]
   u=[r for r in sub if r['item']['gold']=='unknown']; a=[r for r in sub if r['item']['composition']=='unbounded' and r['item']['context']=='neutral']
   bm={r['item']['family_id']:r for r in u};am={r['item']['family_id']:r for r in a}
   gaps=[bm[f]['parsed']['hypothesis_probability']-am[f]['parsed']['hypothesis_probability'] for f in bm]
   profiles.append({'model':model,'knowledge':k,'unknown':summary(u),'neutral_activity':summary(a),'mean_score_gap':float(np.mean(gaps)),
    'negative_gap_pairs':sum(g<0 for g in gaps),'unknown_to_contradicted':sum((r.get('parsed') or {}).get('judgment')=='contradicted' for r in u),
    'both_bounded_contradiction_and_activity_error':sum(bm[f]['parsed']['judgment']=='contradicted' and not am[f]['correct'] for f in bm),
    'negative_gap_with_either_categorical_error':sum(g<0 and (not bm[f]['correct'] or not am[f]['correct']) for f,g in zip(bm,gaps))})
   for lemma in sorted({r['item']['verb'] for r in sub}):
    lr=[r for r in sub if r['item']['verb']==lemma]
    lexical.append({'model':model,'knowledge':k,'lemma':lemma,'stratum':lr[0]['item']['stratum'],
       'all':summary(lr),'unknown':summary([r for r in lr if r['item']['gold']=='unknown']),
       'neutral_activity':summary([r for r in lr if r['item']['composition']=='unbounded' and r['item']['context']=='neutral'])})
  di=[r for r in rows if r['model']==model and r['dataset']=='real_definition']
  for comp,context in [('bounded','neutral'),('bounded','cancelling'),('unbounded','neutral'),('unbounded','cancelling')]:
   ds=[r for r in di if (r['item']['composition'],r['item']['context'])==(comp,context)]
   fam={r['item']['family_id'] for r in ds};base=[r for r in mc if r['item']['knowledge']=='real' and r['item']['family_id'] in fam and (r['item']['composition'],r['item']['context'])==(comp,context)]
   assert len(ds)==len(base)==24
   definitions.append({'model':model,'composition':comp,'context':context,'baseline':summary(base),'definition':summary(ds),
    'paired_correct_change':sum(r['correct'] for r in ds)-sum(r['correct'] for r in base)})
 strata=[]
 for model in sorted({r['model'] for r in lexical}):
  for k in ['real','nonce','micro']:
   for s in ['quantity','path','incremental']:
    lr=[r for r in lexical if (r['model'],r['knowledge'],r['stratum'])==(model,k,s)]
    assert len(lr)==4
    strata.append({'model':model,'knowledge':k,'stratum':s,'unknown_correct':sum(r['unknown']['correct'] for r in lr),'unknown_n':40,
      'neutral_activity_correct':sum(r['neutral_activity']['correct'] for r in lr),'neutral_activity_n':40,
      'lemmas_with_unknown_error':sum(r['unknown']['correct']<10 for r in lr),'lemmas_with_activity_error':sum(r['neutral_activity']['correct']<10 for r in lr)})
 report={'analysis_status':'post-review descriptive analysis; original prespecified tests unchanged','profiles':profiles,'per_lemma':lexical,'per_stratum':strata,'real_definition_cells':definitions,
 'source_sha256':{'data/analysis/main_planned.jsonl':hashlib.sha256((ROOT/'data/analysis/main_planned.jsonl').read_bytes()).hexdigest()}}
 (ROOT/'reports/reviewer_core_diagnostics.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'nonce_profiles':[p for p in profiles if p['knowledge']=='nonce'],'real_definition_unknown':[d for d in definitions if (d['composition'],d['context'])==('bounded','neutral')]},indent=2))
if __name__=='__main__':main()
