#!/usr/bin/env python3
"""Minimal real consumer of TIG's generated public JSON catalog."""
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "generated/json/trust-infrastructure-glossary.catalog.json"
SOURCE = ROOT / "glossary/terms/trust-task.yaml"
PROPOSALS = ROOT / "governance/coverage/dtg-semantic-decision-proposals.json"


class ConsumerError(AssertionError):
    pass


def qualify(catalog, term, proposals):
    rows = catalog.get("concepts")
    if not isinstance(rows, list) or catalog.get("concept_count") != len(rows):
        raise ConsumerError("malformed catalog or mismatch between advertised and actual concept count")
    by_id = {}
    for row in rows:
        cid = row.get("concept_id")
        if not isinstance(cid, str) or cid in by_id:
            raise ConsumerError(f"missing/duplicate concept ID: {cid}")
        by_id[cid] = row
    expected = term.get("concept_id")
    found = by_id.get(expected)
    if found is None:
        raise ConsumerError(f"published consumer cannot resolve {expected}")
    if found.get("designations") != term.get("designations"):
        raise ConsumerError("published designations differ from canonical artifact")
    if found.get("provenance_classification") != term.get("provenance", {}).get("classification"):
        raise ConsumerError("published provenance classification differs from canonical artifact")
    pending = [case for case in proposals["cases"] if expected in case.get("tig_concepts", [])
               and case.get("approval") == "pending"]
    if not pending:
        raise ConsumerError("ambiguity rejection fixture missing from high-risk semantic cases")
    for case in pending:
        if case.get("canonical_change_allowed") is not False:
            raise ConsumerError(f"unapproved source match allowed to mutate TIG: {case['case_id']}")
    return {
        "concept_id": expected, "resolved": True, "catalog_count": len(rows),
        "designations_verified": True, "provenance_verified": True,
        "pending_source_matches_rejected": len(pending),
        "independent_implementation": False,
        "semantic_equivalence_approved": False
    }


def main():
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    term = yaml.safe_load(SOURCE.read_text(encoding="utf-8"))
    proposals = json.loads(PROPOSALS.read_text(encoding="utf-8"))
    print(json.dumps(qualify(catalog, term, proposals), sort_keys=True))


if __name__ == "__main__":
    main()
