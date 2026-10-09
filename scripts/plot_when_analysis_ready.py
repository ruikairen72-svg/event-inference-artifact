from pathlib import Path
import json,time,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
status=ROOT/'reports/pipeline_progress.json'
while True:
 try:s=json.loads(status.read_text())
 except (FileNotFoundError,json.JSONDecodeError):time.sleep(10);continue
 if s['stage']=='pipeline_failed':raise SystemExit('Collection/analysis pipeline failed; no empirical figure export.')
 if s['stage']=='analysis_complete_manuscript_revision_pending':break
 time.sleep(10)
with (ROOT/'reports/figure_execution.log').open('a') as log:
 subprocess.run([sys.executable,str(ROOT/'.research/figures/scripts/main_figures.py')],stdout=log,stderr=log,check=True)
(ROOT/'reports/figure_progress.json').write_text(json.dumps({'stage':'exported_visual_QA_pending','source':'completed main analysis','submission_ready':False},indent=2)+'\n')
