from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
IMAGES = DOCS / "assets/images"


class ConceptInfographicsTest(unittest.TestCase):
    def test_required_images_are_referenced_once_with_text_equivalent(self):
        names = (
            "capa-arquitetura-software.png",
            "m01-mapa-estilos.png",
            "m02-anatomia-api.png",
            "m03-fronteiras-servicos.png",
            "m04-governanca-observavel.png",
            "m05-fluxo-eventos.png",
            "m06-resiliencia-nuvem.png",
        )
        corpus = "\n".join(
            path.read_text(encoding="utf-8")
            for path in DOCS.rglob("*.md")
            if "superpowers" not in path.parts and path.name != "prompts.md"
        )
        for name in names:
            self.assertTrue((IMAGES / name).is_file(), name)
            self.assertEqual(1, corpus.count(name), name)
        self.assertGreaterEqual(corpus.count("**Leitura textual da figura:**"), 7)
