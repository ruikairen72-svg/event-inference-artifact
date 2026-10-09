"""Verify retained unchanged original and published concern sidecar, offline."""
from pathlib import Path
import hashlib,json,collections
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'data/original/upstream/data/imperfectiveNLI.json';f=ROOT/'data/original/disputed_items.jsonl'
assert hashlib.sha256(p.read_bytes()).hexdigest()=='ddd01d06b18b9bab24abb5bc92a8eb740bb145123658fa9a10bd86e38b4bdb5a'
assert hashlib.sha256(f.read_bytes()).hexdigest()=='ea31f1ac089006e19be3a10762ef4e24fab5af3106bf64de24a4747d275eb35b'
data=json.loads(p.read_text());flags=[json.loads(x) for x in f.read_text().splitlines()]
assert len(data)==len(flags)==400
assert {r['id'] for r in data}=={r['id'] for r in flags}
assert collections.Counter(r['label'] for r in data)=={'False':100,'True':200,'Unknown':100}
assert sum(r['critique_vss_exclusion'] for r in flags)==97
assert sum(r['critique_no_explicit_noncompletion'] for r in flags)==76
assert all(r['independent_human_review'] is False for r in flags)
print('Offline retained-original/concern-sidecar integrity verified. Re-deriving concern flags requires the separately acquired primary critique text.')
