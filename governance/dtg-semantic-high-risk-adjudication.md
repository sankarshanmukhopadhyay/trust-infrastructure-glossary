---
title: "DTG Semantic Adjudication — High-Risk Cases"
parent: "Operations & Evolution"
grand_parent: "Govern TIG"
---

# High-risk DTG semantic adjudication proposals

This document provides an actionable **pending review** packet for issue [#9](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/9). The [machine-readable decisions register](coverage/dtg-semantic-decision-proposals.json) selects six high-risk cases from the [17-row first-pass register](coverage/dtg-semantic-first-pass.json) against source revisions fixed in [the three-spec manifest](coverage/pinned-dtg-spec-term-trees.json).

## Proposed treatment

- **Trust Task (two sources):** separate consideration of the versioned operation meaning in VTI, bilateral verifiable work in Trust Tasks, and historical TIG Layer-3 use. Avoid changing the existing concept's meaning silently.
- **Trust context:** VTI's nested key/credential/authority compartment is not TIG's trust decision context. Treat as potentially distinct concepts.
- **Delegate:** a subject acting for another is not the same semantic entity as the *act* of delegation.
- **Subject:** VTI's access-control-entry subject is distinct in scope from the subject of credential claims.
- **Proof:** Trust Tasks' optional W3C Data Integrity Proof for a Trust Task document could map to TIG's narrower Data Integrity Proof concept, but the generic TIG proof is also a lexical candidate. Hold pending review.

## Approval record requirements

Each case requires a reviewer to select the applicable semantic relationship or an explicit exclusion, cite the source definition and TIG counterpart, assess backward compatibility of published concept IDs, and record consequences for downstream profiles and generated representations.

**No relation is approved by this packet.** Each case has `approval: pending` and `canonical_change_allowed: false`; CI asserts those invariants. These are adjudication-ready proposals, not approved TIG term changes. The 89 source labels with no lexical candidate require separate, scoped review before a corpus-wide finding or percentage is published.

Linked flow: [#7](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/7) → [#8](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/8) → **[#9](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/9)** → [#10](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/10), supported by [#11](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/11).
