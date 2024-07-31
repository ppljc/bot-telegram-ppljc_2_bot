# Python модули
import asyncio

# Локальные модули
from create_bot import bot, dp
from handlers import client
from utilities.logger import logger


# Функции при запуске и выключении бота
async def onstartup():
    bot_user = await bot.get_me()
    logger.info(f'BOT_NAME="{bot_user.full_name}", BOT_USERNAME="{bot_user.username}", MESSAGE="up and running..."')


async def onshutdown():
    bot_user = await bot.get_me()
    logger.info(f'BOT_NAME="{bot_user.full_name}", BOT_USERNAME="{bot_user.username}", MESSAGE="shutting down..."')


# Функция запуска бота
async def main():
    dp.startup.register(onstartup)
    dp.shutdown.register(onshutdown)

    dp.include_routers(
        client.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# Запуск бота
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        asyncio.run(bot.session.close())
