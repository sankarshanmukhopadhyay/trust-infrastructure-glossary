---
title: v2.2.0 Release Notes
parent: Project
nav_order: 1
permalink: /release-notes-v2-2-0/
---

# Trust Infrastructure Glossary v2.2.0

**Release date:** 16 September 2026

v2.2.0 is the **governed semantic projection** release. It extends TIG from a controlled vocabulary with semantic relations into a machine-verifiable taxonomy and lightweight ontology while preserving the v2 authority boundary and consumer contract.

## Added

- A machine-readable portfolio vocabulary candidate inventory with explicit `admitted_v2_2` and `deferred` dispositions.
- `governance/semantic-model.yaml` as the controlled predicate, authority-effect and semantic-projection contract.
- `governance/taxonomy-relations.yaml` for reviewed additive hierarchy assertions between existing canonical TIG concept IDs.
- Deterministic taxonomy generation to `generated/json/tig-taxonomy.json`.
- Deterministic ontology generation to `generated/json/tig-ontology.jsonld` and `generated/rdf/tig-ontology.ttl`.
- Semantic validation covering predicate registration, domain/range, inverse relations, endpoint resolution, provenance, taxonomy assertions, authority effect, candidate disposition and deterministic generation.
- GitHub Actions semantic evidence upload (`tig-semantic-model`) on validation runs.

## Initial taxonomy assertions

The release deliberately starts with a small, defensible hierarchy rather than inferring a broad classification tree:

- `delegator` → broader `actor`;
- `delegatee` → broader `actor`;
- `assurance boundary` → broader `assurance`;
- `attestation` → broader `evidence`.

These are descriptive classification assertions. They do not redefine the underlying concepts or create implementation requirements.

## Ontology authority boundary

Generated ontology edges have `descriptive-reference` effect only. TIG does not become a normative authority for downstream specifications merely because it represents semantic relationships in machine-readable form.

Source repositories retain authority for their own normative claims. Every projected edge carries provenance identifying either its originating concept artifact or the governed taxonomy assertion set.

Inherited semantic references whose targets are not canonical TIG concepts are preserved as evidence but excluded from typed ontology projection. The JSON/JSON-LD evidence records those exclusions explicitly and the Turtle projection never emits dangling triples.

## Compatibility

This is an additive minor release.

- Existing v2 concept identifiers remain stable.
- Existing concept fields and vocabulary profiles remain valid.
- Canonical `glossary/terms/*.yaml` artifacts remain the semantic source of truth.
- The taxonomy assertion overlay can classify existing concepts but cannot create, rename, redefine or normatively override them.
- Existing consumers may ignore the new semantic artifacts without migration.

## Portfolio vocabulary intake

The governed candidate inventory explicitly dispositions more than twenty portable cross-repository concepts spanning assurance, evidence, authority, lifecycle, privacy and interoperability. Admission to the candidate inventory is not equivalent to canonical concept promotion; future concept promotion remains separately reviewable.

## Validation and assurance evidence

The release pipeline requires:

```bash
python tools/validate_governance_glossary.py
python tools/validate_profiles.py
python tools/validate_semantic_model.py
python tools/build_governance_glossary.py
python tools/build_quality_report.py
python tools/build_semantic_model.py
python tools/build_jekyll_site.py
```

CI also fails if tracked generated artifacts drift from canonical sources. Semantic JSON/JSON-LD/RDF outputs are uploaded as workflow evidence and attached to the GitHub release.

## Release publication

The v2.2.0 release is published from protected `main` by GitHub Actions after the reviewed PR lands. The workflow creates tag `v2.2.0`, attaches the generated semantic artifacts, uses these release notes, and explicitly marks the release as GitHub's latest release.
