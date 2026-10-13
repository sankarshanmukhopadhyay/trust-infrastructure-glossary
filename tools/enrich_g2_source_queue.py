#!/usr/bin/env python3
"""Resolve source labels for the complete 106-record DTG G2 review queue from pinned checkouts."""
import argparse
import json
import subprocess
from pathlib import Path
from extract_spec_up_t_terms import extract
from build_g2_full_source_queue import build, verify

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = {
    "trustoverip/dtgwg-cred-spec": "credentials",
    "trustoverip/dtgwg-vti-spec": "vti",
    "trustoverip/dtgwg-trust-tasks-spec": "tasks",
}

def enrich(pins, matched, sources_root):
    result = build(pins, matched)
    labels = {}
    for repo in pins["repositories"]:
        name, commit = repo["repository"], repo["commit_sha"]
        root = sources_root / FOLDERS[name]
        actual = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
        if actual != commit:
            raise ValueError(f"source revision drift: {name}")
        listing = subprocess.check_output(
            ["git", "-C", str(root), "ls-tree", "-r", "HEAD", "spec/terms-definitions"],
            text=True,
        )
        found = {}
        for line in listing.splitlines():
            prefix, path = line.split("\t", 1)
            _, kind, sha = prefix.split()
            if kind == "blob" and path.endswith(".md"):
                found[path] = sha
        expected = {x["path"]: x["blob_sha"] for x in repo["term_files"]}
        if found != expected:
            raise ValueError(f"source path/blob evidence drift: {name}")
        definitions = extract(root, name, commit)
        if len(definitions) != len(expected):
            raise ValueError(f"not exactly one explicitly marked definition per file: {name}")
        for entry in definitions:
            key = (name, commit, entry["source_path"])
            if key in labels:
                raise ValueError("duplicate explicit source label")
            labels[key] = entry
    if len(labels) != 106:
        raise ValueError("unreconciled source definition evidence")
    for row in result["records"]:
        key = (row["source_repository"], row["source_commit"], row["source_path"])
        source = labels[key]
        if row["source_label"] is not None and row["source_label"].casefold() != source["label"].casefold():
            raise ValueError(f"first-pass source label differs: {key}")
        row["source_label"] = source["label"]
        row["source_aliases"] = source["aliases"]
        row["source_sha256"] = source["source_sha256"]
        row["source_label_extracted"] = True
    result["pinned_explicit_definition_verification"] = True
    verify(result)
    return result

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--sources-root", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    pins = json.loads((ROOT / "governance/coverage/pinned-dtg-spec-term-trees.json").read_text())
    matched = json.loads((ROOT / "governance/coverage/dtg-g2-adjudications.json").read_text())
    record = enrich(pins, matched, args.sources_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"verified_labels": sum(r["source_label_extracted"] for r in record["records"]),
                      "candidate_records": record["first_pass_matched_count"],
                      "no_candidate_records": record["without_lexical_candidate_count"],
                      "approved_semantic_decisions": 0}, sort_keys=True))

if __name__ == "__main__":
    main()
