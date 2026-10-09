# Study blueprint v0.1 — review before implementation/pilot

Date: 2026-10-07. Status: Phase 2 design checkpoint, **not externally preregistered**, not stimulus-validated, not run. Proposed title: *From Verbs to Events: Compositional Structure and World Knowledge in LLM Event-Completion Reasoning*. Decisions below are fixed for blueprint review; any later change needs a dated amendment before confirmatory responses.

**Question:** How do VP composition, lexical/world priors, contextual evidence and model capability jointly determine event-semantic judgments? **Principle:** We move from verb-level classification to controlled event-level composition. Same-verb pairs are central but already appear in the critique; novelty rests on the joint matched knowledge/context design and distinct probability measurement.

## 1. Measurement repair: occurrence, culmination, entailment, belief

An unbounded activity has no inherent culmination. Therefore “completion probability” is not semantically comparable between bounded and unbounded descriptions. In progressive-to-simple-past NLI, the bounded target normally requires its endpoint, whereas the unbounded target requires activity occurrence. Correct *neutral* target-truth contrasts are expected to be **bounded minus unbounded < 0**, not > 0. Supportive context should shrink the contrast toward zero; cancellation should yield a negative contrast. This is a target-inference diagnostic, not direct measurement of how often an unbounded event completes.

Use a same-episode, same-agent, same-object, fixed reporting interval. The target concerns only that episode before the interval ends. Explicitly rule out later continuation and substitute episodes in cancellation items. Destruction alone is neither necessary nor sufficient: a previously finished object may later be destroyed. Require a substantial unachieved endpoint *before* permanent termination.

Collect JSON:

```json
{"judgment":"unknown","hypothesis_probability":0.55,"completion_probability":0.55}
```

`judgment`: entailed if target true in every compatible history; contradicted if false in every history; unknown if both. `hypothesis_probability`: subjective 0–1 estimate that the target actually held by the reporting horizon given the premise, allowing typical-world expectations; **not probability of entailment**. `completion_probability`: same number for bounded endpoint targets, null for unbounded occurrence targets. No confidence field, long reasoning, or coerced threshold mapping. An unknown statement may have high or low subjective probability. Validate q fields independently from labels. Self-reported q is not a token probability or empirically calibrated probability without outcome data. No Brier score for neutral unknown cases.

This deliberately extends the user's JSON to prevent occurrence/culmination conflation. Primary categorical claims use labels; world-prior claims use subjective q plus bounded-only false-entailment rates. A probability difference with correct categorical labels is *prior sensitivity*, not proof of semantic failure. A separate format ablation checks whether asking for q shifts categorical judgments.

## 2. Family allocation and target inference

Plan 160 independently authored latent families: **40 pilot** and **120 confirmatory**, split before any model responses using seed 20271007. Confirmatory: three manipulation strata, 40 families each; aim at four lexical verbs × ten distinct scenarios per stratum. These are correlated scenario realizations, not 120 independent lexical types. Track verb and family in inference; do not treat name variants as independent samples. Reserve at least one additional verb and new templates per stratum for OOD controls. If fewer families pass genuine linguistic review, reduce N transparently rather than invent “clean” stimuli.

Each core family: 3 knowledge presentations × 2 compositions × 3 contexts = **18 items**. Main N=2,160 per model; pilot N=720 per model. Each family belongs to exactly one manipulation stratum. Two paraphrase templates are counterbalanced across families/cells without duplicating every item. Same lexical verb is mandatory within Real B/U; nonce mapping is identical within its B/U pair; symbolic event code is identical within Micro B/U. The main display never exposes condition labels, family ID, gold, or `bounded/unbounded` tags.

| Context | Bounded target | Unbounded occurrence target |
|---|---|---|
| Neutral: process witnessed; final status unstated | Unknown | Entailed, after sufficient nonzero activity witness |
| Supportive: endpoint attained by horizon | Entailed | Entailed |
| Cancelling: endpoint not attained and no continuation through horizon | Contradicted | Entailed, because activity already occurred |

This structure is intrinsically label-imbalanced (per family: 12 entailed, 3 contradicted, 3 unknown). Verify this exact expectation; report cell accuracy and macro label accuracy. **Do not force equal labels by silently changing semantic targets.** Add separate 60-item label-mapping controls per model (20/label), with explicit occurred/did-not-occur/unknown occurrence facts; exclude these from composition contrasts. Context words necessarily convey evidence; leakage means accidental condition/label tokens, not the presence of genuine outcome evidence.

