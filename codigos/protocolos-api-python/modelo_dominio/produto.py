from dataclasses import dataclass
import uuid

@dataclass
class Produto:
    """
    Representa um Produto.
    Arquitetura: Uso de dataclass para simplificar e garantir imutabilidade parcial.
    """
    nome: str
    preco: float
    codigo: str = None

    def __post_init__(self):
        if self.codigo is None:
            self.codigo = str(uuid.uuid4())

    def to_dict(self):
        return {"codigo": self.codigo, "nome": self.nome, "preco": self.preco}

    @classmethod
    def from_dict(cls, data):
        return cls(
            codigo=data.get("codigo"),
            nome=data.get("nome"),
            preco=data.get("preco")
        )
