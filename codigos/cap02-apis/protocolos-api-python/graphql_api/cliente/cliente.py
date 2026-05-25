import httpx
import json

URL = "http://localhost:9000/"

QUERY_LISTAR_PRODUTOS = '{ produtos { codigo nome preco } }'
MUTATION_CRIAR_PRODUTO = 'mutation($input: ProdutoInput!) { criarProduto(input: $input) { codigo nome preco } }'

headers = {"Content-Type": "application/json"}

def graphql_query(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    resp = httpx.post(URL, json=payload, headers=headers)
    print(f"Status: {resp.status_code}")
    try:
        print(json.dumps(resp.json(), indent=2))
    except Exception:
        print(resp.text)
    print("-" * 40)
    return resp.json()

def demonstracao():
    print("=== Demonstração GraphQL ===")
    graphql_query(QUERY_LISTAR_PRODUTOS)
    graphql_query(MUTATION_CRIAR_PRODUTO, {"input": {"nome": "Mouse", "preco": 99.9}})
    graphql_query(QUERY_LISTAR_PRODUTOS)
    print("=== Fim ===")

if __name__ == "__main__":
    demonstracao()
