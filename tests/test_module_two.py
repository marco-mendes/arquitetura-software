from pathlib import Path
import unittest
import re
import subprocess
from tempfile import TemporaryDirectory

import yaml

from tests.course_assertions import assert_module_contract
from scripts.validate_content import bloom_sections


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "docs" / "modulo-2-apis"
LAB = ROOT / "laboratorios" / "plataforma-hospitalar"
OPENAPI = LAB / "contratos" / "openapi.yaml"
SPECTRAL_PACKAGE = "@stoplight/spectral-cli@6.16.1"


class ModuleTwoTest(unittest.TestCase):
    def test_unit_two_compares_api_styles_and_protocols_architecturally(self):
        text = (MODULE / "conceitos.md").read_text(encoding="utf-8")
        for term in (
            "REST",
            "GraphQL",
            "gRPC",
            "WebSocket",
            "contrato",
            "consumidor",
        ):
            self.assertIn(term, text)

    def test_unit_two_figure_numbers_follow_navigation_reading_order(self):
        pages = (
            "index.md",
            "conceitos.md",
            "padroes-e-decisoes.md",
            "exemplo-arquitetural.md",
            "estudo-de-caso.md",
            "oficina-de-ferramentas.md",
            "exercicios.md",
            "sintese-e-referencias.md",
        )
        figures = [
            int(number)
            for page in pages
            for number in re.findall(
                r"^\*Figura (\d+) —",
                (MODULE / page).read_text(encoding="utf-8"),
                re.MULTILINE,
            )
        ]

        self.assertEqual(list(range(3, 9)), figures)

    def test_api_workshop_names_the_local_application_before_commands(self):
        text = (MODULE / "oficina-de-ferramentas.md").read_text(
            encoding="utf-8"
        )
        for fragment in (
            "API de elegibilidades da plataforma hospitalar",
            "src/hospital/api/main.py",
            "http://127.0.0.1:8000",
        ):
            self.assertIn(fragment, text)

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
            f"npx {SPECTRAL_PACKAGE} lint contratos/openapi.yaml",
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
            "https://github.com/stoplightio/spectral",
            "https://docs.python.org/3/using/index.html",
            "https://brew.sh/",
            "https://grpc.io/docs/what-is-grpc/introduction/",
            "https://graphql.org/learn/",
        ):
            self.assertIn(url, text)

    def test_rest_constraints_are_complete_and_distinguish_rest_from_rpc(self):
        concepts = (MODULE / "conceitos.md").read_text(encoding="utf-8")
        section = concepts.split("## Restrições REST de Fielding", 1)[1].split(
            "## ", 1
        )[0]
        for term in (
            "cliente-servidor",
            "sem estado",
            "cache",
            "interface uniforme",
            "identificação de recursos",
            "representações",
            "mensagens autodescritivas",
            "hipermídia",
            "sistema em camadas",
            "código sob demanda",
            "opcional",
            "RPC com aparência de recurso",
            "uma API HTTP não é automaticamente REST",
        ):
            self.assertIn(term.casefold(), section.casefold(), term)

    def test_linux_setup_adds_flathub_before_install_and_verifies_bruno(self):
        workshop = (MODULE / "oficina-de-ferramentas.md").read_text(
            encoding="utf-8"
        )
        linux = workshop.split("### Linux", 1)[1].split(
            "## Preparação do laboratório", 1
        )[0]
        remote = (
            "flatpak remote-add --if-not-exists flathub "
            "https://flathub.org/repo/flathub.flatpakrepo"
        )
        install = "flatpak install flathub com.usebruno.Bruno"
        verify = "flatpak info com.usebruno.Bruno"
        for command in (remote, install, verify):
            self.assertIn(command, linux)
        self.assertLess(linux.index(remote), linux.index(install))
        self.assertLess(linux.index(install), linux.index(verify))
        self.assertIn("https://www.usebruno.com/downloads", linux)

    def test_spectral_version_and_pipeline_failures_are_not_masked(self):
        workshop = (MODULE / "oficina-de-ferramentas.md").read_text(
            encoding="utf-8"
        )
        self.assertGreaterEqual(workshop.count(SPECTRAL_PACKAGE), 4)
        self.assertNotRegex(workshop, r"@stoplight/spectral-cli(?!@6\.16\.1)")
        for config in (
            ROOT / ".spectral.yaml",
            LAB / ".spectral.yaml",
            LAB / "contratos" / ".spectral.yaml",
        ):
            self.assertIn(SPECTRAL_PACKAGE, config.read_text(encoding="utf-8"))

        capture_blocks = [
            block
            for block in re.findall(r"```bash\n(.*?)```", workshop, re.DOTALL)
            if "| tee" in block
        ]
        self.assertGreaterEqual(len(capture_blocks), 2)
        for block in capture_blocks:
            self.assertIn("set -o pipefail", block)

        powershell_captures = [
            block
            for block in re.findall(
                r"```powershell\n(.*?)```", workshop, re.DOTALL
            )
            if "Tee-Object" in block
        ]
        self.assertGreaterEqual(len(powershell_captures), 2)
        for block in powershell_captures:
            self.assertIn("$LASTEXITCODE", block)
            self.assertRegex(block, r"if \(\$\w+Exit -ne 0\)")

    def test_documented_spectral_edit_targets_validated_request_example(self):
        workshop = (MODULE / "oficina-de-ferramentas.md").read_text(
            encoding="utf-8"
        )
        for fragment in (
            "paths./elegibilidades.post.requestBody.content.application/json.examples.pedidoValido.value.cpf",
            "oas3-valid-media-example",
            '"cpf" property must match pattern',
        ):
            self.assertIn(fragment, workshop)
        self.assertIn(
            "Alterar `components.schemas.PedidoElegibilidade.examples` não "
            "exercita a regra de exemplo de mídia.",
            workshop,
        )

        contract = yaml.safe_load(OPENAPI.read_text(encoding="utf-8"))
        contract["paths"]["/elegibilidades"]["post"]["requestBody"]["content"][
            "application/json"
        ]["examples"]["pedidoValido"]["value"]["cpf"] = "123"
        with TemporaryDirectory(dir=LAB) as temporary:
            experiment = Path(temporary) / "openapi-experimento.yaml"
            experiment.write_text(
                yaml.safe_dump(contract, sort_keys=False, allow_unicode=True),
                encoding="utf-8",
            )
            result = subprocess.run(
                ["npx", SPECTRAL_PACKAGE, "lint", str(experiment)],
                cwd=LAB,
                capture_output=True,
                text=True,
                check=False,
            )
        output = result.stdout + result.stderr
        self.assertNotEqual(0, result.returncode, output)
        self.assertIn("oas3-valid-media-example", output)
        self.assertIn('"cpf" property must match pattern', output)


if __name__ == "__main__":
    unittest.main()
