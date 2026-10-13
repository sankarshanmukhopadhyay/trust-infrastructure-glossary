# G0: authenticated external glossary source-tree inventory

**Programme:** [#28](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/28) · **G0 admission substage:** two ToIP source repositories.

## Purpose

The Credentials Core terminology section refers to external ToIP glossaries, but its rendered page is not an immutable enumeration of its dependencies. GitHub search results and a few checked source blobs do not produce a denominator. This increment produces **complete Git-tree directory inventories at two exact commits**, retaining the full list of filenames and blob object IDs for audit.

## Evidence-generating commands

The repository validation workflow runs the commands below on GitHub-hosted runners (GitHub API authentication from the job token):

```bash
python -m unittest discover -s tests -p 'test_external_glossary_tree.py' -v

python tools/inventory_external_glossary_tree.py \
  --repository trustoverip/ctwg-main-glossary \
  --commit 00608bb6ce7f7e6285f202b580548d61ee716621 \
  --output /tmp/tig-toip-main-tree.json

python tools/inventory_external_glossary_tree.py \
  --repository trustoverip/ctwg-general-glossary \
  --commit 73604cf54c9f238b0d239daecc413a045f61c75e \
  --output /tmp/tig-toip-general-tree.json
```

The CI artifact is **`tig-external-glossary-pinned-source-trees`**. The tool checks that the Git tree is complete (`truncated: false`), refuses invalid blob SHAs and duplicate paths, and records canonical sorted path and blob identities. A failed API fetch or truncated tree fails the job rather than creating a misleading partial count.

## Boundaries and next gates

A complete listing of source files is evidence that the files were present **at the chosen commit**, not that every file defines one term, or that the rendered Credentials Specification used the same commit. G0 still requires:
- Source term parsing and digest/content validation, alias handling and source license review.
- Provenance for the separate DTG Glossary, including references that resolve through Atlassian.
- Build attribution establishing which versions of ToIP glossaries and DTG Glossary the Credentials Specification used or a fully explicit replacement corpus admission decision.
- A precise inclusion/exclusion contract for the larger DTG/VTC terminology universe.

G1 requires separate four-dimensional mapping evidence with denominators. G2 is human semantic judgment; no hash, matching label, or passing CI authorizes `exact` mappings. G5 independent consumer testing is not satisfied by running these CI checks.

## Expected release disposition

This is an evidence-generation and test-hardening increment with no changes to canonical concept semantics. Merge after full CI and leave #28 open. Do not issue a semantic release for this feature alone.
