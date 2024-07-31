# Python модули
from aiogram import Router
from aiogram.types import *


# Локальные модули
from utilities.logger import logger


# Переменные
router = Router(name='client')


# Функции
@router.message()
async def message_any(message: Message):
    try:
        await message.reply(text='Я вас не понимаю!')

        logger.info(f'USER={message.from_user.id}, MESSAGE="unknown: {message.text}"')
    except Exception as e:
        logger.error(f'USER={message.from_user.id}, MESSAGE="{e}"')


@router.callback_query()
async def callback_any(query: CallbackQuery):
    try:
        await query.answer(text='Такой кнопки пока нет!', show_alert=True)

        logger.info(f'USER={query.from_user.id}, MESSAGE="unknown: {query.data}"')
    except Exception as e:
        logger.error(f'USER={query.from_user.id}, MESSAGE="{e}"')
