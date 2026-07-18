from pathlib import Path
import re
import unittest

from tests.course_assertions import assert_module_contract
from scripts.validate_content import bloom_sections, expandable_feedback_errors


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "docs" / "modulo-1-visao-geral"


class ModuleOneTest(unittest.TestCase):
    def test_module_one_begins_with_architectural_styles(self):
        text = (MODULE / "conceitos.md").read_text(encoding="utf-8")

        self.assertEqual("# Conceitos: estilos arquiteturais", text.splitlines()[0])
        self.assertNotIn("## O que torna uma decisão arquitetural", text)

    def test_reference_appendix_preserves_how_to_read_architecture(self):
        appendix = ROOT / "docs/referencia/como-ler-uma-arquitetura.md"
        text = appendix.read_text(encoding="utf-8")

        for term in (
            "Componente",
            "Conector",
            "Configuração",
            "Estrutura",
            "comportamento",
        ):
            self.assertIn(term, text)
        self.assertEqual(2, text.count("```mermaid"))
        self.assertEqual(2, text.count("**Texto alternativo:**"))
        self.assertEqual(2, text.count("*Figura "))
        self.assertEqual(2, text.count("**Leitura textual da figura:**"))

    def test_content(self):
        assert_module_contract(
            self,
            "modulo-1-visao-geral",
            (
                "componente",
                "conector",
                "atributo de qualidade",
                "camadas",
                "pipes and filters",
                "microkernel",
                "monólito modular",
                "ADR",
                "Structurizr Lite",
                "Python",
                ".NET",
                "Java",
            ),
        )

    def test_unit_one_introduces_the_complete_style_map(self):
        text = (MODULE / "conceitos.md").read_text(encoding="utf-8")

        for term in (
            "Camadas",
            "MVC",
            "Hexagonal",
            "Microkernel",
            "Pipes and Filters",
            "DDD",
            "microsserviços",
            "APIs",
            "eventos",
            "nuvem",
            "contêineres",
        ):
            self.assertIn(term, text)

    def test_family_map_includes_operational_and_service_alternatives(self):
        concepts = (MODULE / "conceitos.md").read_text(encoding="utf-8")
        decisions = (MODULE / "padroes-e-decisoes.md").read_text(encoding="utf-8")
        svg = (ROOT / "docs/assets/images/m01-familias-arquiteturais.svg").read_text(
            encoding="utf-8"
        )
        alt = re.search(
            r"!\[(.*?)\]\(\.\./assets/images/m01-familias-arquiteturais\.svg\)",
            concepts,
        ).group(1)
        reading = concepts.split("**Leitura textual da figura:**", 1)[1].split(
            "\n\n", 1
        )[0]
        table = concepts.split("| Família", 1)[1].split("\n\n", 1)[0]
        decomposition = concepts.split("### Decomposição por domínio", 1)[1].split(
            "###", 1
        )[0]
        operation = concepts.split("### Execução e operação", 1)[1].split(
            "## Comparar", 1
        )[0]
        integration = concepts.split("### Integração e comunicação", 1)[1].split(
            "###", 1
        )[0]

        for term, narrative in (
            ("macrosserviços", decomposition),
            ("orquestração", operation),
            ("serverless", operation),
        ):
            self.assertIn(term, alt)
            self.assertIn(term, reading)
            self.assertIn(term, table)
            self.assertIn(term, narrative)
            self.assertIn(term, svg)
        self.assertIn(
            "[Pipes and Filters](padroes-e-decisoes.md#pipes-and-filters)",
            integration,
        )
        self.assertTrue((MODULE / "padroes-e-decisoes.md").is_file())
        self.assertIn("{#pipes-and-filters}", decisions)

    def test_module_one_uses_accessible_static_family_map_not_mermaid_mindmap(self):
        text = (MODULE / "conceitos.md").read_text(encoding="utf-8")

        self.assertIn("m01-familias-arquiteturais.svg", text)
        self.assertNotIn("mindmap", text)
        for family in (
            "Organização interna",
            "Decomposição por domínio",
            "Integração e comunicação",
            "Execução e operação",
        ):
            self.assertIn(family, text)

        asset = ROOT / "docs" / "assets" / "images" / "m01-familias-arquiteturais.svg"
        self.assertTrue(asset.is_file())
        svg = asset.read_text(encoding="utf-8")
        self.assertIn('viewBox="0 0 1200 760"', svg)
        self.assertNotRegex(svg, r"<script\\b|(?:href|src)=[\"']https?://")
        self.assertIn("<title", svg)
        self.assertIn("<desc", svg)
        self.assertIn(
            "![Diagrama em quatro cartões:",
            text,
        )
        self.assertIn("*Figura 1 — Quatro famílias de decisões", text)
        self.assertIn("**Leitura textual da figura:**", text)

    def test_unit_one_recall_and_understand_use_individual_expandable_answers(self):
        exercises = (MODULE / "exercicios.md").read_text(encoding="utf-8")

        self.assertGreaterEqual(exercises.count("<summary>Ver resposta</summary>"), 12)
        self.assertEqual(
            [], expandable_feedback_errors(exercises, "exercicios.md")
        )

    def test_advanced_activities_explain_the_lab_before_commands(self):
        exercises = (MODULE / "exercicios.md").read_text(encoding="utf-8")

        for level in ("Aplicar", "Analisar", "Avaliar", "Criar"):
            section = bloom_sections(exercises)[level]
            for label in (
                "**Objetivo**",
                "**Situação**",
                "**Seu papel**",
                "**Artefato que você irá usar**",
                "**Antes de executar**",
                "**O que fazer**",
                "**Evidência esperada**",
                "**Entrega esperada**",
                "**Critérios de avaliação**",
            ):
                self.assertIn(label, section, f"{level}: {label}")

    def test_style_decision_frames_make_use_and_avoidance_explicit(self):
        text = (MODULE / "padroes-e-decisoes.md").read_text(encoding="utf-8")

        for style in (
            "Camadas",
            "Pipes and Filters",
            "Microkernel",
            "Monólito modular",
        ):
            self.assertIn(f"## {style}", text)
        for label in (
            "Responsabilidade",
            "Conectores",
            "Forças",
            "Anti-padrão",
            "Quando usar",
            "Evite quando",
        ):
            self.assertIn(label, text)

    def test_decision_page_restores_the_three_style_deep_dives(self):
        text = (MODULE / "padroes-e-decisoes.md").read_text(encoding="utf-8")
        expected = {
            "Camadas": ("camada fechada", "camada aberta", "sumidouro", "OCP", "MVC"),
            "Pipes and Filters": (
                "filtro sem estado",
                "filtro com estado",
                "rejeição",
                "ordenação",
                "throughput",
            ),
            "Microkernel": (
                "registro",
                "contrato de extensão",
                "compatibilidade",
                "core creep",
                "plugin",
            ),
        }
        for heading, terms in expected.items():
            section = text.split(f"## {heading}", 1)[1]
            for term in terms:
                self.assertIn(term, section)

    def test_every_example_mermaid_has_alt_caption_and_textual_reading(self):
        text = (MODULE / "exemplo-arquitetural.md").read_text(encoding="utf-8")
        diagrams = text.count("```mermaid")

        self.assertGreaterEqual(diagrams, 3)
        self.assertGreaterEqual(text.count("**Texto alternativo:**"), diagrams)
        self.assertGreaterEqual(text.count("*Figura "), diagrams)
        self.assertGreaterEqual(text.count("**Leitura textual da figura:**"), diagrams)

    def test_example_preserves_code_responsibilities_and_ecosystem_equivalences(self):
        text = (MODULE / "exemplo-arquitetural.md").read_text(encoding="utf-8")

        for fragment in (
            "processamento/",
            "aplicacao/",
            "dominio/",
            "filtros/",
            "adaptadores/",
            "`Pipeline`",
            "| Intenção | Python | Java | .NET |",
            "| contrato do filtro |",
            "| regra de dependência |",
        ):
            self.assertIn(fragment, text)

    def test_advanced_activities_name_a_concrete_workspace_and_start_condition(self):
        exercises = (MODULE / "exercicios.md").read_text(encoding="utf-8")
        sections = bloom_sections(exercises)

        for level, workspace in (
            ("Analisar", "analise-integracao"),
            ("Avaliar", "parecer.md"),
            ("Criar", "baseline-inicial"),
        ):
            section = sections[level]
            self.assertIn(workspace, section)
            self.assertIn("Condição inicial verificável", section)
            self.assertIn("**Entrega esperada**", section)

    def test_advanced_activities_share_a_root_delivery_location(self):
        exercises = (MODULE / "exercicios.md").read_text(encoding="utf-8")
        sections = bloom_sections(exercises)

        for level, delivery in (
            ("Analisar", "entregas/unidade-1/analise-integracao"),
            ("Avaliar", "entregas/unidade-1/avaliacao-leitos"),
            ("Criar", "entregas/unidade-1/baseline-inicial"),
        ):
            self.assertIn(delivery, sections[level])
            self.assertIn("raiz do repositório `arquitetura-software`", sections[level])

    def test_installation_starts_each_platform_at_clone_root(self):
        workshop = (MODULE / "oficina-de-ferramentas.md").read_text(
            encoding="utf-8"
        )

        for start, end in (
            ("### Windows", "### macOS"),
            ("### macOS", "### Linux"),
            ("### Linux", "## Preparação do laboratório"),
        ):
            platform = workshop.split(start, 1)[1].split(end, 1)[0]
            self.assertIn("terminal começa na raiz do clone `arquitetura-software`", platform)

    def test_diagrams_have_textual_readings(self):
        corpus = "\n".join(path.read_text(encoding="utf-8") for path in MODULE.glob("*.md"))

        self.assertGreaterEqual(corpus.count("```mermaid"), 3)
        self.assertGreaterEqual(
            corpus.count("**Leitura textual da figura:**"),
            corpus.count("```mermaid"),
        )

    def test_editorial_mermaid_figures_have_complete_accessible_context(self):
        pages = (
            MODULE / "conceitos.md",
            MODULE / "padroes-e-decisoes.md",
            MODULE / "estudo-de-caso.md",
        )
        contexts = []
        for page in pages:
            text = page.read_text(encoding="utf-8")
            contexts.extend(
                re.findall(
                    r"```mermaid\n.*?```\n\n"
                    r"\*\*Texto alternativo:\*\*.+?\n\n"
                    r"\*Figura (\d+) — .+? Fonte: .+?\*\n\n"
                    r"\*\*Leitura textual(?: da figura)?:\*\*.+?"
                    r"(?=\n\n|\Z)",
                    text,
                    re.DOTALL,
                )
            )

        self.assertEqual(3, len(contexts))

    def test_module_one_figure_numbers_follow_reading_order(self):
        pages = (
            MODULE / "conceitos.md",
            MODULE / "padroes-e-decisoes.md",
            MODULE / "exemplo-arquitetural.md",
            MODULE / "estudo-de-caso.md",
        )
        figures = []
        for page in pages:
            figures.extend(
                int(number)
                for number in re.findall(
                    r"\*Figura (\d+) — .+? Fonte: .+?\*",
                    page.read_text(encoding="utf-8"),
                )
            )

        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9], figures)

    def test_structurizr_models_one_application_with_internal_modules(self):
        workshop = (MODULE / "oficina-de-ferramentas.md").read_text(
            encoding="utf-8"
        )
        dsl = workshop.split("```structurizr", 1)[1].split("```", 1)[0]

        self.assertIn(
            'aplicacao = container "Aplicação hospitalar" '
            '"Monólito modular implantado como uma unidade" '
            '"Python 3.12 e FastAPI" {',
            dsl,
        )
        for module in ("agenda", "triagem", "faturamento", "auditoria"):
            self.assertRegex(dsl, rf"(?m)^\s*{module}\s*=\s*component\b")
            self.assertNotRegex(dsl, rf"(?m)^\s*{module}\s*=\s*container\b")
        self.assertIn('component aplicacao "Modulos"', dsl)
        self.assertNotRegex(
            dsl,
            r'\b(?:container|component)\s+"[^"]+"\s+"[^"]+"\s+'
            r'"(?:Microkernel|Pipes and filters|Módulo[^\"]*)"',
        )

    def test_workshop_captures_exact_evidence_files_on_both_shells(self):
        workshop = (MODULE / "oficina-de-ferramentas.md").read_text(
            encoding="utf-8"
        )
        for command in (
            "mkdir -p evidencias",
            "cp structurizr/workspace.dsl evidencias/workspace.dsl",
            "python -m pytest tests/test_estilos.py -q 2>&1 | tee evidencias/testes-estilos.txt",
            "python evidencias/comparacao.py 2>&1 | tee evidencias/comparacao-modificabilidade.txt",
            "python evidencias/comparacao.py 2>&1 | tee evidencias/comparacao-fluxo.txt",
            "New-Item -ItemType Directory -Force evidencias",
            r"Copy-Item .\structurizr\workspace.dsl .\evidencias\workspace.dsl",
            r".venv\Scripts\python.exe -m pytest tests/test_estilos.py -q 2>&1 | Tee-Object -FilePath evidencias\testes-estilos.txt",
            r".venv\Scripts\python.exe evidencias\comparacao.py 2>&1 | Tee-Object -FilePath evidencias\comparacao-modificabilidade.txt",
            r".venv\Scripts\python.exe evidencias\comparacao.py 2>&1 | Tee-Object -FilePath evidencias\comparacao-fluxo.txt",
        ):
            self.assertIn(command, workshop)
        for filename in (
            "testes-estilos.txt",
            "comparacao-modificabilidade.txt",
            "comparacao-fluxo.txt",
            "workspace.dsl",
            "ADR-001-estilo-inicial.md",
        ):
            self.assertIn(filename, workshop)

    def test_workshop_reports_current_test_order_and_counts(self):
        workshop = (MODULE / "oficina-de-ferramentas.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("O terceiro teste compara", workshop)
        self.assertIn("3 passed", workshop)
        self.assertIn("4 passed", workshop)
        self.assertNotIn("2 passed", workshop)

    def test_advanced_scenarios_do_not_leak_the_resolved_case(self):
        exercises = (MODULE / "exercicios.md").read_text(encoding="utf-8")
        sections = bloom_sections(exercises)
        analyze = sections["Analisar"].casefold()
        evaluate = sections["Avaliar"].casefold()

        self.assertIn("rede de laboratórios", analyze)
        self.assertIn("disponibilidade de leitos", evaluate)
        for section in (analyze, evaluate):
            for leaked in (
                "agenda",
                "triagem",
                "faturamento",
                "matriz do estudo de caso",
                "estudo de caso",
                "adr-001",
            ):
                self.assertNotIn(leaked, section)
            for canonical in (
                "deve adotar",
                "a recomendação é",
                "solução correta",
            ):
                self.assertNotIn(canonical, section)

    def test_adr_is_a_documentation_practice_not_a_solution_pattern(self):
        text = (MODULE / "padroes-e-decisoes.md").read_text(encoding="utf-8")

        self.assertIn("prática de documentação de decisões", text)
        self.assertNotIn("Repository, Adapter, Circuit Breaker e ADR são padrões", text)
        self.assertNotIn("| Padrão de decisão | ADR |", text)

    def test_workshop_has_process_scoped_powershell_contingency(self):
        workshop = (MODULE / "oficina-de-ferramentas.md").read_text(
            encoding="utf-8"
        )
        windows = workshop.split("### Windows", 1)[1].split("### macOS", 1)[0]

        self.assertIn(
            "Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned",
            windows,
        )
        self.assertRegex(
            windows,
            r"(?is)escopo `Process`.*(?:feche|fechar).*PowerShell",
        )
        self.assertLess(
            windows.index("py -m venv .venv"),
            windows.index(
                "Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned"
            ),
        )
        self.assertLess(
            windows.index(
                "Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned"
            ),
            windows.index(r".venv\Scripts\Activate.ps1"),
        )
        self.assertLess(
            windows.index(r".venv\Scripts\Activate.ps1"),
            windows.index(r'.venv\Scripts\python.exe -m pip install -e ".[dev]"'),
        )

        powershell_blocks = re.findall(
            r"```powershell\n(.*?)```", windows, re.DOTALL
        )
        activation_blocks = [
            block.strip()
            for block in powershell_blocks
            if "Activate.ps1" in block
        ]
        self.assertEqual(
            [r".venv\Scripts\Activate.ps1"],
            activation_blocks,
        )
        activation_end = windows.index("```", windows.index("Activate.ps1")) + 3
        checkpoint = windows.index("`(.venv)`", activation_end)
        installation = windows.index(
            r'.venv\Scripts\python.exe -m pip install -e ".[dev]"'
        )
        self.assertLess(activation_end, checkpoint)
        self.assertLess(checkpoint, installation)

        after_venv_creation = windows.split("py -m venv .venv", 1)[1]
        later_commands = "\n".join(
            re.findall(
                r"```powershell\n(.*?)```", after_venv_creation, re.DOTALL
            )
        )
        self.assertNotRegex(later_commands, r"(?m)^python(?:\.exe)?\s")
        for line in later_commands.splitlines():
            if any(
                marker in line
                for marker in (
                    "-m pip",
                    "-m pytest",
                    "python.exe --version",
                    "python.exe evidencias",
                )
            ):
                self.assertTrue(
                    line.startswith(r".venv\Scripts\python.exe"),
                    line,
                )

        no_activation = windows.split("#### Rota sem ativação", 1)[1]
        for command in (
            r".venv\Scripts\python.exe -m pip install --upgrade pip",
            r'.venv\Scripts\python.exe -m pip install -e ".[dev]"',
            r".venv\Scripts\python.exe --version",
            r".venv\Scripts\python.exe -m pytest --version",
            r".venv\Scripts\python.exe -m pytest tests -q",
            r".venv\Scripts\python.exe -m pytest tests/test_estilos.py -q",
        ):
            self.assertIn(command, no_activation)
        commands = "\n".join(
            re.findall(r"```powershell\n(.*?)```", no_activation, re.DOTALL)
        )
        self.assertNotRegex(commands, r"(?m)^python(?:\.exe)?\s")
        self.assertNotIn("Activate.ps1", commands)

    def test_synthesis_links_primary_and_official_public_sources(self):
        text = (MODULE / "sintese-e-referencias.md").read_text(encoding="utf-8")
        for url in (
            "https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions",
            "https://c4model.com/diagrams",
            "https://docs.structurizr.com/dsl",
            "https://docs.python.org/3/tutorial/",
            "https://docs.pytest.org/en/stable/getting-started.html",
            "https://www.sei.cmu.edu/library/quality-attributes/",
        ):
            self.assertIn(url, text)


if __name__ == "__main__":
    unittest.main()
