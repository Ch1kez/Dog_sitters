import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
DB_NAME = os.getenv("DB_NAME", "Dog_sitters")  # Укажите имя базы данных


async def create_database_and_tables():
    # Создаем подключение к серверу PostgreSQL
    conn = await asyncpg.connect(user='admin', password='qwerty', database='postgres', host='localhost', port=5432)

    # Проверка существования базы данных
    db_exists = await conn.fetchval(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}'")

    # Создание базы данных, если она не существует
    if not db_exists:
        await conn.execute(f"CREATE DATABASE {DB_NAME}")

    # Закрываем соединение
    await conn.close()

    # Подключаемся к новой базе данных и создаем таблицы
    conn = await asyncpg.connect(DATABASE_URL)

    # Определение SQL-запросов для создания таблиц
    create_table_query = """
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        apartment_number INTEGER NOT NULL,
        pet_name VARCHAR(255) NOT NULL,
        breed VARCHAR(255) NOT NULL,
        walk_time TIMESTAMPTZ NOT NULL,
        duration_minutes INTEGER NOT NULL
    );
    """

    try:
        await conn.execute(create_table_query)
        print("Database and tables created successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await conn.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(create_database_and_tables())
