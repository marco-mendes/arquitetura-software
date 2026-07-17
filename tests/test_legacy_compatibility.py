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
