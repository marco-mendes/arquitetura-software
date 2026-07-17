"""Telemetria mínima e opt-in para os processos didáticos do hospital."""

import os

from fastapi import FastAPI, Request
from opentelemetry import propagate, trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def instrumentar_app(app: FastAPI, service_name: str) -> None:
    """Emite spans HTTP quando a oficina informa um endpoint OTLP.

    Sem a variável de ambiente, os serviços continuam independentes de um
    coletor; assim os testes locais anteriores não passam a exigir Docker.
    """

    endpoint = os.getenv("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT")
    if not endpoint:
        return

    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

    provider = TracerProvider(resource=Resource.create({SERVICE_NAME: service_name}))
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint)))
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer(service_name)

    @app.middleware("http")
    async def registrar_requisicao(request: Request, call_next):
        contexto = propagate.extract(dict(request.headers))
        correlation_id = request.headers.get("X-Correlation-ID", "")
        with tracer.start_as_current_span(
            f"{request.method} {request.url.path}", context=contexto
        ) as span:
            span.set_attribute("http.request.method", request.method)
            span.set_attribute("url.path", request.url.path)
            if correlation_id:
                span.set_attribute("correlation.id", correlation_id)
            response = await call_next(request)
            span.set_attribute("http.response.status_code", response.status_code)
        if correlation_id:
            response.headers.setdefault("X-Correlation-ID", correlation_id)
        return response
