import asyncio
import json
import websockets

URI = "ws://localhost:8000/ws"

async def receive(ws):
    try:
        while True:
            msg = await ws.recv()
            print("RECEIVED:", msg)
    except websockets.ConnectionClosed:
        print("Server closed connection")

async def send(ws):
    try:
        while True:
            msg = await asyncio.to_thread(input)
            await ws.send(json.dumps({"message": msg}))
    except websockets.ConnectionClosed:
        print("Disconnected")

async def chat():
    async with websockets.connect(URI, ping_interval=20) as ws:
        try:
            username = await asyncio.to_thread(input, "username: ")
            topic = await asyncio.to_thread(input, "topic: ")

            await ws.send(json.dumps({
                "username": username.strip(),
                "topic": topic.strip()
            }))
        except websockets.ConnectionClosed:
            print("Disconnected")

        print("Connected to chat")

        await asyncio.gather(
            receive(ws),
            send(ws)
        )

asyncio.run(chat())
