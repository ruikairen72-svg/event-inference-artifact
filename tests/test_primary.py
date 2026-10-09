import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from event_completion.primary import extract,holm
class PrimaryContracts(unittest.TestCase):
 def test_holm_monotone_and_missing_reserved(self):self.assertEqual(holm([.01,.04,.03,None]),[.04,.09,.09,None])
 def test_missing_q_retained_with_adverse_bounds(self):
  rows=[]
  for k,c,q in [('real','bounded',.2),('real','unbounded',.8),('nonce','bounded',None),('nonce','unbounded',.7)]:
   rows.append({'model':'M','dataset':'main_core','item':{'family_id':'F','verb':'run','knowledge':k,'composition':c,'context':'neutral'},'parsed':{'hypothesis_probability':q} if q is not None else None})
  r=extract(rows,'M')['neutral_cs_real_minus_nonce'][0]
  self.assertFalse(r['valid']);self.assertIsNone(r['value']);self.assertAlmostEqual(r['lower'],-.9);self.assertAlmostEqual(r['upper'],.1)
 def test_all_planned_correctness_counts_missing_in_rule(self):
  rows=[]
  for k in ['real','nonce','micro']:
   for c in ['bounded','unbounded']:
    for x in ['neutral','cancelling']:
     item={'family_id':'F','verb':'run','knowledge':k,'composition':c,'context':x}
     rows.extend([{'model':'M','dataset':'main_core','item':item,'correct':False},{'model':'M','dataset':'structural_rule','item':item,'correct':True}])
  self.assertEqual(extract(rows,'M')['structural_rule_minus_baseline_accuracy'][0]['value'],1)
if __name__=='__main__':unittest.main()
