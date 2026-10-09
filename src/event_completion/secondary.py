"""Complete secondary diagnostics; no significance-dependent selection.

Implemented during collection, before completed-result analysis. Exploratory
additions are explicitly distinguished from the frozen 30 primary tests.
"""
from collections import defaultdict
import numpy as np
from .analysis import cluster_ci

VARIANTS = ['label_order','template_ood','name','label_only','natural_rule','structural_rule','real_definition']

def bh(ps):
    order = sorted(range(len(ps)), key=lambda i: 1 if ps[i] is None else ps[i])
    out = [None] * len(ps)
    previous = 1.0
    for rank in range(len(order)-1, -1, -1):
        i = order[rank]
        value = 1 if ps[i] is None else ps[i]
        previous = min(previous, value * len(order)/(rank+1))
        out[i] = None if ps[i] is None else previous
    return out

def family_only_ci(values, seed=20271007, draws=10000):
    if not values:
        return None
    x = np.asarray(values, float)
    rng = np.random.default_rng(seed)
    means = x[rng.integers(len(x), size=(draws,len(x)))].mean(axis=1)
    return [float(v) for v in np.quantile(means,[.025,.975])]

def analyze(rows, draws=10000):
    result = []
    for model in sorted({r['model'] for r in rows}):
        rr = [r for r in rows if r['model']==model]
        core_ds = 'stress_core' if any(r['dataset']=='stress_core' for r in rr) else 'main_core'
        prior_ds = 'stress_prior' if core_ds=='stress_core' else 'main_prior'
        base = {}
        variants = defaultdict(dict)
        prior = {}
        verbs = {}
        for r in rr:
            i=r['item']; f=i['family_id']; verbs[f]=i.get('verb',f)
            key=(f,i.get('knowledge'),i.get('composition'),i.get('context'))
            if r['dataset']==core_ds:
                if key in base: raise ValueError('Duplicate core cell')
                base[key]=r
            elif r['dataset'] in VARIANTS:
                if key in variants[r['dataset']]: raise ValueError('Duplicate variant cell')
                variants[r['dataset']][key]=r
            elif r['dataset']==prior_ds:
                prior[(f,i['context'],i['prior'])]=r
        families=sorted({k[0] for k in base})
        def q(r): return ((r or {}).get('parsed') or {}).get('hypothesis_probability')
        def correct(r): return float(bool((r or {}).get('correct')))
        def entail(r): return float(((r or {}).get('parsed') or {}).get('judgment')=='entailed')
        def record(metric, group, vals, planned, **meta):
            valid=[(f,v) for f,v in vals if v is not None]
            ci=cluster_ci([v for f,v in valid],[verbs[f] for f,v in valid],b=draws) if valid else None
            result.append({'model':model,'dataset':core_ds,'metric':metric,'multiplicity_family':group,
                           'planned_families':planned,'valid_families':len(valid),'result':ci,
                           'family_only_ci95':family_only_ci([v for f,v in valid],draws=draws),**meta})
        def difference(a,b,fn=q):
            x,y=fn(a),fn(b)
            return None if x is None or y is None else x-y
        for knowledge in ['real','nonce','micro']:
            for context in ['neutral','supportive','cancelling']:
                keys=lambda f,c:(f,knowledge,c,context)
                record('cs_q','composition',[(f,difference(base.get(keys(f,'bounded')),base.get(keys(f,'unbounded')))) for f in families],len(families),knowledge=knowledge,context=context)
                record('cs_categorical_entailment','composition',[(f,difference(base.get(keys(f,'bounded')),base.get(keys(f,'unbounded')),entail)) for f in families],len(families),knowledge=knowledge,context=context,missing_policy='all-planned; absent/invalid answer is not entailment')
            for comp in ['bounded','unbounded']:
                record('cancel_minus_neutral_q','context',[(f,difference(base.get((f,knowledge,comp,'cancelling')),base.get((f,knowledge,comp,'neutral')))) for f in families],len(families),knowledge=knowledge,composition=comp)
        for knowledge in ['nonce','micro']:
            for context in ['neutral','cancelling']:
                record('real_minus_other_bounded_entailment','presentation',[(f,difference(base.get((f,'real','bounded',context)),base.get((f,knowledge,'bounded',context)),entail)) for f in families],len(families),knowledge=knowledge,context=context,missing_policy='all-planned')
        record('micro_minus_real_accuracy','presentation',[(f,float(np.mean([correct(base[(f,'micro',c,x)])-correct(base[(f,'real',c,x)]) for c in ['bounded','unbounded'] for x in ['neutral','supportive','cancelling']]))) for f in families],len(families),missing_policy='all-planned; balanced six-cell comparison')
        for context in ['neutral','supportive','cancelling']:
            fs=sorted({k[0] for k in prior})
            record('intended_high_minus_low_q','intended_prior_exploratory',[(f,difference(prior.get((f,context,'high')),prior.get((f,context,'low')))) for f in fs],len(fs),context=context,human_ratings=0)
        for variant, changed in variants.items():
            fs=sorted({k[0] for k in changed})
            # Real-definition compares only changed Real cells, never diluted
            # by unchanged nonce/micro cells reused from the main baseline.
            values=[];flips=[]
            for f in fs:
                keys=[k for k in changed if k[0]==f]
                if any(k not in base for k in keys): raise ValueError('Unmatched variant')
                values.append((f,float(np.mean([correct(changed[k])-correct(base[k]) for k in keys]))))
                both=[k for k in keys if changed[k].get('parsed') and base[k].get('parsed')]
                flips.append((f,float(np.mean([changed[k]['parsed']['judgment']!=base[k]['parsed']['judgment'] for k in both])) if both else None))
            record('variant_minus_baseline_accuracy','robustness_interventions',values,len(fs),variant=variant,matched_planned_cells=len(changed),missing_policy='all-planned')
            record('variant_label_disagreement','diagnostic_no_test',flips,len(fs),variant=variant,missing_policy='paired parse-valid; disagreement does not identify which answer is correct')
            if variant in ['natural_rule','structural_rule']:
                for knowledge in ['real','nonce','micro']:
                    for context in ['neutral','cancelling']:
                        values=[]
                        for f in fs:
                            kb=(f,knowledge,'bounded',context);ku=(f,knowledge,'unbounded',context)
                            a=difference(changed.get(kb),changed.get(ku));b=difference(base.get(kb),base.get(ku))
                            values.append((f,None if a is None or b is None else a-b))
                        record('rule_minus_baseline_cs_q','robustness_interventions',values,len(fs),variant=variant,knowledge=knowledge,context=context)
    for group in sorted({r['multiplicity_family'] for r in result}):
        rr=[r for r in result if r['multiplicity_family']==group]
        adjusted=bh([r['result']['p_cluster_signflip'] if r['result'] else None for r in rr])
        for r,p in zip(rr,adjusted):
            r['p_bh_secondary']=None if group=='diagnostic_no_test' else p
            r['designation']='exploratory descriptive diagnostic' if group=='diagnostic_no_test' else 'secondary; not a replacement for frozen primary Holm family'
    return result
