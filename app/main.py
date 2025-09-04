import asyncio
import logging

from app.bot import dp, bot

from app.handlers import start, help, favorites, jokes

async def main():
    routers = [
        start.router,
        help.router,
        jokes.router,
        favorites.router

    ]

    for router in routers:
        dp.include_router(router)

    await dp.start_polling(bot)

def cli():
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

if __name__ == "__main__":
    cli()
