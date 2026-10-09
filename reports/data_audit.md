# Phase 3 data and generator audit

2026-10-07. All counts below are local generator/validator observations, not model results or human judgments. Sixteen semantic/parser/data-contract/analysis regression tests passed. Mechanical invariants passed for 160 latent family candidates (120 main, 40 pilot), 12 real lemmas, three manipulation loci, matched 3×2×3 core, and all six robustness renderers. State gold is derived by enumerating admissible histories; neutral permits both terminal and nonterminal continuations. A destruction-after-endpoint test preserves historical completion. The generator never invokes an LLM to create gold.

| Dataset | Items | Purpose |
|---|---:|---|
| Pilot core | 720 | 40 families × 18 |
| Main core | 2,160 | 120 families × 18 |
| Pilot/main intended prior | 60 / 240 | Real bounded only; unvalidated, exploratory |
| Pilot/main explicit label controls | 20 / 60 | Not pooled with composition metrics |
| Stress core/prior | 540 / 120 | Subset, one strong model |
| Six robustness variants | 288 each | 24 families × 12; main baseline reused |
| Real definition control | 96 | Only Real changes; other layers reused |

Original 400 items/gold untouched. Pilot/main family IDs disjoint; normalized source overlap absent. Each core family has 12 entailed/3 contradicted/3 unknown, a semantic imbalance rather than an annotation mistake. Forty-eight nonce strings have no exact collision in `/usr/share/dict/words` (dictionary hash saved); this does not guarantee absence from all training data. Root form is shared across each matched composition/context family. Names and objects vary by a seeded schedule; vocabulary scenarios repeat underlying process logic. Finite abstract progress mechanisms number far fewer than families. IDs/lexeme variants are not evidence of independent logical diversity.

Quantized episodes exclude additional targets so “exactly” does not become unknown merely through unmentioned surplus actions. Real hypotheses use literal entire/exactly/marked-goal expressions, substantial noncompletion and a fixed ten-minute horizon. Activity witnesses assert nonzero motion/material processing, several written/read words, or at least two collected objects. Cancellation rules explicitly exclude endpoint attainment and later resumption within the same episode. Supporting evidence establishes endpoint before any termination. Automatic text checks verify invariant surface features, not that ordinary humans share every reading.

Full machine audit: `reports/data_validation.json`. Family metadata: `data/generated/families.jsonl`. Each candidate has `human_validated=false` and an intended-reading gold-source marker. Real/Nonce labels depend on operational interpretation; Micro labels are exact relative to its stated finite rules. No independent annotators or prior raters have participated. Claims must be limited accordingly. Do not rename automated validation “human review.”

Prior attributes differ in extent/distance or portion size; no assertion of pure world-knowledge causality. Collection object size may be a weak prior cue. This is retained prospectively rather than deleting it on LLM results. Future independently rated stimuli could justify a new version, but neither their gold nor prior direction will be fitted to current model outputs. OOD uses a distinct record-style surface wrapper; it remains a limited paraphrase test, not open-domain OOD generalization.
