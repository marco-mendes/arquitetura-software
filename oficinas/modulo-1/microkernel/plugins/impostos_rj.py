"""Regra tributária do Rio de Janeiro. Acrescentar um estado é acrescentar um arquivo."""

from dominio import Fatura
from nucleo import Plugin

ALIQUOTA_ICMS = 0.20


class IcmsRJ(Plugin):
    nome = "ICMS-RJ"
    categoria = "impostos"

    def aplica_se(self, fatura: Fatura) -> bool:
        return fatura.estado == "RJ"

    def executar(self, fatura: Fatura) -> None:
        base = sum(i.total for i in fatura.itens if i.categoria == "eletronico")
        if base:
            fatura.ajustes.append(("ICMS-RJ", base * ALIQUOTA_ICMS))
