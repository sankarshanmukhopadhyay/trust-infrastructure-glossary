"""Cross-file source intake invariants and negative mutation tests."""
import copy
import json
import unittest
from pathlib import Path
from sys import path as sys_path

ROOT = Path(__file__).resolve().parents[1]
sys_path.insert(0, str(ROOT / "tools"))
from report_dtg_intake_readiness import IntakeError, load, produce, TREE, PASS, DECISIONS, CRED


class SourceReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs = [load(p) for p in (TREE, PASS, DECISIONS, CRED)]

    def run_report(self, mutations=None):
        values = copy.deepcopy(self.inputs)
        if mutations:
            mutations(values)
        return produce(*values)

    def test_pinned_counts_and_uncertainty(self):
        result = self.run_report()
        self.assertEqual(result["pinned_directory_definition_count"], 106)
        self.assertEqual(result["first_pass_lexical_candidate_count"], 17)
        self.assertEqual(result["without_first_pass_lexical_candidate_count"], 89)
        self.assertIsNone(result["metrics"]["semantic_coverage"])
        self.assertFalse(result["automated_semantic_approval"])

    def test_rejects_unpinned_tree(self):
        with self.assertRaises(IntakeError):
            self.run_report(lambda v: v[0]["repositories"][0].update({"tree_truncated": True}))

    def test_rejects_candidate_promotion_without_approval(self):
        with self.assertRaisesRegex(IntakeError, "premature semantic mapping"):
            self.run_report(lambda v: v[1]["records"][0].update({"mapping_assertion": "exact"}))

    def test_rejects_orphan_candidate(self):
        with self.assertRaisesRegex(IntakeError, "orphan"):
            self.run_report(lambda v: v[1]["records"][0].update({"source_path": "spec/terms-definitions/never-existed.md"}))

    def test_rejects_pending_canonical_mutation(self):
        with self.assertRaisesRegex(IntakeError, "permits mutation"):
            self.run_report(lambda v: v[2]["cases"][0].update({"canonical_change_allowed": True}))

    def test_rejects_unverifiable_blob(self):
        with self.assertRaisesRegex(IntakeError, "unverifiable"):
            self.run_report(lambda v: v[0]["repositories"][0]["term_files"][0].update({"blob_sha": "short"}))

    def test_rejects_mismatched_credential_count(self):
        with self.assertRaisesRegex(IntakeError, "count inconsistent"):
            self.run_report(lambda v: v[3].update({"source_directory_term_count_at_pinned_commit": 51}))


if __name__ == "__main__":
    unittest.main()
