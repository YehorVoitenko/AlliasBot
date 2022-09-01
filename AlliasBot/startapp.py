import asyncio
import aioschedule

from Allias.managers.telegram_manager import bot


# TODO: Fix txt files data

async def scheduler():
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def main():
    await asyncio.gather(bot.infinity_polling(), scheduler())


if __name__ == "__main__":
    asyncio.run(main())
