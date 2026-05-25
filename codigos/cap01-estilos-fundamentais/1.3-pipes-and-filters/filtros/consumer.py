"""Consumer — destino final do pipeline."""

from framework import Filtro
from dominio import ResultadoTriagem


class RelatorioDeTriagem(Filtro):
    """
    Consumer: exibe o relatório ordenado por score e retorna os aprovados.
    Ponto de saída do pipeline.
    """

    def processar(self, resultados: list[ResultadoTriagem]) -> list[ResultadoTriagem]:
        aprovados = sorted(
            [r for r in resultados if r.aprovado],
            key=lambda r: r.score,
            reverse=True,
        )

        print(f"\n{'═' * 60}")
        print(f"  TRIAGEM CONCLUÍDA — {len(aprovados)} candidato(s) aprovado(s)")
        print(f"{'═' * 60}")
        for i, r in enumerate(aprovados, 1):
            bar = "█" * int(r.score * 10) + "░" * (10 - int(r.score * 10))
            print(f"\n  {i}. {r.curriculo.candidato_nome}")
            print(f"     Score: {bar} {r.score * 100:.0f}%")
            print(f"     Habilidades compatíveis: {', '.join(r.habilidades_compativeis) or '—'}")
            print(f"     Experiência: {r.curriculo.anos_experiencia} ano(s) | "
                  f"Pretensão: R${r.curriculo.pretensao_salarial:,.0f}")
            print(f"     Cidade: {r.curriculo.cidade}")

        return aprovados
