"""Convert and validate the Abazith lexicon. Standard library only.

Raw format (user-supplied text export): single capital-letter section headers; then
repeating triples of non-empty lines: NAME / GLOSS / CODE·FAMILY (mode).
"""
import json, re, sys, pathlib, difflib, collections

SCHEMA_ID = "abazith-lexicon-v1"
MODES = ("physical", "energetic", "essential", "semi-physical", "semi-energetic")
_CODE = re.compile(r"([A-Z]+)·(.+) \((.+)\)")

def parse_raw(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    out, i, section = [], 0, None
    while i < len(lines):
        if re.fullmatch(r"[A-Z]", lines[i]):
            section = lines[i]; i += 1; continue
        if i + 2 >= len(lines): raise ValueError(f"truncated entry at line {i}: {lines[i]!r}")
        name, gloss, tag = lines[i:i + 3]
        m = _CODE.fullmatch(tag)
        if not m: raise ValueError(f"bad code line for {name!r}: {tag!r}")
        code, family, mode = m.groups()
        out.append({"name": name, "section": section, "gloss": gloss, "code": code, "family": family, "mode": mode})
        i += 3
    return out

def build(raw_path):
    syms = parse_raw(pathlib.Path(raw_path).read_text(encoding="utf-8"))
    return {"schema": SCHEMA_ID, "count": len(syms),
            "provenance": "User-supplied plain-text export (data/abazith/source/symbols_raw.txt); converted mechanically, no values added.",
            "fields_absent": ["phonetic_weight", "fractal_index", "chirality", "v8_coordinates"],
            "symbols": syms}

def problems(doc):
    """Hard errors (list of str). Empty list means the document is structurally valid."""
    e, S = [], doc["symbols"]
    if doc.get("schema") != SCHEMA_ID: e.append("wrong schema id")
    if doc.get("count") != len(S): e.append("count mismatch")
    names = [s["name"] for s in S]
    if len(set(names)) != len(names): e.append("duplicate names")
    code_fam = collections.defaultdict(set)
    for s in S:
        if set(s) != {"name", "section", "gloss", "code", "family", "mode"}: e.append(f"{s.get('name')}: wrong keys")
        if s["mode"] not in MODES: e.append(f"{s['name']}: unknown mode {s['mode']!r}")
        if s["section"] != s["name"][0].upper(): e.append(f"{s['name']}: section {s['section']} != first letter")
        if not s["name"].lower().startswith(s["code"].lower()): e.append(f"{s['name']}: code {s['code']} is not a prefix of the name")
        if not s["gloss"].endswith("."): e.append(f"{s['name']}: gloss lacks terminal period")
        code_fam[s["code"]].add(s["family"])
    for c, f in code_fam.items():
        if len(f) != 1: e.append(f"code {c} spans families {sorted(f)}")
    return e

def near_duplicate_glosses(doc, threshold=0.8):
    """Informational only (not errors): pairs of different symbols whose glosses are very similar."""
    S, out = doc["symbols"], []
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            r = difflib.SequenceMatcher(None, S[i]["gloss"].lower(), S[j]["gloss"].lower()).ratio()
            if r >= threshold: out.append((S[i]["name"], S[j]["name"], round(r, 3)))
    return out

if __name__ == "__main__":
    root = pathlib.Path(__file__).resolve().parents[1] / "data" / "abazith"
    doc = build(root / "source" / "symbols_raw.txt")
    (root / "symbols.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote", doc["count"], "symbols; problems:", problems(doc))
