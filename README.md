# Trust Infrastructure Glossary

[![Validate Trust Infrastructure Glossary](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/actions/workflows/validate-governance-glossary.yml/badge.svg)](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/actions/workflows/validate-governance-glossary.yml)
[![Pages](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/actions/workflows/pages.yml/badge.svg)](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/actions/workflows/pages.yml)
![Concepts](https://img.shields.io/badge/concepts-617-blue)
![Version](https://img.shields.io/badge/version-v2.2.0-blue)
![License](https://img.shields.io/badge/license-OWFa%201.0-blue)

The **Trust Infrastructure Glossary (TIG)** is a governed semantic infrastructure for digital trust systems. It combines a controlled concept vocabulary with governed taxonomy, a lightweight ontology projection, provenance, lifecycle and assurance metadata, bounded profiles, deterministic validation and machine-readable publication.

TIG is written for people and published for machines. It is not a certification authority, and representing a source concept or relationship does not silently transfer normative authority into TIG or from TIG into a downstream implementation.

## Start here

The public GitHub Pages site is organized around reader and adopter jobs rather than repository directories:

- **[Explore Concepts](explore/index.md)** — A–Z, domain paths, generated taxonomy, relationship exploration and search.
- **[Semantic Model](semantic-model/index.md)** — vocabulary, taxonomy, ontology, provenance and authority boundaries.
- **[Use TIG](use/index.md)** — choose an integration path, profile or machine-readable semantic product.
- **[Govern TIG](governance/index.md)** — authoring, admission, source intake, assurance, quality and publication controls.
- **[Project](project/index.md)** — releases, lineage, roadmap and contribution paths.

## Semantic product model

TIG keeps five layers deliberately separate:

| Layer | Role | Authority |
|---|---|---|
| **Vocabulary** | Stable concepts, designations, definitions and provenance | Canonical concept artifacts |
| **Taxonomy** | Reviewed classification over canonical concepts | Governed descriptive projection |
| **Ontology** | Typed semantic relationships with provenance | Governed descriptive projection |
| **Profiles & artifacts** | Bounded and machine-readable consumption surfaces | Derived consumption layer |
| **Governance** | Admission, change control, validation and publication | Maintainer-authored governance |

The authoritative unit is a **concept**, not a string label. New integrations should treat `concept_id` and language-tagged `designations` as authoritative identity fields; legacy `term` and `aliases` remain compatibility fields.

## Repository architecture vs published information architecture

The repository is optimized for maintainers, validation and evidence production. The website is optimized for readers, adopters and semantic navigation. They deliberately do **not** mirror one another.

### Maintainer/source architecture

| Path | Role |
|---|---|
| `glossary/terms/` | Canonical structured concepts |
| `schemas/` | Validation contracts and controlled vocabularies |
| `profiles/` | Bounded vocabulary selections |
| `governance/semantic-model.yaml` | Semantic projection and predicate contract |
| `governance/taxonomy-relations.yaml` | Reviewed additive hierarchy assertions |
| `governance/` | Maintainer governance and operating policy |
| `tools/` | Validation, generation and quality control plane |
| `generated/` | Derived machine-readable evidence |
| `_terms/` | Generated concept pages |

### Published information architecture

The public site groups the same governed material into **Concepts**, **Semantic Model**, **Use TIG**, **Govern TIG**, and **Project**. Generated taxonomy and relationship exploration pages are built from semantic sources; they are navigation views, not a second authority layer.

## Source-of-truth policy

Edit `glossary/terms/*.yaml` for concept-local semantics. Use `governance/taxonomy-relations.yaml` only for reviewed additive hierarchy assertions between existing canonical concept IDs. The semantic projection contract lives in `governance/semantic-model.yaml`.

Generated vocabulary, taxonomy, ontology, site exploration pages, inventories and quality reports are reproducible outputs. They must not be hand-maintained as independent semantic truth.

## Machine-readable semantic products

TIG publishes:

- Vocabulary JSON: `generated/json/trust-infrastructure-glossary.json`
- Vocabulary JSON-LD: `generated/json/trust-infrastructure-glossary.jsonld`
- Vocabulary Turtle: `generated/rdf/trust-infrastructure-glossary.ttl`
- Taxonomy JSON: `generated/json/tig-taxonomy.json`
- Ontology JSON-LD: `generated/json/tig-ontology.jsonld`
- Ontology Turtle: `generated/rdf/tig-ontology.ttl`
- validated vocabulary profiles under `profiles/`
- governance inventories, manifests and quality evidence under `generated/`

See [Machine-readable Artifacts](artifacts.md) for product-oriented consumption guidance.

## Validation and local maintainer workflow

```bash
pip install -r requirements.txt
python tools/validate_governance_glossary.py
python tools/validate_profiles.py
python tools/validate_semantic_model.py
python tools/build_governance_glossary.py
python tools/build_quality_report.py
python tools/build_semantic_model.py
python tools/build_jekyll_site.py
python tools/build_site_information_architecture.py
python tools/validate_site_ia.py
```

Build the site locally:

```bash
bundle install
bundle exec jekyll serve
```

CI performs the same semantic and site-IA checks and rejects tracked generated-artifact drift.

## Current quality posture

The governance quality report covers all **617** canonical concepts and reports `100.0 / 100` with `0` findings for the current release. This is a repository quality signal, not a certification claim.

## Independence and lineage

TIG originated as a fork of the Trust over IP Main Glossary. The v2 series established independent project identity, governance, semantic contract, release process and source-intake policy while preserving inherited attribution and provenance. ToIP is now one monitored source corpus among standards, specifications, frameworks and project vocabularies.

See [Project Lineage](governance/project-lineage.md).

## Contribution guidance

1. Treat the concept as the semantic object and labels as designations.
2. Preserve stable `concept_id` values after publication.
3. Distinguish adopted, adapted, locally defined and mapped material.
4. Retain provenance and applicable attribution evidence.
5. Treat predicate additions, taxonomy assertions and authority-effect changes as semantic-governance changes requiring explicit review.
6. Treat public IA changes as projection changes: they must not redefine canonical semantics.
7. Regenerate and validate derived artifacts before merge.

See [Contributing](Contributing.md), [Repository Operating Model](governance/repository-operating-model.md), and [Term Authoring Guide](governance/term-authoring-guide.md).
