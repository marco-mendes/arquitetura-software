"""O vocabulário compartilhado entre núcleo e plugins."""

from dataclasses import dataclass, field


@dataclass
class Item:
    descricao: str
    quantidade: int
    preco_unitario: float
    categoria: str

    @property
    def total(self) -> float:
        return self.quantidade * self.preco_unitario


@dataclass
class Fatura:
    numero: int
    cliente: str
    estado: str
    email: str
    itens: list[Item] = field(default_factory=list)
    ajustes: list[tuple[str, float]] = field(default_factory=list)

    @property
    def valor_bruto(self) -> float:
        return sum(item.total for item in self.itens)

    @property
    def total(self) -> float:
        return self.valor_bruto + sum(valor for _, valor in self.ajustes)
