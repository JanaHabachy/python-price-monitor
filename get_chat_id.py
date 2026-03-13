import asyncio
from telegram import Bot

TOKEN = "8755719581:AAEubJ7IHYqsyybgZqHwinAvK6GuOnf_2mc"  # BotFather token

async def main():
    bot = Bot(token=TOKEN)
    updates = await bot.get_updates()
    print(updates)  # look for chat.id in the output

asyncio.run(main())