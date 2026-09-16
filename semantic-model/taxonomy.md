---
title: "Taxonomy"
parent: "Semantic Model"
nav_order: 2
permalink: /semantic-model/taxonomy/
---

# Taxonomy

The TIG taxonomy answers **where a concept sits** in a governed classification hierarchy.

Hierarchy is derived from canonical `broader` / `narrower` relations plus reviewed additive assertions in `governance/taxonomy-relations.yaml`. Every hierarchy endpoint must resolve to an existing canonical TIG concept.

## Authority boundary

A taxonomy assertion classifies existing concepts. It does not create a concept, rewrite its definition, or turn a descriptive classification into a downstream implementation requirement.

The v2.2 release intentionally began with a small, defensible hierarchy rather than inferring a broad tree without evidence.

## Public view

[Browse the generated taxonomy]({{ '/explore/taxonomy/' | relative_url }})

## Machine view

Use `generated/json/tig-taxonomy.json` when systems need roots and parent/child edges deterministically derived from governed sources.

[View the artifact catalogue]({{ '/artifacts/' | relative_url }})
