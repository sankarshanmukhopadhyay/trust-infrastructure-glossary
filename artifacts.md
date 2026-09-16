---
title: Machine-readable Artifacts
nav_order: 2
parent: "Use TIG"
---

# Machine-readable Artifacts

Choose the **semantic product** you need first; use the filesystem path only as its transport location. All generated products are derived from governed TIG source artifacts.

## Semantic products

| Product | Format | Purpose | Path |
|---|---|---|---|
| **TIG Vocabulary** | JSON | Complete structured concept dataset for programmatic use | `generated/json/trust-infrastructure-glossary.json` |
| **TIG Vocabulary** | JSON-LD | Linked-data representation of the concept system | `generated/json/trust-infrastructure-glossary.jsonld` |
| **TIG Vocabulary** | Turtle | SKOS-compatible RDF representation | `generated/rdf/trust-infrastructure-glossary.ttl` |
| **TIG Catalogue** | JSON | Compact discovery/catalogue view | `generated/json/trust-infrastructure-glossary.catalog.json` |
| **TIG Taxonomy** | JSON | Governed broader/narrower hierarchy and roots | `generated/json/tig-taxonomy.json` |
| **TIG Ontology** | JSON-LD | Typed, provenance-bearing semantic graph | `generated/json/tig-ontology.jsonld` |
| **TIG Ontology** | Turtle | RDF projection of projectable semantic edges | `generated/rdf/tig-ontology.ttl` |
| **Vocabulary Profiles** | YAML | Bounded concept selections for downstream domains | `profiles/*.yaml` |
| **Governance Inventory** | JSON / Markdown | Authority, lifecycle, evidence and control-plane inventory | `generated/json/governance-inventory.json` |
| **Quality Report** | JSON / Markdown | Repository validation and assurance-readiness evidence | `generated/json/governance-quality-report.json` |
| **Artifact Manifest** | JSON / Markdown | Inputs, generators, intended use and stability expectations | `generated/json/artifact-manifest.json` |

## Which product should I use?

- Use the **Vocabulary** when you need definitions, designations, identifiers or concept metadata.
- Use the **Taxonomy** when you need hierarchical classification or navigation.
- Use the **Ontology** when you need typed semantic relationships or graph traversal.
- Use a **Profile** when your project needs a bounded subset without redefining TIG concepts.
- Use the **Inventory / Quality Report** when you need governance and assurance evidence about the published corpus.

[Read the Semantic Model]({{ '/semantic-model/' | relative_url }}) for the authority boundary between these products.

## Compatibility bundles

The following v1-era filenames remain generated during the v2 migration window:

- `generated/json/governance-executable-glossary.json`
- `generated/json/governance-executable-glossary.jsonld`
- `generated/json/governance-executable-glossary.catalog.json`
- `generated/markdown/governance-executable-glossary.md`

New consumers should use the canonical TIG product names above.

## Generation and evidence

Maintainer workflows validate canonical sources, profiles and semantic projection before generating publication artifacts. CI fails when tracked generated outputs drift from their governed sources.

```bash
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
