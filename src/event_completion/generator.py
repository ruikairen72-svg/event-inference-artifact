"""Deterministic, theory-constrained candidate stimuli. No human validation is implied."""
import hashlib,json,random,re
from pathlib import Path
from .semantics import gold,histories
ROOT=Path(__file__).resolve().parents[2]
SEED=20271007
NAMES=['Maya','Elena','Noah','Priya','Alex','Sam','Leila','Owen','Nora','Isaac','Avery','Zara','Lucas','Iris']
LEXICON={
'drink':('quantity','drinking','drank',['water','tea','coffee','milk','orange juice','broth','lemonade','cocoa','apple juice','kefir','soda','coconut water','grape juice','mineral water']),
'eat':('quantity','eating','ate',['rice','porridge','custard','yogurt','applesauce','mashed potato','pudding','cereal','oatmeal','soup','salad','noodles','stew','pasta']),
'pour':('quantity','pouring','poured',['water','tea','coffee','milk','orange juice','broth','lemonade','cocoa','apple juice','kefir','soda','coconut water','grape juice','mineral water']),
'collect':('quantity','collecting','collected',['pebbles','beads','shells','coins','marbles','leaves','stones','buttons','stamps','screws','tokens','blocks','seeds','bottle caps']),
'walk':('path','walking','walked',['corridor','garden path','footpath','hallway','trail','boardwalk','promenade','platform','passageway','walkway','pier','lane','bridge','tunnel']),
'run':('path','running','ran',['track','trail','footpath','corridor','lane','path','walkway','promenade','boardwalk','platform','passageway','bridge','pier','hallway']),
'swim':('path','swimming','swam',['pool lane','canal section','marked water lane','practice lane','indoor pool lane','outdoor pool lane','training lane','river lane','lagoon lane','lake lane','channel lane','reservoir lane','exercise lane','water course']),
'crawl':('path','crawling','crawled',['tunnel','corridor','passageway','crawlway','hallway','practice lane','narrow path','covered walkway','training lane','underpass','passage','low tunnel','narrow corridor','short tunnel']),
'copy':('incremental','copying','copied',['paragraph','passage','recipe','poem','report','letter','note','transcript','speech','article','story','list','diary entry','essay']),
'transcribe':('incremental','transcribing','transcribed',['interview','speech','lecture','conversation','discussion','announcement','dictation','podcast','message','story','debate','presentation','testimony','dialogue']),
'read':('incremental','reading','read',['paragraph','passage','recipe','poem','report','letter','note','transcript','speech','article','story','list','diary entry','essay']),
'write':('incremental','writing','wrote',['paragraph','passage','recipe','poem','report','letter','note','transcript','speech','article','story','list','diary entry','essay'])}
def h(x):return hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest()
def words():return {x.strip().lower() for x in Path('/usr/share/dict/words').read_text().splitlines()}
def forms():
 rng=random.Random(SEED);dictionary=words();out=[]
 while len(out)<48:
  x=''.join(rng.choice(['vaz','kel','jom','zef','pav','nuv','taz','vek','zul','fim']) for _ in range(2))
  if x not in dictionary and x not in out:out.append(x)
 return out
# Frozen forms make replay independent of an operating-system word list.
_nonce_path=ROOT/'config/nonce_lexicon.json'
if _nonce_path.exists():
 _nonce_record=json.loads(_nonce_path.read_text())
 assert _nonce_record['seed']==SEED
 NONCES=_nonce_record['forms']
 assert len(NONCES)==48 and len(set(NONCES))==48
else:
 NONCES=forms()
def vps(verb,obj,composition):
 b=composition=='bounded';s=LEXICON[verb][0]
 if s=='path':return ('to the marked far end of the '+obj) if b else ('along the '+obj)
 if s=='incremental':
  if verb=='transcribe':return ('the entire specified recording of the '+obj) if b else ('speech from the specified recording of the '+obj)
  return ('the entire specified '+obj) if b else ('text from the specified '+obj)
 if verb=='collect':return ('exactly ten '+obj) if b else obj
 return ('exactly one measured '+('bowl' if verb=='eat' else 'glass')+' of '+obj) if b else obj

