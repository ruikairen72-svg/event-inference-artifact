"""Append-only, content-addressed, provider-pinned OpenRouter collection."""
import argparse,asyncio,datetime,hashlib,json,math,os,random,time
from pathlib import Path
import httpx
from .prompts import messages,parse
ROOT=Path(__file__).resolve().parents[2]
API='https://openrouter.ai/api/v1/chat/completions'
def load(p):return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def returned_charge(obj,reserve):
 cost=(obj.get('usage') or {}).get('cost') if isinstance(obj,dict) else None
 known=isinstance(cost,(int,float)) and not isinstance(cost,bool) and math.isfinite(cost) and cost>=0
 return (float(cost) if known else reserve,not known)
def all_spend():
 total=0
 for p in (ROOT/'data/raw_runs').glob('*/attempts.jsonl'):
  for r in load(p):total+=r.get('charged_or_reserved_usd',0)
 return total

def make_jobs(args):
 spec={m['id']:m for m in json.loads((ROOT/'config/runtime_main.json').read_text())['models']}
 items=[]
 for name in args.datasets.split(','):
  if name=='original':
   data=json.loads((ROOT/'data/original/upstream/data/imperfectiveNLI.json').read_text());mp={'True':'entailed','False':'contradicted','Unknown':'unknown'}
   items += [{**r,'item_id':r['id'],'family_id':r['verb'],'gold':mp[r['label']],'dataset':'original','original':True} for r in data]
  else:
   path=ROOT/f'data/generated/{name}.jsonl'
   if not path.is_file():raise ValueError('Unknown or unavailable dataset: '+name)
   rows=load(path)
   if not rows:raise ValueError('Empty dataset: '+name)
   items += [{**r,'dataset':name,'original':False} for r in rows]
 if args.items_per_model:items=items[:args.items_per_model]
 jobs=[]
 for mid in args.models.split(','):
  s=spec[mid]
  for r in items:
   payload={'model':mid,'messages':messages(r,r['original']),'temperature':0,'top_p':1,'max_tokens':256,'provider':{'only':[s['provider_tag']],'allow_fallbacks':False}}
   if s['reasoning_supported']:payload['reasoning']={'enabled':False,'exclude':True}
   # Use shared raw JSON prompting; requiring JSON API grammar can be a separate constraint across providers.
   if mid.startswith('qwen/qwen3-'):
    payload['messages'][-1]['content']+='\n/no_think'
   rid=digest(payload)
   jobs.append({'request_id':rid,'model':mid,'provider_tag':s['provider_tag'],'item':r,'payload':payload,'price':s['pricing']})
 random.Random(20271007).shuffle(jobs)
 return jobs

