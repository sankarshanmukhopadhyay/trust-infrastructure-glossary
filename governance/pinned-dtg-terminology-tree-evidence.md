---
title: "Pinned DTG Terminology Tree Evidence"
parent: "Operations & Evolution"
grand_parent: "Govern TIG"
---

# Complete pinned directory evidence for selected DTG specifications

The file [`coverage/pinned-dtg-spec-term-trees.json`](coverage/pinned-dtg-spec-term-trees.json) records **untruncated Git trees** for the following source commits:

| Repository | Commit | In-scope term files |
|---|---|---:|
| `trustoverip/dtgwg-cred-spec` | `4088056a15f6e74847eb422e1c2bae33684272ea` | 50 |
| `trustoverip/dtgwg-vti-spec` | `dc1ec07d42ec5c0054037795c06dbead608fbc5b` | 36 |
| `trustoverip/dtgwg-trust-tasks-spec` | `bf667f3e8506b7fb2c3e96665b7060e2ebaad806` | 20 |

These **106 Markdown files** are the entire `spec/terms-definitions/` *directory contents* at those commits, verified from the Git trees; they are not necessarily the entire terminology universe of DTG or VTC.

The [pinned terminology workflow](../.github/workflows/pinned-dtg-terminology.yml) checks out each fixed revision, verifies `git rev-parse HEAD`, compares every tracked terminology file's Git blob SHA to the checked-in manifest, and extracts explicit `[[def: ...]]` definitions. Results are uploaded as `tig-pinned-dtg-terminology`. This build fails closed on a mismatched commit, added/removed term file, changed file blob, or zero extracted definitions.

**Important limits:** Normative versus informative authority is decided by each source, not by TIG. Referenced external glossary definitions and definitions embedded outside `spec/terms-definitions/` are excluded. The coverage denominator for the entire DTG/VTC ecosystem remains undefined. These extraction records require semantic adjudication against TIG before exact/close/broad/narrow mapping claims or concept edits.

Re-run the workflow after any deliberate pinned source revision update and review both the manifest and evidence differences. Prefer to keep a historical release copy of accepted source inventories when establishing later time-as-of comparisons.

## Authenticated, source-scoped lexical reconciliation

The same CI workflow also uses `tools/reconcile_pinned_dtg_terminology.py` to compare each extracted primary term **and all Spec-Up-T aliases** against the canonical TIG concept `term`, `aliases`, and `designations` indexes. The artifact `pinned-lexical-crosswalk.json` reports per-source file evidence, lexical candidate IDs, and an exact **scoped source-definition count**.

`source_definition_denominator` is meaningful **only for the explicit definitions in these three pinned directories**, not for DTG/VTC overall. `semantic_coverage_percentage` and `semantic_coverage_denominator` are intentionally `null`: every row remains `review_required`, even when an exact designation matches, until actual definition comparison and adjudication. CI tests that aliases match without conferring semantic authority.
