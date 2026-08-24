from pathlib import Path
import re
import unittest

import yaml

from scripts.validate_content import MODULES, PAGES


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PAGE = "casos-reais.md"
PROTOCOL = "referencia/como-ler-um-caso-publico.md"

# Todas as páginas de casos reais seguem o formato narrativo.
NARRATIVE_PAGES = tuple(MODULES)

# iFood e Taco Bell deixaram de ser o caso real do módulo 6 e seguem como
# contexto de mercado no estudo de caso da unidade.
LEGACY_CANONICAL = {
    "3.9.1 O caso Netflix.md": "docs/modulo-3-servicos/casos-reais.md",
    "3.9.1.1 Discussão sobre o caso Netflix.md": "docs/modulo-3-servicos/casos-reais.md",
    "4.3.1 Estudo de Caso LinkedIn - Kafka.md": "docs/modulo-5-eventos/casos-reais.md",
    "5.5 Estudo de Caso iFood.md": "docs/modulo-6-nuvem/estudo-de-caso.md",
    "5.6 Estudo de Caso TacoBell.md": "docs/modulo-6-nuvem/estudo-de-caso.md",
}

# Uma empresa por módulo mantém o caso ancorado na decisão central do encontro.
EXPECTED_SUBJECTS = {
    "modulo-1-visao-geral": ("Prime Video",),
    "modulo-2-apis": ("Twitter",),
    "modulo-3-servicos": ("Netflix",),
    "modulo-4-governanca": ("Knight Capital",),
    "modulo-5-eventos": ("LinkedIn", "Kafka"),
    "modulo-6-nuvem": ("GitLab",),
}


def _nav_paths(node) -> tuple[str, ...]:
    if isinstance(node, str):
        return (node,)
    if isinstance(node, list):
        return tuple(path for item in node for path in _nav_paths(item))
    if isinstance(node, dict):
        return tuple(path for item in node.values() for path in _nav_paths(item))
    return ()


