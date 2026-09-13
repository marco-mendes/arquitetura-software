"""Consumidor de faturamento com deduplicação durável por event_id."""

import argparse
import asyncio
import sqlite3
from dataclasses import dataclass
from pathlib import Path

import aio_pika
from pydantic import ValidationError

from hospital.eventos.publicador import (
    EVENT_NAME,
    EXCHANGE_NAME,
    ROUTING_KEY,
    ResultadoLaboratorialDisponibilizadoV1,
    amqp_url,
)


QUEUE_NAME = "billing.resultados.v1"
DLX_NAME = "hospital.events.dlx"
DLQ_NAME = "billing.resultados.v1.dlq"


@dataclass(frozen=True)
class ProcessResult:
    processed: bool
    attempts: int


class ProcessedEventStore:
    """Tabela local para a demonstração; em produção, pertence ao consumidor."""

    def __init__(self, path: Path | str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS processed_events (
                    event_id TEXT PRIMARY KEY,
                    attempts INTEGER NOT NULL,
                    processed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS billing_effects (
                    event_id TEXT PRIMARY KEY,
                    exam_id TEXT NOT NULL,
                    patient_id TEXT NOT NULL,
                    result_reference TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def record(self, event: ResultadoLaboratorialDisponibilizadoV1) -> ProcessResult:
        """Registra toda tentativa e produz o efeito apenas na primeira entrega."""

        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT attempts FROM processed_events WHERE event_id = ?", (event.event_id,)
            ).fetchone()
            if row:
                attempts = int(row[0]) + 1
                connection.execute(
                    "UPDATE processed_events SET attempts = ? WHERE event_id = ?",
                    (attempts, event.event_id),
                )
                return ProcessResult(processed=False, attempts=attempts)
            connection.execute(
                "INSERT INTO processed_events(event_id, attempts) VALUES (?, 1)",
                (event.event_id,),
            )
            connection.execute(
                """INSERT INTO billing_effects(event_id, exam_id, patient_id, result_reference)
                   VALUES (?, ?, ?, ?)""",
                (event.event_id, event.exam_id, event.patient_id, event.result_reference),
            )
            return ProcessResult(processed=True, attempts=1)

    def attempts_for(self, event_id: str) -> int:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT attempts FROM processed_events WHERE event_id = ?", (event_id,)
            ).fetchone()
        return int(row[0]) if row else 0

    def business_effect_count(self) -> int:
        with self._connect() as connection:
            return int(connection.execute("SELECT COUNT(*) FROM billing_effects").fetchone()[0])


class ConsumidorFaturamento:
    def __init__(self, store: ProcessedEventStore):
        self.store = store

    def processar_evento(self, event: ResultadoLaboratorialDisponibilizadoV1) -> ProcessResult:
        return self.store.record(event)

    async def declarar_fila(self, channel: aio_pika.abc.AbstractChannel):
        exchange = await channel.declare_exchange(
            EXCHANGE_NAME, aio_pika.ExchangeType.TOPIC, durable=True
        )
        dlx = await channel.declare_exchange(DLX_NAME, aio_pika.ExchangeType.DIRECT, durable=True)
        queue = await channel.declare_queue(
            QUEUE_NAME,
            durable=True,
            arguments={"x-dead-letter-exchange": DLX_NAME},
        )
        dlq = await channel.declare_queue(DLQ_NAME, durable=True)
        await queue.bind(exchange, routing_key=ROUTING_KEY)
        await dlq.bind(dlx, routing_key=ROUTING_KEY)
        return queue

    async def consumir_uma(self, queue: aio_pika.abc.AbstractQueue) -> ProcessResult | None:
        message = await queue.get(fail=False)
        if message is None:
            return None
        try:
            event = ResultadoLaboratorialDisponibilizadoV1.model_validate_json(message.body)
        except ValidationError as error:
            await message.reject(requeue=False)
            print(f"Mensagem rejeitada para DLQ: schema inválido ({error.error_count()} erro)")
            return None
        async with message.process(requeue=False):
            result = self.processar_evento(event)
            print(
                f"{EVENT_NAME} event_id={event.event_id} "
                f"processed={result.processed} attempts={result.attempts}"
            )
            return result


async def consumir_uma_da_broker(store_path: Path) -> ProcessResult | None:
    connection = await aio_pika.connect_robust(amqp_url())
    try:
        channel = await connection.channel()
        consumer = ConsumidorFaturamento(ProcessedEventStore(store_path))
        queue = await consumer.declarar_fila(channel)
        return await consumer.consumir_uma(queue)
    finally:
        await connection.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Consome um resultado sintético.")
    parser.add_argument("--store", default=".state/processed-events.sqlite3")
    parser.add_argument("--once", action="store_true", help="consome no máximo uma mensagem")
    args = parser.parse_args()
    if not args.once:
        parser.error("use --once nesta oficina para produzir evidência finita")
    asyncio.run(consumir_uma_da_broker(Path(args.store)))


if __name__ == "__main__":
    main()
