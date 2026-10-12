#!/usr/bin/env python3
"""Verify pinned upstream Git trees and extract specification-owned definitions."""
import argparse
import json
import subprocess
from pathlib import Path
from extract_spec_up_t_terms import extract

FOLDERS = {
    "trustoverip/dtgwg-cred-spec": "credentials",
    "trustoverip/dtgwg-vti-spec": "vti",
    "trustoverip/dtgwg-trust-tasks-spec": "tasks",
}


def build(manifest, sources_root):
    results = []
    for entry in manifest["repositories"]:
        repo, commit = entry["repository"], entry["commit_sha"]
        if repo not in FOLDERS:
            raise ValueError("unapproved source repository: " + repo)
        root = sources_root / FOLDERS[repo]
        actual = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
        if actual != commit:
            raise ValueError(f"{repo}: checked out {actual}, expected {commit}")
        expected = {row["path"]: row["blob_sha"] for row in entry["term_files"]}
        tracked = subprocess.check_output(["git", "-C", str(root), "ls-tree", "-r", "HEAD", "spec/terms-definitions"], text=True)
        actual_files = {}
        for line in tracked.splitlines():
            prefix, path = line.split("\t", 1)
            mode, kind, sha = prefix.split()
            if kind == "blob" and path.endswith(".md"):
                actual_files[path] = sha
        if actual_files != expected:
            missing = sorted(set(expected) - set(actual_files))
            extra = sorted(set(actual_files) - set(expected))
            changed = sorted(p for p in set(expected) & set(actual_files) if actual_files[p] != expected[p])
            raise ValueError(f"{repo}: tree drift: missing={missing}; extra={extra}; changed={changed}")
        definitions = extract(root, repo, commit)
        if len(definitions) < 1:
            raise ValueError(f"{repo}: no explicit definitions extracted")
        results.append({
            "repository": repo, "commit_sha": commit, "term_file_count": len(expected),
            "explicit_definition_count": len(definitions), "definitions": definitions,
        })
    return {
        "schema_version": "1.0",
        "scope": "three pinned canonical Spec-Up-T terminology directories",
        "complete_directory_listing_verified": True,
        "external_transcluded_definitions_included": False,
        "out_of_directory_definitions_included": False,
        "crosswalk_semantic_equivalence": "not_established",
        "repositories": results,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--sources-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    report = build(manifest, args.sources_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    for item in report["repositories"]:
        print(f'{item["repository"]}: {item["term_file_count"]} files; {item["explicit_definition_count"]} marked definitions')


if __name__ == "__main__":
    main()
