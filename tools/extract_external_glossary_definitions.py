#!/usr/bin/env python3
"""Extract explicit definitions from authenticated local Git checkouts."""
import argparse
import json
from pathlib import Path

from inventory_external_glossary_tree import TreeAdmissionError, write_report
from extract_spec_up_t_terms import extract
import subprocess


def extract_checked_out_tree(root, repository, commit):
    """Authenticate a local checkout before converting definition markers to evidence."""
    actual = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    if actual != commit:
        raise TreeAdmissionError(f"checkout revision drift: {actual} != {commit}")
    listing = subprocess.check_output(
        ["git", "-C", str(root), "ls-tree", "-r", "HEAD", "spec/terms-definitions"],
        text=True,
    )
    rows = []
    for line in listing.splitlines():
        prefix, path = line.split("\t", 1)
        mode, kind, sha = prefix.split()
        if kind == "blob" and path.endswith(".md"):
            rows.append({"path": path, "blob_sha": sha})
    if not rows:
        raise TreeAdmissionError("no tracked terminology source files")
    definitions = extract(root, repository, commit)
    by_path = {r["path"]: r["blob_sha"] for r in rows}
    for row in definitions:
        row["source_blob_sha"] = by_path[row["source_path"]]
        row["adjudication"] = "unreviewed"
        row["tig_mapping"] = None
    return {
        "schema_version": "1.0",
        "source_repository": repository,
        "source_commit": commit,
        "complete_git_tree_verified": True,
        "file_count": len(rows),
        "explicit_definition_count": len(definitions),
        "files_without_explicit_markers": sorted(
            set(by_path) - {r["source_path"] for r in definitions}),
        "source_section_transclusion_verified": False,
        "semantic_coverage": None,
        "terms": definitions
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    report = extract_checked_out_tree(args.source_root, args.repository, args.commit)
    digest = write_report(report, args.output)
    print(json.dumps({"repository": args.repository, "source_files": report["file_count"],
                      "marked_definitions": report["explicit_definition_count"],
                      "unmarked_files": len(report["files_without_explicit_markers"]),
                      "report_sha256": digest}, sort_keys=True))


if __name__ == "__main__":
    main()
