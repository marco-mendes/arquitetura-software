"""Integração real: requer o Compose de governança ativo.

O teste não cria dados em serviços externos nem depende de painel manual. Ele usa a
API HTTP do Jaeger para observar o mesmo trace id que foi enviado ao gateway.
"""

import os
import time
from uuid import uuid4

import httpx
import pytest


GATEWAY_URL = os.getenv("GATEWAY_URL", "http://localhost:18000")
JAEGER_URL = os.getenv("JAEGER_URL", "http://localhost:16686")


def _running_client() -> httpx.Client:
    client = httpx.Client(timeout=3.0)
    try:
        client.get(f"{GATEWAY_URL}/hospital/elegibilidades/paciente-001")
    except httpx.HTTPError:
        client.close()
        pytest.skip("Compose de governança não está ativo; execute o comando da oficina.")
    return client


def _traceparent(trace_id: str) -> str:
    return f"00-{trace_id}-{uuid4().hex[:16]}-01"


def _wait_for_trace(trace_id: str) -> dict:
    deadline = time.monotonic() + 20
    with httpx.Client(timeout=3.0) as client:
        while time.monotonic() < deadline:
            response = client.get(f"{JAEGER_URL}/api/traces/{trace_id}")
            if response.status_code == 200 and response.json().get("data"):
                trace = response.json()["data"][0]
                services = {
                    process.get("serviceName")
                    for process in trace.get("processes", {}).values()
                }
                if {"kong-gateway", "elegibilidade"}.issubset(services):
                    return trace
            time.sleep(1)
    pytest.fail(f"Jaeger não recebeu o trace {trace_id} dentro de 20 segundos.")


def test_gateway_adds_correlation_limits_traffic_and_propagates_trace():
    trace_id = uuid4().hex
    correlation_id = f"aula-{uuid4()}"
    headers = {
        "X-Correlation-ID": correlation_id,
        "traceparent": _traceparent(trace_id),
    }

    client = _running_client()
    try:
        first = client.get(
            f"{GATEWAY_URL}/hospital/elegibilidades/paciente-001", headers=headers
        )
        assert first.status_code == 200
        assert first.headers["X-Correlation-ID"] == correlation_id

        responses = [
            client.get(
                f"{GATEWAY_URL}/hospital/elegibilidades/paciente-001", headers=headers
            )
            for _ in range(4)
        ]
    finally:
        client.close()
    assert any(response.status_code == 429 for response in responses)

    trace = _wait_for_trace(trace_id)
    processes = {
        process.get("serviceName") for process in trace.get("processes", {}).values()
    }
    assert {"kong-gateway", "elegibilidade"}.issubset(processes)
    spans = [span for span in trace.get("spans", []) if span.get("tags")]
    assert any(
        any(tag.get("value") == correlation_id for tag in span["tags"])
        for span in spans
    )
