# Concept-level versioning and semantic-change audit feasibility

**Date:** 2026-10-13  
**Linked issue:** [#28](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/28)  
**Decision state:** feasibility review; implementation requirements identified, not yet released.

## Question

Can an adopter distinguish a harmless designation change from a material change of meaning while retaining the same stable TIG `concept_id`, or determine what a concept meant at a previous published release?

This is separate from source-version pinning: a source-specification commit is evidence about the source, not a version of a TIG concept.

## Inspected contracts

- `schemas/governance-term.schema.json`: `schema_version: "2.0"`, immutable-in-practice `concept_id`, language-tagged `designations`, `editorial.status` values `proposed`, `draft`, `review-needed`, `stable`, `deprecated`. The schema permits additional top-level properties but defines **no normative semantic-change record** or per-concept revision field.
- `governance/term-authoring-guide.md`: changing a preferred designation does not justify renaming a concept ID; `exact` mappings require interchangeability.
- `governance/repository-operating-model.md`: canonical semantics live in `glossary/terms/*.yaml`, while `_terms/` and `generated/` are derived; published identifiers must not be repurposed.
- `MIGRATION_v2.md`: consumers should pin a TIG release, key concepts by `concept_id` and preserve `term`/`aliases` during v1 migration.
- `RELEASE_NOTES_v2.2.0.md`: v2.2.0 is additive; profiles and concept IDs remain stable; taxonomy/ontology projections are descriptive.
- Git history/tags provide repository-level historical snapshots, but a change record linking **concept + previous and new semantic signatures + review authority + compatibility disposition** is not presently a published, machine-verifiable contract.

## Three falsifiable semantic-change scenarios

| Scenario | Expected stable-ID behavior | Available evidence | Gap / necessary control |
| --- | --- | --- | --- |
| A. Preferred English label changes, definition unchanged | Preserve `concept_id`; preferred designation changes, old label may remain alternative for lookup; no new concept | Before/after Git and release tags can be compared; schema requires designations | Need a repeatable audit that classifies designation-only change without reporting semantic drift; consumers must retain stable-ID round trip |
| B. Definition changes material scope (e.g. broadening or narrowing `trust-task`) | Must **not** silently reuse ID for a different meaning; either clarify same concept compatibly under review or introduce a distinct concept with relationship and provenance | Repository history retains blobs and CI validates current structure | No automated classification of material semantic vs editorial changes; no explicit consumer-facing effect and migration decision |
| C. Concept withdrawn/deprecated or replaced by successor | Retain historical ID and source attribution; mark status; successor needs distinct stable ID where meaning differs; historical release resolution should remain possible | `editorial.status: deprecated` exists; Git tags retain historical source | No governed, durable replacement link or temporal meaning record required by schema; adding status alone does not explain what changed or when |

## Feasibility judgment

**Current release tags and repository provenance are sufficient to reconstruct a historical snapshot when the exact version/commit is retained and accessible.** They are **not sufficient, by themselves, for a machine consumer to detect material semantic change of one concept reliably**. A plain text diff does not adjudicate whether meaning changed; editorial status is state, not a history of transitions.

**Recommended next increment:** implement a deterministic **semantic-change report** comparing two explicit repository snapshots (tags or SHAs) and emitting conservative classes: `unchanged`, `designation_changed`, `semantic_review_required`, `new_concept`, `concept_missing_from_target`, `editorial_status_changed`. Treat changed definitions, mappings, provenance, or typed relations as review-required, not as a conclusive breaking change. Record both exact snapshot SHA/version and affected IDs; preserve all existing JSON/YAML/RDF contracts. Do not add required per-concept version fields merely to satisfy this review.

### Minimum conformance tests for that increment

1. Same corpus vs itself gives zero changed IDs and deterministic output.
2. Label-only edit yields a designation change and preserves the concept ID.
3. Material definition change yields `semantic_review_required` and no automatic approval or rewrite.
4. A disappeared canonical ID is reported as a compatibility event, never treated as harmless removal.
5. Deprecation and a separately introduced successor are reported as distinct changes; nothing is implicitly redirected.
6. Identical inputs yield byte-identical canonical JSON; malformed/missing snapshots fail closed.
7. v1-compatible `term` and `aliases` are checked on material changes.

## Reproducible usage

The additive comparator is implemented by `tools/report_concept_semantic_changes.py`. Supply **two separately checked out** repository revisions with their canonical `glossary/terms/` paths; the script does not itself verify that a directory equals a declared Git ref. Operators must separately record `git rev-parse HEAD` for each checkout and retain that evidence.

```bash
# From a clean TIG checkout with the corresponding releases/SHAs checked out
python tools/report_concept_semantic_changes.py \\
  --before /path/to/old-checkout/glossary/terms \\
  --after /path/to/new-checkout/glossary/terms \\
  --before-ref v2.2.0 \\
  --after-ref COMMIT_SHA_OF_NEW_CHECKOUT \\
  --output /tmp/tig-semantic-change-report.json

python -m unittest discover -s tests -p 'test_concept_semantic_changes.py' -v
```

The comparison includes only direct `*.yaml` artifacts in each directory; it emits sorted concept-ID rows, detected structural-change classes and an explicit `semantic_approval: not_assessed`. This is a **candidate review report**, never a semantic-change verdict or an authentication of snapshot provenance. Pin source revisions outside the tool and do not place this output in the canonical glossary authority layer.

## Why not add a new concept-version field immediately?

A monotonically incremented `concept_version` would imply that the project can authoritatively classify every intervening historical semantic change. At present no stable semantics for such a field, version increment policy, or audited history exist. Introducing it now would create a false assurance layer. First establish a falsifiable two-snapshot diff and consumer evidence. Then consider a reviewed change ledger with authority/decision timestamps if the independent consumer pilot demonstrates demand.

## Authority, compatibility, and redress

The report may identify candidates for review, but only TIG maintainers can approve changes to TIG semantics. Original source specifications remain authoritative for their definitions. Git history is technical provenance, not automatic semantic approval. If a published label or mapping is disputed, retain the historical artifact and document a correction/supersession rather than rewriting previous release claims.

## Current conclusion

**Feasibility decision: an additive two-snapshot comparison has been implemented with bounded unit and negative fixtures; complete deployment/CI assurance and independent consumer utility require verification.** #14's request for three concrete scenarios and a feasibility judgment is addressed here, but the original expanded mandate remains open until the tests, actual diff report and consumer results are integrated.
