# TIG consumer qualification report

**Assessment date:** 2026-10-13  
**Issue:** #26  
**Status:** bounded TIG-owned adoption qualification completed for current artifacts.  
**Decision:** stop further TIG infrastructure work unless a named adopter failure, broken consumer path, approved semantic decision, or machine-readable artifact regression is identified.

## Executive conclusion

The follow-on work left open by #14 is not another semantic-expansion tranche. It is an adoption and consumption check: can a human reader and a machine consumer use current TIG artifacts without confusing lexical similarity with semantic approval?

This tranche qualifies two bounded journeys:

1. **Human concept navigation:** a reader can start from the README/site information architecture, navigate to a concept, inspect provenance and relationship posture, and see the DTG/VTC bounded-assurance limitation.
2. **Machine stable-ID round trip:** a machine consumer can resolve a stable `concept_id`, inspect designations and provenance, locate generated machine-readable products, and preserve unresolved semantic states from the DTG/VTC evidence registers.

The result is **PASS with limits**. TIG already exposes enough repository and generated-artifact structure to support these journeys. The material risk is not missing infrastructure; it is accidental over-claiming. The new validation therefore protects the consumer promise that unresolved semantic candidates remain unresolved.

## Authority boundary

TIG remains descriptive and non-normative. Source specifications remain authoritative for source-specific meanings. A `concept_id` identifies a TIG concept; it does not prove exact equivalence with an external source term. Lexical match, filename match or similar prose is only evidence for review.

## Evidence package

| Artifact | Purpose |
| --- | --- |
| `governance/adoption/tig-consumer-qualification-2026-10-13.json` | Machine-readable journey observations, negative cases and final decision. |
| `tools/validate_tig_consumer_qualification.py` | Validates consumer evidence, stable-ID round trip, machine product presence and unresolved semantic guardrails. |
| `tests/test_tig_consumer_qualification.py` | Regression tests for the consumer qualification and semantic non-approval negative cases. |
| `.github/workflows/validate-governance-glossary.yml` | Runs the qualification validator and tests in CI. |

## Journey 1 — human concept navigation

**Question:** Can a reader locate a concept, its designations, provenance, relationships and usage limits without treating lexical similarity as semantic authority?

### Observed path

1. `README.md` presents TIG as governed semantic infrastructure and states that the authoritative unit is a concept, not a string label.
2. `explore/index.md` and generated concept pages provide reader-facing navigation.
3. `_terms/trust-task.md` exists as the generated page for the deliberately risky `trust-task` example.
4. `glossary/terms/trust-task.yaml` retains stable concept identity, designations, provenance, editorial state and empty approved mapping arrays.
5. `governance/dtg-vtc-bounded-assurance-verdict-2026-10-12.md` explicitly reports DTG/VTC semantic coverage as `INDETERMINATE` and rejects 89 nonmatches as confirmed missing concepts.

**Result:** PASS.

### Interpretation

The reader can find and cite a concept while seeing that external source alignment is not automatically approved. No new graph UI, export format or semantic service is justified by this journey.

## Journey 2 — machine stable-ID round trip

**Question:** Can a machine consumer resolve a stable `concept_id`, its designations, provenance and generated representation while preserving unresolved semantic states?

### Observed path

1. `glossary/terms/trust-task.yaml` exposes `urn:tig:concept:trust-task`, designations, provenance and editorial metadata.
2. Generated machine-readable products exist under `generated/json/` and `generated/rdf/`.
3. `governance/coverage/dtg-semantic-first-pass.json` keeps all first-pass candidates in `requires_semantic_approval` with `mapping_assertion: null`.
4. `governance/coverage/dtg-semantic-decision-proposals.json` keeps high-risk proposals at `approval: pending` and `canonical_change_allowed: false`.

**Result:** PASS.

### Interpretation

A machine consumer has enough structure to consume TIG artifacts without inferring unapproved semantic equivalence. The qualification validates the current shape instead of expanding it.

## Negative cases

| Case | Guard | Result |
| --- | --- | --- |
| Ambiguous `Trust Task` lexical candidate | First-pass semantic comparison must remain approval-required and must not carry a mapping assertion. | PASS |
| High-risk semantic proposals | Pending proposals must not authorize canonical mutation. | PASS |
| 89 unmatched DTG/VTC labels | Nonmatch evidence must remain an evidence gap, not a confirmed missing-concept list. | PASS |

## Acceptance disposition for #26

| Acceptance criterion | Disposition |
| --- | --- |
| Two concrete TIG consumer journeys are documented and reproducible. | Completed through JSON evidence and this report. |
| Baseline/final evidence contains paths and expected vs observed behavior. | Completed in `tig-consumer-qualification-2026-10-13.json`. |
| Negative cases demonstrate that unresolved or ambiguous semantic mappings are not treated as approved. | Completed in validator and tests. |
| TIG-owned defects are fixed or dispositioned. | No consumer-path defect found; guardrail validation added. |
| Stable `concept_id` values and compatibility outputs remain unchanged. | Preserved; no canonical term files were modified. |
| Public navigation/README and generated artifacts are validated and synchronized. | Validation added; README linked to the qualification report. |
| CI is green; PRs, commits, test logs and report are linked. | Pending PR CI at merge review. |
| Issue concludes with stop/further bounded work decision. | Stop decision recorded here and in machine-readable evidence. |

## Residual limits

This is not a full accessibility audit, not an independent downstream implementation, not a semantic approval of DTG/VTC terms and not a release-worthy semantic change. It is a bounded TIG-owned adoption qualification.

Further work is warranted only if one of the following occurs:

- a named adopter cannot resolve or consume TIG artifacts;
- generated public navigation breaks;
- an approved semantic decision requires a canonical compatibility-preserving edit;
- machine-readable outputs regress or become inconsistent with canonical concept sources.

## Release note

No release is warranted. This is test and documentation hardening around current adoption surfaces. No concept identity, schema, profile, generated semantic contract or public authority posture changes.
