from datetime import UTC, datetime
import asyncio
import base64
import json
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from urllib.request import Request, urlopen


LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB / "src"))

import aio_pika
import pytest

from hospital.eventos.consumidor import DLQ_NAME, ConsumidorFaturamento, ProcessedEventStore
from hospital.eventos.publicador import (
    ResultadoLaboratorialDisponibilizadoV1,
    amqp_url,
    publicar_json,
)


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


def _dlq_management_details() -> dict[str, object]:
    port = os.getenv("RABBITMQ_MANAGEMENT_PORT", "15673")
    credentials = base64.b64encode(b"guest:guest").decode("ascii")
    request = Request(
        f"http://localhost:{port}/api/queues/%2F/{DLQ_NAME}",
        headers={"Authorization": f"Basic {credentials}"},
    )
    with urlopen(request, timeout=2) as response:
        return json.load(response)


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


@pytest.mark.skipif(
    os.getenv("COMPOSE_LIVE") != "1",
    reason="requer RabbitMQ local iniciado pelo Compose",
)
def test_live_invalid_event_reaches_dead_letter_queue():
    async def exercise_broker() -> None:
        connection = await aio_pika.connect_robust(amqp_url())
        try:
            channel = await connection.channel()
            with TemporaryDirectory() as directory:
                consumer = ConsumidorFaturamento(
                    ProcessedEventStore(Path(directory) / "processed-events.sqlite3")
                )
                queue = await consumer.declarar_fila(channel)
                dlq = await channel.declare_queue(DLQ_NAME, durable=True)
                await queue.purge()
                await dlq.purge()
                event = ResultadoLaboratorialDisponibilizadoV1(
                    event_id="65e95d82-4f8c-4e93-9bb3-3e0e92deaf1d",
                    occurred_at=datetime(2026, 7, 17, 12, 0, tzinfo=UTC),
                    exam_id="exam-sintetico-001",
                    patient_id="patient-sintetico-001",
                    result_reference="resultados/exam-sintetico-001",
                )
                payload = event.model_dump(mode="json")
                payload.pop("result_reference")

                await publicar_json(payload, url=amqp_url())
                assert await consumer.consumir_uma(queue) is None

                for _ in range(50):
                    details = await asyncio.to_thread(_dlq_management_details)
                    if details.get("messages", 0) >= 1:
                        break
                    await asyncio.sleep(0.2)
                else:
                    pytest.fail("a mensagem inválida não chegou à DLQ")
                assert details["messages"] >= 1

                dead_letter = await dlq.get(fail=False)
                assert dead_letter is not None
                assert json.loads(dead_letter.body) == payload
                await dead_letter.ack()
        finally:
            await connection.close()

    asyncio.run(exercise_broker())
