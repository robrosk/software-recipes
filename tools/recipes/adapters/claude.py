"""Claude-style plugin + marketplace manifests in .claude-plugin/.

Claude Code reads these natively. Codex falls back to .claude-plugin/plugin.json
when it finds no manifest of its own, and Copilot CLI checks .claude-plugin/
for both files, so this one adapter is what makes the repo installable on all
three tools.
"""

from __future__ import annotations

from ..config import PluginConfig
from ..skill import SKILLS_DIR, Skill
from .base import Files, to_json


class ClaudeAdapter:
    name = "claude"

    def enabled(self, config: PluginConfig) -> bool:
        return config.targets.claude

    def render(self, config: PluginConfig, skills: list[Skill]) -> Files:
        return {
            ".claude-plugin/plugin.json": to_json(self._plugin(config, skills)),
            ".claude-plugin/marketplace.json": to_json(self._marketplace(config)),
        }

    @staticmethod
    def _plugin(config: PluginConfig, skills: list[Skill]) -> dict:
        return {
            "name": config.name,
            "displayName": config.display_name,
            "version": config.version,
            "description": config.description,
            "author": {"name": config.author_name},
            "repository": config.repository,
            "license": config.license,
            "keywords": list(config.keywords),
            # Explicit list: Codex's fallback reader needs a `skills` field,
            # and listing folders keeps drafts/ out of every harness.
            "skills": [f"./{SKILLS_DIR}/{s.directory.name}" for s in skills],
        }

    @staticmethod
    def _marketplace(config: PluginConfig) -> dict:
        return {
            "name": config.marketplace_name,
            "owner": {"name": config.author_name},
            "description": config.marketplace_description,
            "plugins": [
                {
                    "name": config.name,
                    "source": "./",
                    "description": config.description,
                    "category": config.category,
                    "keywords": list(config.keywords),
                }
            ],
        }
