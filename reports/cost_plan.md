# Preliminary cost plan

Checked 2026-10-07. No inference spend has occurred. All quantities are planned ceilings. Public [OpenRouter model catalogue](https://openrouter.ai/api/v1/models) was downloaded; prices are USD per token in the API and converted below to per million. Catalogue listing is not authenticated inference availability. [Official model documentation](https://openrouter.ai/docs/guides/overview/models) explains catalogue metadata. Refresh and pin provider price before pilot/full runs.

## Price and volume table

| Exact model ID | Input $/M | Output $/M | Planned requests | Expected $ (750 in, 128 out) | Conservative $ (1200 in, 512 out) |
|---|---:|---:|---:|---:|---:|
| `qwen/qwen3-8b` | 0.117 | 0.455 | 5,676 | 0.829 | 2.119 |
| `meta-llama/llama-3.1-8b-instruct` | 0.050 | 0.080 | 5,676 | 0.271 | 0.573 |
| `mistralai/ministral-8b-2512` | 0.150 | 0.150 | 4,876 | 0.642 | 1.252 |
| `google/gemma-3-12b-it` | 0.050 | 0.150 | 4,876 | 0.276 | 0.667 |
| `qwen/qwen3-14b` | 0.120 | 0.240 | 4,876 | 0.589 | 1.301 |
| `qwen/qwen3-32b` | 0.080 | 0.280 | 4,876 | 0.467 | 1.167 |
| `deepseek/deepseek-v3.2` | 0.280 | 0.420 | 660 | 0.174 | 0.364 |

Totals: **31,516 planned requests**, expected **$3.248**, conservative **$7.444** before retries. A 25% contingency gives **$9.304**. These include one pilot. Reproduce using `python3 scripts/plan_costs.py`; machine-readable arithmetic is `reports/cost_arithmetic.json`.

## Request arithmetic

Per main model: main_core=2160, original_replication=400, world_prior=240, label_controls=60, robustness_six_variants=1728, real_definition_control=288; total 4876. Six main models. Pilot: two models × (720 core + 60 plausibility + 20 label controls)=1,600 calls. Stress: 30 × 18 core + 20 × 6 plausibility=660. Robustness six variants each use 24 × 2 compositions × 3 presentations × 2 contexts=288/model; baseline reused. The definition-load control reserves 288/model; reusing unchanged Nonce/Micro baselines can reduce actual calls. Main label controls are separate.

Pilot conservative estimate **$0.379**, 25% contingency **$0.474**, below the $0.90 scheduling limit. Output cap planned at 256; 512 is a budget stress allowance, not a silent generation change. Original robustness plan used 30 families, but the conservative estimate plus contingency exceeded $10; before any calls this was reduced to 24, retaining all six variants and the complete main matrix.

## Enforced limits for later runner

Dry-run actual rendered prompts and token estimates before calling. Estimate all input including system messages, definitions and schemas; measure returned usage. If reasoning cannot be disabled, hidden reasoning tokens are included in billing; max_tokens behavior and provider-specific caps must be verified. This projection is not a hard guarantee against unbounded reasoning or price changes. Exclude free/batch tiers from the main study; no presumed cache discounts. Log actual cost per request/attempt from returned usage or generation metadata; if cost is unavailable, use conservative provider tariffs and mark estimated. A changed tariff requires an amendment before continuing.

Budget target $10 for all inference phases. Stop new scheduling at accumulated+in-flight worst-case commitment $9; $1 safety reserve. Pilot hard scheduling cap $0.90, including retries. Reserve a 25% retry contingency; three transport retries maximum, no retry of successfully received semantic or parsing errors. Successful calls reused by full content hash. Concurrency ≤4 initially. Never auto-switch to more expensive model/provider or expand families because results are nonsignificant. Optional OOD lexical families and repeated pilots use remaining budget only after revised arithmetic; omit optional additions if they do not fit.

No account/key/credits inspected and no access claim. API funds do not cover genuine human ratings, publication/APCs, registration, travel or compute. Human-study budget is unresolved and must not be hidden inside the $10 inference target.
