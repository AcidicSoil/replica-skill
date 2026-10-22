import json
import os
import unittest

from _load import ROOT
from test_repo import SKILLS


class CodexPlugin(unittest.TestCase):
    def test_codex_manifest_reuses_all_existing_skills(self):
        path = os.path.join(ROOT, ".codex-plugin", "plugin.json")
        with open(path, encoding="utf-8") as fh:
            manifest = json.load(fh)
        self.assertEqual(manifest["name"], "replica-skill")
        self.assertEqual(manifest["skills"], "./")
        self.assertEqual(manifest["repository"], "https://github.com/AcidicSoil/replica-skill")
        self.assertEqual(manifest["version"], "1.0.0")
        self.assertIn("displayName", manifest["interface"])
        for name in SKILLS:
            with self.subTest(skill=name):
                self.assertTrue(os.path.isfile(os.path.join(ROOT, name, "SKILL.md")))

    def test_codex_marketplace_installs_plugin_from_repository_root(self):
        path = os.path.join(ROOT, ".agents", "plugins", "marketplace.json")
        with open(path, encoding="utf-8") as fh:
            market = json.load(fh)
        self.assertEqual(market["name"], "replica-skill-acidicsoil")
        self.assertEqual(len(market["plugins"]), 1)
        plugin = market["plugins"][0]
        self.assertEqual(plugin["name"], "replica-skill")
        self.assertEqual(plugin["source"], {"source": "local", "path": "./"})
        self.assertEqual(plugin["policy"]["installation"], "AVAILABLE")
        self.assertEqual(plugin["policy"]["authentication"], "ON_INSTALL")

    def test_readme_describes_codex_install(self):
        with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as fh:
            readme = fh.read()
        self.assertIn("codex plugin marketplace add AcidicSoil/replica-skill", readme)
        self.assertIn("codex plugin add replica-skill@replica-skill-acidicsoil", readme)


if __name__ == "__main__":
    unittest.main()
