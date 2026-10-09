"""Validate actual returned human forms. Empty forms cannot pass this gate."""
from pathlib import Path
import argparse,csv,json
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('csvfile');a=p.parse_args();rows=list(csv.DictReader(Path(a.csvfile).open()));valid=[];errors=[]
for i,r in enumerate(rows,2):
 if not r.get('reviewer_id'):continue
 labels=set(r.get('acceptable_labels','').split(';'))
 if not labels or not labels<={'entailed','contradicted','unknown'}:errors.append([i,'invalid acceptable labels']);continue
 if r.get('preferred_label') not in labels:errors.append([i,'preferred label not among acceptable labels']);continue
 if r.get('vp_has_required_endpoint') not in ['yes','no','uncertain']:errors.append([i,'missing endpoint assessment']);continue
 if r.get('grammar_ok') not in ['yes','no'] or r.get('ambiguous_reading') not in ['yes','no']:errors.append([i,'missing quality judgments']);continue
 valid.append(r)
report={'source':'actual supplied CSV, not generated judgments','submitted_rows':len(rows),'valid_annotated_rows':len(valid),'reviewer_count':len({r['reviewer_id'] for r in valid}),'errors':errors,'format_passed':bool(valid) and not errors,'semantic_review_gate_passed':False,'note':'This script checks submission format only. Independent expertise, coverage, agreement, ambiguity adjudication and final dataset disposition require a separate documented human review; format success cannot pass that gate.'}
print(json.dumps(report,indent=2));
if not valid:raise SystemExit('NO HUMAN ANNOTATIONS: empty forms do not satisfy independent review.')
