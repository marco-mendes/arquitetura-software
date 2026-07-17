from pathlib import Path
import unittest

from scripts.validate_content import _word_count
from tests.course_assertions import assert_module_contract, navigation_section_paths


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "docs" / "modulo-3-servicos"
LAB = ROOT / "laboratorios" / "plataforma-hospitalar"
COMPOSE = LAB / "infra" / "compose.servicos.yml"
POSTGRES_INIT = LAB / "infra" / "postgres" / "init.sql"


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
        section = navigation_section_paths("Módulo 3 — Serviços")
        self.assertEqual(
            {f"modulo-3-servicos/{page}" for page in pages},
            set(section),
        )

    def test_module_is_substantial_and_uses_accessible_mermaid(self):
        corpus = "\n".join(
            path.read_text(encoding="utf-8") for path in MODULE.glob("*.md")
        )
        words = _word_count(corpus)
        self.assertGreaterEqual(words, 5000)
        self.assertLessEqual(words, 8500)
        self.assertGreaterEqual(corpus.count("```mermaid"), 3)
        # Diagramas Mermaid e infográficos gerados possuem leitura textual.
        # Os infográficos acrescentam equivalências além das exigidas pelos Mermaid.
        self.assertGreaterEqual(
            corpus.count("**Leitura textual da figura:**"),
            corpus.count("```mermaid"),
        )

    def test_workshop_documents_partial_failure_and_reproducible_cleanup(self):
        workshop = (MODULE / "oficina-de-ferramentas.md").read_text(
            encoding="utf-8"
        )
        for fragment in (
            "compose.servicos.yml up -d --build --wait",
            "docker compose ps",
            "localhost:${ELEGIBILIDADE_PORT}/health",
            "localhost:${EXAMES_PORT}/health",
            "docker compose -f infra/compose.servicos.yml stop elegibilidade",
            "503 Service Unavailable",
            "dependencia_indisponivel",
            "test_service_boundaries.py",
            "docker compose -f infra/compose.servicos.yml down -v",
        ):
            self.assertIn(fragment, workshop)

    def test_workshop_uses_a_running_health_wait_and_overrideable_ports(self):
        workshop = (MODULE / "oficina-de-ferramentas.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("wait elegibilidade", workshop)
        for fragment in (
            "docker compose -f infra/compose.servicos.yml up -d --wait",
            "ELEGIBILIDADE_PORT=18001",
            "EXAMES_PORT=18002",
            "$env:ELEGIBILIDADE_PORT = 18001",
            "$env:EXAMES_PORT = 18002",
            "localhost:${ELEGIBILIDADE_PORT}",
            "localhost:${EXAMES_PORT}",
            "4 passed",
            "test_exames_makes_its_own_database_failure_observable",
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

    def test_compose_enforces_database_network_boundaries_and_port_overrides(self):
        compose = COMPOSE.read_text(encoding="utf-8")
        for fragment in (
            "elegibilidade-db-net:",
            "exames-db-net:",
            "application-net:",
            "${ELEGIBILIDADE_PORT:-8001}:8000",
            "${EXAMES_PORT:-8002}:8000",
            "elegibilidade-db",
            "POSTGRES_USER: postgres",
            "POSTGRES_PASSWORD: local-elegibilidade-admin",
            "POSTGRES_PASSWORD: local-exames-admin",
        ):
            self.assertIn(fragment, compose)

        eligibility = compose.split("  elegibilidade:", 1)[1].split(
            "  exames:", 1
        )[0]
        exams = compose.split("  exames:", 1)[1].split("volumes:", 1)[0]
        self.assertIn("application-net", eligibility)
        self.assertIn("elegibilidade-db-net", eligibility)
        self.assertNotIn("exames-db-net", eligibility)
        self.assertIn("application-net", exams)
        self.assertIn("exames-db-net", exams)
        self.assertNotIn("elegibilidade-db-net", exams)

    def test_database_application_roles_are_explicitly_least_privilege(self):
        initialization = POSTGRES_INIT.read_text(encoding="utf-8")
        for role in ("elegibilidade", "exames"):
            self.assertIn(f"CREATE ROLE {role} LOGIN NOSUPERUSER", initialization)
            self.assertIn("NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS", initialization)


if __name__ == "__main__":
    unittest.main()
