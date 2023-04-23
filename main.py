import asyncio

from aiogram.fsm.storage.memory import MemoryStorage

from services.polls import polls_router
from settings import dp, bot
from services.start import start_router
from services.weather import weather_router
from services.exchange import exchange_router
from services.random_pic import random_pic_router

# in the storage variable, we call our storage
storage = MemoryStorage()


# register our routes
async def main() -> None:

    dp.include_router(start_router)
    dp.include_router(weather_router)
    dp.include_router(exchange_router)
    dp.include_router(random_pic_router)
    dp.include_router(polls_router)

    await dp.start_polling(bot, storage=storage)


if __name__ == '__main__':
    asyncio.run(main())
