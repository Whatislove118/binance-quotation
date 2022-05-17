import asyncio

from aiogram import executor

from core.bot import dispatcher
from core.config import Config
from core.ws import consume

if __name__ == "__main__":
    Config.init_streams()
    loop = asyncio.get_event_loop()
    loop.create_task(consume())
    executor.start_polling(dispatcher, skip_updates=True, loop=loop)
