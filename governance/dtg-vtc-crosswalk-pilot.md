---
title: "DTG/VTC Crosswalk Pilot"
parent: "Operations & Evolution"
grand_parent: "Govern TIG"
---

# DTG/VTC source crosswalk pilot

This is an **exploratory, deliberately incomplete** inventory supporting [umbrella #6](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/6) and [crosswalk #8](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/8). It is not a coverage report or a normative equivalence table.

## Data, identities, and authority

- Source: `governance/coverage/dtg-vtc-pilot.json`. Three inspected source files are referenced by URL and **file blob SHA**, not entire-repository commit.
- Each candidate identifies the source and its observed designation. `concept_id` may be null when no canonical mapping has been verified.
- A matching concept label or filename does **not** prove that an external DTG/VTC concept is equivalent to TIG's definition.
- `candidate` rows may only be `review_required` or `unresolved`. `covered` is forbidden until an adjudicated row identifies an existing TIG concept.
- Neither source descriptions nor TIG mapping outputs supersede source-specification authority.

## Validation

From repository root:

```bash
python tools/validate_source_crosswalk.py
python -m unittest discover -s tests -p 'test_source_crosswalk.py' -v
```

Both commands are now included in the existing glossary CI workflow. Validation detects malformed source records, duplicate source/label entries, unknown canonical concept IDs and attempted false coverage claims. Negative fixtures assert these defects are rejected.

## Pilot limitations

The four candidate labels are not an exhaustive enumeration of any source. Therefore **no percentage can be computed from this pilot**. Source intake, licensing, hierarchy, terminology reconciliation and human semantic review remain open under #7–#9. File-not-found checks of expected slug names do not establish concept absence, since aliases and designations may map to other canonical IDs.

## Before scaling

1. Select complete, revision-pinned normative source texts and settle applicable reuse rights (#7).
2. Extract all in-scope source concepts with stable source anchors; record excluded material explicitly (#8).
3. Review exact/close/broad/narrow semantic mapping distinctions, unknowns and disagreements (#9).
4. Only then calculate coverage denominators, correct the source-of-truth terms (#10) and publish reconciled results (#12).
5. Test a bounded real consumer and decide whether broader portfolio checks are justified (#13–#14).

## Verified semantic discrepancy requiring adjudication

The existing TIG [trust-task concept](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/blob/main/glossary/terms/trust-task.yaml) describes a task performed through a trust-task protocol at ToIP stack Layer 3 (inherited ToIP terminology). In contrast, the current [DTGWG Trust Tasks canonical framework README](https://github.com/trustoverip/dtgwg-trust-tasks-spec/blob/main/README.md) describes a self-contained, transport-agnostic, JSON-based outcome document, with the specification published from the canonical `spec/` tree.

These descriptions have **different objects and boundaries**: an interaction/task in a trust-protocol layer versus a portable task description/document. Neither definition should silently overwrite the other. The pilot inventory therefore retains `review_required`; it is **not** an exact semantic match.

**Adjudication required under #9:** establish whether this is a concept specialization, an overloaded designation requiring two separately identified TIG concepts, or an intended successor meaning. Verify against the normative Trust Tasks source and the historical ToIP glossary before choosing. Preserve the existing `urn:tig:concept:trust-task` identity and compatibility until that decision is evidenced; document source versions and licensing in any remediation under #10.

## Canonical Trust Tasks source pin

The pilot now references the [canonical Trust Tasks specification header](https://github.com/trustoverip/dtgwg-trust-tasks-spec/blob/main/spec/header.md), rather than the registry's generated `SPEC.md`. That source declares **Working Draft 0.7.0** (2026-09-24). The registry-generated `SPEC.md` identifies canonical repository commit `52ba2efbf05ab1f3b9af9929dc9a8c6350a88826`; the crosswalk records this source lineage separately from the directly observed header file blob SHA. **A commit SHA in the manifest has not yet been verified against the entire referenced repository tree**; treat it as an upstream-reported pin pending retrieval at that exact revision.

The validator now checks the syntax of optional `canonical_commit` values and rejects malformed values, but it does **not** cryptographically establish that the remote revision contains the recorded blob. Remote evidence replay remains a later conformance task.

## Credential taxonomy evidence increment

The [DTG Credentials Core specification body](https://github.com/trustoverip/dtgwg-cred-spec/blob/main/spec/body.md), observed blob `d45e69bb2f4e4ba9ec84f86c6cf72351a0dc36b1`, identifies seven concrete credential subtypes in its **informative** taxonomy: VMC, VRC, VDC, VIC, VPC, VSC, VAC. These are now included as **seven additional unresolved candidate rows** in the pilot, with no assumed TIG `concept_id` mapping. VEC/VWC are profiles of VSC, not separate type rows; RCard is a VDS, not a credential subtype.

A regression fixture asserts this extracted seven-type set and that all seven remain unadjudicated. This is evidence of accurately transcribing one bounded taxonomy section, **not evidence of overall DTG/VTC glossary completeness**.

## Seven-type concept lookup checkpoint

A filename-based probe for direct canonical concept files matching the seven DTG credential type labels found an existing [delegation-credential](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/blob/main/glossary/terms/delegation-credential.yaml) concept. Its inherited generic definition is **“A credential used to perform delegation.”** It is not established as semantically identical to DTG's concrete `DelegationCredential` (VDC). The crosswalk therefore now records `urn:tig:concept:delegation-credential` with `review_required`, not `covered`.

Expected hyphenated filenames for the other six concrete credential types did not resolve. This **cannot be interpreted as a verified absence of those concepts**: existing canonical IDs, alternative designations, broader concepts, or files using different slugs may be relevant. An exhaustive designation/index scan is required before classifying them as missing.

The pilot regression tests preserve the VDC candidate and its review-required status, making accidental promotion to `covered` visible in code review.

## Complete local designation scan (not semantic conformance)

The crosswalk now has a reproducible **full canonical concept scan** rather than a handful of guessed filenames:

```bash
python tools/report_source_crosswalk_discovery.py --output /tmp/tig-crosswalk-discovery.json
```

The tool enumerates all `glossary/terms/*.yaml` concepts, indexing canonical `term`, `aliases`, and language-tagged `designations`, with case, separator, and CamelCase normalization. Every candidate receives a list of possible exact normalized designation matches. Output explicitly records `coverage_denominator: null` and `semantic_equivalence: not_established`, because this step does not compare definitions or evaluate source completeness.

CI runs the scan on every PR and uploads the JSON evidence artifact `tig-crosswalk-lexical-discovery`. This replaces the earlier filename-only lookup as a reproducible intake aid; adjudication of every lexical match, source versions and source authority still belongs to #9.
