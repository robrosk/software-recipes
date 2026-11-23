"""One-line YAML scalars, checked against the YAML spec with the stdlib only.

SKILL.md frontmatter is read by real YAML parsers in every harness, so a
value this repo accepts must also be a value YAML accepts. A plain
(unquoted) scalar cannot hold ': ' or ' #', cannot end with ':' and cannot
start with an indicator character; any of those makes YAML read a new
mapping, a comment, an anchor and so on. Quote such a value instead.

Double-quoted values are read as JSON strings, which are a strict subset of
YAML double-quoted scalars. Single-quoted values escape a quote as ''.
"""

from __future__ import annotations

import json

# Characters that may never open a plain scalar (YAML 1.2, c-indicator).
_ALWAYS_INDICATOR = frozenset(",[]{}#&*!|>'\"%@`")
# '-', '?' and ':' open a plain scalar only when a non-space follows.
_SPACED_INDICATOR = frozenset("-?:")


class ScalarError(ValueError):
    """Raised when a value is not a valid one-line YAML scalar."""


def parse_scalar(text: str) -> str:
    """Return the string a YAML parser reads from `text`, or raise ScalarError."""
    text = text.strip()
    if text.startswith('"'):
        return _double_quoted(text)
    if text.startswith("'"):
        return _single_quoted(text)
    return _plain(text)


def _double_quoted(text: str) -> str:
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ScalarError(f"bad double-quoted value ({exc.msg}); escape an inner \" as \\\"") from None


def _single_quoted(text: str) -> str:
    inner = text[1:-1] if len(text) >= 2 and text.endswith("'") else None
    if inner is None or "'" in inner.replace("''", ""):
        raise ScalarError("bad single-quoted value; close it with ' and write an inner ' as ''")
    return inner.replace("''", "'")


def _plain(text: str) -> str:
    if not text:
        return text
    first, second = text[0], text[1:2]
    if first in _ALWAYS_INDICATOR or (first in _SPACED_INDICATOR and second in ("", " ", "\t")):
        raise ScalarError(f"unquoted value cannot start with {first!r}; wrap it in double quotes")
    if ": " in text or ":\t" in text or text.endswith(":"):
        raise ScalarError("unquoted value cannot contain ': ' or end with ':'; wrap it in double quotes")
    if " #" in text or "\t#" in text:
        raise ScalarError("unquoted value cannot contain ' #' (YAML reads a comment); wrap it in double quotes")
    return text
