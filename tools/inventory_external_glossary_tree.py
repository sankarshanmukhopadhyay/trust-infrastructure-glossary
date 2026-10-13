#!/usr/bin/env python3
"""Enumerate source-term blobs at immutable Git commits via the GitHub Trees API.

The output is evidence for what was in a repository directory at a revision.
It is NOT evidence that a rendered specification transcluded that revision.
"""
import argparse
import hashlib
import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path

REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
TERM_PREFIX = "spec/terms-definitions/"


class TreeAdmissionError(ValueError):
    pass


def github_json(url, token=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "tig-source-admission/1"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=35) as response:
            return json.load(response)
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        raise TreeAdmissionError(f"GitHub response failed for {url}: {exc}") from exc


def inventory(repository, commit, fetch=github_json, token=None):
    if (not REPO_RE.fullmatch(repository) or not SHA_RE.fullmatch(commit)\n            or any(segment in (".", "..") for segment in repository.split("/"))):
        raise TreeAdmissionError("repository or full commit SHA is invalid")
    url = f"https://api.github.com/repos/{repository}/git/trees/{commit}?recursive=1"
    data = fetch(url, token)
    if data.get("truncated") is not False or not isinstance(data.get("tree"), list):
        raise TreeAdmissionError("source Git tree is truncated or missing; never invent a denominator")
    seen = set()
    records = []
    for node in data["tree"]:
        path = node.get("path")
        if not isinstance(path, str) or not path.startswith(TERM_PREFIX) or not path.endswith(".md"):
            continue
        if node.get("type") != "blob" or not SHA_RE.fullmatch(str(node.get("sha", ""))):
            raise TreeAdmissionError(f"invalid source term blob: {path}")
        if path in seen:
            raise TreeAdmissionError(f"duplicate path: {path}")
        seen.add(path)
        records.append({"path": path, "blob_sha": node["sha"]})
    if not records:
        raise TreeAdmissionError("pinned source tree has no explicit terminology definition files")
    records.sort(key=lambda row: row["path"])
    return {
        "schema_version": "1.0",
        "source_repository": repository,
        "requested_commit": commit,
        "tree_sha": data.get("sha"),
        "tree_truncated": False,
        "term_directory": TERM_PREFIX,
        "term_file_count": len(records),
        "term_files": records,
        "rendered_spec_transclusion_revision_verified": False,
        "semantic_coverage": None,
    }


def write_report(record, output):
    serialized = json.dumps(record, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(serialized, encoding="utf-8")
    return hashlib.sha256(serialized.encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True, help="GitHub owner/repo")
    parser.add_argument("--commit", required=True, help="full 40-digit commit SHA")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    record = inventory(args.repository, args.commit, token=os.environ.get("GH_TOKEN"))
    print(json.dumps({"output": str(args.output), "count": record["term_file_count"],
                      "sha256": write_report(record, args.output)}, sort_keys=True))


if __name__ == "__main__":
    main()
