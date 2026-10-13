import copy
import unittest
from pathlib import Path
from sys import path as sys_path
sys_path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from build_external_glossary_crosswalk import build, normalized, CrosswalkError


def fixture():
    catalog = {"concept_count": 2, "concepts": [
        {"concept_id": "urn:tig:concept:proof", "designations": [{"label": "Proof"}]},
        {"concept_id": "urn:tig:concept:other", "designations": [{"label": "Proof"}, {"label": "Trust context"}]},
    ]}
    report = {"source_repository": "trustoverip/external", "source_commit": "a"*40,
              "explicit_definition_count": 2, "terms": [
                  {"source_repo": "trustoverip/external", "source_commit": "a"*40,
                   "source_path": "spec/terms-definitions/proof.md", "definition_occurrence": 1,
                   "source_blob_sha": "b"*40, "label": "proof", "aliases": []},
                  {"source_repo": "trustoverip/external", "source_commit": "a"*40,
                   "source_path": "spec/terms-definitions/unknown.md", "definition_occurrence": 1,
                   "source_blob_sha": "c"*40, "label": "unknown meaning", "aliases": []},
              ]}
    return catalog, [report]


class CrosswalkTests(unittest.TestCase):
    def test_every_source_row_is_preserved_with_ambiguity(self):
        result = build(*fixture())
        self.assertEqual(result["source_definition_count"], 2)
        self.assertEqual(result["lexical_candidate_source_rows"], 1)
        self.assertEqual(result["no_lexical_candidate_source_rows"], 1)
        self.assertEqual(result["source_definition_rows"][0]["candidate_class"], "ambiguous")
        self.assertEqual(len(result["source_definition_rows"][0]["tig_lexical_candidates"]), 2)
        self.assertTrue(all(row["mapping_assertion"] is None for row in result["source_definition_rows"]))
        self.assertIsNone(result["semantic_coverage"])

    def test_unicode_and_alias_normalization(self):
        self.assertEqual(normalized("  Verifiable-Credential  "), normalized("verifiable credential"))
        cat, sources = fixture()
        sources[0]["terms"][1]["aliases"] = ["TRUST CONTEXT"]
        result = build(cat, sources)
        self.assertEqual(result["lexical_candidate_source_rows"], 2)

    def test_rejects_incomplete_source_inventory(self):
        cat, sources = fixture()
        sources[0]["explicit_definition_count"] = 3
        with self.assertRaises(CrosswalkError):
            build(cat, sources)

    def test_rejects_duplicate_source_rows(self):
        cat, sources = fixture()
        sources[0]["terms"].append(copy.deepcopy(sources[0]["terms"][0]))
        sources[0]["explicit_definition_count"] = 3
        with self.assertRaises(CrosswalkError):
            build(cat, sources)

    def test_rejects_catalog_ambiguity_in_identity(self):
        cat, sources = fixture()
        cat["concepts"][1]["concept_id"] = cat["concepts"][0]["concept_id"]
        with self.assertRaises(CrosswalkError):
            build(cat, sources)

    def test_rejects_source_identity_drift(self):
        cat, sources = fixture()
        sources[0]["terms"][0]["source_commit"] = "0"*40
        with self.assertRaises(CrosswalkError):
            build(cat, sources)


if __name__ == "__main__":
    unittest.main()
