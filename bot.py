import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router



async def main():
    bot = Bot(token='8081181890:AAEDN5HkDqAo-v0a6W83fzmRPf2_IJzNfL0')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)



if __name__=='__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот Выключен')
