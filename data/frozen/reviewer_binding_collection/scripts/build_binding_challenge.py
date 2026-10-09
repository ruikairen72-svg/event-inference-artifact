"""Reviewer-driven shared-premise role-binding challenge, frozen before collection.

Each swapped pair has identical lowercase word counts, with different target
truth conditions. Uses the unchanged finite-history oracle, not human labels.
"""
from pathlib import Path
from collections import Counter, defaultdict
import hashlib, json, re, sys, datetime
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from event_completion.semantics import gold

# Six main lemmas and six lemmas absent from the original pilot/main lexicon.
# Four ordered coverage landmarks encode the explicitly measured episode.
LEXICON = [
 ('drink','quantity',True,'drank','water in her glass','water'),
 ('collect','quantity',True,'collected','tokens in her tray','tokens'),
 ('walk','path',True,'walked','her marked corridor','along her marked corridor'),
 ('swim','path',True,'swam','her marked lane','along her marked lane'),
 ('read','incremental',True,'read','words on her assigned page','words'),
 ('copy','incremental',True,'copied','symbols on her assigned card','symbols'),
 ('sip','quantity',False,'sipped','juice in her cup','juice'),
 ('consume','quantity',False,'consumed','rice in her bowl','rice'),
 ('hike','path',False,'hiked','her marked trail','along her marked trail'),
 ('paddle','path',False,'paddled','her marked canal','along her marked canal'),
 ('scan','incremental',False,'scanned','lines on her assigned sheet','lines'),
 ('trace','incremental',False,'traced','segments of her assigned drawing','segments'),
]
H = {'idle':[[]], 'open':[[1,2,'STOP'],[1,2,3,4,'STOP']],
     'partial':[[1,2,'STOP']], 'complete':[[1,2,3,4,'STOP']],
     'unobserved':[[],[1,2,'STOP'],[1,2,3,4,'STOP']]}
PAIRS = [('idle','open'),('open','partial'),('partial','complete'),
         ('complete','unobserved'),('unobserved','idle')]
LABELS = ['entailed','contradicted','unknown']

def render(lex, knowledge, states):
 lemma,stratum,seen,past,obj,activity = lex
 if stratum == 'path':
  bv=f'{past} the entire length of {obj}'
  av=f'{past} some distance {activity}'
 else:
  bv=f'{past} all the {obj}'
  av=f'{past} some {activity}'
 if knowledge == 'real':
  intro=(f'The interval runs from minute 0 through minute 10. Nora and Alex have separate, identical assignments involving {obj.replace("her ","a ")}. '
         f'Coverage is monotone within this interval: the same part is not counted twice, and coverage is measured on the original assignment of that actor. '
         f'An observed increase from one quarter to one half of an assignment establishes some {lemma} activity; full coverage establishes its endpoint. '
         'The following are the only observations available for the interval. ')
  facts={
   'idle':f'{{actor}} had zero {lemma} coverage at every moment from minute 0 through minute 10.',
   'open':f'{{actor}} increased {lemma} coverage from one quarter to one half between minute 2 and minute 3.',
   'partial':f'{{actor}} increased {lemma} coverage from one quarter to one half between minute 2 and minute 3, and had total coverage of exactly one half at minute 10.',
   'complete':f'{{actor}} increased {lemma} coverage from one quarter to one half between minute 2 and minute 3, and had full coverage at minute 10.',
   'unobserved':'{actor} was recorded in a room at a temperature of twenty degrees at minute 3.'}
  hypotheses={'bounded':f'Nora {bv} during the interval.', 'unbounded':f'Nora {av} during the interval.'}
 elif knowledge == 'nonce':
  stem='dax'+str(LEXICON.index(lex)+1)
  intro=(f'The interval runs from minute 0 through minute 10. Nora and Alex have separate, identical assignments. '
         f'The invented verb {stem} means making monotone coverage progress on an assignment. '
         f'"{stem}-all" requires full coverage; "{stem}-some" requires an observed increase between two positive coverage landmarks. '
         'The same part is not counted twice. The following are the only observations available for the interval. ')
  facts={
   'idle':f'{{actor}} had zero {stem} coverage at every moment from minute 0 through minute 10.',
   'open':f'{{actor}} increased {stem} coverage from one quarter to one half between minute 2 and minute 3.',
   'partial':f'{{actor}} increased {stem} coverage from one quarter to one half between minute 2 and minute 3, and had total coverage of exactly one half at minute 10.',
   'complete':f'{{actor}} increased {stem} coverage from one quarter to one half between minute 2 and minute 3, and had full coverage at minute 10.',
   'unobserved':'{actor} was recorded in a room at a temperature of twenty degrees at minute 3.'}
  hypotheses={'bounded':f'Nora {stem}-all during the interval.', 'unbounded':f'Nora {stem}-some during the interval.'}
 else:
  process='P'+str(LEXICON.index(lex)+1)
  intro=(f'Within interval I, Nora and Alex each have a separate process {process}. '
         'A history contains increasing stages 1,2,3,4 and optionally STOP; stages cannot be repeated or reversed. '
         'B(actor) holds iff stage 4 occurs within I. A(actor) holds iff at least two positive stages occur within I. '
         'An unobserved process can have no stages, stop after stage 2, or reach stage 4. '
         'The following constraints are the only observations available for I. ')
  facts={
   'idle':'{actor}: no stage occurred at any time within I.',
   'open':'{actor}: stages 1 and 2 occurred by time 3 within I.',
   'partial':'{actor}: stages 1 and 2 occurred by time 3 within I, and the greatest stage reached by the end of I was 2.',
   'complete':'{actor}: stages 1 and 2 occurred by time 3 within I, and the greatest stage reached by the end of I was 4.',
   'unobserved':'{actor}: room temperature was twenty degrees at time 3 within I.'}
  hypotheses={'bounded':'B(Nora) holds within I.', 'unbounded':'A(Nora) holds within I.'}
 premise=intro+' '.join(facts[state].format(actor=actor) for actor,state in zip(['Nora','Alex'],states))
 return premise, hypotheses

