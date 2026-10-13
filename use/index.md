---
title: "Use TIG"
nav_order: 4
has_children: true
---

# Use TIG

Choose the smallest stable TIG product that serves your use case. A `concept_id` identifies a TIG concept; it does not automatically approve an external semantic mapping.

## Choose a consumption path

| Your requirement | Recommended starting point |
| --- | --- |
| Reference one meaning consistently | Use the concept's stable `concept_id` and pin a TIG release |
| Find a term or identifier programmatically | [Vocabulary JSON and catalogue]({{ '/artifacts/' | relative_url }}) |
| Reuse a defined subset | [Vocabulary profiles]({{ '/profiles/' | relative_url }}) |
| Browse a classification hierarchy | [Taxonomy]({{ '/semantic-model/taxonomy/' | relative_url }}) |
| Traverse semantic edges | [Ontology]({{ '/semantic-model/ontology/' | relative_url }}) |
| Map another source vocabulary | Apply reviewed mapping strength; do not infer `exact` from labels |

## Minimal adoption pattern

1. Select the concept or bounded profile you actually need.
2. Record its `concept_id`, TIG release/revision and the local context of use.
3. Read provenance and mapping status before asserting correspondence with an external specification.
4. Validate your integration using the published machine-readable artifacts.

[Read the artifact catalogue]({{ '/artifacts/' | relative_url }}) · [Downstream consumption guidance]({{ '/governance/downstream-consumption/' | relative_url }})

## Understand the boundaries

Vocabulary records concepts; taxonomy classifies them; ontology relates them. These are different products, and adopting one does not require adopting them all. None transfers normative authority to TIG.

[Understand the Semantic Model]({{ '/semantic-model/' | relative_url }}) · [Migrating from v1]({{ '/migration-v2/' | relative_url }})
