"""Plugin metadata, loaded once from recipes.toml (the single source of truth)."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

CONFIG_FILE = "recipes.toml"


@dataclass(frozen=True)
class Targets:
    claude: bool
    codex_skill_metadata: bool
    agent_plugins: bool


@dataclass(frozen=True)
class PluginConfig:
    name: str
    display_name: str
    version: str
    description: str
    license: str
    keywords: tuple[str, ...]
    category: str
    author_name: str
    github_owner: str
    marketplace_name: str
    marketplace_description: str
    targets: Targets

    @property
    def repository(self) -> str:
        return f"https://github.com/{self.github_owner}/{self.name}"


def load_config(root: Path) -> PluginConfig:
    data = tomllib.loads((root / CONFIG_FILE).read_text(encoding="utf-8"))
    plugin, author, market = data["plugin"], data["author"], data["marketplace"]
    return PluginConfig(
        name=plugin["name"],
        display_name=plugin["display_name"],
        version=plugin["version"],
        description=plugin["description"],
        license=plugin["license"],
        keywords=tuple(plugin["keywords"]),
        category=plugin["category"],
        author_name=author["name"],
        github_owner=author["github_owner"],
        marketplace_name=market["name"],
        marketplace_description=market["description"],
        targets=Targets(**data["targets"]),
    )
