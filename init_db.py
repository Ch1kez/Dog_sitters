
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv("DB_NAME", "Dog_sitters")  # Укажите имя базы данных

async def create_database_and_tables():
    # Создаем подключение к серверу PostgreSQL
    try:
        conn = await asyncpg.connect(user='admin', password='qwerty', database='postgres', host='localhost',
                                     port=5432)
    except Exception as e:
        raise Exception(f"Failed to connect to PostgreSQL server: {e}")

    # Проверка существования базы данных
    db_exists = await conn.fetchval(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}'")

    # Создание базы данных, если она не существует
    if not db_exists:
        try:
            await conn.execute(f"CREATE DATABASE {DB_NAME} IF NOT EXISTS ")
            print(f"Database {DB_NAME} created successfully.")
        except Exception as e:
            print(f"Failed to create database: {e}")
            return

    # Закрываем соединение
    await conn.close()

    try:
        conn = await asyncpg.connect(user='admin', password='qwerty', database=DB_NAME, host='localhost',
                                     port=5432)
    except Exception as e:
        raise Exception(f"Failed to connect to PostgreSQL server: {e}")

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
    await conn.execute(create_table_query)


if __name__ == "__main__":
    import asyncio
    asyncio.run(create_database_and_tables())
