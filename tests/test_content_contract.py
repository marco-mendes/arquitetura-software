from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.validate_content import (
    BLOOM,
    MODULES,
    PAGES,
    bloom_sections,
    validate_all,
    validate_document,
    validate_module,
)


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class ContentContractTest(unittest.TestCase):
    def test_course_has_six_modules_and_eight_page_contract(self):
        self.assertEqual(6, len(MODULES))
        self.assertEqual(8, len(PAGES))
        self.assertEqual("index.md", PAGES[0])
        self.assertEqual("sintese-e-referencias.md", PAGES[-1])

    def test_public_pages_use_assessment_criteria_vocabulary(self):
        for path in DOCS.rglob("*.md"):
            if "superpowers" in path.parts:
                continue
            text = path.read_text(encoding="utf-8").casefold()
            self.assertNotRegex(
                text,
                r"\brubricas?\b|\bpontua(?:ção|cao)\b|\b\d+\s+pontos?\b",
            )

    def test_bloom_sections_extracts_each_level_without_subheadings(self):
        text = "\n".join(
            f"## {level}\n\nAtividade de {level}.\n\n### Apoio\n\nDetalhe."
            for level in BLOOM
        )

        sections = bloom_sections(text)

        self.assertEqual(set(BLOOM), set(sections))
        self.assertIn("### Apoio", sections["Aplicar"])
        self.assertNotIn("## Analisar", sections["Aplicar"])

    def test_validator_rejects_placeholders_and_public_policy_vocabulary(self):
        samples = {
            "TODO: completar": "marcador provisório",
            "Use a rubrica publicada.": "vocabulário público proibido",
            "A atividade vale dez pontos.": "vocabulário público proibido",
            "Consulte a pontuação.": "vocabulário público proibido",
            "A ferramenta exige cartão para acesso.": "classificação de acesso",
            "O acesso depende de crédito.": "classificação de acesso",
            "Há cobrança para usar a ferramenta.": "classificação de acesso",
            "Acesso à ferramenta:\n- cadastro com cobranca.": "classificação de acesso",
        }
        with TemporaryDirectory() as temporary:
            docs = Path(temporary)
            page = docs / "pagina.md"
            for text, expected in samples.items():
                with self.subTest(text=text):
                    page.write_text(f"# Título\n\n{text}\n", encoding="utf-8")
                    self.assertTrue(
                        any(expected in error for error in validate_document(page, docs))
                    )

    def test_validator_checks_local_links_anchors_and_figure_accessibility(self):
        with TemporaryDirectory() as temporary:
            docs = Path(temporary)
            (docs / "figura.png").write_bytes(b"png")
            (docs / "destino.md").write_text(
                "# Destino\n\n## Âncora existente\n", encoding="utf-8"
            )
            page = docs / "pagina.md"
            page.write_text(
                "# Página\n\n"
                "[Arquivo ausente](ausente.md)\n\n"
                "[Âncora ausente](destino.md#nao-existe)\n\n"
                "![](figura.png)\n\n"
                "![Fluxo do exemplo](figura.png)\n\n"
                "Parágrafo sem equivalência.\n",
                encoding="utf-8",
            )

            errors = validate_document(page, docs)

            for expected in (
                "arquivo local ausente",
                "âncora local ausente",
                "imagem sem texto alternativo",
                "figura sem leitura textual",
            ):
                self.assertTrue(any(expected in error for error in errors), expected)

    def test_procedural_bold_labels_are_isolated_as_paragraphs(self):
        with TemporaryDirectory() as temporary:
            docs = Path(temporary)
            page = docs / "oficina-de-ferramentas.md"
            page.write_text(
                "# Oficina\n\n"
                "**Execute** rode o comando.\n\n"
                "**Observe**\n"
                "Leia a saída.\n",
                encoding="utf-8",
            )
            errors = validate_document(page, docs)
            self.assertEqual(
                2,
                sum("rótulo procedimental aglutinado" in error for error in errors),
            )

            page.write_text(
                "# Oficina\n\n**Execute**\n\nRode o comando.\n",
                encoding="utf-8",
            )
            self.assertFalse(
                any(
                    "rótulo procedimental aglutinado" in error
                    for error in validate_document(page, docs)
                )
            )

    def test_module_validator_enforces_bloom_answers_criteria_and_percentages(self):
        complete_markers = "\n\n".join(
            (
                "**Situação**\n\nCenário.",
                "**Seu papel**\n\nArquiteto.",
                "**Insumos disponíveis**\n\nEvidências.",
                "**Como conduzir**\n\nCompare.",
                "**Entrega esperada**\n\nADR.",
                "**Critérios de avaliação**\n\nCritérios.",
            )
        )
        exercises = (
            "# Exercícios\n\n"
            "## Recordar\n\n**Resposta:** conceito.\n\n"
            "## Compreender\n\nExplique.\n\n"
            "## Aplicar\n\n**Resposta:** execução.\n\n"
            "## Analisar\n\n"
            f"{complete_markers}\n\n"
            "| Critério | Percentual |\n| --- | ---: |\n"
            "| Evidência | 40% |\n| Decisão | 50% |\n\n"
            "## Avaliar\n\n"
            f"{complete_markers}\n\n"
            "| Critério | Percentual |\n| --- | ---: |\n| Recomendação | 100% |\n\n"
            "## Criar\n\nProduza um incremento.\n\n"
            "## Recordar\n\nRepetição indevida.\n"
        )
        with TemporaryDirectory() as temporary:
            docs = Path(temporary)
            slug = next(iter(MODULES))
            module = docs / slug
            module.mkdir()
            for page_name in PAGES:
                (module / page_name).write_text(
                    exercises if page_name == "exercicios.md" else "# Página\n",
                    encoding="utf-8",
                )

            errors = validate_module(slug, docs)

            for expected in (
                "bloco de resposta fora de Recordar/Compreender",
                "Aplicar: marcador obrigatório ausente",
                "percentuais do instrumento somam 90%",
                "seção Bloom duplicada: Recordar",
                "fora da faixa de 5.000–8.500 palavras",
            ):
                self.assertTrue(any(expected in error for error in errors), expected)

    def test_all_validation_skips_internal_superpowers_documents(self):
        with TemporaryDirectory() as temporary:
            docs = Path(temporary)
            internal = docs / "superpowers"
            internal.mkdir()
            (internal / "plano.md").write_text(
                "# Plano\n\nTODO: material interno.\n", encoding="utf-8"
            )
            (docs / "publica.md").write_text("# Página pública\n", encoding="utf-8")

            errors = validate_all(docs)

            self.assertFalse(any("superpowers/plano.md" in error for error in errors))
            self.assertTrue(any("32.000–51.000 palavras" in error for error in errors))
