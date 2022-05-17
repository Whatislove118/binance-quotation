import asyncio

from core.config import Config
from core.ws import consume

if __name__ == "__main__":
    Config.init_streams()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume())
    loop.run_forever()
