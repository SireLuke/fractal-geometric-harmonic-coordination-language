# Abazith lexicon (machine-readable)

`symbols.json` is a mechanical conversion of the user-supplied text export in `source/symbols_raw.txt` (which was a plain-text file named `.json`). Regenerate with `python tools/abazith_lexicon.py`; `python -m unittest discover -s tests -v` checks the committed JSON is exactly that conversion.

**Contents:** 204 symbols, 24 families, modes: physical 124, energetic 64, essential 10, semi-physical 2, semi-energetic 4. Each entry: `name`, `section` (first letter), `gloss` (a one-line description of a feeling), `code` (prefix), `family`, `mode`.

**What this is not.** The source has **no numeric fields**. `FGHCL_foundation.md` (v0.1) says each symbol has a phonetic weight, fractal index and chirality signature; none exist in this data, and `fields_absent` records that. No V8 coordinates are derived here. Any symbol → V8 mapping must be a separately stated, versioned rule.

## Checks (all pass)
Unique names; section equals first letter; the code is a prefix of the name; each code belongs to exactly one family; modes in a fixed vocabulary. Informational (not errors): the closest gloss pairs by wording are Bemara/Vemara (0.75 similarity), Jana/Mavena (0.74), Chehana/Leya (0.71), Jahena/Waja (0.70; same idea, different wording).

## Observed regularities in the data (not rules)
Multi-letter codes ending in `A` are physical (117 symbols) and in `E` energetic (64), with one exception: `AE` (Aenara) is essential. Single-letter codes are `A` physical (7), `O` essential (9), `I` semi-energetic (4); `HU` and `TU` are semi-physical. The code `I` (family Mass & Energy) is distinct from `IA`/`IE` (family Mass into Energy); confirm this is intended.
