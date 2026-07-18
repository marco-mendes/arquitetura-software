from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


class LegacyCompatibilityTest(unittest.TestCase):
    def test_baseline_root_markdown_files_still_exist(self):
        names = subprocess.check_output(
            ["git", "ls-tree", "-r", "--name-only", "e223a79"],
            cwd=ROOT,
            text=True,
        ).splitlines()
        legacy = [name for name in names if "/" not in name and name.endswith(".md")]
        self.assertTrue(legacy)
        for name in legacy:
            self.assertTrue((ROOT / name).is_file(), name)

    def test_legacy_document_body_is_unchanged_after_transition_note(self):
        names = subprocess.check_output(
            ["git", "ls-tree", "-r", "--name-only", "e223a79"],
            cwd=ROOT,
            text=True,
        ).splitlines()
        legacy = [
            name
            for name in names
            if "/" not in name and name.endswith(".md") and name != "README.md"
        ]
        for name in legacy:
            baseline = subprocess.check_output(
                ["git", "show", f"e223a79:{name}"],
                cwd=ROOT,
            )
            current = (ROOT / name).read_bytes()
            self.assertTrue(current.endswith(baseline), name)

    def test_readme_documents_preview_validation_and_pages(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for marker in (
            "python3 -m venv .venv",
            "pip install -r requirements.txt",
            "mkdocs serve",
            "python scripts/validate_content.py --all",
            "mkdocs build --strict",
            "GitHub Actions",
        ):
            self.assertIn(marker, text)

    def test_traceability_matrix_remains_private_to_editorial_work(self):
        private_matrix = ROOT / "docs/superpowers/traceability/recuperacao-editorial.md"
        public_map = ROOT / "docs/referencia/mapa-do-acervo-legado.md"

        self.assertTrue(private_matrix.is_file())
        self.assertFalse(public_map.exists())

        published_markdown = [ROOT / "README.md"]
        published_markdown.extend(
            path
            for path in (ROOT / "docs").rglob("*.md")
            if "superpowers" not in path.parts
        )
        for path in published_markdown:
            self.assertNotIn(
                "mapa-do-acervo-legado",
                path.read_text(encoding="utf-8"),
                path.relative_to(ROOT),
            )
