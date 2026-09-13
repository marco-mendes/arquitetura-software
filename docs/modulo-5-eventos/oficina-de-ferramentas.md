# Oficina de ferramentas: RabbitMQ e consumidor idempotente

Esta oficina responde na prática à pergunta que sustenta o módulo: **se a mesma mensagem pode chegar duas vezes, como garantir que o efeito no negócio aconteça uma só?**

Você vai subir um serviço de mensageria na sua máquina, publicar duas vezes o mesmo evento de resultado de exame, e verificar no banco de dados que houve duas entregas e uma única cobrança. Depois vai publicar uma mensagem deliberadamente inválida e observar para onde ela vai, em vez de sumir em silêncio.

O laboratório usa apenas dados inventados e nada sai da sua máquina. Kafka não é executado aqui: ele aparece ao final como comparação, quando já houver base para discutir o que mudaria.

### O que você vai observar, e por que importa

| O que a oficina mostra | O conceito do livro-texto |
| --- | --- |
| O mesmo evento entregue duas vezes gera uma única cobrança | [Entrega pelo menos uma vez e idempotência](padroes-e-decisoes.md#entrega-pelo-menos-uma-vez-e-idempotencia) |
| Uma mensagem fora do contrato é recusada antes de virar efeito | [Esquema, compatibilidade e evolução](padroes-e-decisoes.md#esquema-compatibilidade-e-evolucao) |
| A mensagem recusada fica visível para inspeção | [Fila de erros como evidência](padroes-e-decisoes.md#dead-letter-queue-como-evidencia-nao-deposito) |
| Quem publica não conhece quem consome | [Broker e mediator](conceitos.md#broker-e-mediator) |

![Entrega duplicada tratada com idempotência e mensagem inválida encaminhada à DLQ](../assets/images/m05-oficina-idempotencia-dlq.png)

*Figura 17 — Duas entregas, uma cobrança, e a mensagem inválida visível na fila de erros. Fonte: curso.*

**Leitura textual da figura:** `publicador.py` publica o evento e origina três caminhos. Nos dois primeiros, a mesma mensagem `ResultadoLaboratorialDisponibilizadoV1` com `event_id: A42` é entregue duas vezes e percorre `hospital.events`, depois `billing.resultados.v1`, até o consumidor. O banco `processed-events.sqlite3` registra duas tentativas e um único efeito, que é a idempotência funcionando. No terceiro caminho, uma mensagem fora do contrato é barrada na validação, nunca entra em `hospital.events` e segue para `hospital.events.dlx` e `billing.resultados.v1.dlq`, onde fica disponível para inspeção.

## Mapa da demonstração local

Esta oficina implementa em código o que as páginas de [Conceitos](conceitos.md) e [Padrões e decisões](padroes-e-decisoes.md) descrevem no livro-texto. Você vai começar numa pasta vazia e escrever os sete arquivos abaixo. Cada um aparece nesta página inteiro, pronto para copiar, e o título de cada bloco é um link para o mesmo arquivo no repositório do curso, byte a byte igual ao que está aqui.

Duas siglas aparecem várias vezes a partir daqui. Uma **dead-letter exchange** (DLX) é a exchange para a qual o RabbitMQ redireciona uma mensagem rejeitada. Uma **dead-letter queue** (DLQ) é a fila ligada a essa DLX, onde a mensagem rejeitada fica disponível para inspeção em vez de reentregue em loop ou descartada.

| Arquivo | O que ele faz | Onde isso aparece na teoria |
| --- | --- | --- |
| [`infra/compose.eventos.yml`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-5/infra/compose.eventos.yml) | Sobe um RabbitMQ 4 isolado, com plugin de management e healthcheck, e declara as portas AMQP e HTTP que os comandos desta oficina vão usar. | A infraestrutura por trás do [broker](conceitos.md#broker-e-mediator): aqui ele é uma exchange `hospital.events` e uma fila de trabalho `billing.resultados.v1`. |
| [`src/hospital/eventos/publicador.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-5/src/hospital/eventos/publicador.py) | Define o contrato `ResultadoLaboratorialDisponibilizadoV1` (modelo Pydantic) e publica na exchange `hospital.events`, com confirmação de publicação ligada. | O que [evento, comando e mensagem](conceitos.md#evento-comando-e-mensagem) chama de publicador: ele afirma um fato e não conhece quem vai reagir a ele. |
| [`src/hospital/eventos/consumidor.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-5/src/hospital/eventos/consumidor.py) | Declara a fila `billing.resultados.v1`, valida o schema recebido, grava tentativa e efeito no SQLite `processed-events.sqlite3` por `event_id`, e liga a fila de rejeitados `billing.resultados.v1.dlq` à DLX `hospital.events.dlx`. | A implementação de [entrega pelo menos uma vez e idempotência](padroes-e-decisoes.md#entrega-pelo-menos-uma-vez-e-idempotencia) e de [dead-letter queue](padroes-e-decisoes.md#dead-letter-queue-como-evidencia-nao-deposito). |
| [`tests/test_event_idempotency.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-5/tests/test_event_idempotency.py) | Teste automatizado que publica o mesmo evento duas vezes e verifica, por código, que existe só um efeito de negócio e duas tentativas registradas. | A prova de que a garantia de repetição sem duplicidade de efeito, descrita na teoria, se sustenta neste código específico. |
| [`pyproject.toml`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-5/pyproject.toml) | Declara as dependências do pacote (`aio-pika` para AMQP assíncrono, `pydantic` para o contrato, `pytest` para o teste) e o torna instalável. | Por que o comando de instalação, mais adiante, não pede nenhum argumento além do caminho do pacote. |

### O caminho de uma entrega duplicada

```mermaid
flowchart TB
    PUB[publicador.py<br/>publica o fato] --> EX[exchange hospital.events]
    EX --> Q[fila billing.resultados.v1]
    Q --> CON{consumidor.py<br/>schema válido?}
    CON -->|não| DLX[DLX hospital.events.dlx<br/>leva à DLQ, disponível para inspeção]
    CON -->|sim| ID{event_id já processado?}
    ID -->|não| EF[grava tentativa e efeito<br/>processed=True attempts=1]
    ID -->|sim| SE[grava só a tentativa<br/>processed=False attempts=2]
```

**Texto alternativo:** o publicador envia à exchange, que entrega à fila, e o consumidor decide em dois passos: primeiro se o schema é válido, encaminhando o inválido à fila de erros, e depois se o identificador do evento já foi processado, gravando efeito apenas na primeira vez.

*Figura 18 — As duas decisões do consumidor, na ordem em que ele as toma. Fonte: curso.*

**Leitura textual:** o publicador afirma um fato e o entrega à exchange, que o roteia para a fila de trabalho. O consumidor então decide duas coisas, em ordem. A primeira é se a mensagem cumpre o schema. Quando não cumpre, ela segue para a dead-letter exchange e daí para a fila de erros, onde fica disponível para inspeção em vez de desaparecer ou voltar em laço. Quando cumpre, vem a segunda decisão: se aquele identificador de evento já foi processado antes. Na primeira vez, o consumidor grava a tentativa e o efeito de negócio, e imprime processado com uma tentativa. Na repetição, ele grava apenas a tentativa, e imprime não processado com duas tentativas. A ordem importa: validar antes de consultar o registro de idempotência evita gravar identificador de mensagem que nunca deveria ter entrado.

### Os sete arquivos, um a um

Crie a estrutura antes de escrever. No macOS e no Linux:

```bash
mkdir -p oficina-eventos/infra oficina-eventos/src/hospital/eventos oficina-eventos/tests
cd oficina-eventos
```

No PowerShell:

```powershell
mkdir oficina-eventos\infra, oficina-eventos\src\hospital\eventos, oficina-eventos\tests
cd oficina-eventos
```

[`pyproject.toml`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-5/pyproject.toml)

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "eventos-hospitalares"
version = "0.1.0"
description = "Publicador, consumidor idempotente e DLQ, oficina do módulo 5"
requires-python = ">=3.11"
dependencies = [
  "aio-pika",
  "pydantic",
]

[project.optional-dependencies]
dev = [
  "pytest",
  "pytest-asyncio",
  "httpx",
]

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

Os dois `__init__.py` ficam vazios e existem para tornar as pastas pacotes Python importáveis.

[`src/hospital/__init__.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-5/src/hospital/__init__.py)

```python

```

[`src/hospital/eventos/__init__.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-5/src/hospital/eventos/__init__.py)

```python

```

O `publicador.py` define o contrato do evento e o publica. Ele não conhece nenhum consumidor.

[`src/hospital/eventos/publicador.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-5/src/hospital/eventos/publicador.py)

```python
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
```

O `consumidor.py` é o arquivo central da oficina, e é nele que as duas decisões da Figura 18 estão escritas.

[`src/hospital/eventos/consumidor.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-5/src/hospital/eventos/consumidor.py)

```python
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
```

O `infra/compose.eventos.yml` sobe um RabbitMQ isolado, com o plugin de administração e verificação de saúde.

[`infra/compose.eventos.yml`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-5/infra/compose.eventos.yml)

```yaml
services:
  rabbitmq:
    image: rabbitmq:4-management
    environment:
      RABBITMQ_DEFAULT_USER: guest
      RABBITMQ_DEFAULT_PASS: guest
    ports:
      - "${RABBITMQ_PORT:-15672}:5672"
      - "${RABBITMQ_MANAGEMENT_PORT:-15673}:15672"
    volumes:
      - rabbitmq_eventos_data:/var/lib/rabbitmq
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "-q", "ping"]
      interval: 2s
      timeout: 3s
      retries: 20

volumes:
  rabbitmq_eventos_data:
```

O `tests/test_event_idempotency.py` prova por código o que os comandos mostram na tela.

[`tests/test_event_idempotency.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-5/tests/test_event_idempotency.py)

```python
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
```

**Estado inicial**

RabbitMQ está parado, não há mensagens nas filas e o arquivo SQLite ainda não contém `event_id` processado. A variável de cada experimento muda uma condição observável; o evento publicado, a evidência e o erro esperado são declarados antes dos comandos.

## Ferramenta

| Ferramenta | Papel local | Evidência observável |
| --- | --- | --- |
| Docker Engine e Compose v2 | executar RabbitMQ isolado | healthcheck e configuração válida |
| RabbitMQ 4 com management plugin | exchange, fila, confirmações e DLQ | filas no endpoint local |
| Python 3.11 ou superior | publicar e consumir modelo Pydantic | saída de tentativas |
| `aio-pika` e SQLite | AMQP assíncrono e store durável local | uma linha de efeito |

AMQP usa `RABBITMQ_PORT` e management usa `RABBITMQ_MANAGEMENT_PORT`; os padrões são 15672 e 15673. A conta e o volume pertencem apenas a este ambiente descartável.

## Pré-requisitos

**Objetivo**

Confirmar que Docker, Compose e Python estão disponíveis e que a execução ocorrerá com dados sintéticos.

**Pré-requisito**

Tenha Docker iniciado e a pasta `oficina-eventos` já criada com os sete arquivos. Execute a partir dela. o pacote já declara `aio-pika`, Pydantic e a dependência de desenvolvimento.

**Execute**

Verifique versões, instale o pacote local e crie uma pasta descartável para a evidência.

**Observe**

`docker version` precisa mostrar Client e Server; `docker compose version` e a versão Python confirmam o caminho escolhido.

**Compare**

Configuração válida não é a mesma evidência que broker pronto. A primeira lê YAML; a segunda depende do healthcheck.

**Questões exploratórias**

- Que dado seria excessivo no payload de um resultado?
- Qual é a diferença entre `exam_id` e `event_id` na repetição?

## Instalação

### Windows

Instale Docker Desktop pelas [instruções oficiais](https://docs.docker.com/desktop/setup/install/windows-install/) e Python pelas [instruções oficiais](https://docs.python.org/3/using/windows.html). Em PowerShell:

```powershell
docker version
docker compose version
py --version
cd oficina-eventos
py -m pip install -e ".[dev]"
New-Item -ItemType Directory -Force evidencias\modulo-5
```

**Resultado esperado**

As versões são exibidas e o pacote pode ser importado pelo Python usado no terminal.

**Contingência**

Se o Docker não responder, abra Docker Desktop e aguarde o mecanismo. Se a instalação Python afetar outro projeto, crie um ambiente virtual local e repita os comandos dentro dele.

### macOS

Instale Docker Desktop pelas [instruções oficiais](https://docs.docker.com/desktop/setup/install/mac-install/) e use Python do sistema, Homebrew ou instalador oficial.

```bash
docker version
docker compose version
python3 --version
cd oficina-eventos
python3 -m pip install -e ".[dev]"
mkdir -p evidencias/modulo-5
```

**Resultado esperado**

O daemon Docker responde e o ambiente contém as bibliotecas do laboratório.

**Contingência**

Se `pip` não puder alterar o ambiente global, use `python3 -m venv .venv`, ative com `source .venv/bin/activate` e execute a instalação novamente.

### Linux

Instale Docker Engine e o plugin Compose pelas [instruções oficiais](https://docs.docker.com/engine/install/) e Python pelo mecanismo da distribuição.

```bash
docker version
docker compose version
python3 --version
cd oficina-eventos
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
mkdir -p evidencias/modulo-5
```

**Resultado esperado**

Docker responde e o ambiente virtual contém o pacote local.

**Contingência**

Se o socket do Docker recusar conexão, siga a orientação pós-instalação da distribuição. Não remova contêineres ou volumes alheios para liberar uma porta.

## Preparação do laboratório

**Objetivo**

Escolher portas, validar o Compose e iniciar um broker isolado.

**Pré-requisito**

Permaneça em `oficina-eventos`. Escolha portas livres; se as sugestões estiverem ocupadas, altere apenas os valores do terminal.

**Execute**

No macOS ou Linux:

```bash
export RABBITMQ_PORT=15672
export RABBITMQ_MANAGEMENT_PORT=15673
export RABBITMQ_URL="amqp://guest:guest@localhost:${RABBITMQ_PORT}/"
docker compose -f infra/compose.eventos.yml config --quiet
docker compose -f infra/compose.eventos.yml up -d --build --wait
docker compose -f infra/compose.eventos.yml ps
```

No PowerShell:

```powershell
$env:RABBITMQ_PORT = 15672
$env:RABBITMQ_MANAGEMENT_PORT = 15673
$env:RABBITMQ_URL = "amqp://guest:guest@localhost:$env:RABBITMQ_PORT/"
docker compose -f infra/compose.eventos.yml config --quiet
docker compose -f infra/compose.eventos.yml up -d --build --wait
docker compose -f infra/compose.eventos.yml ps
```

**Observe**

`config --quiet` termina sem texto de erro. O serviço `rabbitmq` fica saudável antes de `--wait` retornar. A saída de `ps` é a primeira evidência de runtime; ela ainda não demonstra routing nem idempotência.

**Compare**

Compare a porta AMQP 15672 com a porta web 15673. A primeira é usada por `aio-pika`; a segunda existe apenas para inspeção local do management plugin.

**Questões exploratórias**

- Por que alterar variável de porta é mais seguro que editar um arquivo compartilhado?
- O que o healthcheck confirma e o que ele não confirma?

**Objetivo**

Ler a topologia antes de enviar mensagens.

**Pré-requisito**

Abra `src/hospital/eventos/publicador.py`, `src/hospital/eventos/consumidor.py` e `infra/compose.eventos.yml`.

**Execute**

Localize no publicador a publicação, a exchange e a chave de roteamento. Depois, no consumidor, localize a fila, a DLX, a DLQ e o instante exato em que a confirmação é enviada ao broker.

**Observe**

`hospital.events` é a exchange topic; `billing.resultados.v1` é a fila de trabalho; `hospital.events.dlx` encaminha rejeições a `billing.resultados.v1.dlq`.

**Compare**

Compare o que a infraestrutura roteia com o que `ProcessedEventStore` decide. O broker não sabe se já houve lançamento administrativo; o consumidor não decide se uma mensagem inválida deve parecer sucesso. É a fronteira descrita em [broker e mediator](conceitos.md#broker-e-mediator): o RabbitMQ só encaminha, quem decide idempotência e rejeição é o código do consumidor.

**Questões exploratórias**

- Qual mudança exigiria uma nova versão do evento?
- Por que o store pertence ao consumidor, não à exchange?

**Objetivo**

Planejar uma futura avaliação de Kafka sem mudar a oficina principal.

**Pré-requisito**

Considere a necessidade de reprocessar eventos de resultados por vários grupos independentes por um período definido.

**Execute**

Escreva uma hipótese de tópico, chave de partição por `exam_id`, prazo de retenção, grupos de consumidores e regra de proteção de referências. Não suba Kafka nesta etapa.

**Observe**

Replay depende de retenção e offsets; ele não remove a necessidade de `event_id`, idempotência ou versão de contrato.

**Compare**

Compare uma fila de Faturamento, que distribui trabalho pendente, com um log Kafka, que permite posições independentes de leitura.

**Questões exploratórias**

- Que requisito mensurável justificaria a extensão?
- Qual efeito externo ainda exigiria chave de idempotência?

## Execução

**Objetivo**

Declarar a fila, publicar o mesmo fato duas vezes e registrar um único lançamento administrativo sintético.

**Pré-requisito**

O broker está saudável e `RABBITMQ_URL` aponta para o terminal atual. Use um UUID sintético fixo nesta sequência para que as duas mensagens tenham o mesmo `event_id`.

**Variável alterada**

O número de publicação do mesmo `event_id`: primeira entrega e redelivery sintético.

**Evento publicado**

`ResultadoLaboratorialDisponibilizado.v1` válido, duas vezes com o mesmo `event_id`.

**Evidência de processamento**

Saídas `processed=True attempts=1` e `processed=False attempts=2`, com uma linha em `billing_effects`.

**Erro esperado**

Nenhum erro de contrato; duplicar o efeito seria a falha a investigar.

**Execute**

Primeiro execute o consumidor uma vez para declarar a fila; como ela está vazia, ele não produz efeito. Depois publique e consuma, repita a publicação com o mesmo ID e consuma de novo. No macOS ou Linux:

```bash
python -m hospital.eventos.consumidor --once --store evidencias/modulo-5/processed-events.sqlite3
python -m hospital.eventos.publicador --event-id 3fa85f64-5717-4562-b3fc-2c963f66afa6
python -m hospital.eventos.consumidor --once --store evidencias/modulo-5/processed-events.sqlite3
python -m hospital.eventos.publicador --event-id 3fa85f64-5717-4562-b3fc-2c963f66afa6
python -m hospital.eventos.consumidor --once --store evidencias/modulo-5/processed-events.sqlite3
python -m pytest tests/test_event_idempotency.py -q
```

No PowerShell:

```powershell
py -m hospital.eventos.consumidor --once --store evidencias/modulo-5/processed-events.sqlite3
py -m hospital.eventos.publicador --event-id 3fa85f64-5717-4562-b3fc-2c963f66afa6
py -m hospital.eventos.consumidor --once --store evidencias/modulo-5/processed-events.sqlite3
py -m hospital.eventos.publicador --event-id 3fa85f64-5717-4562-b3fc-2c963f66afa6
py -m hospital.eventos.consumidor --once --store evidencias/modulo-5/processed-events.sqlite3
py -m pytest tests/test_event_idempotency.py -q
```

**Observe**

A primeira entrega válida imprime `processed=True attempts=1`. A segunda imprime `processed=False attempts=2`. O teste `test_event_idempotency.py` confirma uma linha de efeito e duas tentativas em banco temporário; a sequência manual preserva a mesma observação no arquivo de evidência. É a demonstração ao vivo de [entrega pelo menos uma vez e idempotência](padroes-e-decisoes.md#entrega-pelo-menos-uma-vez-e-idempotencia): a mensagem chega duas vezes, o efeito de negócio acontece uma.

**Compare**

Compare “duas mensagens recebidas” com “duas cobranças”. O primeiro é comportamento permitido pela entrega pelo menos uma vez; o segundo seria falha de idempotência.

**Questões exploratórias**

- Em qual etapa uma queda poderia gerar redelivery?
- Por que confirmar antes do SQLite seria inseguro?

**Objetivo**

Inspecionar o estado persistido sem revelar dados clínicos.

**Pré-requisito**

A sequência essencial já criou `evidencias/modulo-5/processed-events.sqlite3` com valores sintéticos.

**Variável alterada**

A consulta: tentativas por `event_id` e contagem de efeitos.

**Evento publicado**

Nenhum novo evento; a evidência vem das duas entregas válidas anteriores.

**Evidência de processamento**

Uma identidade com duas tentativas e apenas um efeito persistido.

**Erro esperado**

Arquivo inexistente indica que a sequência essencial não foi concluída.

**Execute**

Consulte apenas contagens e a identidade sintética da ocorrência. No macOS ou Linux:

```bash
python -c "import sqlite3; c=sqlite3.connect('evidencias/modulo-5/processed-events.sqlite3'); print(c.execute('select event_id, attempts from processed_events').fetchall()); print(c.execute('select count(*) from billing_effects').fetchone())"
```

No PowerShell:

```powershell
py -c "import sqlite3; c=sqlite3.connect('evidencias/modulo-5/processed-events.sqlite3'); print(c.execute('select event_id, attempts from processed_events').fetchall()); print(c.execute('select count(*) from billing_effects').fetchone())"
```

**Observe**

Há uma ocorrência com duas tentativas e a contagem de `billing_effects` é um. Registre a saída em um arquivo local de evidência se a turma precisar comparar resultados.

**Compare**

Compare a tabela de tentativas com a de efeitos: a primeira mede entrega vista; a segunda representa a consequência de negócio idempotente.

**Questões exploratórias**

- Como a tabela mudaria se o `event_id` fosse novo?
- Que restrição única seria necessária em um banco compartilhado?

**Objetivo**

Observar uma mensagem inválida na dead-letter queue.

**Pré-requisito**

A fila já foi declarada pelo consumidor. Mantenha o mesmo ambiente local e não use payloads reais.

**Variável alterada**

O payload omite `result_reference`.

**Evento publicado**

`ResultadoLaboratorialDisponibilizado.v1` inválido, com UUID sintético próprio.

**Evidência de processamento**

O endpoint management mostra mensagem em `billing.resultados.v1.dlq`.

**Erro esperado**

Validação Pydantic falha, não há ack de sucesso e a mensagem segue à DLQ.

**Execute**

Publique deliberadamente uma mensagem sem `result_reference`, consuma uma vez e consulte a contagem da DLQ no management endpoint local. No macOS ou Linux:

```bash
python -m hospital.eventos.publicador --event-id 65e95d82-4f8c-4e93-9bb3-3e0e92deaf1d --invalid
python -m hospital.eventos.consumidor --once --store evidencias/modulo-5/processed-events.sqlite3
curl -u guest:guest "http://localhost:${RABBITMQ_MANAGEMENT_PORT}/api/queues/%2F/billing.resultados.v1.dlq"
```

No PowerShell, publique e consuma primeiro:

```powershell
py -m hospital.eventos.publicador --event-id 65e95d82-4f8c-4e93-9bb3-3e0e92deaf1d --invalid
py -m hospital.eventos.consumidor --once --store evidencias/modulo-5/processed-events.sqlite3
```

Essa rejeição é a aplicação prática de [dead-letter queue como evidência](padroes-e-decisoes.md#dead-letter-queue-como-evidencia-nao-deposito): o schema barra a mensagem antes de qualquer regra de negócio rodar, e ela fica visível para inspeção em vez de desaparecer. A consulta HTTP que confirma essa evidência já usa portas e sintaxe específicas do PowerShell, por isso tem uma seção própria a seguir.

**Verificação no PowerShell**

Use `curl.exe`: `curl` pode ser um alias. `%2F` codifica o vhost padrão.

```powershell
if (-not $env:RABBITMQ_MANAGEMENT_PORT) {
  $env:RABBITMQ_MANAGEMENT_PORT = 15673
}
$dlqUrl = "http://localhost:$env:RABBITMQ_MANAGEMENT_PORT/api/queues/%2F/billing.resultados.v1.dlq"
$response = curl.exe --fail --silent --user guest:guest $dlqUrl | ConvertFrom-Json
if ($response.messages -lt 1) {
  throw "A DLQ ainda não contém a mensagem; aguarde um instante e execute a consulta novamente."
}
$response.messages

# Ao terminar este terminal, remova os overrides para voltar aos padrões do Compose.
Remove-Item Env:RABBITMQ_PORT -ErrorAction SilentlyContinue
Remove-Item Env:RABBITMQ_MANAGEMENT_PORT -ErrorAction SilentlyContinue
Remove-Item Env:RABBITMQ_URL -ErrorAction SilentlyContinue
```

**Resultado esperado no PowerShell**

O valor é `1` ou maior e o JSON contém `messages`. Os padrões são AMQP 15672 e management 15673; se ocupados, defina portas livres antes da subida. Os `Remove-Item` removem apenas overrides do terminal.

**Evidência automatizada**

Com Compose ativo, o teste opt-in percorre publicação, validação, rejeição, DLX e DLQ:

```bash
COMPOSE_LIVE=1 RABBITMQ_URL="amqp://guest:guest@localhost:${RABBITMQ_PORT}" RABBITMQ_MANAGEMENT_PORT="${RABBITMQ_MANAGEMENT_PORT}" python -m pytest tests/test_event_idempotency.py -q
```

`3 passed` confirma a mensagem inválida na `billing.resultados.v1.dlq`.

**Observe**

O consumidor rejeita a mensagem ao validar Pydantic; ele não imprime sucesso de processamento. A resposta JSON do endpoint mostra `messages` maior que zero na fila `billing.resultados.v1.dlq`.

**Compare**

Compare uma mensagem inválida em DLQ com uma mensagem temporariamente indisponível. A primeira pede correção de contrato ou decisão de recuperação; a segunda pode pedir retry com atraso e limite.

**Questões exploratórias**

- Por que republicar o corpo inválido sem correção produz um ciclo?
- Qual sinal operacional avisaria que uma DLQ deixou de ser excepcional?

## Resultado esperado

O ambiente termina com RabbitMQ saudável, `hospital.events`, `billing.resultados.v1`, DLQ e SQLite com duas tentativas e um efeito. A mensagem inválida segue para dead-letter. A extensão conceitual trata retenção, offsets, particionamento e transações Kafka.

## Interpretação

O experimento demonstra entrega pelo menos uma vez, não exactly-once. SQLite evita duplicação entre execuções; em sistemas distribuídos, trate-a com banco e efeitos externos. O Compose não é produção: não inclui cluster, TLS, credenciais, backup ou retenção. Use evidência para discutir semântica.

## Limpeza e contingência

**Objetivo**

Remover os recursos locais criados pela oficina sem afetar outros projetos.

**Pré-requisito**

A evidência desejada foi copiada para local apropriado e o terminal ainda está em `oficina-eventos`.

**Execute**

No macOS ou Linux:

```bash
docker compose -f infra/compose.eventos.yml down -v
rm -rf evidencias/modulo-5
```

No PowerShell:

```powershell
docker compose -f infra/compose.eventos.yml down -v
Remove-Item -Recurse -Force evidencias\modulo-5
```

**Observe**

`down -v` remove apenas serviços e volume nomeados por este arquivo Compose. Uma nova subida inicia sem filas e sem SQLite anterior.

**Compare**

Compare esta limpeza limitada com comandos globais do Docker: somente a primeira preserva recursos de outros estudos.

**Questões exploratórias**

- O que seria perdido se a DLQ fosse removida antes de ser analisada?
- Qual evidência deve ser guardada sem registrar dado sensível?

## Evidência a entregar

Entregue uma nota com: configuração validada; saídas `processed=True attempts=1` e `processed=False attempts=2`; consulta de um efeito; mensagem na DLQ; e a explicação de por que há entrega pelo menos uma vez com idempotência, não exactly-once. Use IDs sintéticos. Indique em que cenário Kafka valeria como extensão do desenho atual, sem substituí-lo automaticamente.
