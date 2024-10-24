# websocket_server.py

import asyncio
import websockets
import json

connected_clients = set()

async def handler(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            # Broadcast the message to all connected clients
            for client in connected_clients:
                if client != websocket:  # Don't send the message back to the sender
                    await client.send(message)
    finally:
        connected_clients.remove(websocket)

start_server = websockets.serve(handler, "127.0.0.1", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
