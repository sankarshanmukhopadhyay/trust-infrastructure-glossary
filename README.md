# Trust Infrastructure Glossary

[![Validate Trust Infrastructure Glossary](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/actions/workflows/validate-governance-glossary.yml/badge.svg)](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/actions/workflows/validate-governance-glossary.yml)
[![Pages](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/actions/workflows/pages.yml/badge.svg)](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/actions/workflows/pages.yml)
![Concepts](https://img.shields.io/badge/concepts-617-blue)
![Version](https://img.shields.io/badge/version-v2.2.0-blue)
![License](https://img.shields.io/badge/license-OWFa%201.0-blue)

The **Trust Infrastructure Glossary (TIG)** is an independent, governance-executable concept system for digital trust infrastructure. It combines plain-English and formal definitions with stable concept identifiers, language-tagged designations, provenance, lifecycle and assurance semantics, semantic relationships, cross-vocabulary mappings, deterministic validation, and machine-readable publication.

Version `v2.2.0` adds a governed taxonomy and lightweight ontology projection over the v2 concept corpus. It introduces a machine-readable portfolio candidate inventory, controlled SKOS-aligned predicates, explicit taxonomy assertions over canonical TIG concept IDs, deterministic JSON/JSON-LD/RDF semantic artifacts, and executable safeguards preventing descriptive ontology assertions from becoming downstream normative authority.

## Start here

The rendered GitHub Pages site is organized around what a reader is trying to accomplish rather than the repository's directory structure:

- **[Explore Concepts](explore/index.md)** — browse by topic, A–Z, or search.
- **[Use TIG](use/index.md)** — select vocabulary profiles, consume machine-readable artifacts, or integrate TIG downstream.
- **[Govern TIG](governance/index.md)** — review the semantic model, authoring rules, assurance, quality, source intake, and publication controls.
- **[Project](project/index.md)** — understand lineage, v2 migration, release notes, roadmap, and contribution paths.

Individual concept pages are progressive: plain-English meaning and the formal definition appear first; identity, provenance, relationships, and implementation/governance metadata follow at increasing levels of detail.

## v2 semantic contract

The authoritative unit is a **concept**, not a string label.

Each concept artifact can include:

- a stable `concept_id` such as `urn:tig:concept:delegation`;
- one preferred designation and zero or more alternative, deprecated, or discouraged designations;
- language tags so additional languages can be added without changing the concept identity;
- a formal definition and optional simple-English definition;
- editorial maturity that is separate from the lifecycle semantics described by the concept;
- provenance classification: `adopted`, `adapted`, `locally_defined`, or `mapped`;
- SKOS-aligned semantic relations (`broader`, `narrower`, `related`);
- SKOS-aligned cross-vocabulary mappings (`exact`, `close`, `broad`, `narrow`, `related`);
- governance, assurance, evidence, lifecycle, and control-plane metadata.

The legacy `term` and `aliases` fields remain in v2 as compatibility fields for existing consumers. New integrations should treat `concept_id` and `designations` as authoritative.

### Vocabulary, taxonomy and ontology

TIG keeps these layers deliberately separate:

- **Vocabulary:** canonical concept artifacts remain the source of semantic authority.
- **Taxonomy:** hierarchy is deterministically derived from canonical concept relations plus explicit governed hierarchy assertions between canonical TIG concept IDs.
- **Lightweight ontology:** typed SKOS-aligned edges are deterministically derived with provenance and a non-normative authority effect.

See [Taxonomy & Lightweight Ontology](governance/semantic/taxonomy-ontology.md) for the authority boundary, predicate contract, taxonomy assertion model and validation rules.

## Repository operating model

| Layer | Role | Authority |
|---|---|---|
| `glossary/terms/` | Structured concept artifacts | **Authoritative semantic source** |
| `schemas/` | JSON Schema and controlled vocabularies | **Validation contract** |
| `profiles/` | Reusable vocabulary profiles | Curated downstream consumption layer |
| `tools/` | Validation, generation, and quality utilities | Publication and integrity control plane |
| `governance/` | Maintainer, semantic, provenance, assurance, taxonomy and publication guidance | Maintainer-authored governance |
| `_terms/` | Generated Jekyll concept pages | **Generated output only** |
| `generated/json/` | JSON, JSON-LD, taxonomy, ontology, manifests, inventories and reports | **Generated output only** |
| `generated/rdf/` | SKOS-compatible Turtle, including ontology projection | **Generated output only** |
| `generated/markdown/` | Human-readable bundles and reports | **Generated output only** |

## Source-of-truth policy

Edit `glossary/terms/*.yaml` for concept-local semantics. Use `governance/taxonomy-relations.yaml` only for reviewed additive hierarchy assertions between existing canonical concept IDs where rewriting inherited concept artifacts is neither necessary nor desirable. Generated taxonomy and ontology outputs are projections, not independent sources of authority.

## Independence and lineage

This project originated as a fork of the Trust over IP Main Glossary. The v2.0.0 release created an independent project identity, authority model, semantic contract, release process, and source-intake policy. v2.1.0 expanded foundational portfolio vocabulary; v2.2.0 adds governed semantic projection while preserving those authority boundaries.

The project does **not** erase that lineage:

- concepts inherited or adapted from ToIP retain source citations and provenance;
- ToIP is treated as one monitored source corpus among standards, specifications, frameworks, and project vocabularies;
- new material is admitted through review rather than repository synchronization;
- source provenance does not automatically imply semantic or governance authority in TIG.

See [Project Lineage](governance/project-lineage.md).

## External practices adopted in v2

v2 draws on established open vocabulary practices without copying their governance wholesale:

- **CNCF / OpenSSF:** reader-first and plain-language review;
- **Glossarist / terminology-management practice:** separation of concepts from designations;
- **W3C SKOS:** preferred/alternative labels, concept relations, and mapping relations;
- **DCMI:** stable semantic identifiers and long-lived vocabulary governance;
- **Schema.org:** retirement instead of deletion and machine/human representations of the same vocabulary;
- **SPDX:** model-driven generated artifacts and bounded downstream profiles;
- **MDN:** layered reader experience and concise entry points;
- **Inclusive Naming Initiative:** distinction between deprecated concepts and discouraged designations.

These are design influences. Actual definition text is incorporated only through the repository's source-intake and licensing policy.

## Current quality posture

The generated governance quality report evaluates all **617** concepts and currently reports:

- quality score: `100.0 / 100`
- findings: `0`
- concepts with source coverage: `617`
- concepts with cross-reference coverage: `617`
- concepts with evidence coverage: `617`
- revocation-supported concepts with revocation-relevant evidence: `151`

This is a repository quality signal, not a certification claim.

## Machine-readable artifacts

Run the generators to produce:

- `generated/json/governance-executable-glossary.json`
- `generated/json/governance-executable-glossary.catalog.json`
- `generated/json/governance-executable-glossary.jsonld`
- `generated/json/tig-taxonomy.json`
- `generated/json/tig-ontology.jsonld`
- `generated/rdf/trust-infrastructure-glossary.ttl`
- `generated/rdf/tig-ontology.ttl`
- governance inventories and quality reports
- deterministic Jekyll pages and indexes

## Local maintainer workflow

```bash
pip install -r requirements.txt
python tools/validate_governance_glossary.py
python tools/validate_profiles.py
python tools/validate_semantic_model.py
python tools/build_governance_glossary.py
python tools/build_quality_report.py
python tools/build_semantic_model.py
python tools/build_jekyll_site.py
```

Build the site locally:

```bash
bundle install
bundle exec jekyll serve
```

## Contribution guidance

1. Treat the concept as the semantic object and the preferred label as one designation of it.
2. Preserve stable `concept_id` values after publication.
3. Distinguish adopted, adapted, locally defined, and mapped material.
4. Add plain-English text without weakening the formal definition.
5. Record mapping strength deliberately; do not use `exact` when meanings differ materially.
6. Retain provenance and applicable licensing/attribution evidence.
7. Treat predicate additions, taxonomy assertions and authority-effect changes as semantic-governance changes requiring explicit review.
8. Regenerate and review all derived artifacts before merge.

See [Contributing](Contributing.md), [Repository Operating Model](governance/repository-operating-model.md), and [Term Authoring Guide](governance/term-authoring-guide.md).

## Design intent

TIG is not a certification authority and does not certify implementations. It provides a controlled, inspectable semantic layer that standards, governance frameworks, policy engines, conformance systems, registries, agents, and assurance tooling can reference consistently.
