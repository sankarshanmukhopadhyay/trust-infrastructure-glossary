"""Ensure the six G2 review dossiers remain source-grounded and unapproved."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "governance/completion/tig-high-risk-semantic-adjudication-packet.md"
PROPOSALS = ROOT / "governance/coverage/dtg-semantic-decision-proposals.json"


class DossierTests(unittest.TestCase):
    def test_all_high_risk_cases_covered(self):
        text = PACKET.read_text(encoding="utf-8")
        cases = json.loads(PROPOSALS.read_text(encoding="utf-8"))["cases"]
        self.assertEqual(len(cases), 6)
        for c in cases:
            self.assertIn(c["case_id"], text)
            self.assertIn(f"/blob/{c['source_commit']}/{c['source_path']}", text)
            self.assertEqual(c["approval"], "pending")
            self.assertFalse(c["canonical_change_allowed"])

    def test_no_false_exact_mapping_or_completion(self):
        text = PACKET.read_text(encoding="utf-8")
        self.assertIn("NOT APPROVED", text)
        self.assertIn("other **11**", text)
        self.assertIn("**89**", text)
        self.assertIn("**749**", text)


if __name__ == "__main__":
    unittest.main()
