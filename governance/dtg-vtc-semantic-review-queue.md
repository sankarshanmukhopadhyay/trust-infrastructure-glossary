---
title: "DTG/VTC Semantic Review Queue"
parent: "Operations & Evolution"
grand_parent: "Govern TIG"
---

# DTG/VTC semantic review queue

This workflow turns the [bounded DTG/VTC crosswalk](../governance/coverage/dtg-vtc-pilot.json) into **deterministic review evidence**, not an automated decision about semantic equivalence.

## Generate the review artifact

From the repository root:

```sh
python tools/validate_source_crosswalk.py
python tools/report_source_crosswalk_discovery.py --output /tmp/tig-crosswalk-discovery.json
python tools/build_source_review_queue.py --output /tmp/tig-review-queue.json
python -m unittest discover -s tests -p 'test_source_review_queue.py' -v
```

CI publishes `tig-source-semantic-review-queue` after the same tests. The JSON queue gives the source label, known TIG mapping, alternative normalized lexical matches, potential conflicts, source rationale and review priority.

## Interpretation and limitations

- All eleven pilot entries remain **unadjudicated**; review priority does not confer authority.
- A lexical match may be a homonym, a broader concept or a different version of a term. It cannot prove exact, close or narrower mapping.
- A non-match cannot establish that a concept is absent. The candidate inventory itself is still incomplete.
- The `coverage_denominator` remains `null` until the approved source corpus is enumerated.
- The existing `trust-task` discrepancy and candidate VDC mapping require source-versioned human semantic judgment before changing `glossary/terms/`.
- Reviewed decisions belong in the source-of-truth crosswalk and governance issue #9, not hand-edits to the generated queue.

## Exit criteria before modifying canonical terms

1. Admit and version-pin complete terminology sets for each in-scope source (issue #7).
2. Account for every source concept and explicit exclusion (issue #8).
3. Record adjudicator rationale and evidence for exact/close/broad/narrow/unmapped dispositions (issue #9).
4. Implement only justified terminology changes, preserving stable TIG concept identifiers and source attribution (issue #10).

The queue is a machine-verifiable preparation artifact for semantic review; it is **not** a DTG conformance certificate.
