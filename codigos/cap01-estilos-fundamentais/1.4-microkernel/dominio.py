"""
Domínio — Sistema de Faturamento Multi-Estado
Objetos de dados simples: Fatura, Cliente, ItemFatura, ResultadoEmissao.
"""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class ItemFatura:
    descricao: str
    quantidade: int
    valor_unitario: float
    categoria: str   # "eletronico" | "servico" | "mobiliario" | etc.

    @property
    def subtotal(self) -> float:
        return round(self.quantidade * self.valor_unitario, 2)


@dataclass
class Cliente:
    id: int
    nome: str
    cnpj: str
    estado: str   # "SP" | "RJ" | "MG" | etc.
    tipo: str     # "pj" | "pf"
    email: str


@dataclass
class Fatura:
    id: int
    cliente: Cliente
    itens: list[ItemFatura]

    @property
    def valor_bruto(self) -> float:
        return round(sum(item.subtotal for item in self.itens), 2)


@dataclass
class ResultadoEmissao:
    fatura_id: int
    valor_bruto: float
    impostos: dict[str, float] = field(default_factory=dict)
    frete: float = 0.0
    notificacoes_enviadas: list[str] = field(default_factory=list)

    @property
    def total_impostos(self) -> float:
        return round(sum(self.impostos.values()), 2)

    @property
    def valor_total(self) -> float:
        return round(self.valor_bruto + self.total_impostos + self.frete, 2)
