"""Verify all available extracted archive members using its retained manifest."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'ARCHIVE_MANIFEST.json'
if not p.exists():raise SystemExit('Run this verifier from an extracted anonymous review archive.')
manifest=json.loads(p.read_text())['sha256'];fail=[]
for name,wanted in manifest.items():
 p=ROOT/name
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=wanted:fail.append(name)
if fail:raise SystemExit('Archive member mismatch: '+', '.join(fail))
print('All retained archive members match:',len(manifest))
print('Third-party full sources excluded from the archive are not independently reverified by this check.')
