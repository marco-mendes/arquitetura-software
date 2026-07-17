"""Publica o fato de domínio que disponibiliza um resultado laboratorial."""

import argparse
import asyncio
import json
import os
from datetime import UTC, datetime

import aio_pika
from pydantic import BaseModel, ConfigDict


EVENT_NAME = "ResultadoLaboratorialDisponibilizado.v1"
EXCHANGE_NAME = "hospital.events"
ROUTING_KEY = "laboratory.result.available.v1"


class ResultadoLaboratorialDisponibilizadoV1(BaseModel):
    """Contrato mínimo e versionado do fato publicado pelo laboratório."""

    model_config = ConfigDict(extra="forbid", title=EVENT_NAME)

    event_id: str
    occurred_at: datetime
    exam_id: str
    patient_id: str
    result_reference: str


def amqp_url() -> str:
    return os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:15672/")


async def publicar_resultado(
    event: ResultadoLaboratorialDisponibilizadoV1,
    url: str | None = None,
) -> None:
    """Publica uma cópia persistente do evento na exchange de domínio."""

    await publicar_json(event.model_dump(mode="json"), url=url)


async def publicar_json(payload: dict[str, object], url: str | None = None) -> None:
    """Publica JSON para permitir demonstrar rejeição de esquema no consumidor."""

    connection = await aio_pika.connect_robust(url or amqp_url())
    try:
        channel = await connection.channel(publisher_confirms=True)
        exchange = await channel.declare_exchange(
            EXCHANGE_NAME, aio_pika.ExchangeType.TOPIC, durable=True
        )
        body = json.dumps(payload, default=str, sort_keys=True).encode("utf-8")
        await exchange.publish(
            aio_pika.Message(
                body,
                content_type="application/json",
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                type=EVENT_NAME,
                message_id=str(payload.get("event_id", "invalid-event")),
            ),
            routing_key=ROUTING_KEY,
        )
    finally:
        await connection.close()


def _event_from_arguments(args: argparse.Namespace) -> ResultadoLaboratorialDisponibilizadoV1:
    return ResultadoLaboratorialDisponibilizadoV1(
        event_id=args.event_id,
        occurred_at=datetime.now(UTC),
        exam_id="exam-sintetico-001",
        patient_id="patient-sintetico-001",
        result_reference="resultados/exam-sintetico-001",
    )


async def _main_async(args: argparse.Namespace) -> None:
    event = _event_from_arguments(args)
    if args.invalid:
        payload = event.model_dump(mode="json")
        payload.pop("result_reference")
        await publicar_json(payload)
    else:
        await publicar_resultado(event)
    print(f"Publicado: {EVENT_NAME} event_id={event.event_id}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Publica um resultado sintético.")
    parser.add_argument("--event-id", required=True)
    parser.add_argument(
        "--invalid", action="store_true", help="omite result_reference para a DLQ"
    )
    asyncio.run(_main_async(parser.parse_args()))


if __name__ == "__main__":
    main()
