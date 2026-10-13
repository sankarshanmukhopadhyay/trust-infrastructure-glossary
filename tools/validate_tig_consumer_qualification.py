#!/usr/bin/env python3
"""Validate bounded TIG human and machine consumer qualification evidence."""
import argparse
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVIDENCE = ROOT / "governance/adoption/tig-consumer-qualification-2026-10-13.json"


class QualificationError(AssertionError):
    """Raised when consumer qualification evidence is inconsistent."""


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise QualificationError(message)


def _repo_path(relative: str) -> Path:
    return ROOT / relative


def _validate_observation_paths(evidence: dict) -> None:
    for journey in evidence.get("journeys", []):
        _require(journey.get("id"), "journey missing id")
        _require(journey.get("consumer") in {"human_reader", "machine_consumer"}, f"unsupported consumer for {journey.get('id')}")
        _require(journey.get("question"), f"journey {journey.get('id')} missing question")
        for entry in journey.get("entry_points", []):
            _require(_repo_path(entry).exists(), f"entry point does not exist: {entry}")
        for observation in journey.get("observations", []):
            _require(observation.get("result") in {"PASS", "FAIL", "INDETERMINATE"}, f"invalid result in {observation.get('id')}")
            _require(observation.get("expected"), f"observation {observation.get('id')} missing expected")
            _require(observation.get("observed"), f"observation {observation.get('id')} missing observed")
            _require(_repo_path(observation["path"]).exists(), f"observation path does not exist: {observation['path']}")


def _validate_trust_task_round_trip() -> None:
    term_path = ROOT / "glossary/terms/trust-task.yaml"
    term = yaml.safe_load(term_path.read_text(encoding="utf-8"))
    _require(term["concept_id"] == "urn:tig:concept:trust-task", "trust-task concept_id changed")
    _require(term.get("designations"), "trust-task designations missing")
    _require(term.get("provenance", {}).get("classification") in {"adopted", "adapted", "locally_defined", "mapped"}, "trust-task provenance classification invalid")
    _require(term.get("editorial", {}).get("status"), "trust-task editorial status missing")
    mappings = term.get("concept_mappings") or {}
    for relation in ("exact", "close", "broad", "narrow"):
        _require(mappings.get(relation) == [], f"trust-task unexpectedly has approved {relation} mappings")
    _require((ROOT / "_terms/trust-task.md").exists(), "generated trust-task concept page missing")


def _validate_machine_products_exist() -> None:
    required = [
        "generated/json/trust-infrastructure-glossary.json",
        "generated/json/trust-infrastructure-glossary.jsonld",
        "generated/rdf/trust-infrastructure-glossary.ttl",
        "generated/json/tig-taxonomy.json",
        "generated/json/tig-ontology.jsonld",
        "generated/rdf/tig-ontology.ttl",
    ]
    for relative in required:
        _require(_repo_path(relative).exists(), f"machine-readable product missing: {relative}")


def _validate_unapproved_semantic_candidates() -> None:
    first_pass = _load_json(ROOT / "governance/coverage/dtg-semantic-first-pass.json")
    _require(first_pass.get("approval_required") is True, "first-pass semantic register no longer requires approval")
    records = first_pass.get("records", [])
    _require(records, "first-pass semantic register contains no records")
    for row in records:
        _require(row.get("decision_state") == "requires_semantic_approval", f"semantic candidate approved without explicit review: {row.get('source_label')}")
        _require(row.get("mapping_assertion") is None, f"semantic candidate has mapping assertion: {row.get('source_label')}")
        _require(row.get("tig_lexical_candidates"), f"semantic review record lacks lexical candidates: {row.get('source_label')}")


def _validate_high_risk_decisions_remain_pending() -> None:
    proposals = _load_json(ROOT / "governance/coverage/dtg-semantic-decision-proposals.json")
    records = proposals.get("cases", [])
    _require(records, "semantic decision proposal register contains no cases")
    for row in records:
        _require(row.get("approval") == "pending", f"high-risk proposal unexpectedly approved: {row.get('source_label')}")
        _require(row.get("canonical_change_allowed") is False, f"canonical mutation allowed before approval: {row.get('source_label')}")


def _validate_negative_cases(evidence: dict) -> None:
    cases = evidence.get("negative_cases", [])
    _require(len(cases) >= 3, "expected at least three negative consumer qualification cases")
    for case in cases:
        _require(case.get("result") == "PASS", f"negative case did not pass: {case.get('id')}")
        _require(_repo_path(case["evidence_path"]).exists(), f"negative-case evidence path missing: {case['evidence_path']}")
        _require(case.get("expected_guard"), f"negative case missing expected guard: {case.get('id')}")


def validate_qualification(path: Path = DEFAULT_EVIDENCE) -> dict:
    evidence = _load_json(path)
    _require(evidence.get("schema_version") == "1.0", "unsupported qualification schema_version")
    _require(evidence.get("assessment_date") == "2026-10-13", "unexpected assessment date")
    _require("non-normative" in evidence.get("authority_boundary", ""), "authority boundary must preserve non-normative TIG status")
    _validate_observation_paths(evidence)
    _validate_trust_task_round_trip()
    _validate_machine_products_exist()
    _validate_unapproved_semantic_candidates()
    _validate_high_risk_decisions_remain_pending()
    _validate_negative_cases(evidence)
    _require(evidence.get("final_decision", {}).get("state") == "bounded_work_complete", "final decision must close the bounded tranche")
    return evidence


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", type=Path, default=DEFAULT_EVIDENCE)
    args = parser.parse_args()
    evidence = validate_qualification(args.evidence)
    journeys = ", ".join(j["id"] for j in evidence["journeys"])
    print(f"TIG consumer qualification passed for journeys: {journeys}")


if __name__ == "__main__":
    main()
