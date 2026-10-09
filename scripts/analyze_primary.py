"""Main analysis is gated by an explicit prospective frozen protocol."""
from pathlib import Path
import sys,json,argparse
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from event_completion.primary import analyze_primary
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--protocol',required=True);p.add_argument('--output',required=True);a=p.parse_args()
protocol=json.loads(Path(a.protocol).read_text())
if not protocol.get('main_frozen') or not protocol.get('review_disposition'):
 raise SystemExit('Main freeze and documented human-review/exploratory disposition required; pilot cannot pass this gate.')
rows=[json.loads(l) for l in Path(a.input).read_text().splitlines()]
if any(r['dataset'].startswith('pilot') for r in rows):raise SystemExit('Pilot outputs cannot enter main primary analysis.')
models=json.loads((ROOT/'config/study_protocol_candidate.json').read_text())['main_models']
report={'claim_status':protocol['review_disposition'],'externally_preregistered':protocol.get('externally_preregistered',False),'multiplicity_family':30,'results':analyze_primary(rows,models)}
Path(a.output).write_text(json.dumps(report,indent=2)+'\n')
