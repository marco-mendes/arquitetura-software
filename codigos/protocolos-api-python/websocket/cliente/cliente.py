import asyncio
import websockets
import json

URL = "ws://localhost:7001/ws/produtos"

async def listar_produtos():
    async with websockets.connect(URL) as ws:
        await ws.send("listar")
        resposta = await ws.recv()
        try:
            produtos = json.loads(resposta)
            print("Produtos:")
            for p in produtos:
                print(p)
        except Exception:
            print(resposta)

if __name__ == "__main__":
    asyncio.run(listar_produtos())
