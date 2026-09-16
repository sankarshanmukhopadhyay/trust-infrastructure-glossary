---
title: "Taxonomy & Lightweight Ontology"
parent: "Semantic Model & Authoring"
nav_order: 2
---

# Taxonomy & Lightweight Ontology

TIG v2.2 adds an additive semantic projection over the existing concept corpus. It does **not** replace the canonical `glossary/terms/*.yaml` artifacts and it does not create a new normative authority surface.

## Three layers

| Layer | Purpose | Authority |
|---|---|---|
| Vocabulary | Stable concepts, designations, definitions and provenance | Canonical concept artifacts |
| Taxonomy | Navigable hierarchy derived from canonical `broader` / `narrower` relations | Derived; no independent semantic authority |
| Lightweight ontology | Typed graph derived from canonical `broader`, `narrower` and `related` relations | Derived descriptive-reference assertions |

The distinction is deliberate. A vocabulary answers **what concept is this?** A taxonomy answers **where does it sit?** The lightweight ontology answers **what governed semantic relationship is asserted between two concepts?**

## Authority boundary

All generated semantic edges have `descriptive-reference` effect. TIG MUST NOT transform a source specification, implementation observation or portfolio convention into a downstream normative requirement merely by representing it as an ontology edge. Where a source is normative, that source retains its own authority and provenance must remain visible.

The machine-readable policy is `governance/semantic-model.yaml`; validation fails if the model declares an independent normative effect.

## Derivation

`tools/build_semantic_model.py` scans canonical concept artifacts and deterministically produces:

- `generated/json/tig-taxonomy.json`;
- `generated/json/tig-ontology.jsonld`;
- `generated/rdf/tig-ontology.ttl`.

Taxonomy roots are computed as concepts without a canonical broader parent. Hierarchical edges are normalized from both `broader` and `narrower`. Ontology edges retain their originating concept artifact and provenance classification.

## Governed predicates

The v2.2 predicate surface is intentionally small and SKOS-aligned: `broader`, `narrower`, and `related`. Domain and range are both `Concept`. `broader` and `narrower` are reciprocal predicate definitions; `related` is symmetric. TIG does not infer missing reciprocal edges into canonical source files.

Adding a predicate is an authority-impacting change. Update the registry, validator, documentation and compatibility notes in one reviewed change.

## Assurance checks

Run:

```bash
python tools/validate_semantic_model.py
python tools/build_semantic_model.py
```

Validation tests resolvable featured roots, registered predicates, domain/range constraints, inverse-predicate contracts, edge provenance, descriptive authority effect, candidate disposition and deterministic generation. Existing glossary validation remains independently required.

## Candidate admission

`governance/portfolio-vocabulary-candidates.yaml` records portfolio-derived candidates separately from canonical term promotion. `admitted_v2_2` means the concept is accepted into the bounded v2.2 vocabulary work queue; `deferred` means useful but not promoted in this tranche. Neither disposition imports normative authority from a source repository.
