import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('checks', ROOT / 'scripts/check_fixtures.py')
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)
class ContractTests(unittest.TestCase):
    def test_valid_fixture(self):
        self.assertEqual(checks.validate(), 2)
    def mutated(self, change):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / 'fixtures', root / 'fixtures')
            path = root / 'fixtures/programs.json'
            data = json.loads(path.read_text())
            change(data)
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                checks.validate(root)
    def test_reject_unknown_source(self):
        self.mutated(lambda d: d[0].update(source_ids=['nonexistent']))
    def test_reject_string_availability(self):
        self.mutated(lambda d: d[0].update(availability='probably'))
    def test_reject_reversed_age_range(self):
        self.mutated(lambda d: d[0].update(age_min=20))
    def test_reject_duplicate_ids(self):
        self.mutated(lambda d: d[1].update(id=d[0]['id']))
    def test_unknown_is_preserved_in_fixture(self):
        p=json.loads((ROOT/'fixtures/programs.json').read_text())[0]
        self.assertIsNone(p['availability'])
        self.assertIsNone(p['accommodations'])
if __name__ == '__main__':
    unittest.main()
