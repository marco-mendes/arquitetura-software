from pathlib import Path
import re
import unittest

from tests.course_assertions import assert_module_contract
from scripts.validate_content import bloom_sections


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "docs" / "modulo-1-visao-geral"


class ModuleOneTest(unittest.TestCase):
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
