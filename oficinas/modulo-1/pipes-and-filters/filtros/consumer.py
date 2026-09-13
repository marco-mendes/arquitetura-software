"""Consumidor: o fim do fluxo, onde o resultado vira relatório."""

from dominio import Curriculo
from framework import Filtro


class RelatorioDeTriagem(Filtro):
    def __init__(self) -> None:
        self.aprovados: list[Curriculo] = []

    def processar(self, item: Curriculo) -> Curriculo | None:
        self.aprovados.append(item)
        return item

    def imprimir(self) -> None:
        linha = "═" * 60
        print(f"\n{linha}")
        print(f"  TRIAGEM CONCLUÍDA — {len(self.aprovados)} candidato(s) aprovado(s)")
        print(linha)
        for posicao, item in enumerate(sorted(self.aprovados, key=lambda c: -c.score), 1):
            barras = "█" * (item.score // 10)
            print(f"\n  {posicao}. {item.nome}")
            print(f"     Score: {barras:<10} {item.score}%")
            print(f"     Habilidades compatíveis: {', '.join(item.compativeis)}")
            print(f"     Experiência: {item.anos_experiencia} ano(s) | Pretensão: R${item.pretensao:,}")
            print(f"     Cidade: {item.cidade}")
