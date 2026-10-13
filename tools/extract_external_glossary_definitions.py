#!/usr/bin/env python3
"""Parse pinned external Spec-Up-T definitions from Git blobs, without semantic promotion."""
import argparse
import base64
import hashlib
import json
import os
import re
import urllib.request
from pathlib import Path

from inventory_external_glossary_tree import github_json, TreeAdmissionError, inventory, write_report

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    token = os.environ.get("GH_TOKEN")
    manifest = inventory(args.repository, args.commit, token=token)
    report = extract_from_blobs(manifest, token=token)
    digest = write_report(report, args.output)
    print(json.dumps({"repository": args.repository, "source_files": report["file_count"],
                      "marked_definitions": report["explicit_definition_count"],
                      "unmarked_files": len(report["files_without_explicit_markers"]),
                      "report_sha256": digest}, sort_keys=True))


if __name__ == "__main__":
    main()
