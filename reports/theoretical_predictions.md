# Theory-derived predictions — 2026-10-08

The user explicitly chose no human review and requested theory-derived predictions. This amendment replaces the independent-review gate with a transparent **theory-derived operational benchmark**. No human annotations or plausibility ratings are claimed. It does not turn model responses into gold. All labels below are derived from compatible histories and the stipulated VP interpretation, before any main results. Pilot outputs remain separate.

## Definitions and derivation

A single agent processes one target during one fixed episode/horizon. Let h be a compatible history. B(h) holds iff the required endpoint was reached in that episode; U(h) holds iff the stated sufficient activity witness occurred. U does not require a culmination. The finite oracle uses progress 1→2→3→4, with B requiring 4 and U requiring two witnessed stages. Natural-language arguments express the corresponding quantity, path goal, or full incremental theme. This is an operational interpretation of those sentences, not independently measured population agreement.

Entailed: every compatible h makes the target true. Contradicted: every compatible h makes it false. Unknown: both values occur. The neutral history set permits [1,2,STOP] and [1,2,3,4,STOP]; supportive permits only the latter; cancelling permits only the former and explicitly excludes later resumption. Completion before destruction remains completion.

| Context | Compatible outcomes | Bounded target | Activity target | Coherent target-truth q(B) | Coherent q(U) | CS = q(B)−q(U) |
|---|---|---|---|---|---|---|
| Neutral | Endpoint can be reached or not | Unknown | Entailed | Any [0,1]; no exact prior supplied | 1 | [−1,0] |
| Supportive | Endpoint reached | Entailed | Entailed | 1 | 1 | 0 |
| Cancelling | Endpoint not reached; episode closed | Contradicted | Entailed | 0 | 1 | −1 |

These six label predictions apply to **Real, Nonce and Micro**, yielding 18 cells per family and exactly 12 entailed, 3 contradicted, 3 unknown. They are normative predictions for an interpreter accepting the given rules, not guaranteed observed LLM outputs. A subjective endpoint probability of 1 for a neutral unknown target is not logically an entailment claim; do not force q-to-label thresholds. Therefore a strictly negative neutral CS needs a nondegenerate endpoint belief; logic alone gives the weak inequality.

## What theory predicts and what remains an empirical hypothesis

1. VP composition: an activity witness establishes occurrence; it does not establish a bounded endpoint. Under neutral evidence the categorical B/U contrast is unknown versus entailed. Treating every progressive bounded VP as entailed violates the operational theory.
2. Context: supportive endpoint evidence entails both targets; permanent pre-endpoint cancellation contradicts B while preserving U occurrence. Correct bounded cancellation entailment rate is zero. A later destruction is irrelevant to already-established past completion.
3. Presentation: matched interpretations have the same categorical gold across Real/Nonce/Micro. Theory supplies no necessary ranking of actual model accuracy across them. Neutral subjective q can differ with priors, supplied definitions, notation and interpretation; a layer gap does not identify an internal world-knowledge mechanism.
4. Intended priors: a smaller portion/shorter text/nearer goal is hypothesized to raise neutral completion plausibility under comparable processing speed, start time and obstacles. This is a defeasible burden hypothesis, not a theorem and not a human-validated manipulation. No .15 effect or fixed probability is asserted. Supporting/cancelling evidence fixes the endpoint regardless of these cues. Intended-prior WKE remains exploratory.
5. Rules: a fully competent reasoner already attains the normative labels, so its rule gain is zero. Positive rule gain in an imperfect LLM is an experimental hypothesis; guidance could also have no effect or harm. All outcomes will be retained.
6. Scale: event semantics gives no theorem that a larger model is better. Within-Qwen size trends are empirical associations, limited by provider/precision and training differences. No monotonic ordering is assigned as gold.

## Prediction-to-evidence separation

Machine-readable normative cells are `data/theory/normative_cells.jsonl`; per-item predictions and derivation metadata are `data/theory/item_predictions.jsonl`. Their predictions must equal existing generated gold, which is never rewritten to match model answers. The original 400-item replication preserves published gold and disputed-item flags separately. The main pool/model list/N remain unchanged from before the pilot. No synthetic observations, simulated accuracy, invented reviewers or imputed model responses enter the empirical tables.

A local freeze records the dated user disposition, solver, stimuli, predictions, prompts, providers, decoding and prospective statistical plan. It is not external preregistration. Report agreement with these theory-derived operational labels, not human-validated semantic accuracy; conclusions about ordinary-language interpretation remain conditional on the stipulated reading. General label-control failures are reported separately from event-specific effects.
