import unittest
from event_completion.analysis import cluster_ci

class ClusterIntegrity(unittest.TestCase):
 def test_missing_block_identifier_cannot_silently_drop_a_contrast(self):
  with self.assertRaises(ValueError):cluster_ci([.1,.2],['read'],b=20)
 def test_nonfinite_contrast_cannot_become_an_estimate(self):
  with self.assertRaises(ValueError):cluster_ci([.1,float('nan')],['read','copy'],b=20)
 def test_constant_conditional_sample_has_collapsed_resampling_interval(self):
  result=cluster_ci([1,1,1],['read','read','copy'],b=20)
  self.assertEqual(result['ci95'],[1,1])
  self.assertEqual(result['n_families'],3)
  self.assertEqual(result['n_lexical_blocks'],2)
  self.assertEqual(result['p_cluster_signflip'],.5)
 def test_unequal_lexical_blocks_retain_family_weighted_estimand(self):
  # Ten +.1 families, one +.5 and one -.8 give .7/12.
  # The eight lexical flips have absolute sums .3,.7,1.3,2.3,
  # each twice, so six meet the observed .7 threshold.
  result=cluster_ci([.1]*10+[.5,-.8],['read']*10+['copy','write'],b=20)
  self.assertAlmostEqual(result['estimate'],.7/12)
  self.assertEqual(result['n_families'],12)
  self.assertEqual(result['n_lexical_blocks'],3)
  self.assertEqual(result['p_cluster_signflip'],.75)

if __name__=='__main__':unittest.main()
