# Python модули
from dotenv import load_dotenv

import os


# Чтение переменных окружения из .env файла
load_dotenv(override=True)

BOT_TOKEN = os.environ['BOT_TOKEN']
