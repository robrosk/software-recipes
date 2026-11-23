"""Run with: python3 -m unittest discover -s tests"""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.recipes.pipeline import find_drift, plan_build, write
from tools.recipes.rules import validate
from tools.recipes.scalar import ScalarError, parse_scalar
from tools.recipes.skill import FrontmatterError, load_skill, parse_frontmatter

REPO = Path(__file__).resolve().parents[1]


def make_skill(root: Path, name: str, frontmatter: str, body: str = "Body.\n") -> Path:
    folder = root / "skills" / name
    folder.mkdir(parents=True)
    (folder / "SKILL.md").write_text(f"---\n{frontmatter}\n---\n{body}", encoding="utf-8")
    return folder


class FrontmatterTests(unittest.TestCase):
    def test_parses_scalars_and_metadata(self):
        top, meta, body = parse_frontmatter(
            "---\nname: demo\ndescription: \"Does: things\"\nmetadata:\n  display-name: Demo\n---\nHi\n"
        )
        self.assertEqual(top, {"name": "demo", "description": "Does: things"})
        self.assertEqual(meta, {"display-name": "Demo"})
        self.assertEqual(body, "Hi\n")

    def test_rejects_block_scalars(self):
        with self.assertRaises(FrontmatterError):
            parse_frontmatter("---\nname: demo\ndescription: >\n  folded\n---\n")

    def test_rejects_missing_fence(self):
        with self.assertRaises(FrontmatterError):
            parse_frontmatter("name: demo\n")

    def test_rejects_unquoted_colon_space(self):
        # The design-the-system description that real YAML parsers refused.
        with self.assertRaises(FrontmatterError):
            parse_frontmatter("---\nname: design-the-system\ndescription: Design a system "
                              "together, with you leading: pin down its behavior.\n---\n")

    def test_checks_metadata_values_too(self):
        with self.assertRaises(FrontmatterError):
            parse_frontmatter("---\nname: demo\nmetadata:\n  short-description: Plan: then code\n---\n")

    def test_error_names_the_file(self):
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root)
        folder = make_skill(root, "alpha", "name: alpha\ndescription: Do it: now")
        with self.assertRaisesRegex(FrontmatterError, "skills/alpha/SKILL.md: line 3"):
            load_skill(folder)


class ScalarTests(unittest.TestCase):
    def test_accepts_valid_scalars(self):
        cases = {
            "Plan a change. Use when asked": "Plan a change. Use when asked",
            "ratio 1:2 and C# code": "ratio 1:2 and C# code",
            "-flag is fine": "-flag is fine",
            '"Hunt: then fix"': "Hunt: then fix",
            '"say \\"hi\\""': 'say "hi"',
            "'it''s: quoted'": "it's: quoted",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(parse_scalar(text), expected)

    def test_rejects_what_yaml_rejects_or_misreads(self):
        for text in ("Hunt for bugs: then fix", "ends with:", "a value # comment",
                     "- list item", ": colon", "? key", "*alias", "&anchor", "!tag",
                     "%directive", "@reserved", "`tick", "[a, b]", "{a: b}", "> folded",
                     '"unclosed', '"x" trailing', "'unclosed", "'it's'"):
            with self.subTest(text=text), self.assertRaises(ScalarError):
                parse_scalar(text)


class RuleTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root)

    def errors(self, folder: Path) -> list[str]:
        return [i.message for i in validate([load_skill(folder)]) if i.level == "error"]

    def test_name_must_match_folder(self):
        folder = make_skill(self.root, "alpha", "name: beta\ndescription: Use when testing.")
        self.assertIn("name must match its folder name", self.errors(folder))

    def test_broken_link_is_an_error(self):
        folder = make_skill(self.root, "alpha", "name: alpha\ndescription: Use when testing.",
                            "See [x](references/missing.md).\n")
        self.assertTrue(any("link target missing" in e for e in self.errors(folder)))

    def test_em_dash_is_an_error(self):
        folder = make_skill(self.root, "alpha", "name: alpha\ndescription: Use when testing — now.")
        self.assertTrue(any("em dash" in e for e in self.errors(folder)))


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root)
        shutil.copy(REPO / "recipes.toml", self.root / "recipes.toml")
        make_skill(self.root, "manual-only",
                   "name: manual-only\ndescription: Ship a release.\ndisable-model-invocation: true")

    def test_build_then_check_is_clean(self):
        build = plan_build(self.root)
        write(self.root, build)
        self.assertEqual(find_drift(self.root, plan_build(self.root)), [])

    def test_hand_edit_is_drift(self):
        write(self.root, plan_build(self.root))
        (self.root / ".claude-plugin" / "plugin.json").write_text("{}\n", encoding="utf-8")
        self.assertEqual(find_drift(self.root, plan_build(self.root)), [".claude-plugin/plugin.json"])

    def test_user_invoked_skill_gets_codex_policy(self):
        write(self.root, plan_build(self.root))
        yaml = (self.root / "skills/manual-only/agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn("allow_implicit_invocation: false", yaml)

    def test_plugin_lists_every_skill(self):
        write(self.root, plan_build(self.root))
        manifest = json.loads((self.root / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["skills"], ["./skills/manual-only"])

    def test_repo_itself_is_up_to_date(self):
        build = plan_build(REPO)
        self.assertEqual(build.errors, [])
        self.assertEqual(find_drift(REPO, build), [])


if __name__ == "__main__":
    unittest.main()