## 3. Exact same-verb taxonomy and retention rules

All examples below are candidate *design illustrations*, not a validated benchmark.

| Stratum | Unbounded VP → bounded VP | Endpoint and pitfalls |
|---|---|---|
| Quantized consumption | drink water → drink exactly one measured glass of water | Emptying the stipulated portion; specify non-negligible remainder for cancelling. Drinking some liquid must actually have occurred. |
| Quantized consumption | eat rice → eat exactly one measured bowl of rice | Incremental consumption; reject negligible remainder and eating-onset-only episodes. |
| Quantized transfer | pour water → pour exactly one measured liter of water | Transfer extent; no “pour into a full tank” extra endpoint. |
| Quantized collection | collect pebbles → collect exactly ten pebbles | Count attained; start with at least two collected pebbles so plural occurrence is true. Repeated/replacement collections excluded. |
| Goal path | walk in the corridor → walk to the end of the corridor | Same actor/location; changing preposition is the intended path manipulation. Exclude loops/earlier arrivals. |
| Goal path | run along the path → run to the marked gate | Sustained running versus gate arrival; no race/winning interpretation. |
| Goal path | swim in the lane → swim to the far wall | Nonzero distance traversed, same swimming mode. |
| Goal path | crawl along the tunnel → crawl to the tunnel exit | No hidden crossing requirement in activity form. |
| Incremental creation | copy text → copy the entire specified paragraph | Same copying relation, terminal coverage; partial text must contain enough words to count as copying. |
| Incremental creation | transcribe speech → transcribe the entire specified recording | Same relation, coverage of a fixed recording. |
| Incremental creation | read text → read the entire specified passage | Temporal reading progress; partial-reading senses excluded by entire. |
| Incremental creation | write letters → write the entire specified letter | Orthographic-letter versus correspondence polysemy is dangerous: this candidate is rejected unless replacement wording preserves the sense. Prefer “write text → write the entire specified passage”. |

Quantization and incremental theme overlap theoretically. These strata classify **the locus of the manipulation**, not three independent aspect mechanisms. Resultatives such as “hammer metal → hammer metal flat” add a complement and event result; reserve them as exploratory/OOD, not pool as equally minimal pairs. Exclude fixed achievement predicates (arrive), vague degree changes (clean/wash), habitual/generic/iterative readings, ambiguous indefinite quantities, mere preparations, coercion with time adverbs, and unclear tolerance thresholds. Definite objects alone are insufficient.

Each family sheet records lemma, full VP, manipulation locus, incremental map/path, endpoint, activity witness, target, temporal horizon, exact B/U diff, rival readings and review disposition. Independent linguistic review must check grammar, aspect contrast, and NLI separately; automatic validators cannot certify linguistic truth. No paid annotators or experts have yet been engaged. In Phase 3 require actual reviewer records; if unavailable, report researcher-designed stimuli and restrict strong validation claims.

## 4. World-plausibility module (Real only)

Main module: 40 confirmatory bounded Real families, drawn by seed from the reviewed core with stratum balance; 2 intended prior levels × 3 contexts = **240 items per model**. Separate pilot module: 10 disjoint pilot families, 60/model. Keep lexical verb, syntax tree, argument count, participant role, tense/aspect, endpoint type, temporal horizon and target constant; change one object attribute controlling expected completion difficulty. Candidate examples: “copy the entire short/long specified passage”, “drink the entire small/large measured portion”, “walk to the nearby/distant marked gate”. No comparison of drawing versus writing. Match length as far as possible and record residual tokens.

These manipulate event burden/duration, which intentionally contributes to real-world completion expectations. They do **not** isolate a pure internal world-knowledge component independent of quantity, distance or lexical modifiers. Thus title the effect *plausibility-associated prior sensitivity*. Numeric-size variants and qualitative-size variants are separate template checks. Never use adjectives “easy/impossible/completed” as prior levels. Supporting/cancelling evidence remains logically identical and dominates the endpoint outcome.

