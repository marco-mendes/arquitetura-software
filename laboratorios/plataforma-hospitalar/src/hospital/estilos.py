"""Comparação didática de estilos para o primeiro laboratório."""

_ESTILOS = (
    {
        "estilo": "microkernel",
        "forcas": ("modificabilidade", "extensibilidade", "isolamento de extensões"),
        "limites": (
            "o contrato do núcleo exige estabilidade",
            "plugins incompatíveis aumentam o esforço de testes",
        ),
        "evidencias": {
            "modificabilidade": "medir se uma nova regra entra como plugin sem alterar o núcleo",
            "extensibilidade": "contar quantas extensões são adicionadas pelo contrato existente",
            "isolamento de extensões": "executar a suíte com um plugin desabilitado",
        },
    },
    {
        "estilo": "monólito modular",
        "forcas": ("modificabilidade", "consistência", "simplicidade operacional"),
        "limites": (
            "todos os módulos compartilham o mesmo processo",
            "fronteiras sem testes podem se degradar em acoplamento",
        ),
        "evidencias": {
            "modificabilidade": "verificar por teste que a mudança fica restrita a um módulo",
            "consistência": "executar um teste transacional entre módulos",
            "simplicidade operacional": "registrar uma única unidade de implantação",
        },
    },
    {
        "estilo": "camadas",
        "forcas": ("modificabilidade", "testabilidade", "separação de responsabilidades"),
        "limites": (
            "atalhos entre camadas produzem dependências ocultas",
            "travessias repetidas podem adicionar latência",
        ),
        "evidencias": {
            "modificabilidade": "trocar um adaptador e executar os testes da aplicação",
            "testabilidade": "testar a regra de negócio sem banco ou interface",
            "separação de responsabilidades": "inspecionar dependências entre pacotes",
        },
    },
    {
        "estilo": "pipes and filters",
        "forcas": ("throughput", "composição", "processamento incremental"),
        "limites": (
            "o formato entre filtros precisa ser estável",
            "diagnosticar uma falha distribuída pelo fluxo exige correlação",
        ),
        "evidencias": {
            "throughput": "medir itens processados por segundo com lotes representativos",
            "composição": "reordenar filtros independentes e repetir os testes",
            "processamento incremental": "observar cada etapa produzir saída consumível",
        },
    },
)


def comparar_estilos(cenario: dict) -> list[dict]:
    """Filtra e ordena alternativas pelas prioridades declaradas no cenário.

    A função é deliberadamente pequena: a tabela torna as hipóteses visíveis e
    evita apresentar a comparação como uma decisão automática.
    """

    prioridades = tuple(
        str(prioridade).strip().casefold()
        for prioridade in cenario.get("prioridades", ())
        if str(prioridade).strip()
    )
    candidatos: list[tuple[int, int, dict]] = []

    for ordem, definicao in enumerate(_ESTILOS):
        forcas = tuple(forca.casefold() for forca in definicao["forcas"])
        correspondencias = tuple(
            prioridade for prioridade in prioridades if prioridade in forcas
        )
        if prioridades and not correspondencias:
            continue
        evidencias = (
            [definicao["evidencias"][prioridade] for prioridade in correspondencias]
            if correspondencias
            else ["selecionar uma prioridade mensurável antes de decidir"]
        )
        alternativa = {
            "estilo": definicao["estilo"],
            "forcas": list(definicao["forcas"]),
            "limites": list(definicao["limites"]),
            "evidencias": evidencias,
        }
        candidatos.append((len(correspondencias), ordem, alternativa))

    candidatos.sort(key=lambda item: (-item[0], item[1]))
    return [alternativa for _, _, alternativa in candidatos]
