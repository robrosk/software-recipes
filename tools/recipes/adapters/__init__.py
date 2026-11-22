"""Adapter registry. To support a new tool, write an adapter and add it here."""

from .agent_plugins import AgentPluginsAdapter
from .base import Adapter, Files
from .claude import ClaudeAdapter
from .codex import CodexSkillMetadataAdapter

REGISTRY: tuple[Adapter, ...] = (
    ClaudeAdapter(),
    CodexSkillMetadataAdapter(),
    AgentPluginsAdapter(),
)

__all__ = ["REGISTRY", "Adapter", "Files"]
