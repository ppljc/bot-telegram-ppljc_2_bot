# Python модули
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage


# Локальные модули
from config import BOT_TOKEN


# Основные объекты для взаимодействия
def_props = DefaultBotProperties(
    parse_mode='HTML',
    link_preview_is_disabled=True
)

bot = Bot(
    token=BOT_TOKEN,
    default=def_props
)

dp = Dispatcher(
    storage=MemoryStorage()
)