class RealCasesTest(unittest.TestCase):
    def test_page_is_part_of_the_module_contract(self):
        self.assertIn(PAGE, PAGES)
        self.assertEqual(
            PAGES.index("estudo-de-caso.md") + 1,
            PAGES.index(PAGE),
            "casos-reais.md vem logo depois do estudo de caso",
        )
        self.assertEqual(
            PAGES.index(PAGE) + 1,
            PAGES.index("oficina-de-ferramentas.md"),
            "casos-reais.md vem logo antes da oficina",
        )

    def test_every_module_has_the_page_in_the_expected_navigation_order(self):
        navigation = _nav_paths(
            yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))["nav"]
        )
        for module in MODULES:
            self.assertTrue((DOCS / module / PAGE).is_file(), module)
            ordered = [path for path in navigation if path.startswith(f"{module}/")]
            self.assertEqual(
                [f"{module}/{page}" for page in PAGES], ordered, module
            )

    def test_the_shared_reading_protocol_exists_and_is_published(self):
        self.assertTrue((DOCS / PROTOCOL).is_file())
        navigation = _nav_paths(
            yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))["nav"]
        )
        self.assertIn(PROTOCOL, navigation)

    def test_no_standalone_real_cases_section_remains(self):
        self.assertFalse((DOCS / "casos-reais").exists())

    def test_narrative_pages_do_not_borrow_the_hospital_case(self):
        """O caso real vale pela história do mercado, sem correlação forçada.

        Contrato em transição: vale para as páginas já reescritas em formato
        narrativo. Estender a NARRATIVE_PAGES conforme as demais forem
        refeitas, até cobrir MODULES inteiro.
        """
        for module in NARRATIVE_PAGES:
            text = (DOCS / module / PAGE).read_text(encoding="utf-8")
            self.assertNotIn("](estudo-de-caso.md)", text, module)
            self.assertNotIn("hospital", text.casefold(), module)

    def test_narrative_pages_anchor_events_in_time(self):
        """A página conta uma história situada, e não um resumo atemporal.

        A unidade varia com o caso: a Netflix se estende por uma década, o
        GitLab cabe em uma noite. Por isso a contagem aceita ano, mês e hora.
        """
        marker = re.compile(
            r"\b(?:19|20)\d{2}\b"
            r"|\b\d{1,2}h(?:\d{2})?\b"
            r"|\b(?:janeiro|fevereiro|março|abril|maio|junho|julho|agosto"
            r"|setembro|outubro|novembro|dezembro)\b",
            re.IGNORECASE,
        )
        for module in NARRATIVE_PAGES:
            text = (DOCS / module / PAGE).read_text(encoding="utf-8")
            self.assertGreaterEqual(
                len(marker.findall(text)), 6, f"{module}: história pouco situada"
            )
            self.assertGreaterEqual(
                len({m.group(0) for m in re.finditer(r"\b(?:19|20)\d{2}\b", text)}),
                2,
                f"{module}: sem antes e depois datados",
            )

    # As questões de casos reais ficam em recordar, compreender e comparar. O
    # projeto e a aplicação a outros contextos pertencem a exercicios.md.
    APPLICATION_VERBS = (
        "proponha", "desenhe", "redesenhe", "monte ", "estime",
        "aplique", "formule", "calcule", "escreva o argumento",
    )

    def test_questions_stay_below_the_application_level(self):
        for module in MODULES:
            text = (DOCS / module / PAGE).read_text(encoding="utf-8")
            questions = text.split("## Questões para discussão", 1)[1]
            questions = questions.split("## Fontes", 1)[0].casefold()
            for verb in self.APPLICATION_VERBS:
                self.assertNotIn(verb, questions, f"{module}: verbo de aplicação {verb!r}")

    def test_every_page_closes_with_architect_lens_questions(self):
        for module in MODULES:
            text = (DOCS / module / PAGE).read_text(encoding="utf-8")
            self.assertIn("## Questões para discussão", text, module)
            questions = text.split("## Questões para discussão", 1)[1]
            self.assertIn("lente do arquiteto", questions, module)
            for item in range(1, 6):
                self.assertIn(f"**{item}.", questions, f"{module}: questão {item}")

    def test_module_index_announces_the_page(self):
        for module in MODULES:
            index = (DOCS / module / "index.md").read_text(encoding="utf-8")
            self.assertIn("](casos-reais.md)", index, module)

    def test_each_page_covers_the_company_assigned_to_its_module(self):
        for module, subjects in EXPECTED_SUBJECTS.items():
            text = (DOCS / module / PAGE).read_text(encoding="utf-8")
            for subject in subjects:
                self.assertIn(subject, text, f"{module}: {subject}")

    def test_every_page_declares_its_sources(self):
        for module in MODULES:
            text = (DOCS / module / PAGE).read_text(encoding="utf-8")
            self.assertRegex(text, r"(?m)^## Fontes\b", module)
            sources = text.split("## Fontes", 1)[1]
            self.assertGreaterEqual(sources.count("](https://"), 3, module)

    def test_mermaid_figures_keep_the_module_accessibility_contract(self):
        for module in MODULES:
            text = (DOCS / module / PAGE).read_text(encoding="utf-8")
            diagrams = re.findall(r"```mermaid.*?```", text, re.DOTALL)
            contexts = re.findall(
                r"```mermaid\n.*?```\n\n"
                r"\*\*Texto alternativo:\*\*.+?\n\n"
                r"\*Figura \d+ — .+? Fonte: .+?\*\n\n"
                r"\*\*Leitura textual(?: da figura)?:\*\*.+?(?=\n\n|\Z)",
                text,
                re.DOTALL,
            )
            self.assertEqual(len(diagrams), len(contexts), module)

    def test_legacy_files_point_to_the_canonical_page(self):
        for name, canonical in LEGACY_CANONICAL.items():
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertTrue(text.startswith("> **Acervo legado preservado."), name)
            self.assertIn(canonical, text, name)


if __name__ == "__main__":
    unittest.main()
