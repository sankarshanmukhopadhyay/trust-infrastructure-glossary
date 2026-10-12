#!/usr/bin/env python3
"""Build a deterministic, non-normative human-review queue from TIG candidate mappings."""
import argparse
import json
from pathlib import Path

from report_source_crosswalk_discovery import discover


def build_queue(data, term_dir):
    findings = discover(data, term_dir)
    queue = []
    for row, finding in zip(data["candidates"], findings):
        mapped = row.get("concept_id")
        matches = finding["lexical_matches"]
        conflict = mapped is not None and matches and mapped not in matches
        queue.append({
            "source_id": row["source_id"],
            "label": row["label"],
            "current_concept_id": mapped,
            "lexical_candidates": matches,
            "review_state": row["disposition"],
            "reason": row["rationale"],
            "review_priority": "high" if conflict or row["disposition"] == "review_required" else "normal",
            "lexical_conflict": bool(conflict),
            "semantic_equivalence": "not_established",
        })
    return sorted(queue, key=lambda x: (x["review_priority"] != "high", x["source_id"], x["label"]))


def report(data, term_dir):
    queue = build_queue(data, term_dir)
    return {
        "schema_version": "0.1",
        "scope": data["scope"],
        "status": "exploratory-unadjudicated",
        "coverage_denominator": None,
        "concepts_examined": len(list(term_dir.glob("*.yaml"))),
        "candidate_count": len(queue),
        "review_required": sum(row["review_state"] == "review_required" for row in queue),
        "unresolved": sum(row["review_state"] == "unresolved" for row in queue),
        "lexical_conflicts": sum(row["lexical_conflict"] for row in queue),
        "queue": queue,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--crosswalk", type=Path, default=Path("governance/coverage/dtg-vtc-pilot.json"))
    parser.add_argument("--terms", type=Path, default=Path("glossary/terms"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = json.loads(args.crosswalk.read_text(encoding="utf-8"))
    result = report(data, args.terms)
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
