"""The build pipeline: load -> validate -> render -> (write | check).

Functional core, imperative shell: `render_all` is pure; `write` and
`find_drift` are the only functions that touch generated files on disk.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .adapters import REGISTRY, Adapter, Files
from .config import PluginConfig, load_config
from .rules import Issue, validate
from .skill import Skill, discover_skills


@dataclass(frozen=True)
class Build:
    config: PluginConfig
    skills: list[Skill]
    issues: list[Issue]
    files: Files  # from enabled adapters
    retired: Files  # what disabled adapters would write; must not exist on disk

    @property
    def errors(self) -> list[Issue]:
        return [i for i in self.issues if i.level == "error"]


def render_all(config: PluginConfig, skills: list[Skill], adapters: tuple[Adapter, ...] = REGISTRY) -> tuple[Files, Files]:
    files: Files = {}
    retired: Files = {}
    for adapter in adapters:
        target = files if adapter.enabled(config) else retired
        for path, content in adapter.render(config, skills).items():
            if path in target:
                raise ValueError(f"two adapters both write {path}")
            target[path] = content
    return files, retired


def plan_build(root: Path) -> Build:
    config = load_config(root)
    skills = discover_skills(root)
    files, retired = render_all(config, skills)
    return Build(config=config, skills=skills, issues=validate(skills), files=files, retired=retired)


def write(root: Path, build: Build) -> list[str]:
    written = []
    for rel, content in sorted(build.files.items()):
        path = root / rel
        if path.exists() and path.read_text(encoding="utf-8") == content:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written.append(rel)
    for rel in sorted(build.retired):
        if (root / rel).exists():
            (root / rel).unlink()
            written.append(f"{rel} (removed: target disabled)")
    return written


def find_drift(root: Path, build: Build) -> list[str]:
    """Generated files that are missing, hand-edited, or left over."""
    drift = [
        rel
        for rel, content in sorted(build.files.items())
        if not (root / rel).exists() or (root / rel).read_text(encoding="utf-8") != content
    ]
    drift += [f"{rel} (target disabled)" for rel in sorted(build.retired) if (root / rel).exists()]
    return drift
