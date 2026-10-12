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
