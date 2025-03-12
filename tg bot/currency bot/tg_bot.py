# модули
import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router

import logging # модуль для тестов 

from settings import TOKEN # добавить ключ

bot = Bot(token=TOKEN)
dp = Dispatcher()

# подключение
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')