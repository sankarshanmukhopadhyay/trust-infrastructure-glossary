# External ToIP glossary: verified definition extraction

**Programme:** [#28](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/28) · **Gate:** G0 source admission / G1 candidate preparation

## Scope and evidence

The prior [pinned external tree inventories](external-glossary-git-tree-inventory.md) established 543 ToIP Main Glossary and 215 ToIP General IT Glossary Markdown term files. **File counts are not definition counts.** This increment explicitly extracts primary Spec-Up-T `[[def: ...]]` declarations, including aliases, from local checkouts of those exact upstream commits.

The GitHub Actions workflow checks out:
- `trustoverip/ctwg-main-glossary` at `00608bb6ce7f7e6285f202b580548d61ee716621`;
- `trustoverip/ctwg-general-glossary` at `73604cf54c9f238b0d239daecc413a045f61c75e`.

The extraction fails if the checkout HEAD differs from the pinned commit, or if the tracked terminology directory is empty. Per-definition records include source repository, commit, path, content SHA-256, Git blob SHA, occurrence position, primary label, alternative designations and explicit `unreviewed` / `tig_mapping: null` status. Files without an explicit definition marker are retained in a separate list; do not silently count them as defined concepts.

## Reproduction

Run the local checker on authentic upstream checkouts:

```bash
python -m unittest discover -s tests -p 'test_external_glossary_definition_extraction.py' -v

python tools/extract_external_glossary_definitions.py \
  --repository trustoverip/ctwg-main-glossary \
  --commit 00608bb6ce7f7e6285f202b580548d61ee716621 \
  --source-root /path/to/pinned/toip-main \
  --output /tmp/tig-toip-main-definitions.json
```

The same command supports General IT Glossary using its specified commit. CI publishes both reports as the `tig-external-glossary-pinned-definitions` artifact. Source attribution is by immutable commit, source path, blob SHA and content digest. The tool has no permission to edit canonical TIG concepts.

## What is not yet established

- The full specification-derived DTG terminology boundary, and the actual external glossary revisions transcluded by the published Credentials Specification.
- The separate DTG Glossary's authoritative, immutable content.
- Which extracted external definitions are portable and legitimately in scope for a DTG/VTC-specific crosswalk.
- Any reviewed exact, close, broad or narrow semantic mappings to TIG.
- A complete relationship coverage denominator or independence of an adopter.

**Decision:** This is a measurable G0 source-extraction increment, not G0/G1/G2 acceptance. The next tranche must deduplicate with context retained, establish the source inclusion/exclusion ledger, then conduct source-specific human semantic review.

## Source and operational safeguards

Source glossaries remain authoritative for their own definitions; TIG's mappings are descriptive. Preserve source license and attribution. Do not add hundreds of terms to TIG based solely on lexical discovery. GitHub Actions stores extracted data as test evidence; no direct changes to generated products or the public Pages site are required.
