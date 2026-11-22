"""The adapter contract: one core model in, one platform's files out."""

from __future__ import annotations

import json
from typing import Protocol

from ..config import PluginConfig
from ..skill import Skill

# Relative path (POSIX) -> file content. Pure data, so adapters stay testable.
Files = dict[str, str]


class Adapter(Protocol):
    """Renders the platform-specific files for one target.

    Adapters are pure: no I/O, no clock, no environment. The CLI decides
    whether the rendered files are written or compared against disk.
    """

    name: str

    def enabled(self, config: PluginConfig) -> bool: ...

    def render(self, config: PluginConfig, skills: list[Skill]) -> Files: ...


def to_json(data: object) -> str:
    """Stable JSON so regenerated files diff cleanly."""
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"
