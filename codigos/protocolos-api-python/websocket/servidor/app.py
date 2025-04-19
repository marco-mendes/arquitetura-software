# /Users/marco.mendes/code/arquitetura-software/codigos/protocolos-api-python/websocket/servidor/app.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import sys
import os
# Adiciona o diretório pai ao sys.path para encontrar modelo_dominio
# Isso pode não ser ideal para produção, considere estruturas de pacotes melhores
# ou instalação do seu módulo.
# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(os.path.dirname(current_dir))
# sys.path.append(parent_dir)

from modelo_dominio.produto import Produto
from modelo_dominio.pedido import Pedido
from modelo_dominio.repositorio import RepositorioProduto, RepositorioPedido

app = FastAPI()
repo_produtos = RepositorioProduto()
repo_pedidos = RepositorioPedido()

def seed():
    # Verifica se os repositórios já têm dados para evitar duplicatas ao recarregar
    if not repo_produtos.listar_todos():
        print("Populando repositório de produtos...")
        p1 = Produto(nome="Notebook", preco=3500.0)
        p2 = Produto(nome="Smartphone", preco=2000.0)
        repo_produtos.adicionar(p1)
        repo_produtos.adicionar(p2)
        print("Produtos adicionados.")

    if not repo_pedidos.listar_todos():
        print("Populando repositório de pedidos...")
        # Garante que o produto exista antes de adicionar ao pedido
        produtos_encontrados = repo_produtos.buscar_por_nome("Notebook") # Retorna uma lista
        # Verifica se a lista não está vazia
        if produtos_encontrados:
            ped = Pedido()
            # Pega o PRIMEIRO produto encontrado na lista
            produto_notebook = produtos_encontrados[0]
            ped.adicionar_produto(produto_notebook) # Agora passa um objeto Produto
            repo_pedidos.adicionar(ped)
            print("Pedido adicionado.")
        else:
            print("Produto 'Notebook' não encontrado para adicionar ao pedido inicial.")

seed()

@app.websocket("/ws/produtos")
async def ws_produtos(websocket: WebSocket):
    await websocket.accept()
    client_host = websocket.client.host
    client_port = websocket.client.port
    print(f"Cliente conectado: {client_host}:{client_port}")
    try:
        while True:
            # Espera por uma mensagem do cliente
            data = await websocket.receive_text()
            print(f"Mensagem recebida de {client_host}:{client_port}: {data}")

            if data == "listar":
                produtos = [p.to_dict() for p in repo_produtos.listar_todos()]
                await websocket.send_json(produtos)
                print(f"Lista de produtos enviada para {client_host}:{client_port}.")
            # Adicione aqui outros comandos se necessário
            # elif data == "outro_comando":
            #    await websocket.send_text("Processando outro comando...")
            else:
                await websocket.send_text(f"Comando '{data}' desconhecido")
                print(f"Comando desconhecido recebido de {client_host}:{client_port}: {data}")

    except WebSocketDisconnect:
        # Esta exceção é levantada quando o cliente fecha a conexão
        print(f"Cliente {client_host}:{client_port} desconectado.")
        # Nenhuma ação adicional necessária aqui, a menos que você precise limpar
        # recursos específicos associados a esta conexão.

    except Exception as e:
        # Captura qualquer outra exceção inesperada durante a comunicação
        print(f"Erro inesperado com o cliente {client_host}:{client_port}: {e}")
        # Tenta fechar a conexão de forma limpa se ainda estiver aberta
        try:
            await websocket.close(code=1011) # Código para Internal Server Error
        except RuntimeError:
            # A conexão pode já estar fechada ou em um estado inválido
            print(f"Não foi possível fechar a conexão com {client_host}:{client_port}, pode já estar fechada.")
            pass
    finally:
        # Este bloco é sempre executado, garantindo que a mensagem final seja impressa
        print(f"Encerrando manipulador para a conexão de {client_host}:{client_port}.")

