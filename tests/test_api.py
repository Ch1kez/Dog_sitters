# tests/test_api.py

import pytest
import requests
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"  # Убедитесь, что ваше приложение запущено на этом URL

@pytest.fixture(scope="module")
def setup_db():
    # Тестирование базы данных
    pass

def test_create_order(setup_db):
    # Подготовка данных для создания заказа
    future_time = datetime.utcnow() + timedelta(hours=2)  # Пример времени через 2 часа
    payload = {
        "apartment_number": 101,
        "pet_name": "Buddy",
        "breed": "Labrador",
        "walk_time": future_time.isoformat(),
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
    assert data["walk_time"] == payload["walk_time"]
    assert data["duration_minutes"] == payload["duration_minutes"]

def test_get_orders():
    # Определите дату для запроса
    date = (datetime.utcnow() + timedelta(days=1)).date().isoformat()

    response = requests.get(f"{BASE_URL}/orders/{date}")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Убедитесь, что ответ - это список

    # Проверка, что данные в ответе корректны
    if data:
        assert "id" in data[0]
        assert "apartment_number" in data[0]
        assert "pet_name" in data[0]
        assert "breed" in data[0]
        assert "walk_time" in data[0]
        assert "duration_minutes" in data[0]
