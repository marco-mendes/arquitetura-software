"""Testes de contrato da API de elegibilidades.

Este arquivo responde a uma pergunta: **a aplicação faz o que o contrato promete?**

Há dois contratos em jogo, e a diferença entre eles é o assunto do módulo:

- o **contrato explícito**, escrito à mão em `contratos/openapi.yaml`, é a promessa
  publicada para quem consome a API;
- o **contrato gerado**, que o FastAPI monta sozinho a partir do código e serve em
  `/openapi.json`, descreve o que a aplicação realmente faz hoje.

Os cinco primeiros testes exercitam a aplicação pela porta da frente. Os dois
últimos comparam os dois contratos entre si, que é onde uma divergência costuma
aparecer sem ninguém notar.

Para rodar apenas este arquivo:

    python -m pytest tests/test_api_contract.py -q
"""

from datetime import datetime
from pathlib import Path

from fastapi.testclient import TestClient
import yaml

from hospital.api.main import app, limpar_elegibilidades
from hospital.api.models import ElegibilidadeAceita, ErroAPI, PedidoElegibilidade


# Caminho do contrato escrito à mão, relativo à raiz do laboratório.
ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contratos" / "openapi.yaml"

# Corpo válido reaproveitado por vários testes. CPF e matrícula são sintéticos.
PEDIDO_VALIDO = {
    "cpf": "12345678901",
    "codigo_operadora": "OPS-001",
    "matricula_plano": "MAT-2026-001",
}


def setup_function():
    """Roda antes de cada teste.

    A aplicação guarda os pedidos em memória, então um teste enxergaria os
    protocolos criados pelo anterior. Limpar aqui deixa cada teste independente
    da ordem de execução.
    """
    limpar_elegibilidades()


def carregar_contrato_explicito() -> dict:
    """Lê `contratos/openapi.yaml` como dicionário Python."""
    return yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))


def exemplos_da_resposta(contrato: dict, caminho: str, metodo: str, status: str) -> list:
    """Devolve os exemplos JSON declarados para uma resposta do contrato.

    Existe para evitar a indexação encadeada longa que essa navegação exigiria
    dentro do teste. A estrutura percorrida é a do OpenAPI:
    paths → caminho → método → responses → status → content → mídia → examples.
    """
    resposta = contrato["paths"][caminho][metodo]["responses"][status]
    exemplos = resposta["content"]["application/json"]["examples"]
    return [item["value"] for item in exemplos.values()]


def test_post_aceita_pedido_e_get_recupera_pelo_location():
    """O caminho feliz: `POST` aceita e `GET` recupera pelo endereço devolvido.

    O `202 Accepted` significa "recebi e ainda vou processar", e não "pronto".
    Por isso a resposta traz um `protocolo` e o cabeçalho `Location` com o
    endereço onde consultar o andamento — o consumidor não precisa montar essa
    URL por conta própria.
    """
    client = TestClient(app)

    criado = client.post("/elegibilidades", json=PEDIDO_VALIDO)

    assert criado.status_code == 202
    corpo = criado.json()
    assert corpo["situacao"] == "recebida"
    assert corpo["protocolo"]

    # Não compara a data com um valor fixo: só exige que seja ISO 8601 válida.
    datetime.fromisoformat(corpo["criado_em"].replace("Z", "+00:00"))

    assert criado.headers["location"] == f"/elegibilidades/{corpo['protocolo']}"

    # Seguir o Location é exatamente o que um consumidor bem-comportado faz.
    recuperado = client.get(criado.headers["location"])

    assert recuperado.status_code == 200
    assert recuperado.json() == corpo


def test_pedido_sem_cpf_recebe_erro_422_estruturado():
    """Campo obrigatório ausente vira `422` com corpo previsível.

    O erro faz parte do contrato: quem consome precisa conseguir tratar a falha
    programaticamente, e para isso o corpo traz `codigo`, `mensagem` e a lista
    `detalhes` apontando o campo problemático.
    """
    client = TestClient(app)
    pedido_incompleto = {
        "codigo_operadora": "OPS-001",
        "matricula_plano": "MAT-2026-001",
    }

    resposta = client.post("/elegibilidades", json=pedido_incompleto)

    assert resposta.status_code == 422
    corpo = resposta.json()
    assert corpo["codigo"] == "dados_invalidos"
    assert corpo["mensagem"]
    assert any(detalhe["campo"] == "body.cpf" for detalhe in corpo["detalhes"])


def test_pedido_com_campo_fora_do_contrato_e_recusado():
    """Campo a mais também é violação de contrato, não cortesia.

    Aceitar um campo desconhecido em silêncio faz o consumidor acreditar que ele
    foi processado. O modelo recusa, e o campo extra aparece em `detalhes`.
    """
    client = TestClient(app)
    pedido_com_extra = PEDIDO_VALIDO | {"campo_nao_contratado": "valor"}

    resposta = client.post("/elegibilidades", json=pedido_com_extra)

    assert resposta.status_code == 422
    detalhes = resposta.json()["detalhes"]
    assert any(detalhe["campo"] == "body.campo_nao_contratado" for detalhe in detalhes)


