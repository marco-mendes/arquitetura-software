import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from flask import Flask, jsonify, request
from modelo_dominio.produto import Produto
from modelo_dominio.pedido import Pedido
from modelo_dominio.repositorio import RepositorioProduto, RepositorioPedido

"""
Servidor REST/HTTP2 usando Flask
Aspectos Arquiteturais:
- RESTful, separação de responsabilidades
- Uso didático de HTTP/2 (via Hypercorn)
- CRUD para Produtos e Pedidos
"""

app = Flask(__name__)
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

@app.route('/api/produtos', methods=['GET'])
def listar_produtos():
    return jsonify([p.to_dict() for p in repo_produtos.listar_todos()])

@app.route('/api/produtos/<codigo>', methods=['GET'])
def obter_produto(codigo):
    prod = repo_produtos.obter_por_id(codigo)
    if prod:
        return jsonify(prod.to_dict())
    return jsonify({"erro": "Produto não encontrado"}), 404

@app.route('/api/produtos', methods=['POST'])
def adicionar_produto():
    dados = request.json
    prod = Produto(nome=dados.get('nome'), preco=dados.get('preco'))
    repo_produtos.adicionar(prod)
    return jsonify(prod.to_dict()), 201

@app.route('/api/produtos/<codigo>', methods=['PUT'])
def atualizar_produto(codigo):
    dados = request.json
    prod = Produto(codigo=codigo, nome=dados.get('nome'), preco=dados.get('preco'))
    if repo_produtos.atualizar(codigo, prod):
        return jsonify(prod.to_dict())
    return jsonify({"erro": "Produto não encontrado"}), 404

@app.route('/api/produtos/<codigo>', methods=['DELETE'])
def remover_produto(codigo):
    if repo_produtos.remover(codigo):
        return '', 204
    return jsonify({"erro": "Produto não encontrado"}), 404

@app.route('/api/pedidos', methods=['GET'])
def listar_pedidos():
    return jsonify([p.to_dict() for p in repo_pedidos.listar_todos()])

@app.route('/api/pedidos/<codigo>', methods=['GET'])
def obter_pedido(codigo):
    ped = repo_pedidos.obter_por_id(codigo)
    if ped:
        return jsonify(ped.to_dict())
    return jsonify({"erro": "Pedido não encontrado"}), 404

@app.route('/api/pedidos', methods=['POST'])
def criar_pedido():
    dados = request.json
    ped = Pedido()
    for cod in dados.get('produtos', []):
        prod = repo_produtos.obter_por_id(cod)
        if prod:
            ped.adicionar_produto(prod)
    repo_pedidos.adicionar(ped)
    return jsonify(ped.to_dict()), 201

@app.route('/api/pedidos/<codigo>/produtos', methods=['POST'])
def adicionar_produto_pedido(codigo):
    ped = repo_pedidos.obter_por_id(codigo)
    if not ped:
        return jsonify({"erro": "Pedido não encontrado"}), 404
    dados = request.json
    prod = repo_produtos.obter_por_id(dados.get('codigo_produto'))
    if not prod:
        return jsonify({"erro": "Produto não encontrado"}), 404
    ped.adicionar_produto(prod)
    repo_pedidos.atualizar(codigo, ped)
    return jsonify(ped.to_dict())

@app.route('/api/pedidos/<codigo>/produtos/<codigo_produto>', methods=['DELETE'])
def remover_produto_pedido(codigo, codigo_produto):
    ped = repo_pedidos.obter_por_id(codigo)
    if not ped:
        return jsonify({"erro": "Pedido não encontrado"}), 404
    ped.remover_produto(codigo_produto)
    repo_pedidos.atualizar(codigo, ped)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=5000)
