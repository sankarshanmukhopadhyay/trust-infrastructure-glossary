---
title: "DTG and VTC Source Corpus — Initial Evidence Baseline"
parent: "Operations & Evolution"
grand_parent: "Govern TIG"
---

# DTG and VTC source corpus — initial evidence baseline

**Status:** preliminary intake, **not** a complete or approved source corpus.  
**Observed:** 2026-10-12.  
**Tracking:** [#6](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/6), [#7](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/7).

## Authority boundary

TIG is an independent semantic publisher. External DTG specifications retain their own normative authority. An informative architecture baseline, task-force overview, or implementation README is not a normative vocabulary specification. Source-file blob SHA pins **file bytes**, not an entire repository revision or release. A complete source admission requires the source's declared authority, revision, licensing review, and concept extraction.

## Directly inspected sources

| Source | Role | File blob SHA observed | Editorial disposition |
| --- | --- | --- | --- |
| [DTGWG overview](https://github.com/trustoverip/dtgwg-general/blob/main/README.md) | Working-group scope and pointers; informative overview | `a49375834cf97fc8a8ce47f14685ab1d29309770` | Intake context; not itself a canonical term specification |
| [DTG hybrid interaction architecture baseline](https://github.com/trustoverip/dtgwg-general/blob/main/architecture/dtg-hybrid-interaction-architecture-baseline.md) | Architecture mapping and terminology candidates; **explicitly informative** draft v0.1 (updated 2026-05-25) | `6a4fb9aefcc46f3769edbbf76a8e2395926fbc42` | Candidate inventory and ambiguity discovery, not automatic exact mappings |
| [DTG Credentials Core Specification repository README](https://github.com/trustoverip/dtgwg-cred-spec/blob/main/README.md) | Working-draft entry point; actual specification file and version **still to be pinned** | `a6978347e868989765681e95b94ff5dfa334c216` | Discovery pointer only; NOT a pinned normative specification |
| [OpenVTC implementation README](https://github.com/OpenVTC/openvtc/blob/main/README.md) | Concrete VTC developer-community CLI implementation | `9cbbe4ec71a5323d29e5b4fef1bb7b6679190f2f` | Implementation-local vocabulary; no normative promotion |
| [OpenVTC demo repository README](https://github.com/openvtc-plumbers/demo-repository/blob/main/README.md) | Demo GitHub repository, not a useful terminology corpus in itself | `b67e0ed296537eecbce4ce3faeb11a83041b4f1b` | Excluded from terminology denominator with reason |

## Initial concept families for *review*, not established TIG gaps

1. **Graph/identifiers:** DTG presence, DTG node/edge view, VID, relationship/membership/community/persona DIDs.
2. **Agent/infrastructure:** VTA, pVTA/cVTA, local/cloud VTA, VTA network, PNM, CNM, PNV, VTSP.
3. **Community/network governance:** VTC, VTN, admission, membership, recognition, anchors and trust registries.
4. **Credentials/relationship annotations:** VRC, VMC, VIC, VPC, VEC, VWC, witness and endorsement evidence.
5. **Protocol/interaction:** Trust Tasks, TSP, TRQP, DIDComm, consent/ceremony and policy enforcement.

The architecture baseline expressly distinguishes DTG presence from graph node view, VTA from actor/community, and annotation credentials from relationship structure. It identifies PNM wording alignment, CNM status, and VTA-network details as unresolved or less-formal topics. These are **review candidates**, not errors demonstrated in TIG.

## Outstanding source admission before G0

- [ ] Identify the canonical DTG glossary and confirm the exact revision and licensing.
- [ ] Pin the actual Credentials Core Specification working draft(s), rather than only its README.
- [ ] Decide whether Trust Tasks, TSP and TRQP drafts are within the initial bounded denominator; pin those selected.
- [ ] Identify OpenVTC implementation revision and relevant documentation beyond README; classify implementation-specific terms.
- [ ] Record license/attribution permissions for every imported definition; do not copy source text by default.
- [ ] Record repository commit/release revisions where available; blob SHA above proves only inspected file content.
- [ ] Obtain a reviewed source precedence and explicit exclusion list.

## Evidence and next increment

Do **not** publish a numerical completeness percentage until the approved corpus and denominator exist. Continue through [#8](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/8) only using source-versioned entries, preserving `unknown` and `not_applicable` states. Run the existing glossary/site validation when integrating this document into the site.

## Additional directly inspected sources — second increment

| Source | Role and declared state | File blob SHA observed | Disposition |
| --- | --- | --- | --- |
| [DTG Credentials Task Force README](https://github.com/trustoverip/dtgwg-cred-tf/blob/main/README.md) | Confirms normative Credentials Core specification now resides in `dtgwg-cred-spec`; links the draft DTG Glossary as a separate Google document | `c0d1ecac59404d330d6328feff3490aa898c24b8` | Authority-routing evidence; actual normative spec text not yet pinned |
| [VTI specification README](https://github.com/trustoverip/dtgwg-vti-spec/blob/main/README.md) | Describes specification for trust contexts, authority, lifecycle, node/host composition, VTA, and VTC | `898d3495a0e24701f3843e36268c90c7226daab5` | Spec entry point; chapter-level source/version still needed |
| [VTI implementation README](https://github.com/OpenVTC/verifiable-trust-infrastructure/blob/main/README.md) | Explicitly distinguishes normative VTI specification from its Rust implementation and documents divergence precedence | `ac945db8fbc6bef6be7da58cb6c3c916ca4aa397` | Implementation evidence; prioritize spec where they differ |
| [Trust Tasks TF README](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/main/README.md) | Registry entry point and framework spec publication model | `a80b0a4f70c6990b53cb8201dec8101b45fc7736` | Discovery pointer |
| [Generated Trust Tasks framework SPEC](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/main/SPEC.md) | Working Draft 0.7.0, last updated 2026-09-24; generated from canonical `dtgwg-trust-tasks-spec` commit `52ba2efbf05ab1f3b9af9929dc9a8c6350a88826` | `6664fe5506d9d79515dac0c624d9a4bf5184c80e` | Use canonical source commit for semantic extraction; generated document is not editorial authority |

**Precedence finding:** DTG Credentials and VTI each distinguish canonical specifications from supporting task-force/implementation repositories. The Trust Tasks registry SPEC explicitly points to a canonical source commit. The future crosswalk must key mappings to these actual authoritative texts, not to descriptive README phrases.

**Remaining G0 impediments:** obtain a readable and properly attributable DTG Glossary source; inspect the substantive Credentials Core document and VTI chapters; complete source-level copyright/license determination. No numerical coverage can yet be computed.
