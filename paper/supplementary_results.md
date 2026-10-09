# Supplementary results index

The main paper presents the compatible-history mechanism, full core category table, all 30 primary estimates, an original-benchmark replication summary and matched stress findings. This index locates supporting diagnostics and the separately frozen post-review role-binding experiment. Original primary and secondary test families are unchanged.

| Supporting question | Complete artifact | Interpretation |
|---|---|---|
| All paired robustness variants and prior-context contrasts | `reports/secondary_results.json`; `paper/tables/` CSV exports | 380 rows, complete named BH families; preserve both beneficial and adverse effects |
| Lexical vs family-only uncertainty | `reports/secondary_results.json` | 30 family-only sensitivities accompany the primary lexical/family intervals |
| Mixed-model attempts | `reports/mixed_models.json` | All 32 attempts retained; only one exploratory prior fit usable; core inference uses frozen cluster contrasts |
| Presentation-specific confusions | `paper/tables/core_confusions.csv`; `paper/tables/core_judgment_cells.csv` | Separate unresolved-endpoint entailment, contradiction and witnessed-activity failures |
| Generic labels and all original subsets | `reports/main_descriptive_results.json` | Full denominators; original labels unchanged; concern flags distinct |
| Strong-model same-family comparison | `reports/stress_descriptive_results.json`; `reports/secondary_results.json` | Seven systems on identical 30 core families |
| Initial and complete inherited-wording corrections | `reports/grammar_repair_sensitivity.json`; `reports/grammar_complete_sensitivity.json` | Initial 180 pairs included in final 518; later descriptive supplement, no replaced primary outcomes |
| Supervised surface recovery | `reports/surface_baselines.json` | Disjoint pilot training, full-text/hypothesis-only/majority diagnostics; paired renderer comparison |
| Protocol and exact reproduction | `config/study_protocol_frozen.json`; `reports/offline_reproduction_audit.json` | Local precollection freeze and exact offline results, not external preregistration |

All empirical figures are supplied as PDF, editable SVG and PNG, with captions and source manifests. Research-tool disclosure and author checklist are separate from this results supplement.


## Full original replication and target examples

The complete six-system, eight-column replication table remains in `paper/tables/replication_descriptive.tex`, with unchanged raw data and gold. The three original VP excerpts remain in `paper/tables/vp_examples.tex`.

## Post-review original-core breakdown

`reports/reviewer_core_diagnostics.json` contains all 18 presentation profiles, 216 per-lemma rows, 54 per-stratum rows and 24 Real-definition cells. These are descriptive analyses of unchanged outcomes. Main-paper quantity/path/coverage ranges retain all four high-Real-accuracy systems; no lemma or adverse definition result is removed.

## Shared-premise role-binding challenge: complete example

The challenge is counter-grounded: monotone coverage and landmarks define the occurrence witness and endpoint. The six new Real lemmas are held out of this benchmark's pilot/main inventory, not asserted absent from model pretraining. The role swap changes the assignment, not the record vocabulary. All 720 items, five status pairs, both actor assignments and both targets are retained. Gold uses the unchanged finite-history predicate. Unrelated observations constrain neither occurrence nor completion; a missing record is not a negative event fact.

### Real: original assignment

**Original premise.** The interval runs from minute 0 through minute 10. Nora and Alex have separate, identical assignments involving water in a glass. Coverage is monotone within this interval: the same part is not counted twice, and coverage is measured on the original assignment of that actor. An observed increase from one quarter to one half of an assignment establishes some drink activity; full coverage establishes its endpoint. The following are the only observations available for the interval. Nora had zero drink coverage at every moment from minute 0 through minute 10. Alex increased drink coverage from one quarter to one half between minute 2 and minute 3.

- **bounded target (contradicted):** Nora drank all the water in her glass during the interval.
- **unbounded target (contradicted):** Nora drank some water during the interval.

**Swapped premise.** The interval runs from minute 0 through minute 10. Nora and Alex have separate, identical assignments involving water in a glass. Coverage is monotone within this interval: the same part is not counted twice, and coverage is measured on the original assignment of that actor. An observed increase from one quarter to one half of an assignment establishes some drink activity; full coverage establishes its endpoint. The following are the only observations available for the interval. Nora increased drink coverage from one quarter to one half between minute 2 and minute 3. Alex had zero drink coverage at every moment from minute 0 through minute 10.

- **bounded target (unknown):** Nora drank all the water in her glass during the interval.
- **unbounded target (entailed):** Nora drank some water during the interval.


### Nonce: original assignment

**Original premise.** The interval runs from minute 0 through minute 10. Nora and Alex have separate, identical assignments. The invented verb dax1 means making monotone coverage progress on an assignment. "dax1-all" requires full coverage; "dax1-some" requires reaching at least two positive coverage landmarks. The same part is not counted twice. The following are the only observations available for the interval. Nora had zero dax1 coverage at every moment from minute 0 through minute 10. Alex increased dax1 coverage from one quarter to one half between minute 2 and minute 3.