Before model pilot, a separate genuine rating task asks expected completion within the fixed interval under a neutral premise, without NLI labels. Three or more independent native/competent English raters are desirable; preserve individual judgments. Retain a pair only if the intended prior direction is supported by at least two-thirds and the mean gap is at least 0.15 on a 0–1 scale, while a separate review supports equal boundedness/endpoint interpretation. These thresholds apply to human ratings, never selecting families on LLM effects. Without actual ratings, label high/low as *intended*, and WKE exploratory; do not claim a validated causal world-prior manipulation. No fabricated ratings or LLM surrogate human evidence.

Nonce/Micro receive the matched fixed extent/state logic but not copied short/long lexical priors; do not pretend WorldPrior is fully crossed outside Real. No global `WorldPrior` main effect in the three-layer model.

## 5. Knowledge presentations and matching limits

**Real:** natural verb and arguments. Core models receive no custom endpoint dictionary; explicit entire/exactly/goal composition supplies the relevant endpoint. The reporting horizon and episode restrictions apply to all cells.

**Nonce:** novel inflectable predicate with a neutral process definition such as “to continuously transfer units of material”; cumulative object “units” versus “exactly ten units”. Do not define the root itself as inherently bounded. Define agent/objects and progressive/past conventions independently of label. Four nonce forms per process, assignment permuted by seed and balanced over composition/context/labels; one mapping per family used across B/U. Multiple tokens are robustness variants, not more independent families. Reject dictionary collisions, obvious English roots/brand meanings and uneven condition distributions; publish the exact dictionary/version used. Unknown pretraining associations cannot be guaranteed absent.

**Micro:** symbolic state histories over units/stages/paths, with a generic truth rule for target events. B requires all fixed target units/stages; U requires an adequate activity witness and no inherent final requirement. Rules supplied uniformly, without gold-status fields. Neutral state is a set of compatible histories, not a closed-world assumption that unobserved C failed. Supporting includes terminal evidence; cancelling explicitly closes the same episode before the terminal condition.

```text
Neutral B: admissible histories {A→B, A→B→C}; target C: {false,true} → unknown.
Cancelling B: admissible histories {A→B→STOP}; target C: {false} → contradicted.
Supportive B: admissible histories {A→B→C→STOP}; target C: {true} → entailed.
All U: activity witness A→B; activity target true → entailed.
```

Program gold by enumerating finite admissible histories and applying the target predicate; store `gold_source`, `admissible_histories`, `terminal_observed`, `process_witness`, `episode_closed`, `horizon` and solver version. `culminated=false` in a neutral *observed* state must not be interpreted as eventual noncompletion. Observed C establishes earlier completion even if the artifact is subsequently destroyed. Gold never comes from an LLM.

Matching holds event logic, target, participants and context within a family. Knowledge layers also change definition burden, notation and length. Real→Nonce is not pure removal of lexical priors; Micro adds explicit structure. Include definitions-for-Real on the 24-family robustness subset as an information-load control (one extra 288-item reserved pass/model; unchanged Nonce/Micro baselines may be reused). Report LPE/SR as behavioral gaps, not identified internal lexical or structural effects. Save token counts and conduct length-matched sensitivity analysis without claiming that covariate adjustment removes all presentation confounds.

## 6. RQs and metrics fixed before pilot

RQ1 contemporary replication; RQ2 same-verb VP sensitivity; RQ3 conditional plausibility effect; RQ4 real/nonce gap; RQ5 Micro recovery; RQ6 cancellation override; RQ7 within-family scale interactions; RQ8 semantic-rule intervention. No directional global model-failure hypothesis.

- ACC: per-cell categorical accuracy; macro label accuracy alongside raw overall ACC. Complete-case and all-planned (parse failure counted incorrect) versions.
- CBR: entailment rate on bounded neutral items (gold unknown); separately on bounded cancelling (gold contradicted). Never aggregate correct U entailments into bias.
- CS_target: mean q(B)−q(U) within family/knowledge/context. Negative neutral/cancelling contrasts expected; supporting near zero. Also report categorical entailment-rate contrast. Call this compositional sensitivity of *target inference*.
- WKE: q(high)−q(low), within bounded Real family and context. Positive neutral effect is a prior-direction hypothesis; q differences are not logical errors. Report matched categorical CBR change as separate endpoint.
- LPE: CBR_real−CBR_nonce, bounded neutral; layer × composition difference-in-differences separately.
- SR: macro cell ACC_micro−ACC_real on identical family sets.
- CancelEffect: bounded q(neutral)−q(cancelling); include U occurrence stability as control.
- RG: paired ACC_rule−ACC_no-rule; also CS_target difference and bounded CBR differences.
- Scaling: Qwen3 log2 dense parameter size × composition and × presentation; no causal claim that parameter count alone differs. Training/model-version differences persist.

