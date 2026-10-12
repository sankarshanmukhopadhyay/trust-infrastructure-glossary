#!/usr/bin/env python3
"""Validate a bounded source-to-concept candidate crosswalk.

This checks referential integrity and epistemic states, not semantic equivalence.
"""
import argparse
import json
from pathlib import Path
import sys

STATES = {"candidate", "adjudicated"}
DISPOSITIONS = {"review_required", "unresolved", "covered", "partial", "missing", "not_applicable"}
AUTHORITY = {"normative", "working-draft", "spec-entry-point", "generated-working-draft", "informative-draft", "implementation"}


def validate(data, term_ids):
    errors = []
    if data.get("schema_version") != "0.1":
        errors.append("unsupported schema_version")
    sources = data.get("sources")
    candidates = data.get("candidates")
    if not isinstance(sources, list) or not sources:
        return ["sources must be a nonempty list"]
    if not isinstance(candidates, list):
        return ["candidates must be a list"]
    ids = set()
    for idx, source in enumerate(sources):
        if not isinstance(source, dict):
            errors.append(f"source {idx}: expected object")
            continue
        sid = source.get("id")
        if not isinstance(sid, str) or not sid or sid in ids:
            errors.append(f"source {idx}: missing or duplicate id")
        else:
            ids.add(sid)
        if source.get("authority") not in AUTHORITY:
            errors.append(f"source {idx}: invalid authority")
        if not isinstance(source.get("url"), str) or not source["url"].startswith("https://"):
            errors.append(f"source {idx}: missing HTTPS reference")
        sha = source.get("blob_sha")
        if not isinstance(sha, str) or len(sha) != 40 or any(c not in "0123456789abcdef" for c in sha):
            errors.append(f"source {idx}: invalid file blob SHA")
    seen = set()
    for idx, row in enumerate(candidates):
        if not isinstance(row, dict):
            errors.append(f"candidate {idx}: expected object")
            continue
        label, source, state, disp, cid = [row.get(k) for k in ("label", "source_id", "state", "disposition", "concept_id")]
        if not isinstance(label, str) or not label.strip():
            errors.append(f"candidate {idx}: empty label")
        key = (source, label.casefold()) if isinstance(label, str) else None
        if key in seen:
            errors.append(f"candidate {idx}: duplicate source/label")
        seen.add(key)
        if source not in ids:
            errors.append(f"candidate {idx}: unknown source_id")
        if state not in STATES or disp not in DISPOSITIONS:
            errors.append(f"candidate {idx}: invalid state or disposition")
        if cid is not None and (not isinstance(cid, str) or cid not in term_ids):
            errors.append(f"candidate {idx}: unknown concept_id")
        if disp == "covered" and (state != "adjudicated" or not cid):
            errors.append(f"candidate {idx}: covered requires adjudication and a known concept")
        if state == "candidate" and disp not in {"review_required", "unresolved"}:
            errors.append(f"candidate {idx}: candidate state cannot claim coverage")
        if not isinstance(row.get("rationale"), str) or not row["rationale"].strip():
            errors.append(f"candidate {idx}: missing rationale")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--crosswalk", type=Path, default=Path("governance/coverage/dtg-vtc-pilot.json"))
    parser.add_argument("--terms", type=Path, default=Path("glossary/terms"))
    args = parser.parse_args()
    try:
        import yaml
        ids = set()
        for p in args.terms.glob("*.yaml"):
            term = yaml.safe_load(p.read_text(encoding="utf-8"))
            if isinstance(term, dict) and isinstance(term.get("concept_id"), str):
                ids.add(term["concept_id"])
        data = json.loads(args.crosswalk.read_text(encoding="utf-8"))
        errors = validate(data, ids)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Crosswalk input error: {exc}", file=sys.stderr)
        return 2
    if errors:
        for item in errors:
            print(item, file=sys.stderr)
        return 1
    print(f"Crosswalk valid: {len(data['sources'])} sources; {len(data['candidates'])} exploratory candidates; no completeness claim")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
