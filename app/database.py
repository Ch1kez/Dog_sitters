
import asyncpg
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Чтение параметров подключения из переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL")

async def get_db():
    # Устанавливаем соединение с базой данных
    return await asyncpg.connect(DATABASE_URL)

async def close_db(connection):
    # Закрываем соединение с базой данных
    await connection.close()
