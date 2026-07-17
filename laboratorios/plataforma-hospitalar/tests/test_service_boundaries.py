from pathlib import Path

import httpx
import psycopg
from fastapi.testclient import TestClient

from hospital.servicos import exames


ROOT = Path(__file__).resolve().parents[1]
EXAMES_SOURCE = ROOT / "src" / "hospital" / "servicos" / "exames.py"


def _client_for_eligibility(response: httpx.Response) -> TestClient:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/elegibilidades/paciente-001"
        return response

    dependency_client = httpx.Client(
        transport=httpx.MockTransport(handler), base_url="http://contrato.local"
    )
    exames.app.dependency_overrides[exames.obter_cliente_elegibilidade] = (
        lambda: dependency_client
    )
    return TestClient(exames.app)


def teardown_function():
    exames.app.dependency_overrides.clear()


def test_exames_consumes_eligibility_only_through_http_contract(monkeypatch):
    monkeypatch.setattr(exames, "registrar_solicitacao", lambda *_: 41)
    eligibility_response = httpx.Response(
        200,
        json={"beneficiario_id": "paciente-001", "elegivel": True},
    )

    response = _client_for_eligibility(eligibility_response).post(
        "/exames",
        json={"beneficiario_id": "paciente-001", "codigo_exame": "HEM-001"},
    )

    assert response.status_code == 201
    assert response.json() == {
        "solicitacao_id": 41,
        "beneficiario_id": "paciente-001",
        "codigo_exame": "HEM-001",
        "situacao": "solicitado",
    }


def test_exames_makes_partial_failure_observable_when_dependency_is_down():
    def unavailable(_request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("serviço interrompido")

    dependency_client = httpx.Client(
        transport=httpx.MockTransport(unavailable), base_url="http://contrato.local"
    )
    exames.app.dependency_overrides[exames.obter_cliente_elegibilidade] = (
        lambda: dependency_client
    )

    response = TestClient(exames.app).post(
        "/exames",
        json={"beneficiario_id": "paciente-001", "codigo_exame": "HEM-001"},
    )

    assert response.status_code == 503
    assert response.json()["detail"]["codigo"] == "dependencia_indisponivel"


def test_exames_makes_its_own_database_failure_observable(monkeypatch):
    eligibility_response = httpx.Response(
        200,
        json={"beneficiario_id": "paciente-001", "elegivel": True},
    )
    client = _client_for_eligibility(eligibility_response)

    def database_unavailable(*_args):
        raise psycopg.OperationalError("banco de Exames indisponível")

    monkeypatch.setattr(exames, "registrar_solicitacao", database_unavailable)

    response = client.post(
        "/exames",
        json={"beneficiario_id": "paciente-001", "codigo_exame": "HEM-001"},
    )

    assert response.status_code == 503
    assert response.json()["detail"]["codigo"] == "banco_indisponivel"


def test_exames_source_cannot_access_eligibility_table_directly():
    source = EXAMES_SOURCE.read_text(encoding="utf-8").casefold()

    assert "elegibilidade.beneficiarios" not in source
    assert "from elegibilidade" not in source
    assert "join elegibilidade" not in source
    assert "db_elegibilidade" not in source
