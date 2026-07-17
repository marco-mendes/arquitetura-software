from datetime import UTC, datetime
import asyncio
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory


LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB / "src"))

from hospital.eventos.consumidor import ConsumidorFaturamento, ProcessedEventStore
from hospital.eventos.publicador import ResultadoLaboratorialDisponibilizadoV1


class InvalidMessage:
    def __init__(self):
        self.body = json.dumps({"event_id": "missing-fields"}).encode("utf-8")
        self.rejected_with_requeue = None

    async def reject(self, requeue: bool):
        self.rejected_with_requeue = requeue


class QueueWithInvalidMessage:
    def __init__(self, message: InvalidMessage):
        self.message = message

    async def get(self, fail: bool):
        return self.message


def test_duplicate_event_has_one_business_effect_and_two_attempts():
    event = ResultadoLaboratorialDisponibilizadoV1(
        event_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
        occurred_at=datetime(2026, 7, 17, 12, 0, tzinfo=UTC),
        exam_id="exam-sintetico-001",
        patient_id="patient-sintetico-001",
        result_reference="resultados/exam-sintetico-001",
    )

    with TemporaryDirectory() as directory:
        store = ProcessedEventStore(Path(directory) / "processed-events.sqlite3")
        consumer = ConsumidorFaturamento(store)

        first = consumer.processar_evento(event)
        second = consumer.processar_evento(event)

        assert first.processed is True
        assert second.processed is False
        assert store.business_effect_count() == 1
        assert store.attempts_for(event.event_id) == 2


def test_invalid_event_is_rejected_without_crashing_consumer():
    with TemporaryDirectory() as directory:
        consumer = ConsumidorFaturamento(
            ProcessedEventStore(Path(directory) / "processed-events.sqlite3")
        )
        message = InvalidMessage()

        result = asyncio.run(consumer.consumir_uma(QueueWithInvalidMessage(message)))

        assert result is None
        assert message.rejected_with_requeue is False
