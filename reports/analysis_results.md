# Main analysis results

theory-derived operational evaluation, not human validated. Local freeze is not external preregistration. All tables use real planned responses; no generated prediction is an observation.

Known returned cost: $0.905627; conservative ledger: $2.013209. Unknown-charge attempts are reserved, not assumed free.

| Model | Dataset | Planned | Missing | Parse valid | All-planned accuracy | Macro label accuracy |
|---|---|---:|---:|---:|---:|---:|
| deepseek/deepseek-v3.2 | stress_core | 540 | 0 | 540 | 0.9611 | 0.9222 |
| deepseek/deepseek-v3.2 | stress_prior | 120 | 0 | 120 | 0.7667 | 0.7667 |
| google/gemma-3-12b-it | label_only | 288 | 0 | 288 | 0.9375 | 0.9167 |
| google/gemma-3-12b-it | label_order | 288 | 0 | 288 | 0.9444 | 0.9259 |
| google/gemma-3-12b-it | main_core | 2160 | 0 | 2160 | 0.9477 | 0.8954 |
| google/gemma-3-12b-it | main_labels | 60 | 0 | 60 | 1.0000 | 1.0000 |
| google/gemma-3-12b-it | main_prior | 240 | 0 | 240 | 0.8208 | 0.8208 |
| google/gemma-3-12b-it | name | 288 | 0 | 288 | 0.9479 | 0.9306 |
| google/gemma-3-12b-it | natural_rule | 288 | 0 | 288 | 0.8958 | 0.8611 |
| google/gemma-3-12b-it | original | 400 | 0 | 400 | 0.5750 | 0.4383 |
| google/gemma-3-12b-it | real_definition | 96 | 0 | 96 | 0.9479 | 0.9306 |
| google/gemma-3-12b-it | structural_rule | 288 | 0 | 288 | 0.9062 | 0.8750 |
| google/gemma-3-12b-it | template_ood | 288 | 0 | 288 | 0.9097 | 0.8843 |
| meta-llama/llama-3.1-8b-instruct | label_only | 288 | 0 | 288 | 0.7951 | 0.7269 |
| meta-llama/llama-3.1-8b-instruct | label_order | 288 | 0 | 288 | 0.7500 | 0.6690 |
| meta-llama/llama-3.1-8b-instruct | main_core | 2160 | 0 | 2160 | 0.8569 | 0.7139 |
| meta-llama/llama-3.1-8b-instruct | main_labels | 60 | 0 | 60 | 1.0000 | 1.0000 |
| meta-llama/llama-3.1-8b-instruct | main_prior | 240 | 0 | 240 | 0.5917 | 0.5917 |
| meta-llama/llama-3.1-8b-instruct | name | 288 | 0 | 288 | 0.7674 | 0.6898 |
| meta-llama/llama-3.1-8b-instruct | natural_rule | 288 | 0 | 288 | 0.8646 | 0.8194 |
| meta-llama/llama-3.1-8b-instruct | original | 400 | 0 | 400 | 0.5325 | 0.3950 |
| meta-llama/llama-3.1-8b-instruct | real_definition | 96 | 0 | 96 | 0.8333 | 0.7778 |
| meta-llama/llama-3.1-8b-instruct | structural_rule | 288 | 0 | 288 | 0.8472 | 0.7963 |
| meta-llama/llama-3.1-8b-instruct | template_ood | 288 | 0 | 288 | 0.7188 | 0.6250 |
| mistralai/ministral-8b-2512 | label_only | 288 | 0 | 288 | 0.5729 | 0.7106 |
| mistralai/ministral-8b-2512 | label_order | 288 | 0 | 288 | 0.4688 | 0.6250 |
| mistralai/ministral-8b-2512 | main_core | 2160 | 0 | 2160 | 0.6616 | 0.7926 |
| mistralai/ministral-8b-2512 | main_labels | 60 | 0 | 60 | 1.0000 | 1.0000 |
| mistralai/ministral-8b-2512 | main_prior | 240 | 0 | 240 | 0.8500 | 0.8500 |
| mistralai/ministral-8b-2512 | name | 288 | 0 | 288 | 0.4931 | 0.6366 |
| mistralai/ministral-8b-2512 | natural_rule | 288 | 0 | 288 | 0.5000 | 0.6481 |
| mistralai/ministral-8b-2512 | original | 400 | 0 | 400 | 0.5850 | 0.4983 |
| mistralai/ministral-8b-2512 | real_definition | 96 | 0 | 96 | 0.4896 | 0.6111 |
| mistralai/ministral-8b-2512 | structural_rule | 288 | 0 | 288 | 0.5312 | 0.6713 |
| mistralai/ministral-8b-2512 | template_ood | 288 | 0 | 288 | 0.6146 | 0.7176 |
| qwen/qwen3-14b | label_only | 288 | 0 | 288 | 0.7500 | 0.7616 |
| qwen/qwen3-14b | label_order | 288 | 0 | 288 | 0.7083 | 0.7222 |
| qwen/qwen3-14b | main_core | 2160 | 0 | 2160 | 0.8153 | 0.8000 |
| qwen/qwen3-14b | main_labels | 60 | 0 | 60 | 1.0000 | 1.0000 |
| qwen/qwen3-14b | main_prior | 240 | 0 | 240 | 0.9000 | 0.9000 |
| qwen/qwen3-14b | name | 288 | 0 | 288 | 0.7882 | 0.7824 |
| qwen/qwen3-14b | natural_rule | 288 | 0 | 288 | 0.7361 | 0.7454 |
| qwen/qwen3-14b | original | 400 | 0 | 400 | 0.6800 | 0.5800 |
| qwen/qwen3-14b | real_definition | 96 | 0 | 96 | 0.9375 | 0.9167 |
| qwen/qwen3-14b | structural_rule | 288 | 0 | 288 | 0.7257 | 0.7407 |
| qwen/qwen3-14b | template_ood | 288 | 0 | 288 | 0.8125 | 0.8102 |
| qwen/qwen3-32b | label_only | 288 | 0 | 288 | 0.9271 | 0.9236 |
| qwen/qwen3-32b | label_order | 288 | 0 | 288 | 0.9167 | 0.9213 |
| qwen/qwen3-32b | main_core | 2160 | 0 | 2160 | 0.9375 | 0.9403 |
| qwen/qwen3-32b | main_labels | 60 | 0 | 60 | 1.0000 | 1.0000 |
| qwen/qwen3-32b | main_prior | 240 | 0 | 240 | 0.8625 | 0.8625 |
| qwen/qwen3-32b | name | 288 | 0 | 288 | 0.9062 | 0.9167 |
| qwen/qwen3-32b | natural_rule | 288 | 0 | 288 | 0.8889 | 0.9028 |
| qwen/qwen3-32b | original | 400 | 0 | 400 | 0.6325 | 0.5100 |
| qwen/qwen3-32b | real_definition | 96 | 0 | 96 | 0.9062 | 0.8750 |
| qwen/qwen3-32b | structural_rule | 288 | 0 | 288 | 0.9201 | 0.9259 |
| qwen/qwen3-32b | template_ood | 288 | 0 | 288 | 0.9340 | 0.9375 |
| qwen/qwen3-8b | label_only | 288 | 0 | 288 | 0.7535 | 0.7616 |
| qwen/qwen3-8b | label_order | 288 | 0 | 288 | 0.7535 | 0.7500 |
| qwen/qwen3-8b | main_core | 2160 | 0 | 2160 | 0.8370 | 0.7949 |
| qwen/qwen3-8b | main_labels | 60 | 0 | 60 | 0.6667 | 0.6667 |
| qwen/qwen3-8b | main_prior | 240 | 0 | 240 | 0.8250 | 0.8250 |
| qwen/qwen3-8b | name | 288 | 0 | 288 | 0.7465 | 0.7500 |
| qwen/qwen3-8b | natural_rule | 288 | 0 | 288 | 0.7361 | 0.7431 |
| qwen/qwen3-8b | original | 400 | 0 | 400 | 0.5750 | 0.4350 |
| qwen/qwen3-8b | real_definition | 96 | 0 | 96 | 0.9375 | 0.9167 |
| qwen/qwen3-8b | structural_rule | 288 | 0 | 288 | 0.7431 | 0.7546 |
| qwen/qwen3-8b | template_ood | 288 | 0 | 288 | 0.6910 | 0.6991 |

