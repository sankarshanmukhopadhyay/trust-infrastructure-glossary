# Trust Infrastructure Glossary

[![Validation](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/actions/workflows/validate-governance-glossary.yml/badge.svg)](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/actions/workflows/validate-governance-glossary.yml)
[![Pages](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/actions/workflows/pages.yml/badge.svg)](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/actions/workflows/pages.yml)

**A governed vocabulary, taxonomy and semantic reference for digital trust infrastructure.** TIG publishes human-readable concepts with stable identifiers, provenance and machine-readable representations. It helps teams use consistent terminology without treating a glossary mapping as normative approval or certification.

**[Open the glossary website](https://sankarshanmukhopadhyay.github.io/trust-infrastructure-glossary/)**

## Find what you need

| Your task | Start here |
| --- | --- |
| **Understand a term** | [Explore concepts](https://sankarshanmukhopadhyay.github.io/trust-infrastructure-glossary/explore/) — A–Z, subject areas, taxonomy and relationships |
| **Use TIG in a project** | [Use TIG](https://sankarshanmukhopadhyay.github.io/trust-infrastructure-glossary/use/) — stable IDs, profiles and machine-readable artifacts |
| **Review or contribute** | [Govern TIG](https://sankarshanmukhopadhyay.github.io/trust-infrastructure-glossary/governance/) — authoring, provenance, validation and publication |

For the distinction between definitions, classification and graph relationships, see the [Semantic Model](https://sankarshanmukhopadhyay.github.io/trust-infrastructure-glossary/semantic-model/).

## For developers

**Canonical concepts:** `glossary/terms/*.yaml`  
**Schemas and profiles:** `schemas/`, `profiles/`  
**Generated products:** `generated/`, `_terms/` (do not edit by hand)

See the [artifact catalogue](https://sankarshanmukhopadhyay.github.io/trust-infrastructure-glossary/artifacts/) for JSON, JSON-LD, RDF/Turtle and vocabulary profiles.

To validate a contribution:

```bash
pip install -r requirements.txt
python tools/validate_governance_glossary.py
python tools/validate_profiles.py
python tools/validate_semantic_model.py
python tools/build_governance_glossary.py
python tools/build_quality_report.py
python tools/build_semantic_model.py
python tools/build_jekyll_site.py
python tools/build_site_information_architecture.py
python tools/validate_site_ia.py
```

See [Contributing](Contributing.md) and the [Repository Operating Model](governance/repository-operating-model.md) before modifying sources.

## Authority and assurance

TIG concepts are governed by TIG maintainers; cited specifications remain authoritative for their own terminology. A matching label does **not** establish semantic equivalence. Internal quality scores are not completeness, conformance or certification claims.

The ongoing [DTG/VTC convergence programme](https://github.com/sankarshanmukhopadhyay/trust-infrastructure-glossary/issues/28) separates pinned source evidence, pending semantic review and downstream consumption. Its baseline findings are [documented here](governance/dtg-vtc-bounded-assurance-verdict-2026-10-12.md).

## Project

[Releases and lineage](https://sankarshanmukhopadhyay.github.io/trust-infrastructure-glossary/project/) · [Migration from v1](MIGRATION_v2.md) · [License](LICENSE.md)
