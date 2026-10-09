# Review artifact download

The complete, hash-verified frozen artifact is available as [anonymous-reproducibility.zip](anonymous-reproducibility.zip). Download and extract it into a separate directory before running the offline reproduction commands below. The ZIP contains all 513 manifested files, including the three JSONL files that exceed GitHub's normal per-file size limit.

The browsable repository contains source code and supporting materials. Three large files are available inside the ZIP only:

- `data/analysis/main_planned.jsonl`
- `data/frozen/editorial_prior_delivery/data/analysis/main_planned.jsonl`
- `data/raw_runs/main_v1/responses.jsonl`

Run `python3 scripts/verify_review_archive.py` from the extracted ZIP directory to verify the complete artifact. The ZIP's original README and all its contents are unchanged; this download note is specific to repository hosting.

---

# Endpoint Inference under Compatible Histories

The anonymous main paper is `output/pdf/submission.pdf` (eight pages, 32 verified references), with editable source `paper/manuscript.tex`. Readable supporting material is `output/pdf/supplementary.pdf` (five pages), with source `paper/supplementary.tex`. The local anonymous package is `output/anonymous-reproducibility.zip`. No venue upload or public release has occurred.

The contribution operationalizes compatible-history semantics for occurrence, culmination and unresolved outcomes, and combines category-specific diagnosis with an exact word-count-collision role-binding control. The original 120-family core contains 12 real lemmas. The supplementary challenge contains 12 lexical blocks including six benchmark-held-out predicates, shared-premise dual targets and absent/unobserved activity. Its exact deterministic word-unigram accuracy ceiling is 60%; all seven systems score 66.7–93.3%, while the unchanged pilot-trained unigram baseline scores 40%. Core Micro ceiling systems fall to 63.3–75.8% on the expanded task; all contrary and adverse outcomes remain visible.

The unchanged original suite contains 28,104 planned cells/27,984 unique payloads, 660 stress cells, and 518 wording pairs (180 cached plus 338 new calls). The supplementary challenge adds 5,040 initial cells and a complete 1,680-cell Nonce definition-precision check. Final challenge results use precise event-occurrence definitions, reusing the 3,360 content-identical Real/Micro cells. Initial versions and outcomes are retained separately. The 60 original scientific components, original gold and all original estimates are byte-identical. Theory labels come from the stated histories and predicates, not model answers or human annotations.

## Offline reproduction

Extract the archive into a new directory with Python3 and the observed analysis dependencies in `requirements-analysis.txt`. No API key or new calls are needed.

```sh
python3 scripts/verify_review_archive.py
python3 scripts/verify_retained_original.py
PYTHONPATH=src python3 -m unittest discover -s tests
python3 scripts/analyze_primary.py --input data/analysis/main_planned.jsonl --protocol config/study_protocol_frozen.json --output reports/primary_reproduced.json
python3 scripts/analyze_secondary.py
python3 scripts/analyze_reviewer_diagnostics.py
python3 scripts/analyze_binding_challenge.py
```

Save the original JSON reports before rerunning them. The full primary JSON, full secondary JSON and supplementary reports should reproduce exactly. The tests use disposable fixtures to replay all original generated stimuli, verify the supplementary oracle and exact feature collisions, check all revised definition pairs, and compare all collector inference payloads against the unchanged main collector. Complete primary intervals and original replication are readable in the supplement.

Historical checkpoint hashes are verified against their preserved prior-delivery snapshots when current editorial artifacts have changed. The latest revision continuity audit is `reports/reviewer_revision_audit.json`; independent extraction evidence is `reports/reviewer_offline_reproduction.json`. Original extraction evidence remains unchanged in `reports/offline_reproduction_audit.json`.

## Collection and provenance

The supplementary dataset is outside the original generator directory, in `data/supplementary/`. Collection-time sources and the original supplementary protocol remain in `data/frozen/reviewer_binding_collection/`. The later definition amendment precedes its changed payloads. Technical probes are retained and excluded by exact inference protocol hashes. Duplicate payloads use the earliest timestamp regardless of correctness; successful wrong answers are never retried. Original 30-test Holm and 380-row secondary results remain unchanged; new analyses are supplementary descriptions.

All sources, model endpoints, raw responses, attempts, budget reserves, source-backed figures and scripts are retained as appropriate for offline review. Credentials, third-party full texts and unlicensed upstream code are excluded. The reference-coverage sample and bibliographic access boundaries are in `reports/literature_coverage_report.md`.

The main paper uses the unchanged official SAC acmart class. Build with an existing compiler via `python3 scripts/build_submission_pdf.py`; build the single-column companion via `python3 scripts/build_reviewer_supplement.py`. The desktop editor compiles the single-file supplement; its standalone compiler cannot resolve the main paper's external figures. The exported main PDF is independently compiled with the retained official template.
