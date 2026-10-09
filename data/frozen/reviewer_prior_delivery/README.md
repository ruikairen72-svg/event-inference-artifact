# Endpoint Inference under Compatible Histories

Complete anonymous ACM SAC 2027 research artifact. The eight-page paper is `output/pdf/submission.pdf`; its editable source is `paper/manuscript.tex`. The local review package is `output/anonymous-reproducibility.zip`. No external submission or public release has been performed.

Six main systems cover 28,104 planned cells (27,984 unique payloads); a disjoint 30-family matched DeepSeek stress test adds 660 cells. The complete inherited-wording control adds 518 paired cells, including 180 reused initial corrections and 338 newly collected outcomes. All formal cells parse successfully; original primary outcomes and original benchmark gold remain unchanged. Pilot and generic-control cache reuse are explicitly distinguished from independent replication.

The user chose theory-derived operational predictions without human review. No human annotations or prior ratings exist. The contribution is a controlled diagnostic of occurrence, culmination and unresolved endpoints under inspectable compatible histories. It does not establish population-level language judgments, calibrated probabilities, causal internal world knowledge or a parameter-count scaling law. Primary lexical/family intervals and Holm tests remain separate from the complete exploratory BH families. Unusable mixed-model fits are disclosed and do not support inference.

## Offline reproduction

Extract the anonymous archive into a new directory. Use Python 3 with the observed package versions in `requirements-analysis.txt`. From that directory:

```sh
python3 scripts/verify_review_archive.py
python3 scripts/verify_retained_original.py
PYTHONPATH=src python3 -m unittest discover -s tests
python3 scripts/analyze_primary.py --input data/analysis/main_planned.jsonl --protocol config/study_protocol_frozen.json --output reports/primary_reproduced.json
python3 scripts/analyze_secondary.py
```

The original primary output is `reports/primary_results.json`. Compare its complete JSON with `primary_reproduced.json`; all 30 contrasts are deterministic. Save the original `secondary_results.json` before the last command to compare all 380 secondary rows, 30 family-only interval sensitivities and seven matched stress systems. The final offline audit records independent extraction and exact numerical comparisons. No API key or network call is needed for these checks.

The 25 tests include disposable-directory byte-identical generation of every current stimulus JSONL, including both wording supplements. Never regenerate over a frozen release. Frozen nonce forms are portable; replay does not require the historical system dictionary. `src/event_completion/wording_complete.py` supplies deterministic counterparts while preserving source variants, schemas and theory gold.

Surface-baseline fitting uses disjoint pilot gold and main text; it is a supervised recoverability diagnostic, not a zero-shot leaderboard. Mixed-model fitting additionally requires R 4.6.1/lme4 2.0.6 as recorded in `mixed_models.json`; runtime libraries are excluded from the archive. Of 32 attempted fits, only one exploratory prior fit was usable. Primary inference uses the frozen cluster procedure rather than these fits.

## Figures and paper

Empirical figures include PDF, editable-text SVG and PNG exports, captions, source manifests and denominator records under `figures/` and `.research/figures/`. The placed category-accuracy figure and all eight final paper pages have been visually inspected. Claim/table reconciliation and font/page/metadata checks are retained in `reports/`.

The unchanged official SAC class is `paper/template/acmart.cls` v2.19. `python3 scripts/build_submission_pdf.py` builds with an existing Tectonic 0.17.0 executable and its cached dependencies; no compiler is distributed. The native standalone editor cannot resolve this project's external figure and uses a different bundled class, so its preview is not the verified final PDF. The exported final PDF and its compilation audit are authoritative.

## Provenance and limitations

`data/frozen/theory_main_v1` is a local precollection freeze, not external preregistration. Post-freeze amendments and wording controls are dated and descriptive; they do not replace primary estimates or add confirmatory tests. Original ImperfectiveNLI labels are retained unchanged, alongside separately attributed published concern flags. Original full/filtered/explicit-noncompletion analyses answer different diagnostic questions.

The dataset is attributed to Ma and Miyao (ACL 2026), pinned upstream commit `938ef893c3368f3a597e6add2cfebdad02fddebf`; their paper specifies CC BY-NC 4.0 for the dataset. The archive excludes unlicensed upstream code and full third-party papers/books. Source citations and retained hashes remain. Rebuilding original request prompts additionally requires separately acquiring the pinned source with `acquire_original_source.py`; materialized offline analyses do not require it. Archive notices do not create a new public license grant.

No credentials are included. Collectors are retained for provenance, but completed outcomes need no new collection. Collection must remain sequential under a single conservative budget ledger, with provider fallback disabled and no retries of semantic errors. Known returned charges total $0.9224; the conservative project ledger including unknown-charge reserves totals $2.0425. These are recorded API metadata and reserves, not independently reconciled invoices.

`final_project_report.md`, `completion_requirements.md`, `final_submission_audit.json`, and `offline_reproduction_audit.json` document completion and material scientific limitations. All quality review is agent self-review; no acceptance probability is estimated.

## Editorial revision

The 2026-10-09 revision strengthens the contribution-led argument, consolidates task assumptions, adds a mechanism figure and three verified references, and produces a seven-page paper. `paper/author_checklist.md` and `paper/supplementary_results.md` separate editorial/administrative checks and detailed supporting outcomes from the article. Data, gold and numerical analyses are unchanged. Previous phases 6–12 describe the prior delivery; their evidence is preserved in `data/frozen/editorial_prior_delivery`. The prior editorial source/PDF/figure hashes and scientific checks are recorded in `reports/editorial_revision_audit.json` and `reports/editorial_revision.sha256`.

## Literature coverage revision

The current paper has eight total pages and 32 body-cited references (previously 14). Verified 2024–2026 comparison counts, version distinctions and residual coverage/access boundaries are outside the article in `reports/literature_coverage_report.md`. Current source/PDF and claim audit: `reports/literature_revision_audit.json` and `reports/literature_revision.sha256`. The previous seven-page editorial delivery and its hash evidence are preserved in `data/frozen/literature_prior_delivery`; earlier phases 6–12 remain in `data/frozen/editorial_prior_delivery`. All 60 independently tested scientific components are unchanged; no new experiment or numerical estimate was introduced.
