"""Materialize planned cells from immutable caches, preserving all missing outcomes."""
from pathlib import Path
import sys,json,argparse
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from event_completion.runner_main import make_jobs,ROOT
p=argparse.ArgumentParser();p.add_argument('--datasets',required=True);p.add_argument('--models',required=True);p.add_argument('--output',required=True);a=p.parse_args()
cache={}
for f in (ROOT/'data/raw_runs').glob('*/responses.jsonl'):
 for line in f.read_text().splitlines():
  r=json.loads(line)
  if r['request_id'] in cache:
   raise RuntimeError('Duplicate successful payload request detected: '+r['request_id'])
  cache[r['request_id']]={**r,'source_run':f.parent.name}
rows=[]
for j in make_jobs(SimpleNamespace(datasets=a.datasets,models=a.models,items_per_model=None)):
 r=cache.get(j['request_id'])
 if r:
  # Analysis cells use planned identity; provenance retains the cached identity.
  expected=bool(r.get('parsed')) and r['parsed']['judgment']==j['item']['gold']
  if bool(r.get('correct')) != expected:
   raise RuntimeError('Content-identical cached payload has inconsistent planned gold: '+j['request_id'])
  rows.append({**r,'cached_source_item_id':r['item_id'],'item_id':j['item']['item_id'],
               'item':j['item'],'dataset':j['item']['dataset']})
 else:rows.append({'request_id':j['request_id'],'model':j['model'],'item_id':j['item']['item_id'],'item':j['item'],'dataset':j['item']['dataset'],'parsed':None,'transport_ok':False,'correct':False,'missing':True})
out=ROOT/a.output;out.parent.mkdir(parents=True,exist_ok=True);out.write_text(''.join(json.dumps(r)+'\n' for r in rows));print('Planned rows:',len(rows),'missing:',sum(r.get('missing',False) for r in rows))
