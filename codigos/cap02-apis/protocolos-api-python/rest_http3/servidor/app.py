from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from modelo_dominio.produto import Produto
from modelo_dominio.pedido import Pedido
from modelo_dominio.repositorio import RepositorioProduto, RepositorioPedido

"""
Servidor REST/HTTP3 usando FastAPI (simulação HTTP/3)
Aspectos Arquiteturais:
- RESTful, separação de responsabilidades
- FastAPI para performance e tipagem
- CRUD para Produtos e Pedidos
"""

app = FastAPI()
repo_produtos = RepositorioProduto()
repo_pedidos = RepositorioPedido()

# Dados iniciais
def seed():
    p1 = Produto(nome="Notebook", preco=3500.0)
    p2 = Produto(nome="Smartphone", preco=2000.0)
    repo_produtos.adicionar(p1)
    repo_produtos.adicionar(p2)
    ped = Pedido()
    ped.adicionar_produto(p1)
    repo_pedidos.adicionar(ped)

seed()

class ProdutoIn(BaseModel):
    nome: str
    preco: float

class PedidoIn(BaseModel):
    produtos: List[str] = []

@app.get("/api/produtos")
def listar_produtos():
    return [p.to_dict() for p in repo_produtos.listar_todos()]

@app.get("/api/produtos/{codigo}")
def obter_produto(codigo: str):
    prod = repo_produtos.obter_por_id(codigo)
    if prod:
        return prod.to_dict()
    raise HTTPException(status_code=404, detail="Produto não encontrado")

@app.post("/api/produtos", status_code=201)
def adicionar_produto(prod: ProdutoIn):
    novo = Produto(nome=prod.nome, preco=prod.preco)
    repo_produtos.adicionar(novo)
    return novo.to_dict()

@app.put("/api/produtos/{codigo}")
def atualizar_produto(codigo: str, prod: ProdutoIn):
    novo = Produto(codigo=codigo, nome=prod.nome, preco=prod.preco)
    if repo_produtos.atualizar(codigo, novo):
        return novo.to_dict()
    raise HTTPException(status_code=404, detail="Produto não encontrado")

@app.delete("/api/produtos/{codigo}", status_code=204)
def remover_produto(codigo: str):
    if repo_produtos.remover(codigo):
        return
    raise HTTPException(status_code=404, detail="Produto não encontrado")

@app.get("/api/pedidos")
def listar_pedidos():
    return [p.to_dict() for p in repo_pedidos.listar_todos()]

@app.get("/api/pedidos/{codigo}")
def obter_pedido(codigo: str):
    ped = repo_pedidos.obter_por_id(codigo)
    if ped:
        return ped.to_dict()
    raise HTTPException(status_code=404, detail="Pedido não encontrado")

@app.post("/api/pedidos", status_code=201)
def criar_pedido(ped: PedidoIn):
    novo = Pedido()
    for cod in ped.produtos:
        prod = repo_produtos.obter_por_id(cod)
        if prod:
            novo.adicionar_produto(prod)
    repo_pedidos.adicionar(novo)
    return novo.to_dict()

@app.post("/api/pedidos/{codigo}/produtos")
def adicionar_produto_pedido(codigo: str, dados: dict):
    ped = repo_pedidos.obter_por_id(codigo)
    if not ped:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    prod = repo_produtos.obter_por_id(dados.get("codigo_produto"))
    if not prod:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    ped.adicionar_produto(prod)
    repo_pedidos.atualizar(codigo, ped)
    return ped.to_dict()

@app.delete("/api/pedidos/{codigo}/produtos/{codigo_produto}", status_code=204)
def remover_produto_pedido(codigo: str, codigo_produto: str):
    ped = repo_pedidos.obter_por_id(codigo)
    if not ped:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    ped.remover_produto(codigo_produto)
    repo_pedidos.atualizar(codigo, ped)
