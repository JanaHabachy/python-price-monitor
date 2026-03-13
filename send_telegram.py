import asyncio
from telegram import Bot

TOKEN = "8755719581:AAEubJ7IHYqsyybgZqHwinAvK6GuOnf_2mc"
CHAT_ID = 1096499420

async def send_async(message):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)


def send_telegram(message):
    asyncio.run(send_async(message))