- **bounded target (contradicted):** Nora dax1-all during the interval.
- **unbounded target (contradicted):** Nora dax1-some during the interval.

**Swapped premise.** The interval runs from minute 0 through minute 10. Nora and Alex have separate, identical assignments. The invented verb dax1 means making monotone coverage progress on an assignment. "dax1-all" requires full coverage; "dax1-some" requires reaching at least two positive coverage landmarks. The same part is not counted twice. The following are the only observations available for the interval. Nora increased dax1 coverage from one quarter to one half between minute 2 and minute 3. Alex had zero dax1 coverage at every moment from minute 0 through minute 10.

- **bounded target (unknown):** Nora dax1-all during the interval.
- **unbounded target (entailed):** Nora dax1-some during the interval.


### Micro: original assignment

**Original premise.** Within interval I, Nora and Alex each have a separate process P1. A history contains increasing stages 1,2,3,4 and optionally STOP; stages cannot be repeated or reversed. B(actor) holds iff stage 4 occurs within I. A(actor) holds iff at least two positive stages occur within I. An unobserved process can have no stages, stop after stage 2, or reach stage 4. The following constraints are the only observations available for I. Nora: no stage occurred at any time within I. Alex: stages 1 and 2 occurred by time 3 within I.

- **bounded target (contradicted):** B(Nora) holds within I.
- **unbounded target (contradicted):** A(Nora) holds within I.

**Swapped premise.** Within interval I, Nora and Alex each have a separate process P1. A history contains increasing stages 1,2,3,4 and optionally STOP; stages cannot be repeated or reversed. B(actor) holds iff stage 4 occurs within I. A(actor) holds iff at least two positive stages occur within I. An unobserved process can have no stages, stop after stage 2, or reach stage 4. The following constraints are the only observations available for I. Nora: stages 1 and 2 occurred by time 3 within I. Alex: no stage occurred at any time within I.

- **bounded target (unknown):** B(Nora) holds within I.
- **unbounded target (entailed):** A(Nora) holds within I.


## Collection provenance

The first technical probe used an older collector without the main Qwen disable controls. It was interrupted and all records retained. The corrected collector's inference payloads are exactly identical to `runner_main`; a test verifies this for all 5,040 cells. Non-Qwen content-identical probe responses are eligible for hash reuse. Probe Qwen payloads do not match, so they cannot enter the corrected analysis. If shutdown overlap produced two identical successful payloads, the earliest timestamp is used irrespective of its correctness; both records remain available. Failures count incorrect, and successful malformed outputs are not retried. Recorded charges plus an explicit interruption reserve are reported separately from the immutable original collection ledger.

Complete primary intervals and Holm-adjusted tests: `paper/tables/primary_descriptive.tex`; all 30 contrasts remain in the original reports and are summarized in the main paper without changing their inferential designation.

## Supplementary outcomes and cost accounting

All 5,040 planned final challenge cells are represented with valid labels. Final stimuli are in `data/supplementary/reviewer_binding_v2.jsonl`. The definition correction retests all 1,680 Nonce cells and reuses all 3,360 unchanged Real/Micro cells; histories and oracle labels are unchanged. Initial stimuli and outcomes remain separately available in `reports/reviewer_binding_initial_results.json` and `data/analysis/reviewer_binding_initial_planned.jsonl`. Initial counts describe agreement with the intended oracle under a gloss with an observation/occurrence ambiguity; final evaluation uses the explicit occurrence definition. Complete paired counts and both directions of changes are in the PDF supplement.

Accuracy, macro recall, all gold/target/presentation cells, both-correct pairs, seen/held-out splits and all twelve lemma rows are in `reports/reviewer_binding_results.json`. Exact-protocol records are in `data/analysis/reviewer_binding_planned.jsonl`. The deterministic word-unigram ceiling is 60%; the unchanged pilot-trained full-text baseline scores 40% and 33.3% macro recall. All analyses are supplementary, not new primary tests.

The immutable original ledger reports $0.9224 known returned charges and $2.0425 conservative commitments. Supplementary attempts including both wordings, technical probes and duplicates report $0.254277 known charges and $0.313063 recorded conservative commitments. A further $0.02 reserves up to sixteen interrupted in-flight probe calls: incremental commitments are $0.333063, and project commitments $2.375541. These metadata/reserve figures are not a reconciled invoice.

All original 60 scientific components are unchanged. The original generator reproduces its nineteen original generated files; supplementary data are stored separately. Collection-time sources remain frozen in `data/frozen/reviewer_binding_collection`; the definition-precision amendment precedes its calls.
