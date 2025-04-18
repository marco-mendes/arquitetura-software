import requests
import json

BASE_URL = "http://localhost:5001/api"

def imprimir_resposta(resp):
    print(f"Status: {resp.status_code}")
    try:
        print(json.dumps(resp.json(), indent=2))
    except Exception:
        print(resp.text)
    print("-" * 40)

def listar_produtos():
    resp = requests.get(f"{BASE_URL}/produtos")
    imprimir_resposta(resp)
    return resp.json() if resp.status_code == 200 else []

def adicionar_produto(nome, preco):
    resp = requests.post(f"{BASE_URL}/produtos", json={"nome": nome, "preco": preco})
    imprimir_resposta(resp)
    return resp.json() if resp.status_code == 201 else None

def criar_pedido(codigos):
    resp = requests.post(f"{BASE_URL}/pedidos", json={"produtos": codigos})
    imprimir_resposta(resp)
    return resp.json() if resp.status_code == 201 else None

def demonstracao():
    print("=== Demonstração REST/HTTP2 ===")
    produtos = listar_produtos()
    novo = adicionar_produto("Monitor", 1200)
    produtos = listar_produtos()
    if produtos:
        criar_pedido([produtos[0]["codigo"]])
    print("=== Fim ===")

if __name__ == "__main__":
    demonstracao()
