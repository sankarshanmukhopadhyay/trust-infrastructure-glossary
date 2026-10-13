# Complete G2 source-review queue: 106 pinned definitions

This is the machine-verifiable **initial DTG specification source cohort**, not a complete universe of all transcluded DTG/VTC/ToIP terms. It joins every file in the three pinned specification definition directories to the 17 preliminary lexical candidates already captured in `dtg-g2-adjudications.json`.

The generator emits exactly **106 distinct source-definition records**: **17** with lexical candidates and **89** without. Every record has source repository, commit, source path, blob SHA, explicit pending status and `mapping_assertion: null`. For the 89 nonmatches the source label is deliberately `null` because the pinned file tree only establishes file identities; generating a label from a filename would fabricate source evidence. The existing pinned source extraction tool must be used to recover the actual label and full definition before human review.

## Run

```bash
python tools/build_g2_full_source_queue.py --output /tmp/tig-g2-complete-source-queue.json
python -m unittest discover -s tests -p 'test_g2_full_source_queue.py' -v
```

CI uploads the report as `tig-g2-complete-106-source-queue`, rejects orphan candidate sources, duplicate/missing source records, premature approval and any claim of complete semantic coverage.

## Required review before G2 acceptance

For each of the 89 nonmatched rows, inspect the authentic pinned source definition, synonyms and conceptual scope; then record covered, partial, missing, not applicable or indeterminate along with source evidence, reviewer, date and any proposed compatibility-safe remediation. No lexical candidate is **not** equivalent to a missing TIG concept.

For the 17 initially matched rows, use [the decision register runbook](../completion/tig-g2-adjudication-runbook.md) and the [six source-grounded high-risk dossiers](../completion/tig-high-risk-semantic-adjudication-packet.md). The 749 additional externally extracted ToIP definitions remain **source-admission candidates**, not automatically additions to the 106-row DTG cohort.

**Status:** initial source cohort completely accounted for; human semantic dispositions and wider G0 admission still pending. No canonical change and no new semantic release authorized.
