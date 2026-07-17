from pathlib import Path
import re
import tomllib
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "docs/projeto-integrador"
LAB = ROOT / "laboratorios/plataforma-hospitalar"


class IntegrativeProjectTest(unittest.TestCase):
    def test_context_covers_actors_capabilities_and_architectural_constraints(self):
        text = (PROJECT / "contexto-hospitalar.md").read_text(encoding="utf-8")
        required_terms = (
            "paciente",
            "profissional",
            "plano de saúde",
            "operadora",
            "laboratório",
            "cadastro",
            "agenda",
            "elegibilidade",
            "autorização",
            "exames",
            "resultados",
            "faturamento",
            "notificações",
            "auditoria",
            "privacidade",
            "rastreabilidade",
            "interoperabilidade",
            "disponibilidade",
        )
        for term in required_terms:
            self.assertIn(term.casefold(), text.casefold(), term)

    def test_six_increments_are_structured_and_genuinely_cumulative(self):
        text = (PROJECT / "incrementos.md").read_text(encoding="utf-8")
        increments = re.split(r"(?m)^## Incremento \d[^\n]*$", text)[1:]
        headings = re.findall(r"(?m)^## Incremento \d[^\n]*$", text)

        self.assertEqual(6, len(headings))
        self.assertEqual(6, len(increments))
        for number, increment in enumerate(increments, start=1):
            for section in (
                "Objetivo",
                "Insumos",
                "Passos",
                "Artefato",
                "Evidência",
                "Conexão com o próximo encontro",
            ):
                self.assertIn(f"### {section}", increment, f"incremento {number}")
            if number > 1:
                self.assertIn(
                    f"incremento {number - 1}",
                    increment.casefold(),
                    f"incremento {number} não reutiliza o anterior",
                )

        for integration in ("plano de saúde", "laboratório"):
            self.assertIn(integration, text.casefold())

    def test_delivery_models_link_shared_architecture_references(self):
        text = (PROJECT / "modelos-de-entrega.md").read_text(encoding="utf-8")
        for label in (
            "Registro de decisão",
            "Cenário de atributo de qualidade",
            "Contrato de integração",
            "Evidência reproduzível",
        ):
            self.assertIn(label, text)
        for link in (
            "../referencia/template-adr.md",
            "../referencia/atributos-de-qualidade.md",
            "../referencia/catalogo-de-padroes.md",
            "../referencia/guia-de-ferramentas.md",
        ):
            self.assertIn(link, text)

    def test_assessment_uses_exactly_six_percentages_summing_to_100(self):
        text = (PROJECT / "criterios-de-avaliacao.md").read_text(encoding="utf-8")
        rows = re.findall(r"(?m)^\|\s*([^|]+?)\s*\|\s*(\d+)%\s*\|", text)
        expected = {
            "Coerência": 20,
            "Decisões e trade-offs": 20,
            "Contratos e integrações": 15,
            "Dados e eventos": 15,
            "Governança e operação": 15,
            "Clareza e evidências": 15,
        }

        self.assertEqual(expected, dict((label.strip(), int(value)) for label, value in rows))
        self.assertEqual(100, sum(int(value) for _, value in rows))

    def test_project_pages_are_in_navigation(self):
        config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        navigation = str(config["nav"])
        for page in (
            "projeto-integrador/index.md",
            "projeto-integrador/contexto-hospitalar.md",
            "projeto-integrador/incrementos.md",
            "projeto-integrador/modelos-de-entrega.md",
            "projeto-integrador/criterios-de-avaliacao.md",
        ):
            self.assertIn(page, navigation)

    def test_base_workspace_declares_runtime_and_development_dependencies(self):
        config = tomllib.loads((LAB / "pyproject.toml").read_text(encoding="utf-8"))
        project = config["project"]
        self.assertEqual(">=3.11", project["requires-python"])
        self.assertEqual(
            {
                "fastapi",
                "uvicorn",
                "pydantic",
                "httpx",
                "psycopg[binary]",
                "aio-pika",
                "opentelemetry-sdk",
                "opentelemetry-exporter-otlp-proto-http",
            },
            set(project["dependencies"]),
        )
        self.assertEqual(
            {"pytest", "pytest-asyncio"},
            set(project["optional-dependencies"]["dev"]),
        )
        self.assertTrue((LAB / "src/hospital/__init__.py").is_file())
        self.assertTrue((LAB / "tests/test_package.py").is_file())

    def test_workspace_readme_has_equivalent_posix_and_powershell_preparation(self):
        text = (LAB / "README.md").read_text(encoding="utf-8")
        for heading in ("### PowerShell", "### Shells POSIX"):
            self.assertIn(heading, text)
        self.assertEqual(2, text.count('pip install -e ".[dev]"'))
        self.assertEqual(2, text.count("python -m pytest tests"))

    def test_workspace_readme_maps_python_reference_to_java_and_dotnet(self):
        text = (LAB / "README.md").read_text(encoding="utf-8")
        self.assertIn("## Equivalências em Java e .NET", text)
        self.assertIn("Python é a referência executável", text)
        for ecosystem in ("Spring Boot", "JUnit", "ASP.NET Core", "xUnit"):
            self.assertIn(ecosystem, text)


if __name__ == "__main__":
    unittest.main()
