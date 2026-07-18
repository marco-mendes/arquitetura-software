from pathlib import Path
import unittest

from scripts.validate_content import (
    MODULES,
    expandable_feedback_errors,
    self_contained_activity_errors,
)


ROOT = Path(__file__).resolve().parents[1]
MODULE_SLUGS = tuple(MODULES)
ADVANCED_LABELS = (
    "Objetivo",
    "Situação",
    "Seu papel",
    "Artefato que você irá usar",
    "Antes de executar",
    "O que fazer",
    "Evidência esperada",
    "Entrega esperada",
    "Critérios de avaliação",
)

_ALLOWED_ACTIONS = {"integrar", "consolidar", "substituir figura", "referenciar"}
_ALLOWED_FIGURE_DECISIONS = (
    "manter",
    "recriar em Mermaid",
    "adaptar",
    "não usar",
)


class EditorialRecoveryTest(unittest.TestCase):
    def test_every_module_exercise_page_uses_expandable_feedback_and_self_contained_labels(self):
        for slug in MODULE_SLUGS:
            text = (ROOT / "docs" / slug / "exercicios.md").read_text(
                encoding="utf-8"
            )
            self.assertGreaterEqual(text.count("<summary>Ver resposta</summary>"), 6, slug)
            for label in ADVANCED_LABELS:
                self.assertIn(f"**{label}**", text, slug)

    def test_public_figure_captions_identify_their_source(self):
        for path in (ROOT / "docs").rglob("*.md"):
            if "superpowers" in path.parts:
                continue
            for caption in path.read_text(encoding="utf-8").splitlines():
                if caption.startswith("*Figura "):
                    self.assertIn("Fonte:", caption, path.as_posix())

    def test_expandable_feedback_parser(self):
        text = (
            "## Recordar\n\n"
            "1. Defina conector.\n\n"
            "<details>\n"
            "<summary>Ver resposta</summary>\n\n"
            "Um mecanismo de colaboração entre elementos arquiteturais.\n"
            "</details>\n\n"
            "## Compreender\n\n"
            "1. Explique por que um conector não é um componente.\n\n"
            "<details>\n"
            "<summary>Ver resposta</summary>\n\n"
            "O conector descreve a comunicação; o componente concentra responsabilidade.\n"
            "</details>\n"
        )

        self.assertEqual([], expandable_feedback_errors(text, "exemplo.md"))

    def test_self_contained_activity_parser(self):
        text = """## Aplicar

**Objetivo**

**Situação**

**Seu papel**

**Artefato que você irá usar**

**Antes de executar**

**O que fazer**

**Evidência esperada**

**Entrega esperada**

**Critérios de avaliação**
"""

        self.assertEqual([], self_contained_activity_errors(text, "exemplo.md"))

    def test_self_contained_activity_parser_reports_an_out_of_order_label(self):
        text = """## Aplicar

**Objetivo**

**Situação**

**Seu papel**

**Artefato que você irá usar**

**Antes de executar**

**Evidência esperada**

**O que fazer**

**Entrega esperada**

**Critérios de avaliação**
"""

        self.assertEqual(
            [
                "exemplo.md: Aplicar: marcador fora da ordem: "
                "**Evidência esperada**"
            ],
            self_contained_activity_errors(text, "exemplo.md"),
        )

    def test_traceability_covers_every_numbered_legacy_markdown(self):
        traceability = (
            ROOT / "docs/superpowers/traceability/recuperacao-editorial.md"
        ).read_text(encoding="utf-8")
        sources = sorted(ROOT.glob("[1-5]*.md"))

        self.assertGreater(len(sources), 30)
        for source in sources:
            self.assertIn(f"`{source.name}`", traceability, source.name)

    def test_traceability_rows_have_a_complete_valid_editorial_contract(self):
        traceability = (
            ROOT / "docs/superpowers/traceability/recuperacao-editorial.md"
        ).read_text(encoding="utf-8")
        rows = [
            line
            for line in traceability.splitlines()
            if line.startswith("| `")
        ]
        sources = {source.name for source in ROOT.glob("[1-5]*.md")}

        self.assertEqual(len(sources), len(rows))
        seen_sources: set[str] = set()
        for row in rows:
            fields = [field.strip() for field in row.strip("|").split("|")]
            self.assertEqual(5, len(fields), row)
            self.assertTrue(all(fields), row)

            source, destination, action, _, figure = fields
            source_name = source.removeprefix("`").removesuffix("`")
            self.assertNotIn(source_name, seen_sources, source_name)
            seen_sources.add(source_name)
            self.assertTrue((ROOT / destination.strip("`")).is_file(), destination)
            self.assertIn(action, _ALLOWED_ACTIONS, action)
            self.assertTrue(
                any(figure.startswith(f"{decision} —") for decision in _ALLOWED_FIGURE_DECISIONS),
                figure,
            )

        self.assertEqual(sources, seen_sources)
