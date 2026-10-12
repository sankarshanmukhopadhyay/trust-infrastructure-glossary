import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_source_review_queue import report


class ReviewQueueTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "governance/coverage/dtg-vtc-pilot.json").read_text(encoding="utf-8"))
        self.tmp = tempfile.TemporaryDirectory()
        self.terms = Path(self.tmp.name)
        (self.terms / "task.yaml").write_text(yaml.safe_dump({
            "concept_id": "urn:tig:concept:trust-task",
            "term": "trust-task",
            "aliases": ["Trust Task"],
            "designations": [],
        }), encoding="utf-8")
        (self.terms / "credential.yaml").write_text(yaml.safe_dump({
            "concept_id": "urn:tig:concept:delegation-credential",
            "term": "delegation-credential",
            "designations": [{"label": "Delegation Credential"}],
        }), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_review_queue_preserves_unverified_status(self):
        result = report(self.data, self.terms)
        self.assertEqual(result["coverage_denominator"], None)
        self.assertEqual(result["candidate_count"], 11)
        self.assertTrue(all(x["semantic_equivalence"] == "not_established" for x in result["queue"]))
        self.assertFalse(any(x["review_state"] == "covered" for x in result["queue"]))

    def test_review_queue_is_deterministic(self):
        self.assertEqual(report(self.data, self.terms), report(self.data, self.terms))

    def test_conflicting_lexical_mapping_is_flagged_not_overwritten(self):
        data = copy.deepcopy(self.data)
        task = next(x for x in data["candidates"] if x["label"] == "Trust Task")
        task["concept_id"] = "urn:tig:concept:delegation-credential"
        result = report(data, self.terms)
        finding = next(x for x in result["queue"] if x["label"] == "Trust Task")
        self.assertTrue(finding["lexical_conflict"])
        self.assertEqual(finding["current_concept_id"], "urn:tig:concept:delegation-credential")
        self.assertEqual(finding["review_priority"], "high")


if __name__ == "__main__":
    unittest.main()
