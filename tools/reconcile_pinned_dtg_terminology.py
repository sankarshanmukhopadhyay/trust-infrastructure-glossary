#!/usr/bin/env python3
"""Create a source-scoped, non-semantic TIG lexical crosswalk from authenticated upstream evidence."""
import argparse
import json
from pathlib import Path

import yaml
from report_source_crosswalk_discovery import normalize


def crosswalk(inventory, terms_dir):
    index = {}
    for path in sorted(terms_dir.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        cid = data.get("concept_id")
        if not isinstance(cid, str):
            continue
        labels = [data.get("term"), *(data.get("aliases") or [])]
        labels.extend(d.get("label") for d in (data.get("designations") or []) if isinstance(d, dict))
        for label in labels:
            if isinstance(label, str) and label.strip():
                index.setdefault(normalize(label), set()).add(cid)
    rows = []
    for source in inventory["repositories"]:
        for record in source["definitions"]:
            labels = [record["label"], *(record.get("aliases") or [])]
            matched = sorted({cid for label in labels if isinstance(label, str) for cid in index.get(normalize(label), set())})
            rows.append({
                "source_repository": source["repository"],
                "source_commit": source["commit_sha"],
                "source_path": record["source_path"],
                "source_sha256": record["source_sha256"],
                "source_label": record["label"],
                "source_aliases": record.get("aliases", []),
                "lexical_candidates": matched,
                "lexical_status": "match_candidate" if matched else "no_match_detected",
                "semantic_status": "review_required",
                "mapping_assertion": None,
            })
    rows.sort(key=lambda x: (x["source_repository"], x["source_path"], x["source_label"]))
    total = len(rows)
    with_matches = sum(bool(x["lexical_candidates"]) for x in rows)
    return {
        "schema_version": "1.0",
        "scope": inventory["scope"],
        "source_definition_denominator": total,
        "source_definitions_with_lexical_candidates": with_matches,
        "source_definitions_without_lexical_candidates": total - with_matches,
        "semantic_coverage_denominator": None,
        "semantic_coverage_percentage": None,
        "adjudication_status": "unreviewed",
        "sources_included": [x["repository"] for x in inventory["repositories"]],
        "crosswalk": rows,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--inventory", type=Path, required=True)
    p.add_argument("--terms", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
    result = crosswalk(inventory, args.terms)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{result['source_definitions_with_lexical_candidates']}/{result['source_definition_denominator']} definitions have lexical candidates; semantic coverage unassessed")


if __name__ == "__main__":
    main()
