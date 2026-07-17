from datetime import datetime
from pathlib import Path

from fastapi.testclient import TestClient
import yaml

from hospital.api.main import app, limpar_elegibilidades
from hospital.api.models import ElegibilidadeAceita, ErroAPI, PedidoElegibilidade


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contratos" / "openapi.yaml"


def setup_function():
    limpar_elegibilidades()


def test_post_accepts_request_and_get_recovers_it():
    client = TestClient(app)
    request = {
        "cpf": "12345678901",
        "codigo_operadora": "OPS-001",
        "matricula_plano": "MAT-2026-001",
    }

    created = client.post("/elegibilidades", json=request)

    assert created.status_code == 202
    body = created.json()
    assert body["situacao"] == "recebida"
    assert body["protocolo"]
    datetime.fromisoformat(body["criado_em"].replace("Z", "+00:00"))
    assert created.headers["location"] == f"/elegibilidades/{body['protocolo']}"

    recovered = client.get(created.headers["location"])

    assert recovered.status_code == 200
    assert recovered.json() == body


def test_missing_cpf_returns_structured_422_error():
    client = TestClient(app)

    response = client.post(
        "/elegibilidades",
        json={
            "codigo_operadora": "OPS-001",
            "matricula_plano": "MAT-2026-001",
        },
    )

    assert response.status_code == 422
    body = response.json()
    assert body["codigo"] == "dados_invalidos"
    assert body["mensagem"]
    assert any(detail["campo"] == "body.cpf" for detail in body["detalhes"])


def test_request_rejects_property_forbidden_by_explicit_contract():
    client = TestClient(app)

    response = client.post(
        "/elegibilidades",
        json={
            "cpf": "12345678901",
            "codigo_operadora": "OPS-001",
            "matricula_plano": "MAT-2026-001",
            "campo_nao_contratado": "valor",
        },
    )

    assert response.status_code == 422
    assert any(
        detail["campo"] == "body.campo_nao_contratado"
        for detail in response.json()["detalhes"]
    )


def test_unknown_protocol_returns_structured_404_error():
    client = TestClient(app)

    response = client.get("/elegibilidades/protocolo-inexistente")

    assert response.status_code == 404
    assert response.json() == {
        "codigo": "elegibilidade_nao_encontrada",
        "mensagem": "Protocolo de elegibilidade não encontrado.",
        "detalhes": [],
    }


def test_explicit_openapi_contract_defines_paths_schemas_and_valid_examples():
    contract = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))

    assert contract["openapi"] == "3.1.0"
    assert set(contract["paths"]) == {
        "/elegibilidades",
        "/elegibilidades/{protocolo}",
    }
    schemas = contract["components"]["schemas"]
    for name in ("PedidoElegibilidade", "ElegibilidadeAceita", "ErroAPI"):
        assert name in schemas

    request_schema = schemas["PedidoElegibilidade"]
    assert set(request_schema["required"]) == {
        "cpf",
        "codigo_operadora",
        "matricula_plano",
    }
    example = request_schema["examples"][0]
    response = TestClient(app).post("/elegibilidades", json=example)
    assert response.status_code == 202

    PedidoElegibilidade.model_validate(example)
    for path, status_code, model in (
        ("/elegibilidades", "202", ElegibilidadeAceita),
        ("/elegibilidades", "422", ErroAPI),
        ("/elegibilidades/{protocolo}", "200", ElegibilidadeAceita),
        ("/elegibilidades/{protocolo}", "404", ErroAPI),
    ):
        examples = contract["paths"][path]["post" if path == "/elegibilidades" else "get"][
            "responses"
        ][status_code]["content"]["application/json"]["examples"]
        for item in examples.values():
            model.model_validate(item["value"])


def test_application_and_explicit_contract_agree_on_operations_and_models():
    explicit = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
    generated = app.openapi()

    for path, method in (
        ("/elegibilidades", "post"),
        ("/elegibilidades/{protocolo}", "get"),
    ):
        assert method in explicit["paths"][path]
        assert method in generated["paths"][path]

    explicit_required = set(
        explicit["components"]["schemas"]["PedidoElegibilidade"]["required"]
    )
    generated_required = set(
        generated["components"]["schemas"]["PedidoElegibilidade"]["required"]
    )
    assert generated_required == explicit_required
