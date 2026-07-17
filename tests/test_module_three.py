from pathlib import Path
import re
import unittest

from tests.course_assertions import assert_module_contract


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "docs" / "modulo-3-servicos"
LAB = ROOT / "laboratorios" / "plataforma-hospitalar"
COMPOSE = LAB / "infra" / "compose.servicos.yml"


class ModuleThreeTest(unittest.TestCase):
    def test_content_contract(self):
        assert_module_contract(
            self,
            "modulo-3-servicos",
            (
                "capacidade de negócio",
                "bounded context",
                "coesão",
                "acoplamento",
                "monólito modular",
                "macrosserviço",
                "microsserviço",
                "banco por serviço",
                "consistência",
                "SAGA",
                "CQRS",
                "Docker Compose",
                "PostgreSQL",
            ),
        )

    def test_module_has_exactly_eight_pages_and_expected_navigation(self):
        pages = sorted(path.name for path in MODULE.glob("*.md"))
        self.assertEqual(
            pages,
            sorted(
                (
                    "index.md",
                    "conceitos.md",
                    "padroes-e-decisoes.md",
                    "exemplo-arquitetural.md",
                    "estudo-de-caso.md",
                    "oficina-de-ferramentas.md",
                    "exercicios.md",
                    "sintese-e-referencias.md",
                )
            ),
        )
        navigation = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        section = navigation.split('  - "Módulo 3 — Serviços":', 1)[1].split(
            '  - "Módulo 4 — Governança":', 1
        )[0]
        self.assertEqual(8, section.count("modulo-3-servicos/"))

    def test_module_is_substantial_and_uses_accessible_mermaid(self):
        corpus = "\n".join(
            path.read_text(encoding="utf-8") for path in MODULE.glob("*.md")
        )
        words = re.findall(r"\b[^\W_]+(?:[-'][^\W_]+)*\b", corpus)
        self.assertGreaterEqual(len(words), 5000)
        self.assertLessEqual(len(words), 8500)
        self.assertGreaterEqual(corpus.count("```mermaid"), 3)
        self.assertEqual(
            corpus.count("```mermaid"),
            corpus.count("**Leitura textual da figura:**"),
        )

    def test_workshop_documents_partial_failure_and_reproducible_cleanup(self):
        workshop = (MODULE / "oficina-de-ferramentas.md").read_text(
            encoding="utf-8"
        )
        for fragment in (
            "compose.servicos.yml up -d --build --wait",
            "docker compose ps",
            "localhost:8001/health",
            "localhost:8002/health",
            "docker compose -f infra/compose.servicos.yml stop elegibilidade",
            "503 Service Unavailable",
            "dependencia_indisponivel",
            "test_service_boundaries.py",
            "docker compose -f infra/compose.servicos.yml down -v",
        ):
            self.assertIn(fragment, workshop)

    def test_patterns_are_introduced_without_claiming_they_are_default_choices(self):
        patterns = (MODULE / "padroes-e-decisoes.md").read_text(
            encoding="utf-8"
        )
        for fragment in (
            "SAGA não é uma transação ACID distribuída",
            "CQRS não exige dois bancos",
            "não aplique CQRS por padrão",
            "CAP se torna uma decisão durante uma partição",
            "consistência eventual não significa",
        ):
            self.assertIn(fragment.casefold(), patterns.casefold())

    def test_compose_declares_two_databases_and_healthchecks(self):
        compose = COMPOSE.read_text(encoding="utf-8")
        for service in (
            "db_elegibilidade:",
            "db_exames:",
            "elegibilidade:",
            "exames:",
        ):
            self.assertIn(service, compose)
        self.assertGreaterEqual(compose.count("healthcheck:"), 4)
        self.assertNotIn("container_name:", compose)


if __name__ == "__main__":
    unittest.main()
