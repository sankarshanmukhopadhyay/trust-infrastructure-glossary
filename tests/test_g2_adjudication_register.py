import copy
import json
import unittest
from pathlib import Path
from sys import path as sys_path

ROOT = Path(__file__).resolve().parents[1]
sys_path.insert(0, str(ROOT / "tools"))
from validate_g2_adjudications import compile_register, validate_approval

class G2DecisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.first = json.loads((ROOT / "governance/coverage/dtg-semantic-first-pass.json").read_text())
        cls.proposals = json.loads((ROOT / "governance/coverage/dtg-semantic-decision-proposals.json").read_text())
        cls.register = json.loads((ROOT / "governance/coverage/dtg-g2-adjudications.json").read_text())

    def test_complete_pending_register(self):
        expected = compile_register(self.first, self.proposals)
        self.assertEqual(expected, self.register)
        self.assertEqual(validate_approval(self.register), 0)
        self.assertEqual(self.register["high_risk_count"], 6)

    def test_pending_disposition_cannot_be_faked(self):
        data = copy.deepcopy(self.register)
        data["source_rows"][0]["decision"]["disposition"] = "covered"
        with self.assertRaisesRegex(ValueError, "pending semantic decision"):
            validate_approval(data)

    def test_approval_requires_human_evidence(self):
        data = copy.deepcopy(self.register)
        data["source_rows"][0]["decision"]["approval_state"] = "approved"
        data["source_rows"][0]["decision"]["disposition"] = "covered"
        data["approved_count"] = 1
        data["review_required_count"] = 16
        with self.assertRaisesRegex(ValueError, "missing human"):
            validate_approval(data)

    def test_no_exact_mapping_on_partial_disposition(self):
        data = copy.deepcopy(self.register)
        d = data["source_rows"][0]["decision"]
        d.update({"approval_state": "approved", "disposition": "partial",
                  "mapping_strength": "exact", "rationale": "reviewed",
                  "source_definition_evidence": "sha/path",
                  "reviewer": "reviewer", "reviewed_at": "2026-10-13",
                  "compatibility_assessment": "reviewed",
                  "source_license_review": "reviewed"})
        data["approved_count"] = 1
        data["review_required_count"] = 16
        with self.assertRaisesRegex(ValueError, "exact mapping"):
            validate_approval(data)

    def test_unfinished_register_cannot_claim_complete_coverage(self):
        data = copy.deepcopy(self.register)
        data["semantic_coverage"] = 1.0
        with self.assertRaisesRegex(ValueError, "complete semantic coverage"):
            validate_approval(data)

if __name__ == "__main__":
    unittest.main()
