import grpc
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
import grpc_api.protos.produto_pb2 as produto_pb2
import grpc_api.protos.produto_pb2_grpc as produto_pb2_grpc
import grpc_api.protos.pedido_pb2 as pedido_pb2
import grpc_api.protos.pedido_pb2_grpc as pedido_pb2_grpc


def listar_produtos(stub):
    resposta = stub.ListarProdutos(produto_pb2.ProdutoVazio())
    print("Produtos:")
    for p in resposta.produtos:
        print(f"- {p.codigo}: {p.nome} - R$ {p.preco}")
    print("-")

def listar_pedidos(stub):
    resposta = stub.ListarPedidos(pedido_pb2.PedidoVazio())
    print("Pedidos:")
    for ped in resposta.pedidos:
        print(f"- {ped.codigo}: {ped.data} - R$ {ped.preco_total}")
        for prod in ped.produtos:
            print(f"    > {prod.nome} (R$ {prod.preco})")
    print("-")

def demonstracao():
    channel = grpc.insecure_channel('localhost:6000')
    produto_stub = produto_pb2_grpc.ProdutoServiceStub(channel)
    pedido_stub = pedido_pb2_grpc.PedidoServiceStub(channel)
    listar_produtos(produto_stub)
    listar_pedidos(pedido_stub)

if __name__ == "__main__":
    demonstracao()
