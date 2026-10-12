---
title: "DTG Semantic Comparison — First Pass"
parent: "Operations & Evolution"
grand_parent: "Govern TIG"
---

# DTG/VTC semantic comparison: first-pass evidence

**Status:** preliminary reviewer analysis; no approved exact/close/broad/narrow assertions and no changes to canonical TIG concepts.

## Reproducible source scope

The [pinned source manifest](coverage/pinned-dtg-spec-term-trees.json) and [pinned source workflow](../.github/workflows/pinned-dtg-terminology.yml) verify 106 explicit definitions in 106 term files from Credentials Core (50), VTI (36) and Trust Tasks (20). The workflow produced **17 records with lexical TIG candidates** and **89 records with no candidate designation match**. This is a name-match diagnostic, **not** semantic coverage (17/106 must not be reported as semantic completeness).

The [machine-readable first-pass register](coverage/dtg-semantic-first-pass.json) assesses the **17 candidates only** and requires semantic approval before a mapping can be published. Every source file and revision is independently located in the pinned tree manifest. The review classes are exploratory, not mapping predicates:

| Preliminary class | Count | Meaning |
|---|---:|---|
| `material_divergence` | 5 | Same/similar terminology denotes different objects or boundaries |
| `contextual_narrowing` | 6 | A spec-specific meaning narrows or constrains a more general TIG concept |
| `candidate_scope_overlap` | 5 | Likely conceptual overlap; exact semantic relationship not proven |
| `ambiguous_mapping` | 1 | Multiple TIG lexical candidates with materially different scopes |

## High-impact disagreements

**Trust Task:** [Trust Tasks](https://github.com/trustoverip/dtgwg-trust-tasks-spec/blob/bf667f3e8506b7fb2c3e96665b7060e2ebaad806/spec/terms-definitions/trust_task.md) defines bilateral verifiable work, [VTI](https://github.com/trustoverip/dtgwg-vti-spec/blob/dc1ec07d42ec5c0054037795c06dbead608fbc5b/spec/terms-definitions/trust_task.md) defines a versioned node-exposed operation, and TIG's existing `trust-task` retains a ToIP Layer-3 protocol definition. These are overlapping but **not silently interchangeable**. Resolve whether to introduce discrete concepts, context-specific designations or semantic relations while preserving the existing stable TIG concept ID.

**Trust context:** [VTI](https://github.com/trustoverip/dtgwg-vti-spec/blob/dc1ec07d42ec5c0054037795c06dbead608fbc5b/spec/terms-definitions/trust_context.md) describes a nested partition for key and authority isolation; TIG describes a trust decision context. This is not an exact mapping.

**Delegate versus delegation:** [VTI](https://github.com/trustoverip/dtgwg-vti-spec/blob/dc1ec07d42ec5c0054037795c06dbead608fbc5b/spec/terms-definitions/delegate.md) names the acting subject; TIG `delegation` defines an authorizing act. A lexical stemming match is insufficient.

**Subject:** [VTI](https://github.com/trustoverip/dtgwg-vti-spec/blob/dc1ec07d42ec5c0054037795c06dbead608fbc5b/spec/terms-definitions/subject.md) identifies a principal in an access-control entry, versus TIG's credential claim subject.

**Proof:** [Trust Tasks](https://github.com/trustoverip/dtgwg-trust-tasks-spec/blob/bf667f3e8506b7fb2c3e96665b7060e2ebaad806/spec/terms-definitions/proof.md) means a Data Integrity Proof attached to a task document. TIG has both a generic `proof` and a `data-integrity-proof` concept; selecting the mapping requires reviewed context.

**Recognition and registry:** VTI specifies nontransitive cross-community recognition with status and authority mapping checks, and expressly distinguishes a registry lookup from proof of current authority. Those limitations must not disappear under a broad TIG lexical match.

## Disposition and next gate

- **No canonical term changes** are appropriate solely from the 17 lexical findings.
- **89 unmatched labels are not 89 missing concepts**. Alternative taxonomies, source-specific constructs and out-of-scope terms need individual classification.
- Admit separately owned DTG Glossary terms, externally transcluded definitions and relevant VTC implementation terminology before asserting portfolio-wide completeness.
- Under issue #9, decide candidate mappings with a reviewer-approved semantic relation and evidence; under #10, add or update only justified canonical concepts, with generated outputs and compatibility tests.
- Validate one named downstream consumer under #13 and publish both positive and negative conformance examples before closing umbrella #6.

The included CI regression tests reject treating this first-pass register as approved semantic mappings.
