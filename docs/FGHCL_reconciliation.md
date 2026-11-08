# FGHCL foundation (v0.1): reconciliation with canonical definitions

`FGHCL_foundation.md` is left **unchanged**. This note records where its wording differs from the canonical V8 contract (`univeral-harmonic-field-equations.`, `docs/v8_contract.md`) so a later revision can be made deliberately.

| Item | FGHCL_foundation.md v0.1 says | Canonical contract says |
|---|---|---|
| h | harmonic phase | harmonic coherence, [0,1] |
| r | recursion depth | **R**, recursive depth, [0,1] after normalization (uppercase) |
| u | UHFE polarity | constructive polarity |
| d | UDFE polarity | decoherence / entropy indicator |
| τ | temporal offset | temporal offset, normalized to a declared reference window; not a ninth coordinate |
| χ | chirality | chirality in [−1,1] (mapped to [0,1] by (χ+1)/2 for consumers that need it) |
| s | phonetic weight | information density |
| f | fractal index | fractal forcing index |
| Name | the file is now `FGHCL_foundation.md`, but its body still says "Fractal Harmonic Coordination Language (FHCL)" and "FHCL" in places | **FGHCL**, Fractal Geometric Harmonic Coordination Language (FHCL deprecated) |
| UDFE | foundation: "Universal Decoherence Field Equation" | **Canonical (owner decision): Universal Decoherence Field Equation.** The FGHCL README/spec and the UHFE repository previously said "dissolution"; updated to "decoherence" in prose. Code identifiers and stored strings that contain "dissolution" (e.g. `pair.dissolution`, `UDFE_dissolution`) are unchanged pending a deliberate API rename. `d` is a model coordinate, not quantum decoherence. |
| Repo table | lists `universal-harmonic-formula`, `fractal-harmonic-language` | current names: `univeral-harmonic-field-equations.` (trailing period), `fractal-geometric-harmonic-coordination-language` |

Note the foundation's glosses for `h`, `u`, `d`, `s`, `f` are not just renamings; they describe different quantities (for example a phase versus a coherence), so the symbol-to-vector derivation promised in FHCL §4 will need to be written against the canonical meanings.
