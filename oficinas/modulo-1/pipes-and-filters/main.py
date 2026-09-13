"""Monta o fluxo e o executa. A ordem dos filtros é a arquitetura."""

from dominio import Vaga
from framework import Pipeline
from filtros.consumer import RelatorioDeTriagem
from filtros.producer import LeitorDeCurriculos
from filtros.testers import (
    FiltroPorExperienciaMinima,
    FiltroPorPretensaoSalarial,
    ValidadorDeCurriculo,
)
from filtros.transformers import CalculadorDeScore, NormalizadorDeCampos


def main() -> None:
    vaga = Vaga(
        titulo="Engenheiro(a) de Software Backend",
        anos_minimos=3,
        teto_salarial=18000,
        habilidades=("Python", "PostgreSQL", "Docker", "REST"),
    )

    linha = "=" * 60
    print(linha)
    print("  PIPELINE DE TRIAGEM DE CURRÍCULOS")
    print("  Demonstração — Estilo Pipes and Filters")
    print(linha)
    print(f"\nVaga: {vaga.titulo}")
    print(f"Requisitos: ≥{vaga.anos_minimos} anos | Orçamento: R${vaga.teto_salarial:,}")
    print(f"Habilidades: {', '.join(vaga.habilidades)}")

    relatorio = RelatorioDeTriagem()
    pipeline = (
        Pipeline()
        .adicionar(ValidadorDeCurriculo())
        .adicionar(NormalizadorDeCampos())
        .adicionar(FiltroPorExperienciaMinima(vaga))
        .adicionar(FiltroPorPretensaoSalarial(vaga))
        .adicionar(CalculadorDeScore(vaga))
        .adicionar(relatorio)
    )

    curriculos = LeitorDeCurriculos().ler()
    print(f"\nProcessando {len(curriculos)} currículos...\n")
    print(f"Pipeline: LeitorDeCurriculos → {str(pipeline)[9:-1]}\n")

    pipeline.executar(curriculos)
    relatorio.imprimir()


if __name__ == "__main__":
    main()
