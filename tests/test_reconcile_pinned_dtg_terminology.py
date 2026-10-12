import sys
import tempfile
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from reconcile_pinned_dtg_terminology import crosswalk


class PinnedCrosswalkTests(unittest.TestCase):
    def test_alias_match_is_candidate_not_semantic_coverage(self):
        with tempfile.TemporaryDirectory() as d:
            terms = Path(d)
            (terms / "one.yaml").write_text(yaml.safe_dump({
                "concept_id": "urn:tig:concept:membership",
                "term": "membership",
                "designations": [{"label": "verifiable membership credential"}],
            }), encoding="utf-8")
            inventory = {
                "scope": "fixture",
                "repositories": [{
                    "repository": "trustoverip/fixture",
                    "commit_sha": "a" * 40,
                    "definitions": [{
                        "label": "VMC",
                        "aliases": ["verifiable membership credential"],
                        "source_path": "spec/terms-definitions/vmc.md",
                        "source_sha256": "b" * 64,
                    }, {
                        "label": "VAC",
                        "aliases": [],
                        "source_path": "spec/terms-definitions/vac.md",
                        "source_sha256": "c" * 64,
                    }]
                }],
            }
            result = crosswalk(inventory, terms)
            self.assertEqual(result["source_definition_denominator"], 2)
            self.assertEqual(result["source_definitions_with_lexical_candidates"], 1)
            self.assertIsNone(result["semantic_coverage_percentage"])
            rows = {row["source_label"]: row for row in result["crosswalk"]}
            self.assertEqual(rows["VMC"]["lexical_candidates"], ["urn:tig:concept:membership"])
            self.assertEqual(rows["VAC"]["lexical_status"], "no_match_detected")
            self.assertTrue(all(row["semantic_status"] == "review_required" for row in rows.values()))
            self.assertTrue(all(row["mapping_assertion"] is None for row in rows.values()))


if __name__ == "__main__":
    unittest.main()
