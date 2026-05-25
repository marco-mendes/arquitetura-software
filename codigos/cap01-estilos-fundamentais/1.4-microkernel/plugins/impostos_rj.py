"""Plugin de imposto para Rio de Janeiro."""

from dominio import Fatura, ResultadoEmissao


class ImpostoRJPlugin:
    """ICMS fluminense com alíquota única de 20%."""

    nome = "ICMS-RJ"
    ALIQUOTA = 0.20

    def processar(self, fatura: Fatura, resultado: ResultadoEmissao) -> ResultadoEmissao:
        if fatura.cliente.estado != "RJ":
            return resultado

        icms = resultado.valor_bruto * self.ALIQUOTA
        resultado.impostos[self.nome] = round(icms, 2)
        return resultado
