import subprocess
import tempfile
import unittest
from pathlib import Path
from sys import path as sys_path

sys_path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from extract_external_glossary_definitions import extract_checked_out_tree, TreeAdmissionError


class PinnedExtractionTests(unittest.TestCase):
    def test_end_to_end_local_git_revision_and_aliases(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "tests@example.invalid"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
            termdir = root / "spec/terms-definitions"
            termdir.mkdir(parents=True)
            (termdir / "sample.md").write_text("[[def: stable concept, alternative name]]\n~ A source-defined concept.\n")
            (termdir / "unmarked.md").write_text("A file with no explicit definition.\n")
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-qm", "source fixture"], check=True)
            commit = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
            result = extract_checked_out_tree(root, "trustoverip/test-glossary", commit)
            self.assertEqual(result["file_count"], 2)
            self.assertEqual(result["explicit_definition_count"], 1)
            self.assertEqual(result["terms"][0]["label"], "stable concept")
            self.assertEqual(result["terms"][0]["aliases"], ["alternative name"])
            self.assertEqual(result["terms"][0]["adjudication"], "unreviewed")
            self.assertIsNone(result["terms"][0]["tig_mapping"])
            self.assertEqual(result["files_without_explicit_markers"],
                             ["spec/terms-definitions/unmarked.md"])
            with self.assertRaisesRegex(TreeAdmissionError, "revision drift"):
                extract_checked_out_tree(root, "trustoverip/test-glossary", "0" * 40)

    def test_empty_source_directory_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "tests@example.invalid"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
            (root / "README.md").write_text("test\n")
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-qm", "empty fixture"], check=True)
            commit = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
            with self.assertRaisesRegex(TreeAdmissionError, "no tracked terminology"):
                extract_checked_out_tree(root, "trustoverip/test-glossary", commit)


if __name__ == "__main__":
    unittest.main()
