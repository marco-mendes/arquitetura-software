"""
Demonstração completa — Estilo MicroKernel
Sistema de Faturamento Multi-Estado

Execução: python main.py
Sem dependências externas — apenas stdlib Python 3.10+
"""

from dominio import Cliente, Fatura, ItemFatura
from nucleo import CoreFaturamento
from plugins.impostos_sp import ImpostoSPPlugin, ISSSPPlugin
from plugins.impostos_rj import ImpostoRJPlugin
from plugins.frete import FreteCorrespondenciaPlugin
from plugins.notificacao import NotificacaoEmailPlugin


def imprimir_resultado(titulo: str, fatura: Fatura, core: CoreFaturamento) -> None:
    print(f"\n{'─' * 60}")
    print(f"  {titulo}")
    print(f"{'─' * 60}")
    print(f"  Cliente: {fatura.cliente.nome} ({fatura.cliente.estado})")
    print(f"  Itens:")
    for item in fatura.itens:
        print(f"    • {item.descricao}: {item.quantidade}× R${item.valor_unitario:,.2f}"
              f" = R${item.subtotal:,.2f} [{item.categoria}]")
    print(f"  Valor bruto: R${fatura.valor_bruto:,.2f}")

    resultado = core.emitir(fatura)

    print(f"\n  Resultado da emissão:")
    for nome, valor in resultado.impostos.items():
        print(f"    {nome}: R${valor:,.2f}")
    print(f"    Frete: R${resultado.frete:,.2f}")
    print(f"    ─────────────────────────────")
    print(f"    TOTAL: R${resultado.valor_total:,.2f}")
    if resultado.notificacoes_enviadas:
        print(f"    Notificações: {', '.join(resultado.notificacoes_enviadas)}")


def main():
    print("=" * 60)
    print("  SISTEMA DE FATURAMENTO MULTI-ESTADO")
    print("  Demonstração — Estilo MicroKernel")
    print("=" * 60)

    # ── Configuração do núcleo ─────────────────────────────────
    core = CoreFaturamento()

    print("\nRegistrando plugins...")
    core.registrar_plugin("impostos",    ImpostoSPPlugin())
    core.registrar_plugin("impostos",    ISSSPPlugin())
    core.registrar_plugin("impostos",    ImpostoRJPlugin())
    core.registrar_plugin("frete",       FreteCorrespondenciaPlugin())
    core.registrar_plugin("notificacao", NotificacaoEmailPlugin())

    print(f"\nPlugins ativos: {core.status_plugins()}")

    # ── Fatura 1 — Cliente SP com eletrônicos e serviço ───────
    cliente_sp = Cliente(
        id=1, nome="TechCorp Ltda", cnpj="12.345.678/0001-90",
        estado="SP", tipo="pj", email="financeiro@techcorp.com",
    )
    fatura_sp = Fatura(
        id=1001, cliente=cliente_sp, itens=[
            ItemFatura("Notebook Dell",    2, 5_000.0, "eletronico"),
            ItemFatura("Suporte Técnico", 10,   200.0, "servico"),
        ],
    )
    imprimir_resultado("FATURA #1001 — São Paulo", fatura_sp, core)

    # ── Fatura 2 — Cliente RJ ──────────────────────────────────
    cliente_rj = Cliente(
        id=2, nome="Distribuidora Rio", cnpj="98.765.432/0001-10",
        estado="RJ", tipo="pj", email="nf@distribrj.com",
    )
    fatura_rj = Fatura(
        id=1002, cliente=cliente_rj, itens=[
            ItemFatura("Monitor 4K",         5, 1_200.0, "eletronico"),
            ItemFatura("Cadeira Ergonômica", 3,   800.0, "mobiliario"),
        ],
    )
    imprimir_resultado("FATURA #1002 — Rio de Janeiro", fatura_rj, core)

    # ── Fatura 3 — Frete grátis (valor alto) ──────────────────
    cliente_sp2 = Cliente(
        id=3, nome="InfraCo SA", cnpj="55.666.777/0001-88",
        estado="SP", tipo="pj", email="compras@infraco.com",
    )
    fatura_grande = Fatura(
        id=1003, cliente=cliente_sp2, itens=[
            ItemFatura("Servidor Dell PowerEdge", 3, 25_000.0, "eletronico"),
        ],
    )
    imprimir_resultado("FATURA #1003 — SP (frete grátis acima de R$5k)", fatura_grande, core)

    # ── Extensão sem alterar o núcleo ─────────────────────────
    print(f"\n{'─' * 60}")
    print("  EXTENSÃO: adicionando suporte a MG sem alterar o núcleo")
    print(f"{'─' * 60}")

    class ImpostoMGPlugin:
        nome = "ICMS-MG"
        ALIQUOTA = 0.18

        def processar(self, fatura: Fatura, resultado) -> object:
            if fatura.cliente.estado != "MG":
                return resultado
            resultado.impostos[self.nome] = round(
                resultado.valor_bruto * self.ALIQUOTA, 2
            )
            return resultado

    core.registrar_plugin("impostos", ImpostoMGPlugin())

    cliente_mg = Cliente(
        id=4, nome="Mineração BH", cnpj="11.222.333/0001-44",
        estado="MG", tipo="pj", email="nf@mineracaobh.com",
    )
    fatura_mg = Fatura(
        id=1004, cliente=cliente_mg, itens=[
            ItemFatura("Equipamento Industrial", 1, 45_000.0, "industrial"),
        ],
    )
    imprimir_resultado("FATURA #1004 — Minas Gerais (novo plugin)", fatura_mg, core)


if __name__ == "__main__":
    main()
