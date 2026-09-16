#!/usr/bin/env python3
"""Validate TIG taxonomy/ontology governance and derived graph integrity."""
from __future__ import annotations

import sys

from semantic_model_core import (
    CANDIDATE_PATH,
    MODEL_PATH,
    TAXONOMY_RELATIONS_PATH,
    build_semantic_model,
    canonical_json,
    load_concepts,
    load_yaml,
)


def main() -> int:
    errors: list[str] = []
    model = load_yaml(MODEL_PATH)
    candidates = load_yaml(CANDIDATE_PATH)
    taxonomy_relations = load_yaml(TAXONOMY_RELATIONS_PATH)
    concepts, _ = load_concepts()

    authority = model.get("authority") or {}
    if authority.get("normative_effect") != "none":
        errors.append("semantic model must declare normative_effect: none")

    predicates = (model.get("ontology") or {}).get("predicates") or {}
    required = {"broader", "narrower", "related"}
    if set(predicates) != required:
        errors.append(f"predicate registry must be exactly {sorted(required)}")

    for name, spec in sorted(predicates.items()):
        if spec.get("domain") != "Concept" or spec.get("range") != "Concept":
            errors.append(f"{name}: domain/range must be Concept/Concept")
        inverse = spec.get("inverse")
        if inverse not in predicates:
            errors.append(f"{name}: inverse {inverse!r} is not registered")
        elif predicates[inverse].get("inverse") != name:
            errors.append(f"{name}: inverse contract is not reciprocal")
        if spec.get("authority_effect") != "descriptive-reference":
            errors.append(f"{name}: authority_effect must be descriptive-reference")

    admitted = list((candidates.get("candidates") or {}).get("admitted_v2_2") or [])
    deferred = list((candidates.get("candidates") or {}).get("deferred") or [])
    dispositioned = admitted + deferred
    if len(set(admitted)) < 20:
        errors.append("candidate inventory must explicitly admit at least 20 unique v2.2 candidates")
    if len(set(dispositioned)) != len(dispositioned):
        errors.append("candidate inventory contains duplicate dispositions")

    for concept_id in model.get("taxonomy", {}).get("featured_roots", []):
        if concept_id not in concepts:
            errors.append(f"featured root does not resolve: {concept_id}")

    assertions = taxonomy_relations.get("assertions") or []
    if not assertions:
        errors.append("governed taxonomy assertion set must not be empty")
    for assertion in assertions:
        subject = assertion.get("subject")
        predicate = assertion.get("predicate")
        obj = assertion.get("object")
        provenance = assertion.get("provenance") or {}
        if subject not in concepts:
            errors.append(f"taxonomy assertion subject does not resolve: {subject}")
        if obj not in concepts:
            errors.append(f"taxonomy assertion object does not resolve: {obj}")
        if predicate not in {"broader", "narrower"}:
            errors.append(f"taxonomy assertion predicate must be broader/narrower: {predicate}")
        if not assertion.get("rationale"):
            errors.append(f"taxonomy assertion lacks rationale: {subject} {predicate} {obj}")
        if not provenance.get("classification") or not provenance.get("source"):
            errors.append(f"taxonomy assertion lacks provenance: {subject} {predicate} {obj}")

    graph = build_semantic_model()
    if graph["taxonomy"].get("hierarchy_edge_count", 0) < 1:
        errors.append("derived taxonomy must contain at least one governed hierarchy edge")

    for edge in graph["ontology"]["edges"]:
        source = edge["provenance"].get("concept_artifact", "<unknown>")
        if edge["subject"] not in concepts:
            errors.append(f"edge subject does not resolve: {edge['subject']} (source: {source})")
        if edge["object"] not in concepts:
            errors.append(f"edge object does not resolve: {edge['object']} (source: {source}, subject: {edge['subject']})")
        if edge["predicate"] not in predicates:
            errors.append(f"edge predicate is not registered: {edge['predicate']} (source: {source})")
        if not edge["provenance"].get("concept_artifact") or not edge["provenance"].get("classification"):
            errors.append(f"edge lacks provenance: {edge['subject']} {edge['predicate']} {edge['object']}")

    excluded = graph["ontology"].get("excluded_unresolved_references") or []
    for edge in excluded:
        source = edge.get("provenance", {}).get("concept_artifact", "<unknown>")
        if edge.get("subject") not in concepts:
            errors.append(f"excluded relation subject does not resolve: {edge.get('subject')} (source: {source})")
        if edge.get("object") in concepts:
            errors.append(
                f"excluded relation target now resolves and must be projected: {edge.get('object')} "
                f"(source: {source}, subject: {edge.get('subject')})"
            )
        if edge.get("predicate") not in predicates:
            errors.append(f"excluded relation predicate is not registered: {edge.get('predicate')} (source: {source})")
        if edge.get("projection_status") != "excluded-unresolved-target":
            errors.append(f"excluded relation lacks bounded projection status (source: {source})")
        provenance = edge.get("provenance") or {}
        if not provenance.get("concept_artifact") or not provenance.get("classification"):
            errors.append(
                f"excluded relation lacks provenance: {edge.get('subject')} {edge.get('predicate')} {edge.get('object')}"
            )

    if graph["ontology"].get("excluded_unresolved_reference_count") != len(excluded):
        errors.append("excluded unresolved relation count does not match evidence list")

    if canonical_json(build_semantic_model()) != canonical_json(build_semantic_model()):
        errors.append("semantic model generation is non-deterministic")

    if errors:
        print("Semantic model validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Semantic model validation passed: "
        f"{len(concepts)} concepts, {len(graph['taxonomy']['roots'])} taxonomy roots, "
        f"{graph['taxonomy']['hierarchy_edge_count']} hierarchy edges, "
        f"{graph['ontology']['edge_count']} typed edges, {len(excluded)} unresolved legacy references excluded, "
        f"{len(admitted)} admitted candidates."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
