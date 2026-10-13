#!/usr/bin/env python3
"""Standalone catalog adopter prototype using Python standard library only.

No TIG Python tooling imported. This is an independently runnable reference
implementation, NOT an independently governed downstream implementation.
"""
import argparse
import json
import hashlib
import pathlib


class AdopterError(ValueError):
    pass


def validate(catalog, decisions, concept_id):
    records = catalog.get("concepts")
    if not isinstance(records, list) or catalog.get("concept_count") != len(records):
        raise AdopterError("invalid concept catalog count")
    ids = [record.get("concept_id") for record in records]
    if len(ids) != len(set(ids)) or any(not isinstance(cid, str) for cid in ids):
        raise AdopterError("duplicated or missing identity")
    matching = [row for row in records if row["concept_id"] == concept_id]
    if len(matching) != 1:
        raise AdopterError("concept identity cannot be uniquely resolved")
    record = matching[0]
    labels = record.get("designations") or []
    if not any(item.get("label") and item.get("status") == "preferred" for item in labels):
        raise AdopterError("preferred designation absent")
    if not record.get("provenance_classification"):
        raise AdopterError("provenance classification absent")
    disputed = [c for c in decisions.get("cases", [])
                if concept_id in c.get("tig_concepts", []) and c.get("approval") == "pending"]
    if not disputed:
        raise AdopterError("no negative ambiguity challenge case available")
    if any(c.get("canonical_change_allowed") is not False for c in disputed):
        raise AdopterError("unapproved exact mapping or mutation cannot be consumed")
    return {
        "schema_version": "1.0",
        "consumer": "TIG-owned standalone adopter prototype",
        "independently_maintained": False,
        "concept_id": concept_id,
        "concept_resolved": True,
        "preferred_designation": True,
        "source_provenance_present": True,
        "ambiguous_matches_rejected": len(disputed),
        "semantic_equivalence_verified": False,
        "conformance_scope": "single-concept-catalog-consumption-and-negative-ambiguity"
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--catalog", type=pathlib.Path, required=True)
    p.add_argument("--decisions", type=pathlib.Path, required=True)
    p.add_argument("--concept-id", default="urn:tig:concept:trust-task")
    p.add_argument("--output", type=pathlib.Path, required=True)
    args = p.parse_args()
    catalog_bytes = args.catalog.read_bytes()
    decision_bytes = args.decisions.read_bytes()
    result = validate(json.loads(catalog_bytes), json.loads(decision_bytes), args.concept_id)
    result["inputs"] = {
        "catalog_sha256": hashlib.sha256(catalog_bytes).hexdigest(),
        "decisions_sha256": hashlib.sha256(decision_bytes).hexdigest()
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
