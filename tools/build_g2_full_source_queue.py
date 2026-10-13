#!/usr/bin/env python3
"""Account for all 106 pinned DTG definition files in an unresolved G2 review queue."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def build(pins, matched):
    rows = []
    indexed = {(r["source_repository"], r["source_commit"], r["source_path"]): r
               for r in matched["source_rows"]}
    if len(indexed) != len(matched["source_rows"]) or len(indexed) != 17:
        raise ValueError("17 verified lexical candidate records required")
    encountered = set()
    for repo in pins["repositories"]:
        for file in repo["term_files"]:
            key = (repo["repository"], repo["commit_sha"], file["path"])
            if key in encountered:
                raise ValueError("duplicate pinned source definition file")
            encountered.add(key)
            known = indexed.get(key)
            rows.append({
                "source_repository": key[0], "source_commit": key[1],
                "source_path": key[2], "source_blob_sha": file["blob_sha"],
                "matched_candidate_record": bool(known),
                "case_id": known["case_id"] if known else None,
                "tig_lexical_candidates": known["tig_candidates"] if known else [],
                "source_label": known["source_label"] if known else None,
                "source_label_extracted": bool(known),
                "source_definition_review_status": "pending",
                "semantic_disposition": None,
                "mapping_assertion": None,
                "reviewer": None,
                "review_evidence": None,
                "canonical_change_allowed": False
            })
    if len(rows) != 106 or len(encountered.intersection(indexed)) != 17:
        raise ValueError("pinned 106-row universe does not reconcile to 17 source candidates")
    return {
        "schema_version": "1.0",
        "scope": "three pinned DTG spec/terms-definitions directories",
        "pinned_file_definition_count": len(rows),
        "first_pass_matched_count": 17,
        "without_lexical_candidate_count": 89,
        "approved_semantic_dispositions": 0,
        "semantic_coverage": None,
        "admitted_wider_corpus": False,
        "records": sorted(rows, key=lambda x: (x["source_repository"], x["source_path"]))
    }

def verify(report):
    records = report["records"]
    if len(records) != 106 or len({(r["source_repository"], r["source_commit"], r["source_path"]) for r in records}) != 106:
        raise ValueError("complete unique 106-row source universe required")
    if report["first_pass_matched_count"] != sum(r["matched_candidate_record"] for r in records):
        raise ValueError("inconsistent lexical match count")
    if report["without_lexical_candidate_count"] != sum(not r["matched_candidate_record"] for r in records):
        raise ValueError("inconsistent no-candidate count")
    if any(r["semantic_disposition"] is not None or r["mapping_assertion"] is not None or r["canonical_change_allowed"] for r in records):
        raise ValueError("unreviewed source has an asserted disposition or canonical edit")
    if report["approved_semantic_dispositions"] or report["semantic_coverage"] is not None:
        raise ValueError("source-review register fabricates semantic approval")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    pins = json.loads((ROOT / "governance/coverage/pinned-dtg-spec-term-trees.json").read_text())
    matched = json.loads((ROOT / "governance/coverage/dtg-g2-adjudications.json").read_text())
    report = build(pins, matched)
    verify(report)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("Reconciled 106 source records: 17 lexical candidate rows and 89 without; 0 approved")

if __name__ == "__main__":
    main()
