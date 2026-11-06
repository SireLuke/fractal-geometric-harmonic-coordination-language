import unittest

from azabith import AzabithError, COORDINATE_ORDER, parse, serialize


VALID = '''language FGHCL.Azabith version "0.1"

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
  meta note: "preserve this text"
}
'''


class ParserConformanceTests(unittest.TestCase):
    def test_parses_typed_v8_state_in_canonical_order(self):
        document = parse(VALID)
        self.assertEqual(document.language_version, "0.1")
        self.assertEqual(document.state.semantics, "v8-core-1")
        self.assertEqual(tuple(c.name for c in document.state.coordinates), COORDINATE_ORDER)
        self.assertEqual(document.state.coordinates[0].unit, "1")
        self.assertEqual(document.state.coordinates[0].uncertainty, 0.01)
        self.assertEqual(dict(document.state.metadata)["source_kind"], "illustrative")

    def test_round_trip_is_ast_stable_and_serialization_canonical(self):
        first = parse(VALID)
        canonical = serialize(first)
        second = parse(canonical)
        self.assertEqual(first, second)
        self.assertTrue(canonical.endswith("\n"))
        self.assertLess(canonical.index("h:"), canonical.index("R:"))
        self.assertLess(canonical.index("meta note:"), canonical.index("meta source_kind:"))

    def test_comments_and_whitespace_are_ignored(self):
        source = VALID.replace("language FGHCL.Azabith", "# header comment\nlanguage   FGHCL.Azabith")
        self.assertEqual(parse(source), parse(VALID))

    def test_missing_coordinate_is_rejected_not_imputed_as_zero(self):
        source = VALID.replace("  f: 0.42\n", "")
        with self.assertRaisesRegex(AzabithError, "Missing required V8 coordinates: f"):
            parse(source)

    def test_duplicate_coordinate_is_rejected(self):
        source = VALID.replace("  f: 0.42", "  f: 0.42\n  f: 0.5")
        with self.assertRaisesRegex(AzabithError, "Duplicate V8 coordinate"):
            parse(source)

    def test_unknown_coordinate_is_rejected(self):
        source = VALID.replace("  f: 0.42", "  q: 0.42")
        with self.assertRaisesRegex(AzabithError, "Unknown V8 coordinate"):
            parse(source)

    def test_invalid_unit_is_rejected(self):
        source = VALID.replace('h: 0.82 unit "1"', 'h: 0.82 unit "parsec"')
        with self.assertRaisesRegex(AzabithError, "Unsupported unit"):
            parse(source)

    def test_uncertainty_unknown_is_distinct_from_absent(self):
        source = VALID.replace("  R: 0.61", "  R: 0.61 uncertainty unknown")
        document = parse(source)
        self.assertEqual(document.state.coordinates[1].uncertainty, "unknown")
        self.assertIsNone(parse(VALID).state.coordinates[1].uncertainty)

    def test_negative_uncertainty_is_rejected(self):
        source = VALID.replace("uncertainty 0.01", "uncertainty -0.01")
        with self.assertRaises(AzabithError):
            parse(source)

    def test_duplicate_metadata_is_rejected(self):
        source = VALID.replace(
            '  meta note: "preserve this text"',
            '  meta note: "preserve this text"\n  meta note: "duplicate"',
        )
        with self.assertRaisesRegex(AzabithError, "Duplicate metadata key"):
            parse(source)

    def test_metadata_values_are_preserved_exactly(self):
        document = parse(VALID)
        self.assertEqual(dict(document.state.metadata)["note"], "preserve this text")
        self.assertEqual(parse(serialize(document)), document)

    def test_language_version_mismatch_is_rejected(self):
        with self.assertRaisesRegex(AzabithError, "Unsupported Azabith language version"):
            parse(VALID.replace('version "0.1"', 'version "0.2"'))

    def test_v8_semantic_version_mismatch_is_rejected(self):
        with self.assertRaisesRegex(AzabithError, "Unsupported V8 semantic profile"):
            parse(VALID.replace('"v8-core-1"', '"legacy-v8-unversioned"'))

    def test_malformed_syntax_and_trailing_tokens_are_rejected(self):
        with self.assertRaises(AzabithError):
            parse(VALID.replace("h: 0.82", "h 0.82"))
        with self.assertRaisesRegex(AzabithError, "Expected 'EOF'"):
            parse(VALID + "unexpected")

    def test_unterminated_state_is_rejected(self):
        with self.assertRaisesRegex(AzabithError, "Unterminated"):
            parse(VALID.rsplit("}", 1)[0])


if __name__ == "__main__":
    unittest.main()
