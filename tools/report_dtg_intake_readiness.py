#!/usr/bin/env python3
"""Compute an evidence-conservative DTG intake/semantic-readiness report.

Counts are source-directory inventory and first-pass lexical candidate counts,
NOT semantic coverage. Upstream external glossary admission is tracked separately.
"""
import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TREE = ROOT / "governance/coverage/pinned-dtg-spec-term-trees.json"
PASS = ROOT / "governance/coverage/dtg-semantic-first-pass.json"
DECISIONS = ROOT / "governance/coverage/dtg-semantic-decision-proposals.json"
CRED = ROOT / "governance/coverage/cred-spec-terminology-admission.json"


class IntakeError(ValueError):
    pass


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def produce(trees, first_pass, proposals, cred):
    source_rows = {}
    per_repo = {}
    for repository in trees["repositories"]:
        name = repository["repository"]
        commit = repository["commit_sha"]
        if len(commit) != 40 or repository.get("tree_truncated"):
            raise IntakeError(f"source revision not fully pinned: {name}")
        if name in per_repo:
            raise IntakeError(f"duplicate source repository: {name}")
        paths = repository["term_files"]
        per_repo[name] = len(paths)
        for row in paths:
            key = (name, commit, row["path"])
            if key in source_rows:
                raise IntakeError(f"duplicate source row: {key}")
            if not row["path"].startswith("spec/terms-definitions/") or len(row["blob_sha"]) != 40:
                raise IntakeError(f"unverifiable term file: {key}")
            source_rows[key] = row
    matched = set()
    for row in first_pass["records"]:
        key = (row["source_repository"], row["source_commit"], row["source_path"])
        if key not in source_rows or key in matched:
            raise IntakeError(f"orphan or duplicate semantic candidate: {key}")
        if row.get("decision_state") != "requires_semantic_approval" or row.get("mapping_assertion") is not None:
            raise IntakeError(f"premature semantic mapping: {key}")
        matched.add(key)
    cases = proposals["cases"]
    if len({case["case_id"] for case in cases}) != len(cases):
        raise IntakeError("duplicate semantic decision case")
    for case in cases:
        key = (case["source_repository"], case["source_commit"], case["source_path"])
        if key not in matched:
            raise IntakeError(f"decision proposal has no first-pass evidence: {key}")
        if case.get("approval") == "pending" and case.get("canonical_change_allowed") is not False:
            raise IntakeError(f"pending proposal permits mutation: {case['case_id']}")
    if cred["pinned_commit"] != next(
        (repo["commit_sha"] for repo in trees["repositories"] if repo["repository"] == cred["source_repository"]), None
    ):
        raise IntakeError("rendered Credentials spec pin inconsistent with source tree")
    if cred["source_directory_term_count_at_pinned_commit"] != per_repo[cred["source_repository"]]:
        raise IntakeError("rendered Credentials spec count inconsistent with source tree")
    unresolved = [g["label"] for g in cred["referenced_glossaries"]
                  if g.get("status") == "requires_pinned_source_admission"]
    if not unresolved and not cred["rendered_page_commit_equivalence_verified"]:
        raise IntakeError("external sources appear admitted while rendered build is not pinned")
    return {
        "schema_version": "1.0",
        "source_directory_counts": dict(sorted(per_repo.items())),
        "pinned_directory_definition_count": len(source_rows),
        "first_pass_lexical_candidate_count": len(matched),
        "without_first_pass_lexical_candidate_count": len(source_rows) - len(matched),
        "high_risk_proposals": len(cases),
        "unresolved_referenced_glossaries": unresolved,
        "rendered_page_commit_equivalence_verified": cred["rendered_page_commit_equivalence_verified"],
        "metrics": {
            "lexical_candidate_fraction_in_pinned_directory": {
                "numerator": len(matched), "denominator": len(source_rows),
                "meaning": "first-pass candidate discovery only, not terminology or semantic coverage"
            },
            "semantic_coverage": None,
            "provenance_coverage": None,
            "relationship_coverage": None
        },
        "gate_g0": "partial" if unresolved or not cred["rendered_page_commit_equivalence_verified"] else "requires_external_verification",
        "gate_g1": "partial",
        "gate_g2": "pending_review",
        "automated_semantic_approval": False
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = produce(load(TREE), load(PASS), load(DECISIONS), load(CRED))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{report['pinned_directory_definition_count']} pinned definitions, "
          f"{report['first_pass_lexical_candidate_count']} lexical candidates; semantic coverage unknown")


if __name__ == "__main__":
    main()
