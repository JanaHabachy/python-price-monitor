import asyncio
import os
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def send_async(message):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)


def send_telegram(message):
    try:
        asyncio.run(send_async(message))
        print("Telegram message sent.")
    except Exception as e:
        print(f"Telegram notification failed: {e}")