Ceiling correctness plus nonzero q gaps is informative; floor/ceiling is not reason to remove a model. If all measures are identical, report the null/ceiling outcome and measurement limits.

## 7. Model and pilot protocol

Exact candidate IDs, public catalogue prices and limits are in `model_selection.md` and `cost_plan.md`. No inference/access has been verified. Pilot: Qwen3-8B and Llama-3.1-8B, 40 disjoint families (1,440 core calls) plus 120 plausibility and 40 explicit label controls = **1,600 calls**, ceiling $0.90 with $0.10 unspent buffer. Dry-run prompts and tokenizer estimates first. Temperature 0, top_p 1, no requested CoT, output cap 256, no tools. Disable optional reasoning where supported and record exact request; if impossible, account for hidden billed tokens and treat reasoning mode as model metadata. Provider routing pinned after availability check; no silent fallback to another model. Temperature zero is not a determinism guarantee.

Pilot acceptance: >=98% parse validity, no truncation pattern, no leaking labels, no state-solver errors, structurally complete pairs, valid q domains, total cost below cap. Inspect cell distributions and item ambiguity *without significance tests*. If q range is <0.02 and >=95% responses share one label across genuinely distinct targets, audit prompt/stimuli rather than scale up automatically. Correct ceiling with all expected labels is acceptable; no variance by itself is not a failure. Revise only documented parser/semantic/measurement defects, rerun disjoint pilot items with recorded cost, and freeze before confirmation. Pilot is never pooled into main analysis or used to choose models/families by effect size.

## 8. Freeze, robustness and run integrity

After review and valid pilot, freeze stimuli/schema/gold, selected models/providers/prices, prompts, template assignment, analysis specification and hashes. This phase only prepares the plan; no frozen benchmark exists yet. External time-stamped registration, if later performed, must be described accurately.

Diagnostic subset: 30 main families chosen by seed and stratum (540 full-crossed items). Robustness/intervention evaluation uses 24 of these families, selected by seed with eight per stratum, and neutral+cancelling only (288 items/model), reusing main baseline. Run six paired variants: reversed label order; new held-out paraphrase; name replacement; label-only format; natural-language rule; structural rule. Add one Real-definition-load control, also 288 calls/model. Main six models run all variants; strong model only the main core diagnostic set plus 120 plausibility items. OOD template means held-out renderer; a separate held-out-verb diagnostic is exploratory and not budgeted until cost permits.

Natural-language rule: “Interpret the entire event description and its arguments when judging the hypothesis.” Structural rule: “An ongoing process alone does not establish a required terminal condition. An observed activity can have occurred without a terminal condition. Explicit outcome evidence applies to this episode and interval.” No worked example initially; if added, prespecify balanced examples and treat as separate intervention. Micro already contains explicit rules, so additional-rule gains may be small.

Cache key hashes full prompt/messages, item, exact model/provider, decoding parameters, rule/template version. Append raw response before parsing, request/generation IDs, timestamp, token usage and actual returned cost. Resume only failed/unissued calls; never repeat successful parse-invalid answers to improve results. Transport/429/5xx retries at most three, exponential backoff, charge each attempt. Retain failures, parse flags, missingness and provider changes. No credential appears in logs. Bound budget before scheduling each request at worst-case estimated token cost; stop at $9 with $1 safety reserve across all phases. No inference occurs in this phase.

## 9. Full statistical plan

Primary unit is latent family, with lexical-verb clustering and template metadata. Models are named fixed systems, not a random sample of “all LLMs”. Analyze each model, then a combined descriptive interaction model. Six primary contrasts: neutral CS_target; CS_target Real−Nonce; CS_target Real−Micro; neutral WKE; bounded cancellation q change; structural-rule ACC gain. Holm correction across these six × the six main models (36 tests); report unadjusted and corrected p, effect sizes and 95% CIs. RQ1 replication, natural-rule comparisons, supporting control and scaling are prespecified secondary; apply Benjamini–Hochberg within each disclosed secondary family, never select significant cells.

