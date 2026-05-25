"""Plugin de notificação — simula envio de e-mail sem infraestrutura real."""

from dominio import Fatura, ResultadoEmissao


class NotificacaoEmailPlugin:
    """Simula o envio de e-mail de confirmação de fatura."""

    nome = "Notificação-Email"

    def processar(self, fatura: Fatura, resultado: ResultadoEmissao) -> ResultadoEmissao:
        mensagem = (
            f"Fatura #{fatura.id} emitida para {fatura.cliente.nome}. "
            f"Total: R${resultado.valor_total:,.2f}"
        )
        print(f"  [Email → {fatura.cliente.email}] {mensagem}")
        resultado.notificacoes_enviadas.append(f"email:{fatura.cliente.email}")
        return resultado
