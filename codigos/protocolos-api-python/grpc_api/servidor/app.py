import grpc
from concurrent import futures
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from modelo_dominio.produto import Produto
from modelo_dominio.pedido import Pedido
from modelo_dominio.repositorio import RepositorioProduto, RepositorioPedido
# Importar os módulos gerados pelo protoc após compilação dos protos
import grpc_api.protos.produto_pb2 as produto_pb2
import grpc_api.protos.produto_pb2_grpc as produto_pb2_grpc
import grpc_api.protos.pedido_pb2 as pedido_pb2
import grpc_api.protos.pedido_pb2_grpc as pedido_pb2_grpc

class ProdutoService(produto_pb2_grpc.ProdutoServiceServicer):
    def __init__(self, repo_produtos):
        self.repo_produtos = repo_produtos
    def ListarProdutos(self, request, context):
        produtos = self.repo_produtos.listar_todos()
        return produto_pb2.ListaProdutos(produtos=[produto_pb2.Produto(**p.to_dict()) for p in produtos])
    def ObterProduto(self, request, context):
        prod = self.repo_produtos.obter_por_id(request.codigo)
        if prod:
            return produto_pb2.Produto(**prod.to_dict())
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Produto não encontrado')
        return produto_pb2.Produto()

class PedidoService(pedido_pb2_grpc.PedidoServiceServicer):
    def __init__(self, repo_pedidos):
        self.repo_pedidos = repo_pedidos
    def ListarPedidos(self, request, context):
        pedidos = self.repo_pedidos.listar_todos()
        return pedido_pb2.ListaPedidos(pedidos=[pedido_pb2.Pedido(
            codigo=p.codigo,
            data=p.data.isoformat(),
            preco_total=p.preco_total,
            produtos=[produto_pb2.Produto(**prod.to_dict()) for prod in p.produtos]
        ) for p in pedidos])
    def ObterPedido(self, request, context):
        ped = self.repo_pedidos.obter_por_id(request.codigo)
        if ped:
            return pedido_pb2.Pedido(
                codigo=ped.codigo,
                data=ped.data.isoformat(),
                preco_total=ped.preco_total,
                produtos=[produto_pb2.Produto(**prod.to_dict()) for prod in ped.produtos]
            )
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Pedido não encontrado')
        return pedido_pb2.Pedido()

def serve():
    repo_produtos = RepositorioProduto()
    repo_pedidos = RepositorioPedido()
    # Dados iniciais
    p1 = Produto(nome="Notebook", preco=3500.0)
    p2 = Produto(nome="Smartphone", preco=2000.0)
    repo_produtos.adicionar(p1)
    repo_produtos.adicionar(p2)
    ped = Pedido()
    ped.adicionar_produto(p1)
    repo_pedidos.adicionar(ped)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    produto_pb2_grpc.add_ProdutoServiceServicer_to_server(ProdutoService(repo_produtos), server)
    pedido_pb2_grpc.add_PedidoServiceServicer_to_server(PedidoService(repo_pedidos), server)
    server.add_insecure_port('[::]:6000')
    print('Servidor gRPC rodando na porta 6000...')
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