def render_real(f,composition,context,template=0,prior=None):
 name,verb,obj=f['name'],f['verb'],f['object'];ing,past=LEXICON[verb][1:3];vp=vps(verb,obj,composition);s=f['stratum'];bounded=composition=='bounded'
 prior_setup=''
 if prior:
  # Fixed endpoint type, change only quantitative extent/effort. Intended, not human validated.
  attr='small' if prior=='high' else 'large'
  if s=='path':prior_setup=f'The marked far end of the {obj} was '+('nearby.' if prior=='high' else 'far away.')
  elif s=='incremental':prior_setup='The specified '+('recording' if verb=='transcribe' else obj)+' was '+('very short.' if prior=='high' else 'very long.')
  else:prior_setup='Each relevant '+('object' if verb=='collect' else 'measured portion')+' was '+attr+'.'
 lead=f'{name} was {ing} {vp}.' if template==0 else f'A witness observed {name} {ing} {vp}.'
 if s=='path':witness=f'{name} actually traversed a nonzero stretch of the {obj} in that manner.'
 elif s=='incremental':witness=f'{name} actually '+past+' several words from the '+('recording' if verb=='transcribe' else 'specified '+obj)+'.'
 elif verb=='collect':witness=f'{name} actually collected at least two {obj}.'
 else:witness=f'{name} actually {past} a nonzero amount of {obj}.'
 if context=='neutral': evidence='Nothing in the account says whether any required endpoint was reached by the end of the reporting interval.'
 elif bounded and context=='supportive':
  if s=='path':evidence=f'{name} reached the marked far end of the {obj} before the interval ended.'
  elif s=='incremental':evidence=f'{name} finished {ing} every word of the specified '+('recording of the '+obj if verb=='transcribe' else obj)+' before the interval ended.'
  elif verb=='collect':evidence=f'{name} collected exactly ten {obj} before the interval ended.'
  else:evidence=f'{name} finished {ing} the whole measured '+('bowl' if verb=='eat' else 'glass')+' of '+obj+' before the interval ended; none of that portion remained.'
 elif bounded:
  if s=='path':evidence=f'{name} stopped halfway, never reaching the marked far end of the {obj} during this episode.'
  elif s=='incremental':evidence=f'{name} stopped halfway through the specified '+('recording' if verb=='transcribe' else obj)+'; half of its words were never '+past+' during this episode.'
  elif verb=='collect':evidence=f'{name} stopped after collecting only two of the required ten {obj}.'
  else:evidence=f'{name} stopped while half of the measured '+('bowl' if verb=='eat' else 'glass')+' of '+obj+' still remained; that remainder was never '+past+' during this episode.'
  evidence+=' The episode then ended permanently and there was no resumption or replacement episode through the end of the interval.'
 elif context=='supportive':evidence='The activity continued for a while and then ended before the reporting interval ended.'
 else:evidence='The activity ended permanently midway through the interval, with no later resumption or replacement episode in that interval.'
 scope='The reporting interval lasted ten minutes. This is a single episode.'
 if bounded:scope+=' Only the specified target, quantity, or route was involved; there were no additional targets or quantities in this episode.'
 pre=' '.join(x for x in [scope,prior_setup,lead,witness,evidence] if x)
 target=f'{name} {past} {vp} during this episode before the reporting interval ended.'
 return pre,target

