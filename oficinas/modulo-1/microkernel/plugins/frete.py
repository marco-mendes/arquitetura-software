"""Frete: outra categoria, executada depois dos impostos."""

from dominio import Fatura
from nucleo import Plugin

FAIXA_ISENCAO = 15000.0
TAXA = 120.0


class FretePadrao(Plugin):
    nome = "Frete-Padrão"
    categoria = "frete"

    def aplica_se(self, fatura: Fatura) -> bool:
        return any(i.categoria == "eletronico" for i in fatura.itens)

    def executar(self, fatura: Fatura) -> None:
        if fatura.valor_bruto >= FAIXA_ISENCAO:
            fatura.ajustes.append(("Frete-Isento", 0.0))
            return
        fatura.ajustes.append(("Frete-Padrão", TAXA))
