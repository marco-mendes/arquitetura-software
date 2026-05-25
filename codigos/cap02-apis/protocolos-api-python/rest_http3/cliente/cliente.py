import httpx
import json
import asyncio
import ssl
import os
from pathlib import Path

# Configuração para HTTP/2
HTTP2_ENABLED = False  # Altere para True para usar HTTP/2 (requer certificados TLS)
BASE_URL = "https://localhost:4433/api" if HTTP2_ENABLED else "http://localhost:8000/api"

async def fazer_requisicao_http2(metodo, url, **kwargs):
    """Faz uma requisição usando HTTP/2 via httpx"""
    # Configuração para ignorar verificação de certificado (apenas para testes)
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    # Configuração para HTTP/2
    async with httpx.AsyncClient(http2=True, verify=False) as client:
        if metodo.lower() == "get":
            return await client.get(url, **kwargs)
        elif metodo.lower() == "post":
            return await client.post(url, **kwargs)
        elif metodo.lower() == "put":
            return await client.put(url, **kwargs)
        elif metodo.lower() == "delete":
            return await client.delete(url, **kwargs)

async def fazer_requisicao_http(metodo, url, **kwargs):
    """Faz uma requisição HTTP normal usando httpx"""
    async with httpx.AsyncClient() as client:
        if metodo.lower() == "get":
            return await client.get(url, **kwargs)
        elif metodo.lower() == "post":
            return await client.post(url, **kwargs)
        elif metodo.lower() == "put":
            return await client.put(url, **kwargs)
        elif metodo.lower() == "delete":
            return await client.delete(url, **kwargs)

async def fazer_requisicao(metodo, url, **kwargs):
    """Faz uma requisição usando HTTP/2 ou HTTP/1.1 dependendo da configuração"""
    if HTTP2_ENABLED:
        return await fazer_requisicao_http2(metodo, url, **kwargs)
    else:
        return await fazer_requisicao_http(metodo, url, **kwargs)

def imprimir_resposta(resp):
    print(f"Status: {resp.status_code}")
    print(f"Protocolo: {resp.http_version}")
    try:
        print(json.dumps(resp.json(), indent=2))
    except Exception:
        print(resp.text)
    print("-" * 40)

async def listar_produtos():
    resp = await fazer_requisicao("get", f"{BASE_URL}/produtos")
    imprimir_resposta(resp)
    return resp.json() if resp.status_code == 200 else []

async def adicionar_produto(nome, preco):
    resp = await fazer_requisicao("post", f"{BASE_URL}/produtos", json={"nome": nome, "preco": preco})
    imprimir_resposta(resp)
    return resp.json() if resp.status_code == 201 else None

async def criar_pedido(codigos):
    resp = await fazer_requisicao("post", f"{BASE_URL}/pedidos", json={"produtos": codigos})
    imprimir_resposta(resp)
    return resp.json() if resp.status_code == 201 else None

async def demonstracao():
    print("=== Demonstração REST com HTTP/1.1 (preparação para HTTP/2 e HTTP/3) ===")
    print(f"Usando {'HTTP/2' if HTTP2_ENABLED else 'HTTP/1.1'}")
    produtos = await listar_produtos()
    novo = await adicionar_produto("Teclado", 250)
    produtos = await listar_produtos()
    if produtos:
        await criar_pedido([produtos[0]["codigo"]])
    print("=== Fim ===")

if __name__ == "__main__":
    asyncio.run(demonstracao())
