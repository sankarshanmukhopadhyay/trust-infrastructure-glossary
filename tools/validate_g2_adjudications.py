#!/usr/bin/env python3
"""Construct the complete initial G2 decision register; never infer approval."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIRST = ROOT / "governance/coverage/dtg-semantic-first-pass.json"
PROPOSALS = ROOT / "governance/coverage/dtg-semantic-decision-proposals.json"
REGISTER = ROOT / "governance/coverage/dtg-g2-adjudications.json"
DISPOSITIONS = {"covered", "partial", "missing", "not_applicable", "indeterminate"}

def source_key(row):
    return (row["source_repository"], row["source_commit"], row["source_path"])

def compile_register(first, proposals):
    indexed = {source_key(row): row for row in first["records"]}
    if len(indexed) != len(first["records"]) or len(indexed) != 17:
        raise ValueError("initial 17-record source evidence missing or duplicated")
    high_risk = {}
    for case in proposals["cases"]:
        key = source_key(case)
        if key not in indexed or key in high_risk:
            raise ValueError("orphaned or duplicate G2 high-risk case")
        if case["approval"] != "pending" or case["canonical_change_allowed"] is not False:
            raise ValueError("high-risk case incorrectly approved")
        high_risk[key] = case
    if len(high_risk) != 6:
        raise ValueError("six source-grounded high-risk cases required")
    rows = []
    for key, item in sorted(indexed.items()):
        high = high_risk.get(key)
        rows.append({
            "source_repository": key[0], "source_commit": key[1], "source_path": key[2],
            "source_label": item["source_label"],
            "tig_candidates": item["tig_lexical_candidates"],
            "preliminary_class": item["preliminary_class"],
            "case_id": high["case_id"] if high else None,
            "proposed_safe_handling": high["proposed_disposition"] if high else None,
            "decision": {
                "disposition": None, "mapping_strength": None,
                "rationale": None, "source_definition_evidence": None,
                "reviewer": None, "reviewed_at": None,
                "compatibility_assessment": None, "source_license_review": None,
                "approval_state": "pending", "canonical_change_allowed": False
            }
        })
    return {"schema_version": "1.0", "scope": "17 initially matched pinned DTG source definitions",
            "semantic_coverage": None, "approved_count": 0,
            "review_required_count": len(rows), "high_risk_count": len(high_risk),
            "source_rows": rows}

def validate_approval(register):
    rows = register["source_rows"]
    seen = set()
    approved = 0
    for row in rows:
        key = source_key(row)
        if key in seen:
            raise ValueError("duplicate adjudication record")
        seen.add(key)
        decision = row["decision"]
        state = decision["approval_state"]
        if state == "pending":
            if decision["disposition"] is not None or decision["mapping_strength"] is not None or decision["canonical_change_allowed"]:
                raise ValueError("pending semantic decision mutated to asserted disposition")
        elif state == "approved":
            if decision["disposition"] not in DISPOSITIONS:
                raise ValueError("invalid approved semantic disposition")
            mandatory = ("rationale", "source_definition_evidence", "reviewer", "reviewed_at",
                         "compatibility_assessment", "source_license_review")
            if not all(decision.get(k) for k in mandatory):
                raise ValueError("approved decision missing human source/compatibility evidence")
            if decision["mapping_strength"] == "exact" and decision["disposition"] != "covered":
                raise ValueError("exact mapping on non-covered decision")
            approved += 1
        else:
            raise ValueError("invalid approval state")
    if register["approved_count"] != approved:
        raise ValueError("approved count does not match decision records")
    if register["review_required_count"] != len(rows)-approved:
        raise ValueError("review-required count inconsistent")
    if approved != len(rows) and register["semantic_coverage"] is not None:
        raise ValueError("cannot assert complete semantic coverage with pending decisions")
    return approved

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=REGISTER)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    first = json.loads(FIRST.read_text())
    proposed = json.loads(PROPOSALS.read_text())
    expected = compile_register(first, proposed)
    if args.verify:
        current = json.loads(args.output.read_text())
        validate_approval(current)
        if [source_key(row) for row in current["source_rows"]] != [source_key(row) for row in expected["source_rows"]]:
            raise ValueError("adjudication register missing or adding source rows")
        if current["high_risk_count"] != expected["high_risk_count"]:
            raise ValueError("high-risk count drift")
        print(f"Verified G2 register: {len(current['source_rows'])} source rows; {current['approved_count']} approved")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
        print(f"Created {len(expected['source_rows'])} pending source-specific decisions")

if __name__ == "__main__":
    main()
