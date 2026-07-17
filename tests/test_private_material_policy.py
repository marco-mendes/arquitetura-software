from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PrivateMaterialPolicyTest(unittest.TestCase):
    def test_teacher_material_is_ignored_and_not_in_nav(self):
        ignored = subprocess.run(
            ["git", "check-ignore", "material-professor/README.md"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, ignored.returncode)
        self.assertNotIn(
            "material-professor", (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        )
