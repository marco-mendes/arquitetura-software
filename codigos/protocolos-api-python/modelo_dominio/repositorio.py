from typing import Dict, List, Optional, TypeVar, Generic
from .produto import Produto
from .pedido import Pedido

T = TypeVar('T')

class Repositorio(Generic[T]):
    """
    Repositório genérico em memória.
    Arquitetura: Padrão Repository, uso de generics para reutilização.
    """
    def __init__(self):
        self._items: Dict[str, T] = {}

    def adicionar(self, item: T) -> T:
        self._items[item.codigo] = item
        return item

    def obter_por_id(self, codigo: str) -> Optional[T]:
        return self._items.get(codigo)

    def listar_todos(self) -> List[T]:
        return list(self._items.values())

    def atualizar(self, codigo: str, item: T) -> Optional[T]:
        if codigo in self._items:
            self._items[codigo] = item
            return item
        return None

    def remover(self, codigo: str) -> bool:
        return self._items.pop(codigo, None) is not None

class RepositorioProduto(Repositorio[Produto]):
    def buscar_por_nome(self, nome: str) -> List[Produto]:
        nome_lower = nome.lower()
        return [p for p in self.listar_todos() if nome_lower in p.nome.lower()]

class RepositorioPedido(Repositorio[Pedido]):
    def calcular_valor_total_pedidos(self) -> float:
        return sum(pedido.preco_total for pedido in self.listar_todos())
