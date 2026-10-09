"""Offline provenance/structure audit. Never alters upstream gold or executes upstream code."""
from pathlib import Path
import json, re, hashlib
from collections import Counter
ROOT = Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    src=ROOT/'data/sources'; upstream=ROOT/'data/original/upstream'
    data=json.loads((upstream/'data/imperfectiveNLI.json').read_text())
    ids=[x['id'] for x in data]
    assert len(data)==400 and len(set(ids))==400
    assert all(set(['id','group','verb','premise','hypothesis','label']) <= set(x) for x in data)
    assert set(x['label'] for x in data)=={'True','False','Unknown'}
    text=(src/'critique.txt').read_text()
    vss=set(re.findall(r'[ABCD]_\d{3}', text.split('Examples 1\n',1)[1].split('The examples without explicit evidence',1)[0]))
    nc=set(re.findall(r'A_\d{3}',text.split('Examples 2\n',1)[1].split('Lexically matched Minimal-Pair',1)[0]))
    assert len(vss)==97 and len(nc)==76 and (vss|nc)<=set(ids)
    side=[]
    for x in data:
        side.append({'id':x['id'],'original_label':x['label'], 'critique_vss_exclusion':x['id'] in vss,'critique_no_explicit_noncompletion':x['id'] in nc,'source':'Han & Sun 2026 arXiv v1 Appendix B','independent_human_review':False})
    (ROOT/'data/original/disputed_items.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in side))
    pairkeys=[(x['premise'],x['hypothesis']) for x in data]
    current=json.loads((src/'github_tree.json').read_text())['tree']
    initial=json.loads((src/'github_initial_tree.json').read_text())['tree']
    def blob(tree,path): return next(x['sha'] for x in tree if x['path']==path)
    out={'n':len(data),'group_counts':dict(Counter(x['group'] for x in data)), 'label_counts':dict(Counter(x['label'] for x in data)), 'duplicate_pair_count':len(pairkeys)-len(set(pairkeys)), 'critique_vss_exclusions':len(vss),'critique_no_explicit_noncompletion':len(nc),'vss_retained_groups':dict(Counter(x['id'][0] for x in data if x['id'] not in vss)), 'unique_verbs_by_group':{g:len(set(x['verb'] for x in data if x['id'][0]==g)) for g in 'ABCD'}, 'data_blob_unchanged_since_initial':blob(current,'data/imperfectiveNLI.json')==blob(initial,'data/imperfectiveNLI.json'),'license_files':[x['path'] for x in current if 'license' in x['path'].lower()],'upstream_files':{str(p.relative_to(upstream)):sha(p) for p in upstream.rglob('*') if p.is_file()},'disputed_sidecar_sha256':sha(ROOT/'data/original/disputed_items.jsonl')}
    (ROOT/'reports/original_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
