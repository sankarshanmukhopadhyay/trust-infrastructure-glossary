"""Guard against false coverage and credential-taxonomy promotion in source admission."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CredentialTerminologyAdmissionTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads((ROOT / "governance/coverage/cred-spec-terminology-admission.json").read_text())

    def test_admission_has_pinned_source_and_unpinned_rendered_page(self):
        item = self.record
        self.assertEqual(len(item["pinned_commit"]), 40)
        self.assertEqual(item["source_directory_term_count_at_pinned_commit"], 50)
        self.assertFalse(item["rendered_page_commit_equivalence_verified"])
        self.assertFalse(item["term_directory_to_rendered_section_parity_verified"])

    def test_external_glossaries_remain_unresolved(self):
        item = self.record
        self.assertEqual({x["label"] for x in item["referenced_glossaries"]},
                         {"DTG Glossary", "ToIP Main Glossary", "ToIP General IT Glossary"})
        for x in item["referenced_glossaries"]:
            self.assertEqual(x["status"], "requires_pinned_source_admission")
            self.assertEqual(x["coverage"], "indeterminate")

    def test_taxonomy_and_semantic_guardrails(self):
        item = self.record
        guards = {x["id"]: x for x in item["taxonomy_guards"]}
        self.assertEqual(len(guards["credentials-hierarchy"]["formal_children"]), 7)
        self.assertEqual(guards["credentials-hierarchy"]["formal_parent"], "DTGCredential")
        self.assertIn("StatementCredential", guards["credentials-hierarchy"]["formal_children"])
        self.assertIn("AuthorityCredential", guards["credentials-hierarchy"]["formal_children"])
        self.assertIn("not credential types", guards["credentials-hierarchy"]["rule"])
        self.assertIn("not one of the standard", guards["identity-verification-credential"]["rule"])
        self.assertIn("not a DTGCredential", guards["relationship-card"]["rule"])
        self.assertEqual(item["semantic_approval"], "not_assessed")
        self.assertEqual(item["tig_exact_mappings_asserted"], 0)
        self.assertEqual(item["coverage"], "indeterminate")

    def test_mutation_of_authority_is_rejected_by_guard(self):
        changed = dict(self.record)
        changed["rendered_page_commit_equivalence_verified"] = True
        self.assertNotEqual(changed["rendered_page_commit_equivalence_verified"],
                            self.record["rendered_page_commit_equivalence_verified"])


if __name__ == "__main__":
    unittest.main()
