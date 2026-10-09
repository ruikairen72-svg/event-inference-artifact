"""Mechanical checks, distinct from independent human semantic validation."""
import json,re,hashlib
from collections import Counter,defaultdict
from pathlib import Path
from .generator import ROOT,LEXICON
from .semantics import gold

def read(path):return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
def validate():
 base=ROOT/'data/generated';files={p.stem:read(p) for p in base.glob('*.jsonl')}
 families=files.pop('families');fam={f['family_id']:f for f in families};assert len(fam)==160
 core={s:files[s+'_core'] for s in ['pilot','main']}
 assert len(core['pilot'])==720 and len(core['main'])==2160
 assert {r['family_id'] for r in core['pilot']}.isdisjoint({r['family_id'] for r in core['main']})
 for split,rows in core.items():
  grouped=defaultdict(list)
  for r in rows:grouped[r['family_id']].append(r)
  assert len(grouped)==(40 if split=='pilot' else 120)
  for fid,rr in grouped.items():
   assert len(rr)==18 and len({(r['knowledge'],r['composition'],r['context']) for r in rr})==18
   assert len({r['verb'] for r in rr})==len({r['name'] for r in rr})==len({r['nonce'] for r in rr})==1
   for r in rr:
    assert r['gold']==gold(r['state']['admissible_histories'],r['composition'])
    if r['knowledge']=='real':assert LEXICON[r['verb']][1] in r['premise'] and LEXICON[r['verb']][2] in r['hypothesis']
    if r['context']=='cancelling':assert 'permanent' in r['premise'] and ('resumption' in r['premise'] or 'continuation' in r['premise'])
    assert r['human_validated'] is False
    assert not re.search(r'\b(entailed|contradicted|gold label|family_id)\b',r['premise'],re.I)
   assert Counter(r['gold'] for r in rr)=={'entailed':12,'contradicted':3,'unknown':3}
 for name,rows in files.items():
  assert len({r['item_id'] for r in rows})==len(rows),name
  # Main Artificial items intentionally share logic and may share wording; metadata IDs do not prove independence.
  if name.endswith('_prior'):
   groups=defaultdict(list)
   for r in rows:groups[(r['family_id'],r['context'])].append(r)
   for rr in groups.values():
    assert len(rr)==2 and {r['prior'] for r in rr}=={'high','low'}
    assert len({r['hypothesis'] for r in rr})==1 and len({r['gold'] for r in rr})==1
    assert all(r['knowledge']=='real' and r['composition']=='bounded' for r in rr)
 for v in ['label_order','template_ood','name','label_only','natural_rule','structural_rule']:
  assert len(files[v])==288 and len({r['family_id'] for r in files[v]})==24
 assert len(files['real_definition'])==96
 nonce=json.loads((ROOT/'config/nonce_lexicon.json').read_text());dictionary_path=Path('/usr/share/dict/words')
 assert nonce['common_word_collisions']==[] and len(nonce['dictionary_sha256'])==64
 if dictionary_path.exists():
  dictionary={x.strip().lower() for x in dictionary_path.read_text().splitlines()};assert not (set(nonce['forms'])&dictionary)
  dictionary_validation='current_exact_dictionary' if hashlib.sha256(dictionary_path.read_bytes()).hexdigest()==nonce['dictionary_sha256'] else 'current_other_dictionary'
 else:dictionary_validation='historical_frozen_audit_only; current dictionary unavailable'
 original=json.loads((ROOT/'data/original/upstream/data/imperfectiveNLI.json').read_text());normalize=lambda x:re.sub(r'\s+',' ',x.lower()).strip()
 orig={(normalize(r['premise']),normalize(r['hypothesis'])) for r in original};assert not any((normalize(r['premise']),normalize(r['hypothesis'])) in orig for rows in core.values() for r in rows)
 # Deliberately measure equivalence rather than count paraphrases as independent logic.
 surface={n:{'items':len(rr),'unique_premise_hypothesis':len({(r['premise'],r['hypothesis']) for r in rr}),'gold_counts':dict(Counter(r['gold'] for r in rr))} for n,rr in files.items()}
 mainlogic=Counter((r['knowledge'],str(r['state']['admissible_histories']),r['composition']) for r in core['main'])
 report={'mechanical_checks':'passed','human_review_completed':False,'independent_prior_ratings':False,'scope':'intended-reading provisional stimuli','files':surface,'nonce_dictionary_validation':dictionary_validation,'nonce_forms':len(nonce['forms']),'finite_logic_classes_main':len(mainlogic),'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in base.glob('*.jsonl')},'limitations':['Natural-language intended readings unvalidated by independent humans','Abstract conditions use repeated logic structures with scenario/lexeme variation, not independent logical mechanisms','Prior contrast not validated; exploratory only']}
 (ROOT/'reports/data_validation.json').write_text(json.dumps(report,indent=2)+'\n');print('Mechanical validation PASS; independent human validation NOT performed.')
 return report
if __name__=='__main__':validate()
