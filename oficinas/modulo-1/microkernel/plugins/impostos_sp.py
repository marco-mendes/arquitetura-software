"""Regras tributárias de São Paulo, isoladas num arquivo só."""

from dominio import Fatura
from nucleo import Plugin

ALIQUOTA_ICMS = 0.18
ALIQUOTA_ISS = 0.05


class IcmsSP(Plugin):
    nome = "ICMS-SP"
    categoria = "impostos"

    def aplica_se(self, fatura: Fatura) -> bool:
        return fatura.estado == "SP"

    def executar(self, fatura: Fatura) -> None:
        base = sum(i.total for i in fatura.itens if i.categoria == "eletronico")
        if base:
            fatura.ajustes.append(("ICMS-SP", base * ALIQUOTA_ICMS))


class IssSP(Plugin):
    nome = "ISS-SP"
    categoria = "impostos"

    def aplica_se(self, fatura: Fatura) -> bool:
        return fatura.estado == "SP"

    def executar(self, fatura: Fatura) -> None:
        base = sum(i.total for i in fatura.itens if i.categoria == "servico")
        if base:
            fatura.ajustes.append(("ISS-SP", base * ALIQUOTA_ISS))
