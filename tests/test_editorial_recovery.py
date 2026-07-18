from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class EditorialRecoveryTest(unittest.TestCase):
    def test_traceability_covers_every_numbered_legacy_markdown(self):
        traceability = (
            ROOT / "docs/superpowers/traceability/recuperacao-editorial.md"
        ).read_text(encoding="utf-8")
        sources = sorted(ROOT.glob("[1-5]*.md"))

        self.assertGreater(len(sources), 30)
        for source in sources:
            self.assertIn(f"`{source.name}`", traceability, source.name)
