# Official benchmark audit

Audit date 2026-10-07. This report concerns upstream data and implementation; no model has been run. Source: [official repository](https://github.com/boleima/ImperfectiveParadox), fixed at **938ef893c3368f3a597e6add2cfebdad02fddebf** (September 4). The tree, commit, six-commit history and all four published files are retained locally. `scripts/audit_original.py` reproduces the structural counts and sidecar extraction.

## Observed locally

| Check | Result |
|---|---|
| Items / unique IDs | 400 / 400 |
| Groups A/B/C/D | 100 each |
| Original True/False/Unknown | 200 / 100 / 100 |
| Exact premise–hypothesis duplicates | 0 |
| Unique verb entries within each group | 100 |
| Dataset SHA-256 | `ddd01d06b18b9bab24abb5bc92a8eb740bb145123658fa9a10bd86e38b4bdb5a` |
| Data blob versus initial January 13 commit | Identical Git blob |
| Repository license files | None; API license field null |
| Upstream files | README, inference script, dataset JSON, updated TBR image |

Original labels are unchanged. `data/original/disputed_items.jsonl` has one row per ID with original label plus two *published concern flags*. Extracted from [Han & Sun Appendix B](https://arxiv.org/html/2608.25005v1): 97 VSS exclusions (remaining A/B/C/D = 49/98/58/98), and a separate 76-item A list lacking explicit noncompletion. These are attributed flags, not our independent annotations or definitive replacement gold. The two lists are not interchangeable. No subset is called causally clean merely because a critique retained it.

## Script and update audit

The [pinned upstream](https://github.com/boleima/ImperfectiveParadox/tree/938ef893c3368f3a597e6add2cfebdad02fddebf) defines strict, definition-aware, CoT and counterfactual prompts. It applies Hugging Face chat templates, greedy generation and a 512-token CLI default; results include prompts/raw predictions. It has no hosted-cost ledger, durable per-item resume, metric implementation, or representation-analysis code. Its default `simple` prompt is absent from choices. We inspected it as text and did not execute it. September README acknowledges world-knowledge-dependent A interpretations and adds TBR_A; the dataset itself was not revised. Paper §8 grants dataset CC BY-NC 4.0; that does not license repository code automatically.

## Validity and use policy

A label reflects an event description, not an isolated verb. A progressive predicate does not entail its culmination; lack of entailment is different from evidence of its negation. Destruction after culmination cannot negate an earlier completed event. “Stopped” alone leaves resumption open. Definite objects can allow partial readings, and path phrases can bound ostensibly activity verbs. Consequently, aggregate A accuracy is sensitive to the fixed original convention.

Layer 0 will run the full 400 items using the upstream strict prompt and original three-label format, report A/B/C/D accuracy and TBR_C/TBR_A, and show full label distributions. A supplementary sensitivity table uses the published 303-item VSS *without changing labels*. A second analysis stratifies by the 76 explicit-noncompletion flags. This is contemporary conceptual replication through hosted models, not an exact local-weight/decoding replication. Hosted generation and original greedy decoding differ. Main new-benchmark causal claims must come from independently specified controlled families. Budget and page allocation reserve roughly 15–20% of results space to Layer 0.

Human evidence in the original paper validates sentence quality; it does not establish each NLI label. Our automated audit likewise checks consistency/provenance, not linguistic validity. A real human-review sheet is required before describing the new real-world stimuli as human validated. Release original dataset with attribution and noncommercial restrictions; release our independent code separately. Do not distribute upstream code under an invented license.
