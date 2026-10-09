from pathlib import Path
import json,time,subprocess,sys,fcntl
ROOT=Path(__file__).resolve().parents[1]
with (ROOT/'.runtime/table_export.lock').open('w') as lock:
 fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 while True:
  try:s=json.loads((ROOT/'reports/pipeline_progress.json').read_text())
  except (FileNotFoundError,json.JSONDecodeError):time.sleep(10);continue
  if s['stage']=='pipeline_failed':raise SystemExit('Empirical pipeline failed; no paper-table export.')
  if s['stage']=='analysis_complete_manuscript_revision_pending':break
  time.sleep(10)
 with (ROOT/'reports/table_execution.log').open('a') as log:
  for name in ['export_paper_tables.py','audit_integrity.py']:
   subprocess.run([sys.executable,str(ROOT/'scripts'/name)],stdout=log,stderr=log,check=True)
 (ROOT/'reports/table_progress.json').write_text(json.dumps({'stage':'exported_manuscript_interpretation_pending','submission_ready':False},indent=2)+'\n')
