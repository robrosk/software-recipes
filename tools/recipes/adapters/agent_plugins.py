"""Root plugin.json in the Agent Plugins 1.0 format.

Codex and Copilot both prefer this file over .claude-plugin/ when present.
The schema is closed: no component fields; skills load from skills/<name>/.
Vendor settings live under `extensions`. Off by default (see recipes.toml)
until an install on both tools confirms the shape below.
"""

from __future__ import annotations

from ..config import PluginConfig
from ..skill import Skill
from .base import Files, to_json

SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"


class AgentPluginsAdapter:
    name = "agent-plugins"

    def enabled(self, config: PluginConfig) -> bool:
        return config.targets.agent_plugins

    def render(self, config: PluginConfig, skills: list[Skill]) -> Files:
        manifest = {
            "$schema": SCHEMA,
            "name": config.name,
            "version": config.version,
            "description": config.description,
            "author": {"name": config.author_name},
            "repository": config.repository,
            "license": config.license,
            "keywords": list(config.keywords),
            "extensions": {
                "com.openai": {
                    "interface": {
                        "displayName": config.display_name,
                        "shortDescription": config.description,
                        "category": config.category.title(),
                    }
                }
            },
        }
        return {"plugin.json": to_json(manifest)}
