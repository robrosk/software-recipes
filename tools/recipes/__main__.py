"""CLI: python3 -m tools.recipes {validate,build,check}

validate  lint every SKILL.md
build     validate, then regenerate every platform manifest
check     validate, then fail if any generated file is stale (use in CI)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .pipeline import find_drift, plan_build, write
from .skill import FrontmatterError

ROOT = Path(__file__).resolve().parents[2]


def _report(build) -> bool:
    for issue in build.issues:
        print(issue, file=sys.stderr if issue.level == "error" else sys.stdout)
    print(f"{len(build.skills)} skill(s), {len(build.errors)} error(s), "
          f"{len(build.issues) - len(build.errors)} warning(s)")
    return not build.errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="recipes", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["validate", "build", "check"])
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)

    try:
        build = plan_build(args.root)
    except FrontmatterError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if not _report(build):
        return 1
    if args.command == "build":
        changed = write(args.root, build)
        print("\n".join(f"wrote {p}" for p in changed) or "generated files already up to date")
    elif args.command == "check":
        drift = find_drift(args.root, build)
        if drift:
            print("stale generated files (run `make build`):", *drift, sep="\n  ", file=sys.stderr)
            return 1
        print("generated files up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