Binary correct GLMM per model: `correct ~ composition * knowledge * context + stratum + template + (1 + composition | family) + (1 | verb)`. Combined fixed-model version adds `model * composition * knowledge` and `model * context`, not an unestimable full four-way interaction. Template has only two levels, so use fixed template effects, not a poorly estimated random variance. Interactions primarily via marginal standardized paired contrasts; correctness has unequal label difficulty, hence interpret alongside q and cell accuracy. Complete separation/ceiling may make logistic estimates undefined. Prespecified fallback: report exact cell proportions and family-block bootstrap contrasts rather than claim a converged effect. Simplify random slopes only if singular/nonconvergent, record rationale, retain family intercept and cluster-aware uncertainty.

Q is bounded with expected exact zeros/ones. Primary q analysis is paired family contrast with 10,000 seeded block bootstraps; resample lexical verbs then families within verbs when enough verbs per stratum, and show family-only bootstrap as sensitivity. Permute pair direction within verb blocks for p-values; disclose limited power with few lexical blocks. A secondary linear mixed model on raw q uses the same design and cluster uncertainty. Do not apply ordinary beta regression with 0/1 values or silently clip them; zero/one-inflated beta is exploratory only if estimable. No distribution-based fishing for whichever link is significant.

WKE GLMM/LMM is a separate Real-bounded model: `outcome ~ prior * context + model + template + (1 | family)`, with prior random slope where identifiable. Analyze only validated prior pairs for the planned primary WKE; if validation unavailable report intended-prior analysis exploratory and amend designation before runs. Never treat missing Nonce/Micro prior values as “low”.

Scale: within Qwen3 only, log2(8.2/14.8/32.8) × composition + log2(size) × knowledge, conditional on context, family/verb structure retained. Three sizes support a trend, not a phase-transition claim or broad causal scaling law. Report point-wise contrasts with CIs. Quantization, providers and training differences must be disclosed; do not pool dense parameters with MoE active parameters.

Missingness: parse errors are incorrect in planned ACC and excluded from q contrasts, with paired validity/missingness by cell. Report sensitivity bounds for unavailable q (assign missing q 0 or 1 in adverse directions). No semantic-response retry. API-failed items remain missing; completed-pair analysis alongside all-planned ACC prevents asymmetric deletions. Store and disclose denominators per contrast.

Power/resolution: with 120 family contrasts and SD=0.30, illustrative independent-family SE=0.0274 and 95% half-width≈0.054; true uncertainty is larger with lexical clustering/multiplicity. With 40 WKE families, half-width≈0.093 under the same illustrative SD. These are assumptions, not empirical pilot estimates or a guaranteed power calculation. Phase 3 should simulate clustered outcomes using prespecified small/medium effects and report minimum detectable differences without adapting N to observed significance. Prefer honest imprecision to expanded ambiguous stimuli.

## 10. Validator contract and release checks

1. Same root/lemma and participants within B/U; exact surface diffs whitelist only intended argument/path manipulation.
2. World-prior pairs preserve parse roles, aspect, endpoint type; attributes and residual complexity recorded.
3. Cancelling has unachieved endpoint, episode closure, no later continuation; supportive endpoint witness survives later destruction.
4. Sufficient activity witness, especially plural objects; no hypothetical initiation mistaken for occurrence.
5. Nonce lexicon collision audit and balanced mapping; words/forms never identify labels.
6. Symbolic histories consistent, nonempty; solver gold checked exhaustively against a separate truth-set calculation; no LLM gold.
7. Cross-layer gold/context/target-role agreement within family; neutral observed incompletion does not force contradiction.
8. Label distributions match semantic truth table, stratified name/object assignment; macro reporting compensates imbalance.
9. Exact/normalized duplicates, pilot/main family disjointness, original/new accidental overlap checks.
10. Prompt metadata stripped; hypothesis-only and context-marker baselines diagnose shortcuts, with label controls counterbalanced.
11. Store actual human reviews, ambiguity/rejection reasons and prespecified exclusion criteria before model results.
12. Immutable raw results, hashes, transport/parse failure denominators and cost ledger complete.

Stop now for user blueprint review. Phase 3 generator/validator code, human ratings, pilot, confirmation, paper and final PDF remain future work. No result claim is warranted by this blueprint.
