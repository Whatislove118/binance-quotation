import json
import logging

import websockets

from core.config import Config
from core.stream import Stream


def subscribe_message() -> dict:
    return {
        "method": "SUBSCRIBE",
        "params": [stream.full_name() for stream in Config.STREAM_REGISTRY.values()],
        "id": 1,
    }


logging.basicConfig(level=logging.INFO)


async def handler(websocket):
    async for message in websocket:
        data = json.loads(message)
        # skipping handshake message
        if symbol := data.get("s"):
            stream = Config.STREAM_REGISTRY[symbol]
            is_triggered = stream.compare(float(data.get("c")))

            logging.info(message + "" + str(is_triggered))


async def consume(remote: str = Config.REMOTE_URL):
    async with websockets.connect(remote) as websocket:
        message = json.dumps(subscribe_message())
        await websocket.send(message)
        await handler(websocket)
