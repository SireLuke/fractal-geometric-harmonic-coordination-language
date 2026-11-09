# FGHCL foundation

## Current scope

FGHCL (Fractal Geometric Harmonic Coordination Language) is the project language and typed data model. Abazith is its human-readable notation. The implemented v0.1 parser accepts versioned V8 state records and provides tokenization, AST construction, schema/version checks, and canonical serialization.

The parser does not execute geometry, translate Janus Hydra records, calculate UHFE/UDFE, or validate physical claims. Draft concepts are proposals until specified and implemented.

## V8 record

The parser uses the versioned eight-coordinate state schema:

`(h, R, u, d, tau, chi, s, f)`

Each coordinate has the semantics declared by the selected profile. In the current `v8-core-1` profile, `tau` is a temporal offset normalized against a declared reference window. The letter `T` is only a provisional alias when explicitly declared; persistence is a separate concept.

The parser preserves declared values and metadata. It does not derive coordinates from Abazith symbols. The machine-readable lexicon contains descriptive fields only.

## Repository boundaries

- The FGHCL parser handles the supported Abazith state-record syntax.
- The PAN V8 contract defines coordinate order and semantics.
- The UHFE/UDFE repository contains mathematical and software contracts for those representations.
- The PANoRAMic.os and RelayWorks repositories provide application and backend code.

These repositories have distinct interfaces. A concept becomes a software capability only when an implemented interface and its validation criteria exist.