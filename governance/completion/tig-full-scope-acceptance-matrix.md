# TIG full-scope completion — acceptance and evidence baseline

**Date:** 2026-10-13  
**Execution issue:** [#28](../../issues/28) (repository-relative issue reference; use the canonical GitHub issue URL if rendered outside GitHub)  
**Original obligations:** [#6](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/6), [#10](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/10), [#14](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/14)  
**Evidence baseline:** merge of PR #27; do not interpret this report as full acceptance.

## Completion interpretation

The 2026-10-12 bounded verdict closed a *diagnostic*, explicitly not the full acceptance obligations. The 2026-10-13 internal consumer exercise qualifies repository-local consumption, not independent interoperation. Issue #28 now authorizes pursuit of the original scope, subject to real source authority, reviewed semantic decisions and compatibility.

A gate marked `unmet` is executable work; `blocked_authority` requires a real semantic decision, not an inferred pass. `partial` does not count as completed. Do not calculate complete semantic coverage from 17/106 lexical candidates or assign missing status to the other 89.

## Gate-by-gate traceability

| Source | Gate or original criterion | Observed evidence | Current state | Completion evidence needed |
| --- | --- | --- | --- | --- |
| #6 / #7 | G0 complete source universe / versions, provenance and authority | Three pinned Git source trees: 50 Credentials, 36 VTI, 20 Trust Tasks | partial | Source admission/selection ledger including DTG Glossary, transclusions and explicitly bounded implementation sources; license, pinned text and exclusions |
| #6 / #8 | G1 source-to-TIG mappings with four dimensions and exact denominators | 106-row source assurance ledger; 17 lexical candidates, 89 nonmatches | partial | Each selected definition examined, uncertainty and four coverage dimensions reported independently |
| #6 / #9 | G2 authoritative, source-pinned semantic adjudication | 17 preliminary comparisons; 6 high-risk proposed decisions, no approved exact mappings | blocked_authority | Source-specific reviewer decisions across admitted corpus, with rationale and rejection cases |
| #6 / #10 | G3 justified canonical corrections | No canonical changes from initial diagnostic | unmet | Adjudicated repair set or explicit per-record no-repair outcomes; diff, provenance, stable IDs, tests, generated artifacts |
| #6 / #11 | G4 validation | Crosswalk, source-integrity and semantic non-approval tests pass CI | partial | Tested drift under approved decisions, determinism, negative mappings, compatibility and Pages |
| #6 / #12 | G4 publication | Bounded assurance verdict and reader navigation | partial | Four-axis coverage and corrections, linked sources, Pages navigation, accessibility result with limitations |
| #6 / #13 | G5 independent downstream pilot | #26 / PR #27 test internal consumer journeys | unmet | Named independently maintained downstream consumer, pinned integration and positive/negative conformance run |
| #6 | Seven children and umbrella acceptance | Children closed under scoped stop; many original criteria unticked | partial | Individual gate records and independently validated completion without prior narrower scope |
| #10 | Every semantic edit source-approved | Six pending proposals, no accepted approval | blocked_authority | Reviewed decisions and source-level adjudication, or explicit no-change verdict per finding |
| #10 | IDs and v1 compatibility preserved | 617 concept baseline and no canonical mutation | verified_baseline_only | Per-remediation regression evidence and migration check |
| #10 | Tests, provenance, relationships and regen | Existing checks, no repairs exercised | unmet | Actual semantic correction regressions, build and CI evidence |
| #14 | Nine improvements dispositioned | Issue #14 priority table | partial | Reconcile each priority to current evidence and actual G5 outcome |
| #14 | Inspect #4/#5 baseline | #4 navigation and #5 semantics implemented | verified_baseline_only | Preserve proven functionality in semantic changes |
| #14 | Portfolio expansion based on #13 | Original #13 independent pilot not performed | unmet | Decision following actual G5 results |
| #14 | Concept versioning feasibility | Stable IDs, statuses and release version exist | partial | Three scenario analysis and tested history/diff behavior; see [versioning review](tig-concept-versioning-feasibility.md) |
| #14 | Follow-on implementation and closure | Scope closed as bounded diagnostic | unmet | Full outcome with open blocker disclosure and issue/PR evidence |

## Work sequence

1. **Source admission / G0:** inventory canonical and supplemental sources; assert repository-owned authority classifications; verify digests and attribution.
2. **Complete crosswalk / G1:** account for all selected source terms; distinguish lexical similarity, overlap, specialization, and absent concept.
3. **Semantic adjudication / G2:** first the six high-risk records, then other 11 lexical comparisons, then the 89 nonmatches, then any newly admitted source records. Do not commit canonical semantic mutations from a pending proposal.
4. **Remediation / G3:** implement accepted decisions as compatible concept/mapping/provenance changes with tests and regenerated outputs.
5. **G4 + G5:** publish four-axis evidence, validate machine and human consumption, and execute an actual independently maintained consumer pilot.
6. **#14 roadmap closure:** complete concept history feasibility and nine-priority disposition after G5; implement demonstrated defects only.
7. **Acceptance:** attach SHA-specific CI, Pages, external consumer and exact source evidence to #28, then decide semantic-version and publication actions.

## Falsification and safety conditions

- An unresolved or review-required lexical match asserted as `exact` is failure.
- A missing lexical match automatically counted as a missing concept is failure.
- A new definition overwriting a published concept's meaning under the existing ID is failure.
- A passed local fixture represented as an independent implementation is failure.
- Missing, inaccessible, outdated, or unlicensed source evidence silently counted as validated is failure.
- A green CI run without source-specific semantic approval cannot complete G2.
- A released semantic change with untested v1/v2 compatibility cannot complete G3.

## Explicit compatibility / governance boundaries

TIG controls its own editorial semantics. Source specifications remain authoritative for their terminology. A maintainer may approve a TIG representation of a source concept but cannot thereby change a source specification. Treat source mapping approval and TIG publication approval as separate evidence. Retain OWFa/attribution obligations, existing identifiers, v1 `term`/`aliases`, and deterministic projection.

## Completion decision

**IN PROGRESS** — #28 restores the original criteria. This document is an acceptance baseline, not evidence that the gates have passed.
