import asyncio
import websockets

async def test():
    uri = "wss://echo.websocket.org"
    # Desativar compressão explicitamente
    async with websockets.connect(uri, compression=None) as websocket:
        await websocket.send("Olá, servidor!")
        response = await websocket.recv()
        print(f"Resposta do servidor: {response}")

asyncio.run(test())
