---
title: "Pinned Specification Term Extraction"
parent: "Operations & Evolution"
grand_parent: "Govern TIG"
---

# Extracting source-owned terminology

This optional offline intake tool supports [#7](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/7) and [#8](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/8). It operates on a locally checked-out, revision-pinned Spec-Up-T specification, not on mutable `main` or a rendered site.

## Procedure

1. Identify the canonical source repository, approved scope, licensing requirements, and complete 40-character commit SHA.
2. Check out that exact revision in a separate working directory, ensuring `spec/terms-definitions/` exists.
3. Run:

```sh
python tools/extract_spec_up_t_terms.py \
  --source-root /path/to/pinned/specification \
  --repository trustoverip/dtgwg-trust-tasks-spec \
  --commit FULL_40_CHARACTER_COMMIT_SHA \
  --output /tmp/source-terms.json
```

4. Compare the extracted labels and source-file hashes against the approved corpus manifest, then create *candidate* mappings for semantic review under #9. Preserve excluded or external-glossary definitions explicitly.

The tool only extracts explicit `[[def: ...]]` declarations from Markdown files in `spec/terms-definitions/`. It records the caller-supplied commit identifier and SHA-256 of each file; **it does not verify that the directory is actually the specified Git commit**. The operator must independently verify the checkout provenance. Definitions declared outside that directory, external transclusions, implicit terminology, and non-Spec-Up-T sources are *not included*; zero extracted rows does not mean the specification contains no terms. The output is an inventory candidate, not completeness evidence or a conformance determination.

CI tests extraction behavior using controlled fixtures. It does not download or reproduce upstream specifications in the glossary's default workflow.