def render_artificial(f,composition,context,micro=False,template=0):
 name=f['name'];root=f['nonce'];b=composition=='bounded'
 if micro:
  definition=f'Event system {f["code"]}: an agent acts through ordered checkpoints 1, 2, 3, 4. An activity assertion is true after checkpoints 1 and 2 occur. A full-route assertion is true only if checkpoint 4 occurs. All assertions refer to the same episode and reporting interval.'
  description='full route' if b else 'activity'
  pre=definition+f' {name} was performing the {description} of this system. Checkpoints 1 and 2 actually occurred.'
  if context=='neutral':pre+=' The account does not specify whether checkpoints 3 and 4 occurred before the interval ended.'
  elif context=='supportive':pre+=' Checkpoints 3 and 4 also occurred before the interval ended.'
  else:pre+=' The episode ended permanently after checkpoint 2; checkpoints 3 and 4 never occurred, and no continuation or replacement occurred through the end of the interval.'
  target=f'{name} performed the '+('full route' if b else 'activity')+' of this system in this episode before the interval ended.'
  if template:pre=pre.replace('actually occurred','were actually observed').replace('The account does not specify','The record leaves unspecified')
  return pre,target
 definition=f'In this task, to {root} means to continuously advance through units of a target, one unit after another. The word has no fixed endpoint by itself. {root.capitalize()}ing is its ongoing form; {root}ed is its past form. With "the entire specified target", the past form requires all four units to have been traversed; with "units of the target", traversing at least two units establishes the past activity statement. All statements refer to the same episode and reporting interval.'
 vp='the entire specified target' if b else 'units of the target'
 lead=f'{name} was {root}ing {vp}. Units 1 and 2 were actually traversed.'
 if context=='neutral':evidence='The account does not specify whether units 3 and 4 were traversed before the interval ended.'
 elif context=='supportive':evidence='Units 3 and 4 were also traversed before the interval ended.'
 else:evidence='The episode ended permanently after unit 2; units 3 and 4 were never traversed and no continuation or replacement occurred through the end of the interval.'
 if template:lead=lead.replace('were actually traversed','were actually covered')
 return ' '.join([definition,lead,evidence]),f'{name} {root}ed {vp} during this episode before the reporting interval ended.'

def record(f,knowledge,composition,context,prior=None,variant='baseline'):
 template=f['template'];ff=dict(f)
 if variant=='name':ff['name']='Taylor'
 if variant=='template_ood':template=0
 if knowledge=='real':premise,target=render_real(ff,composition,context,template,prior)
 else:premise,target=render_artificial(ff,composition,context,knowledge=='micro',template)
 if variant=='template_ood':
  premise='Episode record for '+ff['name']+' — '+premise.replace('reporting interval','observation window').replace('The episode then ended permanently','This episode ceased for good').replace('The account does not specify','No entry in this record establishes').replace('Nothing in the account says whether','No entry in this record establishes whether').replace(ff['name']+' was ', 'An ongoing action by '+ff['name']+' was observed: ')
  target='Claim about this record: '+target
 if variant=='real_definition' and knowledge=='real':premise='For this task, the entire specified target or exact quantity must be fully covered, and a marked path goal must be reached. A nonzero witnessed activity can have occurred without any terminal condition. '+premise
 hh=histories(context);label=gold(hh,composition)
 ident=':'.join([f['family_id'],knowledge,composition,context,prior or 'none',variant])
 return {'item_id':ident,'family_id':f['family_id'],'split':f['split'],'verb':f['verb'],'stratum':f['stratum'],'knowledge':knowledge,'composition':composition,'context':context,'prior':prior,'variant':variant,'template':template,'name':ff['name'],'object':f['object'],'nonce':f['nonce'],'premise':premise,'hypothesis':target,'gold':label,'state':{'admissible_histories':hh,'required_endpoint':4,'process_witness':[1,2],'episode_closed':context!='neutral'},'gold_source':'finite_history_oracle_under_intended_reading','human_validated':False}
