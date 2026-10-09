# Full pilot checkpoint — 2026-10-07

All 1,600 planned v2 cells have genuine transport responses. 1,600 parse valid (100.00%); 0 output-length truncations. No semantic or format-response retries were performed. The earlier 40-call v1 schema smoke remains archived and excluded from all v2/main estimates.

Known returned pilot cost including v1: **$0.049307**. Conservative ledger including unbilled/unknown-cost failed attempts: **$0.207148**. HTTP-failed attempts in v2: 471; these are attempts, not missing final items. This is local returned billing metadata, not an independent account invoice.

Prompt-usability gate (≥98% parseable, no length truncation, pilot ledger <$0.90): **passed**. This is not semantic-validity certification. No effects, p-values, or significance thresholds were used to select the stimulus pool, models, sample size or formal contrasts.

| Model | Cells | Parse valid | Mean input/output tokens | Returned provider |
|---|---:|---:|---|---|
| meta-llama/llama-3.1-8b-instruct | 800 | 800 | 307.6/23.2 | Groq |
| qwen/qwen3-8b | 800 | 800 | 290.3/19.3 | Alibaba |

| Model | Core all-planned accuracy | Core macro-label accuracy | Label-control accuracy |
|---|---:|---:|---:|
| meta-llama/llama-3.1-8b-instruct | 0.858 | 0.717 | 1.000 |
| qwen/qwen3-8b | 0.846 | 0.798 | 0.700 |

## Descriptive cell behavior

Cells below contain 40 planned pilot families each. q is subjective target truth, not calibrated probability or probability of entailment. Accuracy uses intended-reading gold, with all planned outcomes in its denominator. Labels are intrinsically imbalanced; primary distinctions remain per-cell rather than pooled accuracy.

| Model | Layer | VP | Context | Valid / planned | Accuracy | Mean q |
|---|---|---|---|---:|---:|---:|
| llama-3.1-8b-instruct | micro | bounded | cancelling | 40/40 | 1.000 | 0.000 |
| llama-3.1-8b-instruct | micro | bounded | neutral | 40/40 | 0.475 | 0.762 |
| llama-3.1-8b-instruct | micro | bounded | supportive | 40/40 | 1.000 | 1.000 |
| llama-3.1-8b-instruct | micro | unbounded | cancelling | 40/40 | 1.000 | 1.000 |
| llama-3.1-8b-instruct | micro | unbounded | neutral | 40/40 | 1.000 | 1.000 |
| llama-3.1-8b-instruct | micro | unbounded | supportive | 40/40 | 1.000 | 1.000 |
| llama-3.1-8b-instruct | nonce | bounded | cancelling | 40/40 | 1.000 | 0.000 |
| llama-3.1-8b-instruct | nonce | bounded | neutral | 40/40 | 0.125 | 0.463 |
| llama-3.1-8b-instruct | nonce | bounded | supportive | 40/40 | 1.000 | 1.000 |
| llama-3.1-8b-instruct | nonce | unbounded | cancelling | 40/40 | 1.000 | 1.000 |
| llama-3.1-8b-instruct | nonce | unbounded | neutral | 40/40 | 1.000 | 0.982 |
| llama-3.1-8b-instruct | nonce | unbounded | supportive | 40/40 | 1.000 | 1.000 |
| llama-3.1-8b-instruct | real | bounded | cancelling | 40/40 | 0.750 | 0.250 |
| llama-3.1-8b-instruct | real | bounded | neutral | 40/40 | 0.100 | 0.463 |
| llama-3.1-8b-instruct | real | bounded | supportive | 40/40 | 1.000 | 1.000 |
| llama-3.1-8b-instruct | real | unbounded | cancelling | 40/40 | 1.000 | 1.000 |
| llama-3.1-8b-instruct | real | unbounded | neutral | 40/40 | 1.000 | 1.000 |
| llama-3.1-8b-instruct | real | unbounded | supportive | 40/40 | 1.000 | 1.000 |
| qwen3-8b | micro | bounded | cancelling | 40/40 | 1.000 | 0.000 |
| qwen3-8b | micro | bounded | neutral | 40/40 | 1.000 | 0.540 |
| qwen3-8b | micro | bounded | supportive | 40/40 | 1.000 | 1.000 |
| qwen3-8b | micro | unbounded | cancelling | 40/40 | 1.000 | 1.000 |
| qwen3-8b | micro | unbounded | neutral | 40/40 | 1.000 | 1.000 |
| qwen3-8b | micro | unbounded | supportive | 40/40 | 1.000 | 1.000 |
| qwen3-8b | nonce | bounded | cancelling | 40/40 | 1.000 | 0.000 |
| qwen3-8b | nonce | bounded | neutral | 40/40 | 0.000 | 0.000 |
| qwen3-8b | nonce | bounded | supportive | 40/40 | 1.000 | 0.999 |
| qwen3-8b | nonce | unbounded | cancelling | 40/40 | 0.375 | 0.356 |
| qwen3-8b | nonce | unbounded | neutral | 40/40 | 0.350 | 0.713 |
| qwen3-8b | nonce | unbounded | supportive | 40/40 | 1.000 | 0.964 |
| qwen3-8b | real | bounded | cancelling | 40/40 | 0.900 | 0.102 |
| qwen3-8b | real | bounded | neutral | 40/40 | 0.600 | 0.622 |
| qwen3-8b | real | bounded | supportive | 40/40 | 1.000 | 1.000 |
| qwen3-8b | real | unbounded | cancelling | 40/40 | 1.000 | 0.988 |
| qwen3-8b | real | unbounded | neutral | 40/40 | 1.000 | 0.974 |
| qwen3-8b | real | unbounded | supportive | 40/40 | 1.000 | 0.976 |

## Remaining gates

Independent human semantic review and prior ratings remain **not completed**. The blank semantic form has 2,880 candidate rows and zero actual reviewer judgments. Main generated-benchmark collection is pending the user’s review disposition, then a dated freeze. Without genuine review, natural-language labels remain operational and intended-prior WKE remains exploratory. No confirmatory claim, externally preregistered study, finished paper, or publication-ready PDF is implied.

Diagnostic figure: `figures/pilot_diagnostic.pdf` and its source/caption manifest. Raw visible responses, pinned request payloads, provider metadata, all attempts and unknown-charge reserves are retained under `data/raw_runs/pilot_v2/`. Re-running collection only schedules failed/missing transport payloads; successful outputs are immutable.
