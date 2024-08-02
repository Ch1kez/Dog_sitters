# tests/test_api.py

import pytest
import requests
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"  # Убедитесь, что ваше приложение запущено на этом URL

@pytest.fixture(scope="module")
def setup_db():
    # Настройка базы данных перед тестами, если необходимо
    pass

def test_create_order(setup_db):
    # Подготовка данных для создания заказа
    future_time = datetime.utcnow() + timedelta(hours=2)  # Пример времени через 2 часа
    payload = {
        "apartment_number": 101,
        "pet_name": "Buddy",
        "breed": "Labrador",
        "walk_time": future_time.isoformat(),  # Преобразование datetime в ISO 8601
        "duration_minutes": 30
    }

    response = requests.post(f"{BASE_URL}/orders", json=payload)

    assert response.status_code == 200
    data = response.json()
    print(data)
    assert "id" in data
    assert data["apartment_number"] == payload["apartment_number"]
    assert data["pet_name"] == payload["pet_name"]
    assert data["breed"] == payload["breed"]
    # Проверка соответствия времени, преобразование к строке формата ISO 8601 для сравнения
    assert data["walk_time"] == payload["walk_time"]
    assert data["duration_minutes"] == payload["duration_minutes"]

def test_get_orders(setup_db):
    # Определите дату для запроса
    date = (datetime.utcnow() + timedelta(days=1)).date().isoformat()

    response = requests.get(f"{BASE_URL}/orders/{date}")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Убедитесь, что ответ - это список

    # Проверка, что данные в ответе корректны
    if data:
        order = data[0]
        assert "id" in order
        assert "apartment_number" in order
        assert "pet_name" in order
        assert "breed" in order
        assert "walk_time" in order
        assert "duration_minutes" in order

        # Дополнительная проверка значений (если необходимо)
        # Например, можно проверять, что время прогулки находится в пределах допустимого диапазона
        walk_time = datetime.fromisoformat(order["walk_time"])
        assert walk_time.hour >= 7 and walk_time.hour <= 23
