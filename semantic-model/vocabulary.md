---
title: "Vocabulary"
parent: "Semantic Model"
nav_order: 1
permalink: /semantic-model/vocabulary/
---

# Vocabulary

The TIG vocabulary is the controlled concept layer: **what a concept is called, what it means, how it is identified, and where that meaning came from**.

## Canonical unit

The authoritative unit is a concept identified by a stable `concept_id`, not a string label. A concept can carry a preferred designation, alternative or deprecated designations, formal and plain-language definitions, provenance, editorial state, mappings and governance/assurance metadata.

Canonical concept artifacts live in `glossary/terms/*.yaml`. Generated pages and machine-readable bundles are publication views over those artifacts.

## What vocabulary does not do

Vocabulary membership alone does not assert that one concept is a subtype of another or that a source specification normatively requires a relationship. Classification belongs to the taxonomy layer; typed graph traversal belongs to the ontology layer.

## Explore or consume

- [Explore concepts]({{ '/explore/' | relative_url }})
- [Browse A–Z]({{ '/terms-index/' | relative_url }})
- [Browse by domain]({{ '/concepts/' | relative_url }})
- [Choose a machine-readable product]({{ '/artifacts/' | relative_url }})