## Prespecified 30-test family

Paired family contrasts, lexical-block sign flips, Holm correction across all five contrasts × six main systems. Values in q units or accuracy units; q is uncalibrated subjective target truth. Complete-pair counts and adverse missing-q bounds are retained in the JSON.

| Model | Contrast | Valid/planned families | Estimate | Cluster CI95 | p Holm |
|---|---|---:|---:|---|---:|
| qwen/qwen3-8b | neutral_cs_target_real | 120/120 | -0.3437 | [-0.4575, -0.2204] | 0.0429688 |
| qwen/qwen3-8b | neutral_cs_real_minus_nonce | 120/120 | 0.3725 | [0.2350, 0.5208] | 0.0146484 |
| qwen/qwen3-8b | neutral_cs_real_minus_micro | 120/120 | 0.1562 | [0.0425, 0.2796] | 0.279297 |
| qwen/qwen3-8b | bounded_real_cancel_minus_neutral_q | 120/120 | -0.4846 | [-0.5854, -0.3808] | 0.0146484 |
| qwen/qwen3-8b | structural_rule_minus_baseline_accuracy | 24/24 | -0.0069 | [-0.0263, 0.0109] | 1 |
| meta-llama/llama-3.1-8b-instruct | neutral_cs_target_real | 120/120 | -0.5042 | [-0.7125, -0.3000] | 0.0649414 |
| meta-llama/llama-3.1-8b-instruct | neutral_cs_real_minus_nonce | 120/120 | -0.0158 | [-0.2225, 0.1858] | 1 |
| meta-llama/llama-3.1-8b-instruct | neutral_cs_real_minus_micro | 120/120 | -0.3208 | [-0.5375, -0.1083] | 0.240234 |
| meta-llama/llama-3.1-8b-instruct | bounded_real_cancel_minus_neutral_q | 120/120 | -0.2792 | [-0.4209, -0.1375] | 0.109375 |
| meta-llama/llama-3.1-8b-instruct | structural_rule_minus_baseline_accuracy | 24/24 | 0.0382 | [0.0083, 0.0667] | 0.279297 |
| mistralai/ministral-8b-2512 | neutral_cs_target_real | 120/120 | -0.2477 | [-0.3614, -0.1405] | 0.0649414 |
| mistralai/ministral-8b-2512 | neutral_cs_real_minus_nonce | 120/120 | -0.2477 | [-0.3614, -0.1405] | 0.0649414 |
| mistralai/ministral-8b-2512 | neutral_cs_real_minus_micro | 120/120 | -0.2477 | [-0.3614, -0.1405] | 0.0649414 |
| mistralai/ministral-8b-2512 | bounded_real_cancel_minus_neutral_q | 120/120 | -0.4462 | [-0.6021, -0.2767] | 0.0429688 |
| mistralai/ministral-8b-2512 | structural_rule_minus_baseline_accuracy | 24/24 | 0.0312 | [0.0000, 0.0679] | 1 |
| google/gemma-3-12b-it | neutral_cs_target_real | 120/120 | -0.2735 | [-0.4170, -0.1411] | 0.109375 |
| google/gemma-3-12b-it | neutral_cs_real_minus_nonce | 120/120 | 0.4210 | [0.2899, 0.5414] | 0.0146484 |
| google/gemma-3-12b-it | neutral_cs_real_minus_micro | 120/120 | 0.0165 | [-0.1270, 0.1489] | 1 |
| google/gemma-3-12b-it | bounded_real_cancel_minus_neutral_q | 120/120 | -0.6646 | [-0.8053, -0.5109] | 0.0146484 |
| google/gemma-3-12b-it | structural_rule_minus_baseline_accuracy | 24/24 | -0.0278 | [-0.0516, -0.0032] | 0.703125 |
| qwen/qwen3-14b | neutral_cs_target_real | 120/120 | -0.3146 | [-0.4154, -0.2025] | 0.0649414 |
| qwen/qwen3-14b | neutral_cs_real_minus_nonce | 120/120 | 0.2333 | [0.1300, 0.3483] | 0.0146484 |
| qwen/qwen3-14b | neutral_cs_real_minus_micro | 120/120 | -0.0621 | [-0.1750, 0.0608] | 1 |
| qwen/qwen3-14b | bounded_real_cancel_minus_neutral_q | 120/120 | -0.6767 | [-0.7842, -0.5817] | 0.0146484 |
| qwen/qwen3-14b | structural_rule_minus_baseline_accuracy | 24/24 | 0.0000 | [-0.0192, 0.0208] | 1 |
| qwen/qwen3-32b | neutral_cs_target_real | 120/120 | -0.3083 | [-0.4100, -0.1975] | 0.0429688 |
| qwen/qwen3-32b | neutral_cs_real_minus_nonce | 120/120 | -0.0742 | [-0.1996, 0.0671] | 1 |
| qwen/qwen3-32b | neutral_cs_real_minus_micro | 120/120 | 0.2767 | [0.1692, 0.3917] | 0.0146484 |
| qwen/qwen3-32b | bounded_real_cancel_minus_neutral_q | 120/120 | -0.6917 | [-0.8025, -0.5900] | 0.0146484 |
| qwen/qwen3-32b | structural_rule_minus_baseline_accuracy | 24/24 | 0.0174 | [-0.0031, 0.0362] | 1 |

Do not interpret a probability difference with correct categorical labels as a logical error. Layer contrasts also change definitions/notation/length. Intended-prior effects lack human ratings and remain exploratory. Rule and robustness conditions are not pooled into baseline cell accuracy. Source/filter details and unchanged original-gold outcomes are in `analysis_results.json`; mixed-model convergence is reported separately.
