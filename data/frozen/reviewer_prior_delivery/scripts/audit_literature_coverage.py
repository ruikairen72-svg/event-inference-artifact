"""Count references in retrieved comparison PDFs, with version and layout evidence.

Full third-party PDFs are local reading resources and excluded from the review
archive. This audit can be rerun after retrieving the declared URLs. Counts are
purposive-sample observations, not estimates of a venue-wide distribution.
"""
from pathlib import Path
import hashlib, json, re, statistics
import fitz

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = [
    ('sac2025_simre', 'SimRE: A Requirements Similarity Tool for Software Product Lines', 'SAC 2025', 'SAC published-layout', 'https://lbd.udc.es/Repository/Publications/Drafts/1741695248136_227_220.pdf', '10.1145/3672608.3707758', 46),
    ('sac2026_validators', 'Robust LLM-as-a-Judge Validators for Assessing the Quality of Educational Exams', 'SAC 2026', 'SAC published-layout', 'https://rdegiovanni.github.io/publications/files/SAC2026_validators.pdf', '10.1145/3748522.3779926', 35),
    ('sac2024_process', 'Process Knowledge Extraction and Knowledge Graph Construction Through Prompting: A Quantitative Analysis', 'SAC 2024', 'SAC author draft (separate)', 'https://raw.githubusercontent.com/patriziobellan86/Process-Knowledge-Extraction-and-Knowledge-Graph-Construction-Through-Prompting/main/ProcessKnowledgeExtractionAndKnowledgeGraphConstructionThroughPrompting.pdf', '10.1145/3605098.3635957', 32),
    ('sac2024_retrofit_author', 'An Experiment in Retrofitting Competency Questions for Existing Ontologies', 'SAC 2024', 'SAC author preprint (separate)', 'https://arxiv.org/pdf/2311.05662', '10.1145/3605098.3636053', 28),
    ('prus2024', 'Human Temporal Inferences Go Beyond Aspectual Class', 'EACL 2024', 'Closest-topic NLP published', 'https://aclanthology.org/2024.eacl-long.115.pdf', '10.18653/v1/2024.eacl-long.115', 31),
    ('prus2025', 'World Knowledge Resolves Some Aspectual Ambiguity', 'Findings ACL 2025', 'Closest-topic NLP published', 'https://aclanthology.org/2025.findings-acl.683.pdf', '10.18653/v1/2025.findings-acl.683', 25),
    ('core_2025', 'CoRE: Condition-based Reasoning for Identifying Outcome Variance in Complex Events', 'Findings ACL 2025', 'Closest-topic NLP published', 'https://aclanthology.org/2025.findings-acl.992.pdf', '10.18653/v1/2025.findings-acl.992', 43),
    ('cxmp_2026', 'CxMP: A Linguistic Minimal-Pair Benchmark for Evaluating Constructional Understanding in Language Models', 'ACL 2026', 'Closest-topic NLP published', 'https://aclanthology.org/2026.acl-long.2132.pdf', '10.18653/v1/2026.acl-long.2132', 42),
]

def count_refs(name):
    path = ROOT / 'data/sources' / (name + '.pdf')
    doc = fitz.open(path)
    active = False
    entries = []
    start = stop = None
    for pn, page in enumerate(doc, 1):
        columns = [[], []]
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                t = ''.join(s['text'] for s in line['spans']).strip()
                x, y = line['bbox'][:2]
                if y > 775:
                    continue
                columns[int(x > 280)].append((y, x, t, max(s['size'] for s in line['spans'])))
        for col, lines in enumerate(columns):
            for y, x, t, size in sorted(lines):
                if t in ('References', 'REFERENCES'):
                    active = True
                    start = [pn, col, round(y, 2)]
                    continue
                if not active:
                    continue
                if name.startswith('sac'):
                    m = re.match(r'^\[(\d+)\](?:\s|$)', t)
                    if m:
                        entries.append({'number': int(m[1]), 'page': pn, 'column': col, 'y': round(y, 2)})
                else:
                    if size > 10.9 and (re.match(r'^[A-Z](?:\s|$)', t) or t.startswith('Appendix')):
                        active = False
                        stop = [pn, col, round(y, 2), t]
                    elif abs(x - (306.14 if col else 70.86)) < 1.2 and t and size < 10.8:
                        entries.append({'page': pn, 'column': col, 'y': round(y, 2), 'first_line': t})
    if name.startswith('sac'):
        numbers = [e['number'] for e in entries]
        assert numbers == list(range(1, len(numbers) + 1)), (name, numbers)
    return {'total_pdf_pages': len(doc), 'reference_start': start, 'reference_end_or_appendix': stop, 'reference_entries': entries, 'reference_count': len(entries), 'pdf_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}

def main():
    rows = []
    for name, title, venue, group, url, doi, expected in SAMPLES:
        row = {'id': name, 'title': title, 'venue': venue, 'group': group, 'pdf_url': url, 'published_work_doi': doi, **count_refs(name)}
        assert row['reference_count'] == expected, (name, row['reference_count'])
        row['version_note'] = ('First-page venue/date/DOI verified; author-hosted published-layout copy.' if group == 'SAC published-layout' else 'PDF has placeholder DOI/venue metadata; count applies only to this retrieved author version, excluded from published-layout range.' if name.startswith('sac') else 'Official ACL Anthology PDF; total length includes reference pages and any appendices.')
        rows.append(row)
    summaries = {}
    for group in ['SAC published-layout', 'Closest-topic NLP published']:
        values = [r['reference_count'] for r in rows if r['group'] == group]
        summaries[group] = {'n': len(values), 'range': [min(values), max(values)], 'median': statistics.median(values), 'individual_counts': values}
    tex = (ROOT / 'paper/manuscript.tex').read_text()
    bib = re.findall(r'\\bibitem\{([^}]+)\}', tex)
    cited = {k for group in re.findall(r'\\cite\{([^}]+)\}', tex) for k in group.split(',')}
    assert len(bib) == len(set(bib)) and set(bib) == cited
    report = {'selection': 'Purposive 2024–2026 sample: SAC eight-page applied NLP/LLM empirical studies for format; closest event/aspect/construction benchmarks at EACL/ACL/Findings for topic. Author drafts listed separately. Not random, exhaustive, a population common range, or a submission threshold.', 'count_method': 'Numbered SAC entries checked as contiguous 1..N; ACL hanging-indent first lines counted in column reading order from References to appendix. Coordinates retained; reference boundaries and numbering visually inspected.', 'samples': rows, 'observed_ranges': summaries, 'manuscript_before': 14, 'manuscript_after': len(bib), 'all_bibliography_items_cited_in_body': True, 'manuscript_sha256': hashlib.sha256(tex.encode()).hexdigest()}
    (ROOT / 'reports/literature_coverage_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print('Reference counts and manuscript coverage verified:', summaries, '14 ->', len(bib))

if __name__ == '__main__':
    main()
