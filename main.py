import asyncio

from core.bot import dispatcher
from core.config import Config
from core.ws import consume


async def main():
    Config.init_streams()
    await asyncio.gather(
        consume(),
        dispatcher.start_polling(),
    )


if __name__ == "__main__":
    asyncio.run(main())
