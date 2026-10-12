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
