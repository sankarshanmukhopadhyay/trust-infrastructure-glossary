# Standalone TIG catalog consumer and independent adoption protocol

**Related issues:** [#28](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/28), #6, #13, #14  
**Implementation:** [catalog_adopter.py](catalog_adopter.py)

## Purpose

This example proves a minimal stable-ID catalog consumption contract using **only the Python standard library**, without importing TIG's Python tooling or YAML parser. It also performs a deliberately negative check: an unresolved `trust-task` source-meaning candidate must not be consumed as an approved exact match.

A separate program is **not** the same thing as an independently maintained consumer. This example is authored and maintained inside TIG, so its `independently_maintained` flag remains `false`. Its passing CI result can strengthen G4 implementation validation but **cannot** close G5.

## Run the example

From the repository root:

```bash
python examples/consumers/standalone/catalog_adopter.py \
  --catalog generated/json/trust-infrastructure-glossary.catalog.json \
  --decisions governance/coverage/dtg-semantic-decision-proposals.json \
  --concept-id urn:tig:concept:trust-task \
  --output /tmp/tig-standalone-adopter-result.json

python -m unittest discover -s tests -p 'test_standalone_catalog_adopter.py' -v
```

The result records SHA-256 hashes of the two input files, the resolved TIG concept ID, presence of a preferred designation and provenance, count of pending/ambiguous cases rejected, and an explicit assertion that source-semantic equivalence is **not verified**. CI uploads the report as `tig-standalone-adopter-conformance`.

## Genuine independent G5 acceptance

A **separately maintained implementation** must consume a pinned TIG commit or release and produce verifiable operation logs. Acceptance needs:

1. External maintainer and repository/implementation revision, named in an issue/PR without ambiguity.
2. Explicit input URL, TIG revision, artifact digests and profile or `concept_id` selection.
3. A positive lookup that resolves the stable identifier, formal labels, provenance and (when applicable) mapped relationship scope.
4. A negative lookup that rejects a misleading same-label or pending exact mapping. No uncontrolled silent fallback.
5. Independently reproducible execution commands, test/environment evidence, original observation artifacts and a reviewed conformance disposition.
6. An adoption assessment with installation friction, semantic ambiguity, backwards compatibility, revision pinning and operator documentation findings.

**Do not** mark G5 PASS on the basis of this same-repository prototype, its source independence, a successful CI run, a sample JSON fixture, or unverified downstream claims.

## Compatibility and authority

This example does not edit the `glossary/terms/` source, alter its schema, define an external specification's terminology, or grant TIG normative authority. If semantics change in the future, retest both the positive and negative journeys against a pinned published revision.

## Conformance report template

| Evidence | Required downstream value |
| --- | --- |
| Adopter owner and repository | Real independently maintained source |
| Adopter revision | Immutable tag/SHA |
| TIG source revision | Immutable tag/SHA |
| Input digests | SHA-256 of actual consumed data |
| Positive case | Stable-ID resolution with observed values |
| Negative case | Ambiguous or pending mapping rejected |
| Compatibility | Runtime and API/format observations |
| Decision | PASS/FAIL/INDETERMINATE with reason |
| Review attribution | Human reviewer and date |

If any mandatory external evidence is unavailable, record G5 **INDETERMINATE — external consumer evidence absent**, not PASS.
