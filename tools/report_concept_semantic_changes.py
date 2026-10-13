#!/usr/bin/env python3
"""Conservative, deterministic comparison of two TIG concept snapshots.

Inputs must be two already checked-out, explicitly identified corpus directories.
This tool does not authenticate a Git revision or adjudicate semantic equivalence.
"""
import argparse
import json
from pathlib import Path
import yaml


class SnapshotError(ValueError):
    pass


def read_concepts(directory):
    directory = Path(directory)
    if not directory.is_dir():
        raise SnapshotError(f"concept snapshot directory missing: {directory}")
    paths = sorted(directory.glob("*.yaml"))
    if not paths:
        raise SnapshotError(f"concept snapshot contains no YAML artifacts: {directory}")
    concepts = {}
    for path in paths:
        try:
            item = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            raise SnapshotError(f"invalid concept artifact {path}: {exc}") from exc
        if not isinstance(item, dict) or not isinstance(item.get("concept_id"), str):
            raise SnapshotError(f"artifact missing concept_id: {path}")
        cid = item["concept_id"]
        if not cid.startswith("urn:tig:concept:"):
            raise SnapshotError(f"unsupported concept_id: {cid}")
        if cid in concepts:
            raise SnapshotError(f"duplicate concept_id: {cid}")
        concepts[cid] = item
    return concepts


def compare(before, after, before_ref, after_ref):
    if not before_ref.strip() or not after_ref.strip():
        raise SnapshotError("snapshot references must be nonempty")
    changes = []
    for cid in sorted(set(before) | set(after)):
        left, right = before.get(cid), after.get(cid)
        if left is None:
            change = ["new_concept"]
        elif right is None:
            change = ["concept_missing_from_target"]
        elif left == right:
            continue
        else:
            change = []
            if left.get("designations") != right.get("designations"):
                change.append("designation_changed")
            if left.get("editorial", {}).get("status") != right.get("editorial", {}).get("status"):
                change.append("editorial_status_changed")
            for key in ("definition", "simple_definition", "concept_mappings", "semantic_relations", "provenance", "sources"):
                if left.get(key) != right.get(key):
                    change.append("semantic_review_required")
                    break
            covered = {"designations", "editorial"}
            watched = {"definition", "simple_definition", "concept_mappings", "semantic_relations", "provenance", "sources"}
            if {k: v for k, v in left.items() if k not in covered | watched} != {k: v for k, v in right.items() if k not in covered | watched}:
                change.append("other_metadata_review_required")
            if left.get("editorial", {}).get("reviewed") != right.get("editorial", {}).get("reviewed"):
                change.append("other_metadata_review_required")
            change = sorted(set(change))
        changes.append({"concept_id": cid, "change_classes": change, "semantic_approval": "not_assessed"})
    return {
        "schema_version": "1.0",
        "before_ref": before_ref,
        "after_ref": after_ref,
        "authoritative": False,
        "semantic_equivalence_assessed": False,
        "changed_count": len(changes),
        "changes": changes,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", required=True, type=Path, help="older glossary/terms directory")
    parser.add_argument("--after", required=True, type=Path, help="newer glossary/terms directory")
    parser.add_argument("--before-ref", required=True, help="explicit tag or full commit SHA")
    parser.add_argument("--after-ref", required=True, help="explicit tag or full commit SHA")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = compare(read_concepts(args.before), read_concepts(args.after), args.before_ref, args.after_ref)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{result['changed_count']} concept identities have detected changes; semantic approval not assessed")


if __name__ == "__main__":
    main()
