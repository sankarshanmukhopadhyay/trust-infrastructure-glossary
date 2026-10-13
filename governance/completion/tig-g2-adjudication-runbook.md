# G2 source-specific semantic decision register

[Machine-readable pending adjudications](../coverage/dtg-g2-adjudications.json) cover **all 17 initially lexically matched** definitions from the three SHA-pinned DTG specification term directories. Six records link existing high-risk proposals. This is a **decision register**, not an approved mapping catalogue.

## Review workflow

1. Open the pinned source definition using the record's `source_repository`, `source_commit`, and `source_path`. Read the full definition and surrounding specification context.
2. Compare each proposed TIG concept's current definition, provenance, authority scope and compatibility requirements. Review synonym candidates and competing interpretations.
3. Record `disposition` as `covered`, `partial`, `missing`, `not_applicable` or `indeterminate`; record mapping strength where applicable. An `exact` assertion is permissible only for a genuinely covered definition.
4. Supply independently inspectable `source_definition_evidence`, rationale, reviewer identity, review date, compatibility assessment and source-license review.
5. Set `approval_state: approved` only following an actual TIG maintainer editorial decision. Update `approved_count` and `review_required_count` to match; do not backfill identity or approval from machine output.
6. If remediation is justified, open a separate source- and review-linked PR. Preserve published concept IDs and v1/v2 compatibility.

The default for every new record is `pending` with `canonical_change_allowed: false`. Schema validation fails when an unapproved case is silently assigned a coverage disposition or an incompatible mapping. Tests include negative approval/coverage fixtures.

## Validate

```bash
python tools/validate_g2_adjudications.py --verify
python -m unittest discover -s tests -p 'test_g2_adjudication_register.py' -v
```

To regenerate a **blank** register from the current first-pass source manifest (this overwrites decisions, so only do it before adjudication):

```bash
python tools/validate_g2_adjudications.py --output /tmp/dtg-g2-proposed-blank.json
```

## Boundaries

This register accounts for **17/106** initial lexical candidate rows only. The other **89/106** source definitions require separate semantic assessment even though no lexical candidate was found. The 749 ToIP source definitions from subsequent external extraction remain candidate admission material, not automatically part of the DTG/VTC coverage denominator. Full G0 authority, four-axis G1 measurement, G3 remediation, and independently maintained G5 consumer evidence are still unresolved.

[Six source-grounded high-risk comparison dossiers](../completion/tig-high-risk-semantic-adjudication-packet.md) remain recommendations awaiting maintainer review, not approved editorial actions.
