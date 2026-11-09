# Fractal-Geometric Harmonic Coordination Language (FGHCL)

**Abazith** is the human-readable notation/dialect for FGHCL.

FGHCL defines a typed, provenance-preserving language for describing PAN V8 states, geometric/cymatic observations, JOBF transformations, Janus Hydra translations, and paired UHFE/UDFE representations.

## Architecture boundaries

- **E8 / Gosset 4₂₁:** canonical geometric reference.
- **D8:** distinct rank-8 root system and compatible symmetry subgroup in the relevant E8 construction; not a synonym for E8 or for eight-dimensional space.
- **JOBF:** breathing, folding, flipping, rotating, and omnidirectional geometric operations.
- **V8:** eight-coordinate manifold/state representation.
- **Janus Hydra:** fractal-geometric translator operating in tandem with V8; it is neither UHFE nor UDFE.
- **UHFE / UDFE:** paired formation and decoherence representations downstream of Janus translation.

## Specifications

- [FGHCL / Abazith Foundational Language Specification — Draft 0.1](docs/FGHCL_ABAZITH_SPEC_v0.1.md)
- [Abazith v0.1 Frozen State Grammar](docs/ABAZITH_V0.1_GRAMMAR.md)

## Parser implementation

The first executable Abazith v0.1 subset parses typed V8 state records. It provides a tokenizer, immutable AST records, schema/version validation, and deterministic canonical serialization. The scope is intentionally limited: JOBF operation syntax, Janus Hydra translation blocks, UHFE/UDFE expressions, geometry declarations, and cymatics records are not parsed yet.

Run the conformance suite:

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

Parser tests establish syntax and declared-schema behavior only. They do not validate physical interpretations or models.

## Documents
- [`FGHCL_foundation.md`](FGHCL_foundation.md): implementation-grounded foundation
- [`docs/janus_hydra_semantic_ingestor.md`](docs/janus_hydra_semantic_ingestor.md): the ten-head Janus Hydra semantic reader


