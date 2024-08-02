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
    global TIME_ORDER
    # Подготовка данных для создания заказа
    # Определим время через 2 часа, округленное до ближайших получаса или целого часа
    current_time = datetime.utcnow()
    future_time = current_time + timedelta(hours=2)
    minute = 0 if future_time.minute < 30 else 30
    future_time = future_time.replace(minute=minute, second=0, microsecond=0)

    # Убедимся, что время в пределах 07:00 и 23:00
    if future_time.hour < 7:
        future_time = future_time.replace(hour=7, minute=0)
    elif future_time.hour == 23 and future_time.minute > 0:
        future_time = future_time.replace(hour=22, minute=30)

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
    assert "id" in data
    assert data["apartment_number"] == payload["apartment_number"]
    assert data["pet_name"] == payload["pet_name"]
    assert data["breed"] == payload["breed"]
    assert data["walk_time"] == payload["walk_time"]
    assert data["duration_minutes"] == payload["duration_minutes"]

def test_get_orders(setup_db):
    # Определите дату для запроса
    date = datetime.today().date().isoformat()

    response = requests.get(f"{BASE_URL}/orders/{date}")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Убедитесь, что ответ - это список

    # Проверка, что данные в ответе корректны
    for order in data:
        assert "id" in order
        assert "apartment_number" in order
        assert "pet_name" in order
        assert "breed" in order
        assert "walk_time" in order
        assert "duration_minutes" in order

        walk_time = datetime.fromisoformat(order["walk_time"].replace("Z", "+00:00"))
        assert walk_time.hour >= 7 and (walk_time.hour < 23 or (walk_time.hour == 23 and walk_time.minute == 0))
        assert order["duration_minutes"] == 30
        assert walk_time.minute in [0, 30]  # Проверка, что прогулка начинается либо в начале часа, либо в половину

        # Дополнительные проверки можно добавить при необходимости
