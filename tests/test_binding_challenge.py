"""Semantic/counterbalancing contracts for the supplementary challenge."""
import unittest,json,sys,hashlib,importlib.util
from pathlib import Path
from collections import defaultdict,Counter
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from event_completion.semantics import gold
from event_completion import runner_main
import tempfile,shutil
main_jobs=runner_main.make_jobs
from event_completion.runner_binding import make_jobs as binding_jobs
spec=importlib.util.spec_from_file_location('binding_generator',ROOT/'scripts/build_binding_challenge.py')
generator=importlib.util.module_from_spec(spec);spec.loader.exec_module(generator)
class BindingContract(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.rows=[json.loads(l) for l in (ROOT/'data/supplementary/reviewer_binding.jsonl').read_text().splitlines()]
  cls.protocol=json.loads((ROOT/'reports/reviewer_binding_protocol.json').read_text())
 def test_oracle_and_gold_balance(self):
  self.assertEqual(len(self.rows),720)
  for r in self.rows:self.assertEqual(gold(r['compatible_histories'],r['composition']),r['gold'])
  self.assertEqual(Counter(r['gold'] for r in self.rows),Counter(entailed=288,contradicted=216,unknown=216))
 def test_shared_premise_and_surface_ceiling(self):
  pairs=defaultdict(list);premises=defaultdict(set);signatures=defaultdict(Counter)
  for r in self.rows:
   pairs[r['pair_id']].append(r)
   premises[(r['family_id'],tuple(r['status_pair']),r['swap'],r['knowledge'])].add(r['premise'])
   signatures[generator.signature(r['premise'],r['hypothesis'])][r['gold']]+=1
  self.assertTrue(all(len(p)==1 for p in premises.values()))
  for p in pairs.values():
   self.assertEqual(len(p),2)
   self.assertEqual(generator.signature(p[0]['premise'],p[0]['hypothesis']),generator.signature(p[1]['premise'],p[1]['hypothesis']))
  self.assertEqual(sum(max(c.values()) for c in signatures.values())/720,.6)
 def test_unseen_lexicon_and_frozen_source(self):
  old=[json.loads(l) for l in (ROOT/'data/generated/pilot_core.jsonl').read_text().splitlines()]
  self.assertFalse(set(r['verb'] for r in old)&set(self.protocol['held_out_lemmas']))
  for path,key in [('data/supplementary/reviewer_binding.jsonl','dataset_sha256'),('scripts/build_binding_challenge.py','generator_sha256'),('src/event_completion/runner_binding.py','collector_sha256')]:
   source=ROOT/path if key=='dataset_sha256' else ROOT/'data/frozen/reviewer_binding_collection'/path
   self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),self.protocol[key])
 def test_main_inference_payload_identity(self):
  args=SimpleNamespace(datasets='reviewer_binding',models=','.join(self.protocol['models']),items_per_model=None)
  expected=[j['payload'] for j in binding_jobs(args)]
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);(root/'config').mkdir();(root/'data/generated').mkdir(parents=True)
   shutil.copyfile(ROOT/'config/runtime_main.json',root/'config/runtime_main.json')
   shutil.copyfile(ROOT/'data/supplementary/reviewer_binding.jsonl',root/'data/generated/reviewer_binding.jsonl')
   oldroot=runner_main.ROOT
   try:
    runner_main.ROOT=root
    self.assertEqual([j['payload'] for j in main_jobs(args)],expected)
   finally:runner_main.ROOT=oldroot
 def test_definition_precision_preserves_all_histories_and_counterbalance(self):
  revised=[json.loads(l) for l in (ROOT/'data/supplementary/reviewer_binding_v2.jsonl').read_text().splitlines()]
  changes=0;counts=defaultdict(Counter)
  for before,after in zip(self.rows,revised):
   premise=after['premise'];same=dict(after);same['premise']=before['premise']
   self.assertEqual(before,same)
   if before['knowledge']=='nonce':
    self.assertIn('requires reaching at least two positive coverage landmarks',premise)
    self.assertNotIn('requires an observed increase',premise);changes+=1
   else:self.assertEqual(before['premise'],premise)
   counts[generator.signature(premise,after['hypothesis'])][after['gold']]+=1
  self.assertEqual(changes,240)
  self.assertEqual(sum(max(c.values()) for c in counts.values())/720,.6)
if __name__=='__main__':unittest.main()
