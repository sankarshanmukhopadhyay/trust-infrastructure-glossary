#!/usr/bin/env python3
"""Shared deterministic builder/validator support for the TIG semantic model."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "governance" / "semantic-model.yaml"
CANDIDATE_PATH = ROOT / "governance" / "portfolio-vocabulary-candidates.yaml"
TERMS_DIR = ROOT / "glossary" / "terms"


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a mapping")
    return data


def load_concepts() -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    concepts: dict[str, dict[str, Any]] = {}
    paths: dict[str, str] = {}
    for path in sorted(TERMS_DIR.glob("*.yaml")):
        data = load_yaml(path)
        concept_id = data.get("concept_id")
        if not isinstance(concept_id, str) or not concept_id:
            raise ValueError(f"{path}: missing concept_id")
        if concept_id in concepts:
            raise ValueError(f"duplicate concept_id: {concept_id}")
        concepts[concept_id] = data
        paths[concept_id] = path.relative_to(ROOT).as_posix()
    return concepts, paths


def canonical_edges(
    model: dict[str, Any],
    concepts: dict[str, dict[str, Any]],
    paths: dict[str, str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return projectable edges plus unresolved legacy references.

    Canonical concept artifacts can retain inherited semantic references whose target
    has never been promoted to a TIG concept. Those references remain source evidence,
    but they are not emitted as ontology edges because a typed ontology edge must have
    resolvable Concept/Concept endpoints.
    """
    predicates = model["ontology"]["predicates"]
    edges: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    for subject in sorted(concepts):
        concept = concepts[subject]
        provenance = concept.get("provenance") or {}
        classification = provenance.get("classification")
        relations = concept.get("semantic_relations") or {}
        for predicate in sorted(relations):
            if predicate not in predicates:
                continue
            targets = relations.get(predicate) or []
            for obj in sorted(set(targets)):
                record = {
                    "subject": subject,
                    "predicate": predicate,
                    "object": obj,
                    "provenance": {
                        "concept_artifact": paths[subject],
                        "classification": classification,
                    },
                    "authority_effect": predicates[predicate]["authority_effect"],
                }
                if obj not in concepts:
                    unresolved.append(
                        {
                            **record,
                            "projection_status": "excluded-unresolved-target",
                            "reason": "target concept_id is not present in the canonical TIG concept corpus",
                        }
                    )
                    continue
                edges.append(record)
    return edges, unresolved


def build_semantic_model() -> dict[str, Any]:
    model = load_yaml(MODEL_PATH)
    concepts, paths = load_concepts()
    edges, unresolved = canonical_edges(model, concepts, paths)

    child_ids: set[str] = set()
    hierarchy_edges: list[dict[str, str]] = []
    for edge in edges:
        if edge["predicate"] == "broader":
            child_ids.add(edge["subject"])
            hierarchy_edges.append({"child": edge["subject"], "parent": edge["object"]})
        elif edge["predicate"] == "narrower":
            child_ids.add(edge["object"])
            hierarchy_edges.append({"child": edge["object"], "parent": edge["subject"]})

    hierarchy_edges = sorted(
        {(edge["child"], edge["parent"]) for edge in hierarchy_edges}
    )
    hierarchy = [{"child": child, "parent": parent} for child, parent in hierarchy_edges]
    roots = sorted(set(concepts) - child_ids)

    return {
        "schema_version": model["schema_version"],
        "model_id": model["model_id"],
        "status": model["status"],
        "authority": model["authority"],
        "taxonomy": {
            "derivation": model["taxonomy"]["derivation"],
            "root_policy": model["taxonomy"]["root_policy"],
            "featured_roots": sorted(model["taxonomy"].get("featured_roots", [])),
            "roots": roots,
            "hierarchy": hierarchy,
            "concept_count": len(concepts),
        },
        "ontology": {
            "derivation": model["ontology"]["derivation"],
            "predicates": model["ontology"]["predicates"],
            "edges": edges,
            "edge_count": len(edges),
            "excluded_unresolved_references": unresolved,
            "excluded_unresolved_reference_count": len(unresolved),
        },
    }


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def jsonld_document(graph: dict[str, Any]) -> dict[str, Any]:
    predicates = graph["ontology"]["predicates"]
    return {
        "@context": {
            "tig": "urn:tig:",
            "skos": "http://www.w3.org/2004/02/skos/core#",
            **{name: spec["iri"] for name, spec in sorted(predicates.items())},
        },
        "@id": graph["model_id"],
        "@type": "tig:SemanticModel",
        "authority": graph["authority"],
        "taxonomy": graph["taxonomy"],
        "edges": [
            {
                "@id": f"{edge['subject']}#{edge['predicate']}#{edge['object']}",
                "subject": {"@id": edge["subject"]},
                "predicate": edge["predicate"],
                "object": {"@id": edge["object"]},
                "provenance": edge["provenance"],
                "authority_effect": edge["authority_effect"],
            }
            for edge in graph["ontology"]["edges"]
        ],
        "excluded_unresolved_references": graph["ontology"]["excluded_unresolved_references"],
    }


def turtle_document(graph: dict[str, Any]) -> str:
    lines = [
        "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .",
        "@prefix tig: <urn:tig:> .",
        "",
        "# Generated from canonical TIG concept artifacts.",
        "# These triples have descriptive-reference effect only; source repositories retain normative authority.",
        "# Unresolved legacy references are excluded from triples and reported in the JSON/JSON-LD evidence.",
        "",
    ]
    iri_by_predicate = {
        name: spec["iri"] for name, spec in graph["ontology"]["predicates"].items()
    }
    for edge in graph["ontology"]["edges"]:
        predicate_iri = iri_by_predicate[edge["predicate"]]
        lines.append(f"<{edge['subject']}> <{predicate_iri}> <{edge['object']}> .")
    return "\n".join(lines) + "\n"
