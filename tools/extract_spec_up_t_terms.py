#!/usr/bin/env python3
"""Extract explicit Spec-Up-T term definitions from pinned local source snapshots.

No network calls, inferred meaning, or semantic equivalence. Source snapshots
must be supplied by the operator from an identified repository revision.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

PATTERN = re.compile(r"\[\[def:\s*([^\]\n]+?)\s*\]\]", re.IGNORECASE)


def extract(source_root, repository, commit):
    if not re.fullmatch(r"[a-f0-9]{40}", commit):
        raise ValueError("commit must be a full 40-character lowercase SHA")
    terms_dir = source_root / "spec" / "terms-definitions"
    if not terms_dir.is_dir():
        raise ValueError("missing spec/terms-definitions directory")
    results = []
    for path in sorted(terms_dir.rglob("*.md")):
        data = path.read_bytes()
        labels = PATTERN.findall(data.decode("utf-8"))
        for position, label in enumerate(labels, start=1):
            results.append({
                "label": label.strip(),
                "source_repo": repository,
                "source_commit": commit,
                "source_path": str(path.relative_to(source_root)),
                "source_sha256": hashlib.sha256(data).hexdigest(),
                "definition_occurrence": position,
                "semantic_equivalence": "not_established",
            })
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    results = extract(args.source_root, args.repository, args.commit)
    output = {
        "extraction_method": "spec-up-t-explicit-definition-markers",
        "completeness": "only-marked-definitions-in-supplied-directory",
        "source_repository": args.repository,
        "source_commit": args.commit,
        "count": len(results),
        "semantic_coverage_claim": False,
        "terms": results,
    }
    rendered = json.dumps(output, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
