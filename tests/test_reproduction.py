import hashlib,json,tempfile,unittest,shutil,importlib
from pathlib import Path
from unittest.mock import patch
import event_completion.generator as generator

class Reproduction(unittest.TestCase):
 def test_frozen_forms_load_without_os_dictionary(self):
  original=Path.read_text
  def read(p,*a,**kw):
   if str(p)=='/usr/share/dict/words':raise FileNotFoundError('Simulated non-macOS host')
   return original(p,*a,**kw)
  with patch.object(Path,'read_text',read):importlib.reload(generator)
  self.assertEqual(generator.NONCES,json.loads((generator.ROOT/'config/nonce_lexicon.json').read_text())['forms'])
 def test_generator_replays_all_frozen_stimuli_in_disposable_directory(self):
  root=generator.ROOT
  with tempfile.TemporaryDirectory(prefix='sac_event_replay_') as name:
   replay=Path(name);(replay/'config').mkdir();(replay/'data/generated').mkdir(parents=True)
   shutil.copyfile(root/'config/nonce_lexicon.json',replay/'config/nonce_lexicon.json')
   with patch.object(generator,'ROOT',replay):generator.generate()
   if (root/'data/generated/grammar_repair.jsonl').exists():
    from event_completion.wording import repair_rows
    core=[json.loads(x) for x in (replay/'data/generated/main_core.jsonl').read_text().splitlines()]
    generator.dump(replay/'data/generated/grammar_repair.jsonl',repair_rows(core))
   if (root/'data/generated/grammar_complete_main.jsonl').exists():
    from event_completion.wording_complete import generate_rows,MAIN_DATASETS,STRESS_DATASETS
    generator.dump(replay/'data/generated/grammar_complete_main.jsonl',generate_rows(replay,MAIN_DATASETS))
    generator.dump(replay/'data/generated/grammar_complete_stress.jsonl',generate_rows(replay,STRESS_DATASETS))
   expected=list((root/'data/generated').glob('*.jsonl'))
   self.assertEqual(len(expected),len(list((replay/'data/generated').glob('*.jsonl'))))
   for p in expected:self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),hashlib.sha256((replay/'data/generated'/p.name).read_bytes()).hexdigest(),p.name)
   self.assertEqual((root/'config/nonce_lexicon.json').read_bytes(),(replay/'config/nonce_lexicon.json').read_bytes())

if __name__=='__main__':unittest.main()
