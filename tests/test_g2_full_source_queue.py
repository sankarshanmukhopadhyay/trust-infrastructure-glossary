import copy
import json
import unittest
from pathlib import Path
from sys import path as sys_path
ROOT = Path(__file__).resolve().parents[1]
sys_path.insert(0, str(ROOT / "tools"))
from build_g2_full_source_queue import build, verify

class AllSourceQueueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pins = json.loads((ROOT / "governance/coverage/pinned-dtg-spec-term-trees.json").read_text())
        cls.matched = json.loads((ROOT / "governance/coverage/dtg-g2-adjudications.json").read_text())

    def test_all_106_pinned_source_files_accounted_for(self):
        report = build(self.pins, self.matched)
        verify(report)
        self.assertEqual(report["pinned_file_definition_count"], 106)
        self.assertEqual(report["first_pass_matched_count"], 17)
        self.assertEqual(report["without_lexical_candidate_count"], 89)
        self.assertEqual(sum(row["source_label"] is None for row in report["records"]), 89)

    def test_refuses_missing_pinned_source_file(self):
        pins = copy.deepcopy(self.pins)
        pins["repositories"][0]["term_files"].pop()
        with self.assertRaises(ValueError):
            build(pins, self.matched)

    def test_refuses_orphan_lexical_candidate(self):
        matched = copy.deepcopy(self.matched)
        matched["source_rows"][0]["source_path"] = "spec/terms-definitions/does-not-exist.md"
        with self.assertRaises(ValueError):
            build(self.pins, matched)

    def test_refuses_unreviewed_approval(self):
        report = build(self.pins, self.matched)
        report["records"][0]["semantic_disposition"] = "covered"
        with self.assertRaises(ValueError):
            verify(report)

if __name__ == "__main__":
    unittest.main()
