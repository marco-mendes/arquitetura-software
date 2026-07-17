from pathlib import Path
import unittest

from scripts.validate_content import _word_count
from tests.course_assertions import assert_module_contract, navigation_section_paths


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "docs" / "modulo-5-eventos"
LAB = ROOT / "laboratorios" / "plataforma-hospitalar"
COMPOSE = LAB / "infra" / "compose.eventos.yml"
CONSUMER = LAB / "src" / "hospital" / "eventos" / "consumidor.py"


class ModuleFiveTest(unittest.TestCase):
    def test_content_contract(self):
        assert_module_contract(
            self,
            "modulo-5-eventos",
            (
                "evento",
                "comando",
                "mensagem",
                "broker",
                "fila",
                "tópico",
                "entrega pelo menos uma vez",
                "idempotência",
                "ordenação",
                "dead-letter queue",
                "RabbitMQ",
                "Kafka",
                "consistência eventual",
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
        section = navigation_section_paths("Módulo 5 — Eventos")
        self.assertEqual(
            {f"modulo-5-eventos/{page}" for page in pages},
            set(section),
        )

        corpus = "\n".join(path.read_text(encoding="utf-8") for path in MODULE.glob("*.md"))
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

    def test_workshop_has_rabbitmq_tracks_and_idempotency_evidence(self):
        workshop = (MODULE / "oficina-de-ferramentas.md").read_text(encoding="utf-8")
        for fragment in (
            "compose.eventos.yml config --quiet",
            "compose.eventos.yml up -d --build --wait",
            "compose.eventos.yml down -v",
            "hospital.events",
            "billing.resultados.v1",
            "ResultadoLaboratorialDisponibilizado.v1",
            "test_event_idempotency.py",
            "COMPOSE_LIVE=1",
            "dead-letter",
            "RABBITMQ_PORT",
            "RABBITMQ_MANAGEMENT_PORT",
        ):
            self.assertIn(fragment, workshop)
        self.assertIn("Kafka", workshop)
        self.assertIn("Extensão", workshop)

    def test_workshop_has_a_native_powershell_dlq_proof(self):
        workshop = (MODULE / "oficina-de-ferramentas.md").read_text(encoding="utf-8")
        for fragment in (
            "**Verificação no PowerShell**",
            "$env:RABBITMQ_MANAGEMENT_PORT = 15673",
            "curl.exe --fail --silent --user guest:guest $dlqUrl",
            "api/queues/%2F/billing.resultados.v1.dlq",
            "$response.messages -lt 1",
            "Remove-Item Env:RABBITMQ_MANAGEMENT_PORT",
        ):
            self.assertIn(fragment, workshop)

    def test_local_stack_declares_durable_exchange_queue_and_dlx(self):
        compose = COMPOSE.read_text(encoding="utf-8")
        self.assertIn("rabbitmq:4-management", compose)
        self.assertIn("RABBITMQ_PORT", compose)
        self.assertIn("RABBITMQ_MANAGEMENT_PORT", compose)
        self.assertNotIn("container_name:", compose)

    def test_dead_letter_binding_preserves_the_original_routing_key(self):
        consumer = CONSUMER.read_text(encoding="utf-8")
        self.assertIn("await dlq.bind(dlx, routing_key=ROUTING_KEY)", consumer)


if __name__ == "__main__":
    unittest.main()
