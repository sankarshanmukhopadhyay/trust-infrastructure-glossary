import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from validate_source_crosswalk import validate

PILOT = json.loads((Path(__file__).resolve().parents[1] / "governance/coverage/dtg-vtc-pilot.json").read_text())
IDS = {"urn:tig:concept:trust-task", "urn:tig:concept:trust-registry"}


class SourceCrosswalkTests(unittest.TestCase):
    def test_credential_taxonomy_has_seven_unadjudicated_types(self):
        rows = [row for row in PILOT["candidates"] if row["source_id"] == "dtg-credential-taxonomy"]
        self.assertEqual({row["label"] for row in rows}, {
            "MembershipCredential", "RelationshipCredential", "DelegationCredential",
            "InvitationCredential", "PersonaCredential", "StatementCredential",
            "AuthorityCredential",
        })
        self.assertTrue(all(row["disposition"] == "unresolved" and row["concept_id"] is None for row in rows))

    def test_valid_candidate_corpus(self):
        self.assertEqual(validate(PILOT, IDS), [])

    def test_unknown_concept_is_rejected(self):
        data = copy.deepcopy(PILOT)
        data["candidates"][0]["concept_id"] = "urn:tig:concept:not-real"
        self.assertTrue(any("unknown concept_id" in error for error in validate(data, IDS)))

    def test_unknown_source_is_rejected(self):
        data = copy.deepcopy(PILOT)
        data["candidates"][0]["source_id"] = "unknown"
        self.assertTrue(any("unknown source_id" in error for error in validate(data, IDS)))

    def test_unreviewed_claim_cannot_be_covered(self):
        data = copy.deepcopy(PILOT)
        data["candidates"][0]["disposition"] = "covered"
        self.assertTrue(any("requires adjudication" in error or "cannot claim coverage" in error for error in validate(data, IDS)))

    def test_duplicate_source_label_rejected(self):
        data = copy.deepcopy(PILOT)
        data["candidates"].append(copy.deepcopy(data["candidates"][0]))
        self.assertTrue(any("duplicate source/label" in error for error in validate(data, IDS)))

    def test_invalid_canonical_revision_rejected(self):
        data = copy.deepcopy(PILOT)
        data["sources"][1]["canonical_commit"] = "bad-revision"
        self.assertTrue(any("invalid canonical commit SHA" in error for error in validate(data, IDS)))

    def test_malformed_sha_rejected(self):
        data = copy.deepcopy(PILOT)
        data["sources"][0]["blob_sha"] = "not-a-sha"
        self.assertTrue(any("invalid file blob SHA" in error for error in validate(data, IDS)))


if __name__ == "__main__":
    unittest.main()
