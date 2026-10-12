import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from extract_spec_up_t_terms import extract

COMMIT = "a" * 40


class ExtractSourceTermsTests(unittest.TestCase):
    def test_explicit_terms_only_and_deterministic(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            directory = root / "spec" / "terms-definitions"
            directory.mkdir(parents=True)
            (directory / "b.md").write_text("See [[ref: Not a definition]].\n[[def: Trust Task]]\n")
            (directory / "a.md").write_text("[[def: VAC, authority credential, VACs]]\n[[def: Delegation Credential]]\n")
            result = extract(root, "trustoverip/example-spec", COMMIT)
            self.assertEqual([x["label"] for x in result], [
                "VAC", "Delegation Credential", "Trust Task",
            ])
            self.assertEqual(result[0]["aliases"], ["authority credential", "VACs"])
            self.assertTrue(all(x["semantic_equivalence"] == "not_established" for x in result))
            self.assertEqual(result, extract(root, "trustoverip/example-spec", COMMIT))

    def test_missing_directory_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaisesRegex(ValueError, "missing"):
                extract(Path(td), "trustoverip/example-spec", COMMIT)

    def test_bad_commit_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaisesRegex(ValueError, "commit"):
                extract(Path(td), "trustoverip/example-spec", "main")


if __name__ == "__main__":
    unittest.main()
