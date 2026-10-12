# DTG/VTC terminology assurance: bounded baseline and disposition

**Assessment date:** 2026-10-12  
**Status:** Completed *bounded diagnostic*; **not** an assertion of semantic coverage, specification conformance, or upstream terminology authority.  
**Decision:** Publish and maintain this source-scoped assurance snapshot. Do not expand TIG automatically, modify stable concept IDs, or publish a semantic-completeness score without accepted source comparisons.

## Executive conclusion

The Trust Infrastructure Glossary (TIG) has an established governed corpus and functioning machine-verifiable source intake, but the evidence does **not** substantiate a claim that TIG semantically covers the terminology of the DTG/VTC specification portfolio. The checked source slice contains **106 explicit definitions** in **106 definition files** across three pinned, canonical specification repositories. Reproducible designation matching identified TIG candidate concepts for **17** and no lexical candidate for **89**. **Those are lexical lookup results, not the proportion of semantically covered or missing concepts.**

The assessed 17 candidates contain **five material divergences, six context-specific narrowings, five scope-overlap candidates, and one ambiguous mapping**. Six particularly consequential cases have machine-readable hold/non-equivalence proposals. The remaining 89 are evidence gaps for definition-level comparison, *not* automatically 89 TIG omissions.

**Assurance finding:** `INDETERMINATE` for semantic coverage of the admitted three-spec slice. **No confirmed semantic-completeness percentage.** This is a valid negative/insufficient-evidence assessment outcome, not a CI failure or a reason to generate further infrastructure by default.

## Source boundary and verification

