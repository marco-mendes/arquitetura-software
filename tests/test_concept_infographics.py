from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
IMAGES = DOCS / "assets/images"


class ConceptInfographicsTest(unittest.TestCase):
    def test_each_infographic_has_its_own_markdown_reference_and_equivalent(self):
        figures = (
            ("index.md", "assets/images/capa-arquitetura-software.png", 1),
            ("modulo-1-visao-geral/conceitos.md", "../assets/images/m01-mapa-estilos.png", 4),
            ("modulo-2-apis/conceitos.md", "../assets/images/m02-anatomia-api.png", 4),
            ("modulo-3-servicos/conceitos.md", "../assets/images/m03-fronteiras-servicos.png", 4),
            ("modulo-4-governanca/conceitos.md", "../assets/images/m04-governanca-observavel.png", 5),
            ("modulo-5-eventos/conceitos.md", "../assets/images/m05-fluxo-eventos.png", 6),
            ("modulo-6-nuvem/conceitos.md", "../assets/images/m06-resiliencia-nuvem.png", 7),
        )
        for page_name, reference, number in figures:
            page = DOCS / page_name
            name = Path(reference).name
            self.assertTrue((IMAGES / name).is_file(), name)
            content = page.read_text(encoding="utf-8")
            figure = re.compile(
                rf"!\[[^\]\n]+\]\({re.escape(reference)}\)\n\n"
                rf"\*Figura {number} — [^\n]+\.\*\n\n"
                rf"\*\*Leitura textual da figura:\*\* [^\n]+"
            )
            self.assertEqual(
                1,
                len(figure.findall(content)),
                f"{name} deve aparecer como imagem Markdown, legenda e leitura textual em {page_name}",
            )
