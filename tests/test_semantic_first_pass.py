import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SemanticFirstPassTests(unittest.TestCase):
    def setUp(self):
        self.reg = json.loads((ROOT / "governance/coverage/dtg-semantic-first-pass.json").read_text(encoding="utf-8"))
        self.trees = json.loads((ROOT / "governance/coverage/pinned-dtg-spec-term-trees.json").read_text(encoding="utf-8"))
        self.repositories = {x["repository"]: x for x in self.trees["repositories"]}

    def test_all_17_source_scoped_reviews_have_pinned_provenance(self):
        self.assertEqual(len(self.reg["records"]), 17)
        seen = set()
        for row in self.reg["records"]:
            repo = self.repositories[row["source_repository"]]
            self.assertEqual(row["source_commit"], repo["commit_sha"])
            self.assertIn(row["source_path"], {x["path"] for x in repo["term_files"]})
            key = (row["source_repository"], row["source_path"], row["source_label"].casefold())
            self.assertNotIn(key, seen)
            seen.add(key)

    def test_preliminary_review_does_not_invent_semantic_approval(self):
        allowed = {"material_divergence", "contextual_narrowing", "candidate_scope_overlap", "ambiguous_mapping"}
        self.assertTrue(self.reg["approval_required"])
        for row in self.reg["records"]:
            self.assertIn(row["preliminary_class"], allowed)
            self.assertEqual(row["decision_state"], "requires_semantic_approval")
            self.assertIsNone(row["mapping_assertion"])
            self.assertTrue(row["rationale"].strip())
            for cid in row["tig_lexical_candidates"]:
                self.assertTrue(cid.startswith("urn:tig:concept:"))


if __name__ == "__main__":
    unittest.main()
