# Python модули
import asyncio

# Локальные модули
from create_bot import bot, dp


# Функции при запуске и выключении бота
async def onstartup():
    bot_user = await bot.get_me()
    print(f'{bot_user.full_name} [@{bot_user.username}] up and running | 🌄')


async def onshutdown():
    print('Shutting down... | 💤')


# Функция запуска бота
async def main():
    dp.startup.register(onstartup)
    dp.shutdown.register(onshutdown)

    dp.include_routers(

    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# Запуск бота
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        asyncio.run(bot.session.close())
