# Python модули
import time
import urllib.parse
import math

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup


# Локальные модули
from utilities.logger import logger


# Переменные
filename = 'parser.py'


# Вспомогательные функции
def scroll_down(driver: webdriver, scrolls: int) -> None:
    """
    Прокручивает страницу вниз, чтобы прогрузить все позиции.
    :param driver: Webdriver
    :param scrolls: Количество прокруток (умножается на 1000 пикселей)
    :return:
    """
    for i in range(scrolls):
        driver.execute_script(f"window.scrollTo({i*1000}, {(i+1)*1000});")
        time.sleep(2)


# Основные функции
def get_htmlCode(link: str, amount: int = 60) -> str:
    """
    Получает HTML-код страницы по заданной ссылке.
    :param link: Ссылка
    :param amount:
    :return: HTML-код
    """
    try:
        edge_options = Options()
        edge_options.add_argument('--headless')
        edge_options.add_argument('--remote-debugging-port=0')
        driver = webdriver.Edge(options=edge_options)
        driver.get(link)
        time.sleep(2)
        scrolls = math.ceil(amount / 4)
        scroll_down(driver, scrolls=scrolls)
        html_code = driver.page_source
        driver.quit()
        return html_code
    except Exception as e:
        print(f'Ошибка {e}')


def parse_htmlCode(html_code: str, name: str, class_: str):
    """
    Выбор необходимых частей HTML-кода.
    :param html_code: HTML-код
    :param name: HTML-тэг
    :param class_: HTML-класс
    :return: Все отрывки кода, подходящие по заданным параметрам
    """
    soup = BeautifulSoup(
        markup=html_code,
        features='html.parser'
    )
    soup_code = soup.find_all(
        name=name,
        class_=class_
    )
    return soup_code


def get_products(keyword: str, amount: int, sort: str = 'popular',  without: list = []) -> list[dict]:
    """
    Получает список товаров по заданным параметрам.
    :param keyword: Ключевое слово
    :param amount: Количество товаров
    :param sort: Параметр, по которому происходит сортировка товара
    :param without: Список товаров (id), которые не нужно добавлять
    :return: Список товаров (имя, цена, id)
    """
    current_card = 1
    current_page = 1
    products = []

    while current_card <= amount:
        content = urllib.parse.urlencode({'page': current_page, 'sort': sort, 'search': keyword})
        link = f'https://www.wildberries.ru/catalog/0/search.aspx?{content}'

        html_code = get_htmlCode(
            link=link,
            amount=amount
        )
        html_products = parse_htmlCode(
            html_code=html_code,
            name='article',
            class_='product-card j-card-item product-card--adv'
        )
        if not html_products:
            html_products = parse_htmlCode(
                html_code=html_code,
                name='article',
                class_='product-card j-card-item'
            )

        if html_products:
            products_len = len(html_products)
        else:
            products_len = 0
        logger.debug(f'USER=BOT, MESSAGE="html_products={products_len}"')

        end = False

        for product in html_products:
            id = int(product['data-nm-id'])
            name = product.find('span', 'product-card__name').text[3:]
            price = int(product.find('ins', 'price__lower-price').text.replace(' ', '').replace('₽', '').replace(' ', ''))
            link_photos = product.find('img', 'j-thumbnail')['src']

            if id in without:
                continue

            link_photo = '/'.join(link_photos.split('/')[:6]) + f'/images/big/1.webp'

            products.append({
                'name': name,
                'price': price,
                'id': id,
                'photo': link_photo
            })

            if current_card >= amount:
                end = True
                break
            current_card += 1

        if end:
            break
        current_page += 1

    return products