async def run(args):
 jobs=make_jobs(args);out=ROOT/'data/raw_runs'/args.run_id;out.mkdir(parents=True,exist_ok=True)
 if args.dry_run:
  req=sum(len(json.dumps(j['payload']['messages'])) for j in jobs)
  print(json.dumps({'jobs':len(jobs),'mean_input_chars':req/max(1,len(jobs)),'estimated_input_tokens_char_div3':math.ceil(req/max(1,len(jobs))/3),'no_calls':True}));return
 key=Path(args.key_file).read_text().strip()
 responses=load(out/'responses.jsonl');done={r['request_id'] for r in responses if r.get('transport_ok')}
 # Cross-run cache reuses successful content-identical requests; item/context metadata remains from original record.
 for p in (ROOT/'data/raw_runs').glob('*/responses.jsonl'):
  done|={r['request_id'] for r in load(p) if r.get('transport_ok')}
 unique={}
 for j in jobs:
  if j['request_id'] not in done:unique.setdefault(j['request_id'],j)
 jobs=list(unique.values())
 if args.limit:jobs=jobs[:args.limit]
 invocation_started=utc()
 plan_path=out/('plan.json' if not (out/'plan.json').exists() else 'plan_'+invocation_started.replace(':','-')+'.json')
 plan_path.write_text(json.dumps({'started_utc':invocation_started,'datasets':args.datasets,'models':args.models,'planned_pending':len(jobs),'concurrency':args.concurrency,'max_output_tokens':256,'run_cap_usd':args.cap,'payload_protocol_sha256':digest([j['payload'] for j in jobs])},indent=2))
 lock=asyncio.Lock();semaphore=asyncio.Semaphore(args.concurrency);spent=all_spend();runspent=sum(x.get('charged_or_reserved_usd',0) for x in load(out/'attempts.jsonl'));reserved=0;counts={'complete':0,'transport_errors':0,'parse_invalid':0,'endpoint_mismatch':0};start=time.time();stopped=False
 model_locks={m:asyncio.Semaphore(1 if m=='qwen/qwen3-8b' else args.concurrency) for m in args.models.split(',')}
 last_started={}
 def append(name,row):
  with (out/name).open('a') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n');f.flush();os.fsync(f.fileno())
 async def one(j,client):
  nonlocal spent,runspent,reserved,stopped
  async with model_locks[j['model']], semaphore:
   worst=(math.ceil(len(json.dumps(j['payload']['messages']))/2)+100)*float(j['price']['prompt'])+512*float(j['price']['completion'])
   base={'request_id':j['request_id'],'model':j['model'],'provider_tag':j['provider_tag'],'item_id':j['item']['item_id'],'dataset':j['item']['dataset']}
   for attempt in range(4):
    async with lock:
     if spent+reserved+worst>9 or runspent+reserved+worst>args.cap:stopped=True;return
     reserved+=worst
    if j['model']=='qwen/qwen3-8b':
     await asyncio.sleep(max(0,2.05-(time.time()-last_started.get(j['model'],0))))
     last_started[j['model']]=time.time()
    began=utc();t=time.time();cost=worst;obj=None;raw='';err=None;httpstatus=None;retry=False;transport=False
    try:
     rr=await client.post(API,headers={'Authorization':'Bearer '+key,'Content-Type':'application/json','X-OpenRouter-Metadata':'enabled'},json=j['payload']);httpstatus=rr.status_code
     obj=rr.json()
     if rr.status_code!=200 or obj.get('error'):
      err=f'HTTP {rr.status_code}: '+str(obj.get('error') or obj)[:500];retry=rr.status_code in [408,429,500,502,503,504]
      # Server may reject before generation, but reserve unknown charge instead of claiming zero.
     else:
      raw=obj['choices'][0]['message'].get('content') or '';transport=True
      usage=obj.get('usage') or {};cost=float(usage['cost']) if isinstance(usage.get('cost'),(int,float)) else worst
    except (httpx.HTTPError,ValueError,KeyError,IndexError) as e:err=type(e).__name__+': '+str(e)[:300];retry=isinstance(e,httpx.HTTPError)
    cost,cost_estimated=returned_charge(obj,worst)
    if err:err=err.replace(key,'[REDACTED]')
    async with lock:
     reserved-=worst;spent+=cost;runspent+=cost
     append('attempts.jsonl',{**base,'attempt':attempt,'started_utc':began,'http_status':httpstatus,'api_id':obj.get('id') if obj else None,'transport_ok':transport,'charged_or_reserved_usd':cost,'cost_is_estimate':cost_estimated,'error':err})
     if transport:
      parsed,status=parse(raw,j['item'],j['item']['original']);usage=obj.get('usage') or {};choice=obj['choices'][0]
      counts['complete']+=1;counts['parse_invalid']+=int(parsed is None);counts['endpoint_mismatch']+=int(status=='endpoint_field_mismatch')
      # Persist raw visible response, usage and route; omit private reasoning fields.
      append('responses.jsonl',{**base,'item':j['item'],'payload':j['payload'],'started_utc':began,'latency_seconds':round(time.time()-t,3),'api_id':obj.get('id'),'returned_model':obj.get('model'),'returned_provider':obj.get('provider'),'routing_metadata':obj.get('openrouter_metadata'),'usage':usage,'cost_usd':cost,'raw_response':raw,'finish_reason':choice.get('finish_reason'),'parsed':parsed,'parse_status':status,'transport_ok':True,'correct':parsed is not None and parsed['judgment']==j['item']['gold'],'retry_index':attempt})
     else:
      append('errors.jsonl',{**base,'timestamp_utc':began,'error':err,'attempt':attempt});counts['transport_errors']+=1
     (out/'progress.json').write_text(json.dumps({'run_id':args.run_id,'utc':utc(),'pending_at_start':len(jobs),**counts,'run_spend_usd':runspent,'project_spend_usd':spent,'elapsed_s':round(time.time()-start),'budget_stopped':stopped},indent=2))
     if counts['complete'] and counts['complete']%50==0:print(f"{args.run_id}: completed {counts['complete']}/{len(jobs)}, invalid {counts['parse_invalid']}, transport errors {counts['transport_errors']}, spend ${runspent:.4f}",flush=True)
    if transport or not retry:return
    if attempt<3:await asyncio.sleep(min(20,2**attempt+random.random()))
 async with httpx.AsyncClient(timeout=httpx.Timeout(90,connect=20),limits=httpx.Limits(max_connections=args.concurrency)) as client:
  # Separate model queues avoid a slow, rate-limited model blocking other providers.
  queues={}
  for j in jobs:
   queues.setdefault(j['model'],asyncio.Queue()).put_nowait(j)
  async def worker(queue):
   while not queue.empty() and not stopped:
    j=queue.get_nowait();await one(j,client);queue.task_done();await asyncio.sleep(0)
  workers=[]
  for mid,queue in queues.items():
   for _ in range(1 if mid=='qwen/qwen3-8b' else min(2,args.concurrency)):
    workers.append(worker(queue))
  await asyncio.gather(*workers)
 print(json.dumps({'run_id':args.run_id,**counts,'spent':runspent,'budget_stopped':stopped}),flush=True)
def cli():
 p=argparse.ArgumentParser();p.add_argument('--run-id',required=True);p.add_argument('--datasets',required=True);p.add_argument('--models',required=True);p.add_argument('--key-file',default='/private/tmp/sac_event_openrouter_key');p.add_argument('--concurrency',type=int,default=4);p.add_argument('--cap',type=float,default=.9);p.add_argument('--limit',type=int);p.add_argument('--items-per-model',type=int);p.add_argument('--dry-run',action='store_true');args=p.parse_args()
 if args.concurrency<1 or args.cap<=0:p.error('Concurrency and run cap must be positive.')
 asyncio.run(run(args))
if __name__=='__main__':cli()