| Canonical repository | Pinned revision | Term files | Explicit definitions |
| --- | --- | ---: | ---: |
| [DTG Credentials Core](https://github.com/trustoverip/dtgwg-cred-spec/tree/4088056a15f6e74847eb422e1c2bae33684272ea/spec/terms-definitions) | `4088056a15f6e74847eb422e1c2bae33684272ea` | 50 | 50 |
| [Verifiable Trust Infrastructure](https://github.com/trustoverip/dtgwg-vti-spec/tree/dc1ec07d42ec5c0054037795c06dbead608fbc5b/spec/terms-definitions) | `dc1ec07d42ec5c0054037795c06dbead608fbc5b` | 36 | 36 |
| [Trust Tasks](https://github.com/trustoverip/dtgwg-trust-tasks-spec/tree/bf667f3e8506b7fb2c3e96665b7060e2ebaad806/spec/terms-definitions) | `bf667f3e8506b7fb2c3e96665b7060e2ebaad806` | 20 | 20 |
| **Total** | | **106** | **106** |

The source tree manifest `governance/coverage/pinned-dtg-spec-term-trees.json` records exact Git blob identities. The dedicated `.github/workflows/pinned-dtg-terminology.yml` verifies checkout commit hashes, complete in-scope Git trees, declared source file blobs, extracted Spec-Up-T definitions and source-to-TIG lexical discovery. Its `tig-pinned-dtg-terminology` artifact includes the extracted definitions, candidate crosswalk and **all-106-record source assurance ledger**.

CI provenance:
- [Source extraction / lexical crosswalk](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/actions/runs/38202631769): passed; 17/106 lexical candidates.
- [Initial semantic review](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/actions/runs/38203029894): passed.
- [Consolidated ledger](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/actions/runs/38204062983): passed.

The observed source slice excludes external DTG Glossary transclusions, definitions outside these three terminology directories, and other DTG/VTC, implementation and portfolio sources. It cannot serve as a complete DTG/VTC universe denominator. Licensing/source-precedence admission for any future external corpus must be explicit.

## Results and independent findings

| Evidence class | Result | Allowed conclusion |
| --- | ---: | --- |
| Source definitions explicitly inventoried | 106 | Complete for the three pinned `spec/terms-definitions` directories |
| TIG lexical candidate discovered | 17 | Definition-level semantic review warranted |
| No TIG lexical candidate detected | 89 | **Unknown** TIG coverage; no missing-concept inference |
| Material semantic divergences among 17 | 5 | Exact correspondence **not supported** for these comparisons |
| Context-specific narrowing among 17 | 6 | TIG meaning may be broader; requires relation judgment |
| Possible scope overlap among 17 | 5 | Non-equivalence and equivalence both remain unproved |
| Ambiguous mapping among 17 | 1 | Hold multiple plausible candidates |
| High-risk decision proposals | 6 | Pending authoritative semantic acceptance |
| Approved semantic mappings | 0 | Semantic completeness is **indeterminate**, not 0% |

### Examples that directly matter

- **Trust Task:** [VTI](https://github.com/trustoverip/dtgwg-vti-spec/blob/dc1ec07d42ec5c0054037795c06dbead608fbc5b/spec/terms-definitions/trust_task.md) defines a versioned, node-exposed operation; [Trust Tasks](https://github.com/trustoverip/dtgwg-trust-tasks-spec/blob/bf667f3e8506b7fb2c3e96665b7060e2ebaad806/spec/terms-definitions/trust_task.md) defines bilateral verifiable work; the existing TIG `trust-task` retains an earlier Layer-3 task-protocol interpretation. Reusing one ID for all three would silently change meaning.
- **Trust context:** [VTI](https://github.com/trustoverip/dtgwg-vti-spec/blob/dc1ec07d42ec5c0054037795c06dbead608fbc5b/spec/terms-definitions/trust_context.md) identifies an isolation and authority partition; TIG describes the context of a trust decision. They must not be asserted equivalent.
- **Delegate versus delegation:** VTI identifies a subject acting for another, whereas TIG's `delegation` describes the authorizing act. A similar stem is not an identity of concepts.
- **Subject:** The access-control subject in VTI and a credential-claim subject in TIG are different contextual uses; an undifferentiated exact mapping would mislead implementers.
- **Proof:** Trust Tasks describes an optional W3C Data Integrity Proof object; TIG has distinct `proof` and `data-integrity-proof` concepts. A context-sensitive mapping needs a specific decision.
- **VDC:** A source-defined bounded, revocable appointment to act in another's name, expressly distinguished from authority, cannot automatically be mapped to TIG's generic delegation-credential concept without constraints.

Detailed evidence: `governance/coverage/dtg-semantic-first-pass.json`, `governance/coverage/dtg-semantic-decision-proposals.json` and `governance/dtg-semantic-comparison-first-pass.md`.

## Engineering and governance disposition

1. **Accept the source-scoped diagnostic as the deliverable for the bounded baseline work.** Its purpose is to determine what can be substantiated now, not to impose 106 new TIG definitions.
2. **No canonical semantic mutation is approved from the evidence.** Stable TIG `concept_id` values, historical meaning, and existing compatibility projections remain unchanged.
3. **No automatic release or coverage score.** This documentation/evidence baseline does not by itself warrant a semantic version increment or claim of DTG-wide conformance.
4. **Stop building supplementary intake or review tools.** The source extraction, lexical discovery, evidence ledger and CI are adequate for this scoped diagnostic. Further work must begin with a specific reviewed semantic decision or downstream consumer requirement.
5. **Separate substantive residuals:** adjudication of the six high-risk cases, evaluation of the other 11 matches, review of the 89 nonmatches, external glossary admission, and one named consumer test. These are candidate future tranches requiring evidence and utility, **not reasons to reopen the completed diagnostic**.

## Closeout and provenance

Related umbrella [#6](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/6) and work items [#7](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/7)–[#14](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/14) contain the detailed audit history. Source evidence and tests were built across PRs #15, #16, #18–#24; the report is the **bounded decision record**, not a claim that every original ambition has been met.

**Final decision:** The bounded assessment may be marked complete when this document is merged and validated. Broader semantic convergence or implementation is not completed and must be tracked explicitly if resumed.
