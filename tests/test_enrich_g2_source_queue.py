"""Defensive tests for full-source queue label hydration."""
import copy
import json
import unittest
from pathlib import Path
from sys import path as sys_path
ROOT=Path(__file__).resolve().parents[1]
sys_path.insert(0,str(ROOT/"tools"))
from enrich_g2_source_queue import enrich

class HydrateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pins=json.loads((ROOT/"governance/coverage/pinned-dtg-spec-term-trees.json").read_text())
        cls.matched=json.loads((ROOT/"governance/coverage/dtg-g2-adjudications.json").read_text())

    def test_missing_checkout_fails_closed(self):
        with self.assertRaises(Exception):
            enrich(self.pins,self.matched,Path("/nonexistent-pinned-dtg-source"))

    def test_missing_term_file_rejected_before_source_access(self):
        pins=copy.deepcopy(self.pins)
        pins["repositories"][0]["term_files"].pop()
        with self.assertRaises(ValueError):
            enrich(pins,self.matched,Path("/nonexistent-pinned-dtg-source"))

    def test_ambiguous_orphan_matched_source_rejected(self):
        matched=copy.deepcopy(self.matched)
        matched["source_rows"][0]["source_path"]="spec/terms-definitions/no-such-definition.md"
        with self.assertRaises(ValueError):
            enrich(self.pins,matched,Path("/nonexistent-pinned-dtg-source"))

if __name__=="__main__":
    unittest.main()
