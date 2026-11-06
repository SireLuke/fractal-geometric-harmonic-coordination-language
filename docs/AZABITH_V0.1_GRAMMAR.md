# Azabith v0.1 — Frozen State Grammar

**Status:** parser-backed v0.1 subset  
**Language:** FGHCL (host language)  
**Notation:** Azabith  
**Scope:** the first executable grammar covers the versioned V8 state record. It does not yet parse JOBF sequences, Janus Hydra translation blocks, UHFE/UDFE pair expressions, geometry declarations, or cymatics records.

## 1. Architecture and semantic boundaries

- **FGHCL** is the host language and typed data model.
- **Azabith** is its human-readable notation.
- **V8** is the versioned eight-coordinate state schema.
- **JOBF** names geometric operations; it is not the state schema.
- **Janus Hydra** is the fractal-geometric translator; it is neither UHFE nor UDFE.
- **UHFE / UDFE** are the paired formation / dissolution representations downstream of translation.

The parser only constructs and validates source records. It does not execute geometry, perform Janus translation, calculate UHFE/UDFE, or assert physical validity.

## 2. Canonical V8 semantic profile

The v0.1 profile identifier is `v8-core-1`, with coordinate order:

`(h, R, u, d, tau, chi, s, f)`

| Field | Meaning |
|---|---|
| `h` | Harmonic Coherence |
| `R` | Recursive Depth |
| `u` | Constructive Polarity |
| `d` | Decoherence / entropy |
| `tau` | Temporal Persistence |
| `chi` | Chirality / Orientation |
| `s` | Information Density |
| `f` | Forcing / Fractal Forcing Index |

This profile does not silently absorb legacy coordinate interpretations. A different meaning requires a different semantic profile/version and a separately specified migration. The parser rejects unknown semantic profile identifiers rather than guessing.

## 3. EBNF

The grammar below describes the supported v0.1 state document. Whitespace and comments are insignificant. A comment begins with `#` and continues to the end of the line.

```ebnf
document       = language_decl, state_decl, EOF ;
language_decl  = "language", "FGHCL.Azabith", "version", string ;
state_decl     = "state", "V8", string, "semantics", string,
                 "{", { state_member }, "}" ;
state_member   = coordinate | metadata ;
coordinate     = coordinate_name, ":", number,
                 [ "unit", string ],
                 [ "uncertainty", uncertainty_value ] ;
metadata       = "meta", identifier, ":", string ;
coordinate_name = "h" | "R" | "u" | "d" | "tau" | "chi" | "s" | "f" ;
uncertainty_value = number | "unknown" ;
number         = [ "-" ], digit, { digit }, [ ".", digit, { digit } ],
                 [ ("e" | "E"), [ "+" | "-" ], digit, { digit } ] ;
identifier     = letter, { letter | digit | "_" | "-" } ;
string         = JSON-compatible quoted string ;
```

A coordinate may appear exactly once. All eight coordinates are required. Coordinate order in source is flexible; canonical serialization always uses the registry order shown above.

## 4. Typed value and metadata rules

- Coordinate values are finite numbers. The parser does not impose a universal `[0,1]` range.
- A coordinate unit is optional; omission means **unspecified**, not dimensionless. When present, it must be one of: `1`, `%`, `m`, `s`, `ms`, `rad`, `deg`, `Hz`, `kg`.
- This v0.1 unit list is a syntax/type allowlist, not a claim that every unit is meaningful for every coordinate. Coordinate-specific dimensional constraints remain future work.
- Uncertainty is either a finite non-negative numeric value or the literal `unknown`. Omission means not supplied; it is distinct from `unknown`.
- Metadata keys are unique within a state and values are strings. Metadata is preserved exactly as text; the parser does not infer provenance semantics from a key.
- Duplicate coordinates, duplicate metadata keys, unknown coordinates, unknown units, malformed numbers, missing coordinates, trailing tokens, and version/profile mismatches are errors.
- Missing, zero, and unknown are never conflated.

## 5. Canonical serialization

Canonical output uses:
1. the exact language header;
2. the V8 coordinates in canonical registry order;
3. normalized finite numeric formatting (no redundant trailing zeroes);
4. optional unit and uncertainty clauses in that order;
5. metadata sorted lexicographically by key;
6. two-space indentation and a final newline.

For every accepted AST, `parse(serialize(ast))` must produce an AST equal to the original AST. Source comments and whitespace are intentionally not preserved.

## 6. Example

```azabith
language FGHCL.Azabith version "0.1"

state V8 "state-0001" semantics "v8-core-1" {
  h: 0.82 unit "1" uncertainty 0.01
  R: 0.61
  u: 0.73
  d: 0.18
  tau: 0.54
  chi: 0.67
  s: 0.76
  f: 0.42
  meta source_kind: "illustrative"
  meta note: "Example only; not a measured physical state."
}
```

## 7. Compatibility and non-goals

The parser's acceptance of a document establishes syntactic and declared-schema conformance only. It does not validate metric provenance, physical interpretation, E8/Gosset geometry, JOBF invariants, Janus transforms, UHFE/UDFE mappings, or any physical model. Those require independent specifications and tests.
