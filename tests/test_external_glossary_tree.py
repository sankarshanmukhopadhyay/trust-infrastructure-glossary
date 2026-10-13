"""Unit and negative tests for complete Git-tree admission from a pinned commit."""
import json
import tempfile
import unittest
from pathlib import Path
from sys import path as sys_path

sys_path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from inventory_external_glossary_tree import TreeAdmissionError, inventory, write_report

COMMIT = "a" * 40
BLOB = "b" * 40
TREE = {
    "sha": "c" * 40,
    "truncated": False,
    "tree": [
        {"path": "spec/terms-definitions/zeta.md", "type": "blob", "sha": BLOB},
        {"path": "spec/terms-definitions/alpha.md", "type": "blob", "sha": BLOB},
        {"path": "README.md", "type": "blob", "sha": BLOB},
        {"path": "spec/terms-definitions/archive", "type": "tree", "sha": BLOB},
    ],
}


def fetch_response(payload):
    def fetch(url, token):
        if url != f"https://api.github.com/repos/trustoverip/ctwg-main-glossary/git/trees/{COMMIT}?recursive=1":
            raise AssertionError(f"unexpected URL: {url}")
        return payload
    return fetch


class ExternalGlossaryInventoryTests(unittest.TestCase):
    def test_complete_sorted_inventory_with_no_transclusion_assertion(self):
        record = inventory("trustoverip/ctwg-main-glossary", COMMIT, fetch_response(TREE))
        self.assertEqual(record["term_file_count"], 2)
        self.assertEqual([row["path"] for row in record["term_files"]],
                         ["spec/terms-definitions/alpha.md", "spec/terms-definitions/zeta.md"])
        self.assertFalse(record["rendered_spec_transclusion_revision_verified"])
        self.assertIsNone(record["semantic_coverage"])
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "evidence.json"
            digest = write_report(record, output)
            self.assertEqual(len(digest), 64)
            self.assertEqual(json.loads(output.read_text()), record)

    def test_truncated_trees_fail_closed(self):
        with self.assertRaisesRegex(TreeAdmissionError, "truncated"):
            inventory("trustoverip/ctwg-main-glossary", COMMIT,
                      fetch_response({**TREE, "truncated": True}))

    def test_missing_tree_fails_closed(self):
        with self.assertRaises(TreeAdmissionError):
            inventory("trustoverip/ctwg-main-glossary", COMMIT,
                      fetch_response({"truncated": False}))

    def test_invalid_or_missing_blob_fails_closed(self):
        malformed = {**TREE, "tree": [{"path": "spec/terms-definitions/alpha.md",
                                       "type": "blob", "sha": "not-a-blob-sha"}]}
        with self.assertRaisesRegex(TreeAdmissionError, "invalid source term blob"):
            inventory("trustoverip/ctwg-main-glossary", COMMIT, fetch_response(malformed))

    def test_duplicate_paths_fail_closed(self):
        malformed = {**TREE, "tree": [TREE["tree"][0], TREE["tree"][0]]}
        with self.assertRaisesRegex(TreeAdmissionError, "duplicate path"):
            inventory("trustoverip/ctwg-main-glossary", COMMIT, fetch_response(malformed))

    def test_empty_directory_fails_closed(self):
        with self.assertRaisesRegex(TreeAdmissionError, "no explicit terminology"):
            inventory("trustoverip/ctwg-main-glossary", COMMIT,
                      fetch_response({"truncated": False, "tree": []}))

    def test_invalid_commit_or_repository_fails_closed(self):
        with self.assertRaises(TreeAdmissionError):
            inventory("trustoverip/ctwg-main-glossary", "main", fetch_response(TREE))
        with self.assertRaises(TreeAdmissionError):
            inventory("../exfiltrate", COMMIT, fetch_response(TREE))


if __name__ == "__main__":
    unittest.main()
