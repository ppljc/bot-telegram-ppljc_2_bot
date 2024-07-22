# <---------- Python modules ---------->
import time
import requests
import os

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup


# <---------- Variables ---------->
filename = 'parser.py'


# <---------- Secondary functions ---------->
def scroll_down(driver: webdriver, scrolls: int) -> None:
    """
    Scrolls the page down to load.
    :param driver: Webdriver
    :param scrolls: Number of scrolls
    :return:
    """
    for i in range(scrolls):
        driver.execute_script(f"window.scrollTo({i*1000}, {(i+1)*1000});")
        time.sleep(2)


# <---------- Main functions---------->
def get_htmlCode(link: str) -> str:
    """
    Gets the HTML code of a page at a given URL.
    :param link: URL
    :return: HTML code
    """
    edge_options = Options()
    # edge_options.add_argument('--headless')
    driver = webdriver.Edge(options=edge_options)
    driver.get(link)
    time.sleep(2)
    scroll_down(driver, scrolls=15)
    html_code = driver.page_source
    driver.quit()
    return html_code


def parse_htmlCode(html_code: str, name: str, class_: str):
    """
    Selection of the necessary parts from a given HTML code.
    :param html_code: HTML code
    :param name: HTML tag name
    :param class_: HTML tag class
    :return: Required code snippet
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


def get_products(category: int, keyword: str, amount: int, without: list = []):
    current_card = 1
    current_page = 1
    products = []
    while current_card <= amount:
        link = f'https://www.wildberries.ru/catalog/0/search.aspx?page={current_page}&sort=popular&search={keyword}&ssubject={category}'

        html_code = get_htmlCode(link=link)
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

        end = False

        for product in html_products:
            id = int(product['data-nm-id'])
            name = product.find('span', 'product-card__name').text[3:]
            price = int(product.find('ins', 'price__lower-price').text.replace(' ', '').replace('₽', '').replace(' ', ''))
            link_photos = product.find('img', 'j-thumbnail')['src']

            if id in without:
                continue

            link_photo = '/'.join(link_photos.split('/')[:6]) + f'/images/big/1.webp'
            path_photos = f'C:/Users/tony_/PycharmProjects/bot-telegram_wildberries-parser/images'
            path_photo = f'{path_photos}/{id}.webp'
            if not os.path.exists(path_photos):
                os.makedirs(path_photos)
            position_photo = requests.get(
                url=link_photo,
                stream=True
            )
            with open(path_photo, 'wb') as file:
                for chunk in position_photo.iter_content(chunk_size=8192):
                    file.write(chunk)

            products.append({
                'name': name,
                'price': price,
                'id': id
            })

            if current_card >= amount:
                end = True
                break
            current_card += 1

        if end:
            break
        current_page += 1
