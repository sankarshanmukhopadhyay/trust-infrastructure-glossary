---
title: "Ontology"
parent: "Semantic Model"
nav_order: 3
permalink: /semantic-model/ontology/
---

# Ontology

The TIG lightweight ontology answers **how canonical concepts are related** in a machine-verifiable graph.

The v2.2 predicate surface is intentionally small and SKOS-aligned: `broader`, `narrower`, and `related`. Projected edges require resolvable concept endpoints and provenance, and they carry `descriptive-reference` authority effect.

## What the ontology provides

- typed semantic edges between canonical concepts;
- deterministic JSON-LD and Turtle projections;
- provenance identifying the concept artifact or governed taxonomy assertion that produced an edge;
- explicit exclusion evidence for inherited references whose targets are not canonical TIG concepts.

## What it does not provide

The ontology does not certify implementations, infer normative requirements for downstream specifications, or create authority merely because a relationship is machine-readable.

## Public view

[Explore semantic relationships]({{ '/explore/relationships/' | relative_url }})

## Machine views

- `generated/json/tig-ontology.jsonld`
- `generated/rdf/tig-ontology.ttl`

[View the artifact catalogue]({{ '/artifacts/' | relative_url }})
