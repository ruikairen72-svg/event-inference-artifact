"""Report complete pilot usability without significance/effect-based selection."""
from pathlib import Path
import sys,json,collections,statistics
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from event_completion.analysis import load,summary
rows=load(ROOT/'data/analysis/pilot_v2_planned.jsonl')
if len(rows)!=1600 or any(r.get('missing') for r in rows):raise SystemExit('Complete planned pilot needed; resume missing transport requests first.')
attempts=load(ROOT/'data/raw_runs/pilot_v2/attempts.jsonl');allattempts=attempts+load(ROOT/'data/raw_runs/pilot_v1/attempts.jsonl')
actual=sum(r['charged_or_reserved_usd'] for r in allattempts if not r['cost_is_estimate']);ledger=sum(r['charged_or_reserved_usd'] for r in allattempts)
valid=sum(r.get('parsed') is not None for r in rows);truncated=sum(r.get('finish_reason')=='length' for r in rows)
passed=valid/len(rows)>=.98 and truncated==0 and ledger<.9
lines=['# Full pilot checkpoint — 2026-10-07','',f'All {len(rows):,} planned v2 cells have genuine transport responses. {valid:,} parse valid ({valid/len(rows):.2%}); {truncated} output-length truncations. No semantic or format-response retries were performed. The earlier 40-call v1 schema smoke remains archived and excluded from all v2/main estimates.','',f'Known returned pilot cost including v1: **${actual:.6f}**. Conservative ledger including unbilled/unknown-cost failed attempts: **${ledger:.6f}**. HTTP-failed attempts in v2: {sum(not r["transport_ok"] for r in attempts)}; these are attempts, not missing final items. This is local returned billing metadata, not an independent account invoice.','',f'Prompt-usability gate (≥98% parseable, no length truncation, pilot ledger <$0.90): **{"passed" if passed else "failed"}**. This is not semantic-validity certification. No effects, p-values, or significance thresholds were used to select the stimulus pool, models, sample size or formal contrasts.','', '| Model | Cells | Parse valid | Mean input/output tokens | Returned provider |','|---|---:|---:|---|---|']
for m in sorted({r['model'] for r in rows}):
 rr=[r for r in rows if r['model']==m];tokens='/'.join(f'{statistics.mean(r["usage"].get(k,0) for r in rr):.1f}' for k in ['prompt_tokens','completion_tokens']);providers=', '.join(sorted({r.get('returned_provider') or 'unspecified' for r in rr}))
 lines.append(f'| {m} | {len(rr)} | {sum(r.get("parsed") is not None for r in rr)} | {tokens} | {providers} |')
lines+=['','| Model | Core all-planned accuracy | Core macro-label accuracy | Label-control accuracy |','|---|---:|---:|---:|']
for m in sorted({r['model'] for r in rows}):
 core=[r for r in rows if r['model']==m and r['dataset']=='pilot_core'];controls=[r for r in rows if r['model']==m and r['dataset']=='pilot_labels']
 acc=sum(bool(r.get('correct')) for r in core)/len(core)
 macro=statistics.mean(sum(bool(r.get('correct')) for r in core if r['item']['gold']==gold)/sum(r['item']['gold']==gold for r in core) for gold in ['entailed','contradicted','unknown'])
 control=sum(bool(r.get('correct')) for r in controls)/len(controls)
 lines.append(f'| {m} | {acc:.3f} | {macro:.3f} | {control:.3f} |')
lines+=['','## Descriptive cell behavior','','Cells below contain 40 planned pilot families each. q is subjective target truth, not calibrated probability or probability of entailment. Accuracy uses intended-reading gold, with all planned outcomes in its denominator. Labels are intrinsically imbalanced; primary distinctions remain per-cell rather than pooled accuracy.','','| Model | Layer | VP | Context | Valid / planned | Accuracy | Mean q |','|---|---|---|---|---:|---:|---:|']
for c in summary([r for r in rows if r['dataset']=='pilot_core']):
 q='NA' if c['mean_q'] is None else f'{c["mean_q"]:.3f}'
 lines.append(f'| {c["model"].split("/")[-1]} | {c["knowledge"]} | {c["composition"]} | {c["context"]} | {c["parsed_n"]}/{c["n"]} | {c["accuracy"]:.3f} | {q} |')
lines+=['','## Remaining gates','','Independent human semantic review and prior ratings remain **not completed**. The blank semantic form has 2,880 candidate rows and zero actual reviewer judgments. Main generated-benchmark collection is pending the user’s review disposition, then a dated freeze. Without genuine review, natural-language labels remain operational and intended-prior WKE remains exploratory. No confirmatory claim, externally preregistered study, finished paper, or publication-ready PDF is implied.','','Diagnostic figure: `figures/pilot_diagnostic.pdf` and its source/caption manifest. Raw visible responses, pinned request payloads, provider metadata, all attempts and unknown-charge reserves are retained under `data/raw_runs/pilot_v2/`. Re-running collection only schedules failed/missing transport payloads; successful outputs are immutable.']
(ROOT/'reports/pilot_report.md').write_text('\n'.join(lines)+'\n')
print('Pilot report written; usability gate:',passed)
