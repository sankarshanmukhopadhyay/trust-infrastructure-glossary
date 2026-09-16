---
title: "Use TIG"
nav_order: 4
has_children: true
---

# Use TIG

TIG is designed to be referenced, integrated and governed downstream, not merely read. Start with the job you need to accomplish.

| I want to… | Use this TIG capability |
|---|---|
| Reference one stable concept | Use its canonical `concept_id` and pin the release where reproducibility matters |
| Adopt a bounded vocabulary | Use a validated vocabulary profile |
| Validate terminology or metadata | Consume the JSON/catalog/schema artifacts |
| Navigate broader/narrower classification | Consume the generated taxonomy |
| Traverse semantic relationships | Consume JSON-LD or Turtle ontology artifacts |
| Map another vocabulary | Use concept mappings with explicit mapping strength |
| Build governance or assurance tooling | Consume governance, evidence, lifecycle and control-plane metadata |
| Preserve repeatability across releases | Pin a TIG version and record the profile/subset consumed |

## Choose an integration path

### Use a bounded vocabulary

Vocabulary profiles select stable TIG concepts for a particular implementation or governance domain without redefining them.

[Explore vocabulary profiles]({{ '/profiles/' | relative_url }})

### Consume machine-readable semantics

Choose the semantic product you need: vocabulary bundle, taxonomy, ontology, profiles, inventory or quality evidence.

[View the artifact catalogue]({{ '/artifacts/' | relative_url }})

### Reference TIG downstream

Use stable concept IDs, identify the TIG release used, and preserve the local context in which a concept or profile is applied.

[Read downstream consumption guidance]({{ '/governance/downstream-consumption/' | relative_url }})

### Understand the semantic layers first

If you are unsure whether you need the vocabulary, taxonomy or ontology, start with the semantic model.

[Open the Semantic Model]({{ '/semantic-model/' | relative_url }})

## Moving from v1

Version 2 separates concepts from their designations and changes the canonical artifact names while retaining compatibility outputs during migration.

[Read the v2 migration guide]({{ '/migration-v2/' | relative_url }})

## Adoption rule of thumb

Use the **smallest TIG surface that satisfies your requirement**. Referencing a concept does not require adopting the ontology; consuming the ontology does not transfer TIG governance authority to your implementation; and a profile remains a bounded selection rather than a new definition layer.
