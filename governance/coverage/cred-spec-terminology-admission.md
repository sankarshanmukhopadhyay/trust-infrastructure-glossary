# Credentials specification: rendered terminology source admission

**Issue:** [#28](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/28) · **Gates:** G0 / G1 / G2  
**Observed:** 2026-10-13  
**Machine record:** [cred-spec-terminology-admission.json](cred-spec-terminology-admission.json)

## Source and authority

The user-identified [DTG Credentials Core Specification — Terminology](https://trustoverip.github.io/dtgwg-cred-spec/#terminology) is a **Working Draft v1.0**, and its Terminology section is expressly **informative**. The section says its defined terms are drawn from a DTGWG-maintained **DTG Glossary**, with external references to the **ToIP Main Glossary** and **ToIP General IT Glossary**.

The existing TIG pinned tree ledger has **50 explicit term files** from `trustoverip/dtgwg-cred-spec` at commit `4088056a15f6e74847eb422e1c2bae33684272ea`. This is an authenticated source-directory count, **not** the count of all definitions imported by the rendered page. A rendered live URL is not itself pinned evidence. We have **not** established that the published rendered page was built from this exact pinned commit. Consequently, do not conflate page content, pinned repository terms, imported glossary definitions, and all hyperlinked concepts into one denominator.

### Admission classes

| Class | Current treatment | Why |
| --- | --- | --- |
| Explicit `spec/terms-definitions/*.md` entries | Admitted pinned source subset | Tree and blob SHAs are already in `pinned-dtg-spec-term-trees.json` |
| Terminology rendered directly on the Working Draft page | Useful observation; pending SHA-to-build parity | HTML is not immutable by construction |
| DTG Glossary definitions referenced by the spec | **Pending separately pinned admission** | Linked upstream semantic source not captured by directory-only intake |
| ToIP Main Glossary and General IT Glossary links | **Pending separately pinned admission** | External transclusion and license/revision/scope must be inventoried |
| General web hyperlinks in explanatory prose | **Not automatically glossary entries** | Contextual references are not all authored definitions |

## Semantic boundaries that must survive G2

1. **Formal type hierarchy vs explanation.** The document groups edge, invitation and annotation credentials for reader comprehension. Its formal hierarchy is `VerifiableCredential → DTGCredential → {MembershipCredential, RelationshipCredential, InvitationCredential, PersonaCredential, EndorsementCredential, WitnessCredential}`. The grouping labels are not additional schema types.
2. **VRC/VMC meaning.** A VRC represents a direction of a bidirectional peer relationship, while a VMC establishes membership; do not flatten these into undifferentiated 'relationship credential' synonyms.
3. **IDVC exclusion.** An identity verification credential may support a community's onboarding process; it is **not** itself a standard DTG Core Credential.
4. **R-card exclusion.** The relationship card is characterized as a verifiable data structure, not a DTGCredential subtype.
5. **Task contexts.** The specification distinguishes credential claims from Trust Task artifacts and contextual bindings. Do not mutate TIG's inherited `trust-task` meaning based on an unapproved lexical match.
6. **Source-version state.** A Working Draft statement is source-identified evidence, not automatic approval for TIG exact mappings or normative coverage claims.

## G0 evidence and next G1 operations

1. Pin the **source commit of the actually deployed HTML build** or identify it as unverifiable; compare the rendered section to term-file data by explicit primary labels and aliases, recording discrepancies.
2. Resolve the canonical DTG Glossary location and immutable revision; inventory all referenced and transcluded definitions and their licenses.
3. Separately source-pin ToIP Main/General IT glossary inventories where admissible. Do not import everything indiscriminately: classify in-scope referenced definitions vs out-of-scope common terms with rationale.
4. Add each admitted record to the four-axis source-to-TIG ledger; include `source_repository`, `source_commit`, `path_or_anchor`, primary designation, aliases, definition or source hash, authority class, licensing and mapping-review state.
5. Route the high-risk credential cases through G2 review; assert no exact mapping until review.
6. Generate measured denominators independently for pinned explicit definitions, in-scope external definitions, and excluded references.

## Falsifiable checks before G0 passes

- Fails if the page is counted as immutable when its build SHA is unknown.
- Fails if `50` is reported as the entire resolved terminology denominator.
- Fails if an external glossary reference is silently declared covered.
- Fails if reader categories are emitted as credential schema types.
- Fails if lexical matching to TIG is interpreted as source-semantic approval.
- Fails if IDVC or r-card becomes a DTG Core Credential by automated conversion.

## Current disposition

**G0 PARTIAL / G1 PENDING / G2 PENDING.** This increment admits the rendered specification as a source of observable terminology and records unresolved transclusion dependencies. It does not alter canonical concepts or fabricate a coverage percentage. Further reconciliation must consume pinned upstream source text rather than a live documentation page alone.

## Candidate ToIP repository pins (2026-10-13)

The [external glossary candidate pin register](toip-external-glossary-candidate-pins.json) identifies immutable **candidate repository revisions** for the ToIP Main Glossary (`trustoverip/ctwg-main-glossary` at `00608bb6ce7f7e6285f202b580548d61ee716621`) and General IT Glossary (`trustoverip/ctwg-general-glossary` at `73604cf54c9f238b0d239daecc413a045f61c75e`). A source file was fetched and its blob SHA recorded from each commit. Those results verify the repositories and examples, **not** their complete definition sets and **not** the commits transcluded by the rendered Credentials specification. The DTG Glossary referenced through Atlassian has not been reduced to an authenticated immutable source.

The G0 requirement for authenticated, complete inventories and published-version correspondence remains unmet. Do not change G0 to PASS or add candidate source counts to the accepted coverage denominator until the tree/transclusion checks and source license examination are complete.
