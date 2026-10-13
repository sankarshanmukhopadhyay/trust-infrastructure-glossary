# G0–G5 operator and acceptance runbook

**Programme:** [#28](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/28)  
**Baseline:** PRs #21–#25 (pinned sources, lexical comparisons, preliminary decisions), #27 (TIG-owned consumer checks), #29 (concept snapshot changes), #30 (Credentials terminology/transclusion admission).

## Current executable command

```bash
python -m unittest discover -s tests -p 'test_dtg_intake_readiness.py' -v
python tools/report_dtg_intake_readiness.py --output /tmp/tig-dtg-intake-readiness.json
python -m unittest discover -s tests -p 'test_concept_semantic_changes.py' -v
python tools/validate_governance_glossary.py
python tools/validate_profiles.py
python tools/validate_semantic_model.py
```

The produced report derives its counts from independently committed pinned source-tree, candidate and proposed-decision ledgers. It must show the 106 **explicit pinned directory definitions**, 17 lexical candidates, 89 without such candidates, unresolved glossary transclusions, and **null semantic, provenance and relationship coverage** while those domains lack reviewed denominators. No test legitimately converts absence of candidate labels into missing terms.

## G0: versioned source admission

1. Start at the upstream [Credentials Core Terminology](https://trustoverip.github.io/dtgwg-cred-spec/#terminology) and its pinned directory at the SHA in `governance/coverage/pinned-dtg-spec-term-trees.json`.
2. Identify the deployed HTML generation commit by the upstream documentation publishing configuration or build attestations. A live URL alone is not an authenticated commit.
3. Resolve the DTG Glossary linked from the draft, ToIP Main Glossary (`trustoverip/ctwg-main-glossary`) and General IT Glossary (candidate `trustoverip/ctwg-general-glossary`) with exact source SHAs, license, permissions, file inventory and transclusion rules. These GitHub repository names are **candidate sources**: availability does not prove which revision the spec transcluded.
4. Inventory VTI and Trust Tasks pinned directories, then identify other DTG/VTC documentation explicitly selected for this corpus. Exclude future planned specs and implementation-specific terms unless clearly admitted with separate authority class.
5. Store complete verified inventories with counts and exclusions. Never report a complete universe without documented source boundary.

## G1: four-axis crosswalk

For each admitted definition, provide the source repository, SHA, path or stable anchor, definition text or verifiable digest, primary labels, aliases, language, source authority, candidate TIG IDs and reviewer disposition. Do not assume a name match proves concept equivalence.

Coverage dimensions have distinct valid denominators:
- **Lexical:** candidate TIG designations over admitted source definitions, using documented normalization.
- **Semantic:** reviewer-adjudicated `covered` or `partial` dispositions over the *reviewed semantic denominator*. Unreviewed records remain unknown, not false.
- **Provenance:** admitted definitions with verified source references, digests and licenses over admitted definitions.
- **Relationships:** specifically identified source relationships whose endpoints and semantics have been reviewed over *admitted source relationships*. A count of source terms is not a valid relationship denominator.

Only report a numeric dimension after its denominator and verification basis are published.

## G2: human semantic adjudication

Order: six high-risk proposal cases; the remaining eleven first-pass lexical matches; all 89 unmatched-source rows (including synonym searches); newly admitted external definitions. Review the exact source definitions, applicable normative scope and TIG definitions. Decision options: `covered`, `partial`, `missing`, `not_applicable`, `indeterminate`; every decision requires references, reviewer attribution, date, assertion strength and reason. A machine regression test can validate the review record but cannot itself grant semantic approval.

For `trust-task`, compare the original TIG protocol framing with the Trust Tasks specification's bilateral-work meaning; preserve both historical semantics. Do not reassign a published concept ID just to make coverage look better.

## G3: minimal canonical remediation

After a reviewed discrepancy is approved, make one or more focused PRs that update `glossary/terms/*.yaml`, semantic overlays and prose as applicable. Preserve IDs and compatibility fields. Attach side-by-side definition/mapping rationale, alternate interpretations rejected, consent/maintainer approval and source license conditions. Regenerate all tracked artifacts and execute core schema, semantic and drift validation.

No proposed decision's `approval: pending` is permission to change canonical terms.

## G4: publication and conformance

Run repository CI, structured projections and deterministic rebuilds, link checker and GitHub Pages navigation. Consumer tests must actually parse generated JSON and resolve a named `concept_id` to its designations/provenance; file-presence checks are insufficient. Verify one ambiguous mapping is *not* consumed as `exact`. Record WCAG/a11y checks separately as tested or untested, not as implied by a successful Jekyll build.

## G5: independently maintained consumer

A TIG-controlled sample consumer validates the format, **not independent interoperation**. Admit a genuine external consumer only when a separate maintainer/implementation has operated against a pinned TIG release or commit. Capture code revision, input hashes, positive concept resolution, a rejected ambiguous match, tests/logs, environmental conditions and a reviewable report. If no such consumer is available, mark G5 **BLOCKED — independent validation missing** rather than issuing a fictitious PASS.

## Quality and decision rules

- **PASS** requires executable evidence and source/consumer attribution.
- **FAIL** means a falsifiable check demonstrated a defect; create a repair PR.
- **INDETERMINATE** means source, denominator, semantic approval or evaluator missing; keep open.
- **NOT APPLICABLE** requires an explicit corpus-boundary or design justification.
- **STOP** is permitted after completed tests and a meaningful adoption/engineering assessment; it is not a retroactive excuse to skip #6 or #14 acceptance.

### Release criteria

Do not publish a semantic release until accepted definitions and mappings, source provenance, generated contract compatibility, consumer impact and CI are documented. Documentation/test-only changes can merge without an extra release. The final report must reference exact merge SHA, CI run, Pages result and all G0–G5 evidence. Retain original issue acceptance checklist as the exit contract.
