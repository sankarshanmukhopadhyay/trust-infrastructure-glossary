#!/usr/bin/env python3
"""Generate deterministic TIG taxonomy and lightweight ontology artifacts."""
from __future__ import annotations

import json
from pathlib import Path

from semantic_model_core import ROOT, build_semantic_model, canonical_json, jsonld_document, load_yaml, MODEL_PATH, turtle_document


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(path.relative_to(ROOT))


def main() -> None:
    config = load_yaml(MODEL_PATH)
    graph = build_semantic_model()
    outputs = config["outputs"]

    taxonomy = {
        "schema_version": graph["schema_version"],
        "model_id": graph["model_id"],
        "authority": graph["authority"],
        "taxonomy": graph["taxonomy"],
    }
    write(ROOT / outputs["taxonomy_json"], canonical_json(taxonomy))
    write(ROOT / outputs["ontology_jsonld"], canonical_json(jsonld_document(graph)))
    write(ROOT / outputs["ontology_turtle"], turtle_document(graph))


if __name__ == "__main__":
    main()
