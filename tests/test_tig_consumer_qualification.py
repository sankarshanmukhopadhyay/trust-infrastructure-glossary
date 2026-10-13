import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from validate_tig_consumer_qualification import validate_qualification


class TigConsumerQualificationTests(unittest.TestCase):
    def test_consumer_qualification_evidence_is_valid(self):
        evidence = validate_qualification()
        self.assertEqual(evidence["final_decision"]["state"], "bounded_work_complete")
        self.assertEqual({journey["consumer"] for journey in evidence["journeys"]}, {"human_reader", "machine_consumer"})

    def test_negative_cases_preserve_unapproved_semantic_state(self):
        evidence = validate_qualification()
        cases = {case["id"]: case for case in evidence["negative_cases"]}
        self.assertIn("negative-ambiguous-trust-task", cases)
        self.assertIn("negative-high-risk-canonical-mutation", cases)
        self.assertIn("negative-unmatched-terms", cases)
        for case in cases.values():
            self.assertEqual(case["result"], "PASS")


if __name__ == "__main__":
    unittest.main()
