import copy
import json
import tempfile
import unittest
from pathlib import Path
from sys import path as sys_path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys_path.insert(0, str(ROOT / "tools"))
from report_concept_semantic_changes import SnapshotError, compare, read_concepts


def term(cid="alpha"):
    return {
        "concept_id": f"urn:tig:concept:{cid}",
        "definition": "An original meaning.",
        "term": cid,
        "aliases": [],
        "designations": [{"label": cid, "language": "en", "status": "preferred"}],
        "editorial": {"status": "stable", "reviewed": {"domain": True}},
        "provenance": {"classification": "locally_defined", "source_corpus": "TIG"},
        "concept_mappings": {"exact": []},
        "semantic_relations": {"related": []},
    }


class ConceptHistoryTests(unittest.TestCase):
    def setUp(self):
        self.old = {"urn:tig:concept:alpha": term()}

    def diff(self, newer):
        return compare(self.old, newer, "v2.2.0", "candidate")["changes"]

    def test_unchanged_snapshot_is_empty_and_deterministic(self):
        first = compare(self.old, copy.deepcopy(self.old), "v2.2.0", "candidate")
        second = compare(self.old, copy.deepcopy(self.old), "v2.2.0", "candidate")
        self.assertEqual(first["changes"], [])
        self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))

    def test_label_only_change_preserves_concept_identity(self):
        updated = copy.deepcopy(self.old)
        updated["urn:tig:concept:alpha"]["designations"][0]["label"] = "renamed"
        changes = self.diff(updated)
        self.assertEqual(changes[0]["concept_id"], "urn:tig:concept:alpha")
        self.assertEqual(changes[0]["change_classes"], ["designation_changed"])

    def test_material_definition_change_requires_review(self):
        updated = copy.deepcopy(self.old)
        updated["urn:tig:concept:alpha"]["definition"] = "An entirely different meaning."
        changes = self.diff(updated)
        self.assertEqual(changes[0]["change_classes"], ["semantic_review_required"])
        self.assertEqual(changes[0]["semantic_approval"], "not_assessed")

    def test_deleted_id_is_not_silent(self):
        changes = self.diff({"urn:tig:concept:beta": term("beta")})
        self.assertEqual([r["change_classes"] for r in changes],
                         [["concept_missing_from_target"], ["new_concept"]])

    def test_deprecation_and_successor_remain_distinct(self):
        updated = copy.deepcopy(self.old)
        updated["urn:tig:concept:alpha"]["editorial"]["status"] = "deprecated"
        updated["urn:tig:concept:beta"] = term("beta")
        changes = self.diff(updated)
        self.assertEqual(changes[0]["change_classes"], ["editorial_status_changed"])
        self.assertEqual(changes[1]["change_classes"], ["new_concept"])

    def test_missing_and_duplicate_inputs_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            with self.assertRaises(SnapshotError):
                read_concepts(directory)
            (directory / "one.yaml").write_text(yaml.safe_dump(term()))
            (directory / "two.yaml").write_text(yaml.safe_dump(term()))
            with self.assertRaisesRegex(SnapshotError, "duplicate concept_id"):
                read_concepts(directory)
        with self.assertRaises(SnapshotError):
            compare(self.old, self.old, "", "candidate")

    def test_nonsemantic_metadata_change_is_not_silently_unchanged(self):
        updated = copy.deepcopy(self.old)
        updated["urn:tig:concept:alpha"]["aliases"] = ["alias"]
        self.assertEqual(self.diff(updated)[0]["change_classes"], ["other_metadata_review_required"])


if __name__ == "__main__":
    unittest.main()
