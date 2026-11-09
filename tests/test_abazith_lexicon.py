import collections, json, pathlib, sys, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import abazith_lexicon as a

DOC = json.loads((ROOT / "data/abazith/symbols.json").read_text(encoding="utf-8"))

class TestAbazithLexicon(unittest.TestCase):
    def test_committed_json_is_exact_conversion_of_raw_source(self):
        self.assertEqual(a.build(ROOT / "data/abazith/source/symbols_raw.txt"), DOC)

    def test_structurally_valid(self):
        self.assertEqual(a.problems(DOC), [])

    def test_pinned_counts(self):
        S = DOC["symbols"]
        self.assertEqual(len(S), 204)
        self.assertEqual(len({s["family"] for s in S}), 24)
        self.assertEqual(dict(collections.Counter(s["mode"] for s in S)),
                         {"physical": 124, "energetic": 64, "essential": 10, "semi-physical": 2, "semi-energetic": 4})

    def test_no_numeric_v8_fields_are_claimed(self):
        # The source has no phonetic weight / fractal index / chirality / V8 values; none may appear.
        self.assertEqual(set(DOC["fields_absent"]), {"phonetic_weight", "fractal_index", "chirality", "v8_coordinates"})
        for s in DOC["symbols"]:
            self.assertFalse(any(isinstance(v, (int, float)) for v in s.values()))

    def test_observed_suffix_mode_regularity_and_its_single_exception(self):
        # Multi-letter codes ending in A are physical and ending in E are energetic, except AE (essential).
        for s in DOC["symbols"]:
            c = s["code"]
            if len(c) > 1 and c not in ("HU", "TU", "AE"):
                self.assertEqual(s["mode"], "physical" if c.endswith("A") else "energetic", s["name"])
        self.assertEqual([s["name"] for s in DOC["symbols"] if s["code"] == "AE"], ["Aenara"])

    def test_validator_rejects_corruption(self):
        bad = json.loads(json.dumps(DOC)); bad["symbols"][1]["name"] = bad["symbols"][0]["name"]
        self.assertTrue(a.problems(bad))
        bad = json.loads(json.dumps(DOC)); bad["symbols"][0]["mode"] = "mystical"
        self.assertTrue(a.problems(bad))
        with self.assertRaises(ValueError): a.parse_raw("A\n\nOnlyName\n")

if __name__ == "__main__": unittest.main()
