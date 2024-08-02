
import asyncpg
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Чтение параметров подключения из переменных окружения
DB_NAME = os.getenv("DB_NAME")

async def get_db():
    # Устанавливаем соединение с базой данных
    return await asyncpg.connect(user='admin', password='qwerty', database=DB_NAME, host='localhost',
                                     port=5432)

async def close_db(connection):
    # Закрываем соединение с базой данных
    await connection.close()
