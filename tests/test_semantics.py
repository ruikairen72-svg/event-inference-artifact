import unittest,sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from event_completion.semantics import gold
from event_completion.prompts import parse
class OracleTests(unittest.TestCase):
 def test_neutral_is_not_closed_world(self):self.assertEqual(gold([[1,2,'STOP'],[1,2,3,4,'STOP']],'bounded'),'unknown')
 def test_destroyed_after_endpoint(self):self.assertEqual(gold([[1,2,3,4,'DESTROYED']],'bounded'),'entailed')
 def test_stopped_activity(self):self.assertEqual(gold([[1,2,'STOP']],'unbounded'),'entailed')
 def test_before_endpoint(self):self.assertEqual(gold([[1,2,'STOP']],'bounded'),'contradicted')
 def test_onset_not_enough_for_plural_activity(self):self.assertEqual(gold([[1,'STOP']],'unbounded'),'contradicted')
 def test_parser_does_not_coerce_unknown_probability(self):
  d,s=parse('{"judgment":"unknown","hypothesis_probability":0.99,"completion_probability":0.99}',{'composition':'bounded'});self.assertEqual(s,'ok');self.assertEqual(d['hypothesis_probability'],.99)
 def test_no_percent_clipping(self):self.assertEqual(parse('{"judgment":"unknown","hypothesis_probability":99,"completion_probability":99}',{'composition':'bounded'})[1],'invalid_probability')
 def test_unknown_low_probability(self):
  d,s=parse('{"judgment":"unknown","hypothesis_probability":0.01}',{'composition':'bounded'});self.assertEqual(s,'ok');self.assertEqual(d['hypothesis_probability'],.01)
if __name__=='__main__':unittest.main()
