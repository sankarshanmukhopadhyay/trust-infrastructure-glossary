"""Reader-first information architecture regression checks.

These tests check navigable intent and stable routes, not visual WCAG conformance.
"""
import re
import unittest
from pathlib import Path
from sys import path as sys_path

ROOT = Path(__file__).resolve().parents[1]
sys_path.insert(0, str(ROOT / "tools"))
from validate_site_ia import normalize_route, route_index, front_matter, RELATIVE_URL_RE


class ConsumerNavigationTests(unittest.TestCase):
    def test_readme_is_gateway_not_full_manual(self):
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertLess(len(content.split()), 650)
        for phrase in ["Explore concepts", "Use TIG", "Govern TIG", "Authority and assurance",
                       "tools/validate_site_ia.py"]:
            self.assertIn(phrase, content)
        self.assertIn("issues/28", content)

    def test_primary_journeys_have_distinct_entry_points(self):
        home = (ROOT / "index.md").read_text(encoding="utf-8")
        for route in ["/explore/", "/use/", "/semantic-model/", "/governance/", "/start-here/"]:
            self.assertIn(f"'{route}' | relative_url", home)
            self.assertIn(normalize_route(route), route_index())
        for name in ["index.md", "start-here.md", "explore/index.md", "use/index.md"]:
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertEqual(len(re.findall(r"^# ", text, re.M)), 1, name)
            for match in RELATIVE_URL_RE.finditer(text):
                self.assertIn(normalize_route(match.group("route")), route_index(),
                              f"{name} has missing route {match.group('route')}")

    def test_stable_route_and_navigation_separation(self):
        self.assertEqual(front_matter(ROOT / "start-here.md")["permalink"], "/start-here/")
        self.assertEqual(front_matter(ROOT / "index.md")["nav_exclude"], True)
        for path in ("explore/index.md", "semantic-model/index.md", "use/index.md",
                     "governance/index.md", "project/index.md"):
            self.assertTrue(front_matter(ROOT / path).get("has_children"))

    def test_public_text_does_not_overclaim_semantics(self):
        for name in ("README.md", "index.md", "start-here.md", "explore/index.md", "use/index.md"):
            text = (ROOT / name).read_text(encoding="utf-8").lower()
            self.assertTrue(any(p in text for p in ("not automatically", "does not", "do not")),
                            name + " must explain at least one authority boundary")


if __name__ == "__main__":
    unittest.main()
