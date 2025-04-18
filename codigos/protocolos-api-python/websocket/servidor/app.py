from fastapi import FastAPI, WebSocket
import sys
import os
from modelo_dominio.produto import Produto
from modelo_dominio.pedido import Pedido
from modelo_dominio.repositorio import RepositorioProduto, RepositorioPedido

app = FastAPI()
repo_produtos = RepositorioProduto()
repo_pedidos = RepositorioPedido()

def seed():
    p1 = Produto(nome="Notebook", preco=3500.0)
    p2 = Produto(nome="Smartphone", preco=2000.0)
    repo_produtos.adicionar(p1)
    repo_produtos.adicionar(p2)
    ped = Pedido()
    ped.adicionar_produto(p1)
    repo_pedidos.adicionar(ped)
seed()

@app.websocket("/ws/produtos")
async def ws_produtos(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        if data == "listar":
            produtos = [p.to_dict() for p in repo_produtos.listar_todos()]
            await websocket.send_json(produtos)
        else:
            await websocket.send_text("Comando desconhecido")
