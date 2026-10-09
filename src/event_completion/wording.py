"""A deterministic, post-freeze participle repair; original items are retained."""
from .semantics import gold
REPAIRS = {'was never drank':'was never drunk', 'was never ate':'was never eaten',
           'were never wrote':'were never written'}
def repair_rows(rows):
    out=[]
    for row in sorted(rows,key=lambda r:r['item_id']):
        hits=[old for old in REPAIRS if old in row['premise']]
        if not hits: continue
        assert len(hits)==1
        assert (row['knowledge'],row['composition'],row['context'])==('real','bounded','cancelling')
        assert row['gold']==gold(row['state']['admissible_histories'],row['composition'])=='contradicted'
        changed={**row,'item_id':row['item_id']+':grammar_repair','variant':'grammar_repair',
                 'grammar_repair_baseline_item_id':row['item_id'],
                 'premise':row['premise'].replace(hits[0],REPAIRS[hits[0]])}
        assert changed['hypothesis']==row['hypothesis'] and changed['state']==row['state']
        out.append(changed)
    assert len(out)==30 and {r['verb'] for r in out}=={'drink','eat','write'}
    return out
