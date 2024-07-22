# Python модули
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage


# Локальные модули
import config


# Основные объекты для взаимодействия
def_props = DefaultBotProperties(
    parse_mode='HTML',
)

bot = Bot(
    token=config.TOKEN,
    default=def_props
)

dp = Dispatcher(
    storage=MemoryStorage()
)
