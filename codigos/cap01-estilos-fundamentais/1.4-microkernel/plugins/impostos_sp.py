"""Plugins de impostos para São Paulo — ICMS e ISS."""

from dominio import Fatura, ResultadoEmissao


class ImpostoSPPlugin:
    """ICMS paulista com alíquotas diferenciadas por categoria de produto."""

    nome = "ICMS-SP"

    ALIQUOTAS = {
        "eletronico": 0.12,
        "servico":    0.05,
        "alimentacao": 0.07,
    }
    ALIQUOTA_PADRAO = 0.18

    def processar(self, fatura: Fatura, resultado: ResultadoEmissao) -> ResultadoEmissao:
        if fatura.cliente.estado != "SP":
            return resultado

        icms = sum(
            item.subtotal * self.ALIQUOTAS.get(item.categoria, self.ALIQUOTA_PADRAO)
            for item in fatura.itens
        )
        resultado.impostos[self.nome] = round(icms, 2)
        return resultado


class ISSSPPlugin:
    """ISS paulista — aplica apenas a itens de serviço."""

    nome = "ISS-SP"
    ALIQUOTA = 0.05

    def processar(self, fatura: Fatura, resultado: ResultadoEmissao) -> ResultadoEmissao:
        if fatura.cliente.estado != "SP":
            return resultado

        iss = sum(
            item.subtotal * self.ALIQUOTA
            for item in fatura.itens
            if item.categoria == "servico"
        )
        if iss > 0:
            resultado.impostos[self.nome] = round(iss, 2)
        return resultado
