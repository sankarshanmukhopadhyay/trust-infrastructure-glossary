#!/usr/bin/env python3
"""Parse pinned external Spec-Up-T definitions from Git blobs, without semantic promotion."""
import argparse
import base64
import hashlib
import json
import os
import re
from pathlib import Path

from inventory_external_glossary_tree import TreeAdmissionError, write_report
from extract_spec_up_t_terms import extract
import subprocess

PATTERN = re.compile(r"\[\[def:\s*([^\]\n]+?)\s*\]\]", re.IGNORECASE)


def extract_from_blobs(manifest, fetch=github_json, token=None):
    repo = manifest["source_repository"]
    terms = []
    unmarked = []
    for file in manifest["term_files"]:
        path, sha = file["path"], file["blob_sha"]
        payload = fetch(f"https://api.github.com/repos/{repo}/git/blobs/{sha}", token)
        if payload.get("encoding") != "base64" or not isinstance(payload.get("content"), str):
            raise TreeAdmissionError(f"blob unavailable or not base64: {path}")
        try:
            raw = base64.b64decode(payload["content"], validate=False)
        except Exception as exc:
            raise TreeAdmissionError(f"unreadable blob: {path}") from exc
        # Verify that returned blob is actually the committed Git object.
        header = f"blob {len(raw)}\0".encode()
        git_sha = hashlib.sha1(header + raw).hexdigest()
        if git_sha != sha:
            raise TreeAdmissionError(f"blob SHA mismatch: {path}")
        decoded = raw.decode("utf-8")
        matches = PATTERN.findall(decoded)
        if not matches:
            unmarked.append(path)
        for index, literal in enumerate(matches, 1):
            parts = [part.strip() for part in literal.split(",")]
            label = parts[0]
            if not label:
                raise TreeAdmissionError(f"empty definition label: {path}")
            terms.append({
                "source_repository": repo,
                "source_commit": manifest["requested_commit"],
                "source_path": path,
                "source_blob_sha": sha,
                "source_sha256": hashlib.sha256(raw).hexdigest(),
                "occurrence": index,
                "label": label,
                "aliases": [x for x in parts[1:] if x],
                "adjudication": "unreviewed",
                "tig_mapping": None
            })
    return {
        "schema_version": "1.0",
        "source_repository": repo,
        "source_commit": manifest["requested_commit"],
        "complete_git_tree_verified": not manifest["tree_truncated"],
        "file_count": manifest["term_file_count"],
        "explicit_definition_count": len(terms),
        "files_without_explicit_markers": unmarked,
        "source_section_transclusion_verified": False,
        "semantic_coverage": None,
        "terms": terms
    }


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
        prefix, path = line.split("\\t", 1)
        mode, kind, sha = prefix.split()
        if kind == "blob" and path.endswith(".md"):
            rows.append({"path": path, "blob_sha": sha})
    if not rows:
        raise TreeAdmissionError("no tracked terminology source files")
    manifest = {"source_repository": repository, "requested_commit": commit,
                "tree_truncated": False, "term_file_count": len(rows),
                "term_files": sorted(rows, key=lambda x: x["path"])}
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
