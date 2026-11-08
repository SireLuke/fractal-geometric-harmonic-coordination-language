# Janus Hydra Semantic Ingestor (ten-head geometric semantic reader)

**Status:** Descriptive specification of an implemented computational layer (`hydra_semantic_reader.py`, `janus_hydra.py` in `pan-fractal-kernel`). Engineering construct, not a physical field theory.
**Baseline rule:** `JANUS-HYDRA-DYNAMIC-INVERSE-v1` (formal definition: `univeral-harmonic-field-equations.`, `docs/janus_hydra_dynamic_inverse_v1.md`).
**"Ten":** the ingestor emits **ten heads**: five UHFE (formation) and five UDFE (inverse), explicitly paired. (If "10" was meant as version 1.0, the baseline above is that version's identifier.)

## 1. Where it sits in FGHCL

In the four-layer stack of `FGHCL_foundation.md`, the ingestor is the **symbol/semantic → 8D vector → field** gateway between the language layer and the processor layer. It is the single reader through which sources reach V8, JOBF and the data adapters; downstream code consumes its frame and must not re-implement the head mappings.

`source / calibrated semantic input → coerce_v8_state → ten Janus heads → paired-head records → two eight-channel projections → JOBF / adapters`

Janus Hydra is the translator. It is **not** the V8 manifold and **not** UHFE or UDFE: V8 is the input state, UHFE the formation-side output, UDFE the inverse-side output. These layers stay separate.

## 2. Input contract

Accepts exactly one of: a `V8State`; a mapping with the exact keys `h, R, u, d, tau, chi, s, f`; an ordered 8-value sequence in that order. The provisional alias `T` is accepted for `tau` only if `tau` is absent. All eight values must be finite and in **[0,1]**. Missing keys, extra keys, wrong length, NaN/inf and out-of-range values are **rejected, never clamped**. Chirality must arrive already mapped to [0,1] (χ₀₁ = (χ+1)/2); the reader does not map it.

## 3. The ten heads

| Pair | UHFE head (support) | UDFE inverse head (support) |
|---|---|---|
| Bubble | `bubble` (h, R, u) | `antibubble_cavitation` (d, u, h) |
| Honeycomb | `honeycomb` (τ, s) | `inversehoneycomb` (d, τ, s) |
| SpiderWeb | `spiderweb` (f, h, R) | `inversespiderweb_radialvoid` (d, f, h, R) |
| ChiralDNA | `chiraldna` (χ, τ, R) | `chiralvoid` (d, χ, τ, R) |
| CompoundEye | `compoundeye` (s, h, d) | `discretesingulardots_inversecompoundeye` (d, s, h) |

Formulas: UHFE as in the UHFE repository; UDFE inverse heads use complements 1−x (an involution) plus `d` in **every** inverse head. Inverse names are deliberately not renamed to match the UHFE keys; the pairing is explicit and each pair record carries `inverse_rule = JANUS-HYDRA-DYNAMIC-INVERSE-v1`.

## 4. Output frame (`HydraSemanticFrame`, frozen)

`state`, `uhfe_heads` (5), `udfe_heads` (5), `paired_heads` (per pair: `formation`, `inverse`, `inverse_rule`), `uhfe_channels` (8), `udfe_channels` (8), `coordinate_order`, `reader`, `schema_version`.

**Channel projection.** For each coordinate, the channel value is the arithmetic mean of the scores of all heads whose support includes that coordinate; every coordinate must be covered (the reader raises if not). Head counts per coordinate (h, R, u, d, τ, χ, s, f):

- UHFE channels: 3, 3, 1, 1, 2, 1, 2, 1
- UDFE channels: 3, 2, 1, **5**, 2, 1, 2, 1

Hence under v1 the `d` channel of UDFE is the mean of all five inverse heads, while UHFE's `d` channel sees one head. The two projections are independent; no relation U_D = 1 − U_H is imposed.

## 5. Interface with Azabith v0.1 (as of the current parser)

The Azabith parser (`src/azabith`) reads a `state V8 ... semantics "v8-core-1"` record into typed coordinates in canonical order, each with an optional unit (one of `1, %, m, s, ms, rad, deg, Hz, kg`) and uncertainty. Per `docs/AZABITH_V0.1_GRAMMAR.md` it requires finite numbers and **does not impose a [0,1] range**. The reader above requires unitless values in [0,1] with χ already mapped. So between a parsed Azabith state and this ingestor there must be an explicit, declared normalization step (native domain, unit, transform) that does **not yet exist**; the reader will reject, not clamp, anything outside [0,1]. Janus translation blocks and UHFE/UDFE expressions are not parsed by Azabith v0.1 yet.

## 6. Guarantees and non-guarantees

- Exactly 5 + 5 heads, two 8-channel projections over the same validated state; both projections finite.
- The semantic mapping is unchanged by the choice of downstream geometry (JOBF's production boundary is the Gosset 4₂₁ hull; the 8D cross-polytope is a comparison baseline only).
- Numerical conformance validates implementation invariants, not a physical interpretation.
- Dataset adapters (Gaia DR3, GRMHD) produce **provisional proxy V8 vectors**; those are engineering assumptions and must pass through this reader with source values and provenance retained.

## 7. Open items

- An FGHCL grammar for *how symbols produce V8 vectors* (Abazith → h, R, u, d, τ, χ, s, f) is still unspecified; this document covers only what happens after a V8 state exists.
- See `FGHCL_reconciliation.md` for older wording in `FGHCL_foundation.md` that differs from the canonical definitions.
