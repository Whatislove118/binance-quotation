import asyncio
from ast import operator

from aiogram import Bot, Dispatcher, types

from .config import Config

bot = Bot(token=Config.TELEGRAM_API_TOKEN)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=["start"])
async def connect_user(message: types.Message):
    chat_id = message.chat.id
    if chat_id in Config.CHAT_SET:
        await message.reply("You are already connected")
    Config.CHAT_SET.add(chat_id)
    await message.reply("Welcome in Binance Notifier app.")


@dispatcher.message_handler(commands=["stop"])
async def disconnect_user(message: types.Message):
    chat_id = message.chat.id
    Config.CHAT_SET.discard(chat_id)
    await message.reply("See you soon")


async def send_message(chat_id, message):
    await bot.send_message(chat_id, message)


async def send_message_to_users(message):
    for chat_id in Config.CHAT_SET.copy():
        await send_message(chat_id, message)
        await asyncio.sleep(3)
