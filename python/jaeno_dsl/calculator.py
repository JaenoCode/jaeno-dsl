"""``calculator`` v1 pre-send validation.

Two things the generated Pydantic model can't check, ported faithfully from
``calculator_handler.dart`` so the bot rejects the same payloads the client
would fall back on:

1. **The field rules** — non-empty list, <= 8 entries, each ``key`` a unique
   identifier, ``choice`` fields with real options, etc. (The model enforces
   ``max_length=8`` on ``fields`` but nothing below that.)
2. **The formula grammar** — ``expr := term (('+'|'-') term)*`` … the whole
   restricted arithmetic language. An unparseable formula is still a
   well-formed JSON string, so the model sees nothing wrong with it.

``parse_calculator_formula`` mirrors the Dart parser token-for-token; keep the
two in lockstep if either grammar ever changes (it is versioned — a change is
a new ``calculator.v2``).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

MAX_FIELDS = 8  # schemas/calculator.v1.json `maxItems`, and calculator_handler.dart `_kMaxFields`


class FormulaError(ValueError):
    """The formula violates the restricted-arithmetic grammar."""


# ── formula grammar ─────────────────────────────────────────────────────────
#
#   expr    := term (('+' | '-') term)*
#   term    := factor (('*' | '/') factor)*
#   factor  := ('+' | '-')? primary
#   primary := NUMBER | IDENT | '(' expr ')'
#
# Everything else — '**', '^', '%', calls, attribute access, indexing,
# comparisons, ternaries, strings, commas, and any identifier not in
# `allowed_keys` — is a parse error.


def _is_ident_start(c: str) -> bool:
    return c.isascii() and (c.isalpha() or c == "_")


def _is_ident_part(c: str) -> bool:
    return _is_ident_start(c) or (c.isascii() and c.isdigit())


@dataclass(frozen=True)
class _Token:
    kind: str  # 'num' | 'ident' | 'op' | '(' | ')'
    text: str


def _tokenize(source: str) -> list[_Token]:
    tokens: list[_Token] = []
    i = 0
    n = len(source)
    while i < n:
        c = source[i]
        if c in " \t\n\r":
            i += 1
            continue
        if c in "()":
            tokens.append(_Token(c, c))
            i += 1
            continue
        if c in "+-*/":
            tokens.append(_Token("op", c))
            i += 1
            continue
        if (c.isascii() and c.isdigit()) or c == ".":
            start = i
            while i < n and ((source[i].isascii() and source[i].isdigit()) or source[i] == "."):
                i += 1
            text = source[start:i]
            try:
                float(text)
            except ValueError:
                raise FormulaError(f'invalid number "{text}" in formula') from None
            tokens.append(_Token("num", text))
            continue
        if _is_ident_start(c):
            start = i
            while i < n and _is_ident_part(source[i]):
                i += 1
            tokens.append(_Token("ident", source[start:i]))
            continue
        raise FormulaError(f'unexpected character "{c}" in formula')
    return tokens


class _Parser:
    def __init__(self, tokens: list[_Token], allowed_keys: set[str]) -> None:
        self.tokens = tokens
        self.allowed = allowed_keys
        self.refs: set[str] = set()
        self.pos = 0

    def parse(self) -> None:
        self._expr()
        if self.pos != len(self.tokens):
            raise FormulaError(f'unexpected "{self.tokens[self.pos].text}" in formula')

    def _is_op(self, text: str) -> bool:
        return (
            self.pos < len(self.tokens)
            and self.tokens[self.pos].kind == "op"
            and self.tokens[self.pos].text == text
        )

    def _expr(self) -> None:
        self._term()
        while self._is_op("+") or self._is_op("-"):
            self.pos += 1
            self._term()

    def _term(self) -> None:
        self._factor()
        while self._is_op("*") or self._is_op("/"):
            self.pos += 1
            self._factor()

    def _factor(self) -> None:
        if self._is_op("+") or self._is_op("-"):
            self.pos += 1
        self._primary()

    def _primary(self) -> None:
        if self.pos >= len(self.tokens):
            raise FormulaError("formula ends unexpectedly")
        tok = self.tokens[self.pos]
        if tok.kind == "num":
            self.pos += 1
            return
        if tok.kind == "ident":
            self.pos += 1
            if tok.text not in self.allowed:
                raise FormulaError(f'formula references unknown field "{tok.text}"')
            self.refs.add(tok.text)
            return
        if tok.kind == "(":
            self.pos += 1
            self._expr()
            if self.pos >= len(self.tokens) or self.tokens[self.pos].kind != ")":
                raise FormulaError("unbalanced parentheses in formula")
            self.pos += 1
            return
        raise FormulaError(f'unexpected "{tok.text}" in formula')


def parse_calculator_formula(source: str, allowed_keys: set[str]) -> set[str]:
    """Validate ``source`` against the grammar, rejecting any identifier not in
    ``allowed_keys``. Returns the set of field keys the formula references.
    Raises :class:`FormulaError` on anything the grammar doesn't cover."""
    parser = _Parser(_tokenize(source), allowed_keys)
    parser.parse()
    return parser.refs


# ── field rules ─────────────────────────────────────────────────────────────


def validate_calculator_data(data: dict[str, Any]) -> None:
    """Raise :class:`ValueError` if a ``calculator`` v1 ``data`` payload would
    be rejected by ``calculator_handler.dart``'s ``render()``."""
    raw_fields = data.get("fields")
    if not isinstance(raw_fields, list):
        raise ValueError('calculator: "fields" must be a list')
    if not raw_fields:
        raise ValueError('calculator: "fields" is empty')
    if len(raw_fields) > MAX_FIELDS:
        raise ValueError(f"calculator: {len(raw_fields)} fields exceeds the cap of {MAX_FIELDS}")

    seen: set[str] = set()
    keys: set[str] = set()
    for entry in raw_fields:
        if not isinstance(entry, dict):
            raise ValueError("calculator: field must be an object")
        key = entry.get("key")
        label = entry.get("label")
        ftype = entry.get("type")
        if not isinstance(key, str) or not key:
            raise ValueError('calculator: field needs a "key"')
        if not _is_ident_start(key[0]) or not all(_is_ident_part(ch) for ch in key):
            raise ValueError(f'calculator: field key "{key}" is not an identifier')
        if key in seen:
            raise ValueError(f'calculator: duplicate field key "{key}"')
        seen.add(key)
        keys.add(key)
        if not isinstance(label, str) or not label:
            raise ValueError(f'calculator: field "{key}" needs a "label"')
        if ftype not in ("number", "choice"):
            raise ValueError(f'calculator: field "{key}" has an unknown type')
        options = entry.get("options")
        if options is not None:
            if not isinstance(options, list):
                raise ValueError('calculator: "options" must be a list')
            for opt in options:
                if not isinstance(opt, dict):
                    raise ValueError("calculator: option must be an object")
                if not isinstance(opt.get("label"), str) or not opt["label"]:
                    raise ValueError('calculator: option needs a "label"')
                if not isinstance(opt.get("value"), (int, float)) or isinstance(
                    opt.get("value"), bool
                ):
                    raise ValueError('calculator: option "value" must be a number')
        if ftype == "choice" and not options:
            raise ValueError(f'calculator: choice field "{key}" has no options')

    formula = data.get("formula")
    if not isinstance(formula, str):
        raise ValueError('calculator: "formula" must be a string')
    parse_calculator_formula(formula, keys)
