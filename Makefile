PY ?= python3

.PHONY: validate build check test

validate:  ## lint every SKILL.md
	$(PY) -m tools.recipes validate

build:  ## regenerate .claude-plugin/, agents/openai.yaml and (optionally) plugin.json
	$(PY) -m tools.recipes build

check: test  ## CI gate: lint, unit tests, and no stale generated files
	$(PY) -m tools.recipes check

test:
	$(PY) -m unittest discover -s tests
