import inspect

from hospital.estilos import comparar_estilos


def test_comparador_expoe_o_contrato_publico_do_modulo():
    assinatura = inspect.signature(comparar_estilos)

    assert assinatura.parameters["cenario"].annotation is dict
    assert assinatura.return_annotation == list[dict]


def test_alternativas_explicam_forcas_limites_e_evidencias():
    alternativas = comparar_estilos(
        {
            "dominio": "agenda hospitalar",
            "prioridades": ["modificabilidade"],
        }
    )

    assert alternativas
    for alternativa in alternativas:
        assert alternativa["estilo"]
        assert alternativa["forcas"]
        assert alternativa["limites"]
        assert alternativa["evidencias"]


def test_mudar_prioridade_altera_primeira_alternativa_e_justificativa():
    por_modificabilidade = comparar_estilos(
        {"prioridades": ["modificabilidade"]}
    )
    por_throughput = comparar_estilos({"prioridades": ["throughput"]})

    assert por_modificabilidade[0]["estilo"] != por_throughput[0]["estilo"]
    assert (
        por_modificabilidade[0]["evidencias"]
        != por_throughput[0]["evidencias"]
    )
