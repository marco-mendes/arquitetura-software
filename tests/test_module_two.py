from pathlib import Path
import unittest

from tests.course_assertions import assert_module_contract
from scripts.validate_content import bloom_sections


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "docs" / "modulo-2-apis"


class ModuleTwoTest(unittest.TestCase):
    def test_content(self):
        assert_module_contract(
            self,
            "modulo-2-apis",
            (
                "REST",
                "HTTP",
                "OpenAPI",
                "idempotência",
                "versionamento",
                "paginação",
                "FastAPI",
                "Bruno",
                "Spectral",
                "ASP.NET Core",
                "Spring Boot",
            ),
        )

    def test_workshop_has_executable_contract_workflow(self):
        workshop = (MODULE / "oficina-de-ferramentas.md").read_text(
            encoding="utf-8"
        )
        for fragment in (
            "uvicorn hospital.api.main:app --reload",
            "http://127.0.0.1:8000/docs",
            "openapi.yaml",
            "POST /elegibilidades",
            "GET /elegibilidades/{protocolo}",
            "npx @stoplight/spectral-cli lint contratos/openapi.yaml",
            "202 Accepted",
            "422 Unprocessable Entity",
            "Ctrl+C",
        ):
            self.assertIn(fragment, workshop)

    def test_windows_commands_keep_using_explicit_virtualenv_python(self):
        workshop = (MODULE / "oficina-de-ferramentas.md").read_text(
            encoding="utf-8"
        )
        windows = workshop.split("### Windows", 1)[1].split("### macOS", 1)[0]

        self.assertIn("py -m venv .venv", windows)
        self.assertIn(
            '`.venv\\Scripts\\python.exe -m pip install -e ".[dev]"`', windows
        )
        self.assertIn(
            ".venv\\Scripts\\python.exe -m uvicorn hospital.api.main:app --reload",
            workshop,
        )
        self.assertNotIn("Set-ExecutionPolicy -Scope LocalMachine", windows)

    def test_advanced_prompts_are_guided_without_canonical_answer_leaks(self):
        exercises = (MODULE / "exercicios.md").read_text(encoding="utf-8")
        sections = bloom_sections(exercises)
        for level in ("Analisar", "Avaliar", "Criar"):
            section = sections[level].casefold()
            for leak in (
                "a resposta correta",
                "deve adotar rest",
                "deve usar gateway",
                "solução canônica",
            ):
                self.assertNotIn(leak, section)

    def test_synthesis_uses_public_primary_or_official_references(self):
        text = (MODULE / "sintese-e-referencias.md").read_text(encoding="utf-8")
        for url in (
            "https://www.rfc-editor.org/rfc/rfc9110",
            "https://spec.openapis.org/oas/v3.1.0",
            "https://fastapi.tiangolo.com/",
            "https://docs.usebruno.com/",
            "https://docs.stoplight.io/docs/spectral/",
            "https://grpc.io/docs/what-is-grpc/introduction/",
            "https://graphql.org/learn/",
        ):
            self.assertIn(url, text)


if __name__ == "__main__":
    unittest.main()
