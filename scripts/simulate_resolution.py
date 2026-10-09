"""Design simulation, explicitly NOT model experimental data."""
from pathlib import Path
import json,itertools
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
rng=np.random.default_rng(20271007);G=12;F=10;R=1000;SD=.30
signs=np.array(list(itertools.product([-1,1],repeat=G)))
results=[]
for icc in [.2,.5]:
 for delta in [0,.05,.1,.2]:
  # Normal bounded-contrast approximation, clipped to mathematically possible [-1,1].
  shared=rng.normal(0,SD*np.sqrt(icc),(R,G,1));individual=rng.normal(0,SD*np.sqrt(1-icc),(R,G,F));samples=np.clip(delta+shared+individual,-1,1);clustermeans=samples.mean(axis=2)
  observed=abs(clustermeans.mean(axis=1));null=abs(clustermeans.dot(signs.T)/G);p=(null>=observed[:,None]-1e-12).mean(axis=1)
  results.append({'assumed_effect':delta,'assumed_sd':SD,'assumed_icc':icc,'independent_lexical_blocks':G,'families_per_block':F,'simulations':R,'uncorrected_005_rejection_fraction':float((p<=.05).mean()),'bonferroni_30_rejection_fraction':float((p<=.05/30).mean()),'mean_estimate':float(samples.mean()),'effective_n_approx':G*F/(1+(F-1)*icc)})
(ROOT/'reports/design_resolution_simulation.json').write_text(json.dumps({'source':'prospective design simulation, NOT LLM responses','seed':20271007,'model':'normal paired contrasts with lexical random component, bounded by clipping','multiplicity':'Bonferroni 30 conservative planning bound for future Holm family','results':results},indent=2)+'\n')
print('Design simulation saved. Not experimental evidence; no sample-size adaptation to pilot effects.')
