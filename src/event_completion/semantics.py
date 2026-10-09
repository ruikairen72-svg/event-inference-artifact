"""Finite-history oracle: observation incompleteness is not a negative fact."""
def target_truth(history, composition, required=4):
    stages=[s for s in history if isinstance(s,int)]
    if composition=='bounded': return required in stages
    if composition=='unbounded': return len(stages)>=2
    raise ValueError(composition)
def gold(histories,composition,required=4):
    if not histories: raise ValueError('Empty compatible-history set')
    truths={target_truth(h,composition,required) for h in histories}
    return 'entailed' if truths=={True} else 'contradicted' if truths=={False} else 'unknown'
def histories(context):
    return {'neutral':[[1,2,'STOP'],[1,2,3,4,'STOP']], 'supportive':[[1,2,3,4,'STOP']], 'cancelling':[[1,2,'STOP']]}[context]
