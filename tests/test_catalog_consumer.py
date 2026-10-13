import copy
import json
import unittest
from pathlib import Path
from sys import path as sys_path
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys_path.insert(0, str(ROOT / "tools"))
from qualify_catalog_consumer import qualify, ConsumerError


class CatalogConsumerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / "generated/json/trust-infrastructure-glossary.catalog.json").read_text())
        cls.term = yaml.safe_load((ROOT / "glossary/terms/trust-task.yaml").read_text())
        cls.decisions = json.loads((ROOT / "governance/coverage/dtg-semantic-decision-proposals.json").read_text())

    def run_consumer(self, mutate=None):
        inputs = copy.deepcopy((self.catalog, self.term, self.decisions))
        if mutate:
            mutate(inputs)
        return qualify(*inputs)

    def test_resolves_a_real_exported_concept_and_rejects_ambiguous_source_match(self):
        actual = self.run_consumer()
        self.assertEqual(actual["concept_id"], "urn:tig:concept:trust-task")
        self.assertTrue(actual["designations_verified"])
        self.assertTrue(actual["provenance_verified"])
        self.assertGreater(actual["pending_source_matches_rejected"], 0)
        self.assertFalse(actual["independent_implementation"])

    def test_rejects_missing_concept(self):
        with self.assertRaises(ConsumerError):
            self.run_consumer(lambda x: x[1].update({"concept_id": "urn:tig:concept:missing"}))

    def test_rejects_catalog_count_drift(self):
        with self.assertRaises(ConsumerError):
            self.run_consumer(lambda x: x[0].update({"concept_count": -1}))

    def test_rejects_designation_drift(self):
        with self.assertRaises(ConsumerError):
            self.run_consumer(lambda x: x[1].update({"designations": []}))

    def test_rejects_premature_mutation(self):
        with self.assertRaises(ConsumerError):
            self.run_consumer(lambda x: x[2]["cases"][1].update({"canonical_change_allowed": True}))


if __name__ == "__main__":
    unittest.main()
