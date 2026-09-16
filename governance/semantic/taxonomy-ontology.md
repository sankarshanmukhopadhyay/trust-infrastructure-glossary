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
| Taxonomy | Navigable hierarchy over canonical TIG concept IDs | Governed descriptive assertions; no independent normative authority |
| Lightweight ontology | Typed graph derived from canonical semantic relations plus governed taxonomy assertions | Derived descriptive-reference assertions |

The distinction is deliberate. A vocabulary answers **what concept is this?** A taxonomy answers **where does it sit?** The lightweight ontology answers **what governed semantic relationship is asserted between two concepts?**

## Authority boundary

All generated semantic edges have `descriptive-reference` effect. TIG MUST NOT transform a source specification, implementation observation or portfolio convention into a downstream normative requirement merely by representing it as an ontology edge. Where a source is normative, that source retains its own authority and provenance must remain visible.

The machine-readable policy is `governance/semantic-model.yaml`; validation fails if the model declares an independent normative effect.

## Canonical relation sources

The v2.2 graph has two governed input surfaces:

1. `glossary/terms/*.yaml` supplies concept-local `broader`, `narrower`, and `related` relations.
2. `governance/taxonomy-relations.yaml` supplies explicit additive hierarchy assertions between existing canonical TIG concept IDs when a cross-cutting classification should not require rewriting inherited concept artifacts.

Every taxonomy assertion must resolve both endpoints, use only `broader` or `narrower`, provide a rationale and provenance, and retain `descriptive-reference` authority effect. The overlay cannot create concepts and cannot override concept definitions.

## Derivation

`tools/build_semantic_model.py` deterministically produces:

- `generated/json/tig-taxonomy.json`;
- `generated/json/tig-ontology.jsonld`;
- `generated/rdf/tig-ontology.ttl`.

Taxonomy roots are computed as concepts without a governed broader parent. Hierarchical edges are normalized from both `broader` and `narrower`. Ontology edges retain provenance identifying either the originating concept artifact or the governed taxonomy assertion set.

Inherited semantic references whose targets are not canonical TIG concepts remain auditable source evidence but are excluded from typed ontology projection. The JSON/JSON-LD evidence reports those exclusions explicitly; Turtle never emits a dangling triple.

## Governed predicates

The v2.2 predicate surface is intentionally small and SKOS-aligned: `broader`, `narrower`, and `related`. Domain and range are both `Concept`. `broader` and `narrower` are reciprocal predicate definitions; `related` is symmetric. TIG does not infer missing reciprocal edges into canonical source files.

Adding a predicate is an authority-impacting change. Update the registry, validator, documentation and compatibility notes in one reviewed change.

## Assurance checks

Run:

```bash
python tools/validate_semantic_model.py
python tools/build_semantic_model.py
```

Validation tests resolvable featured roots, governed taxonomy assertions, registered predicates, domain/range constraints, inverse-predicate contracts, edge provenance, descriptive authority effect, candidate disposition, exclusion of unresolved legacy targets, non-empty taxonomy hierarchy and deterministic generation. Existing glossary validation remains independently required.

## Candidate admission

`governance/portfolio-vocabulary-candidates.yaml` records portfolio-derived candidates separately from canonical term promotion. `admitted_v2_2` means the concept is accepted into the bounded v2.2 vocabulary work queue; `deferred` means useful but not promoted in this tranche. Neither disposition imports normative authority from a source repository.
