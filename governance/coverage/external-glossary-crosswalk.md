# External source-to-TIG lexical crosswalk

**Programme:** [#28](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/28) · **Gate:** G1 reproducible candidate discovery.

## Reproducible pipeline

The main validation workflow:

1. Authenticates two external glossary Git checkouts at immutable commits.
2. Extracts every explicit `[[def: ...]]` declaration, including source aliases and source blob identities.
3. Reads `generated/json/trust-infrastructure-glossary.catalog.json` (617 TIG concepts at the current baseline).
4. Matches normalized labels and aliases, retaining all TIG concept candidates rather than choosing an arbitrary candidate.
5. Emits a record for **every extracted source definition**, including unmatched labels, with `semantic_disposition: unreviewed` and `mapping_assertion: null`.

The machine-readable output is retained as artifact `tig-external-glossary-lexical-crosswalk`. Reproduce locally:

```bash
python -m unittest discover -s tests -p 'test_external_glossary_crosswalk.py' -v
python tools/build_external_glossary_crosswalk.py \
  --catalog generated/json/trust-infrastructure-glossary.catalog.json \
  --source /tmp/tig-toip-main-definitions.json \
  --source /tmp/tig-toip-general-definitions.json \
  --output /tmp/tig-external-source-crosswalk.json
```

The source inputs must originate from the pinned extraction procedure in [external-glossary-definition-extraction.md](external-glossary-definition-extraction.md).

## Meaning of the output

- `one_candidate` means a lexical designation resolves to one TIG concept ID. It is **not semantic equivalence**.
- `ambiguous` means a source label or alias has multiple TIG identity candidates; **all candidates are retained**.
- `unmatched` means no designation candidate was found using this normalization; it is **not evidence that the concept is absent**.
- `source_definition_count` counts explicit definition occurrences, not files.
- `semantic_coverage: null` is mandatory until source-specific semantic decisions have been reviewed.

Normalizing Unicode text, case and punctuation is a lexical discovery aid. It is not a license to flatten contextual meanings, treat `close` as `exact`, or change stable TIG concept identities.

## Next acceptance gates

**G0** remains partial while source transclusion parity, separate DTG Glossary admission and copyright/attribution decisions are unresolved. **G1** becomes machine-reproducible for the two selected external glossary source commits, but the full, formally admitted DTG/VTC source universe requires expansion and explicit exclusions. **G2** requires review of definition text and source contexts, beginning with the six existing high-risk cases; **G3** then implements only approved corrections. G5 requires independent adopter evidence.

The crosswalk is CI evidence, not a generated canonical semantic product or a public normative dataset. It must not be used as an automatic exact-match registry.
