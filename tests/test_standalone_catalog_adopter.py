"""Acceptance and failure-mode tests for the dependency-free adopter prototype."""
import copy
import json
import unittest
from pathlib import Path
from sys import path as sys_path

ROOT = Path(__file__).resolve().parents[1]
sys_path.insert(0, str(ROOT / "examples/consumers/standalone"))
from catalog_adopter import AdopterError, validate


class StandaloneAdopterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / "generated/json/trust-infrastructure-glossary.catalog.json").read_text())
        cls.decisions = json.loads((ROOT / "governance/coverage/dtg-semantic-decision-proposals.json").read_text())

    def test_current_published_catalog_resolution_with_negative_match(self):
        r = validate(self.catalog, self.decisions, "urn:tig:concept:trust-task")
        self.assertTrue(r["concept_resolved"])
        self.assertGreater(r["ambiguous_matches_rejected"], 0)
        self.assertFalse(r["independently_maintained"])
        self.assertFalse(r["semantic_equivalence_verified"])

    def test_unknown_id_is_rejected(self):
        with self.assertRaises(AdopterError):
            validate(self.catalog, self.decisions, "urn:tig:concept:nonexistent")

    def test_duplicate_id_is_rejected(self):
        catalog = copy.deepcopy(self.catalog)
        catalog["concepts"].append(catalog["concepts"][0])
        catalog["concept_count"] += 1
        with self.assertRaises(AdopterError):
            validate(catalog, self.decisions, "urn:tig:concept:trust-task")

    def test_unapproved_semantic_mutation_is_rejected(self):
        decisions = copy.deepcopy(self.decisions)
        for case in decisions["cases"]:
            if "urn:tig:concept:trust-task" in case.get("tig_concepts", []):
                case["canonical_change_allowed"] = True
        with self.assertRaises(AdopterError):
            validate(self.catalog, decisions, "urn:tig:concept:trust-task")

    def test_absent_disputed_case_is_rejected(self):
        with self.assertRaises(AdopterError):
            validate(self.catalog, {"cases": []}, "urn:tig:concept:trust-task")


if __name__ == "__main__":
    unittest.main()
