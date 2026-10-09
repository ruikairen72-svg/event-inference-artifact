import unittest
from event_completion.secondary import bh,analyze

class SecondaryIntegrity(unittest.TestCase):
    def test_bh_keeps_unavailable_test_in_family(self):
        got=bh([.01,.04,None,.03])
        self.assertAlmostEqual(got[0],.04)
        self.assertAlmostEqual(got[1],.04*4/3)
        self.assertIsNone(got[2])
        self.assertAlmostEqual(got[3],.04*4/3)
    def rows(self):
        rows=[]
        for k in ['real','nonce','micro']:
            for c in ['bounded','unbounded']:
                for x in ['neutral','supportive','cancelling']:
                    rows.append({'model':'test','dataset':'main_core','correct':True,
                      'parsed':{'judgment':'entailed','hypothesis_probability':1.0},
                      'item':{'family_id':'F1','verb':'read','knowledge':k,'composition':c,'context':x}})
        return rows
    def test_definition_control_uses_changed_real_cells_only(self):
        rows=self.rows()
        rows += [{**r,'dataset':'real_definition','correct':False} for r in rows if r['item']['knowledge']=='real' and r['item']['context']!='supportive']
        report=analyze(rows,draws=20)
        r=next(r for r in report if r['metric']=='variant_minus_baseline_accuracy')
        self.assertEqual(r['matched_planned_cells'],4)
        self.assertEqual(r['result']['estimate'],-1)
    def test_missing_probability_is_not_imputed(self):
        rows=self.rows();rows[0]['parsed']=None;rows[0]['correct']=False
        report=analyze(rows,draws=20)
        r=next(r for r in report if r['metric']=='cs_q' and r['knowledge']=='real' and r['context']=='neutral')
        self.assertEqual(r['planned_families'],1)
        self.assertEqual(r['valid_families'],0)
        self.assertIsNone(r['result'])

if __name__=='__main__': unittest.main()
