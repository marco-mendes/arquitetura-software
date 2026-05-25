"""
Demonstração completa — Estilo Pipes and Filters
Pipeline de Triagem de Currículos para vaga de Engenheiro Backend

Execução: python main.py
Sem dependências externas — apenas stdlib Python 3.10+
"""

from dominio import Vaga
from framework import Pipeline
from filtros.producer import LeitorDeCurriculos
from filtros.testers import (
    ValidadorDeCurriculo,
    FiltroPorExperienciaMinima,
    FiltroPorPretensaoSalarial,
)
from filtros.transformers import NormalizadorDeCampos, CalculadorDeScore
from filtros.consumer import RelatorioDeTriagem


CURRICULOS_BRUTOS = [
    {
        "id": 1, "candidato_nome": "  ana lima  ", "email": "ana@mail.com",
        "anos_experiencia": 5, "habilidades": ["Python", "PostgreSQL", "Docker", "REST", "Django"],
        "pretensao_salarial": 14_000.0, "cidade": "São Paulo",
    },
    {
        "id": 2, "candidato_nome": "Bruno Rocha", "email": "bruno@mail.com",
        "anos_experiencia": 1, "habilidades": ["Python", "MySQL"],
        "pretensao_salarial": 8_000.0, "cidade": "Campinas",
    },
    {
        "id": 3, "candidato_nome": "", "email": "invalido@mail.com",
        "anos_experiencia": 4, "habilidades": ["Java"],
        "pretensao_salarial": 12_000.0, "cidade": "Curitiba",
    },
    {
        "id": 4, "candidato_nome": "Clara Mendes", "email": "clara@mail.com",
        "anos_experiencia": 4, "habilidades": ["Python", "REST", "Docker"],
        "pretensao_salarial": 22_000.0, "cidade": "Belo Horizonte",
    },
    {
        "id": 5, "candidato_nome": "Diego Faria", "email": "diego@mail.com",
        "anos_experiencia": 6, "habilidades": ["Python", "PostgreSQL", "REST", "Kubernetes"],
        "pretensao_salarial": 16_000.0, "cidade": "São Paulo",
    },
    {
        "id": 6, "candidato_nome": "Elena Souza", "email": "elena@mail.com",
        "anos_experiencia": 3, "habilidades": ["Python", "Docker", "REST", "PostgreSQL"],
        "pretensao_salarial": 12_000.0, "cidade": "Recife",
    },
]


def main():
    print("=" * 60)
    print("  PIPELINE DE TRIAGEM DE CURRÍCULOS")
    print("  Demonstração — Estilo Pipes and Filters")
    print("=" * 60)

    vaga = Vaga(
        id=1,
        titulo="Engenheiro(a) de Software Backend",
        experiencia_minima=3,
        habilidades_requeridas=["Python", "PostgreSQL", "Docker", "REST"],
        salario_maximo=18_000.0,
    )

    print(f"\nVaga: {vaga.titulo}")
    print(f"Requisitos: ≥{vaga.experiencia_minima} anos | "
          f"Orçamento: R${vaga.salario_maximo:,.0f}")
    print(f"Habilidades: {', '.join(vaga.habilidades_requeridas)}")
    print(f"\nProcessando {len(CURRICULOS_BRUTOS)} currículos...\n")

    pipeline = (
        Pipeline()
        .adicionar(LeitorDeCurriculos(CURRICULOS_BRUTOS))
        .adicionar(ValidadorDeCurriculo())
        .adicionar(NormalizadorDeCampos())
        .adicionar(FiltroPorExperienciaMinima(vaga))
        .adicionar(FiltroPorPretensaoSalarial(vaga))
        .adicionar(CalculadorDeScore(vaga))
        .adicionar(RelatorioDeTriagem())
    )

    print(f"Pipeline: {pipeline}\n")
    aprovados = pipeline.executar(None)
    print(f"\n  → {len(aprovados)} candidato(s) encaminhado(s) para entrevista.")


if __name__ == "__main__":
    main()
