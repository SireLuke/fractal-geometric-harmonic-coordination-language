# FHCL foundation (v0.1): reconciliation with canonical definitions

`FHCL_foundation.md` is left **unchanged**. This note records where its wording differs from the canonical V8 contract (`univeral-harmonic-field-equations.`, `docs/v8_contract.md`) so a later revision can be made deliberately.

| Item | FHCL v0.1 says | Canonical contract says |
|---|---|---|
| h | harmonic phase | harmonic coherence, [0,1] |
| r | recursion depth | **R**, recursive depth, [0,1] after normalization (uppercase) |
| u | UHFE polarity | constructive polarity |
| d | UDFE polarity | decoherence / entropy indicator |
| τ | temporal offset | temporal offset, normalized to a declared reference window; not a ninth coordinate |
| χ | chirality | chirality in [−1,1] (mapped to [0,1] by (χ+1)/2 for consumers that need it) |
| s | phonetic weight | information density |
| f | fractal index | fractal forcing index |
| Name | FHCL, "Fractal Harmonic Coordination Language" | **FGHCL**, Fractal Geometric Harmonic Coordination Language (FHCL deprecated) |
| UDFE | Universal Decoherence Field Equation | the UHFE repo says "Dissolution"; unresolved, needs the owner's decision |
| Repo table | lists `universal-harmonic-formula`, `fractal-harmonic-language` | current names: `univeral-harmonic-field-equations.` (trailing period), `fractal-geometric-harmonic-coordination-language` |

Note the FHCL glosses for `h`, `u`, `d`, `s`, `f` are not just renamings; they describe different quantities (for example a phase versus a coherence), so the symbol-to-vector derivation promised in FHCL §4 will need to be written against the canonical meanings.
