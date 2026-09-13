"""Notificação: a última categoria, por isso enxerga o total já fechado."""

from dominio import Fatura
from nucleo import Plugin


class NotificacaoEmail(Plugin):
    nome = "Notificação-Email"
    categoria = "notificacao"

    def executar(self, fatura: Fatura) -> None:
        print(
            f"  [Email → {fatura.email}] Fatura #{fatura.numero} emitida para "
            f"{fatura.cliente}. Total: R${fatura.total:,.2f}"
        )
