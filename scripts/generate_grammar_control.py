"""Generate the declared supplementary wording control without changing core."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from event_completion.wording import repair_rows,REPAIRS
from event_completion.generator import dump
source=ROOT/'data/generated/main_core.jsonl'
rows=repair_rows([json.loads(line) for line in source.read_text().splitlines()])
target=ROOT/'data/generated/grammar_repair.jsonl';dump(target,rows)
manifest={'status':'post-freeze supplementary wording control; primary benchmark and tests unchanged',
 'declared_before_supplementary_calls':True,'main_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'control_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'repairs':REPAIRS,
 'items_per_model':30,'models':6,'planned_cells':180,'human_annotations':0,
 'analysis':'paired all-planned categorical accuracy and complete-pair q change; no new significance test',
 'limitation':'Corrected requests occur later; service variability and collection order prevent a pure causal attribution.'}
design=ROOT/'reports/grammar_repair_design.json'
if design.exists():
 previous=json.loads(design.read_text())
 assert all(previous[k]==v for k,v in manifest.items()), 'Declared supplementary design must not be overwritten'
else:
 import datetime
 manifest['declared_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
 design.write_text(json.dumps(manifest,indent=2)+'\n')
print('Supplementary grammar controls:',len(rows))
