# G2 source-verified labels for the initial DTG corpus

The existing 106-file inventory is a source-identity ledger. This increment supplements it with **actual primary labels and aliases**, parsed from the three pinned upstream checkouts. All 106 definitions are required to reconcile exactly; checkout SHA or Git blob drift causes failure. Each source record retains its file path, blob identity, exact source content digest and its unapproved semantic state.

## Reproduction

From the TIG repository root, clone and check out the exact commits listed in `governance/coverage/pinned-dtg-spec-term-trees.json` under `_upstream/dtg/{credentials,vti,tasks}`. Then:

```bash
python -m unittest discover -s tests -p 'test_enrich_g2_source_queue.py' -v
python tools/enrich_g2_source_queue.py --sources-root _upstream/dtg --output /tmp/tig-g2-source-verified-definitions.json
```

CI carries out the immutable checkouts and publishes the `tig-g2-source-verified-106-definitions` artifact.

## Evidence boundary

The 17 initial lexical rows and 89 rows without lexical candidates are retained. Labels and aliases are **facts extracted from the pinned upstream definitions**, not semantic adjudications. Each source record remains `semantic_disposition: null`, `mapping_assertion: null` and `canonical_change_allowed: false`.

This removes the missing-label obstacle for G2 review. Actual human source-comparison and 5-way disposition for each definition, full G0 admission, and independent G5 adoption remain required. Do not convert the presence of source labels into a claim of coverage.
