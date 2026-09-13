"""Registra os plugins e processa três faturas de estados diferentes."""

from dominio import Fatura, Item
from nucleo import Nucleo, Registro
from plugins.frete import FretePadrao
from plugins.impostos_rj import IcmsRJ
from plugins.impostos_sp import IcmsSP, IssSP
from plugins.notificacao import NotificacaoEmail


def imprimir_cabecalho(fatura: Fatura, titulo: str) -> None:
    print("\n" + "─" * 60)
    print(f"  FATURA #{fatura.numero} — {titulo}")
    print("─" * 60)
    print(f"  Cliente: {fatura.cliente} ({fatura.estado})")
    print("  Itens:")
    for item in fatura.itens:
        print(
            f"    • {item.descricao}: {item.quantidade}× R${item.preco_unitario:,.2f} "
            f"= R${item.total:,.2f} [{item.categoria}]"
        )
    print(f"  Valor bruto: R${fatura.valor_bruto:,.2f}")


def main() -> None:
    linha = "=" * 60
    print(linha)
    print("  SISTEMA DE FATURAMENTO MULTI-ESTADO")
    print("  Demonstração — Estilo MicroKernel")
    print(linha)

    print("\nRegistrando plugins...")
    registro = Registro()
    for plugin in (IcmsSP(), IssSP(), IcmsRJ(), FretePadrao(), NotificacaoEmail()):
        registro.registrar(plugin)
    print(f"\nPlugins ativos: {registro.ativos()}")

    nucleo = Nucleo(registro)

    faturas = [
        (
            "São Paulo",
            Fatura(1001, "TechCorp Ltda", "SP", "financeiro@techcorp.com", [
                Item("Notebook Dell", 2, 5000.0, "eletronico"),
                Item("Suporte Técnico", 10, 200.0, "servico"),
            ]),
        ),
        (
            "Rio de Janeiro",
            Fatura(1002, "Cariocode SA", "RJ", "contas@cariocode.com", [
                Item("Servidor Rack", 1, 9000.0, "eletronico"),
            ]),
        ),
        (
            "São Paulo, acima da faixa de frete",
            Fatura(1003, "Indústria Paulista", "SP", "fiscal@indpaulista.com", [
                Item("Estação de trabalho", 4, 4000.0, "eletronico"),
            ]),
        ),
    ]

    for titulo, fatura in faturas:
        imprimir_cabecalho(fatura, titulo)
        nucleo.processar(fatura)
        for nome, valor in fatura.ajustes:
            print(f"  {nome}: R${valor:,.2f}")
        print(f"  TOTAL: R${fatura.total:,.2f}")


if __name__ == "__main__":
    main()