def test_protocolo_inexistente_recebe_erro_404_estruturado():
    """Consultar protocolo que não existe devolve `404` no mesmo formato de erro.

    O corpo segue o mesmo esquema `ErroAPI` do `422`: um formato de erro por API,
    não um por operação.
    """
    client = TestClient(app)

    resposta = client.get("/elegibilidades/protocolo-inexistente")

    assert resposta.status_code == 404
    assert resposta.json() == {
        "codigo": "elegibilidade_nao_encontrada",
        "mensagem": "Protocolo de elegibilidade não encontrado.",
        "detalhes": [],
    }


def test_health_separa_processo_vivo_de_pronto_para_receber_trafego():
    """`/health/live` e `/health/ready` respondem perguntas diferentes.

    Vivo significa que o processo não travou. Pronto significa que ele pode
    receber tráfego. Um orquestrador reinicia com base no primeiro e tira do
    balanceamento com base no segundo.
    """
    client = TestClient(app)

    assert client.get("/health/live").json() == {"status": "live"}
    assert client.get("/health/ready").json() == {"status": "ready"}


def test_contrato_explicito_declara_operacoes_schemas_e_exemplos_validos():
    """O `openapi.yaml` está bem formado e seus exemplos são de verdade.

    Um exemplo desatualizado no contrato é pior que exemplo nenhum, porque quem
    consome copia e não funciona. Aqui cada exemplo declarado é validado contra o
    modelo correspondente, e o exemplo de requisição é enviado à aplicação real.
    """
    contrato = carregar_contrato_explicito()

    assert contrato["openapi"] == "3.1.0"
    assert set(contrato["paths"]) == {
        "/elegibilidades",
        "/elegibilidades/{protocolo}",
    }

    schemas = contrato["components"]["schemas"]
    for nome in ("PedidoElegibilidade", "ElegibilidadeAceita", "ErroAPI"):
        assert nome in schemas

    schema_pedido = schemas["PedidoElegibilidade"]
    assert set(schema_pedido["required"]) == set(PEDIDO_VALIDO)

    # O exemplo publicado precisa ser aceito pela aplicação de verdade.
    exemplo_pedido = schema_pedido["examples"][0]
    PedidoElegibilidade.model_validate(exemplo_pedido)
    assert TestClient(app).post("/elegibilidades", json=exemplo_pedido).status_code == 202

    # Cada exemplo de resposta precisa bater com o modelo daquela resposta.
    respostas_documentadas = (
        ("/elegibilidades", "post", "202", ElegibilidadeAceita),
        ("/elegibilidades", "post", "422", ErroAPI),
        ("/elegibilidades/{protocolo}", "get", "200", ElegibilidadeAceita),
        ("/elegibilidades/{protocolo}", "get", "404", ErroAPI),
    )
    for caminho, metodo, status, modelo in respostas_documentadas:
        for exemplo in exemplos_da_resposta(contrato, caminho, metodo, status):
            modelo.model_validate(exemplo)


def test_contrato_explicito_e_contrato_gerado_nao_divergem():
    """O contrato publicado e o que a aplicação gera dizem a mesma coisa.

    Este é o teste que pega o erro mais caro do módulo: alguém altera o código,
    o contrato gerado acompanha, e o `openapi.yaml` publicado continua prometendo
    o formato antigo para quem consome. A comparação é pontual de propósito —
    operações, campos obrigatórios e a resposta `202` —, porque comparar os dois
    documentos inteiros quebraria a cada detalhe de formatação.
    """
    explicito = carregar_contrato_explicito()
    gerado = app.openapi()

    for caminho, metodo in (
        ("/elegibilidades", "post"),
        ("/elegibilidades/{protocolo}", "get"),
    ):
        assert metodo in explicito["paths"][caminho]
        assert metodo in gerado["paths"][caminho]

    campos_obrigatorios_explicito = set(
        explicito["components"]["schemas"]["PedidoElegibilidade"]["required"]
    )
    campos_obrigatorios_gerado = set(
        gerado["components"]["schemas"]["PedidoElegibilidade"]["required"]
    )
    assert campos_obrigatorios_gerado == campos_obrigatorios_explicito

    aceito_explicito = explicito["paths"]["/elegibilidades"]["post"]["responses"]["202"]
    aceito_gerado = gerado["paths"]["/elegibilidades"]["post"]["responses"]["202"]
    assert aceito_gerado["description"] == aceito_explicito["description"]
    assert aceito_gerado["headers"]["Location"] == aceito_explicito["headers"]["Location"]
