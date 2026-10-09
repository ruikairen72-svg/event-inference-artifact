"""Precise occurrence definition: no dependence on observation availability.

Retains original stimuli/results. Replaces all and only the 240 Nonce glosses,
not their histories, labels, records, actors or hypotheses.
"""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def main():
 source=ROOT/'data/supplementary/reviewer_binding.jsonl'
 rows=[json.loads(l) for l in source.read_text().splitlines()];changed=0
 old='requires an observed increase between two positive coverage landmarks'
 new='requires reaching at least two positive coverage landmarks'
 for r in rows:
  if r['knowledge']=='nonce':
   assert r['premise'].count(old)==1
   r['premise']=r['premise'].replace(old,new);changed+=1
 assert changed==240
 out=ROOT/'data/supplementary/reviewer_binding_v2.jsonl'
 out.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
 p=ROOT/'reports/reviewer_binding_definition_protocol.json';protocol=json.loads(p.read_text())
 h=hashlib.sha256(out.read_bytes()).hexdigest()
 if 'dataset_sha256' in protocol:assert protocol['dataset_sha256']==h
 else:
  protocol.update({'dataset_sha256':h,'source_dataset_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'repair_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
  p.write_text(json.dumps(protocol,indent=2)+'\n')
 print('Definition repair: 240/720 item texts; all gold and histories unchanged; 1680 new payloads across seven models.')
if __name__=='__main__':main()
