import unittest,sys,json
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from event_completion.runner import make_jobs,returned_charge
from event_completion.prompts import messages
class DataContractTests(unittest.TestCase):
 def test_same_nonce_root_changes_argument_not_root(self):
  root=Path(__file__).resolve().parents[1];rs=[json.loads(l) for l in (root/'data/generated/main_core.jsonl').read_text().splitlines()];rr=[r for r in rs if r['family_id']=='F001' and r['knowledge']=='nonce' and r['context']=='neutral'];self.assertEqual(len(rr),2);self.assertEqual(len({r['nonce'] for r in rr}),1);self.assertNotEqual(rr[0]['hypothesis'],rr[1]['hypothesis'])
 def test_failed_response_charge_and_unknown_cost_are_distinct(self):
  self.assertEqual(returned_charge({'error':{},'usage':{'cost':.01}},.1),(.01,False))
  self.assertEqual(returned_charge({'error':{}},.1),(.1,True))
  self.assertEqual(returned_charge({'usage':{'cost':float('nan')}},.1),(.1,True))
  self.assertEqual(returned_charge({'usage':{'cost':True}},.1),(.1,True))
 def test_unknown_dataset_cannot_silently_schedule_zero_calls(self):
  with self.assertRaises(ValueError):make_jobs(SimpleNamespace(datasets='unknown_dataset',models='qwen/qwen3-8b',items_per_model=None))
 def test_payload_cache_contains_decode_and_provider(self):
  jobs=make_jobs(SimpleNamespace(datasets='pilot_labels',models='qwen/qwen3-8b',items_per_model=1));p=jobs[0]['payload'];self.assertEqual(p['provider']['only'],['alibaba']);self.assertFalse(p['provider']['allow_fallbacks']);self.assertEqual(p['max_tokens'],256)
 def test_prompt_does_not_include_gold(self):
  item={'premise':'A process occurred.','hypothesis':'The endpoint was reached.','gold':'contradicted','family_id':'SECRET_ID'};text=json.dumps(messages(item));self.assertNotIn('SECRET_ID',text);self.assertNotIn('gold',text)
if __name__=='__main__':unittest.main()
