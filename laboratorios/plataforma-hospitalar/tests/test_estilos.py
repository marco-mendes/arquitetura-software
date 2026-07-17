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


def test_prioridades_distintivas_selecionam_estilos_e_evidencias_exatos():
    por_modificabilidade = comparar_estilos(
        {"prioridades": ["modificabilidade", "extensibilidade"]}
    )
    por_fluxo = comparar_estilos(
        {"prioridades": ["throughput", "processamento incremental"]}
    )

    assert por_modificabilidade[0]["estilo"] == "microkernel"
    assert por_modificabilidade[0]["forcas"][:2] == [
        "modificabilidade",
        "extensibilidade",
    ]
    assert por_modificabilidade[0]["evidencias"] == [
        "medir se uma nova regra entra como plugin sem alterar o núcleo",
        "contar quantas extensões são adicionadas pelo contrato existente",
    ]
    assert por_fluxo[0]["estilo"] == "pipes and filters"
    assert por_fluxo[0]["forcas"] == [
        "throughput",
        "composição",
        "processamento incremental",
    ]
    assert por_fluxo[0]["evidencias"] == [
        "medir itens processados por segundo com lotes representativos",
        "observar cada etapa produzir saída consumível",
    ]
