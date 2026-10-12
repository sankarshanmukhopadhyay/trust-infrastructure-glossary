#!/usr/bin/env python3
"""Build an auditable, explicitly unresolved source-scoped assurance ledger.

This never converts lexical similarity into approved semantic coverage.
"""
import argparse
import json
from collections import Counter
from pathlib import Path

CLASSIFICATIONS = {"review_required", "covered", "partial", "missing", "not_applicable", "insufficient_evidence"}


def build(crosswalk, first_pass, proposals):
    reviewed = {(r["source_repository"], r["source_path"]): r for r in first_pass["records"]}
    decisions = {(r["source_repository"], r["source_path"]): r for r in proposals["cases"]}
    rows = []
    for source in crosswalk["crosswalk"]:
        key = (source["source_repository"], source["source_path"])
        review = reviewed.get(key)
        proposal = decisions.get(key)
        row = {
            "source_repository": source["source_repository"],
            "source_commit": source["source_commit"],
            "source_path": source["source_path"],
            "source_sha256": source["source_sha256"],
            "source_label": source["source_label"],
            "source_aliases": source.get("source_aliases", []),
            "lexical_candidates": source.get("lexical_candidates", []),
            "disposition": "review_required",
            "semantic_mapping": None,
            "approval_evidence": None,
            "review_class": review["preliminary_class"] if review else None,
            "review_rationale": review["rationale"] if review else "Source definition requires comparison with TIG, including alternative terms and domain scoping.",
            "decision_proposal": proposal["case_id"] if proposal else None,
            "canonical_change_authorized": False,
        }
        rows.append(row)
    identifiers = [(x["source_repository"], x["source_path"]) for x in rows]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("duplicate source-definition file identities")
    if len(rows) != crosswalk["source_definition_denominator"]:
        raise ValueError("source inventory count mismatch")
    if len(reviewed) != 17 or len(decisions) != 6:
        raise ValueError("review evidence differs from pinned baseline")
    if not set(reviewed).issubset(identifiers) or not set(decisions).issubset(identifiers):
        raise ValueError("orphan first-pass findings or decision proposals")
    return {
        "schema_version": "1.0",
        "scope": crosswalk["scope"],
        "source_definition_count": len(rows),
        "lexical_candidate_count": sum(bool(x["lexical_candidates"]) for x in rows),
        "initial_semantic_comparison_count": len(reviewed),
        "pending_decision_proposals": len(decisions),
        "approved_semantic_mappings": 0,
        "semantic_coverage_percentage": None,
        "completion_gate": "blocked_pending_source_adjudication",
        "disposition_counts": dict(Counter(x["disposition"] for x in rows)),
        "records": rows,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--crosswalk", type=Path, required=True)
    parser.add_argument("--first-pass", type=Path, required=True)
    parser.add_argument("--proposals", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build(
        json.loads(args.crosswalk.read_text(encoding="utf-8")),
        json.loads(args.first_pass.read_text(encoding="utf-8")),
        json.loads(args.proposals.read_text(encoding="utf-8")),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Assurance ledger: {result['source_definition_count']} source definitions; {result['initial_semantic_comparison_count']} first-pass comparisons; {result['approved_semantic_mappings']} approved")


if __name__ == "__main__":
    main()
