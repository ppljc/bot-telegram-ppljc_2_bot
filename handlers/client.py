# Python модули
from aiogram import Router, F
from aiogram.types import *
from aiogram.filters import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter


# Локальные модули
from create_bot import bot
from utilities import parser
from utilities.logger import logger


# Переменные
router = Router(name='client')

sort = {
    'popular': 'По популярности',
    'rate': 'По рейтингу',
    'priceup': 'По возрастанию цены',
    'pricedown': 'По убыванию цены',
    'newly': 'По новинкам',
    'benefit': 'Сначала выгодные',
}

view = {
    'view_normal': 'Нормальный вывод',
    'view_reverse': 'Обратный вывод'
}


# Клавиатуры
keyboard_cancel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ Назад', callback_data='search_cancel')]
])

keyboard_search = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Поиск 🔎', callback_data='search')]
])


# Класс
class FSMSearch(StatesGroup):
    first_message = State()
    keyword = State()
    amount = State()
    sort = State()


# Функции
@router.message(Command(commands=['start', 'help'], ignore_case=True))
async def message_start(message: Message):
    try:
        await message.delete()
        await message.answer(
            text=(
                'Привет, я бот для поиска товаров на Wildberries\n'
                'Давай начнём работу ⬇️'
            ),
            reply_markup=keyboard_search
        )

        logger.info(f'USER={message.from_user.id}, MESSAGE=""')
    except Exception as e:
        logger.error(f'USER={message.from_user.id}, MESSAGE="{e}"')


@router.callback_query(F.data == 'search_cancel')
async def callback_cancel(query: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await state.clear()

        await query.answer()
        await query.message.edit_text(
            text='Используй кнопку для начала работы ⬇️',
            reply_markup=keyboard_search
        )

        logger.info(f'USER={query.from_user.id}, MESSAGE=""')
    except Exception as e:
        logger.error(f'USER={query.from_user.id}, MESSAGE="{e}"')


@router.callback_query(F.data == 'search')
async def callback_search(query: CallbackQuery, state: FSMContext):
    try:
        await query.answer()
        await query.message.edit_text(
            text=(
                'Вот список всего, что нам надо указать:\n'
                '1. Ключевое слово (текст)\n'
                '2. Количество позиций\n'
                '3. Метод сортировки\n\n'
                'Для начала укажите, что ищите ⬇️'
            ),
            reply_markup=keyboard_cancel
        )
        await state.update_data(first_message=query.message.message_id)
        await state.set_state(state=FSMSearch.keyword)

        logger.info(f'USER={query.from_user.id}, MESSAGE=""')
    except Exception as e:
        logger.error(f'USER={query.from_user.id}, MESSAGE="{e}"')


@router.message(StateFilter(FSMSearch.keyword))
async def message_keyword(message: Message, state: FSMContext):
    try:
        data = await state.get_data()

        await message.delete()
        await bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=data['first_message'],
            text=(
                'Вот список всего, что нам надо указать:\n'
                f'1. {message.text}\n'
                '2. Количество позиций\n'
                '3. Метод сортировки\n\n'
                'Теперь укажите, сколько позиций хотите получить ⬇️'
            ),
            reply_markup=keyboard_cancel
        )

        await state.update_data(keyword=message.text)
        await state.set_state(state=FSMSearch.amount)

        logger.info(f'USER={message.from_user.id}, MESSAGE=""')
    except Exception as e:
        logger.error(f'USER={message.from_user.id}, MESSAGE="{e}"')


@router.message(StateFilter(FSMSearch.amount))
async def message_amount(message: Message, state: FSMContext):
    try:
        data = await state.get_data()

        reply_markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=sort['popular'], callback_data='popular')],
            [InlineKeyboardButton(text=sort['rate'], callback_data='rate')],
            [InlineKeyboardButton(text=sort['priceup'], callback_data='priceup')],
            [InlineKeyboardButton(text=sort['pricedown'], callback_data='pricedown')],
            [InlineKeyboardButton(text=sort['newly'], callback_data='newly')],
            [InlineKeyboardButton(text=sort['benefit'], callback_data='benefit')],
            [InlineKeyboardButton(text='⬅️ Назад', callback_data='search_cancel')]
        ])

        await message.delete()
        await bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=data['first_message'],
            text=(
                'Вот список всего, что нам надо указать:\n'
                f'1. {data["keyword"]}\n'
                f'2. {message.text}\n'
                '3. Метод сортировки\n\n'
                'Осталось указать метод сортировки ⬇️'
            ),
            reply_markup=reply_markup
        )

        await state.update_data(amount=message.text)
        await state.set_state(state=FSMSearch.sort)

        logger.info(f'USER={message.from_user.id}, MESSAGE=""')
    except Exception as e:
        logger.error(f'USER={message.from_user.id}, MESSAGE="{e}"')


@router.callback_query(StateFilter(FSMSearch.sort))
async def callback_sort(query: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()

        await bot.edit_message_text(
            chat_id=query.from_user.id,
            message_id=data['first_message'],
            text=(
                'Вот наш список аргументов:\n'
                f'1. {data["keyword"]}\n'
                f'2. {data["amount"]}\n'
                f'3. {sort[query.data]}\n\n'
                'Теперь немного подожди, я ищу товары 🔄️'
            ),
        )

        products = parser.get_products(
            keyword=data['keyword'],
            amount=int(data['amount']),
            sort=query.data
        )

        for product in products:
            await bot.send_photo(
                chat_id=query.from_user.id,
                photo=product['photo'],
                caption=(
                    f'Название: <b>{product["name"]}</b>\n'
                    f'Цена: <b>{product["price"]}₽</b>\n'
                    f'Артикул (ссылка): <a href="https://www.wildberries.ru/catalog/{product["id"]}/detail.aspx">{product["id"]}</a>'
                )
            )

        await bot.send_message(
            chat_id=query.from_user.id,
            text='Вот, что мне удалось найти',
            reply_markup=keyboard_cancel
        )

        await state.clear()

        logger.info(f'USER={query.from_user.id}, MESSAGE=""')
    except Exception as e:
        logger.error(f'USER={query.from_user.id}, MESSAGE="{e}"')
