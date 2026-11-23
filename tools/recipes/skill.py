"""Skill model and SKILL.md loader.

Frontmatter is a deliberately small YAML subset: top-level `key: value`
scalars plus one nested `metadata:` map of scalars. Every harness parses
that subset the same way, so a skill that loads here loads everywhere.
Each value must also be a valid YAML scalar (see scalar.py), because the
harnesses read this block with real YAML parsers.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .scalar import ScalarError, parse_scalar

SKILLS_DIR = "skills"
SKILL_FILE = "SKILL.md"

_FENCE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?(.*)\Z", re.DOTALL)
_KEY_VALUE = re.compile(r"^([a-z][a-z0-9_-]*):(?:\s+(.*))?$")


class FrontmatterError(ValueError):
    """Raised when SKILL.md frontmatter falls outside the supported subset."""


@dataclass(frozen=True)
class Skill:
    """One skill folder: `skills/<name>/SKILL.md` plus its siblings."""

    directory: Path
    frontmatter: dict[str, str]
    metadata: dict[str, str]
    body: str
    raw: str = field(repr=False)

    @property
    def name(self) -> str:
        return self.frontmatter.get("name", "")

    @property
    def description(self) -> str:
        return self.frontmatter.get("description", "")

    @property
    def user_invoked(self) -> bool:
        """True when only the human may fire it (Claude: disable-model-invocation)."""
        return self.frontmatter.get("disable-model-invocation", "false") == "true"

    @property
    def display_name(self) -> str:
        return self.metadata.get("display-name") or self.name.replace("-", " ").title()

    @property
    def short_description(self) -> str:
        return self.metadata.get("short-description") or self.description

    @property
    def skill_file(self) -> Path:
        return self.directory / SKILL_FILE


def _scalar(value: str, key: str, lineno: int) -> str:
    try:
        return parse_scalar(value)
    except ScalarError as exc:
        raise FrontmatterError(f"line {lineno}: '{key}': {exc}") from None


def parse_frontmatter(text: str) -> tuple[dict[str, str], dict[str, str], str]:
    """Split SKILL.md text into (frontmatter, metadata, body)."""
    match = _FENCE.match(text)
    if not match:
        raise FrontmatterError("no '---' frontmatter block at the top of the file")
    header, body = match.groups()

    top: dict[str, str] = {}
    metadata: dict[str, str] = {}
    in_metadata = False
    for lineno, line in enumerate(header.splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        nested = line.startswith("  ")
        found = _KEY_VALUE.match(line.strip())
        if not found:
            raise FrontmatterError(f"line {lineno}: expected 'key: value', got {line!r}")
        key, value = found.group(1), found.group(2)
        if nested:
            if not in_metadata:
                raise FrontmatterError(f"line {lineno}: only 'metadata:' may hold nested keys")
            metadata[key] = _scalar(value or "", key, lineno)
            continue
        in_metadata = key == "metadata" and value is None
        if in_metadata:
            continue
        if value is None:
            raise FrontmatterError(f"line {lineno}: '{key}' has no value")
        if value.startswith(("[", "{", "|", ">")):
            raise FrontmatterError(f"line {lineno}: '{key}' must be a plain one-line scalar")
        top[key] = _scalar(value, key, lineno)
    return top, metadata, body


def load_skill(directory: Path) -> Skill:
    raw = (directory / SKILL_FILE).read_text(encoding="utf-8")
    try:
        frontmatter, metadata, body = parse_frontmatter(raw)
    except FrontmatterError as exc:
        raise FrontmatterError(f"{SKILLS_DIR}/{directory.name}/{SKILL_FILE}: {exc}") from None
    return Skill(directory=directory, frontmatter=frontmatter, metadata=metadata, body=body, raw=raw)


def discover_skills(root: Path) -> list[Skill]:
    """Every direct child of skills/ that holds a SKILL.md, sorted by folder name."""
    skills_dir = root / SKILLS_DIR
    folders = sorted(p for p in skills_dir.iterdir() if (p / SKILL_FILE).is_file())
    return [load_skill(folder) for folder in folders]