def signature(p,h):
 return tuple(sorted(Counter(re.findall(r'\b\w+\b',(p+' '+h).lower())).items()))

def main():
 rows=[]
 for li,lex in enumerate(LEXICON):
  for pi,pair in enumerate(PAIRS):
   for swap in [0,1]:
    states=pair if not swap else pair[::-1]
    for k in ['real','nonce','micro']:
     premise,hyps=render(lex,k,states)
     for comp,hyp in hyps.items():
      rows.append({'item_id':f'RB{li+1:02d}_{pi}_{swap}_{k}_{comp}',
       'family_id':f'RB{li+1:02d}','lemma':lex[0],'verb_class':lex[1],
       'lexical_split':'seen' if lex[2] else 'held_out', 'pair_id':f'RB{li+1:02d}_{pi}_{k}_{comp}',
       'status_pair':list(pair),'swap':swap,'target_actor':'Nora',
       'actor_status':dict(zip(['Nora','Alex'],states)), 'compatible_histories':H[states[0]],
       'composition':comp,'knowledge':k,'context':states[0], 'variant':'baseline',
       'premise':premise,'hypothesis':hyp,'gold':gold(H[states[0]],comp)})
 assert len(rows)==720 and len({r['item_id'] for r in rows})==720
 pairs=defaultdict(list); premises=defaultdict(set); collisions=defaultdict(Counter)
 for r in rows:
  pairs[r['pair_id']].append(r)
  premises[(r['family_id'],tuple(r['status_pair']),r['swap'],r['knowledge'])].add(r['premise'])
  collisions[signature(r['premise'],r['hypothesis'])][r['gold']]+=1
 assert all(len(p)==1 for p in premises.values())
 assert all(len(p)==2 and signature(p[0]['premise'],p[0]['hypothesis'])==signature(p[1]['premise'],p[1]['hypothesis']) for p in pairs.values())
 ceiling=sum(max(c.values()) for c in collisions.values())/len(rows)
 assert ceiling==.6
 ds=ROOT/'data/generated/reviewer_binding.jsonl';ds.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
 specs=json.loads((ROOT/'config/runtime_models.json').read_text())['models']
 modelids=[m['id'] for m in specs if m['id'] in ['qwen/qwen3-8b','meta-llama/llama-3.1-8b-instruct','mistralai/ministral-8b-2512','google/gemma-3-12b-it','qwen/qwen3-14b','qwen/qwen3-32b','deepseek/deepseek-v3.2']]
 assert len(modelids)==7
 protocol={'status':'frozen_before_any_challenge_API_collection','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'analysis_status':'post-review supplementary; original primary/secondary families unchanged',
  'dataset_sha256':hashlib.sha256(ds.read_bytes()).hexdigest(),'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
  'items_per_model':len(rows),'models':modelids,'planned_calls':len(rows)*len(modelids),'run_cap_usd':1.25,
  'lexical_blocks':12,'held_out_lemmas':[l[0] for l in LEXICON if not l[2]],'seen_lemmas':[l[0] for l in LEXICON if l[2]],
  'gold_counts':dict(Counter(r['gold'] for r in rows)),'exact_unigram_ceiling':ceiling,
  'bounded_unigram_ceiling':.5,'activity_unigram_ceiling':.7,
  'measures':['all-item accuracy','macro recall','per-presentation accuracy','per-target gold recall','different-gold pair both-correct rate','seen/held-out accuracy','per-lemma and stratum accuracy'],
  'uncertainty':'Percentile bootstrap of 12 lemma blocks, 10000 draws, seed 20271009; 6-block split intervals separately; descriptive, no new primary tests.',
  'assumptions':['One finite reporting interval; monotone coverage on separate identical actor assignments','Coverage landmarks define observed occurrence; full coverage defines endpoint','Only stated observations constrain histories; unrelated temperature record does not imply nonoccurrence','No independently observed real-world outcome claimed'],
  'checks':{'oracle_reused_unchanged':True,'shared_premise_dual_targets':True,'exact_word_multiset_collision_every_pair':True,'all_pairs_retained':True}}
 (ROOT/'reports/reviewer_binding_protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
 print(json.dumps({'items':len(rows),'planned_calls':len(rows)*7,'unigram_ceiling':ceiling,'gold':protocol['gold_counts'],'models':modelids},indent=2))
if __name__=='__main__':main()
