from dataclasses import dataclass, field
from typing import List
import uuid
from datetime import datetime
from .produto import Produto

@dataclass
class Pedido:
    """
    Representa um Pedido.
    Arquitetura: Composição (Pedido contém Produtos), cálculo automático de preço total.
    """
    produtos: List[Produto] = field(default_factory=list)
    data: datetime = field(default_factory=datetime.now)
    codigo: str = None
    preco_total: float = 0.0

    def __post_init__(self):
        if self.codigo is None:
            self.codigo = str(uuid.uuid4())
        self.calcular_preco_total()

    def adicionar_produto(self, produto: Produto):
        self.produtos.append(produto)
        self.calcular_preco_total()

    def remover_produto(self, codigo_produto: str):
        self.produtos = [p for p in self.produtos if p.codigo != codigo_produto]
        self.calcular_preco_total()

    def calcular_preco_total(self):
        self.preco_total = sum(produto.preco for produto in self.produtos)

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "data": self.data.isoformat(),
            "produtos": [p.to_dict() for p in self.produtos],
            "preco_total": self.preco_total
        }

    @classmethod
    def from_dict(cls, data):
        produtos = [Produto.from_dict(p) for p in data.get("produtos", [])]
        data_obj = datetime.fromisoformat(data.get("data")) if data.get("data") else datetime.now()
        return cls(
            codigo=data.get("codigo"),
            data=data_obj,
            produtos=produtos,
            preco_total=data.get("preco_total", 0.0)
        )
