import asyncio
import websockets
import json

ip = "ws://10.83.131.155:9090"

async def connect_and_subscribe():
    async with websockets.connect(ip) as ws:
        subscribe_msg = {
            "op": "subscribe",
            "topic": "/mirwebapp/web_path"
        }
        await ws.send(json.dumps(subscribe_msg))  # ✅ Uso de 'await'

        while True:
            mensagem = await ws.recv()  # ✅ Uso de 'await'
            print(f"📩 Mensagem recebida: {mensagem}")
            data = json.loads(mensagem)

            if "msg" in data:
                caminho = data["msg"]
                wsData = [{"x": x, "y": y} for x, y in zip(caminho["x"], caminho["y"])]
                print(f"🔄 Caminho atualizado: {wsData}")

# Executa a função assíncrona
asyncio.run(connect_and_subscribe())
