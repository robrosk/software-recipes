"""Validation rules. Each rule is a small pure function: Skill -> issues.

Add a rule by writing a function and appending it to RULES. Nothing else
changes (open/closed, rules as a list of strategies).
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable, Iterator
from dataclasses import dataclass

from .skill import Skill

MAX_NAME = 64
MAX_DESCRIPTION = 1024  # Agent Skills standard limit
MAX_BODY_LINES = 500  # past this, disclose reference into references/
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MD_LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
TRIGGER_PHRASE = re.compile(r"\buse when\b", re.IGNORECASE)
EM_DASH = "—"


@dataclass(frozen=True)
class Issue:
    level: str  # "error" fails the build, "warning" is printed only
    where: str
    message: str

    def __str__(self) -> str:
        return f"{self.level}: {self.where}: {self.message}"


Rule = Callable[[Skill], Iterator[Issue]]


def _where(skill: Skill) -> str:
    return f"skills/{skill.directory.name}/SKILL.md"


def name_is_valid(skill: Skill) -> Iterator[Issue]:
    if not KEBAB.match(skill.name) or len(skill.name) > MAX_NAME:
        yield Issue("error", _where(skill), f"name must be kebab-case, at most {MAX_NAME} chars")
    if skill.name != skill.directory.name:
        yield Issue("error", _where(skill), "name must match its folder name")


def description_is_valid(skill: Skill) -> Iterator[Issue]:
    text = skill.description.strip()
    if not text:
        yield Issue("error", _where(skill), "description is required")
    elif len(text) > MAX_DESCRIPTION:
        yield Issue("error", _where(skill), f"description is over {MAX_DESCRIPTION} chars")


def description_matches_invocation(skill: Skill) -> Iterator[Issue]:
    """Model-invoked: model-facing triggers. User-invoked: human-facing summary."""
    has_trigger = bool(TRIGGER_PHRASE.search(skill.description))
    if skill.user_invoked and has_trigger:
        yield Issue("warning", _where(skill), "user-invoked skill: drop 'Use when' triggers")
    if not skill.user_invoked and not has_trigger:
        yield Issue("warning", _where(skill), "model-invoked skill: add 'Use when ...' triggers")


def body_is_short(skill: Skill) -> Iterator[Issue]:
    lines = skill.body.count("\n")
    if lines > MAX_BODY_LINES:
        yield Issue("warning", _where(skill), f"{lines} lines; move reference into references/")


def links_resolve(skill: Skill) -> Iterator[Issue]:
    for target in MD_LINK.findall(skill.body):
        if "://" in target:
            continue
        if not (skill.directory / target).exists():
            yield Issue("error", _where(skill), f"link target missing: {target}")


def no_em_dashes(skill: Skill) -> Iterator[Issue]:
    if EM_DASH in skill.raw:
        yield Issue("error", _where(skill), "em dash found; rewrite with a comma, colon or period")


def no_symlinks(skill: Skill) -> Iterator[Issue]:
    """Codex copies plugins into its cache and drops symlinks."""
    for path in skill.directory.rglob("*"):
        if path.is_symlink():
            yield Issue("error", _where(skill), f"symlink not allowed: {path.name}")


def evals_are_well_formed(skill: Skill) -> Iterator[Issue]:
    path = skill.directory / "evals" / "triggers.json"
    if not path.exists():
        if not skill.user_invoked:
            yield Issue("warning", _where(skill), "no evals/triggers.json for a model-invoked skill")
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        yield Issue("error", _where(skill), f"evals/triggers.json: {exc}")
        return
    for key in ("should_trigger", "should_not_trigger"):
        if not isinstance(data.get(key), list) or not data[key]:
            yield Issue("error", _where(skill), f"evals/triggers.json needs a non-empty '{key}' list")


RULES: tuple[Rule, ...] = (
    name_is_valid,
    description_is_valid,
    description_matches_invocation,
    body_is_short,
    links_resolve,
    no_em_dashes,
    no_symlinks,
    evals_are_well_formed,
)


def validate(skills: list[Skill], rules: tuple[Rule, ...] = RULES) -> list[Issue]:
    issues = [issue for skill in skills for rule in rules for issue in rule(skill)]
    names = [s.name for s in skills]
    issues += [Issue("error", "skills/", f"duplicate skill name: {n}") for n in set(names) if names.count(n) > 1]
    return issues