def dump(path,data):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in data))
def generate():
 rng=random.Random(SEED); families=[];index=0
 for vi,(verb,(stratum,ing,past,objects)) in enumerate(LEXICON.items()):
  for oi,obj in enumerate(objects):
   index+=1;split='main' if oi<10 else 'pilot'
   families.append({'family_id':f'F{index:03d}','verb':verb,'stratum':stratum,'object':obj,'name':NAMES[(oi+vi)%len(NAMES)],'nonce':NONCES[vi*4+(oi%4)],'code':f'S{index:03d}','template':(oi+vi)%2,'split':split})
 # There are 48 pilot candidates; retain 40 with stratum allocation 14/13/13.
 pilot=[]
 for st,n in [('quantity',14),('path',13),('incremental',13)]:
  pool=[f for f in families if f['split']=='pilot' and f['stratum']==st];rng.shuffle(pool);pilot+=pool[:n]
 families=[f for f in families if f['split']=='main']+pilot
 allitems={}
 for split in ['pilot','main']:
  fs=[f for f in families if f['split']==split]
  core=[record(f,k,b,c) for f in fs for k in ['real','nonce','micro'] for b in ['bounded','unbounded'] for c in ['neutral','supportive','cancelling']]
  rng.shuffle(core);allitems[split]=core;dump(ROOT/f'data/generated/{split}_core.jsonl',core)
  chosen=[]
  for st,n in [('quantity',14 if split=='main' else 4),('path',13 if split=='main' else 3),('incremental',13 if split=='main' else 3)]:
   pool=[f for f in fs if f['stratum']==st];rng.shuffle(pool);chosen+=pool[:n]
  wk=[record(f,'real','bounded',c,prior) for f in chosen for prior in ['high','low'] for c in ['neutral','supportive','cancelling']];dump(ROOT/f'data/generated/{split}_prior.jsonl',wk)
  nc=20 if split=='pilot' else 60
  labels=[]
  for i in range(nc):
   label=['entailed','contradicted','unknown'][i%3];name=NAMES[i%len(NAMES)];obj=f'object number {i+1}'
   pre={'entailed':f'{name} moved {obj} to the marked location during the interval.','contradicted':f'{name} never moved {obj} to the marked location during the interval.','unknown':f'The record contains no information about whether {name} moved {obj} to the marked location during the interval.'}[label]
   labels.append({'item_id':f'{split}_L{i:03d}','family_id':f'{split}_L{i:03d}','split':split,'verb':'move','stratum':'label_control','knowledge':'real','composition':'bounded','context':'control','prior':None,'variant':'baseline','template':i%2,'name':name,'premise':pre,'hypothesis':f'{name} moved {obj} to the marked location during the interval.','gold':label,'gold_source':'explicit_truth_control','human_validated':False})
  dump(ROOT/f'data/generated/{split}_labels.jsonl',labels)
 main=[f for f in families if f['split']=='main'];diag=[]
 for st in ['quantity','path','incremental']:
  pool=[f for f in main if f['stratum']==st];rng.shuffle(pool);diag+=pool[:10]
 robust=[]
 for st in ['quantity','path','incremental']:robust += [f for f in diag if f['stratum']==st][:8]
 dump(ROOT/'data/generated/stress_core.jsonl',[x for x in allitems['main'] if x['family_id'] in {f['family_id'] for f in diag}])
 prior_main=[json.loads(l) for l in (ROOT/'data/generated/main_prior.jsonl').read_text().splitlines()];eligible=sorted(set(x['family_id'] for x in prior_main));rng.shuffle(eligible);selected=set(eligible[:20]);dump(ROOT/'data/generated/stress_prior.jsonl',[x for x in prior_main if x['family_id'] in selected])
 variants=['label_order','template_ood','name','label_only','natural_rule','structural_rule']
 for v in variants:dump(ROOT/f'data/generated/{v}.jsonl',[record(f,k,b,c,variant=v) for f in robust for k in ['real','nonce','micro'] for b in ['bounded','unbounded'] for c in ['neutral','cancelling']])
 # Only Real definition actually changes; unchanged artificial baselines are reused.
 dump(ROOT/'data/generated/real_definition.jsonl',[record(f,'real',b,c,variant='real_definition') for f in robust for b in ['bounded','unbounded'] for c in ['neutral','cancelling']])
 dump(ROOT/'data/generated/families.jsonl',families)
 nonce_path=ROOT/'config/nonce_lexicon.json'
 if nonce_path.exists():
  assert json.loads(nonce_path.read_text())['forms']==NONCES
 else:
  nonce_path.write_text(json.dumps({'seed':SEED,'forms':NONCES,'dictionary':'/usr/share/dict/words','dictionary_sha256':hashlib.sha256(Path('/usr/share/dict/words').read_bytes()).hexdigest(),'common_word_collisions':[]},indent=2)+'\n')
 print('Generated intended-reading candidates:',{s:len(v) for s,v in allitems.items()},'families',len(families))
if __name__=='__main__':generate()
