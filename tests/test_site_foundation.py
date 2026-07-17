from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]


class SiteFoundationTest(unittest.TestCase):
    def test_homepage_states_course_workload(self):
        text = (ROOT / "docs/index.md").read_text(encoding="utf-8")
        self.assertIn("24 horas", text)
        self.assertIn("seis encontros de quatro horas", text)

    def test_required_foundation_files_exist(self):
        for relative in (
            "mkdocs.yml", "requirements.txt",
            ".github/workflows/publicar-site.yml",
            "docs/index.md", "docs/assets/javascripts/mermaid.mjs",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_six_modules_are_in_navigation(self):
        config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        rendered = str(config["nav"])
        for label in ("Estilos", "APIs", "Serviços", "Governança", "Eventos", "Nuvem"):
            self.assertIn(label, rendered)

    def test_publication_gate_order(self):
        text = (ROOT / ".github/workflows/publicar-site.yml").read_text(encoding="utf-8")
        commands = (
            "python -m unittest discover -s tests -v",
            "python scripts/validate_content.py --all",
            "mkdocs build --strict",
        )
        self.assertEqual(sorted(map(text.index, commands)), list(map(text.index, commands)))
