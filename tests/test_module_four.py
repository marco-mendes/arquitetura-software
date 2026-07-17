from pathlib import Path
import re
import unittest

from tests.course_assertions import assert_module_contract


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "docs" / "modulo-4-governanca"
LAB = ROOT / "laboratorios" / "plataforma-hospitalar"
COMPOSE = LAB / "infra" / "compose.governanca.yml"
KONG = LAB / "infra" / "kong" / "kong.yml"
KONG_DOCKERFILE = LAB / "infra" / "kong" / "Dockerfile"
COLLECTOR = LAB / "infra" / "observabilidade" / "otel-collector.yml"
COLLECTOR_DOCKERFILE = LAB / "infra" / "observabilidade" / "Dockerfile"


class ModuleFourTest(unittest.TestCase):
    def test_content_contract(self):
        assert_module_contract(
            self,
            "modulo-4-governanca",
            (
                "governança",
                "política",
                "gateway",
                "rate limiting",
                "correlation ID",
                "logs",
                "métricas",
                "traces",
                "SLO",
                "OpenTelemetry",
                "Jaeger",
                "Kong",
            ),
        )

    def test_module_has_eight_pages_navigation_and_accessible_diagrams(self):
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
        section = navigation.split('  - "Módulo 4 — Governança":', 1)[1].split(
            '  - "Módulo 5 — Eventos":', 1
        )[0]
        self.assertEqual(8, section.count("modulo-4-governanca/"))

        corpus = "\n".join(path.read_text(encoding="utf-8") for path in MODULE.glob("*.md"))
        words = re.findall(r"\b[^\W_]+(?:[-'][^\W_]+)*\b", corpus)
        self.assertGreaterEqual(len(words), 5000)
        self.assertLessEqual(len(words), 8500)
        self.assertGreaterEqual(corpus.count("```mermaid"), 3)
        self.assertEqual(
            corpus.count("```mermaid"),
            corpus.count("**Leitura textual da figura:**"),
        )

    def test_workshop_covers_safe_reproducible_governance_evidence(self):
        workshop = (MODULE / "oficina-de-ferramentas.md").read_text(encoding="utf-8")
        for fragment in (
            "compose.governanca.yml config --quiet",
            "compose.governanca.yml up -d --build --wait",
            "http://localhost:${ELEGIBILIDADE_PORT}/elegibilidades/paciente-001",
            "http://localhost:${GATEWAY_PORT}/hospital/elegibilidades/paciente-001",
            "X-Correlation-ID",
            "api/traces/${TRACE_ID}",
            "429 Too Many Requests",
            "kong.yml",
            "docker compose -f infra/compose.governanca.yml up -d --build kong",
            "docker compose -f infra/compose.governanca.yml down -v",
            "test_gateway_policy.py",
        ):
            self.assertIn(fragment, workshop)

    def test_declarative_stack_has_reproducible_runtime_policies(self):
        compose = COMPOSE.read_text(encoding="utf-8")
        kong = KONG.read_text(encoding="utf-8")
        collector = COLLECTOR.read_text(encoding="utf-8")
        for service in ("elegibilidade:", "kong:", "otel-collector:", "jaeger:"):
            self.assertIn(service, compose)
        self.assertIn("KONG_DATABASE: \"off\"", compose)
        self.assertIn("KONG_DECLARATIVE_CONFIG: /kong/kong.yml", compose)
        self.assertIn("KONG_TRACING_INSTRUMENTATIONS: request", compose)
        self.assertIn("build: ./kong", compose)
        self.assertIn("FROM kong:3.8.0", KONG_DOCKERFILE.read_text(encoding="utf-8"))
        self.assertNotIn("container_name:", compose)
        self.assertIn("FROM kong:3.8.0", KONG_DOCKERFILE.read_text(encoding="utf-8"))
        self.assertIn("build: ./observabilidade", compose)
        self.assertIn("FROM otel/opentelemetry-collector-contrib:0.111.0", COLLECTOR_DOCKERFILE.read_text(encoding="utf-8"))
        self.assertIn("image: jaegertracing/all-in-one:", compose)

        for fragment in (
            "_format_version: \"3.0\"",
            "paths:",
            "- /hospital",
            "name: correlation-id",
            "header_name: X-Correlation-ID",
            "echo_downstream: true",
            "name: rate-limiting",
            "second: 3",
            "name: opentelemetry",
            "traces_endpoint: http://otel-collector:4318/v1/traces",
            "extract: [w3c]",
            "inject: [w3c]",
            "default_format: w3c",
            "sampling_rate: 1",
        ):
            self.assertIn(fragment, kong)
        self.assertNotIn("tracing_sampling_rate", kong)
        self.assertNotIn("header_type:", kong)
        for fragment in ("receivers:", "otlp:", "exporters:", "otlp/jaeger:", "jaeger:4317"):
            self.assertIn(fragment, collector)


if __name__ == "__main__":
    unittest.main()
