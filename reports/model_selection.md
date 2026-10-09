# Model-selection protocol and catalogue audit

Checked 2026-10-07. Public [OpenRouter model endpoint](https://openrouter.ai/api/v1/models) was acquired without authentication or inference. Snapshot: `data/sources/openrouter_models.json`; selected metadata: `config/models_candidate.json`. **Listed is not callable:** credit, account permissions, live providers, schema support and reasoning controls remain pilot checks. No credentials were sought from other projects.

| Tier | Exact OpenRouter ID | Role |
|---|---|---|
| A + B | `qwen/qwen3-8b` | Small dense Qwen; pilot |
| A | `meta-llama/llama-3.1-8b-instruct` | Llama family; pilot |
| A | `mistralai/ministral-8b-2512` | Mistral family, small model |
| A | `google/gemma-3-12b-it` | Gemma family, 12B |
| B | `qwen/qwen3-14b` | Medium dense Qwen |
| B | `qwen/qwen3-32b` | Large dense Qwen |
| C | `deepseek/deepseek-v3.2` | One strong-model stress test, limited diagnostic set |

Four cross-family small/medium representatives, three Qwen size points (8/14/32 nominal B), one strong open-weight family. Six unique main systems because Qwen8 belongs to both A and B. Avoid substituting a VL Qwen2.5-72B for a text-only scaling point. The [Qwen author cards](https://huggingface.co/Qwen/Qwen3-8B), [14B](https://huggingface.co/Qwen/Qwen3-14B), [32B](https://huggingface.co/Qwen/Qwen3-32B) confirm dense variants and thinking/nonthinking modes. Use exact parameter counts from cards in final regression metadata, not rounded model names (cards give 8.2/14.8/32.8B); scale names 8/14/32 denote nominal classes, while the regression uses exact counts. [Ministral author card](https://huggingface.co/mistralai/Ministral-3-8B-Instruct-2512) identifies the intended generation. OpenRouter aliases/provider quantization may differ from author weights; hosted lineage is not sufficient for exact reproduction.

Selection is by coverage, identifiable within-family scale and catalogue cost—not pilot bias, significance or low accuracy. DeepSeek is a prespecified stress candidate, not a model we have independently established to be better on this task. It will not be deleted for ceiling performance. Original paper's seven models are not all listed at matching versions; report conceptual replication, not a seven-model exact rerun. Larger current Qwen3.7 variants have no comparable disclosed dense size in this protocol and do not substitute for the scale series.

## Pre-pilot freeze rules

1. Refresh catalogue/provider endpoints, validate account availability using only authorized credentials, and record provider IDs, quantization, tariff and supported parameters. Do not assume an upstream thinking switch is exposed by every provider.
2. Request temperature=0/top_p=1, max output 256, no tools or long reasoning. Prefer nonthinking mode for all Qwen3 sizes; preserve the same routing/decoding protocol across size points. If unavailable, explicitly stratify by reasoning mode and revise costs before runs.
3. Pin provider routing where possible, disallow silent model fallback. Same exact alias, provider and protocol for matched cells. Capture response model string, generation ID, usage and any upstream model version supplied. A hosted alias may still drift; record run dates and metadata.
4. Replacement allowed only for a documented availability/transport limitation before confirmatory inference. Use another listed 7–14B general model from the same family if possible, then closest general model by cost/size. Rewrite IDs, cost table and date before any replacement calls. Never select a replacement using semantic accuracy. For scale series, fewer than three comparable points means RQ7 unavailable, not filling with a cross-family model.
5. Parsing failures are scored/retained, not grounds to exclude a poorly performing system. Do not impose provider-specific answer repair prompts on just one model. If a format cannot be supported, revise a shared protocol in pilot, retain the original attempts and mark the amendment.
6. Quantization, modality support, release/training differences and instruction conventions limit scale/cross-family attribution. Use text-only inputs throughout, even for models supporting images. Active MoE parameter count is not substituted for dense total size; the stress model is outside scale regression.

Price units and arithmetic are in `cost_plan.md`. Authentication/inference checks deliberately await the approved blueprint and future pilot. Public metadata acquisition spent $0 on model inference.
