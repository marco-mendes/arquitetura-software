"""Plugin de cálculo de frete por estado de destino."""

from dominio import Fatura, ResultadoEmissao


class FreteCorrespondenciaPlugin:
    """Frete calculado por estado — tabela fixa sem infraestrutura externa."""

    nome = "Frete-Padrão"

    TABELA = {
        "SP": 15.00,
        "RJ": 22.00,
        "MG": 25.00,
        "RS": 35.00,
        "BA": 40.00,
    }
    FRETE_PADRAO = 50.00
    ISENCAO_ACIMA_DE = 5_000.00   # frete grátis para faturas acima desse valor

    def processar(self, fatura: Fatura, resultado: ResultadoEmissao) -> ResultadoEmissao:
        if resultado.valor_bruto >= self.ISENCAO_ACIMA_DE:
            resultado.frete = 0.0
            return resultado

        resultado.frete = self.TABELA.get(fatura.cliente.estado, self.FRETE_PADRAO)
        return resultado
