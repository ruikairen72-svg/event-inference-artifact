"""Post-freeze wording audit; retain all original data and primary estimates."""
from pathlib import Path
import json, hashlib, collections
ROOT = Path(__file__).resolve().parents[1]
PATTERNS = ('was never drank', 'was never ate', 'were never wrote')
def affected(item):
    return any(p in item['premise'] for p in PATTERNS)
def load(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
def audit():
    datasets = {}
    for path in sorted((ROOT/'data/generated').glob('*.jsonl')):
        if path.name == 'families.jsonl': continue
        rows = load(path)
        bad = [r for r in rows if affected(r)]
        datasets[path.stem] = {'planned':len(rows), 'affected':len(bad),
            'affected_by_verb':dict(collections.Counter(r['verb'] for r in bad)),
            'item_ids':[r['item_id'] for r in bad],
            'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    estimates = []
    for name in ('main','stress'):
        path = ROOT/f'data/analysis/{name}_planned.jsonl'
        if not path.exists(): continue
        rows = load(path)
        for model in sorted({r['model'] for r in rows}):
            core = [r for r in rows if r['model']==model and r['dataset'] in ('main_core','stress_core')]
            if not core: continue
            kept = [r for r in core if not affected(r['item'])]
            pairs = {(r['item']['family_id'], r['item']['context']):r for r in core
                     if r['item']['knowledge']=='real' and r['item']['composition']=='bounded'}
            changes = []
            planned_pairs = 0
            for (family,ctx),r in pairs.items():
                if ctx!='cancelling' or affected(r['item']): continue
                planned_pairs += 1
                neutral = pairs[(family,'neutral')]
                q1 = (r.get('parsed') or {}).get('hypothesis_probability')
                q0 = (neutral.get('parsed') or {}).get('hypothesis_probability')
                if q1 is not None and q0 is not None: changes.append(q1-q0)
            estimates.append({'model':model,'dataset':name,'core_planned':len(core),
                'wording_affected_cells':len(core)-len(kept),
                'accuracy_all_planned':sum(bool(r.get('correct')) for r in core)/len(core),
                'accuracy_without_affected_cells':sum(bool(r.get('correct')) for r in kept)/len(kept),
                'real_bounded_cancel_minus_neutral_unaffected_planned_families':planned_pairs,
                'real_bounded_cancel_minus_neutral_unaffected_valid_pairs':len(changes),
                'real_bounded_cancel_minus_neutral_unaffected_mean':sum(changes)/len(changes) if changes else None})
    report = {'status':'post-freeze descriptive wording sensitivity; not prespecified inference',
        'defect':'Simple past was used instead of the past participle in three passive cancellation templates.',
        'patterns':list(PATTERNS),'primary_data_and_tests_unchanged':True,
        'scope':'Removing cells changes their composition and lexical mix; differences do not identify a causal wording effect. Original responses are retained; paired corrections are reported separately. No new significance tests.',
        'datasets':datasets,'empirical_sensitivity':estimates}
    (ROOT/'reports/stimulus_wording_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'main_core_affected':datasets['main_core']['affected'],
        'main_core_planned':datasets['main_core']['planned'],'empirical_reports':len(estimates)}))
if __name__=='__main__': audit()
