---
title: "Upstream DTG Terminology Discovery Evidence"
parent: "Operations & Evolution"
grand_parent: "Govern TIG"
---

# Upstream terminology discovery checkpoint

At the inspected repository revisions on 2026-10-12, GitHub code search for explicit Spec-Up-T `[[def:` markers found file paths in three canonical repositories: **50** Credentials Core, **36** VTI, and **20** Trust Tasks. The machine-readable manifest is [`governance/coverage/discovered-dtg-spec-term-files.json`](coverage/discovered-dtg-spec-term-files.json).

These **106 discovered paths are not an asserted exhaustive set of defined concepts**. Some files can contain multiple definitions; some may have no conventional marker, be unindexed, or represent references rather than source-owned definitions. The `search_commit` is the revision surfaced by GitHub search, not an independently authenticated complete tree export. Each directory still needs a complete revision-pinned tree listing plus actual extractor execution and source licensing review before #7/#8 can close.

## Directly inspected source findings

- Credentials Core defines `VMC`, `VRC`, `VDC`, `VAC` with comma-separated preferred designations and aliases. The first identifier is the Spec-Up-T primary label. The source defines VDC as a bounded, revocable appointment to act in another's name, explicitly distinguishing delegation from authority.
- The VTI `trust_task.md` defines a canonically versioned node-exposed operation; the Trust Tasks framework `trust_task.md` defines a unit of verifiable work exchanged through bilateral documents. This is a real same-label/different-definition review target rather than a justified exact mapping.
- Credentials Core and VTI both define VTA and VTC, but scope and authority differ; mapping decisions must preserve provenance and specification context.
- The source extractor previously treated all `[[def: primary, alias1, alias2]]` values as one label. This revision separates the primary designation from its aliases and tests the behavior.

## Reproduce and adjudicate

Run `python tools/extract_spec_up_t_terms.py --source-root PATH --repository REPO --commit SHA` against an **independently verified checkout** of each listed repository. Compare the output with the full upstream Git tree, record source definition hashes, licensing, exclusions and exact source anchors, and append decisions under #9. Do not publish overall coverage percentages until the source denominator is complete.

**Disposition:** concrete external evidence discovery delivered; source admission, exhaustive reconciliation, and adjudication remain open.
