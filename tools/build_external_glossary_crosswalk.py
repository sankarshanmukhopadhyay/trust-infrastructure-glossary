#!/usr/bin/env python3
"""Build an exhaustive, non-semantic source-to-TIG lexical review queue."""
import argparse
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path


class CrosswalkError(ValueError):
    pass


def normalized(value):
    text = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(re.findall(r"[\w]+", text, re.UNICODE))


def build(catalog, source_reports):
    concepts = catalog.get("concepts")
    if not isinstance(concepts, list) or catalog.get("concept_count") != len(concepts):
        raise CrosswalkError("TIG concept catalog incomplete")
    labels_to_ids = defaultdict(set)
    ids = set()
    for concept in concepts:
        cid = concept.get("concept_id")
        if not cid or cid in ids:
            raise CrosswalkError("missing or duplicate TIG concept ID")
        ids.add(cid)
        for designation in concept.get("designations") or []:
            label = designation.get("label")
            if label and normalized(label):
                labels_to_ids[normalized(label)].add(cid)
    rows = []
    seen = set()
    for source in source_reports:
        repo, sha = source["source_repository"], source["source_commit"]
        if source.get("explicit_definition_count") != len(source.get("terms", [])):
            raise CrosswalkError(f"incomplete source definition inventory: {repo}")
        for item in source["terms"]:
            key = (repo, sha, item["source_path"], item["definition_occurrence"])
            if key in seen:
                raise CrosswalkError(f"duplicate source definition: {key}")
            seen.add(key)
            if item["source_repo"] != repo or item["source_commit"] != sha:
                raise CrosswalkError(f"unverified source identity: {key}")
            labels = [item["label"], *(item.get("aliases") or [])]
            candidates = sorted({cid for label in labels for cid in labels_to_ids.get(normalized(label), set())})
            rows.append({
                "source_repository": repo,
                "source_commit": sha,
                "source_path": item["source_path"],
                "source_blob_sha": item["source_blob_sha"],
                "definition_occurrence": item["definition_occurrence"],
                "source_label": item["label"],
                "source_aliases": item.get("aliases") or [],
                "tig_lexical_candidates": candidates,
                "candidate_class": "unmatched" if not candidates else ("ambiguous" if len(candidates) > 1 else "one_candidate"),
                "semantic_disposition": "unreviewed",
                "mapping_assertion": None,
            })
    rows.sort(key=lambda row: (row["source_repository"], row["source_path"], row["definition_occurrence"]))
    count = sum(bool(row["tig_lexical_candidates"]) for row in rows)
    return {
        "schema_version": "1.0",
        "source_definition_count": len(rows),
        "tig_concept_count": len(ids),
        "lexical_candidate_source_rows": count,
        "no_lexical_candidate_source_rows": len(rows) - count,
        "semantic_coverage": None,
        "authority_status": "preliminary-non-normative-candidate-discovery",
        "source_definition_rows": rows,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--catalog", type=Path, required=True)
    p.add_argument("--source", type=Path, action="append", required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    result = build(json.loads(args.catalog.read_text(encoding="utf-8")),
                   [json.loads(path.read_text(encoding="utf-8")) for path in args.source])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"source_rows": result["source_definition_count"],
                      "lexical_candidates": result["lexical_candidate_source_rows"],
                      "no_lexical_candidates": result["no_lexical_candidate_source_rows"],
                      "semantic_coverage": None}, sort_keys=True))


if __name__ == "__main__":
    main()
