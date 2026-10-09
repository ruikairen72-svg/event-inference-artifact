"""Retrieve the pinned public source locally; never execute upstream code."""
from pathlib import Path
import hashlib,urllib.request
ROOT=Path(__file__).resolve().parents[1]
PIN='938ef893c3368f3a597e6add2cfebdad02fddebf'
FILES={'run_inference.py':'5b0fb856ed3ebc0d384ba97887fc3948a09c3269db99572e977d4196ec541880','data/imperfectiveNLI.json':'ddd01d06b18b9bab24abb5bc92a8eb740bb145123658fa9a10bd86e38b4bdb5a'}
for relative,wanted in FILES.items():
 p=ROOT/'data/original/upstream'/relative
 if p.exists():
  if hashlib.sha256(p.read_bytes()).hexdigest()!=wanted:raise RuntimeError('Existing source differs from pin; refusing overwrite: '+relative)
  print('Verified local pinned source:',relative);continue
 url='https://raw.githubusercontent.com/boleima/ImperfectiveParadox/'+PIN+'/'+relative
 with urllib.request.urlopen(url,timeout=60) as response:content=response.read()
 if hashlib.sha256(content).hexdigest()!=wanted:raise RuntimeError('Downloaded source hash mismatch: '+relative)
 p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(content)
 print('Retrieved and verified pinned source:',relative)
