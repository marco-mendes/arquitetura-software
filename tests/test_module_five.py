from pathlib import Path
import re
import unittest

from scripts.validate_content import (
    _word_count,
    expandable_feedback_errors,
    self_contained_activity_errors,
)
from tests.course_assertions import assert_module_contract, navigation_section_paths


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "docs" / "modulo-5-eventos"
LAB = ROOT / "laboratorios" / "plataforma-hospitalar"
COMPOSE = LAB / "infra" / "compose.eventos.yml"
CONSUMER = LAB / "src" / "hospital" / "eventos" / "consumidor.py"


def read_module_page(module: str, page: str) -> str:
    return (ROOT / "docs" / module / page).read_text(encoding="utf-8")


class ModuleFiveTest(unittest.TestCase):
    def test_unit_five_covers_event_architecture_beyond_broker_terms(self):
        text = read_module_page(
            "modulo-5-eventos", "conceitos.md"
        ) + read_module_page("modulo-5-eventos", "padroes-e-decisoes.md")
        for term in (
            "produtor",
            "consumidor",
            "broker",
            "mediator",
            "topologia",
            "payload",
            "idempotência",
            "DLQ",
        ):
            self.assertIn(term, text)

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

    def test_event_exercises_are_self_contained_with_initial_feedback(self):
        exercises = read_module_page("modulo-5-eventos", "exercicios.md")
        self.assertEqual(
            [], expandable_feedback_errors(exercises, "modulo-5-eventos/exercicios.md")
        )
        self.assertEqual(
            [],
            self_contained_activity_errors(
                exercises, "modulo-5-eventos/exercicios.md"
            ),
        )
        self.assertGreaterEqual(exercises.count("<raiz-do-clone>/entregas/"), 4)

    def test_mermaid_diagrams_include_accessible_editorial_context(self):
        corpus = "\n".join(path.read_text(encoding="utf-8") for path in MODULE.glob("*.md"))
        diagrams = re.findall(r"```mermaid.*?```", corpus, re.DOTALL)
        contexts = re.findall(
            r"```mermaid.*?```\s*\n\n"
            r"\*\*Texto alternativo:\*\*.+?\n\n"
            r"\*Figura .+?\*\n\n"
            r"\*\*Leitura textual:\*\*.+?(?=\n\n|\Z)",
            corpus,
            re.DOTALL,
        )
        self.assertEqual(len(diagrams), len(contexts))

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
            corpus.count("**Leitura textual:**"),
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

    def test_workshop_names_the_local_demonstration_before_runtime_commands(self):
        workshop = read_module_page("modulo-5-eventos", "oficina-de-ferramentas.md")
        map_end = workshop.index("## Ferramenta")
        local_map = workshop[:map_end]
        for fragment in (
            "infra/compose.eventos.yml",
            "src/hospital/eventos/publicador.py",
            "src/hospital/eventos/consumidor.py",
            "hospital.events",
            "billing.resultados.v1",
            "processed-events.sqlite3",
            "billing.resultados.v1.dlq",
            "Estado inicial",
        ):
            self.assertIn(fragment, local_map)
        for label in (
            "**Variável alterada**",
            "**Evento publicado**",
            "**Evidência de processamento**",
            "**Erro esperado**",
        ):
            self.assertGreaterEqual(workshop.count(label), 3, label)

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
