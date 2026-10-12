#!/usr/bin/env python3
"""Inspect every canonical TIG concept for a candidate designation; no semantic equivalence inference."""
import argparse
import json
from pathlib import Path
import yaml


def normalize(value):
    return " ".join(value.casefold().replace("-", " ").replace("_", " ").split())


def discover(data, terms):
    index = {}
    for path in sorted(terms.glob("*.yaml")):
        item = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        cid = item.get("concept_id")
        if not isinstance(cid, str):
            continue
        names = [item.get("term")] + (item.get("aliases") or [])
        names += [d.get("label") for d in item.get("designations", []) if isinstance(d, dict)]
        for name in names:
            if isinstance(name, str) and name.strip():
                index.setdefault(normalize(name), set()).add(cid)
    report = []
    for row in data["candidates"]:
        candidates = sorted(index.get(normalize(row["label"]), set()))
        report.append({
            "source_id": row["source_id"], "label": row["label"],
            "recorded_concept_id": row.get("concept_id"),
            "lexical_matches": candidates,
            "lexical_match_count": len(candidates),
            "disposition": row["disposition"],
            "semantic_equivalence": "not_established",
        })
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--crosswalk", type=Path, default=Path("governance/coverage/dtg-vtc-pilot.json"))
    parser.add_argument("--terms", type=Path, default=Path("glossary/terms"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = json.loads(args.crosswalk.read_text(encoding="utf-8"))
    output = {"scope": data["scope"], "canonical_term_files_scanned": len(list(args.terms.glob("*.yaml"))),
              "coverage_denominator": None, "semantic_coverage_claim": False,
              "candidate_results": discover(data, args.terms)}
    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
