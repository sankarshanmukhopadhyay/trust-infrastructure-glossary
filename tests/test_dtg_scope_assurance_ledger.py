import unittest
from pathlib import Path

class LedgerTests(unittest.TestCase):
    def test_generator_exists(self):
        self.assertTrue((Path(__file__).resolve().parents[1] / 'tools' / 'build_dtg_scope_assurance_ledger.py').is_file())
