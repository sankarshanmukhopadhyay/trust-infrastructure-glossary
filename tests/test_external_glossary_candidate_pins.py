"""Validate pinned candidate ToIP glossary sources without pretending deployed transclusion."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "governance/coverage/toip-external-glossary-candidate-pins.json"


class ExternalPinsTests(unittest.TestCase):
    def test_candidate_pins_have_complete_hashes_and_unresolved_parity(self):
        data = json.loads(DATA.read_text(encoding="utf-8"))
        records = data["external_glossary_candidates"]
        self.assertEqual(len(records), 2)
        self.assertEqual({item["repository"] for item in records}, {
            "trustoverip/ctwg-main-glossary", "trustoverip/ctwg-general-glossary"
        })
        for item in records:
            self.assertEqual(len(item["pinned_candidate_commit"]), 40)
            self.assertEqual(len(item["verified_example"]["blob_sha"]), 40)
            self.assertTrue(item["source_file_at_revision_verified"])
            self.assertFalse(item["complete_tree_verified"])
            self.assertFalse(item["transclusion_revision_verified"])
            self.assertEqual(item["admission_status"], "candidate_requires_tree_and_transclusion_audit")
        self.assertIsNone(data["source_glossary_coverage"])
        self.assertFalse(data["source_normative_equivalence_approved"])
        self.assertIsNone(data["dtg_glossary"]["verified_immutable_source"])

    def test_no_candidate_is_reported_as_complete(self):
        data = json.loads(DATA.read_text(encoding="utf-8"))
        self.assertFalse(any(item["complete_tree_verified"] and item["transclusion_revision_verified"]
                             for item in data["external_glossary_candidates"]))


if __name__ == "__main__":
    unittest.main()
