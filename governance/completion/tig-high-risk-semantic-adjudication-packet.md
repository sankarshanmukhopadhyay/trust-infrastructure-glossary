# G2 — source-grounded high-risk semantic adjudication packet

**Programme:** [#28](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/28) · **Cases:** DTG-SEM-001–006 · **Prepared:** 2026-10-13

**Review state: READY FOR MAINTAINER ADJUDICATION, NOT APPROVED.** This packet compares pinned upstream *actual definitions*, not just case labels. The six cases are all presently `approval: pending`. No exact TIG mappings or canonical edits are authorized.

## Decision matrix

| Case | Authenticated source distinction | Current TIG distinction | Proposed safe disposition | Potential remediation if approved |
| --- | --- | --- | --- | --- |
| DTG-SEM-001 `proof` | Trust Tasks: optional **W3C Data Integrity Proof** object attached to a Trust Task document | `proof`: a wider cryptographic proof object; `data-integrity-proof`: cryptographic document protection | **partial/ambiguous**: do not map to generic `proof` as exact; narrower candidate `data-integrity-proof` still needs source-context review | Add source-qualified mapping to the proper concept only if reviewed; otherwise keep source use unmapped |
| DTG-SEM-002 `Trust Task` | Trust Tasks: **bilateral unit of verifiable work**, with at most one issuer and recipient per task document and `threadId` linking multi-party flows | Legacy TIG `trust-task`: activity performed by a Layer-3 trust-task protocol | **distinct meaning**: reject exact and preserve legacy concept | Consider a distinct DTG verifiable work/task concept with new stable ID only if editorially admitted |
| DTG-SEM-003 `delegate` | VTI: the **acting subject**, represented through an access control entry; cannot exceed delegator authority | TIG `delegation`: **act** of authorizing another party, with delegation as a process | **distinct referent**: actor vs authorization act | Review reuse of `delegatee` and/or new VTI-qualified concept; do not equate the actor to delegation |
| DTG-SEM-004 `subject` | VTI: party/identifier named by an access control entry, including clients, devices and software agents | TIG `subject`: entity described by one or more claims, especially credential claims | **contextual specialization**: not exact by label | Source-qualified VTI authority-entry subject representation, with approved relationship to existing TIG subject if warranted |
| DTG-SEM-005 `trust context` | VTI: **nested key/data/credential/memory isolation partition**, scope of authority grants | TIG `trust-context`: contextual factors of a **trust decision** | **distinct meaning**: reject exact equivalence | New differentiated context-isolation concept if approved; preserve legacy `trust-context` |
| DTG-SEM-006 `trust task` | VTI: canonically identified, versioned **node operation** exposed and invoked by peers | TIG `trust-task`: Layer-3 protocol activity; Trust Tasks spec uses bilateral work | **multiple upstream meanings**: not exact; VTI and Trust Tasks uses require separate adjudication | Admit separate node-operation terminology only if approved; avoid conflating VTI with bilateral task documents |

## Immutable source definitions examined

- **DTG-SEM-001:** [Trust Tasks `proof.md` at pinned SHA](https://github.com/trustoverip/dtgwg-trust-tasks-spec/blob/bf667f3e8506b7fb2c3e96665b7060e2ebaad806/spec/terms-definitions/proof.md). Explicit source label `proof`, alternative label `Data Integrity Proof`; its role is the proof attached to a task document.
- **DTG-SEM-002:** [Trust Tasks `trust_task.md` at pinned SHA](https://github.com/trustoverip/dtgwg-trust-tasks-spec/blob/bf667f3e8506b7fb2c3e96665b7060e2ebaad806/spec/terms-definitions/trust_task.md). The source ties bilateral issuer/recipient work to documents and `threadId`.
- **DTG-SEM-003:** [VTI `delegate.md` at pinned SHA](https://github.com/trustoverip/dtgwg-vti-spec/blob/dc1ec07d42ec5c0054037795c06dbead608fbc5b/spec/terms-definitions/delegate.md). The delegate is a subject acting for another party, instantiated through a VTI access control entry.
- **DTG-SEM-004:** [VTI `subject.md` at pinned SHA](https://github.com/trustoverip/dtgwg-vti-spec/blob/dc1ec07d42ec5c0054037795c06dbead608fbc5b/spec/terms-definitions/subject.md). A subject is the principal named by an access control entry.
- **DTG-SEM-005:** [VTI `trust_context.md` at pinned SHA](https://github.com/trustoverip/dtgwg-vti-spec/blob/dc1ec07d42ec5c0054037795c06dbead608fbc5b/spec/terms-definitions/trust_context.md). Contexts form nested isolation partitions and delimit authority reach.
- **DTG-SEM-006:** [VTI `trust_task.md` at pinned SHA](https://github.com/trustoverip/dtgwg-vti-spec/blob/dc1ec07d42ec5c0054037795c06dbead608fbc5b/spec/terms-definitions/trust_task.md). A versioned, canonically identified exposed peer-invocable operation.

## TIG canonical concepts examined

- `glossary/terms/proof.yaml` and `glossary/terms/data-integrity-proof.yaml`
- `glossary/terms/trust-task.yaml`
- `glossary/terms/delegation.yaml`
- `glossary/terms/subject.yaml`
- `glossary/terms/trust-context.yaml`

The above concepts retain existing published IDs. Their earlier definitions have not been overwritten or repurposed.

## Required decision protocol

For each case, TIG's maintainer must record: (1) admission scope and authoritative source revision, (2) selected semantic disposition among `covered`, `partial`, `missing`, `not_applicable`, `indeterminate`, (3) exact candidate mapping strength or expressly `none`, (4) rationale, alternate interpretation rejected and compatibility impact, (5) reviewer identity/date and source license/attribution, and (6) whether a canonical change is authorized. The pending `governance/coverage/dtg-semantic-decision-proposals.json` ledger is **not** itself an approval record.

**Immediate safe default:** reject exact matching in all six cases until authorized review. That is a precautionary execution rule, not an affirmative source-semantic approval.

## Publication and compatibility consequences

Do not overwrite `urn:tig:concept:trust-task`, `urn:tig:concept:trust-context` or `urn:tig:concept:delegation` with specialized VTI or Trust Tasks meanings. A reviewed proposal for a separate concept must include an individual ID, source provenance, authoring template, crosswalk strength, migration tests and generated projections. No semantic release should be cut before that review completes.

## Remaining G2 scope

This packet covers **six** of the **17** initial lexical candidates; the other **11**, the **89** initial lexical nonmatches and the later **749** external source definitions still require scope-controlled review. These groups should not be conflated or counted as automatically distinct TIG omissions.
