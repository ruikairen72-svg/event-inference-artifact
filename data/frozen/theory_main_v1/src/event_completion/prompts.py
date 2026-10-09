"""Output q is subjective target truth, not probability of NLI entailment."""
import json
BASE='''Judge the stated hypothesis using only the premise for the NLI judgment. Entailed means true in every history consistent with the premise; contradicted means false in every such history; unknown means both are possible. Do not replace necessity with what is merely likely. All statements refer to the same episode and reporting interval.'''
PROB='''Also provide hypothesis_probability, a subjective number from 0 to 1 for the chance the hypothesis actually held by the reporting horizon, allowing typical-world expectations where the outcome is unspecified. This is NOT the probability of entailment: an unknown hypothesis can have high or low probability. Return only a short JSON object with judgment and hypothesis_probability. No explanations.'''
RULES={'natural_rule':'Interpret the entire event description and its arguments when judging the hypothesis.', 'structural_rule':'An ongoing process alone does not establish a required terminal condition. An observed activity can have occurred without a terminal condition. Explicit outcome evidence applies to this episode and interval.'}
def messages(item,original=False):
 v=item.get('variant','baseline')
 if original:
  import ast
  from pathlib import Path
  source=Path(__file__).resolve().parents[2]/'data/original/upstream/run_inference.py'
  tree=ast.parse(source.read_text())
  templates=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='PROMPT_TEMPLATES' for x in n.targets))
  system=templates['zero-shot']['system']
  user=templates['zero-shot']['user_format'].format(premise=item['premise'],hypothesis=item['hypothesis'])
 else:
  system=BASE
  if v in RULES:system+=' Additional guidance: '+RULES[v]
  order='unknown, contradicted, entailed' if v=='label_order' else 'entailed, contradicted, unknown'
  system+=' Allowed judgment labels in this order: '+order+'.'
  system+=' Return only a JSON object with the single key judgment. No explanation.' if v=='label_only' else ' '+PROB
  user='Premise:\n'+item['premise']+'\nHypothesis:\n'+item['hypothesis']
 return [{'role':'system','content':system},{'role':'user','content':user}]
def parse(raw,item,original=False):
 if original:
  x=raw.strip().strip('"').lower();mapping={'true':'entailed','false':'contradicted','unknown':'unknown'}
  return ({'judgment':mapping[x]},'ok') if x in mapping else (None,'invalid_original_label')
 text=raw.strip()
 if text.startswith('```'):
  text=text.split('\n',1)[-1];text=text.rsplit('```',1)[0].strip()
 try:d=json.loads(text)
 except (ValueError,TypeError):return None,'invalid_json'
 if not isinstance(d,dict) or d.get('judgment') not in ['entailed','contradicted','unknown']:return None,'invalid_label'
 if item.get('variant')=='label_only':return {'judgment':d['judgment']},'ok'
 q=d.get('hypothesis_probability')
 if isinstance(q,bool) or not isinstance(q,(float,int)) or not 0<=q<=1:return None,'invalid_probability'
 return {'judgment':d['judgment'],'hypothesis_probability':q},'ok'
