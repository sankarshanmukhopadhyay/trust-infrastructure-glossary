---
title: "Provenance & Authority"
parent: "Semantic Model"
nav_order: 4
permalink: /semantic-model/provenance/
---

# Provenance & Authority

TIG distinguishes **semantic representation** from **normative authority**.

A source repository can be authoritative for its own specification while TIG represents a portable concept or relationship derived from that source. TIG provenance records where material came from and how it was incorporated; it does not automatically transfer source authority into TIG or TIG authority downstream.

## Governing rule

Generated taxonomy and ontology assertions have `descriptive-reference` effect. They help humans and systems navigate meaning, classification and relationships. They do not silently create requirements for an implementation, registry, agent, protocol or policy engine.

## Evidence carried by TIG

Depending on the concept or edge, TIG can preserve:

- source corpus and source citation;
- provenance classification (`adopted`, `adapted`, `locally_defined`, `mapped`);
- originating concept artifact;
- governed taxonomy assertion provenance;
- editorial status and review state;
- explicit evidence that an inherited reference could not be projected because its target is not canonical.

## Source of truth

- Concept-local semantics: `glossary/terms/*.yaml`
- Reviewed additive hierarchy assertions: `governance/taxonomy-relations.yaml`
- Semantic projection contract: `governance/semantic-model.yaml`
- Generated graph views: publication evidence only

For authoring, intake and change-control rules, use [Govern TIG]({{ '/governance/' | relative_url }}).
