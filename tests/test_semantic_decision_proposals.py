import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SemanticDecisionTests(unittest.TestCase):
    def test_high_risk_proposals_have_no_approved_exact_mappings(self):
        proposals = json.loads((ROOT / "governance/coverage/dtg-semantic-decision-proposals.json").read_text())
        baseline = json.loads((ROOT / "governance/coverage/dtg-semantic-first-pass.json").read_text())
        source_keys = {(r["source_repository"], r["source_path"]) for r in baseline["records"]}
        self.assertEqual(len(proposals["cases"]), 6)
        self.assertEqual(len({x["case_id"] for x in proposals["cases"]}), 6)
        self.assertTrue(all((x["source_repository"], x["source_path"]) in source_keys for x in proposals["cases"]))
        self.assertTrue(all(x["approval"] == "pending" and x["canonical_change_allowed"] is False for x in proposals["cases"]))
        self.assertTrue(all(x["proposed_disposition"] in {"do_not_assert_exact_match", "hold_ambiguous"} for x in proposals["cases"]))
        self.assertEqual(proposals["status"], "proposed-for-review")


if __name__ == "__main__":
    unittest.main()
