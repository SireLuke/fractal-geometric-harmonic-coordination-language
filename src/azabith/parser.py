"""Tokenizer, typed AST, parser, and canonical serializer for Azabith v0.1.

The implementation intentionally supports only the frozen V8 state grammar.
It does not execute JOBF, Janus Hydra, UHFE, or UDFE operations.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import math
import re
from typing import Optional, Union


LANGUAGE_VERSION = "0.1"
V8_SEMANTICS = "v8-core-1"
COORDINATE_ORDER = ("h", "R", "u", "d", "tau", "chi", "s", "f")
SUPPORTED_UNITS = frozenset({"1", "%", "m", "s", "ms", "rad", "deg", "Hz", "kg"})


class AzabithError(ValueError):
    """Raised when an Azabith document is lexically or semantically invalid."""


@dataclass(frozen=True)
class Coordinate:
    name: str
    value: float
    unit: Optional[str] = None
    uncertainty: Optional[Union[float, str]] = None


@dataclass(frozen=True)
class State:
    state_id: str
    semantics: str
    coordinates: tuple[Coordinate, ...]
    metadata: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class Document:
    language_version: str
    state: State


@dataclass(frozen=True)
class Token:
    kind: str
    value: str
    offset: int


_TOKEN_RE = re.compile(
    r"""
    (?P<SPACE>\s+)
  | (?P<COMMENT>\#[^\n]*)
  | (?P<STRING>"(?:\\.|[^"\\])*")
  | (?P<NUMBER>-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?)
  | (?P<PUNCT>[{}:])
  | (?P<IDENT>[A-Za-z_][A-Za-z0-9_.-]*)
    """,
    re.VERBOSE,
)


def _tokenize(source: str) -> list[Token]:
    tokens: list[Token] = []
    pos = 0
    while pos < len(source):
        match = _TOKEN_RE.match(source, pos)
        if match is None:
            raise AzabithError(f"Unexpected character at offset {pos}: {source[pos]!r}")
        kind = match.lastgroup
        value = match.group()
        if kind not in {"SPACE", "COMMENT"}:
            tokens.append(Token(kind or "", value, pos))
        pos = match.end()
    tokens.append(Token("EOF", "", len(source)))
    return tokens


class _Parser:
    def __init__(self, source: str):
        self.tokens = _tokenize(source)
        self.index = 0

    @property
    def current(self) -> Token:
        return self.tokens[self.index]

    def _take(self, kind: str, value: Optional[str] = None) -> Token:
        token = self.current
        if token.kind != kind or (value is not None and token.value != value):
            expected = value if value is not None else kind
            raise AzabithError(
                f"Expected {expected!r} at offset {token.offset}, "
                f"found {token.value or token.kind!r}"
            )
        self.index += 1
        return token

    def _keyword(self, value: str) -> None:
        self._take("IDENT", value)

    def _string(self) -> str:
        token = self._take("STRING")
        try:
            value = json.loads(token.value)
        except json.JSONDecodeError as exc:
            raise AzabithError(f"Invalid string at offset {token.offset}") from exc
        if not isinstance(value, str):
            raise AzabithError(f"Expected string at offset {token.offset}")
        return value

    def _number(self) -> float:
        token = self._take("NUMBER")
        value = float(token.value)
        if not math.isfinite(value):
            raise AzabithError(f"Number must be finite at offset {token.offset}")
        return value

    def parse(self) -> Document:
        self._keyword("language")
        self._take("IDENT", "FGHCL.Azabith")
        self._keyword("version")
        language_version = self._string()
        if language_version != LANGUAGE_VERSION:
            raise AzabithError(
                f"Unsupported Azabith language version {language_version!r}; "
                f"expected {LANGUAGE_VERSION!r}"
            )

        self._keyword("state")
        self._take("IDENT", "V8")
        state_id = self._string()
        self._keyword("semantics")
        semantics = self._string()
        if semantics != V8_SEMANTICS:
            raise AzabithError(
                f"Unsupported V8 semantic profile {semantics!r}; "
                f"expected {V8_SEMANTICS!r}"
            )

        self._take("PUNCT", "{")
        coordinates: dict[str, Coordinate] = {}
        metadata: dict[str, str] = {}

        while not (self.current.kind == "PUNCT" and self.current.value == "}"):
            if self.current.kind == "EOF":
                raise AzabithError("Unterminated V8 state block")
            if self.current.kind != "IDENT":
                raise AzabithError(
                    f"Expected coordinate or metadata at offset {self.current.offset}"
                )

            if self.current.value == "meta":
                self._keyword("meta")
                key = self._take("IDENT").value
                if key in metadata:
                    raise AzabithError(f"Duplicate metadata key {key!r}")
                self._take("PUNCT", ":")
                metadata[key] = self._string()
                continue

            name = self._take("IDENT").value
            if name not in COORDINATE_ORDER:
                raise AzabithError(f"Unknown V8 coordinate {name!r}")
            if name in coordinates:
                raise AzabithError(f"Duplicate V8 coordinate {name!r}")
            self._take("PUNCT", ":")
            value = self._number()
            unit: Optional[str] = None
            uncertainty: Optional[Union[float, str]] = None

            if self.current.kind == "IDENT" and self.current.value == "unit":
                self._keyword("unit")
                unit = self._string()
                if unit not in SUPPORTED_UNITS:
                    raise AzabithError(f"Unsupported unit {unit!r} for coordinate {name!r}")

            if self.current.kind == "IDENT" and self.current.value == "uncertainty":
                self._keyword("uncertainty")
                if self.current.kind == "IDENT" and self.current.value == "unknown":
                    self._keyword("unknown")
                    uncertainty = "unknown"
                else:
                    uncertainty = self._number()
                    if uncertainty < 0:
                        raise AzabithError("Uncertainty must be non-negative")

            coordinates[name] = Coordinate(name, value, unit, uncertainty)

        self._take("PUNCT", "}")
        self._take("EOF")

        missing = [name for name in COORDINATE_ORDER if name not in coordinates]
        if missing:
            raise AzabithError(f"Missing required V8 coordinates: {', '.join(missing)}")

        ordered = tuple(coordinates[name] for name in COORDINATE_ORDER)
        return Document(
            language_version=language_version,
            state=State(
                state_id=state_id,
                semantics=semantics,
                coordinates=ordered,
                metadata=tuple(sorted(metadata.items())),
            ),
        )


def parse(source: str) -> Document:
    """Parse a complete Azabith v0.1 V8 state document."""
    return _Parser(source).parse()


def _format_number(value: float) -> str:
    if not math.isfinite(value):
        raise AzabithError("Cannot serialize a non-finite number")
    if value == 0:
        return "0"
    return format(value, ".15g")


def serialize(document: Document) -> str:
    """Serialize an AST to deterministic canonical Azabith source."""
    if document.language_version != LANGUAGE_VERSION:
        raise AzabithError("Cannot serialize an unsupported language version")
    if document.state.semantics != V8_SEMANTICS:
        raise AzabithError("Cannot serialize an unsupported V8 semantic profile")

    by_name = {coordinate.name: coordinate for coordinate in document.state.coordinates}
    if len(by_name) != len(document.state.coordinates):
        raise AzabithError("Cannot serialize duplicate coordinates")
    if set(by_name) != set(COORDINATE_ORDER):
        raise AzabithError("Cannot serialize incomplete V8 state")

    lines = [
        f'language FGHCL.Azabith version {json.dumps(document.language_version)}',
        "",
        (
            f'state V8 {json.dumps(document.state.state_id, ensure_ascii=False)} '
            f'semantics {json.dumps(document.state.semantics)} {{'
        ),
    ]
    for name in COORDINATE_ORDER:
        coordinate = by_name[name]
        line = f"  {name}: {_format_number(coordinate.value)}"
        if coordinate.unit is not None:
            if coordinate.unit not in SUPPORTED_UNITS:
                raise AzabithError(f"Unsupported unit {coordinate.unit!r}")
            line += f" unit {json.dumps(coordinate.unit)}"
        if coordinate.uncertainty is not None:
            if coordinate.uncertainty == "unknown":
                line += " uncertainty unknown"
            else:
                uncertainty = float(coordinate.uncertainty)
                if not math.isfinite(uncertainty) or uncertainty < 0:
                    raise AzabithError("Uncertainty must be finite and non-negative")
                line += f" uncertainty {_format_number(uncertainty)}"
        lines.append(line)

    for key, value in sorted(document.state.metadata):
        lines.append(f"  meta {key}: {json.dumps(value, ensure_ascii=False)}")
    lines.append("}")
    return "\n".join(lines) + "\n"
