from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from event_completion.analysis import analyze_run
analyze_run(sys.argv[1],pilot='pilot' in sys.argv[1])
